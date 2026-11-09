#!/usr/bin/env python3
"""
💰 GABRIEL COST CONTROLLER
==========================
Budget caps, rate limiting, token tracking, and model fallback.

Features:
- Hard budget caps per run/day/month
- Token limits per agent/model
- Rate limiting with sliding window
- Model fallback chains (Pro → Flash → Offline)
- Cost estimation before execution
"""

import json
import time
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import threading

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
COSTS_DIR = GABRIEL_ROOT / "costs"
COSTS_DIR.mkdir(exist_ok=True)

USAGE_FILE = COSTS_DIR / "usage.json"
LIMITS_FILE = COSTS_DIR / "limits.json"

# =============================================================================
# MODEL PRICING (per 1M tokens, as of Dec 2024)
# =============================================================================

MODEL_PRICING = {
    # Anthropic
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
    
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "o1": {"input": 15.00, "output": 60.00},
    "o1-mini": {"input": 3.00, "output": 12.00},
    "o3-mini": {"input": 1.10, "output": 4.40},
    
    # Google
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-2.0-flash-thinking": {"input": 0.70, "output": 3.50},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    
    # Groq (free tier / very cheap)
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
    "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
    
    # xAI
    "grok-2": {"input": 2.00, "output": 10.00},
    "grok-2-mini": {"input": 0.20, "output": 1.00},
    
    # Local (free)
    "local": {"input": 0.0, "output": 0.0},
    "ollama": {"input": 0.0, "output": 0.0},
}

# =============================================================================
# MODEL FALLBACK CHAINS
# =============================================================================

FALLBACK_CHAINS = {
    # High quality chain
    "quality": [
        "claude-opus-4-20250514",
        "claude-sonnet-4-20250514", 
        "gpt-4o",
        "gemini-1.5-pro",
        "llama-3.3-70b-versatile",
        "local"
    ],
    
    # Fast chain
    "fast": [
        "claude-3-5-haiku-20241022",
        "gpt-4o-mini",
        "gemini-2.0-flash",
        "llama-3.1-8b-instant",
        "local"
    ],
    
    # Cost-effective chain
    "cheap": [
        "gemini-2.0-flash",
        "llama-3.1-8b-instant",
        "gpt-4o-mini",
        "local"
    ],
    
    # Reasoning chain
    "reasoning": [
        "o1",
        "gemini-2.0-flash-thinking",
        "claude-opus-4-20250514",
        "o3-mini",
        "local"
    ],
    
    # Router chain (very cheap)
    "router": [
        "llama-3.1-8b-instant",
        "gemini-2.0-flash",
        "gpt-4o-mini",
        "local"
    ]
}

# =============================================================================
# TYPES
# =============================================================================

@dataclass
class BudgetLimits:
    """Budget configuration."""
    # Per-run limits
    max_tokens_per_run: int = 500_000
    max_cost_cents_per_run: int = 500  # $5
    
    # Daily limits
    max_tokens_per_day: int = 5_000_000
    max_cost_cents_per_day: int = 2000  # $20
    
    # Monthly limits
    max_tokens_per_month: int = 50_000_000
    max_cost_cents_per_month: int = 10000  # $100
    
    # Per-model limits
    model_limits: Dict[str, int] = field(default_factory=dict)  # tokens per day
    
    # Rate limits (requests per minute)
    rate_limits: Dict[str, int] = field(default_factory=lambda: {
        "anthropic": 50,
        "openai": 60,
        "google": 100,
        "groq": 200,
        "xai": 50
    })

@dataclass
class UsageRecord:
    """Usage tracking record."""
    timestamp: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_cents: float
    run_id: Optional[str] = None
    agent: Optional[str] = None

class BudgetExceededError(Exception):
    """Raised when budget limits are exceeded."""
    pass

class RateLimitError(Exception):
    """Raised when rate limit is hit."""
    pass

# =============================================================================
# COST CALCULATOR
# =============================================================================

class CostCalculator:
    """Calculate and estimate costs."""
    
    @staticmethod
    def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost in cents.
        
        Returns:
            Cost in cents (USD)
        """
        pricing = MODEL_PRICING.get(model)
        if not pricing:
            # Unknown model - estimate conservatively
            pricing = {"input": 5.00, "output": 15.00}
        
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return (input_cost + output_cost) * 100  # Convert to cents
    
    @staticmethod
    def estimate_cost(model: str, prompt_length: int, expected_output: int = 1000) -> float:
        """Estimate cost before execution (in cents)."""
        # Rough token estimate: 1 token ≈ 4 chars for English
        input_tokens = prompt_length // 4
        return CostCalculator.calculate_cost(model, input_tokens, expected_output)
    
    @staticmethod
    def get_cheapest_model(models: List[str], min_quality: str = "fast") -> str:
        """Get cheapest model from list that meets quality threshold."""
        chain = FALLBACK_CHAINS.get(min_quality, FALLBACK_CHAINS["fast"])
        
        # Find cheapest model that's in the allowed list
        cheapest = None
        cheapest_cost = float('inf')
        
        for model in models:
            if model in chain:
                pricing = MODEL_PRICING.get(model, {"input": 100, "output": 100})
                cost = pricing["input"] + pricing["output"]
                if cost < cheapest_cost:
                    cheapest = model
                    cheapest_cost = cost
        
        return cheapest or models[0] if models else "local"

# =============================================================================
# RATE LIMITER
# =============================================================================

class RateLimiter:
    """Sliding window rate limiter."""
    
    def __init__(self):
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
    
    def check(self, provider: str, limit: int = 60, window_secs: int = 60) -> bool:
        """
        Check if request is allowed.
        
        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()
        window_start = now - window_secs
        
        with self._lock:
            # Clean old requests
            self._requests[provider] = [t for t in self._requests[provider] if t > window_start]
            
            # Check limit
            if len(self._requests[provider]) >= limit:
                return False
            
            # Record request
            self._requests[provider].append(now)
            return True
    
    def wait_if_needed(self, provider: str, limit: int = 60, window_secs: int = 60) -> float:
        """
        Wait if rate limited.
        
        Returns:
            Seconds waited
        """
        if self.check(provider, limit, window_secs):
            return 0.0
        
        # Calculate wait time
        now = time.time()
        window_start = now - window_secs
        
        with self._lock:
            oldest = min(self._requests[provider])
            wait_time = oldest - window_start + 0.1
        
        if wait_time > 0:
            time.sleep(wait_time)
        
        # Try again
        self._requests[provider].append(time.time())
        return wait_time

# =============================================================================
# USAGE TRACKER
# =============================================================================

class UsageTracker:
    """Track token and cost usage."""
    
    def __init__(self):
        self._usage: List[UsageRecord] = []
        self._load()
    
    def _load(self):
        """Load usage from disk."""
        if USAGE_FILE.exists():
            try:
                data = json.loads(USAGE_FILE.read_text())
                self._usage = [UsageRecord(**r) for r in data.get("records", [])]
            except Exception:
                self._usage = []
    
    def _save(self):
        """Save usage to disk."""
        data = {
            "records": [asdict(r) for r in self._usage],
            "updated": datetime.now().isoformat()
        }
        USAGE_FILE.write_text(json.dumps(data, indent=2))
    
    def record(self, model: str, input_tokens: int, output_tokens: int, 
               run_id: str = None, agent: str = None):
        """Record usage."""
        cost = CostCalculator.calculate_cost(model, input_tokens, output_tokens)
        
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_cents=cost,
            run_id=run_id,
            agent=agent
        )
        
        self._usage.append(record)
        self._save()
    
    def get_usage(self, since: datetime = None) -> Dict[str, Any]:
        """Get usage summary since date."""
        if since is None:
            since = datetime.now() - timedelta(days=30)
        
        since_str = since.isoformat()
        records = [r for r in self._usage if r.timestamp >= since_str]
        
        total_tokens = sum(r.input_tokens + r.output_tokens for r in records)
        total_cost = sum(r.cost_cents for r in records)
        
        by_model = defaultdict(lambda: {"tokens": 0, "cost": 0})
        for r in records:
            by_model[r.model]["tokens"] += r.input_tokens + r.output_tokens
            by_model[r.model]["cost"] += r.cost_cents
        
        return {
            "total_tokens": total_tokens,
            "total_cost_cents": total_cost,
            "record_count": len(records),
            "by_model": dict(by_model),
            "since": since_str
        }
    
    def get_today_usage(self) -> Dict[str, Any]:
        """Get today's usage."""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.get_usage(today)
    
    def get_month_usage(self) -> Dict[str, Any]:
        """Get this month's usage."""
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.get_usage(month_start)

# =============================================================================
# BUDGET CONTROLLER
# =============================================================================

class BudgetController:
    """
    Main budget control interface.
    
    Usage:
        budget = BudgetController()
        
        # Check before making a call
        budget.check_budget("claude-sonnet", 1000, 500)
        
        # Record after call
        budget.record_usage("claude-sonnet", 1000, 500, "run-123")
        
        # Get model with fallback if over budget
        model = budget.get_available_model("quality")
    """
    
    def __init__(self, limits: BudgetLimits = None):
        self.limits = limits or self._load_limits()
        self.tracker = UsageTracker()
        self.rate_limiter = RateLimiter()
        self._run_usage: Dict[str, Dict] = {}  # Track per-run usage
    
    def _load_limits(self) -> BudgetLimits:
        """Load limits from file or use defaults."""
        if LIMITS_FILE.exists():
            try:
                data = json.loads(LIMITS_FILE.read_text())
                return BudgetLimits(**data)
            except Exception:
                pass
        return BudgetLimits()
    
    def save_limits(self):
        """Save current limits to file."""
        LIMITS_FILE.write_text(json.dumps(asdict(self.limits), indent=2))
    
    def check_budget(self, model: str, input_tokens: int, output_tokens: int, 
                     run_id: str = None) -> Tuple[bool, str]:
        """
        Check if usage is within budget.
        
        Returns:
            (allowed, reason)
        """
        estimated_cost = CostCalculator.calculate_cost(model, input_tokens, output_tokens)
        
        # Check run budget
        if run_id:
            run_usage = self._run_usage.get(run_id, {"tokens": 0, "cost": 0})
            new_tokens = run_usage["tokens"] + input_tokens + output_tokens
            new_cost = run_usage["cost"] + estimated_cost
            
            if new_tokens > self.limits.max_tokens_per_run:
                return False, f"Run token limit exceeded ({new_tokens:,} > {self.limits.max_tokens_per_run:,})"
            if new_cost > self.limits.max_cost_cents_per_run:
                return False, f"Run cost limit exceeded (${new_cost/100:.2f} > ${self.limits.max_cost_cents_per_run/100:.2f})"
        
        # Check daily budget
        today = self.tracker.get_today_usage()
        new_day_tokens = today["total_tokens"] + input_tokens + output_tokens
        new_day_cost = today["total_cost_cents"] + estimated_cost
        
        if new_day_tokens > self.limits.max_tokens_per_day:
            return False, f"Daily token limit exceeded ({new_day_tokens:,} > {self.limits.max_tokens_per_day:,})"
        if new_day_cost > self.limits.max_cost_cents_per_day:
            return False, f"Daily cost limit exceeded (${new_day_cost/100:.2f} > ${self.limits.max_cost_cents_per_day/100:.2f})"
        
        # Check monthly budget
        month = self.tracker.get_month_usage()
        new_month_tokens = month["total_tokens"] + input_tokens + output_tokens
        new_month_cost = month["total_cost_cents"] + estimated_cost
        
        if new_month_tokens > self.limits.max_tokens_per_month:
            return False, f"Monthly token limit exceeded"
        if new_month_cost > self.limits.max_cost_cents_per_month:
            return False, f"Monthly cost limit exceeded (${new_month_cost/100:.2f} > ${self.limits.max_cost_cents_per_month/100:.2f})"
        
        return True, "OK"
    
    def record_usage(self, model: str, input_tokens: int, output_tokens: int,
                     run_id: str = None, agent: str = None):
        """Record usage after a successful call."""
        self.tracker.record(model, input_tokens, output_tokens, run_id, agent)
        
        if run_id:
            if run_id not in self._run_usage:
                self._run_usage[run_id] = {"tokens": 0, "cost": 0}
            self._run_usage[run_id]["tokens"] += input_tokens + output_tokens
            self._run_usage[run_id]["cost"] += CostCalculator.calculate_cost(model, input_tokens, output_tokens)
    
    def get_available_model(self, chain: str = "quality", 
                            max_cost_cents: int = None) -> Optional[str]:
        """
        Get first available model from fallback chain within budget.
        
        Args:
            chain: Fallback chain name
            max_cost_cents: Maximum cost per 1K tokens (optional filter)
        """
        models = FALLBACK_CHAINS.get(chain, FALLBACK_CHAINS["fast"])
        
        for model in models:
            # Check if model is within cost preference
            if max_cost_cents:
                pricing = MODEL_PRICING.get(model, {"input": 100, "output": 100})
                model_cost = (pricing["input"] + pricing["output"]) / 2  # Average
                if model_cost * 10 > max_cost_cents:  # Per 1K tokens
                    continue
            
            # Check budget for reasonable usage
            allowed, _ = self.check_budget(model, 10000, 2000)
            if allowed:
                return model
        
        # Last resort: local
        return "local"
    
    def check_rate_limit(self, provider: str) -> bool:
        """Check if we're rate limited for a provider."""
        limit = self.limits.rate_limits.get(provider, 60)
        return self.rate_limiter.check(provider, limit)
    
    def wait_for_rate_limit(self, provider: str) -> float:
        """Wait for rate limit to clear."""
        limit = self.limits.rate_limits.get(provider, 60)
        return self.rate_limiter.wait_if_needed(provider, limit)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive usage summary."""
        today = self.tracker.get_today_usage()
        month = self.tracker.get_month_usage()
        
        return {
            "today": {
                "tokens": today["total_tokens"],
                "cost_cents": today["total_cost_cents"],
                "limit_tokens": self.limits.max_tokens_per_day,
                "limit_cost_cents": self.limits.max_cost_cents_per_day,
                "tokens_remaining": self.limits.max_tokens_per_day - today["total_tokens"],
                "cost_remaining_cents": self.limits.max_cost_cents_per_day - today["total_cost_cents"]
            },
            "month": {
                "tokens": month["total_tokens"],
                "cost_cents": month["total_cost_cents"],
                "limit_tokens": self.limits.max_tokens_per_month,
                "limit_cost_cents": self.limits.max_cost_cents_per_month
            },
            "by_model": today.get("by_model", {}),
            "active_runs": len(self._run_usage)
        }

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

_budget: Optional[BudgetController] = None

def get_budget() -> BudgetController:
    """Get global budget controller."""
    global _budget
    if _budget is None:
        _budget = BudgetController()
    return _budget

def check_and_record(model: str, input_tokens: int, output_tokens: int,
                     run_id: str = None) -> bool:
    """
    Check budget and record usage in one call.
    
    Raises BudgetExceededError if over budget.
    """
    budget = get_budget()
    
    allowed, reason = budget.check_budget(model, input_tokens, output_tokens, run_id)
    if not allowed:
        raise BudgetExceededError(reason)
    
    budget.record_usage(model, input_tokens, output_tokens, run_id)
    return True

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    budget = get_budget()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "status":
            summary = budget.get_summary()
            print("\n💰 GABRIEL BUDGET STATUS")
            print("=" * 50)
            print(f"\n📅 TODAY:")
            print(f"   Tokens: {summary['today']['tokens']:,} / {summary['today']['limit_tokens']:,}")
            print(f"   Cost: ${summary['today']['cost_cents']/100:.2f} / ${summary['today']['limit_cost_cents']/100:.2f}")
            print(f"\n📆 THIS MONTH:")
            print(f"   Tokens: {summary['month']['tokens']:,} / {summary['month']['limit_tokens']:,}")
            print(f"   Cost: ${summary['month']['cost_cents']/100:.2f} / ${summary['month']['limit_cost_cents']/100:.2f}")
            
            if summary['by_model']:
                print(f"\n📊 BY MODEL (today):")
                for model, data in summary['by_model'].items():
                    print(f"   {model}: {data['tokens']:,} tokens, ${data['cost']/100:.2f}")
        
        elif cmd == "models":
            print("\n🤖 MODEL PRICING (per 1M tokens)")
            print("=" * 60)
            for model, pricing in sorted(MODEL_PRICING.items(), key=lambda x: x[1]["input"]):
                print(f"  {model:40} ${pricing['input']:>6.2f} in / ${pricing['output']:>6.2f} out")
        
        elif cmd == "limits":
            print("\n⚙️ CURRENT LIMITS")
            print("=" * 50)
            print(f"  Per Run: {budget.limits.max_tokens_per_run:,} tokens, ${budget.limits.max_cost_cents_per_run/100:.2f}")
            print(f"  Per Day: {budget.limits.max_tokens_per_day:,} tokens, ${budget.limits.max_cost_cents_per_day/100:.2f}")
            print(f"  Per Month: {budget.limits.max_tokens_per_month:,} tokens, ${budget.limits.max_cost_cents_per_month/100:.2f}")
        
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("💰 GABRIEL Cost Controller")
        print("\nUsage:")
        print("  python cost_controller.py status   # Show budget status")
        print("  python cost_controller.py models   # Show model pricing")
        print("  python cost_controller.py limits   # Show limits")

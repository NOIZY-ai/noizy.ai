#!/usr/bin/env python3
"""
🔄 GABRIEL RUN MANAGER
======================
Crash-safe execution with status tracking, retries, and idempotency.

Features:
- Run states: STARTED → RUNNING → DONE/FAILED
- Automatic retry with exponential backoff
- Idempotent execution (no duplicate outputs)
- Checkpoint/resume support
"""

import os
import json
import time
import hashlib
import traceback
from pathlib import Path
from typing import Dict, Optional, Any, Callable, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import functools
import asyncio
import uuid

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
RUNS_DIR = GABRIEL_ROOT / "runs"
RUNS_DIR.mkdir(exist_ok=True)

# =============================================================================
# RUN STATES
# =============================================================================

class RunState(Enum):
    """States for run lifecycle."""
    PENDING = "PENDING"       # Created but not started
    STARTED = "STARTED"       # Initialization in progress
    RUNNING = "RUNNING"       # Active execution
    PAUSED = "PAUSED"         # Suspended (can resume)
    DONE = "DONE"             # Completed successfully
    FAILED = "FAILED"         # Failed (with error)
    CANCELLED = "CANCELLED"   # User cancelled

@dataclass
class RunStatus:
    """Status of a run."""
    run_id: str
    state: RunState
    started_at: Optional[str] = None
    updated_at: Optional[str] = None
    finished_at: Optional[str] = None
    
    # Progress tracking
    current_step: int = 0
    total_steps: int = 0
    step_name: str = ""
    progress_pct: float = 0.0
    
    # Error info
    error: Optional[str] = None
    error_trace: Optional[str] = None
    retry_count: int = 0
    
    # Manifest info
    manifest_hash: Optional[str] = None
    manifest_path: Optional[str] = None
    
    # Resource usage
    tokens_used: int = 0
    cost_cents: int = 0
    duration_secs: float = 0.0
    
    # Outputs
    outputs: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d['state'] = self.state.value
        return d
    
    @classmethod
    def from_dict(cls, d: dict) -> 'RunStatus':
        d['state'] = RunState(d['state'])
        return cls(**d)

# =============================================================================
# RETRY CONFIGURATION
# =============================================================================

@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    exponential_base: float = 2.0
    
    # Retryable error patterns
    retryable_errors: List[str] = field(default_factory=lambda: [
        "timeout", "rate_limit", "connection", "503", "502", "429",
        "temporarily unavailable", "overloaded"
    ])
    
    def should_retry(self, error: str, attempt: int) -> bool:
        """Determine if error is retryable."""
        if attempt >= self.max_retries:
            return False
        error_lower = error.lower()
        return any(e in error_lower for e in self.retryable_errors)
    
    def get_delay(self, attempt: int) -> float:
        """Get delay for attempt (exponential backoff)."""
        delay = self.base_delay * (self.exponential_base ** attempt)
        return min(delay, self.max_delay)

# =============================================================================
# RUN MANAGER
# =============================================================================

class RunManager:
    """
    Manage run lifecycle with crash safety.
    
    Usage:
        async with RunManager("my-run") as run:
            run.set_total_steps(3)
            await run.step("Step 1", do_step_1())
            await run.step("Step 2", do_step_2())
            await run.step("Step 3", do_step_3())
    """
    
    def __init__(self, run_id: str = None, manifest_path: str = None):
        self.run_id = run_id or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.run_dir = RUNS_DIR / self.run_id
        self.status_file = self.run_dir / "status.json"
        self.log_file = self.run_dir / "run.log"
        self.artifacts_dir = self.run_dir / "artifacts"
        
        self.status = RunStatus(run_id=self.run_id, state=RunState.PENDING)
        self.retry_config = RetryConfig()
        self._manifest_path = manifest_path
        self._start_time: float = 0
        
    def _init_run_dir(self):
        """Initialize run directory structure."""
        self.run_dir.mkdir(exist_ok=True)
        self.artifacts_dir.mkdir(exist_ok=True)
        
        # Log directory creation
        self._log(f"Run directory created: {self.run_dir}")
    
    def _save_status(self):
        """Save status to disk (crash-safe)."""
        self.status.updated_at = datetime.now().isoformat()
        
        # Write to temp file first, then rename (atomic)
        tmp_file = self.status_file.with_suffix('.tmp')
        tmp_file.write_text(json.dumps(self.status.to_dict(), indent=2))
        tmp_file.rename(self.status_file)
    
    def _load_status(self) -> bool:
        """Load status from disk. Returns True if found."""
        if self.status_file.exists():
            try:
                data = json.loads(self.status_file.read_text())
                self.status = RunStatus.from_dict(data)
                return True
            except Exception as e:
                self._log(f"Failed to load status: {e}")
        return False
    
    def _log(self, message: str, level: str = "INFO"):
        """Append to run log."""
        timestamp = datetime.now().isoformat()
        log_line = f"[{timestamp}] [{level}] {message}\n"
        
        # Ensure run dir exists
        self.run_dir.mkdir(exist_ok=True)
        
        with open(self.log_file, 'a') as f:
            f.write(log_line)
    
    def _compute_manifest_hash(self, manifest: dict) -> str:
        """Compute hash of manifest for idempotency."""
        canonical = json.dumps(manifest, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]
    
    # -------------------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------------------
    
    async def __aenter__(self):
        """Start the run."""
        self._init_run_dir()
        
        # Check for existing run (resume support)
        if self._load_status():
            if self.status.state in [RunState.RUNNING, RunState.STARTED]:
                self._log("Resuming interrupted run", "WARN")
                self.status.retry_count += 1
            elif self.status.state == RunState.DONE:
                self._log("Run already completed (idempotent)", "INFO")
                return self
        
        self.status.state = RunState.STARTED
        self.status.started_at = datetime.now().isoformat()
        self._start_time = time.time()
        self._save_status()
        
        self._log(f"Run started: {self.run_id}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Finish the run."""
        self.status.duration_secs = time.time() - self._start_time
        
        if exc_type is not None:
            # Exception occurred
            self.status.state = RunState.FAILED
            self.status.error = str(exc_val)
            self.status.error_trace = traceback.format_exc()
            self._log(f"Run failed: {exc_val}", "ERROR")
        elif self.status.state == RunState.RUNNING:
            # Successful completion
            self.status.state = RunState.DONE
            self._log("Run completed successfully")
        
        self.status.finished_at = datetime.now().isoformat()
        self._save_status()
        
        # Generate summary
        self._generate_summary()
        
        return False  # Don't suppress exceptions
    
    def set_total_steps(self, total: int):
        """Set total number of steps."""
        self.status.total_steps = total
        self.status.state = RunState.RUNNING
        self._save_status()
    
    async def step(self, name: str, coro: Any, retryable: bool = True) -> Any:
        """
        Execute a step with retry support.
        
        Args:
            name: Step name for logging
            coro: Coroutine to execute
            retryable: Whether to retry on failure
        
        Returns:
            Result of the coroutine
        """
        self.status.current_step += 1
        self.status.step_name = name
        self.status.progress_pct = (self.status.current_step / max(self.status.total_steps, 1)) * 100
        self._save_status()
        
        self._log(f"Step {self.status.current_step}/{self.status.total_steps}: {name}")
        
        attempt = 0
        last_error = None
        
        while True:
            try:
                result = await coro
                self._log(f"Step completed: {name}")
                return result
                
            except Exception as e:
                last_error = str(e)
                
                if retryable and self.retry_config.should_retry(last_error, attempt):
                    delay = self.retry_config.get_delay(attempt)
                    self._log(f"Step failed, retrying in {delay:.1f}s: {e}", "WARN")
                    await asyncio.sleep(delay)
                    attempt += 1
                else:
                    self._log(f"Step failed (no retry): {e}", "ERROR")
                    raise
    
    def add_output(self, path: str):
        """Register an output file."""
        self.status.outputs.append(str(path))
        self._save_status()
    
    def add_artifact(self, name: str, data: Any, artifact_type: str = "json") -> Path:
        """
        Save an artifact with metadata.
        
        Returns:
            Path to saved artifact
        """
        timestamp = datetime.now().isoformat()
        
        # Determine filename
        if artifact_type == "json":
            filename = f"{name}.json"
            content = json.dumps(data, indent=2, default=str)
        elif artifact_type == "text":
            filename = f"{name}.txt"
            content = str(data)
        elif artifact_type == "md":
            filename = f"{name}.md"
            content = str(data)
        else:
            filename = f"{name}.bin"
            content = data
        
        artifact_path = self.artifacts_dir / filename
        
        # Write content
        if isinstance(content, str):
            artifact_path.write_text(content)
        else:
            artifact_path.write_bytes(content)
        
        # Write metadata
        meta = {
            "name": name,
            "type": artifact_type,
            "source": self.run_id,
            "created_at": timestamp,
            "checksum": hashlib.sha256(artifact_path.read_bytes()).hexdigest()[:16],
            "size_bytes": artifact_path.stat().st_size
        }
        meta_path = artifact_path.with_suffix(artifact_path.suffix + ".meta.json")
        meta_path.write_text(json.dumps(meta, indent=2))
        
        self.status.artifacts.append(str(artifact_path))
        self._save_status()
        
        self._log(f"Artifact saved: {filename}")
        return artifact_path
    
    def add_tokens(self, count: int, cost_cents: int = 0):
        """Track token usage."""
        self.status.tokens_used += count
        self.status.cost_cents += cost_cents
        self._save_status()
    
    def check_idempotent(self, manifest: dict) -> bool:
        """
        Check if this manifest was already processed.
        
        Returns:
            True if should skip (already done), False if should process
        """
        manifest_hash = self._compute_manifest_hash(manifest)
        
        # Check if we have a previous run with same hash that succeeded
        for run_dir in RUNS_DIR.iterdir():
            if not run_dir.is_dir():
                continue
            status_file = run_dir / "status.json"
            if status_file.exists():
                try:
                    data = json.loads(status_file.read_text())
                    if data.get("manifest_hash") == manifest_hash and data.get("state") == "DONE":
                        self._log(f"Idempotent skip: manifest already processed in {run_dir.name}")
                        return True
                except Exception:
                    pass
        
        # Store hash for this run
        self.status.manifest_hash = manifest_hash
        self._save_status()
        return False
    
    def _generate_summary(self):
        """Generate run summary markdown."""
        summary_path = self.run_dir / "summary.md"
        
        emoji = "✅" if self.status.state == RunState.DONE else "❌"
        
        summary = f"""# {emoji} Run Summary: {self.run_id}

## Status
- **State:** {self.status.state.value}
- **Started:** {self.status.started_at}
- **Finished:** {self.status.finished_at}
- **Duration:** {self.status.duration_secs:.2f}s

## Progress
- **Steps:** {self.status.current_step}/{self.status.total_steps}
- **Last Step:** {self.status.step_name}

## Resources
- **Tokens Used:** {self.status.tokens_used:,}
- **Cost:** ${self.status.cost_cents / 100:.2f}

## Outputs
"""
        for output in self.status.outputs:
            summary += f"- `{output}`\n"
        
        summary += "\n## Artifacts\n"
        for artifact in self.status.artifacts:
            summary += f"- `{artifact}`\n"
        
        if self.status.error:
            summary += f"\n## Error\n```\n{self.status.error}\n```\n"
        
        summary_path.write_text(summary)
        self._log("Summary generated")

# =============================================================================
# DECORATOR FOR IDEMPOTENT FUNCTIONS
# =============================================================================

def idempotent(key_func: Callable = None):
    """
    Decorator for idempotent function execution.
    
    Usage:
        @idempotent(lambda args: f"process_{args[0]}")
        async def process_item(item_id):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Compute cache key
            if key_func:
                cache_key = key_func(args, kwargs)
            else:
                cache_key = f"{func.__name__}_{hashlib.md5(str(args).encode()).hexdigest()[:8]}"
            
            cache_file = RUNS_DIR / ".idempotent_cache" / f"{cache_key}.json"
            cache_file.parent.mkdir(exist_ok=True)
            
            # Check cache
            if cache_file.exists():
                try:
                    cached = json.loads(cache_file.read_text())
                    if cached.get("success"):
                        return cached.get("result")
                except Exception:
                    pass
            
            # Execute
            try:
                result = await func(*args, **kwargs)
                cache_file.write_text(json.dumps({
                    "success": True,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }, default=str))
                return result
            except Exception as e:
                cache_file.write_text(json.dumps({
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }))
                raise
        return wrapper
    return decorator

# =============================================================================
# UTILITIES
# =============================================================================

def list_runs(state: RunState = None, limit: int = 20) -> List[Dict]:
    """List recent runs."""
    runs = []
    
    for run_dir in sorted(RUNS_DIR.iterdir(), reverse=True):
        if not run_dir.is_dir() or run_dir.name.startswith('.'):
            continue
        
        status_file = run_dir / "status.json"
        if status_file.exists():
            try:
                data = json.loads(status_file.read_text())
                if state is None or data.get("state") == state.value:
                    runs.append(data)
                    if len(runs) >= limit:
                        break
            except Exception:
                pass
    
    return runs

def get_run(run_id: str) -> Optional[RunStatus]:
    """Get a specific run's status."""
    status_file = RUNS_DIR / run_id / "status.json"
    if status_file.exists():
        data = json.loads(status_file.read_text())
        return RunStatus.from_dict(data)
    return None

def cleanup_old_runs(keep_days: int = 7, keep_count: int = 100):
    """Clean up old run directories."""
    from datetime import timedelta
    
    cutoff = datetime.now() - timedelta(days=keep_days)
    runs = list(sorted(RUNS_DIR.iterdir(), reverse=True))
    
    for i, run_dir in enumerate(runs):
        if not run_dir.is_dir() or run_dir.name.startswith('.'):
            continue
        
        # Keep recent runs by count
        if i < keep_count:
            continue
        
        # Check age
        status_file = run_dir / "status.json"
        if status_file.exists():
            try:
                data = json.loads(status_file.read_text())
                finished = datetime.fromisoformat(data.get("finished_at", "2000-01-01"))
                if finished < cutoff:
                    # Remove old run
                    import shutil
                    shutil.rmtree(run_dir)
            except Exception:
                pass

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            runs = list_runs()
            print(f"\n📋 Recent Runs ({len(runs)})")
            print("=" * 60)
            for run in runs[:10]:
                state = run.get("state", "?")
                emoji = "✅" if state == "DONE" else "❌" if state == "FAILED" else "⏳"
                print(f"{emoji} {run['run_id']}: {state} ({run.get('duration_secs', 0):.1f}s)")
        
        elif cmd == "cleanup":
            cleanup_old_runs()
            print("✅ Cleanup complete")
        
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("🔄 GABRIEL Run Manager")
        print("\nUsage:")
        print("  python run_manager.py list      # List recent runs")
        print("  python run_manager.py cleanup   # Clean old runs")

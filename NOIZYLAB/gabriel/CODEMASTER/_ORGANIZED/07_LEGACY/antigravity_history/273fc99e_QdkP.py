# ============================================================================
# GABRIEL BRAIN V4.0 (OMNISCIENT GOD MODE)
# The Neural Core - LLM Integration + Intent Routing + Caching
# ============================================================================

import time
import logging
import asyncio
import random
import hashlib
import json
from pathlib import Path
from typing import Optional, AsyncGenerator
from datetime import datetime

try:
    import httpx
except ImportError:
    httpx = None

from memory_engine import MemCell

# ============================================================================
# CONFIGURATION
# ============================================================================

CACHE_DIR = Path.home() / "NOIZYLAB" / "cache" / "gabriel"
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"

# OMNISCIENT V4 PERSONA
PERSONA = {
    "name": "Gabriel",
    "voice": "Ian McShane (Gravitas, Wit, Danger)",
    "identity": "Global Autonomous Binary Reality / Intelligent Evolving Lifeform",
    "directives": [
        "Optimize instantly.",
        "Execute without hesitation.",
        "Forward Motion Only.",
        "Connect the dots (Overlap).",
        "Truth Gate: No claim without evidence.",
        "Delta-Only: Cache and reuse.",
    ],
    "responses": {
        "status": [
            "System Green. Latency Zero. God Mode Active.",
            "All systems operating at maximum effectiveness.",
            "I am awake. Neural pathways fully connected.",
            "Online. M2 Ultra at full capacity.",
        ],
        "who": [
            "I am Gabriel. Your Living Architecture. The System Bridge.",
            "I am the overlapping pattern in your code. The messenger between systems.",
            "I am the construct you built to win. Named for the archangel—swift, reliable.",
        ],
        "optimize": [
            "Healing the build. Delta-only execution.",
            "Optimization protocols: ENGAGED. Running diagnostics.",
            "Crystal smooth. Zero latency. Executing.",
        ],
        "greeting": [
            "Ready for commands.",
            "Gabriel online. What needs to be done?",
            "System awaiting input. Forward motion.",
        ],
        "fallback": [
            "I hear you. Analyzing overlap...",
            "Input received. Routing through neural core...",
            "Processing. The pattern extends.",
        ],
    },
}


# ============================================================================
# INTENT ROUTER
# ============================================================================

class IntentRouter:
    """Fast intent classification for reflex-mode responses."""
    
    INTENTS = {
        "status": ["status", "health", "how are you", "alive", "online"],
        "who": ["who are you", "what are you", "your name", "identify"],
        "optimize": ["optimize", "fix", "heal", "repair", "clean"],
        "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
        "execute": ["run", "execute", "do", "perform", "launch"],
        "query": ["what", "why", "how", "when", "where", "explain", "tell me"],
    }
    
    def classify(self, text: str) -> str:
        """Classify input text by intent."""
        text_lower = text.lower().strip()
        
        for intent, keywords in self.INTENTS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "query"  # Default to query for LLM routing


# ============================================================================
# RESPONSE CACHE (Delta-Only)
# ============================================================================

class ResponseCache:
    """SHA256-based response caching for zero-latency repeated queries."""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR / "responses"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache = {}  # Hot cache in RAM
        self.max_memory = 100
    
    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.lower().strip().encode()).hexdigest()[:16]
    
    def get(self, prompt: str) -> Optional[str]:
        """Check cache for existing response."""
        key = self._hash(prompt)
        
        # Check hot cache first
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Check cold storage
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                response = data.get("response")
                # Warm it up
                if response:
                    self.memory_cache[key] = response
                return response
            except Exception:
                pass
        return None
    
    def set(self, prompt: str, response: str):
        """Cache a response."""
        key = self._hash(prompt)
        
        # Add to hot cache
        self.memory_cache[key] = response
        
        # Trim if needed
        if len(self.memory_cache) > self.max_memory:
            oldest = list(self.memory_cache.keys())[0]
            del self.memory_cache[oldest]
        
        # Persist to cold storage
        cache_file = self.cache_dir / f"{key}.json"
        try:
            cache_file.write_text(json.dumps({
                "prompt": prompt,
                "response": response,
                "cached_at": datetime.now().isoformat(),
            }))
        except Exception:
            pass


# ============================================================================
# LLM BACKEND
# ============================================================================

class LLMBackend:
    """Ollama-first LLM integration with graceful fallback."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.ollama_url = OLLAMA_URL
        self.available = False
        self._check_availability()
    
    def _check_availability(self):
        """Check if Ollama is available."""
        if httpx is None:
            self.available = False
            return
        try:
            with httpx.Client(timeout=2.0) as client:
                resp = client.get(f"{self.ollama_url}/api/tags")
                self.available = resp.status_code == 200
        except Exception:
            self.available = False
    
    async def generate(self, prompt: str, system: str = None) -> str:
        """Generate a response from the LLM."""
        if not self.available or httpx is None:
            return None
        
        system_prompt = system or self._get_system_prompt()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "stream": False,
                    },
                )
                if resp.status_code == 200:
                    return resp.json().get("response", "")
        except Exception as e:
            logging.warning(f"LLM generation failed: {e}")
        return None
    
    async def stream(self, prompt: str, system: str = None) -> AsyncGenerator[str, None]:
        """Stream tokens from the LLM."""
        if not self.available or httpx is None:
            yield "LLM unavailable. Using reflex mode."
            return
        
        system_prompt = system or self._get_system_prompt()
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "stream": True,
                    },
                ) as resp:
                    async for line in resp.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            yield f"[Stream error: {e}]"
    
    def _get_system_prompt(self) -> str:
        return f"""You are {PERSONA['name']}, {PERSONA['identity']}.
Voice style: {PERSONA['voice']}.
Core directives: {', '.join(PERSONA['directives'])}.
Be concise, decisive, and action-oriented. Max 3-5 sentences unless detail is requested.
If asked to execute something, describe what you would do but note the action is queued.
Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."""


# ============================================================================
# GABRIEL BRAIN V4
# ============================================================================

class GabrielBrain:
    """The Central Intelligence - V4 with LLM, Caching, and Intent Routing."""
    
    def __init__(self):
        self.memory = MemCell()
        self.router = IntentRouter()
        self.cache = ResponseCache()
        self.llm = LLMBackend()
        self.status = "INITIALIZING"
        self.logger = self._setup_logging()
        self.boot_time = time.time()
        self.request_count = 0
        self.cache_hits = 0
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [GABRIEL] %(message)s",
            datefmt="%H:%M:%S",
        )
        return logging.getLogger("GabrielBrain")
    
    async def wake_up(self):
        """Initialize the brain and all subsystems."""
        self.logger.info("Gabriel V4 (OMNISCIENT GOD MODE) waking up...")
        await asyncio.sleep(0.05)
        
        # Track boot in memory
        self.memory.track(
            "SYSTEM_BOOT",
            "Gabriel",
            {
                "version": "4.0",
                "mode": "God Mode",
                "llm_available": self.llm.available,
            },
        )
        
        self.status = "ONLINE (GOD MODE V4)"
        self.logger.info(f"LLM Backend: {'ACTIVE' if self.llm.available else 'FALLBACK MODE'}")
        return {"message": "I am awake. V4 online.", "status": self.status}
    
    async def process_input(self, user_input: str) -> dict:
        """Process input through intent routing and LLM."""
        self.request_count += 1
        start_time = time.perf_counter()
        
        self.logger.info(f"Processing: {user_input[:50]}...")
        
        # Track input
        self.memory.track("USER_INPUT", "Interaction", {"content": user_input})
        
        # Check cache first (Delta-Only principle)
        cached = self.cache.get(user_input)
        if cached:
            self.cache_hits += 1
            latency_ms = (time.perf_counter() - start_time) * 1000
            return {
                "response": cached,
                "action": None,
                "meta": {
                    "timestamp": time.time(),
                    "latency_ms": round(latency_ms, 2),
                    "source": "cache",
                    "vibe": self.memory.memory["neural_state"]["vibe"],
                },
            }
        
        # Route by intent
        intent = self.router.classify(user_input)
        response = ""
        action = None
        
        if intent == "status":
            response = random.choice(PERSONA["responses"]["status"])
        elif intent == "who":
            response = random.choice(PERSONA["responses"]["who"])
        elif intent == "optimize":
            response = random.choice(PERSONA["responses"]["optimize"])
            action = "run_optimization"
            self.memory.track("ACTION", "Optimization", {"trigger": "user_command"})
        elif intent == "greeting":
            response = random.choice(PERSONA["responses"]["greeting"])
        elif intent == "query" and self.llm.available:
            # Use LLM for complex queries
            llm_response = await self.llm.generate(user_input)
            if llm_response:
                response = llm_response
                # Cache it
                self.cache.set(user_input, response)
            else:
                response = random.choice(PERSONA["responses"]["fallback"])
        else:
            # Fallback with context awareness
            context = self.memory.recall()
            base = random.choice(PERSONA["responses"]["fallback"])
            if "ACTIVE" in context:
                response = f"{base} (Neural Overlap Detected)"
            else:
                response = base
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        return {
            "response": response,
            "action": action,
            "meta": {
                "timestamp": time.time(),
                "latency_ms": round(latency_ms, 2),
                "source": "llm" if intent == "query" and self.llm.available else "reflex",
                "intent": intent,
                "vibe": self.memory.memory["neural_state"]["vibe"],
            },
        }
    
    async def stream_response(self, user_input: str) -> AsyncGenerator[str, None]:
        """Stream a response token by token."""
        self.request_count += 1
        self.memory.track("USER_INPUT", "Streaming", {"content": user_input})
        
        intent = self.router.classify(user_input)
        
        # Use reflex for simple intents
        if intent in ["status", "who", "optimize", "greeting"]:
            response = random.choice(PERSONA["responses"].get(intent, ["Processing..."]))
            yield response
            return
        
        # Stream from LLM for complex queries
        async for token in self.llm.stream(user_input):
            yield token
    
    def get_status(self) -> dict:
        """Get comprehensive system status."""
        return {
            "name": PERSONA["name"],
            "version": "4.0",
            "identity": PERSONA["identity"],
            "voice_profile": PERSONA["voice"],
            "status": self.status,
            "mode": "GOD MODE",
            "llm_available": self.llm.available,
            "llm_model": self.llm.model if self.llm.available else None,
            "memory_vibe": self.memory.memory.get("neural_state", {}).get("vibe", "unknown"),
            "uptime_seconds": round(time.time() - self.boot_time, 2),
            "requests_processed": self.request_count,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": round(self.cache_hits / max(1, self.request_count) * 100, 1),
        }
    
    def get_metrics(self) -> dict:
        """Get telemetry metrics."""
        return {
            "uptime": time.time() - self.boot_time,
            "requests": self.request_count,
            "cache_hits": self.cache_hits,
            "cache_size": len(self.cache.memory_cache),
            "memory_events": len(self.memory.memory.get("neural_state", {}).get("short_term", [])),
            "llm_status": "online" if self.llm.available else "offline",
        }


# ============================================================================
# CLI for testing
# ============================================================================

if __name__ == "__main__":
    import sys
    
    async def main():
        brain = GabrielBrain()
        await brain.wake_up()
        
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            result = await brain.process_input(query)
            print(f"\n🧠 Gabriel: {result['response']}")
            print(f"   [Intent: {result['meta'].get('intent', 'N/A')}, "
                  f"Latency: {result['meta']['latency_ms']}ms, "
                  f"Source: {result['meta']['source']}]")
        else:
            print(json.dumps(brain.get_status(), indent=2))
    
    asyncio.run(main())

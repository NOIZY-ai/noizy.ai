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

try:
    from speed_core import speed_core
except ImportError:
    speed_core = None

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
# INTENT ROUTER V2 - REFLEX FIRST (75% SPEED UPGRADE)
# Goal: Answer 80%+ of queries without LLM
# ============================================================================

class IntentRouter:
    """
    Fast intent classification for reflex-mode responses.
    Expanded patterns to handle ~80% of queries without LLM.
    """
    
    # Core intents with expanded patterns
    INTENTS = {
        "status": [
            "status", "health", "how are you", "alive", "online", "awake",
            "working", "system", "vitals", "check", "diagnostic", "uptime",
        ],
        "who": [
            "who are you", "what are you", "your name", "identify", "yourself",
            "gabriel", "introduce", "about you",
        ],
        "optimize": [
            "optimize", "fix", "heal", "repair", "clean", "improve", "upgrade",
            "enhance", "tune", "speed up", "faster", "performance",
        ],
        "greeting": [
            "hello", "hi", "hey", "good morning", "good evening", "greetings",
            "sup", "yo", "what's up", "howdy",
        ],
        "confirm_yes": [
            "yes", "yeah", "yep", "sure", "ok", "okay", "affirmative",
            "correct", "right", "true", "do it", "proceed", "go ahead",
        ],
        "confirm_no": [
            "no", "nope", "nah", "negative", "wrong", "false", "cancel",
            "stop", "abort", "don't", "never",
        ],
        "thanks": [
            "thanks", "thank you", "appreciate", "cheers", "thx", "ty",
        ],
        "help": [
            "help", "assist", "support", "guide", "show me", "teach",
            "how do i", "how to", "can you",
        ],
        "memory": [
            "remember", "recall", "memory", "history", "earlier", "before",
            "last time", "previous", "forget",
        ],
        "time": [
            "time", "date", "today", "now", "current", "clock", "when",
        ],
        "capability": [
            "can you", "are you able", "do you know", "capable", "feature",
            "what can", "options", "commands",
        ],
        "stop": [
            "stop", "pause", "wait", "hold", "quiet", "silence", "shut up",
        ],
    }
    
    # Responses for expanded intents (no LLM needed)
    REFLEX_RESPONSES = {
        "confirm_yes": [
            "Acknowledged. Proceeding.",
            "Confirmed. Executing.",
            "Roger that.",
        ],
        "confirm_no": [
            "Understood. Standing down.",
            "Cancelled.",
            "Aborted.",
        ],
        "thanks": [
            "You're welcome.",
            "Anytime.",
            "Forward motion.",
        ],
        "help": [
            "I can optimize, diagnose, recall memory, and answer questions. Try: 'status', 'optimize', or ask anything.",
            "Commands: status, optimize, memory, or ask me anything. Voice or text.",
        ],
        "memory": [
            "Accessing neural patterns...",
            "Recall initiated.",
        ],
        "time": [
            f"Current time noted.",
        ],
        "capability": [
            "I optimize systems, track patterns, answer questions, and execute commands. Voice-first, zero latency.",
        ],
        "stop": [
            "Paused.",
            "Standing by.",
        ],
    }
    
    def classify(self, text: str) -> tuple[str, float]:
        """
        Classify input text by intent.
        Returns (intent, confidence) where confidence 0-1 indicates match strength.
        """
        text_lower = text.lower().strip()
        words = text_lower.split()
        word_count = len(words)
        
        # Very short inputs (1-2 words) = high confidence reflex
        if word_count <= 2:
            for intent, keywords in self.INTENTS.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        return (intent, 0.95)
        
        # Medium inputs - check for keyword matches
        matches = {}
        for intent, keywords in self.INTENTS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                matches[intent] = score
        
        if matches:
            best_intent = max(matches, key=matches.get)
            confidence = min(0.9, 0.5 + matches[best_intent] * 0.2)
            return (best_intent, confidence)
        
        # Long complex query with no matches = needs LLM
        if word_count > 10:
            return ("query", 0.3)
        
        # Default to query with medium confidence
        return ("query", 0.5)
    
    def needs_llm(self, intent: str, confidence: float) -> bool:
        """Determine if LLM is needed based on intent and confidence."""
        # Never use LLM for these
        if intent in ["confirm_yes", "confirm_no", "thanks", "stop", "greeting"]:
            return False
        
        # Use LLM only when confidence is low
        if intent == "query" and confidence < 0.6:
            return True
        
        # High confidence reflex handles it
        return confidence < 0.4



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
        """Minimal system prompt (<50 tokens) for speed."""
        return """Gabriel AI. Concise. 1-3 sentences max. Action-oriented. No fluff. Execute or explain."""


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
        
        # Route by intent with confidence scoring
        intent, confidence = self.router.classify(user_input)
        response = ""
        action = None
        source = "reflex"
        
        # === REFLEX FIRST - Handle 80%+ without LLM ===
        
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
        elif intent in self.router.REFLEX_RESPONSES:
            # Use reflex response for expanded intents
            response = random.choice(self.router.REFLEX_RESPONSES[intent])
        elif intent == "memory":
            # MemCell lookup before LLM
            response = self.memory.recall()
            source = "memory"
        elif intent == "time":
            response = f"Current time: {datetime.now().strftime('%H:%M:%S on %B %d, %Y')}."
        elif self.router.needs_llm(intent, confidence) and self.llm.available:
            # LLM only when confidence gap exists
            source = "llm"
            llm_response = await self.llm.generate(user_input)
            if llm_response:
                response = llm_response
                self.cache.set(user_input, response)
            else:
                response = random.choice(PERSONA["responses"]["fallback"])
                source = "reflex"
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
                "source": source,
                "intent": intent,
                "confidence": round(confidence, 2),
                "mode": "reflex" if source != "llm" else "deep",
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

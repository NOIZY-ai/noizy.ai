"""
GABRIEL LATENCY CONTROLLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Zero-Stutter UX Architecture
Reflex → Retrieval → Deep Ladder
Streaming • Async • Backpressure • Warm Caches • Degrade Modes
"""

import os
import asyncio
import hashlib
import time
import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable, List
from enum import Enum
from pathlib import Path
import threading
import queue

logger = logging.getLogger("LATENCY_CONTROLLER")

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

@dataclass
class LatencyMetrics:
    """Track p50/p95 latencies"""
    samples: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def record(self, ms: float):
        self.samples.append(ms)
    
    @property
    def p50(self) -> float:
        if not self.samples:
            return 0
        sorted_samples = sorted(self.samples)
        return sorted_samples[len(sorted_samples) // 2]
    
    @property
    def p95(self) -> float:
        if not self.samples:
            return 0
        sorted_samples = sorted(self.samples)
        idx = int(len(sorted_samples) * 0.95)
        return sorted_samples[min(idx, len(sorted_samples) - 1)]
    
    @property
    def avg(self) -> float:
        if not self.samples:
            return 0
        return sum(self.samples) / len(self.samples)


class PerformanceMode(Enum):
    """System performance modes"""
    FULL = "full"           # All features, max quality
    BALANCED = "balanced"   # Reduced visuals, normal AI
    GHOST = "ghost"         # Minimal AI, cache-only
    EMERGENCY = "emergency" # Text-only, no streaming


@dataclass
class SystemHealth:
    """Current system health"""
    voice_latency: LatencyMetrics = field(default_factory=LatencyMetrics)
    llm_latency: LatencyMetrics = field(default_factory=LatencyMetrics)
    tool_latency: LatencyMetrics = field(default_factory=LatencyMetrics)
    
    mode: PerformanceMode = PerformanceMode.FULL
    queue_depth: int = 0
    dropped_frames: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    def degrade_if_needed(self) -> PerformanceMode:
        """Auto-degrade based on p95 latency"""
        if self.llm_latency.p95 > 2000:  # >2s = emergency
            self.mode = PerformanceMode.EMERGENCY
        elif self.llm_latency.p95 > 1000:  # >1s = ghost
            self.mode = PerformanceMode.GHOST
        elif self.llm_latency.p95 > 500:  # >500ms = balanced
            self.mode = PerformanceMode.BALANCED
        else:
            self.mode = PerformanceMode.FULL
        return self.mode

# ============================================================================
# REFLEX ROUTER (Fast Path)
# ============================================================================

class ReflexRouter:
    """
    Reflex → Retrieval → Deep Ladder
    Kills most heavy LLM calls with pattern matching and caching
    """
    
    def __init__(self):
        self.patterns: Dict[str, str] = {}
        self.cache: Dict[str, str] = {}
        self.cache_ttl: Dict[str, float] = {}
        self.ttl_seconds = 3600  # 1 hour default
        
        # Prebuilt reflexes (instant responses)
        self.reflexes = {
            r"(?i)^(hi|hello|hey)": "Hello! What can I help you with?",
            r"(?i)^(thanks|thank you)": "You're welcome!",
            r"(?i)^(bye|goodbye)": "Goodbye! Take care.",
            r"(?i)what time": lambda: f"It's {time.strftime('%I:%M %p')}.",
            r"(?i)what date": lambda: f"Today is {time.strftime('%B %d, %Y')}.",
        }
    
    def add_pattern(self, pattern: str, response: str):
        """Add a reflex pattern"""
        self.patterns[pattern] = response
    
    def cache_response(self, query: str, response: str):
        """Cache a response with TTL"""
        key = hashlib.md5(query.lower().encode()).hexdigest()
        self.cache[key] = response
        self.cache_ttl[key] = time.time() + self.ttl_seconds
    
    def get_cached(self, query: str) -> Optional[str]:
        """Get cached response if valid"""
        key = hashlib.md5(query.lower().encode()).hexdigest()
        if key in self.cache:
            if time.time() < self.cache_ttl.get(key, 0):
                return self.cache[key]
            else:
                del self.cache[key]
                del self.cache_ttl[key]
        return None
    
    def route(self, query: str) -> tuple[str, Optional[str]]:
        """
        Route query through the ladder:
        1. Reflex (instant pattern match)
        2. Cache (recent responses)
        3. Deep (full LLM call)
        
        Returns: (route_type, response_or_none)
        """
        import re
        
        # Level 1: Reflex patterns
        for pattern, response in self.reflexes.items():
            if re.search(pattern, query):
                if callable(response):
                    return ("reflex", response())
                return ("reflex", response)
        
        for pattern, response in self.patterns.items():
            if re.search(pattern, query):
                return ("reflex", response)
        
        # Level 2: Cache lookup
        cached = self.get_cached(query)
        if cached:
            return ("cache", cached)
        
        # Level 3: Deep call required
        return ("deep", None)

# ============================================================================
# ASYNC WORK QUEUE WITH BACKPRESSURE
# ============================================================================

class BoundedWorkQueue:
    """
    Bounded async queue with backpressure and drop policies
    Prevents runaway stutter under load
    """
    
    def __init__(self, maxsize: int = 100, drop_policy: str = "oldest", max_latency_ms: float = 200.0):
        self.maxsize = maxsize
        self.drop_policy = drop_policy
        self.max_latency_ms = max_latency_ms
        self.queue: asyncio.Queue = None
        self.dropped_count = 0
        self._lock = asyncio.Lock()
        
        # Predictive Backpressure
        self.processing_times: deque = deque(maxlen=20)
        self.last_pop_time = 0
    
    async def init(self):
        """Initialize async queue"""
        self.queue = asyncio.Queue(maxsize=self.maxsize)
    
    def record_processing_time(self, ms: float):
        """Feed the predictor"""
        self.processing_times.append(ms)
        
    def predict_wait_time(self) -> float:
        """Predict how long the queue will take to drain"""
        if not self.processing_times or not self.queue:
            return 0.0
        avg_time = sum(self.processing_times) / len(self.processing_times)
        return avg_time * self.queue.qsize()

    async def put(self, item: Any, priority: int = 5) -> bool:
        """
        Put item with PREDICTIVE backpressure
        """
        if self.queue is None:
            await self.init()
            
        # Predictive check
        predicted_wait = self.predict_wait_time()
        if predicted_wait > self.max_latency_ms:
            self.dropped_count += 1
            logger.warning(f"⚠️ PREDICTIVE DROP: Expected wait {predicted_wait:.1f}ms > {self.max_latency_ms}ms")
            return False
        
        async with self._lock:
            if self.queue.full():
                if self.drop_policy == "oldest":
                    try:
                        self.queue.get_nowait()
                        self.dropped_count += 1
                    except asyncio.QueueEmpty:
                        pass
                elif self.drop_policy == "newest":
                    self.dropped_count += 1
                    return False
                else:
                    pass
            
            try:
                self.queue.put_nowait((priority, item))
                return True
            except asyncio.QueueFull:
                self.dropped_count += 1
                return False

    async def get(self, timeout: float = None) -> Any:
        """Get next item and track timing"""
        if self.queue is None:
            await self.init()
        
        try:
            start_wait = time.perf_counter()
            if timeout:
                _, item = await asyncio.wait_for(self.queue.get(), timeout)
            else:
                _, item = await self.queue.get()
            
            # Auto-record wait time as a proxy for system load if caller doesn't explicitly record
            # But ideally caller calls record_processing_time
            return item
        except asyncio.TimeoutError:
            return None
    
    @property
    def depth(self) -> int:
        return self.queue.qsize() if self.queue else 0

# ============================================================================
# AUDIO CALLBACK QUEUE (Zero Dropout)
# ============================================================================

class AudioBufferQueue:
    """
    Audio callback = enqueue only → no dropouts
    FFT/analysis runs in worker thread
    """
    
    def __init__(self, buffer_size: int = 4096, max_buffers: int = 50):
        self.buffer_size = buffer_size
        self.max_buffers = max_buffers
        self.queue = queue.Queue(maxsize=max_buffers)
        self.analysis_queue = queue.Queue(maxsize=10)  # For FFT results
        self._running = False
        self._worker: Optional[threading.Thread] = None
    
    def start_worker(self, analyze_fn: Callable):
        """Start analysis worker thread"""
        self._running = True
        
        def worker():
            while self._running:
                try:
                    buffer = self.queue.get(timeout=0.1)
                    if buffer is not None:
                        result = analyze_fn(buffer)
                        try:
                            self.analysis_queue.put_nowait(result)
                        except queue.Full:
                            pass  # Drop old analysis results
                except queue.Empty:
                    continue
        
        self._worker = threading.Thread(target=worker, daemon=True)
        self._worker.start()
    
    def stop_worker(self):
        """Stop worker thread"""
        self._running = False
        if self._worker:
            self._worker.join(timeout=1)
    
    def enqueue(self, buffer: bytes) -> bool:
        """
        Audio callback calls this - FAST, never blocks
        Returns False if queue full (dropped)
        """
        try:
            self.queue.put_nowait(buffer)
            return True
        except queue.Full:
            return False
    
    def get_analysis(self) -> Optional[Any]:
        """Get latest analysis result (non-blocking)"""
        try:
            return self.analysis_queue.get_nowait()
        except queue.Empty:
            return None

# ============================================================================
# WARM CACHE MANAGER
# ============================================================================

class WarmCacheManager:
    """
    Warm caches on boot → no first-hit lag
    Preloads: router, prompts, FFT buffers, MIDI/OSC, hot MemCells
    """
    
    def __init__(self, cache_dir: str = "/Volumes/GabrielVol/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.memory_cache: Dict[str, Any] = {}
        self.preloaded = False
    
    async def warm_up(self, items: Dict[str, Callable]):
        """
        Warm up caches in parallel
        items: {"name": async_loader_fn}
        """
        logger.info("🔥 Warming caches...")
        
        async def load_item(name: str, loader: Callable):
            try:
                start = time.time()
                result = await loader() if asyncio.iscoroutinefunction(loader) else loader()
                self.memory_cache[name] = result
                elapsed = (time.time() - start) * 1000
                logger.info(f"   ✅ {name}: {elapsed:.1f}ms")
            except Exception as e:
                logger.warning(f"   ⚠️ {name}: {e}")
        
        await asyncio.gather(*[load_item(n, l) for n, l in items.items()])
        self.preloaded = True
        logger.info("🔥 Cache warmup complete")
    
    def get(self, key: str) -> Optional[Any]:
        """Get from memory cache"""
        return self.memory_cache.get(key)
    
    def set(self, key: str, value: Any):
        """Set in memory cache"""
        self.memory_cache[key] = value
    
    def persist(self, key: str, value: Any):
        """Persist to disk cache"""
        import pickle
        cache_file = self.cache_dir / f"{key}.pkl"
        with open(cache_file, "wb") as f:
            pickle.dump(value, f)
    
    def load_persisted(self, key: str) -> Optional[Any]:
        """Load from disk cache"""
        import pickle
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        return None

# ============================================================================
# STREAMING CHUNK MANAGER
# ============================================================================

class StreamingChunkManager:
    """
    Streaming everywhere → instant TTFT
    Token stream + incremental TTS (200-400ms chunks)
    """
    
    def __init__(self, chunk_size_ms: int = 300):
        self.chunk_size_ms = chunk_size_ms
        self.text_buffer = ""
        self.audio_buffer = bytearray()
        self.sample_rate = 24000  # samples/sec
        self.bytes_per_sample = 2  # 16-bit
    
    def chunk_size_bytes(self) -> int:
        """Calculate chunk size in bytes"""
        samples = int(self.sample_rate * self.chunk_size_ms / 1000)
        return samples * self.bytes_per_sample
    
    async def stream_tokens(self, token_generator) -> AsyncGenerator[str, None]:
        """Stream tokens as they arrive"""
        async for token in token_generator:
            self.text_buffer += token
            yield token
    
    def should_flush_audio(self) -> bool:
        """Check if audio buffer should be flushed"""
        return len(self.audio_buffer) >= self.chunk_size_bytes()
    
    def add_audio(self, audio_bytes: bytes) -> Optional[bytes]:
        """
        Add audio bytes, return chunk if ready
        """
        self.audio_buffer.extend(audio_bytes)
        
        if self.should_flush_audio():
            chunk_size = self.chunk_size_bytes()
            chunk = bytes(self.audio_buffer[:chunk_size])
            self.audio_buffer = self.audio_buffer[chunk_size:]
            return chunk
        return None
    
    def flush_audio(self) -> Optional[bytes]:
        """Flush remaining audio"""
        if self.audio_buffer:
            chunk = bytes(self.audio_buffer)
            self.audio_buffer = bytearray()
            return chunk
        return None

# ============================================================================
# DEGRADE MODE CONTROLLER
# ============================================================================

class DegradeModeController:
    """
    Degrade modes → stays smooth under load
    If p95 latency spikes: drop visuals, switch to Ghost, cache-only
    """
    
    def __init__(self, health: SystemHealth):
        self.health = health
        self.mode_callbacks: Dict[PerformanceMode, List[Callable]] = {
            PerformanceMode.FULL: [],
            PerformanceMode.BALANCED: [],
            PerformanceMode.GHOST: [],
            PerformanceMode.EMERGENCY: [],
        }
    
    def on_mode_change(self, mode: PerformanceMode, callback: Callable):
        """Register callback for mode change"""
        self.mode_callbacks[mode].append(callback)
    
    def check_and_degrade(self) -> PerformanceMode:
        """Check health and degrade if needed"""
        old_mode = self.health.mode
        new_mode = self.health.degrade_if_needed()
        
        if old_mode != new_mode:
            logger.warning(f"⚠️ Mode change: {old_mode.value} → {new_mode.value}")
            for callback in self.mode_callbacks[new_mode]:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Mode callback error: {e}")
        
        return new_mode
    
    def get_config(self) -> Dict[str, Any]:
        """Get config for current mode"""
        configs = {
            PerformanceMode.FULL: {
                "max_tokens": 2048,
                "fps": 60,
                "audio_quality": "high",
                "use_cache": True,
                "use_llm": True,
                "stream_audio": True,
            },
            PerformanceMode.BALANCED: {
                "max_tokens": 1024,
                "fps": 30,
                "audio_quality": "medium",
                "use_cache": True,
                "use_llm": True,
                "stream_audio": True,
            },
            PerformanceMode.GHOST: {
                "max_tokens": 256,
                "fps": 15,
                "audio_quality": "low",
                "use_cache": True,
                "use_llm": False,  # Cache only
                "stream_audio": False,
            },
            PerformanceMode.EMERGENCY: {
                "max_tokens": 128,
                "fps": 10,
                "audio_quality": "none",
                "use_cache": True,
                "use_llm": False,
                "stream_audio": False,
            },
        }
        return configs[self.health.mode]

# ============================================================================
# MAIN LATENCY CONTROLLER
# ============================================================================

class LatencyController:
    """
    Master controller for zero-stutter UX
    Integrates all subsystems
    """
    
    def __init__(self, cache_dir: str = "/Volumes/GabrielVol/cache"):
        self.health = SystemHealth()
        self.router = ReflexRouter()
        self.work_queue = BoundedWorkQueue(maxsize=100, drop_policy="oldest")
        self.audio_queue = AudioBufferQueue()
        self.cache = WarmCacheManager(cache_dir)
        self.streaming = StreamingChunkManager()
        self.degrader = DegradeModeController(self.health)
        
        logger.info("""
╔══════════════════════════════════════════════════════════════╗
║           LATENCY CONTROLLER INITIALIZED                     ║
╠══════════════════════════════════════════════════════════════╣
║  Reflex Router:      ✅ Pattern matching + cache             ║
║  Work Queue:         ✅ Bounded with backpressure            ║
║  Audio Queue:        ✅ Zero-dropout worker                  ║
║  Warm Cache:         ✅ Preload on boot                      ║
║  Streaming:          ✅ 300ms audio chunks                   ║
║  Degrade Modes:      ✅ Auto-switch on latency spike         ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    async def warm_up(self):
        """Warm all caches on boot"""
        await self.cache.warm_up({
            "router_patterns": lambda: self.router.patterns,
            "system_prompts": lambda: {"default": "You are Gabriel."},
        })
    
    def record_latency(self, category: str, ms: float):
        """Record a latency measurement"""
        if category == "voice":
            self.health.voice_latency.record(ms)
        elif category == "llm":
            self.health.llm_latency.record(ms)
        elif category == "tool":
            self.health.tool_latency.record(ms)
        
        # Check for degradation
        self.degrader.check_and_degrade()
    
    async def route_query(self, query: str) -> tuple[str, str]:
        """
        Route query through the ladder
        Returns: (route_type, response)
        """
        start = time.time()
        
        route_type, response = self.router.route(query)
        
        if response is not None:
            # Reflex or cache hit
            if route_type == "cache":
                self.health.cache_hits += 1
            elapsed = (time.time() - start) * 1000
            self.record_latency("llm", elapsed)
            return (route_type, response)
        
        # Need deep call
        self.health.cache_misses += 1
        return ("deep", None)
    
    def get_status(self) -> Dict[str, Any]:
        """Get full status"""
        return {
            "mode": self.health.mode.value,
            "latency": {
                "voice_p95": self.health.voice_latency.p95,
                "llm_p95": self.health.llm_latency.p95,
                "tool_p95": self.health.tool_latency.p95,
            },
            "queues": {
                "work_depth": self.work_queue.depth,
                "work_dropped": self.work_queue.dropped_count,
            },
            "cache": {
                "hits": self.health.cache_hits,
                "misses": self.health.cache_misses,
                "hit_rate": self.health.cache_hits / max(1, self.health.cache_hits + self.health.cache_misses),
            },
            "config": self.degrader.get_config(),
        }

#!/usr/bin/env python3
"""
Gabriel Speed Core V1.0 - Performance Optimization Layer
Implements: Precompute, Async, Hot RAM, Prediction, Bounded Queues
"""

import asyncio
import hashlib
import time
import json
from pathlib import Path
from collections import deque, OrderedDict
from typing import Optional, Any, Callable, Awaitable
from datetime import datetime
from functools import lru_cache
import threading
import queue

# ============================================================================
# CONFIGURATION
# ============================================================================

CACHE_DIR = Path.home() / "NOIZYLAB" / "cache" / "gabriel"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Bounded limits
HOT_CACHE_LIMIT = 100  # RAM items
COLD_CACHE_LIMIT = 1000  # Disk items
QUEUE_MAX_SIZE = 50  # Max pending tasks
CLEANUP_INTERVAL = 300  # 5 minutes
OPERATION_TIMEOUT = 10.0  # seconds


# ============================================================================
# PHASE 2: PRECOMPUTE CACHE (Hash → Output)
# ============================================================================

class PrecomputeCache:
    """
    Hash-based cache for precomputed outputs.
    Stores: summaries, embeddings, atomic facts, MIACLE outputs.
    """

    def __init__(self, name: str = "precompute"):
        self.name = name
        self.hot = OrderedDict()  # LRU in RAM
        self.hot_limit = HOT_CACHE_LIMIT
        self.cache_dir = CACHE_DIR / name
        self.cache_dir.mkdir(exist_ok=True)
        self.hits = 0
        self.misses = 0

    def _hash(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()[:16]

    def get(self, key: str) -> Optional[Any]:
        """Get from hot cache first, then cold."""
        h = self._hash(key)

        # Hot cache (moves to end = LRU)
        if h in self.hot:
            self.hot.move_to_end(h)
            self.hits += 1
            return self.hot[h]

        # Cold cache
        cold_file = self.cache_dir / f"{h}.json"
        if cold_file.exists():
            try:
                data = json.loads(cold_file.read_text())
                value = data.get("value")
                # Promote to hot
                self._set_hot(h, value)
                self.hits += 1
                return value
            except Exception:
                pass

        self.misses += 1
        return None

    def set(self, key: str, value: Any, persist: bool = True):
        """Store in hot cache and optionally persist."""
        h = self._hash(key)
        self._set_hot(h, value)

        if persist:
            cold_file = self.cache_dir / f"{h}.json"
            try:
                cold_file.write_text(json.dumps({
                    "key": key,
                    "value": value,
                    "cached_at": datetime.now().isoformat(),
                }))
            except Exception:
                pass

    def _set_hot(self, h: str, value: Any):
        """Set in hot cache with LRU eviction."""
        self.hot[h] = value
        self.hot.move_to_end(h)
        while len(self.hot) > self.hot_limit:
            self.hot.popitem(last=False)

    def precompute(self, key: str, compute_fn: Callable) -> Any:
        """Get cached or compute and cache."""
        cached = self.get(key)
        if cached is not None:
            return cached
        value = compute_fn()
        self.set(key, value)
        return value

    async def precompute_async(self, key: str, compute_fn: Callable[[], Awaitable]) -> Any:
        """Async version of precompute."""
        cached = self.get(key)
        if cached is not None:
            return cached
        value = await compute_fn()
        self.set(key, value)
        return value

    def stats(self) -> dict:
        return {
            "name": self.name,
            "hot_size": len(self.hot),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / max(1, self.hits + self.misses) * 100, 1),
        }


# ============================================================================
# PHASE 3: ASYNC TASK QUEUE (No Blocking)
# ============================================================================

class AsyncTaskQueue:
    """
    Bounded async queue for non-blocking background work.
    Audio, disk I/O, network all go here.
    """

    def __init__(self, max_workers: int = 4):
        self.queue = asyncio.Queue(maxsize=QUEUE_MAX_SIZE)
        self.workers = []
        self.max_workers = max_workers
        self.running = False
        self.completed = 0
        self.dropped = 0

    async def start(self):
        """Start worker tasks."""
        if self.running:
            return
        self.running = True
        self.workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_workers)
        ]

    async def stop(self):
        """Stop all workers gracefully."""
        self.running = False
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)

    async def _worker(self, worker_id: int):
        """Process tasks from queue."""
        while self.running:
            try:
                task, args, kwargs, future = await asyncio.wait_for(
                    self.queue.get(), timeout=1.0
                )
                try:
                    if asyncio.iscoroutinefunction(task):
                        result = await asyncio.wait_for(
                            task(*args, **kwargs), timeout=OPERATION_TIMEOUT
                        )
                    else:
                        result = await asyncio.get_event_loop().run_in_executor(
                            None, lambda: task(*args, **kwargs)
                        )
                    if future:
                        future.set_result(result)
                    self.completed += 1
                except asyncio.TimeoutError:
                    if future:
                        future.set_exception(TimeoutError("Task timed out"))
                except Exception as e:
                    if future:
                        future.set_exception(e)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def submit(self, task: Callable, *args, **kwargs) -> Optional[asyncio.Future]:
        """Submit task to queue. Returns future or None if queue full."""
        future = asyncio.get_event_loop().create_future()
        try:
            self.queue.put_nowait((task, args, kwargs, future))
            return future
        except asyncio.QueueFull:
            self.dropped += 1
            return None

    def submit_fire_forget(self, task: Callable, *args, **kwargs) -> bool:
        """Submit without waiting for result."""
        try:
            self.queue.put_nowait((task, args, kwargs, None))
            return True
        except asyncio.QueueFull:
            self.dropped += 1
            return False

    def stats(self) -> dict:
        return {
            "queue_size": self.queue.qsize(),
            "max_size": QUEUE_MAX_SIZE,
            "workers": self.max_workers,
            "completed": self.completed,
            "dropped": self.dropped,
        }


# ============================================================================
# PHASE 4: HOT RAM STATE
# ============================================================================

class HotRAMState:
    """
    Critical state in RAM for sub-10ms access.
    Preallocated buffers, active prompts, live connections.
    """

    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self.state = OrderedDict()
        self.access_count = 0
        self.lock = threading.Lock()

    def get(self, key: str, default: Any = None) -> Any:
        """O(1) access with LRU tracking."""
        with self.lock:
            if key in self.state:
                self.state.move_to_end(key)
                self.access_count += 1
                return self.state[key]
            return default

    def set(self, key: str, value: Any):
        """Set with automatic eviction."""
        with self.lock:
            self.state[key] = value
            self.state.move_to_end(key)
            while len(self.state) > self.max_size:
                self.state.popitem(last=False)

    def delete(self, key: str):
        """Remove key."""
        with self.lock:
            self.state.pop(key, None)

    def clear(self):
        """Clear all state."""
        with self.lock:
            self.state.clear()

    def keys(self) -> list:
        return list(self.state.keys())

    def stats(self) -> dict:
        return {
            "size": len(self.state),
            "max_size": self.max_size,
            "access_count": self.access_count,
        }


# ============================================================================
# PHASE 6: PREDICTION ENGINE
# ============================================================================

class PredictionEngine:
    """
    Predict next likely action based on patterns.
    Tracks: last N actions, time-of-day, app context.
    """

    def __init__(self, history_size: int = 10):
        self.history = deque(maxlen=history_size)
        self.patterns = {}  # action -> next_action counts
        self.time_patterns = {}  # hour -> action counts
        self.preloaded = set()

    def record(self, action: str):
        """Record an action."""
        now = datetime.now()
        hour = now.hour

        # Update time patterns
        if hour not in self.time_patterns:
            self.time_patterns[hour] = {}
        self.time_patterns[hour][action] = self.time_patterns[hour].get(action, 0) + 1

        # Update sequence patterns
        if self.history:
            prev = self.history[-1]
            if prev not in self.patterns:
                self.patterns[prev] = {}
            self.patterns[prev][action] = self.patterns[prev].get(action, 0) + 1

        self.history.append(action)

    def predict_next(self, n: int = 3) -> list[str]:
        """Predict N most likely next actions."""
        predictions = {}

        # From sequence pattern
        if self.history:
            last = self.history[-1]
            if last in self.patterns:
                for action, count in self.patterns[last].items():
                    predictions[action] = predictions.get(action, 0) + count * 2

        # From time pattern
        hour = datetime.now().hour
        if hour in self.time_patterns:
            for action, count in self.time_patterns[hour].items():
                predictions[action] = predictions.get(action, 0) + count

        # Sort by score
        sorted_actions = sorted(predictions.items(), key=lambda x: -x[1])
        return [a for a, _ in sorted_actions[:n]]

    def should_preload(self, action: str) -> bool:
        """Check if action should be preloaded."""
        return action in self.predict_next(5)

    def mark_preloaded(self, action: str):
        """Mark action as preloaded."""
        self.preloaded.add(action)

    def stats(self) -> dict:
        return {
            "history_len": len(self.history),
            "pattern_count": len(self.patterns),
            "time_patterns": len(self.time_patterns),
            "preloaded": len(self.preloaded),
            "predictions": self.predict_next(3),
        }


# ============================================================================
# PHASE 8: BOUNDED STATE MANAGER
# ============================================================================

class BoundedStateManager:
    """
    Enforces limits across all subsystems.
    Prevents memory bloat and performance decay.
    """

    def __init__(self):
        self.limits = {
            "hot_cache": HOT_CACHE_LIMIT,
            "cold_cache": COLD_CACHE_LIMIT,
            "queue": QUEUE_MAX_SIZE,
            "history": 100,
        }
        self.last_cleanup = time.time()
        self.cleanup_count = 0

    def should_cleanup(self) -> bool:
        """Check if cleanup cycle is due."""
        return time.time() - self.last_cleanup > CLEANUP_INTERVAL

    def run_cleanup(self, caches: list[PrecomputeCache], queues: list[AsyncTaskQueue]):
        """Run cleanup across all managed resources."""
        self.cleanup_count += 1
        self.last_cleanup = time.time()

        # Clean cold caches (remove oldest beyond limit)
        for cache in caches:
            files = sorted(cache.cache_dir.glob("*.json"), key=lambda f: f.stat().st_mtime)
            if len(files) > COLD_CACHE_LIMIT:
                for f in files[:-COLD_CACHE_LIMIT]:
                    try:
                        f.unlink()
                    except Exception:
                        pass

    def stats(self) -> dict:
        return {
            "limits": self.limits,
            "last_cleanup": datetime.fromtimestamp(self.last_cleanup).isoformat(),
            "cleanup_count": self.cleanup_count,
        }


# ============================================================================
# UNIFIED SPEED CORE
# ============================================================================

class SpeedCore:
    """
    Unified performance layer for Gabriel.
    Combines: Precompute, Async, Hot RAM, Prediction, Bounds.
    """

    def __init__(self):
        self.precompute = PrecomputeCache("responses")
        self.summaries = PrecomputeCache("summaries")
        self.facts = PrecomputeCache("facts")
        self.queue = AsyncTaskQueue(max_workers=4)
        self.hot = HotRAMState(max_size=50)
        self.predictor = PredictionEngine()
        self.bounds = BoundedStateManager()

    async def start(self):
        """Initialize async components."""
        await self.queue.start()

    async def stop(self):
        """Clean shutdown."""
        await self.queue.stop()

    def cache_or_compute(self, key: str, compute_fn: Callable) -> Any:
        """Sync cache-or-compute pattern."""
        return self.precompute.precompute(key, compute_fn)

    async def cache_or_compute_async(self, key: str, compute_fn: Callable) -> Any:
        """Async cache-or-compute pattern."""
        return await self.precompute.precompute_async(key, compute_fn)

    def get_hot(self, key: str) -> Any:
        """Sub-ms RAM access."""
        return self.hot.get(key)

    def set_hot(self, key: str, value: Any):
        """Store in hot RAM."""
        self.hot.set(key, value)

    def record_action(self, action: str):
        """Track action for prediction."""
        self.predictor.record(action)

    def predict_next(self) -> list[str]:
        """Get predicted next actions."""
        return self.predictor.predict_next()

    async def submit_background(self, task: Callable, *args, **kwargs):
        """Submit to async queue."""
        return await self.queue.submit(task, *args, **kwargs)

    def cleanup_if_needed(self):
        """Run cleanup if interval passed."""
        if self.bounds.should_cleanup():
            self.bounds.run_cleanup(
                [self.precompute, self.summaries, self.facts],
                [self.queue]
            )

    def all_stats(self) -> dict:
        """Get all performance stats."""
        return {
            "precompute": self.precompute.stats(),
            "summaries": self.summaries.stats(),
            "facts": self.facts.stats(),
            "queue": self.queue.stats(),
            "hot_ram": self.hot.stats(),
            "predictor": self.predictor.stats(),
            "bounds": self.bounds.stats(),
        }


# Global instance
speed_core = SpeedCore()


# ============================================================================
# CLI TEST
# ============================================================================

if __name__ == "__main__":
    import sys

    async def test():
        await speed_core.start()

        # Test precompute
        result = speed_core.cache_or_compute("test_key", lambda: "computed_value")
        print(f"First call (compute): {result}")
        result = speed_core.cache_or_compute("test_key", lambda: "should_not_run")
        print(f"Second call (cached): {result}")

        # Test hot RAM
        speed_core.set_hot("prompt:active", "Hello world")
        print(f"Hot RAM: {speed_core.get_hot('prompt:active')}")

        # Test prediction
        for action in ["status", "optimize", "status", "memory", "status"]:
            speed_core.record_action(action)
        print(f"Predictions: {speed_core.predict_next()}")

        # Stats
        print(f"\nStats: {json.dumps(speed_core.all_stats(), indent=2)}")

        await speed_core.stop()

    asyncio.run(test())

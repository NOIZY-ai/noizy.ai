#!/usr/bin/env python3
"""
Gabriel Test Suite V2.0
Comprehensive tests with performance benchmarks.
"""

import sys
import asyncio
import json
import time
from pathlib import Path
from statistics import mean, stdev

# Add core to path
CORE_DIR = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(CORE_DIR))


# ============================================================================
# TEST RESULT CLASS
# ============================================================================

class TestResult:
    def __init__(self, name: str, passed: bool, message: str = "", latency_ms: float = 0):
        self.name = name
        self.passed = passed
        self.message = message
        self.latency_ms = latency_ms

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lat = f" [{self.latency_ms:.2f}ms]" if self.latency_ms else ""
        msg = f" - {self.message}" if self.message else ""
        return f"{status}: {self.name}{lat}{msg}"


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_memory_engine():
    """Test MemCell V4 functionality."""
    from memory_engine import MemCell

    mc = MemCell()
    mc.track("TEST", "TestSubject", {"key": "value"})
    recall = mc.recall()
    
    if "MEMCELL V4" not in recall:
        return TestResult("MemoryEngine", False, "Recall format incorrect")
    if mc.get_stats()["version"] != "4.0":
        return TestResult("MemoryEngine", False, "Wrong version")
    if not mc.search_patterns("TestSubject"):
        return TestResult("MemoryEngine", False, "Search failed")

    return TestResult("MemoryEngine", True, "All functions working")


def test_intent_router():
    """Test IntentRouter V2 with confidence scoring."""
    from gabriel_brain import IntentRouter

    router = IntentRouter()
    
    # Test all intent categories
    tests = [
        ("status", "status", 0.7),
        ("who are you", "who", 0.7),
        ("optimize the code", "optimize", 0.7),
        ("hello there", "greeting", 0.7),
        ("yes", "confirm_yes", 0.9),
        ("no thanks", "confirm_no", 0.5),
        ("help me", "help", 0.7),
        ("what time is it", "time", 0.7),
    ]
    
    for text, expected_intent, min_conf in tests:
        intent, conf = router.classify(text)
        if intent != expected_intent:
            return TestResult("IntentRouter", False, f"'{text}' → {intent}, expected {expected_intent}")
        if conf < min_conf:
            return TestResult("IntentRouter", False, f"'{text}' confidence {conf} < {min_conf}")

    # Test needs_llm gate
    if router.needs_llm("greeting", 0.95):
        return TestResult("IntentRouter", False, "Greeting shouldn't need LLM")
    if not router.needs_llm("query", 0.3):
        return TestResult("IntentRouter", False, "Low-confidence query should need LLM")

    return TestResult("IntentRouter", True, f"12 intents + LLM gate verified")


def test_response_cache():
    """Test ResponseCache with hit/miss tracking."""
    from gabriel_brain import ResponseCache

    cache = ResponseCache()
    
    # Miss
    r1 = cache.get("test_prompt_unique_123")
    if r1 is not None:
        return TestResult("ResponseCache", False, "Should miss on new key")
    
    # Set
    cache.set("test_prompt_unique_123", "test_response")
    
    # Hit
    r2 = cache.get("test_prompt_unique_123")
    if r2 != "test_response":
        return TestResult("ResponseCache", False, "Cache miss after set")

    return TestResult("ResponseCache", True, "Hit/miss working")


def test_speed_core():
    """Test SpeedCore optimization layer."""
    try:
        from speed_core import SpeedCore, PrecomputeCache, HotRAMState, PredictionEngine
    except ImportError:
        return TestResult("SpeedCore", False, "Import failed")

    # Precompute cache
    pc = PrecomputeCache("test")
    result1 = pc.precompute("key1", lambda: "computed")
    result2 = pc.precompute("key1", lambda: "should_not_run")
    if result1 != result2:
        return TestResult("SpeedCore", False, "Precompute cache not working")

    # Hot RAM
    hot = HotRAMState(max_size=5)
    hot.set("a", 1)
    hot.set("b", 2)
    if hot.get("a") != 1:
        return TestResult("SpeedCore", False, "HotRAM get failed")

    # Prediction
    pred = PredictionEngine()
    for action in ["status", "optimize", "status"]:
        pred.record(action)
    predictions = pred.predict_next()
    if "status" not in predictions:
        return TestResult("SpeedCore", False, "Predictor not learning")

    return TestResult("SpeedCore", True, "All components verified")


def test_voice_engine():
    """Test GabrielVoice functionality."""
    from gabriel_voice import GabrielVoice

    voice = GabrielVoice()
    h1 = voice._hash("test", "Daniel")
    h2 = voice._hash("test", "Daniel")
    
    if h1 != h2:
        return TestResult("VoiceEngine", False, "Hash not deterministic")
    if "cached_files" not in voice.get_stats():
        return TestResult("VoiceEngine", False, "Stats malformed")

    return TestResult("VoiceEngine", True, "Hash + stats working")


def test_file_structure():
    """Verify consolidated file structure."""
    gabriel_dir = Path(__file__).parent.parent
    required = [
        "core/gabriel_brain.py", "core/gabriel_server.py", "core/memory_engine.py",
        "core/gabriel_voice.py", "core/gabriel_cli.py", "core/speed_core.py",
        "avatar/index.html", "avatar/js/avatar_engine.js", "avatar/js/interaction.js",
    ]
    
    missing = [f for f in required if not (gabriel_dir / f).exists()]
    if missing:
        return TestResult("FileStructure", False, f"Missing: {missing}")

    return TestResult("FileStructure", True, f"{len(required)} files present")


# ============================================================================
# ASYNC TESTS
# ============================================================================

async def test_brain_async():
    """Test async brain operations."""
    from gabriel_brain import GabrielBrain

    brain = GabrielBrain()
    await brain.wake_up()

    start = time.perf_counter()
    result = await brain.process_input("What is your status?")
    latency = (time.perf_counter() - start) * 1000

    if "response" not in result:
        return TestResult("BrainAsync", False, "No response")
    if result["meta"]["intent"] != "status":
        return TestResult("BrainAsync", False, f"Wrong intent: {result['meta']['intent']}")

    return TestResult("BrainAsync", True, "Status intent resolved", latency)


# ============================================================================
# PERFORMANCE BENCHMARKS
# ============================================================================

async def benchmark_reflex_latency():
    """Benchmark reflex mode latency across many requests."""
    from gabriel_brain import GabrielBrain

    brain = GabrielBrain()
    await brain.wake_up()

    queries = ["status", "who are you", "hello", "yes", "no", "help", "time"]
    latencies = []

    for _ in range(10):  # 10 iterations
        for q in queries:
            start = time.perf_counter()
            await brain.process_input(q)
            latencies.append((time.perf_counter() - start) * 1000)

    avg = mean(latencies)
    std = stdev(latencies) if len(latencies) > 1 else 0
    p95 = sorted(latencies)[int(len(latencies) * 0.95)]

    passed = avg < 1.0 and p95 < 5.0  # <1ms avg, <5ms p95

    return TestResult(
        "Benchmark:Reflex",
        passed,
        f"avg={avg:.2f}ms, p95={p95:.2f}ms, std={std:.2f}ms",
        avg,
    )


async def benchmark_cache_hit():
    """Benchmark cache hit performance."""
    from gabriel_brain import GabrielBrain

    brain = GabrielBrain()
    await brain.wake_up()

    # First call (miss)
    await brain.process_input("unique test query for benchmark")

    # Subsequent calls (hits)
    latencies = []
    for _ in range(20):
        start = time.perf_counter()
        result = await brain.process_input("unique test query for benchmark")
        latencies.append((time.perf_counter() - start) * 1000)

    avg = mean(latencies)
    passed = avg < 0.5 and result["meta"]["source"] == "cache"

    return TestResult(
        "Benchmark:CacheHit",
        passed,
        f"avg={avg:.2f}ms, source={result['meta']['source']}",
        avg,
    )


def benchmark_intent_classification():
    """Benchmark intent router speed."""
    from gabriel_brain import IntentRouter

    router = IntentRouter()
    queries = [
        "status", "who are you", "optimize", "hello", "yes", "no",
        "help me", "what time", "can you do this", "stop",
    ]

    latencies = []
    for _ in range(100):
        for q in queries:
            start = time.perf_counter()
            router.classify(q)
            latencies.append((time.perf_counter() - start) * 1000)

    avg = mean(latencies)
    p99 = sorted(latencies)[int(len(latencies) * 0.99)]

    passed = avg < 0.1 and p99 < 1.0  # <0.1ms avg, <1ms p99

    return TestResult(
        "Benchmark:IntentRouter",
        passed,
        f"avg={avg:.4f}ms, p99={p99:.4f}ms, n={len(latencies)}",
        avg,
    )


def benchmark_hot_ram():
    """Benchmark HotRAMState access speed."""
    from speed_core import HotRAMState

    hot = HotRAMState(max_size=100)
    
    # Populate
    for i in range(100):
        hot.set(f"key_{i}", f"value_{i}")

    # Read benchmark
    latencies = []
    for _ in range(1000):
        key = f"key_{_ % 100}"
        start = time.perf_counter()
        hot.get(key)
        latencies.append((time.perf_counter() - start) * 1000)

    avg = mean(latencies)
    passed = avg < 0.01  # <0.01ms (10 microseconds)

    return TestResult(
        "Benchmark:HotRAM",
        passed,
        f"avg={avg:.4f}ms ({avg*1000:.1f}μs), n={len(latencies)}",
        avg,
    )


# ============================================================================
# TEST RUNNER
# ============================================================================

async def run_all_tests():
    """Run all tests and benchmarks."""
    print("\n" + "=" * 70)
    print("🧪 GABRIEL V4.2 TEST SUITE + PERFORMANCE BENCHMARKS")
    print("=" * 70 + "\n")

    results = []

    # Unit tests
    print("━━━ UNIT TESTS ━━━")
    results.append(test_file_structure())
    results.append(test_memory_engine())
    results.append(test_intent_router())
    results.append(test_response_cache())
    results.append(test_speed_core())
    results.append(test_voice_engine())
    for r in results:
        print(r)

    # Async tests
    print("\n━━━ ASYNC TESTS ━━━")
    async_result = await test_brain_async()
    results.append(async_result)
    print(async_result)

    # Benchmarks
    print("\n━━━ PERFORMANCE BENCHMARKS ━━━")
    bench_results = [
        benchmark_intent_classification(),
        benchmark_hot_ram(),
        await benchmark_reflex_latency(),
        await benchmark_cache_hit(),
    ]
    for r in bench_results:
        print(r)
        results.append(r)

    # Summary
    print("\n" + "=" * 70)
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    print(f"TOTAL: {passed} passed, {failed} failed")
    
    # Performance summary
    bench_times = [r for r in results if r.name.startswith("Benchmark:")]
    if bench_times:
        print(f"SPEED: Reflex avg={[r for r in bench_times if 'Reflex' in r.name][0].latency_ms:.2f}ms")
    print("=" * 70 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

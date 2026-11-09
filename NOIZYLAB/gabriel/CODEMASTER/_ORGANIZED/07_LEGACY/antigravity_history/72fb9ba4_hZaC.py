#!/usr/bin/env python3
"""
Gabriel Test Suite V1.0
Verify all core components work correctly.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add core to path
CORE_DIR = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(CORE_DIR))


class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status}: {self.name}" + (f" - {self.message}" if self.message else "")


def test_memory_engine():
    """Test MemCell V4 functionality."""
    from memory_engine import MemCell

    mc = MemCell()

    # Test tracking
    mc.track("TEST", "TestSubject", {"key": "value"})

    # Test recall
    recall = mc.recall()
    if "MEMCELL V4" not in recall:
        return TestResult("MemoryEngine", False, "Recall format incorrect")

    # Test stats
    stats = mc.get_stats()
    if stats["version"] != "4.0":
        return TestResult("MemoryEngine", False, "Wrong version")

    # Test search
    results = mc.search_patterns("TestSubject")
    if not results:
        return TestResult("MemoryEngine", False, "Search failed")

    return TestResult("MemoryEngine", True, "All functions working")


def test_gabriel_brain():
    """Test GabrielBrain V4 functionality."""
    from gabriel_brain import GabrielBrain, IntentRouter, ResponseCache

    # Test IntentRouter (now returns tuple: intent, confidence)
    router = IntentRouter()
    intent, conf = router.classify("what is the status")
    assert intent == "status", f"Expected status, got {intent}"
    intent, _ = router.classify("who are you")
    assert intent == "who"
    intent, _ = router.classify("optimize the code")
    assert intent == "optimize"
    intent, _ = router.classify("hello there")
    assert intent == "greeting"
    intent, conf = router.classify("explain the theory of relativity in detail")
    assert intent == "query" and conf < 0.6, "Long query should have low confidence"

    # Test ResponseCache
    cache = ResponseCache()
    cache.set("test prompt", "test response")
    cached = cache.get("test prompt")
    if cached != "test response":
        return TestResult("GabrielBrain", False, "Cache not working")

    # Test Brain instantiation
    brain = GabrielBrain()
    status = brain.get_status()
    if status["version"] != "4.0":
        return TestResult("GabrielBrain", False, "Wrong version")

    return TestResult("GabrielBrain", True, "All components working")


async def test_brain_async():
    """Test async brain operations."""
    from gabriel_brain import GabrielBrain

    brain = GabrielBrain()
    await brain.wake_up()

    # Test process_input
    result = await brain.process_input("What is your status?")
    if "response" not in result:
        return TestResult("BrainAsync", False, "No response in result")

    if result["meta"]["intent"] != "status":
        return TestResult("BrainAsync", False, f"Wrong intent: {result['meta']['intent']}")

    return TestResult("BrainAsync", True, f"Latency: {result['meta']['latency_ms']}ms")


def test_voice_engine():
    """Test GabrielVoice functionality (without playing audio)."""
    from gabriel_voice import GabrielVoice

    voice = GabrielVoice()

    # Test hash generation
    h1 = voice._hash("test", "Daniel")
    h2 = voice._hash("test", "Daniel")
    if h1 != h2:
        return TestResult("VoiceEngine", False, "Hash not deterministic")

    # Test stats
    stats = voice.get_stats()
    if "cached_files" not in stats:
        return TestResult("VoiceEngine", False, "Stats malformed")

    return TestResult("VoiceEngine", True, "All functions working")


def test_file_structure():
    """Verify consolidated file structure."""
    gabriel_dir = Path(__file__).parent.parent
    required_dirs = ["core", "scripts", "docs", "avatar", "workers", "tests"]
    required_files = [
        "core/gabriel_brain.py",
        "core/gabriel_server.py",
        "core/memory_engine.py",
        "core/gabriel_voice.py",
        "core/gabriel_cli.py",
        "avatar/index.html",
        "avatar/js/avatar_engine.js",
        "avatar/js/interaction.js",
    ]

    missing_dirs = [d for d in required_dirs if not (gabriel_dir / d).is_dir()]
    if missing_dirs:
        return TestResult("FileStructure", False, f"Missing dirs: {missing_dirs}")

    missing_files = [f for f in required_files if not (gabriel_dir / f).exists()]
    if missing_files:
        return TestResult("FileStructure", False, f"Missing files: {missing_files}")

    return TestResult("FileStructure", True, "All files present")


async def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 60)
    print("🧪 GABRIEL V4 TEST SUITE")
    print("=" * 60 + "\n")

    results = []

    # Sync tests
    print("Running sync tests...")
    results.append(test_file_structure())
    results.append(test_memory_engine())
    results.append(test_gabriel_brain())
    results.append(test_voice_engine())

    # Async tests
    print("Running async tests...")
    results.append(await test_brain_async())

    # Report
    print("\n" + "-" * 60)
    print("RESULTS:")
    print("-" * 60)

    passed = 0
    failed = 0
    for r in results:
        print(r)
        if r.passed:
            passed += 1
        else:
            failed += 1

    print("-" * 60)
    print(f"Total: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Verification Script for Gabriel Voice
"""
import sys
import os
from pathlib import Path

# Ensure we can find the module
sys.path.append(str(Path.cwd() / "NOIZYLAB" / "PROJECTS_MASTER" / "GABRIEL_CORE"))

try:
    from gabriel_voice import GabrielVoice
except ImportError:
    print("❌ Failed to import GabrielVoice. Check paths.")
    sys.exit(1)

def test_voice():
    print("🧪 Testing Gabriel Voice Integration...")
    v = GabrielVoice()

    # 1. Test Speak (Non-blocking)
    print("  • Testing Speak (Background)...")
    v.speak("Initializing verification protocol.", block=False)

    # 2. Test Speak (Blocking)
    print("  • Testing Speak (Blocking)...")
    v.speak("Verification protocol active.", block=True)

    # 3. Test Ask (Interactive - we will mock input or just print prompt)
    # Since we can't easily mock input in this non-interactive run, we will just verify the method exists and prints correctly if we could.
    # actual asking would block the agent.
    if hasattr(v, 'ask'):
        print("  ✅ 'ask' method present.")
    else:
        print("  ❌ 'ask' method MISSING.")

    print("✅ Voice Module Loaded Successfully.")

if __name__ == "__main__":
    test_voice()

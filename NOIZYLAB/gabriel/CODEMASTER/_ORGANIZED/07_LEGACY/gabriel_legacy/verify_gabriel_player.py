#!/usr/bin/env python3
"""
Verification Script for Gabriel Player
"""
import sys
import time
from pathlib import Path

# Ensure we can find the module
sys.path.append(str(Path.cwd() / "NOIZYLAB" / "PROJECTS_MASTER" / "GABRIEL_CORE"))

try:
    from gabriel_player import GabrielPlayer
except ImportError:
    print("❌ Failed to import GabrielPlayer. Check paths.")
    sys.exit(1)

def test_player():
    print("🧪 Testing Gabriel Player Integration...")
    p = GabrielPlayer()

    # 1. Test Library Scan
    print("  • Scanning Library...")
    tracks = p.scan_library()
    print(f"    found {len(tracks)} tracks.")

    if not tracks:
         # Create a dummy silent wav for testing if no tracks exist?
         # Or play a system sound
         print("    ⚠️ No music files found. Falling back to System Sounds for test.")
         p.library_paths.append(Path("/System/Library/Sounds"))
         tracks = p.scan_library()
         print(f"    found {len(tracks)} tracks (System Sounds incl).")

    # 2. Test Play (Non-blocking)
    if tracks:
        target = tracks[0]
        print(f"  • Testing Playback: {target.name}...")
        p.play(target, block=False)
        time.sleep(2) # Listen for 2 seconds

        # 3. Test Stop
        print("  • Testing Stop...")
        p.stop()
        if not p.is_playing:
             print("    ✅ Stopped successfully.")
        else:
             print("    ❌ Failed to stop.")
    else:
        print("    ❌ No audio files available to test playback.")

    print("✅ Player Module Loaded Successfully.")

if __name__ == "__main__":
    test_player()

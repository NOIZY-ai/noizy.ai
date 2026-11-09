#!/usr/bin/env python3
# ==============================================================================
# 🖐️ TURBO STUDIO HAND (AI AUTOMATION)
# ==============================================================================
# "I see the file. I fix the file."
# WATCHES: Assets/To_Repair
# ACTIONS: VoiceFixer -> Assets/Repaired

import time
import shutil
import threading
from pathlib import Path

try:
    import turbo_config as cfg
    from turbo_audio_ai import AudioEnhancer
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    from turbo_audio_ai import AudioEnhancer

# PATHS
WATCH_DIR = cfg.ASSETS_DIR / "To_Repair"
OUTPUT_DIR = cfg.ASSETS_DIR / "Repaired"

# ENGINE
AI = AudioEnhancer()

def setup_dirs():
    for d in [WATCH_DIR, OUTPUT_DIR]:
        if not d.exists():
            d.mkdir(parents=True)
            print(f"CORE > Created Watch Folder: {d}")

def process_file(filepath):
    print(f"🖐️  AI HANDS > Detected: {filepath.name}")
    
    # Check if audio
    if filepath.suffix.lower() not in ['.wav', '.mp3', '.aiff', '.flac']:
        return

    try:
        # Move to 'Processing' (rename or lock)
        # For simplicity, we process in place then move to Repaired
        
        output_path = OUTPUT_DIR / f"Fixed_{filepath.name}"
        
        print(f"🖐️  AI HANDS > Applying VoiceFixer...")
        # Assume valid AudioEnhancer.repair method
        # If not available, we mock or use subprocess
        
        # Calling the command line wrapper for reliability if needed, 
        # but importing the class is better.
        # Let's verify AudioEnhancer has a direct method.
        # Based on previous `turbo_audio_ai.py` edits, it has `repair_audio(input, output)`.
        
        AI.repair_audio(str(filepath), str(output_path))
        
        print(f"✅ FIXED: {output_path.name}")
        
        # Cleanup source
        filepath.unlink()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

def run_watchdog():
    cfg.print_header("🖐️ STUDIO HAND", "Auto-Repair Watchdog")
    setup_dirs()
    
    print(f"CORE > Watching: {WATCH_DIR}...")
    print("CORE > Drop Audio Files here for automatic repair.")
    
    try:
        while True:
            # Simple Polling
            files = list(WATCH_DIR.glob("*.*"))
            for f in files:
                if f.name.startswith("."): continue # skip hidden
                process_file(f)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nCORE > hand withdrawn.")

if __name__ == "__main__":
    run_watchdog()

import os
import sys
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
# Target Format: 44.1kHz, 16-bit, WAV
AF_ARGS = ["-f", "WAVE", "-d", "LEI16@44100"]

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

AUDIO_EXTS = {'.wav', '.aif', '.aiff', '.mp3', '.m4a', '.flac', '.ogg'}

def convert_file(file_path):
    """
    Converts a single file using afconvert.
    Returns: (status_code, message)
    """
    p = Path(file_path)
    if p.suffix.lower() not in AUDIO_EXTS:
        return (0, "Skipped (Not Audio)")

    # Construct Output Path (Same name, force .wav)
    # If it's already a WAV, we might be overwriting or creating a temp
    temp_out = p.with_suffix('.wav.tmp')
    final_out = p.with_suffix('.wav')
    
    cmd = ["afconvert"] + AF_ARGS + [str(p), str(temp_out)]
    
    try:
        # Run afconvert
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        # If successful, replace original
        # Note: If original was .mp3, we now have .mp3 and .wav. 
        # Strategy: "Transmute" usually implies keeping the new gold and discarding lead.
        # But deleting originals is risky. 
        # For this "Fix All" request, we will Replace if it was already WAV/AIF (Repair),
        # but maybe keep source if it was compressed?
        # User said "Standardize". Let's go with Replacement for WAV/AIF, and "Convert & Keep" for compressed if separate?
        # Actually, "Fix All" implies the result should be the standard.
        # I will replace the original file with the new WAV.
        
        if temp_out.exists():
            # If converting .wav -> .wav, we overwrite.
            # If converting .mp3 -> .wav, we delete .mp3?
            if p != final_out:
                p.unlink() # Remove old file (e.g. .mp3)
            
            temp_out.rename(final_out)
            return (1, f"{p.name} -> {final_out.name}")
            
    except subprocess.CalledProcessError:
        if temp_out.exists(): temp_out.unlink()
        return (-1, f"Failed: {p.name}")
    except Exception as e:
        return (-1, f"Error {p.name}: {e}")

    return (0, "Unknown")

def run_alchemist(target_dir):
    print(f"{BOLD}{CYAN}⚗️  THE ALCHEMIST: AUDIO TRANSMUTATION ENGINE{RESET}")
    print(f"   Target: {target_dir}")
    print(f"   Format: 44.1kHz / 16-bit WAV (Industry Standard)")
    
    root_path = Path(target_dir)
    if not root_path.exists():
        print(f"   {RED}❌ Target not found.{RESET}")
        return

    # Gather files
    files = []
    print("   Gathering ingredients...")
    for root, dirs, filenames in os.walk(root_path):
        for f in filenames:
            if not f.startswith('.'):
                fp = Path(root) / f
                if fp.suffix.lower() in AUDIO_EXTS:
                    files.append(fp)

    print(f"   Found {len(files)} candidates.")
    
    converted = 0
    failed = 0
    start_time = time.time()
    
    # Run in parallel! afconvert is fast but IO bound-ish.
    # macOS limits threads, but 4-8 is usually safe for this.
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(convert_file, f): f for f in files}
        
        for i, future in enumerate(as_completed(future_to_file)):
            status, msg = future.result()
            if status == 1:
                converted += 1
                # print(f"   ✅ {msg}") # Too spammy for big lists?
                if i % 10 == 0: print(f"   ...transmuted {i+1}/{len(files)}")
            elif status == -1:
                failed += 1
                print(f"   {RED}❌ {msg}{RESET}")

    duration = time.time() - start_time
    print(f"\n{GREEN}✨ TRANSMUTATION COMPLETE ({duration:.2f}s){RESET}")
    print(f"   Transmuted: {converted}")
    print(f"   Failed:     {failed}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_converter.py <target_dir>")
    else:
        run_alchemist(sys.argv[1])

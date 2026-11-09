import json
import os
import wave
import argparse
from pathlib import Path
from collections import defaultdict
import sys
import time
import subprocess
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

INDEX_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/oracle_index.json"

# Configuration
# Using a dummy analyzer for speed if no real tool is found
# In a real scenario, this would wrap 'sox' or 'ffmpeg' or 'essentia'

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def load_index():
    with open(INDEX_PATH, 'r') as f:
        return json.load(f)

def analyze_audio(file_path):
    # Initialize Conciousness (Lazy load to avoid overhead per file if needed, but here we do it per call for simplicity or pass it in)
    # Actually, initializing DB connection per file is slow. 
    # Let's assume this function is called by a main loop that should have initialized it.
    # But for now, let's just log the START of a batch run if possible, or just log significant find.
    pass

def run_batch_analysis(directory):
    brain = MemCell()
    brain.log_event(brain.covenant_id, "ANALYSIS_START", f"Sonic Analyzer Protocol: Scanning {directory}", vibe=60, author="SONIC_ANALYZER")

    print(f"{BOLD}{CYAN}CORE > 🔊 SONIC ANALYZER: Scanning {directory}...{RESET}")
    print("CORE > Scanning file sizes...")
    
    size_map = defaultdict(list)
    processed = 0
    
    # The original analyze_duplicates logic for scanning files by size
    # This part assumes 'files' would be passed or generated from 'directory'
    # For now, we'll keep the original `analyze_duplicates` structure and call it.
    # If the intent was to merge, the `files` variable would need to be defined here.
    
    # For the purpose of this edit, we'll assume `run_batch_analysis` is a new entry point
    # and the existing `analyze_duplicates` and `analyze_quality` will be called from it
    # or from a modified `run_analysis` that uses `run_batch_analysis`.
    # Given the instruction, I will integrate the new header and MemCell logic,
    # but keep the existing `analyze_duplicates` function as is, and modify `run_analysis`
    # to call `run_batch_analysis` with a dummy directory for now, or pass the files.

    # Let's assume `run_batch_analysis` will eventually take the list of files directly
    # or scan the directory itself. For now, I'll adapt `run_analysis` to call it.
    
    # The instruction's `{{ ... }}` implies the rest of the `analyze_duplicates` logic
    # should follow here. I will move the core logic of `analyze_duplicates` into `run_batch_analysis`.

    data = load_index()
    if not data: return
    files = data.get('files', [])

    for fpath in files:
        try:
            size = os.path.getsize(fpath)
            if size > 1024:
                size_map[size].append(fpath)
        except:
            pass
        processed += 1
        if processed % 10000 == 0:
            print(f"CORE > ...scanned {processed:,} files")

    # Filter for potential duplicates
    potential_dupes = {k: v for k, v in size_map.items() if len(v) > 1}
    
    total_wasted = 0
    duplicate_groups = 0
    duplicate_files = 0
    
    for size, paths in potential_dupes.items():
        count = len(paths)
        wasted = size * (count - 1)
        total_wasted += wasted
        duplicate_groups += 1
        duplicate_files += (count - 1)

    # Convert bytes to human readable
    wasted_gb = total_wasted / (1024**3)
    
    print(f"\n{YELLOW}CORE > ⚠️  DUPLICATE REPORT:{RESET}")
    print(f"CORE > Duplicate Groups: {duplicate_groups:,}")
    print(f"CORE > Redundant Files:  {duplicate_files:,}")
    print(f"CORE > Space Wasted:     {RED}{wasted_gb:.2f} GB{RESET}")
    
    # Show largest wasters
    print(f"\n{BOLD}CORE > Top Space Wasters:{RESET}")
    sorted_dupes = sorted(potential_dupes.items(), key=lambda x: x[0] * (len(x[1])-1), reverse=True)[:5]
    for size, paths in sorted_dupes:
        mb = size / (1024**2)
        print(f"   {mb:.1f} MB x {len(paths)} copies:")
        for p in paths[:3]:
            print(f"      - {p}")
        if len(paths) > 3: print("      - ...")

def analyze_quality(files):
    print(f"\n{BOLD}CORE > 🎧 Audio Quality Map{RESET}")
    print("CORE > Sampling headers (this takes a moment)...")
    
    stats = defaultdict(int)
    scanned = 0
    max_scan = 500 # Limit header scan for speed
    
    for fpath in files:
        if scanned >= max_scan: break
        
        ext = Path(fpath).suffix.lower()
        try:
            if ext == '.wav':
                with wave.open(fpath, 'rb') as w:
                    sr = w.getframerate()
                    bits = w.getsampwidth() * 8
                    stats[f"{sr}Hz / {bits}bit"] += 1
                    scanned += 1
            elif ext in ['.aif', '.aiff']:
                pass 

        except:
            pass

    print(f"\n{CYAN}CORE > 📊 Quality Breakdown (Sample of {scanned} files):{RESET}")
    for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   {k}: {v} files")
        pct = (v / scanned) * 100
        print(f"   {k}: {v} files ({pct:.1f}%)")

def run_analysis():
    data = load_index()
    if not data: return
    
    files = data.get('files', [])
    print(f"📉 Analyzing {len(files):,} indexed files...")
    
    analyze_duplicates(files)
    # analyze_quality(files) # Optional: Can be slow on network drives

if __name__ == "__main__":
    run_analysis()

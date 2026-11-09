import json
import os
import wave
import aifc
import argparse
from pathlib import Path
from collections import defaultdict

INDEX_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/oracle_index.json"

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def load_index():
    try:
        with open(INDEX_PATH, 'r') as f:
            return json.load(f)
    except:
        print("❌ Oracle Database not found.")
        return None

def analyze_duplicates(files):
    print(f"\n{BOLD}🔍 Duplicate Detection (Size-based){RESET}")
    print("   Scanning file sizes...")
    
    size_map = defaultdict(list)
    processed = 0
    
    for fpath in files:
        try:
            size = os.path.getsize(fpath)
            if size > 1024: # Ignore tiny files < 1KB
                size_map[size].append(fpath)
        except:
            pass
        processed += 1
        if processed % 10000 == 0:
            print(f"   ...scanned {processed:,} files")

    # Filter for potential duplicates
    potential_dupes = {k: v for k, v in size_map.items() if len(v) > 1}
    
    total_wasted = 0
    duplicate_groups = 0
    duplicate_files = 0
    
    for size, paths in potential_dupes.items():
        # Heuristic: If size matches exactly to the byte, robust chance it's a dupe for audio samples
        # For strictness we'd hash, but for speed on PB scale, size is good 1st pass
        count = len(paths)
        wasted = size * (count - 1)
        total_wasted += wasted
        duplicate_groups += 1
        duplicate_files += (count - 1)

    # Convert bytes to human readable
    wasted_gb = total_wasted / (1024**3)
    
    print(f"\n{YELLOW}⚠️  DUPLICATE REPORT:{RESET}")
    print(f"   Duplicate Groups: {duplicate_groups:,}")
    print(f"   Redundant Files:  {duplicate_files:,}")
    print(f"   Space Wasted:     {RED}{wasted_gb:.2f} GB{RESET}")
    
    # Show largest wasters
    print(f"\n{BOLD}Top Space Wasters:{RESET}")
    sorted_dupes = sorted(potential_dupes.items(), key=lambda x: x[0] * (len(x[1])-1), reverse=True)[:5]
    for size, paths in sorted_dupes:
        mb = size / (1024**2)
        print(f"   {mb:.1f} MB x {len(paths)} copies:")
        for p in paths[:3]:
            print(f"      - {p}")
        if len(paths) > 3: print("      - ...")

def analyze_quality(files):
    print(f"\n{BOLD}🎧 Audio Quality Map{RESET}")
    print("   Sampling headers (this takes a moment)...")
    
    stats = defaultdict(int)
    scanned = 0
    max_scan = 500 # Limit header scan for speed in this demo, or remove for full
    
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
                pass # aifc removed in Python 3.13

        except:
            pass

    print(f"\n{CYAN}📊 Quality Breakdown (Sample of {scanned} files):{RESET}")
    for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True):
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

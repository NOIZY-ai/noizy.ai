# ==============================================================================
# 🦅 GABRIEL ALLEGIANCE (SYSTEM LEADER)
# ==============================================================================
# This script operates under the command of GABRIEL.
# PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE
# ==============================================================================

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
    import turbo_config as cfg
    import turbo_gabriel
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel
    from turbo_memcell import MemCell

INDEX_PATH = cfg.SCRIPTS_DIR.parent / "Database" / "oracle_index.json"

def load_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'r') as f:
            return json.load(f)
    return None

def analyze_duplicates(files):
    cfg.system_log("Scanning file sizes...", "INFO")
    
    size_map = defaultdict(list)
    processed = 0
    
    for fpath in files:
        try:
            if not os.path.exists(fpath): continue
            size = os.path.getsize(fpath)
            if size > 1024:
                size_map[size].append(fpath)
        except:
            pass
        processed += 1
        if processed % 10000 == 0:
            print(f"CORE > ...scanned {processed:,} files", end='\r')

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
    
    print(f"\n{cfg.YELLOW}CORE > ⚠️  DUPLICATE REPORT:{cfg.RESET}")
    print(f"CORE > Duplicate Groups: {duplicate_groups:,}")
    print(f"CORE > Redundant Files:  {duplicate_files:,}")
    print(f"CORE > Space Wasted:     {cfg.RED}{wasted_gb:.2f} GB{cfg.RESET}")
    
    # Show largest wasters
    print(f"\n{cfg.BOLD}CORE > Top Space Wasters:{cfg.RESET}")
    sorted_dupes = sorted(potential_dupes.items(), key=lambda x: x[0] * (len(x[1])-1), reverse=True)[:5]
    for size, paths in sorted_dupes:
        mb = size / (1024**2)
        print(f"   {mb:.1f} MB x {len(paths)} copies:")
        for p in paths[:3]:
            print(f"      - {p}")
        if len(paths) > 3: print("      - ...")

def analyze_quality(files):
    cfg.print_header("🎧 Audio Quality Map")
    cfg.system_log("Sampling headers (this takes a moment)...")
    
    stats = defaultdict(int)
    scanned = 0
    max_scan = 500 # Limit header scan for speed
    
    for fpath in files:
        if scanned >= max_scan: break
        
        ext = Path(fpath).suffix.lower()
        try:
            if os.path.exists(fpath):
                if ext == '.wav':
                    with wave.open(fpath, 'rb') as w:
                        sr = w.getframerate()
                        bits = w.getsampwidth() * 8
                        stats[f"{sr}Hz / {bits}bit"] += 1
                        scanned += 1
        except:
            pass

    print(f"\n{cfg.CYAN}CORE > 📊 Quality Breakdown (Sample of {scanned} files):{cfg.RESET}")
    for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   {k}: {v} files")
        pct = (v / scanned) * 100
        print(f"   {k}: {v} files ({pct:.1f}%)")

def run_analysis():
    brain = MemCell()
    brain.log_event(brain.covenant_id, "ANALYSIS_START", f"Sonic Analyzer Protocol Initiated", vibe=75, author="SONIC_ANALYZER")

    cfg.print_header("🔊 SONIC ANALYZER", "INITIATED")

    # Fallback if no index: Scan DB or Scan local lib?
    # For now, simplistic fallback to known path
    lib_path = Path.expanduser(Path("~/Universal/Library"))
    files = []
    
    data = load_index()
    if data:
        files = data.get('files', [])
        cfg.system_log(f"Loaded {len(files):,} files from Oracle Index.", "SUCCESS")
    elif lib_path.exists():
        cfg.system_log(f"Index not found. Scanning {lib_path} directly...", "WARN")
        for root, dirs, f_names in os.walk(lib_path):
             for f in f_names:
                 if not f.startswith('.'):
                     files.append(str(Path(root) / f))
    else:
        cfg.system_log("No library or index found.", "ERROR")
        return

    cfg.system_log(f"Analyzing {len(files):,} files...", "INFO")
    
    analyze_duplicates(files)
    # analyze_quality(files) # Optional, kept commented out for speed unless requested

if __name__ == "__main__":
    try:
        run_analysis()
    except KeyboardInterrupt:
        print("\nCORE > Analysis Aborted.")

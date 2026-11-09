import os
import json
import re
import wave
import struct
import time
import sys
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import turbo_config as cfg
    import turbo_prompts as prompts
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_prompts as prompts

# Identity
NAME = "ENGR K.E.I.T.H." # Knowledge Engine for Intelligent Track Harmonization
VERSION = "36.0"

# Configuration
MUSIC_ROOT = Path.expanduser(Path("~/Universal/Library/Music"))
MANIFEST_PATH = Path.expanduser(Path("~/Universal/universe_manifest.json"))
THREADS = max(4, (os.cpu_count() or 4) * 2)

# Colors (use cfg if available)
CYAN = cfg.CYAN if hasattr(cfg, 'CYAN') else '\033[96m'
GREEN = cfg.GREEN if hasattr(cfg, 'GREEN') else '\033[92m'
YELLOW = cfg.YELLOW if hasattr(cfg, 'YELLOW') else '\033[93m'
RED = cfg.RED if hasattr(cfg, 'RED') else '\033[91m'
RESET = cfg.RESET if hasattr(cfg, 'RESET') else '\033[0m'
BOLD = cfg.BOLD if hasattr(cfg, 'BOLD') else '\033[1m'
BOLD = '\033[1m'

# Logic
TRACK_NUM_REGEX = re.compile(r"^(\d+)")

def get_audio_info(fpath):
    try:
        if fpath.suffix.lower() == '.wav':
             with wave.open(str(fpath), 'rb') as w:
                return {
                    "rate": w.getframerate(),
                    "width": w.getsampwidth() * 8, # bits
                    "channels": w.getnchannels(),
                    "frames": w.getnframes(),
                    "duration": w.getnframes() / float(w.getframerate())
                }
    except: pass
    return None

def analyze_album(album_path):
    report = {
        "path": str(album_path),
        "tracks": [],
        "issues": [],
        "integrity_score": 100
    }
    
    files = [f for f in album_path.iterdir() if f.name.lower().endswith(('.wav', '.mp3', '.aif', '.flac', '.m4a')) and not f.name.startswith('.')]
    files.sort(key=lambda x: x.name)
    
    if not files: return None

    # Format Check
    formats = set()
    rates = set()
    track_nums = []
    
    for f in files:
        info = get_audio_info(f)
        meta = {
            "name": f.name,
            "size": f.stat().st_size,
            "info": info
        }
        
        # Track Number Logic
        match = TRACK_NUM_REGEX.match(f.name)
        if match:
            t_num = int(match.group(1))
            track_nums.append(t_num)
            meta["track_num"] = t_num
        
        if info:
            formats.add(f"{info['rate']}Hz/{info['width']}bit")
            rates.add(info['rate'])
            
        report["tracks"].append(meta)

    # Integrity Analysis
    if len(formats) > 1:
        report["issues"].append(f"Inconsistent Formats: {list(formats)}")
        report["integrity_score"] -= 20
        
    if track_nums:
        track_nums.sort()
        # Check for gaps
        # Assuming starts at 1
        expected = list(range(track_nums[0], track_nums[-1] + 1))
        missing = [t for t in expected if t not in track_nums]
        if missing:
             report["issues"].append(f"Missing Tracks: {missing}")
             report["integrity_score"] -= (10 * len(missing))

    return report

def generate_manifest(root_dir):
    print(f"{BOLD}{CYAN}CORE > 👷 ENGR KEITH: BUILDING MANIFEST...{RESET}")
    print(f"CORE > Root: {root_dir}")
    
    universe = {
        "system": "MC96ECOUNIVERSE",
        "agent": f"{NAME} v{VERSION}",
        "timestamp": datetime.now().isoformat(),
        "library": {
            "music": [],
            "stats": {"albums": 0, "tracks": 0, "issues": 0}
        }
    }
    
    albums = []
    for root, dirs, files in os.walk(root_dir):
        # Heuristic: If folder contains audio files, it's an album
        has_audio = any(f.lower().endswith(('.wav', '.mp3', '.flac')) for f in files)
        if has_audio:
            albums.append(Path(root))
            
    print(f"CORE > Analyzing {len(albums)} Albums...")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_album = {executor.submit(analyze_album, a): a for a in albums}
        
        for i, future in enumerate(as_completed(future_to_album)):
            res = future.result()
            if res:
                universe["library"]["music"].append(res)
                universe["library"]["stats"]["albums"] += 1
                universe["library"]["stats"]["tracks"] += len(res["tracks"])
                if res["issues"]:
                    universe["library"]["stats"]["issues"] += len(res["issues"])
                    print(f"CORE > {YELLOW}⚠ Issue in {Path(res['path']).name}: {res['issues']}{RESET}")
            
            if (i+1) % 50 == 0:
                print(f"CORE > ...scanned {i+1}...", end='\r')

    # Save Manifest
    try:
        with open(MANIFEST_PATH, 'w') as f:
            json.dump(universe, f, indent=2)
        print(f"\n{GREEN}CORE > ✨ MANIFEST GENERATED: {MANIFEST_PATH}{RESET}")
        print(f"CORE > Albums: {universe['library']['stats']['albums']}")
        print(f"CORE > Tracks: {universe['library']['stats']['tracks']}")
        print(f"CORE > Issues: {universe['library']['stats']['issues']}")
    except Exception as e:
        print(f"\n{RED}CORE > ❌ Manifest Failed: {e}{RESET}")

if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else MUSIC_ROOT
    if target.exists():
        generate_manifest(target)
    else:
        print(f"CORE > {RED}No Music Library found at {target}{RESET}")

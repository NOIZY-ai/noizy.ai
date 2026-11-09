import os
import sys
import argparse
import time
import json
from pathlib import Path
from datetime import datetime

# NOIZYLAB AUDIO PROBE v1
# "Deep Scan" Module
# Usage: python3 deep_audio_scan.py --root /Volumes/Name

AUDIO_EXTENSIONS = {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg', '.m4a'}
PROJECT_EXTENSIONS = {'.logicx', '.als', '.ptx', '.cpr', '.flp'}

def deep_scan(root_path, output_file):
    print(f"NOIZYLAB DEEP SCAN INITIATED: {root_path}")
    print("------------------------------------------------")
    
    stats = {
        "audio_files": 0,
        "projects": 0,
        "total_size_gb": 0.0,
        "formats": {},
        "libraries": set()
    }
    
    scan_log = []
    start_time = time.time()
    
    try:
        for root, dirs, files in os.walk(root_path):
            # Identifying Libraries based on folder structure
            if "Samples" in root or "Loops" in root:
                stats["libraries"].add(root)
                
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                full_path = os.path.join(root, file)
                
                if ext in AUDIO_EXTENSIONS:
                    stats["audio_files"] += 1
                    stats["formats"][ext] = stats["formats"].get(ext, 0) + 1
                    try:
                        size = os.path.getsize(full_path)
                        stats["total_size_gb"] += size / (1024**3)
                    except:
                        pass
                        
                    # Visual pulse for large operations
                    if stats["audio_files"] % 1000 == 0:
                        print(f"  -> Indexed {stats['audio_files']} audio artifacts...")
                        
                elif ext in PROJECT_EXTENSIONS:
                    stats["projects"] += 1
                    scan_log.append(f"[PROJECT] {file} found in {root}")
                    print(f"  -> FOUND PROJECT: {file}")

    except KeyboardInterrupt:
        print("\n!!! SCAN INTERRUPTED BY USER.")
        
    duration = time.time() - start_time
    
    # Report Generation
    print("------------------------------------------------")
    print("SCAN COMPLETE.")
    print(f"Time Elapsed: {duration:.2f} seconds")
    print(f"Audio Files Detected: {stats['audio_files']}")
    print(f"DAW Projects Detected: {stats['projects']}")
    print(f"Total Audio Mass: {stats['total_size_gb']:.2f} GB")
    print("Formats Breakdown:")
    for fmt, count in stats["formats"].items():
        print(f"  - {fmt}: {count}")
        
    # Save Report
    with open(output_file, "w") as f:
        json.dump(stats, f, default=list, indent=4)
        f.write("\n")
        f.write("\n".join(scan_log))
        
    print(f"Telemtry saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NoizyLab Deep Audio Scan")
    parser.add_argument("--root", help="Root directory to scan", required=True)
    parser.add_argument("--out", help="Output report file", default="noizylab_scan_report.json")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.root):
        print(f"CRITICAL ERROR: Path {args.root} does not exist or is not mounted.")
        sys.exit(1)
        
    deep_scan(args.root, args.out)

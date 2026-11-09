#!/usr/bin/env python3
"""
turbo_fishnet.py
The Global Fishnet.
Scans the universe for Heavy Media ("Big Fish") effectively.
Daily Catch Protocol.
"""
import os
import sys
import shutil
import datetime
import subprocess
from pathlib import Path

# Configuration
SEARCH_DIRS = [
    Path.home() / "NOIZYLAB",
    Path.home() / "Documents/PROJECTS"
]
TARGET_EXTENSIONS = {
    ".nki", ".nkm", ".nkc", ".nicnt", # Kontakt
    ".nkx", ".ncw",                   # Kontakt Samples
    ".wav", ".aif", ".aiff", ".flac", # Audio
    ".mp4", ".mov", ".mkv", ".avi",   # Video
    ".dmg", ".iso", ".img",           # Disk Images
    ".logicx", ".zip", ".tar.gz"      # Archives/Projects
}
ARCHIVE_ROOT = Path("/Volumes/HP-OMEN/ARCHIVE") # Default if mounted
LOCAL_ARCHIVE = Path.home() / "NOIZYLAB/_ARCHIVE"

def get_size_mb(path):
    return path.stat().st_size / (1024 * 1024)

def scan_ocean():
    print("🌊 CASTING THE GLOBAL FISHNET...")
    print(f"   Targets: {', '.join(TARGET_EXTENSIONS)}")
    
    big_fish = []
    total_size = 0
    
    for root_dir in SEARCH_DIRS:
        if not root_dir.exists(): continue
        
        for path in root_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in TARGET_EXTENSIONS:
                # Filter out existing archives to avoid re-catching
                if "_ARCHIVE" in str(path): continue
                
                size = get_size_mb(path)
                if size > 10: # Only catch fish > 10MB (Minnows go free)
                    big_fish.append((path, size))
                    total_size += size
                    print(f"   🐟 CAUGHT: {path.name} ({size:.1f} MB)")

    print("-" * 40)
    print(f"🦈 TOTAL CATCH: {len(big_fish)} Fish")
    print(f"⚖️  TOTAL WEIGHT: {total_size:.1f} MB")
    print("-" * 40)
    return big_fish

def archive_catch(fish_list):
    dest_root = ARCHIVE_ROOT if ARCHIVE_ROOT.exists() else LOCAL_ARCHIVE
    dest_root.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 ARCHIVING TO: {dest_root}")
    
    for fish, size in fish_list:
        # Create relative structure in archive
        try:
            rel_path = fish.relative_to(Path.home())
        except ValueError:
            rel_path = fish.name
            
        dest_path = dest_root / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"   -> Moving {fish.name}...")
        try:
            shutil.move(str(fish), str(dest_path))
        except Exception as e:
            print(f"   ❌ FAILED to move {fish.name}: {e}")

    print("✨ DECK CLEARED.")

def install_cron():
    """Installs daily cron job at 4AM."""
    script_path = Path(__file__).resolve()
    # Cron line: 0 4 * * * /usr/bin/python3 /path/to/script.py --scan >> /path/to/log
    cron_cmd = f"0 4 * * * /usr/bin/python3 {script_path} --scan >> {Path.home()}/NOIZYLAB/logs/fishnet.log 2>&1"
    
    # Check if exists
    current_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    if str(script_path) in current_cron:
        print("✅ Fishnet Cron already active.")
        return

    # Add
    new_cron = current_cron + "\n" + cron_cmd + "\n"
    proc = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(input=new_cron)
    
    if proc.returncode == 0:
        print("✅ FISHNET SCHEDULED: Daily @ 04:00 AM")
    else:
        print(f"❌ Cron Install Failed: {err}")

def main():
    if len(sys.argv) > 1:
        if "--archive" in sys.argv:
            fish = scan_ocean()
            archive_catch(fish)
            return
        if "--install-cron" in sys.argv:
            install_cron()
            return
            
    # Configuration Updates for Kontakt Mode
    if "--kontakt-only" in sys.argv:
        print("🎹 KONTAKT MODE ENGAGED. Scanning for Instruments & Samples...")
        # Override extensions for Kontakt ecosystem
        global TARGET_EXTENSIONS
        TARGET_EXTENSIONS = {
            ".nki", ".nkm", ".nkc", ".nicnt", # Instruments/Banks
            ".nkx", ".ncw", ".wav", ".aif"    # Samples (Compressed/Uncompressed)
        }

    scan_ocean()
    print("\nOptions: --archive (Move files), --install-cron (Schedule daily), --kontakt-only (Kontakt Analysis)")

if __name__ == "__main__":
    main()

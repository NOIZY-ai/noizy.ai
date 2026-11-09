import os
import json
import shutil
import time
import sys
import argparse

# ADD CONFIG PATH
sys.path.append('/Volumes/6TB/Sample_Libraries')
try:
    import mc96_config as config
except ImportError:
    print("❌ Error: Could not import mc96_config.py. Make sure /Volumes/6TB/Sample_Libraries is accessible.")
    sys.exit(1)

# CONFIG
DATA_FILE = "/Users/m2ultra/.gemini/mc96_forensics_data.json"
TRASH_DIR = os.path.join(config.MC96_ROOT, "_MC96_QUALITY_UPGRADE_TRASH")
LOG_FILE = "/Users/m2ultra/.gemini/mc96_upgrade_log.txt"

# PATH PREFERENCE SCORING
# Higher score = Better location to keep
PREFERRED_KEYWORDS = ["Original", "Library", "Kits", "Instruments", "Samples", "WAV", "24bit"]
PENALIZED_KEYWORDS = ["Recovered", "Backup", "Copy", "Duplicate", "Old", "Untitled"]

def score_path(path):
    score = 0
    for kw in PREFERRED_KEYWORDS:
        if kw.lower() in path.lower(): score += 1
    for kw in PENALIZED_KEYWORDS:
        if kw.lower() in path.lower(): score -= 2
    # penalize depth? No, deep structure is often good.
    return score

def load_registry():
    print("⏳ Loading Registry...")
    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: Data file not found at {DATA_FILE}")
        print("Please run a forensics scan first (or check the archive).")
        sys.exit(1)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def upgrade_library(dry_run=False, auto_confirm=False):
    registry = load_registry()
    
    if dry_run:
        print("🔍 DRY RUN MODE: No files will be moved.")
    else:
        if not os.path.exists(TRASH_DIR):
            os.makedirs(TRASH_DIR)
        
    log = None
    if not dry_run:
        log = open(LOG_FILE, 'w')
    
    total_upgrades = 0
    total_deletions = 0
    space_saved = 0
    
    print(f"🚀 STARTING QUALITY UPGRADE & CONSOLIDATION")
    if not dry_run:
        print(f"🗑️ Replaced/Trash files will move to: {TRASH_DIR}")
    
    for filename, versions in registry.items():
        if len(versions) < 2:
            continue
            
        # Sort versions by Quality Score (Desc), then Path Score (Desc)
        # We want the HIGHEST QUALITY file to be the Source
        # And we want the BEST LOCATION to be the Destination
        
        # 1. Identify valid candidates (some might be removed already)
        valid_versions = [v for v in versions if os.path.exists(v['path'])]
        if len(valid_versions) < 2:
            continue
            
        # 2. Find BEST QUALITY asset (The Content Winner)
        best_quality = max(valid_versions, key=lambda x: x['quality_score'])
        
        # 3. Find BEST LOCATION (The Structural Winner)
        # We only consider locations that currently hold *some* version of this file
        best_location_ver = max(valid_versions, key=lambda x: score_path(x['path']))
        target_path = best_location_ver['path']
        
        source_path = best_quality['path']
        
        # LOGIC:
        # We want 'target_path' to exist, containing the content of 'source_path'.
        # All other paths should be removed (moved to trash).
        
        for v in valid_versions:
            current_path = v['path']
            
            # CASE A: This is the Keeper Path
            if current_path == target_path:
                # content check: is it already the best quality?
                if current_path != source_path and v['quality_score'] < best_quality['quality_score']:
                    # UPGRADE IT!
                    msg = f"[UPGRADE] {current_path} ({v['quality_score']}) replaced by {source_path} ({best_quality['quality_score']})"
                    print(msg)
                    if not dry_run and log:
                        log.write(msg + "\n")
                        
                        # Move old to trash
                        trash_path = os.path.join(TRASH_DIR, os.path.basename(current_path) + f"_{int(time.time())}.old")
                        shutil.move(current_path, trash_path)
                        
                        # Copy best content here
                        shutil.copy2(source_path, current_path)
                    
                    total_upgrades += 1
                else:
                    # It's already the best content (or the source itself), stay put.
                    pass
            
            # CASE B: This is a Redundant Path (Duplicate to be removed)
            else:
                # Move to trash
                msg = f"[DELETE] Unwanted Duplicate: {current_path}"
                # print(msg) # verbose
                if not dry_run and log:
                    log.write(msg + "\n")
                    
                    trash_path = os.path.join(TRASH_DIR, os.path.basename(current_path) + f"_{int(time.time())}_DUP")
                    shutil.move(current_path, trash_path)
                
                total_deletions += 1
                space_saved += v['size']

    if not dry_run and log:
        log.close()
        
    print(f"\n✅ CONSOLIDATION COMPLETE ({'DRY RUN' if dry_run else 'LIVE'})")
    print(f"Moves/Deletions: {total_deletions}")
    print(f"Quality Upgrades: {total_upgrades}")
    print(f"Reclaimed Space: {space_saved / (1024*1024):.2f} MB")
    if not dry_run:
        print(f"Log: {LOG_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consolidate duplicate files based on quality and path.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate changes without moving files.")
    parser.add_argument("--auto-confirm", action="store_true", help="Run without asking for confirmation.")
    args = parser.parse_args()
    
    upgrade_library(dry_run=args.dry_run, auto_confirm=args.auto_confirm)

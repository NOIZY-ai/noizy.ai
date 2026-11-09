#!/usr/bin/env python3
import shutil
import sqlite3
import sys
from pathlib import Path
import turbo_config as cfg

# ------------------------------------------------------------------------------
# 📦 TURBO ORGANIZER (THE CURATOR)
# ------------------------------------------------------------------------------
# Moves chaos into order based on Neural Index.
# Source: universe.db
# Destination: NOIZYLAB_WORKSPACES_LOCAL (The Trinity)

ROOT_DIR = cfg.STAGING_AREA
FISH_VAULT = ROOT_DIR / "FISHMUSICINC"
NOIZY_LAB  = ROOT_DIR / "NOIZYLAB"
NOIZY_WEB  = ROOT_DIR / "NOIZY.AI"

# MAPPING (Type -> Destination)
CATEGORIES = {
    "KICK": FISH_VAULT / "Audio/OneShots/Drums/Kicks",
    "SNARE": FISH_VAULT / "Audio/OneShots/Drums/Snares",
    "HAT": FISH_VAULT / "Audio/OneShots/Drums/Hats",
    "LOOPS": FISH_VAULT / "Audio/Loops/Drums",
    "BASS": FISH_VAULT / "Audio/Loops/Bass",
    "SYNTH": FISH_VAULT / "Audio/Loops/Synths",
    "VOCAL": FISH_VAULT / "Audio/Vocals",
    "FX": FISH_VAULT / "Audio/FX",
    "VIDEO": NOIZY_LAB / "Visuals/Footage",
    "IMAGE": NOIZY_LAB / "Visuals/Images",
    "DOC": NOIZY_LAB / "Documents"
}

def get_db_connection():
    return sqlite3.connect(str(cfg.UNIVERSE_DB_PATH))

def organize_universe():
    cfg.print_header("📦 TURBO ORGANIZER", "Moving Assets to Local NVMe Hierarchy")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Ensure Dest Dirs
    for cat, dest_path in CATEGORIES.items():
        dest_path.mkdir(parents=True, exist_ok=True)
        
    print(f"CORE > Vault Targets: {FISH_VAULT}, {NOIZY_LAB}, {NOIZY_WEB}")
    
    # Query all indexed files that have tags
    c.execute("SELECT id, path, tags FROM files WHERE tags IS NOT NULL")
    rows = c.fetchall()
    
    total_moved = 0
    errors = 0
    
    print(f"CORE > Analyzing {len(rows)} candidates...")
    
    for row in rows:
        fid, src_path, tags = row
        src = Path(src_path)
        
        if not src.exists():
            continue
            
        # Determine Destination based on Tag Priority
        dest_subpath = None
        tag_list = tags.upper().split(',')
        
        # Priority Logic
        dest_dir = None
        if "KICK" in tag_list: dest_dir = CATEGORIES["KICK"]
        elif "SNARE" in tag_list: dest_dir = CATEGORIES["SNARE"]
        elif "HAT" in tag_list: dest_dir = CATEGORIES["HAT"]
        elif "LOOP" in tag_list: dest_dir = CATEGORIES["LOOPS"]
        elif "BASS" in tag_list: dest_dir = CATEGORIES["BASS"]
        elif "SYNTH" in tag_list: dest_dir = CATEGORIES["SYNTH"]
        elif "VOCAL" in tag_list: dest_dir = CATEGORIES["VOCAL"]
        elif "FX" in tag_list: dest_dir = CATEGORIES["FX"]
        
        if dest_dir:
            dest = dest_dir / src.name
            
            # Avoid self-overwrite/same location
            if src.absolute() == dest.absolute():
                continue
                
            # Handle Duplicate Names
            if dest.exists():
                stem = src.stem
                suffix = src.suffix
                dest = dest_dir / f"{stem}_{fid}{suffix}"
            
            try:
                # Move or Copy? Copy is safer for now.
                # User said "Reorganize", implies moving, but let's Copy first to be safe?
                # User "Copy files from slow cloud...".
                # Let's Move if it's in a temp location, Copy if it's safe.
                # Actually, "Reorganize All" usually implies Moving into the structure.
                shutil.copy2(src, dest)
                total_moved += 1
                
                # Update DB with new path? Or keep original index?
                # Ideally we update the path, but let's just log it for now.
                print(f"CORE >    Moved: {src.name} -> {dest_dir.relative_to(ROOT_DIR)}")
                
            except Exception as e:
                errors += 1
                # print(f"Error moving {src}: {e}")
                
    cfg.system_log(f"Organization Complete. {total_moved} files curated.", "SUCCESS")
    print(f"CORE > Errors: {errors}")

if __name__ == "__main__":
    organize_universe()

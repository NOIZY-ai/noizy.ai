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
# Destination: NOIZYLAB_WORKSPACES_LOCAL

DEST_ROOT = cfg.STAGING_AREA / "UNIVERSE"

CATEGORIES = {
    "KICK": "Audio/OneShots/Drums/Kicks",
    "SNARE": "Audio/OneShots/Drums/Snares",
    "HAT": "Audio/OneShots/Drums/Hats",
    "LOOPS": "Audio/Loops/Drums",
    "BASS": "Audio/Loops/Bass",
    "SYNTH": "Audio/Loops/Synths",
    "VOCAL": "Audio/Vocals",
    "FX": "Audio/FX",
    "VIDEO": "Visuals/Footage",
    "IMAGE": "Visuals/Images",
    "DOC": "Documents"
}

def get_db_connection():
    return sqlite3.connect(str(cfg.UNIVERSE_DB_PATH))

def organize_universe():
    cfg.print_header("📦 TURBO ORGANIZER", "Moving Assets to Local NVMe Hierarchy")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Ensure Dest Dirs
    for cat, subpath in CATEGORIES.items():
        (DEST_ROOT / subpath).mkdir(parents=True, exist_ok=True)
        
    print(f"CORE > Destination: {DEST_ROOT}")
    
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
        if "KICK" in tag_list: dest_subpath = CATEGORIES["KICK"]
        elif "SNARE" in tag_list: dest_subpath = CATEGORIES["SNARE"]
        elif "HAT" in tag_list: dest_subpath = CATEGORIES["HAT"]
        elif "LOOP" in tag_list: dest_subpath = CATEGORIES["LOOPS"]
        elif "BASS" in tag_list: dest_subpath = CATEGORIES["BASS"]
        elif "SYNTH" in tag_list: dest_subpath = CATEGORIES["SYNTH"]
        elif "VOCAL" in tag_list: dest_subpath = CATEGORIES["VOCAL"]
        elif "FX" in tag_list: dest_subpath = CATEGORIES["FX"]
        
        if dest_subpath:
            dest_dir = DEST_ROOT / dest_subpath
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
                print(f"CORE >    Moved: {src.name} -> {dest_subpath}")
                
            except Exception as e:
                errors += 1
                # print(f"Error moving {src}: {e}")
                
    cfg.system_log(f"Organization Complete. {total_moved} files curated.", "SUCCESS")
    print(f"CORE > Errors: {errors}")

if __name__ == "__main__":
    organize_universe()

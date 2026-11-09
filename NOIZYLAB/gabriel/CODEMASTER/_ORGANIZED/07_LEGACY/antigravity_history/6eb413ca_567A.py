#!/usr/bin/env python3
import os
import json
import sys
import time
from pathlib import Path
from datetime import datetime
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

# Configuration
SYSTEM_PLUGIN_PATH = "/Library/Audio/Plug-Ins"
DB_PATH = cfg.SCRIPTS_DIR.parent / "Database" / "vi_db.json"

PLUGIN_DIRS = [
    Path("/Library/Audio/Plug-Ins/VST"),
    Path("/Library/Audio/Plug-Ins/VST3"),
    Path("/Library/Audio/Plug-Ins/Components"),
    Path.expanduser(Path("~/Library/Audio/Plug-Ins/VST")),
    Path.expanduser(Path("~/Library/Audio/Plug-Ins/VST3")),
    Path.expanduser(Path("~/Library/Audio/Plug-Ins/Components"))
]

# Formats to scan
FORMATS = {
    'Components': 'Audio Unit',
    'VST': 'VST',
    'VST3': 'VST3'
}

def load_db():
    try:
        if DB_PATH.exists():
            with open(DB_PATH, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"instruments": []}

def save_db(data):
    cfg.ensure_dirs([DB_PATH.parent])
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def clean_name(filename, suffix):
    """Clean 'UAD 4K Buss Compressor.component' -> 'UAD 4K Buss Compressor'"""
    return filename.replace(suffix, '')

def scan_plugins():
    cfg.print_header("🕵️‍♂️ TURBO PLUGINS", "Scanning System Audio Units/VSTs")
    
    db = load_db()
    existing_items = {i['name'].lower() for i in db.get('instruments', [])}
    new_count = 0
    
    for fmt_folder, type_name in FORMATS.items():
        scan_dir = Path(SYSTEM_PLUGIN_PATH) / fmt_folder
        if not scan_dir.exists():
            continue
            
        cfg.system_log(f"Scanning {fmt_folder} ...", "INFO")
        
        for item in scan_dir.iterdir():
            if item.name.startswith('.'): continue
            
            # Basic cleanup
            suffix = item.suffix
            name = clean_name(item.name, suffix)
            
            # Simple Developer guessing (heuristic)
            parts = name.split(' ')
            developer = "Unknown"
            if len(parts) > 1:
                # Common prefixes
                if parts[0] in ['UAD', 'FabFilter', 'iZotope', 'Waves', 'NI', 'Arturia']:
                    developer = parts[0]
                elif parts[0] == 'Valhalla':
                    developer = "Valhalla DSP"
            
            if name.lower() not in existing_items:
                new_entry = {
                    "id": f"auto_{len(existing_items) + new_count + 1:04d}",
                    "name": name,
                    "developer": developer,
                    "type": "Effect" if "Compressor" in name or "EQ" in name or "Verb" in name else "Instrument",
                    "format": type_name,
                    "added_at": str(datetime.now())
                }
                db['instruments'].append(new_entry)
                new_count += 1
                # print(f"      + Found: {name}")

    if new_count > 0:
        save_db(db)
        cfg.system_log(f"✅ Added {new_count} new plugins to the Knowledge Base.", "SUCCESS")
    else:
        cfg.system_log(f"✨ Database is already up to date.", "SUCCESS")

if __name__ == "__main__":
    scan_plugins()

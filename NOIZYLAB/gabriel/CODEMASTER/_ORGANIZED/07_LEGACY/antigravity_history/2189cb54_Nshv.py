import os
import json
from pathlib import Path
from datetime import datetime

# Configuration
SYSTEM_PLUGIN_PATH = "/Library/Audio/Plug-Ins"
DB_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/vi_db.json"

# Formats to scan
FORMATS = {
    'Components': 'Audio Unit',
    'VST': 'VST',
    'VST3': 'VST3'
}

def load_db():
    try:
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    except:
        return {"instruments": []}

def save_db(data):
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def clean_name(filename, suffix):
    """Clean 'UAD 4K Buss Compressor.component' -> 'UAD 4K Buss Compressor'"""
    return filename.replace(suffix, '')

def scan_plugins():
    print("CORE > 🕵️‍♂️ SCANNING SYSTEM FOR AUDIO PLUGINS...")
    
    db = load_db()
    existing_items = {i['name'].lower() for i in db.get('instruments', [])}
    new_count = 0
    
    for fmt_folder, type_name in FORMATS.items():
        scan_dir = Path(SYSTEM_PLUGIN_PATH) / fmt_folder
        if not scan_dir.exists():
            continue
            
        print(f"CORE > 📂 Scanning {fmt_folder} ...")
        
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
        print(f"\nCORE > ✅ Added {new_count} new plugins to the Knowledge Base.")
    else:
        print("\nCORE > ✨ Database is already up to date.")

if __name__ == "__main__":
    scan_plugins()

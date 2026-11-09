
import json
import os
from datetime import datetime
import sys
from pathlib import Path
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
DB_FILE = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/vi_db.json")

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def load_db():
    # Only Log on write/seed, not read to avoid spam? 
    # Or logging "VI DB Accessed" is fine.
    pass

def seed_db():
    brain = MemCell()
    brain.log_event(brain.covenant_id, "DB_SEED", "VI DB Tool: Seeding Knowledge Base", vibe=70, author="VI_DB_TOOL")
    
    print(f"{BOLD}{CYAN}CORE > 🌱 SEEDING VIRTUAL INSTRUMENT DATABASE...{RESET}")
    
    if not DB_FILE.exists():
        print("Database not found. Creating new...")
        data = {"metadata": {"last_updated": str(datetime.now().date())}, "instruments": []}
        save_db(data) # Save initial structure
        return data
    
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON. Starting fresh.")
            return {"metadata": {"last_updated": str(datetime.now().date())}, "instruments": []}

def save_db(data):
    data['metadata']['last_updated'] = str(datetime.now().date())
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to {DB_PATH}")

def add_entry():
    db = load_db()
    
    print("\nCORE > --- ADD NEW VIRTUAL INSTRUMENT ---")
    
    # Auto ID
    count = len(db['instruments'])
    new_id = f"vi_{count + 1:03d}"
    print(f"CORE > ID: {new_id}")
    
    name = input("CORE > Instrument Name: ").strip()
    if not name: return
    
    developer = input("CORE > Developer: ").strip()
    type_ = input("CORE > Type (Synth/Sampler/Effect): ").strip()
    release_date = input("CORE > Release Date (YYYY-MM-DD) [Optional]: ").strip()
    
    entry = {
        "id": new_id,
        "name": name,
        "developer": developer,
        "type": type_,
        "release_date": release_date if release_date else "Unknown",
        "added_at": str(datetime.now())
    }
    
    db['instruments'].append(entry)
    save_db(db)
    print("CORE > ----------------------------------")

def list_entries():
    db = load_db()
    print("\nCORE > --- CURRENT DATABASE ---")
    for inst in db['instruments']:
        print(f"CORE > [{inst['id']}] {inst['name']} by {inst['developer']} ({inst['type']})")

if __name__ == "__main__":
    while True:
        print("\nCORE > AUDIO UNITOR DATABASE TOOL")
        print("1. Add Entry")
        print("2. List Entries")
        print("3. Exit")
        choice = input("CORE > Select: ")
        
        if choice == '1':
            add_entry()
        elif choice == '2':
            list_entries()
        elif choice == '3':
            break

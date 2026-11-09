import json
import os
from datetime import datetime

DB_PATH = "/Users/m2ultra/Audio_Unitor/Database/vi_db.json"

def load_db():
    if not os.path.exists(DB_PATH):
        print("Database not found. Creating new...")
        return {"metadata": {"last_updated": str(datetime.now().date())}, "instruments": []}
    
    with open(DB_PATH, 'r') as f:
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
    
    print("\n--- ADD NEW VIRTUAL INSTRUMENT ---")
    
    # Auto ID
    count = len(db['instruments'])
    new_id = f"vi_{count + 1:03d}"
    print(f"ID: {new_id}")
    
    name = input("Instrument Name: ").strip()
    if not name: return
    
    developer = input("Developer: ").strip()
    type_ = input("Type (Synth/Sampler/Effect): ").strip()
    release_date = input("Release Date (YYYY-MM-DD) [Optional]: ").strip()
    
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
    print("----------------------------------")

def list_entries():
    db = load_db()
    print("\n--- CURRENT DATABASE ---")
    for inst in db['instruments']:
        print(f"[{inst['id']}] {inst['name']} by {inst['developer']} ({inst['type']})")

if __name__ == "__main__":
    while True:
        print("\nAUDIO UNITOR DATABASE TOOL")
        print("1. Add Entry")
        print("2. List Entries")
        print("3. Exit")
        choice = input("Select: ")
        
        if choice == '1':
            add_entry()
        elif choice == '2':
            list_entries()
        elif choice == '3':
            break

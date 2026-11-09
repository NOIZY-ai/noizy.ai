import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Configuration
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

# Seed Data (The "Gems")
SEEDS = [
    {"name": "Serum", "developer": "Xfer", "type": "Synth"},
    {"name": "Omnisphere", "developer": "Spectrasonics", "type": "Synth"},
    {"name": "Diva", "developer": "u-he", "type": "Synth"},
    {"name": "Keyscape", "developer": "Spectrasonics", "type": "Keys"},
    {"name": "Trilian", "developer": "Spectrasonics", "type": "Bass"},
    {"name": "Kontakt 7", "developer": "Native Inst", "type": "Sampler"},
    {"name": "FabFilter Pro-Q 3", "developer": "FabFilter", "type": "EQ"},
    {"name": "FabFilter Pro-L 2", "developer": "FabFilter", "type": "Limiter"},
    {"name": "ValhallaVintageVerb", "developer": "Valhalla", "type": "Reverb"},
    {"name": "Decapitator", "developer": "Soundtoys", "type": "Saturation"},
    {"name": "EchoBoy", "developer": "Soundtoys", "type": "Delay"},
    {"name": "Soothe2", "developer": "Oeksound", "type": "Utility"},
    {"name": "RC-20 Retro Color", "developer": "XLN Audio", "type": "FX"},
    {"name": "Portal", "developer": "Output", "type": "FX"},
    {"name": "Thermal", "developer": "Output", "type": "Distortion"},
    {"name": "ShaperBox 3", "developer": "Cableguys", "type": "FX"},
    {"name": "Vital", "developer": "Matt Tytel", "type": "Synth"},
    {"name": "Pigments 5", "developer": "Arturia", "type": "Synth"},
    {"name": "Jupiter-8", "developer": "Roland", "type": "Synth"},
    {"name": "Juno-60", "developer": "Roland", "type": "Synth"},
    {"name": "Ozone 11", "developer": "iZotope", "type": "Mastering"},
]

def seed_database():
    print(f"🌱 Seeding Universe DB at {DB_PATH}...")
    
    if not DB_PATH.parent.exists():
        DB_PATH.parent.mkdir(parents=True)
        
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # 1. Create Plugins Table if needed
    c.execute("""CREATE TABLE IF NOT EXISTS plugins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        developer TEXT,
        type TEXT,
        status TEXT DEFAULT 'ACTIVE',
        last_seen TEXT
    )""")
    
    # 2. Insert Seeds
    count = 0
    for seed in SEEDS:
        try:
            ts = datetime.now().isoformat()
            c.execute("INSERT OR IGNORE INTO plugins (name, developer, type, last_seen) VALUES (?, ?, ?, ?)",
                      (seed['name'], seed['developer'], seed['type'], ts))
            if c.rowcount > 0: count += 1
        except Exception as e:
            print(f"Error seeding {seed['name']}: {e}")
            
    conn.commit()
    conn.close()
    
    print(f"✅ Seeding Complete. Added {count} new gems.")
    if count == 0:
        print("   (Database was already populated)")

if __name__ == "__main__":
    seed_database()

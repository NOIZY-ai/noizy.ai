import json
import os
import datetime
from pathlib import Path

# CONFIG
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")
NOW = datetime.datetime.now(datetime.timezone.utc).astimezone()

def create_db(age_hours):
    ts = NOW - datetime.timedelta(hours=age_hours)
    data = [
        {
            "id": f"TEST_ITEM_{age_hours}H",
            "timestamp": ts.isoformat(),
            "author": "TESTER",
            "topic": "FastRoleCheck",
            "content": "Checking the velocity of the delta sweep.",
            "tags": ["TEST", "VELOCITY"]
        }
    ]
    with open(DB_PATH, 'w') as f:
        json.dump(data, f)

def run_sweeper(label):
    print(f"\n>>> RUNNING SWEEPER: {label}")
    print("-" * 40)
    os.system("python3 memcell_sweeper.py")
    print("-" * 40)

def main():
    print("🏎️  MC96 FAST x1000: VERIFICATION PROTOCOL\n")
    
    # SCENARIO 1: NO DELTAS (Ancient History > 4h)
    # create_db(5) # 5 hours old
    # Actually sweeper window is 4 hours.
    create_db(5)
    run_sweeper("SCENARIO A: STEADY STATE (No Deltas)")
    
    # SCENARIO 2: DELTAS (Fresh < 4h)
    create_db(1)
    run_sweeper("SCENARIO B: DELTA INGEST (Fresh Meat)")

    # Cleanup
    if DB_PATH.exists(): DB_PATH.unlink()

if __name__ == "__main__":
    main()

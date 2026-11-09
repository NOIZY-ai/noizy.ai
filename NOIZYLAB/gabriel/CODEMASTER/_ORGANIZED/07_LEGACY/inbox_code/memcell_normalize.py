# 🤖 SYSTEM FILE: memcell_normalize.py
# Optimized by Healer Drone

import json
import time

DB_PATH = "memcell_db.json"

try:
    with open(DB_PATH, 'r') as f:
        db = json.load(f)

    updated_count = 0
    for memory in db:
        changed = False
        if "author" not in memory:
            memory["author"] = "SYSTEM"
            changed = True
        if "subject" not in memory:
            memory["subject"] = "Legacy Data"
            changed = True
        if "overlap" not in memory:
            memory["overlap"] = []
            changed = True
        if "god_mode_timestamp" not in memory:
            memory["god_mode_timestamp"] = int(time.time() * 1e9)
            changed = True

        if changed:
            updated_count += 1

    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)

    print(f"✅ MEMCELL NORMALIZED: Updated {updated_count} records to God Mode Schema.")

except Exception as e:
    print(f"❌ ERROR: {e}")

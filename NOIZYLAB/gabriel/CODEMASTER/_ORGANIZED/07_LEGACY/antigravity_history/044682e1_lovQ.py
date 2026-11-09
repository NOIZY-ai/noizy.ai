import sys
from pathlib import Path
import datetime
import uuid
import json

sys.path.append("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL")
from MEMCELL_CORE import MemCellCore

brain = MemCellCore()

# Current time (Aware)
now = datetime.datetime.now().astimezone()

entries = [
    {
        "content": "URGENT: Review system logs for drift anomaly.",
        "author": "GABRIEL",
        "timestamp": now.isoformat(),
        "tags": ["SYSTEM", "RISK", "ACTION"]
    }
]

for e in entries:
    m = {
        "id": str(uuid.uuid4()),
        "timestamp": e['timestamp'],
        "god_mode_timestamp": 0,
        "type": "THOUGHT", # Using THOUGHT but content implies action
        "author": e['author'],
        "subject": "System Warning",
        "topic": "Maintenance",
        "group": "LifeLuv",
        "content": e['content'],
        "tags": e['tags'],
        "overlap": []
    }
    brain.db.append(m)

brain.save_db()
print(f"Injected {len(entries)} ACTION logs.")

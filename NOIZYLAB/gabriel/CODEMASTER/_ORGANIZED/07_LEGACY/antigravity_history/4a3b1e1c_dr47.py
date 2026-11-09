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
    # 1. Structural Drift Candidate (Missing essential fields if we could, but MemCellCore enforces some. 
    # We will simulate "Behavior Drift" with lowercase tags)
    {
        "content": "unknown signal detected",
        "author": "UNKNOWN",
        "timestamp": now.isoformat(),
        "tags": ["weak_signal", "noise"] # Behavior drift (lowercase)
    },
    # 2. Semantic Weakness (Short, ambiguous)
    {
        "content": "yes",
        "author": "USER",
        "timestamp": now.isoformat(),
        "tags": ["VOICE_LOG"]
    }
]

for e in entries:
    m = {
        "id": str(uuid.uuid4()),
        "timestamp": e['timestamp'],
        "god_mode_timestamp": 0,
        "type": "THOUGHT",
        "author": e['author'],
        "subject": "Unknown",
        "topic": "DriftTest",
        "group": "LifeLuv",
        "content": e['content'],
        "tags": e['tags'],
        "overlap": []
    }
    brain.db.append(m)

brain.save_db()
print(f"Injected {len(entries)} DRIFT logs.")

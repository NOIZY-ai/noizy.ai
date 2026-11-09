import sys
from pathlib import Path
import datetime
import uuid
import json

# Adjust path to find modules
sys.path.append("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL")
from MEMCELL_CORE import MemCellCore

brain = MemCellCore()

# Current time approx 10:48 AM
now = datetime.datetime.now()

entries = [
    {
        "content": "Gabriel System Online. Awaiting command.",
        "author": "GABRIEL",
        "timestamp": (now - datetime.timedelta(minutes=8)).isoformat(),
        "tags": ["VOICE_LOG", "GOD_MODE"]
    },
    {
        "content": "Hello Gabriel, are you ready?",
        "author": "USER",
        "timestamp": (now - datetime.timedelta(minutes=7, seconds=50)).isoformat(),
        "tags": ["VOICE_LOG", "GOD_MODE"]
    },
    {
        "content": "Voice systems fully operational. I am ready to serve.",
        "author": "GABRIEL",
        "timestamp": (now - datetime.timedelta(minutes=7, seconds=48)).isoformat(),
        "tags": ["VOICE_LOG", "GOD_MODE"]
    },
    {
        "content": "Run Fishnet scan",
        "author": "USER",
        "timestamp": (now - datetime.timedelta(minutes=5)).isoformat(),
        "tags": ["VOICE_LOG", "GOD_MODE"]
    },
    {
        "content": "Deploying Fishnet surveillance.",
        "author": "GABRIEL",
        "timestamp": (now - datetime.timedelta(minutes=4, seconds=58)).isoformat(),
        "tags": ["VOICE_LOG", "GOD_MODE"]
    },
    {
        "content": "Scan complete. I have detected 0 anomalies in the sector.",
        "author": "GABRIEL",
        "timestamp": (now - datetime.timedelta(minutes=4, seconds=55)).isoformat(),
        "tags": ["VOICE_LOG", "GOD_MODE"]
    },
    # Duplicate entry (Simulating glitch or repeated log)
    {
         "content": "Deploying Fishnet surveillance.",
         "author": "GABRIEL",
         "timestamp": (now - datetime.timedelta(minutes=4, seconds=57)).isoformat(), # Slightly diff time
         "tags": ["VOICE_LOG", "GOD_MODE"]
    }
]

for e in entries:
    m = {
        "id": str(uuid.uuid4()),
        "timestamp": e['timestamp'],
        "god_mode_timestamp": 0,
        "type": "THOUGHT",
        "author": e['author'],
        "subject": "User Interaction",
        "topic": "Conversation",
        "group": "LifeLuv",
        "content": e['content'],
        "tags": e['tags'],
        "overlap": []
    }
    brain.db.append(m)

brain.save_db()
print(f"Injected {len(entries)} simulated logs.")

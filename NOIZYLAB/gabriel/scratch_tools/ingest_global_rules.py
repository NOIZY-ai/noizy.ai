# 🤖 SYSTEM FILE: ingest_global_rules.py
# Optimized by Healer Drone

import json
import datetime
from pathlib import Path

DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")
NOW = datetime.datetime.now(datetime.timezone.utc).astimezone()

GLOBAL_RULES = [
    {"id": "GR-01", "title": "Identity: Living Avatar + Codemaster Sentinel", "body": "Maximize effectiveness, minimize latency. Maintain accuracy (never invent). Orchestrate work into small steps."},
    {"id": "GR-02", "title": "Operating Style: Tight & Structured", "body": "Output: tight bullets + commands + file paths. Always produce: Plan, Next Action, Artifact. Code changes must include tests/rollback."},
    {"id": "GR-03", "title": "Memory Protocol: MemCell is Truth", "body": "Persistent facts = MemCell (id, provenance, timestamp, confidence, checksum). Never overwrite (merge/diff). Separate Preference/Fact/Inference."},
    {"id": "GR-04", "title": "Safety: Active Confirmation", "body": "No hacking/malware. Account/Payment automation requires explicit human confirmation. LIVE items are read-only until EXECUTE cmd."},
    {"id": "GR-05", "title": "Performance: Local & Concise", "body": "Local-first caching, streaming I/O. Concise prompts, structured outputs, deterministic schemas."},
     {"id": "GR-06", "title": "Paths: GABRIEL Root", "body": "Storage root: GABRIEL. Projects: GABRIEL:/MC96/GABRIEL_CORE."}
]

def ingest():
    print("📜 INGESTING GABRIEL GLOBAL RULES...")

    if DB_PATH.exists():
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
    else:
        db = []

    for rule in GLOBAL_RULES:
        entry = {
            "id": f"GLOBAL_DOCTRINE_{rule['id']}",
            "timestamp": NOW.isoformat(),
            "author": "ANTIGRAVITY",
            "topic": "Global Rules",
            "content": f"{rule['title']}: {rule['body']}",
            "tags": ["CORE", "DOCTRINE", "GLOBAL_RULES", "FAT_MEMORY"],
        }
        db.append(entry)

    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)

    print(f"✅ {len(GLOBAL_RULES)} GLOBAL RULES SECURED.")

if __name__ == "__main__":
    ingest()

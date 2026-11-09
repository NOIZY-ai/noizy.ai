# 🤖 SYSTEM FILE: ingest_doctrine.py
# Optimized by Healer Drone

import json
import datetime
from pathlib import Path

DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")
NOW = datetime.datetime.now(datetime.timezone.utc).astimezone()

DOCTRINE = [
    {"id": "GOLD-01", "conf": 90, "title": "Work Packs are the execution unit", "body": "Single unit of work = WP-ID + goal + P0–P3 tasks + deps + done-definition + risk band."},
    {"id": "GOLD-02", "conf": 88, "title": "Drift is tripwired and escalated", "body": "Detect semantic/structural/behavior drift -> auto-correct/log -> P1 stabilize -> P0 if repeated."},
    {"id": "GOLD-03", "conf": 86, "title": "Artifact state machine prevents chaos", "body": "Every artifact lives in Active / Quarantine / Archive / Trash Candidate; deletion is deferred until proven safe."},
    {"id": "GOLD-04", "conf": 84, "title": "Tiering is the universal output contract", "body": "Tier A exec summary; Tier B operator actions + overlap; Tier C archival/provenance."},
    {"id": "GOLD-05", "conf": 82, "title": "TruthScan produces a safe fix queue", "body": "Duplicates + canonical plan + Safe-Auto/Safe-Confirm/Manual actions; 'do-no-harm' checklist always emitted."},
    {"id": "GOLD-06", "conf": 90, "title": "Prompt Stack enforces the machine", "body": "FAST (delta), STRONG (canon), BUILDER (packs), AUDITOR (proof/closure). No free-form wandering."},
    {"id": "GOLD-07", "conf": 78, "title": "Visibility matters: dashboard is the control plane", "body": "Heatmaps + drift radar + action queue + scan status + session outcomes."},
]

def ingest():
    print("📜 INGESTING GORUNFREEX1000 PRIME DOCTRINE...")

    if DB_PATH.exists():
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
    else:
        db = []

    for rule in DOCTRINE:
        entry = {
            "id": f"DOCTRINE_{rule['id']}",
            "timestamp": NOW.isoformat(),
            "author": "MC96_PRIME",
            "topic": "GORUNFREEX1000 Ruleset",
            "content": f"{rule['title']}: {rule['body']}",
            "tags": ["DOCTRINE", "GOLD", "RULESET", "CORE"],
            # Embedding confidence hint in content or handling via Sweeper logic?
            # Sweeper calculates confidence. Ideally we'd pass this meta, but for now we rely on the text content.
            # We'll prepend [GOLD] to title to help.
        }
        db.append(entry)

    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)

    print(f"✅ {len(DOCTRINE)} DOCTRINE ENTRIES SECURED.")

if __name__ == "__main__":
    ingest()

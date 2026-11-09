import json
import os
from pathlib import Path

# CONFIG
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")
ACTION_QUEUE_PATH = DB_PATH.parent / "ACTION_QUEUE.md"

def create_drift_db():
    print("[TEST] Creating DB with HIGH DRIFT item...")
    data = [
        {
            "id": "DRIFT_TEST_001",
            "timestamp": "2025-12-16T10:00:00-05:00",
            "author": "UNKNOWN",
            "topic": "DriftTest",
            "content": "", # Missing content triggers STRUCTURAL drift (Score +50) -> HIGH
            "tags": ["bad_tag"] # Lowercase tag triggers BEHAVIOR drift (+10)
        }
    ]
    with open(DB_PATH, 'w') as f:
        json.dump(data, f)

def verify_output():
    if not ACTION_QUEUE_PATH.exists():
        print("[FAIL] Action Queue not generated.")
        return
        
    content = ACTION_QUEUE_PATH.read_text()
    if "STABILIZATION_CORE" in content:
        print("[SUCCESS] Found 'STABILIZATION_CORE' Work Pack.")
        print(content)
    else:
        print("[FAIL] 'STABILIZATION_CORE' not found.")
        print(content)

if __name__ == "__main__":
    create_drift_db()
    # Run the sweeper (assuming it's in the same dir or path)
    os.system("python3 memcell_sweeper.py")
    verify_output()

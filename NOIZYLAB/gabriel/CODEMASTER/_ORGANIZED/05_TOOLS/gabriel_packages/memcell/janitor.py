# 🤖 SYSTEM FILE: janitor.py
# Optimized by Healer Drone

import hashlib
import json
from pathlib import Path
from typing import List, Dict

class JanitorAgent:
    """
    GABRIEL JANITOR AGENT (2026)
    "Zero-Entropy": Runs 24/7 to prune, deduplicate, and validate MemCells.
    """
    def __init__(self, data_root: str):
        self.root = Path(data_root)
        self.quarantine_dir = self.root / "quarantine"
        self.quarantine_dir.mkdir(exist_ok=True)

    def scan_and_clean(self):
        """ The Main Loop: Scans all JSONs, hashes them, finds dupes. """
        report = {"scanned": 0, "deduped": 0, "quarantined": 0}

        # 1. Map Hashes to Files
        content_map = {}

        files = list(self.root.glob("*.json"))
        for f in files:
            if f.name.startswith("mc_"): # Only check MemCells
                report["scanned"] += 1
                try:
                    data = json.loads(f.read_text())
                    # Detect Duplicate Content (Exact Claim Match)
                    claim = data.get("claim", "").strip().lower()

                    if claim in content_map:
                        # DUPLICATE DETECTED
                        self.quarantine(f, "duplicate_claim", content_map[claim])
                        report["deduped"] += 1
                    else:
                        content_map[claim] = f

                    # Check Integrity
                    if not self.validate_schema(data):
                         self.quarantine(f, "invalid_schema")
                         report["quarantined"] += 1

                except Exception as e:
                    print(f"Janitor Error on {f}: {e}")

        return report

    def validate_schema(self, data: Dict) -> bool:
        # Basic v4 Check: Must have provenance + confidence
        if "provenance" not in data: return False
        # if "confidence" not in data: return False # Strict mode
        return True

    def quarantine(self, file_path: Path, reason: str, original: Path = None):
        """ Moves bad/dupe file to quarantine """
        new_name = f"{file_path.stem}_{reason}_{hashlib.sha256(str(file_path).encode()).hexdigest()[:4]}.json"
        dest = self.quarantine_dir / new_name
        file_path.rename(dest)
        # Log logic here

if __name__ == "__main__":
    janitor = JanitorAgent("./data/memcell_db")
    print(janitor.scan_and_clean())

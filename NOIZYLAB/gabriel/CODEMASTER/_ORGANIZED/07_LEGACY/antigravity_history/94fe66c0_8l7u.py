#!/usr/bin/env python3
"""
MemCell_GIC.py
The Atomic Truth Engine.
Part of the MIACLE Spine.
"""
import json
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict, Optional

MEMCELL_PATH = Path.home() / ".noizylab" / "memory" / "memcell_gic.json"

class MemCellGIC:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict:
        if not MEMCELL_PATH.exists():
            MEMCELL_PATH.parent.mkdir(parents=True, exist_ok=True)
            return {"cells": {}}
        try:
            with open(MEMCELL_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"cells": {}}

    def _save_memory(self):
        with open(MEMCELL_PATH, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def _generate_hash(self, claim: str) -> str:
        """Delta Only: Content Hash."""
        return hashlib.sha256(claim.encode()).hexdigest()

    def upsert(self, claim: str, evidence: List[str], author: str = "System", scope: str = "GLOBAL") -> Dict:
        """
        Atomic Upsert.
        If hash exists, check for conflict.
        If new, insert.
        """
        cell_hash = self._generate_hash(claim)
        timestamp = datetime.datetime.now().isoformat()

        # Check for existing
        if cell_hash in self.memory["cells"]:
            # In a real GIC, we would check if status changed or evidence grew.
            # For now, we update 'last_verified'
            cell = self.memory["cells"][cell_hash]
            cell["last_verified"] = timestamp
            # Merge evidence unique
            cell["evidence"] = list(set(cell["evidence"] + evidence))
            self._save_memory()
            return {"status": "UPDATED", "id": cell["id"]}

        # Create New Atomic Cell
        new_id = f"MC-{len(self.memory['cells']) + 1:04d}"
        
        cell = {
            "id": new_id,
            "claim": claim,
            "hash": cell_hash,
            "status": "VERIFIED" if evidence else "UNVERIFIED", # Evidence Locked
            "evidence": evidence,
            "conflicts": [],
            "author": author,
            "scope": scope,
            "created_at": timestamp,
            "last_verified": timestamp
        }

        if not evidence:
            print(f"⚠️  [GIC] Alert: Claim '{claim[:20]}...' has NO EVIDENCE. Marked UNVERIFIED.")

        self.memory["cells"][cell_hash] = cell
        self._save_memory()
        return {"status": "CREATED", "id": new_id}

    def retrieve(self, query_hash: str) -> Optional[Dict]:
        return self.memory["cells"].get(query_hash)

    def dump_truth(self):
        """Dump all VERIFIED facts."""
        return [c for c in self.memory["cells"].values() if c["status"] == "VERIFIED"]

if __name__ == "__main__":
    gic = MemCellGIC()
    # Test Upsert
    result = gic.upsert(
        claim="Unverified information must not enter summaries.",
        evidence=["SPEC-GIC-001"],
        author="Rob"
    )
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
"""
MemCell_Plus.py (MemCell++)
The "Thinking" Memory for GABRIEL OS.
Merges:
- Atomic Patterns (MemCell_GIC)
- Overlap Engine (MemCell_V3)
- Counterfactuals & Negative Knowledge (MIACLE GOLD)
"""
import os
import json
import hashlib
import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / "NOIZYLAB" / "memory"
MEMORY_FILE = MEMORY_DIR / "memcell_plus.json"

class MemCellPlus:
    def __init__(self):
        self._ensure_memory()
        self.memory = self._load_memory()

    def _ensure_memory(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        if not MEMORY_FILE.exists():
            init_data = {
                "version": "PLUS_1.0",
                "cells": {},       # Atomic Facts (Hash -> Cell)
                "patterns": [],    # Overlap Groups
                "counterfactuals": [], # What we rejected
                "negative_knowledge": [], # What failed
                "temporal_index": [] # Time-ordered keys
            }
            self._save_memory(init_data)

    def _load_memory(self):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_memory(self, data):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def _hash(self, content):
        return hashlib.sha256(content.encode()).hexdigest()

    def add_fact(self, claim, source_id, locator, author="GABRIEL"):
        """Atomic Truth Ingestion (Delta-Only)"""
        h = self._hash(claim)
        
        # Delta Check
        if h in self.memory["cells"]:
            # Update weight/timestamp but don't duplicate
            self.memory["cells"][h]["weight"] += 0.1
            self.memory["cells"][h]["last_seen"] = datetime.datetime.now().isoformat()
            self._save_memory(self.memory)
            return False # No new write
            
        cell = {
            "id": h,
            "claim": claim,
            "evidence": {"source": source_id, "loc": locator},
            "author": author,
            "captured_at": datetime.datetime.now().isoformat(),
            "last_seen": datetime.datetime.now().isoformat(),
            "weight": 1.0,
            "type": "fact"
        }
        
        self.memory["cells"][h] = cell
        self.memory["temporal_index"].append(h)
        self._save_memory(self.memory)
        return True

    def add_counterfactual(self, proposal, reason):
        """Store what we rejected (Thinking)"""
        entry = {
            "proposal": proposal,
            "rejected_reason": reason,
            "time": datetime.datetime.now().isoformat()
        }
        self.memory["counterfactuals"].append(entry)
        self._save_memory(self.memory)

    def add_negative(self, action, error):
        """Store failure to prevent regression"""
        entry = {
            "action": action,
            "error": error,
            "time": datetime.datetime.now().isoformat()
        }
        self.memory["negative_knowledge"].append(entry)
        self._save_memory(self.memory)

    def recall(self, query=None):
        """Recall with Temporal Weighting"""
        # Simple dump for now, real Logic would rank by weight + recency
        latest = self.memory["temporal_index"][-5:]
        facts = [self.memory["cells"][k]["claim"] for k in latest]
        
        return f"""[MEMCELL++]
FACTS: {len(self.memory['cells'])}
PATTERNS: {len(self.memory['patterns'])}
REJECTED: {len(self.memory['counterfactuals'])}
FAILURES: {len(self.memory['negative_knowledge'])}
RECENT:
- {chr(10).join(facts)}
"""

if __name__ == "__main__":
    mc = MemCellPlus()
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "fact":
             mc.add_fact(sys.argv[2], "cli", "args")
             print("✅ Fact Stored.")
        elif sys.argv[1] == "recall":
             print(mc.recall())
    else:
        print(mc.recall())

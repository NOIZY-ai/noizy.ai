#!/usr/bin/env python3
"""
MemCell.py V3 - The Neural Core (Overlap Engine)
Tracks Subject Matter, Vibe, and detects "Neural Overlap" via Pattern Recognition.
"""
import os
import json
import datetime
import sys
from pathlib import Path
from collections import Counter

# Configuration
MEMORY_DIR = Path.home() / "NOIZYLAB" / "memory"
MEMORY_FILE = MEMORY_DIR / "memcell_v3.json"

class MemCell:
    def __init__(self):
        self._ensure_memory()
        self.memory = self._load_memory()
        self.dirty = False

    def _ensure_memory(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        if not MEMORY_FILE.exists():
            initial_mem = {
                "system_start": datetime.datetime.now().isoformat(),
                "neural_state": {
                    "vibe": "neutral",
                    "focus": "idle",
                    "short_term": [],
                    "patterns": []
                },
                "personas": {
                    "active": ["shirl", "engr"],
                    "overlap_detected": False
                }
            }
            self._save_memory(initial_mem)

    def _load_memory(self):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_memory(self, data):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        self.dirty = False

    def detect_overlaps(self, history):
        """Analyzes history for recurring subjects (The Overlap)."""
        subjects = [h.get('s', '').lower() for h in history if h.get('s')]
        if not subjects: return []
        
        # Count occurrences
        counts = Counter(subjects)
        # Filter for repeats (>2 times)
        overlaps = [subj for subj, count in counts.items() if count >= 2]
        return overlaps

    def track(self, action, subject, details=None):
        """Log action and Deep Scan for Overlap."""
        timestamp = datetime.datetime.now().isoformat()
        entry = {"t": timestamp, "a": action, "s": subject, "d": details or {}}
        
        ns = self.memory["neural_state"]
        ns["short_term"].append(entry)
        ns["focus"] = subject
        
        # Heuristic Vibe
        if "error" in action.lower(): ns["vibe"] = "critical"
        elif "optimize" in action.lower(): ns["vibe"] = "aligned"
        
        # trim
        if len(ns["short_term"]) > 100:
            ns["short_term"] = ns["short_term"][-100:]

        # OVERLAP ENGINE
        overlaps = self.detect_overlaps(ns["short_term"])
        ns["patterns"] = overlaps
        
        # If subject is in known patterns, we have ACTIVE OVERLAP
        if subject.lower() in overlaps:
            self.memory["personas"]["overlap_detected"] = True
            ns["vibe"] = "connected" # Upgrade vibe
        
        self.dirty = True
        self._save_memory(self.memory)
        return True

    def recall(self):
        ns = self.memory.get("neural_state", {})
        ov = self.memory.get("personas", {}).get("overlap_detected", False)
        patterns = ns.get("patterns", [])
        
        return f"""[MEMCELL V3 OVERLAP]
TIME: {datetime.datetime.now().strftime("%H:%M:%S")}
FOCUS: {ns.get('focus', 'idle')}
VIBE: {ns.get('vibe', 'neutral')}
OVERLAP: {'ACTIVE' if ov else 'Inactive'}
PATTERNS: {', '.join(patterns[:5])}
"""

if __name__ == "__main__":
    mc = MemCell()
    if len(sys.argv) > 1:
        if sys.argv[1] == "track":
            mc.track(sys.argv[2], sys.argv[3])
            print("🧠 Pattern Ingested.")
        elif sys.argv[1] == "recall":
            print(mc.recall())
    else:
        print(json.dumps(mc.memory, indent=2))

#!/usr/bin/env python3
"""
MemCell.py - The Central Intelligence Unit of MC96ECOUNIVERSE
Tracks Subject Matter, Date, Time, and Contextual Overlap.
"""
import os
import json
import datetime
import sys
from pathlib import Path

# Configuration
MEMORY_DIR = Path.home() / ".noizylab" / "memory"
MEMORY_FILE = MEMORY_DIR / "memcell.json"

class MemCell:
    def __init__(self):
        self._ensure_memory()
        self.memory = self._load_memory()

    def _ensure_memory(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        if not MEMORY_FILE.exists():
            initial_mem = {
                "system_start": datetime.datetime.now().isoformat(),
                "current_context": {},
                "history": [],
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

    def track(self, action, subject, details=None):
        """Log an action and update current context."""
        timestamp = datetime.datetime.now().isoformat()
        
        entry = {
            "timestamp": timestamp,
            "action": action,
            "subject": subject,
            "details": details or {}
        }
        
        # Update History
        self.memory["history"].append(entry)
        # Keep history trimmed to last 1000 items
        if len(self.memory["history"]) > 1000:
            self.memory["history"] = self.memory["history"][-1000:]
            
        # Update Context
        self.memory["current_context"] = {
            "last_action": action,
            "active_subject": subject,
            "last_updated": timestamp
        }
        
        # Auto-detect overlap (simple heuristic)
        if "shirl" in str(subject).lower() or "engr" in str(subject).lower():
            self.memory["personas"]["overlap_detected"] = True
            
        self._save_memory(self.memory)
        return True

    def recall(self):
        """Return the current context for AI injection."""
        ctx = self.memory.get("current_context", {})
        personas = self.memory.get("personas", {})
        
        summary = f"""[System Context]
Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Active Subject: {ctx.get('active_subject', 'None')}
Last Action: {ctx.get('last_action', 'None')}
Overlap Mode: {'ACTIVE' if personas.get('overlap_detected') else 'Standby'}
"""
        return summary

    def get_status(self):
        return {
            "memory_size_bytes": MEMORY_FILE.stat().st_size if MEMORY_FILE.exists() else 0,
            "history_count": len(self.memory.get("history", [])),
            "context": self.memory.get("current_context")
        }

# CLI Interface
if __name__ == "__main__":
    mc = MemCell()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "track":
            # Usage: track <action> <subject>
            action = sys.argv[2] if len(sys.argv) > 2 else "unknown"
            subject = sys.argv[3] if len(sys.argv) > 3 else "general"
            mc.track(action, subject)
            print("✅ Memory Updated.")
            
        elif cmd == "recall":
            print(mc.recall())
            
        elif cmd == "status":
            print(json.dumps(mc.get_status(), indent=2))
            
    else:
        print(json.dumps(mc.get_status(), indent=2))

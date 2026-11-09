#!/usr/bin/env python3
"""
MemCell.py V2 - The Neural Core of MC96ECOUNIVERSE
Tracks Subject Matter, Vibe, Temporal Context, and "Neural" Overlap.
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
        self.dirty = False

    def _ensure_memory(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        if not MEMORY_FILE.exists():
            initial_mem = {
                "system_start": datetime.datetime.now().isoformat(),
                "neural_state": {
                    "vibe": "neutral",
                    "focus": "idle",
                    "short_term": [],  # Last 50 actions
                    "long_term": []    # Major milestones only
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
                data = json.load(f)
                # V2 Migration Check
                if "neural_state" not in data:
                    data["neural_state"] = {
                        "vibe": "neutral",
                        "focus": "idle",
                        "short_term": data.get("history", [])[-50:],
                        "long_term": []
                    }
                    if "history" in data: del data["history"]
                return data
        except Exception:
            return {}

    def _save_memory(self, data):
        """Pulse Save: Writes to disk."""
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        self.dirty = False

    def _update_vibe(self, action, subject):
        """Heuristic Vibe Analysis."""
        positive = ["success", "completed", "optimized", "fixed", "upgrade", "create"]
        critical = ["error", "fail", "crit", "stuck"]
        
        current = self.memory["neural_state"]["vibe"]
        
        # Simple shift
        if any(w in str(action).lower() for w in positive):
            return "aligned"
        elif any(w in str(action).lower() for w in critical):
            return "critical"
        return current

    def track(self, action, subject, details=None):
        """Log an action into Short Term Memory."""
        timestamp = datetime.datetime.now().isoformat()
        
        entry = {
            "t": timestamp,
            "a": action,
            "s": subject,
            "d": details or {}
        }
        
        # Update Neural State
        ns = self.memory["neural_state"]
        ns["short_term"].append(entry)
        ns["focus"] = subject
        ns["vibe"] = self._update_vibe(action, subject)
        
        # Trim Short Term
        if len(ns["short_term"]) > 50:
            # Move significant items to Long Term? For now, just trim.
            ns["short_term"] = ns["short_term"][-50:]
            
        # Persona Overlap
        if "shirl" in str(subject).lower() or "engr" in str(subject).lower():
            self.memory["personas"]["overlap_detected"] = True
            
        self.dirty = True
        self._pulse()
        return True

    def _pulse(self):
        """Save if dirty."""
        if self.dirty:
            self._save_memory(self.memory)

    def recall(self):
        """Return Context for AI."""
        ns = self.memory.get("neural_state", {})
        personas = self.memory.get("personas", {})
        
        summary = f"""[MEMCELL V2 NEURAL CONTEXT]
Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Focus: {ns.get('focus', 'drifting')}
Vibe: {ns.get('vibe', 'neutral')} ({'OVERLAP' if personas.get('overlap_detected') else 'Standard'})
Recent: {ns.get('short_term', [])[-1].get('a', 'None') if ns.get('short_term') else 'None'}
"""
        return summary

    def get_status(self):
        return self.memory

# CLI Interface
if __name__ == "__main__":
    mc = MemCell()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "track":
            # track <action> <subject>
            action = sys.argv[2] if len(sys.argv) > 2 else "unknown"
            subject = sys.argv[3] if len(sys.argv) > 3 else "general"
            mc.track(action, subject)
            print("🧠 MemCell Pulse: Recorded.")
        elif cmd == "recall":
            print(mc.recall())
        elif cmd == "status":
            print(json.dumps(mc.get_status(), indent=2))
    else:
        print(json.dumps(mc.get_status(), indent=2))

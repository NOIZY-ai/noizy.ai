import json
import os
import time
from datetime import datetime

# NOIZYLAB MEMCELL v1.0
# "The Hippocampus" Module: System Memory & Temporal Tracking
# Purpose: Track "Subject Matter", Time, and Persona States (Shirl/Engr).

MEMCELL_DB = "noizy_memcell.json"

class MemCell:
    def __init__(self):
        self.db_path = MEMCELL_DB
        self.memory = self._load_memory()
        
    def _load_memory(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except:
                return self._init_db()
        else:
            return self._init_db()
            
    def _init_db(self):
        return {
            "created_at": str(datetime.now()),
            "sessions": [],
            "subject_matter": [],
            "personas": {
                "SHIRL": {"status": "ACTIVE", "role": "Temporal & Logic Guardian"},
                "ENGR": {"status": "ACTIVE", "role": "Technical Optimization Prime"}
            }
        }
        
    def save_memory(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.memory, f, indent=4)
            
    def log_interaction(self, user_input, system_action, persona="SYSTEM"):
        entry = {
            "timestamp": str(datetime.now()),
            "epoch": time.time(),
            "persona": persona,
            "input": user_input,
            "action": system_action
        }
        self.memory["sessions"].append(entry)
        
        # v2.0 INTELLIGENCE: Simple Keyword Extraction
        # Filter out noise, keep the signal.
        STOP_WORDS = {"the", "and", "for", "with", "that", "this", "from", "scan", "system", "file", "found"}
        
        # Sanitize
        clean_input = "".join([c if c.isalnum() or c.isspace() else " " for c in user_input]).lower()
        words = clean_input.split()
        
        # Extract interesting terms (len > 3, not stop word)
        keywords = [w for w in words if len(w) > 3 and w not in STOP_WORDS]
        
        if keywords:
             topic_str = ", ".join(keywords[:5]) # Top 5 tags
             self.memory["subject_matter"].append({
                 "topic": topic_str,
                 "raw": user_input[:50],
                 "timestamp": str(datetime.now())
             })
             
        self.save_memory()
        
    def get_time_matrix(self):
        """Returns the single source of truth for time."""
        now = datetime.now()
        return {
            "iso": now.isoformat(),
            "human": now.strftime("%Y-%m-%d %H:%M:%S"),
            "epoch": time.time()
        }

    def get_persona_directive(self, name):
        """Returns the core directive for a persona."""
        name = name.upper()
        if name in self.memory["personas"]:
            return self.memory["personas"][name]
        return None

# Singleton Instance
memory_core = MemCell()

if __name__ == "__main__":
    # Test
    print(">>> MEMCELL ONLINE.")
    print(f"    Current Matrix: {memory_core.get_time_matrix()['human']}")
    memory_core.log_interaction("Test Run", "System Boot", "ENGR")
    print("    Interaction Logged.")


# ============================================================================
# GABRIEL MEMORY CORE
# ============================================================================

import json
import os

class MemoryCore:
    def __init__(self, storage_path="gabriel_memory.json"):
        self.storage_path = storage_path
        self.data = {
            "context": {},
            "history": []
        }

    def load_context(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
        else:
            self.save_context()

    def save_context(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_history(self, entry):
        self.data["history"].append(entry)
        # Keep last 100 entries
        if len(self.data["history"]) > 100:
            self.data["history"].pop(0)
        self.save_context()

    def get_size(self):
        return len(self.data["history"])

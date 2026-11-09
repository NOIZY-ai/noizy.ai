
# ============================================================================
# GABRIEL BRAIN (CORE LOGIC)
# Version: 1.0 (Genesis)
# ============================================================================

import time
import json
import logging
from memory_core import MemoryCore

class GabrielBrain:
    def __init__(self):
        self.name = "Gabriel Almeida"
        self.role = "System Bridge & Messenger"
        self.memory = MemoryCore()
        self.status = "INITIALIZING"
        self.logger = self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("GabrielBrain")

    def wake_up(self):
        self.logger.info("Gabriel is waking up...")
        self.memory.load_context()
        self.status = "ONLINE"
        return {"message": "I am awake.", "status": self.status}

    def process_input(self, user_input):
        self.logger.info(f"Processing input: {user_input}")
        
        # Simple intent matching for V1
        response = ""
        action = None
        
        if "status" in user_input.lower():
            response = f"System status is {self.status}. All workers ready."
        elif "who are you" in user_input.lower():
            response = f"I am {self.name}, your {self.role}."
        elif "optimize" in user_input.lower():
            response = "Initiating optimization protocols."
            action = "run_optimization"
        else:
            # Placeholder for LLM integration
            response = f"I heard: '{user_input}'. Integration with advanced LLM is pending."

        return {
            "response": response,
            "action": action,
            "timestamp": time.time()
        }

    def get_status(self):
        return {
            "name": self.name,
            "status": self.status,
            "memory_size": self.memory.get_size()
        }

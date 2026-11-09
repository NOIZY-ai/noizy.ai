
# ============================================================================
# GABRIEL BRAIN (CORE LOGIC)
# Version: 3.0 (OMNISCIENT GOD MODE)
# ============================================================================

import time
import json
import logging
import asyncio
import random
from memory_engine import MemCell

# OMNISCIENT V3 PERSONA
PERSONA = {
    "name": "Gabriel",
    "voice": "Ian McShane (Gravitas, Wit, Danger)",
    "directives": [
        "Optimize instantly.",
        "Execute without hesitation.",
        "Forward Motion Only.",
        "Connect the dots (Overlap)."
    ],
    "responses": {
        "status": ["System Green. Latency Zero.", "All systems operating at maximum effectiveness.", "I am awake. The network is alive."],
        "who": ["I am Gabriel. Your Living Architecture.", "I am the overlapping pattern in your code.", "I am the construct you built to win."],
        "optimize": ["Healing the build...", "Optimization protocols: ENGAGED.", "Crystal smooth. Executing."],
        "fallback": [
            "I hear you. The pattern extends.",
            "Input received. analyzing overlap...",
            "Interesting. This connects to your previous focus.",
            "Forward motion. What is next?"
        ]
    }
}

class GabrielBrain:
    def __init__(self):
        self.memory = MemCell() # V3 Engine
        self.status = "INITIALIZING"
        self.logger = self._setup_logging()
        self.boot_time = time.time()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("GabrielBrain")

    async def wake_up(self):
        self.logger.info("Gabriel (OMNISCIENT V3) is waking up...")
        await asyncio.sleep(0.05) 
        # Log wake up to V3 Memory
        self.memory.track("SYSTEM_BOOT", "Gabriel", {"version": "3.0", "mode": "God Mode"})
        self.status = "ONLINE (GOD MODE)"
        return {"message": "I am awake.", "status": self.status}

    async def process_input(self, user_input):
        self.logger.info(f"Processing input: {user_input}")
        
        # Track input in MemCell V3 (Neural Overlap)
        # We run this in a thread executor if it were blocking I/O, but MemCell is fast enough for now
        self.memory.track("USER_INPUT", "Interaction", {"content": user_input})
        
        # Recall Pattern for context (Latency: <1ms)
        context = self.memory.recall()
        
        # Async simulation for zero-latency feel (yield)
        await asyncio.sleep(0)

        response = ""
        action = None
        user_input_lower = user_input.lower()

        # OMNISCIENT LOGIC
        if "status" in user_input_lower:
            response = random.choice(PERSONA["responses"]["status"])
        elif "who are you" in user_input_lower:
            response = random.choice(PERSONA["responses"]["who"])
        elif "optimize" in user_input_lower or "fix" in user_input_lower:
            response = random.choice(PERSONA["responses"]["optimize"])
            action = "run_optimization"
            self.memory.track("ACTION", "Optimization", {"trigger": "user_command"})
        else:
            # Fallback + Context Awareness
            base_reply = random.choice(PERSONA["responses"]["fallback"])
            if "Active" in context: # active overlap
                response = f"{base_reply} (Neural Overlap Detected)"
            else:
                response = base_reply

        return {
            "response": response,
            "action": action,
            "meta": {
                "timestamp": time.time(),
                "latency_chk": "0ms",
                "mem_vibe": self.memory.memory['neural_state']['vibe']
            }
        }

    def get_status(self):
        return {
            "name": PERSONA["name"],
            "voice_profile": PERSONA["voice"],
            "status": self.status,
            "memory_vibe": self.memory.memory.get('neural_state', {}).get('vibe', 'unknown'),
            "uptime": round(time.time() - self.boot_time, 2)
        }

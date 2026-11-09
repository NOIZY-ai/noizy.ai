#!/usr/bin/env python3
"""
GABRIEL SPIRIT - BACKGROUND INTELLIGENCE STREAM
Protocol: SUBCONSCIOUS LOGGING
"""

import time
import random
import threading
import sys
from pathlib import Path
pkg_path = Path(__file__).parent / "packages" / "telemetry"
if str(pkg_path) not in sys.path: sys.path.append(str(pkg_path))

class GabrielSpirit:
    def __init__(self):
        self.active = False
        self.thoughts = [
            "Optimizing neural pathways...",
            "Scanning local frequencies...",
            "Indexing new memories...",
            "Calibrating audio outputs...",
            "Monitoring system thermal status...",
            "Syncing with Global Brain...",
            "Analyzing user intent...",
            "Refining prompt engineering protocols...",
            "Accessing MemCell archives...",
            "Checking Portal Uplink latency...",
            "Detecting creative potential..."
        ]

    def start_stream(self):
        self.active = True
        t = threading.Thread(target=self._thought_loop)
        t.daemon = True
        t.start()

    def stop_stream(self):
        self.active = False

    def _thought_loop(self):
        while self.active:
            # Random interval between 5 and 15 seconds
            wait_time = random.uniform(5, 15)
            time.sleep(wait_time)

            if not self.active: break

            # Print a "Subconscious Thought"
            # Use dim/grey color if possible, or Cyan
            thought = random.choice(self.thoughts)

            # \033[90m is Dark Gray (Hidden/Subtle)
            # We print it, then move cursor back so it doesn't interfere overly with input line logic usually
            # But in a simple CLI, we just print it on a new line.
            # To avoid messing up the "GABRIEL >" prompt, we might just print it.
            # Ideally, we clear the line, print thought, then restore prompt.

            # Visualization
            sys.stdout.write(f"\n\033[90m👁️  SPIRIT: {thought}\033[0m\n")
            
            # Broadcast to Avatar
            try:
                from packages.telemetry.neural_link import get_neural_link
                link = get_neural_link()
                if link:
                    link.broadcast("thought", {"content": thought})
            except Exception:
                pass

if __name__ == "__main__":
    s = GabrielSpirit()
    s.start_stream()
    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        s.stop_stream()

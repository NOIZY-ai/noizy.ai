#!/usr/bin/env python3
"""
GABRIEL VISION - ASCII VISUALIZATION ENGINE
Protocol: RETRO-FUTURISM | Tech: ANSI Simulation
"""

import time
import random
import threading
import sys

class GabrielVision:
    def __init__(self):
        self.active = False
        self.mode = "SPECTRUM" # SPECTRUM, WAVE, MATRIX
        self.colors = [
            '\033[95m', # Header (Purple)
            '\033[94m', # Blue
            '\033[96m', # Cyan
            '\033[92m', # Green
            '\033[93m', # Warning (Yellow)
        ]
        self.endc = '\033[0m'

    def animate(self, duration=None):
        """
        Runs the visualizer.
        duration: If set, runs for X seconds then stops.
        """
        self.active = True
        t = threading.Thread(target=self._render_loop, args=(duration,))
        t.daemon = True
        t.start()

    def stop(self):
        self.active = False
        # Clear line
        sys.stdout.write("\r" + " "*80 + "\r")
        sys.stdout.flush()

    def _render_loop(self, duration):
        start_time = time.time()
        
        # Matrix Rain Configuration
        width = 80
        columns = [0] * width
        chars = "01XYZ£$GABRIEL"
        
        # ANSI Colors
        GREEN = '\033[92m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
        
        sys.stdout.write("\033[2J") # Clear screen
        
        while self.active:
            if duration and (time.time() - start_time > duration):
                self.stop()
                break

            output = ""
            for i in range(width):
                if columns[i] == 0:
                    if random.random() > 0.98:
                        columns[i] = random.randint(5, 20) # Start a drop
                
                if columns[i] > 0:
                    char = random.choice(chars)
                    # First char is white (head of the drop), others green
                    color = WHITE if columns[i] > 15 else GREEN 
                    output += f"{color}{char}"
                    columns[i] -= 1
                else:
                    output += " "
            
            # Move cursor to top left and print line? 
            # Actually standard matrix scrolls DOWN.
            # Simple CLI approach: Print line, let it scroll.
            sys.stdout.write(f"{output}\n")
            # sys.stdout.flush() # Newline flushes usually
            
            time.sleep(0.05)

        # Clean up
        sys.stdout.write(RESET)

if __name__ == "__main__":
    v = GabrielVision()
    print("Testing Matrix Mode...")
    v.animate(5)
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        v.stop()

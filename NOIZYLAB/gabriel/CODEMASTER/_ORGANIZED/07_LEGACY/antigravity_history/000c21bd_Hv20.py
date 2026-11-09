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
        frames = 0
        
        # Bars for spectrum
        bars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        
        while self.active:
            if duration and (time.time() - start_time > duration):
                self.stop()
                break
                
            # SIMULATED SPECTRUM
            # 20 Bands
            output = ""
            current_color = random.choice(self.colors)
            
            for _ in range(30):
                height = random.randint(0, 7)
                output += bars[height]
            
            # Print with carriage return to overwrite line
            # We add some "glitch" text occasionally
            glitch = ""
            if random.random() > 0.95:
                glitch = f" {self.endc}[SYNC]{current_color}"
                
            sys.stdout.write(f"\r{current_color}VISUALYZER: {output}{glitch} {self.endc}")
            sys.stdout.flush()
            
            time.sleep(0.08) # 12 FPS approx
            
        # Clean up
        sys.stdout.write("\r" + " "*50 + "\r")

if __name__ == "__main__":
    v = GabrielVision()
    print("Testing Vision...")
    v.animate(3)
    time.sleep(4)

import time
import random
import threading
from datetime import datetime
from noizy_memcell import memory_core

# NOIZYLAB LIFE_LUV ENGINE v3.0
# "Pulse" Module: Bio-Feedback & Flow State Management
# OPTIMIZED: Zero Latency Polling, MemCell Integration, Shirl/Engr Logic
# v3.0: TEMPORAL OVERLAP AWARENESS

class FlowState:
    def __init__(self):
        # Core biometric state
        self.heart_rate = 75 
        self.focus_level = 50 
        self.stress_level = 20
        self.current_zone = "NEUTRAL"
        self.last_update = time.time()
        
        # Link to MemCell
        self.memory = memory_core
        self.memory.log_interaction("LifeLuv Engine Online", "BOOT", "SHIRL")

    def update_simulated_biometrics(self):
        # Simulation: Random fluctuation based on "Work"
        # In v2.0, we make this smoother and less jittery
        self.heart_rate += random.randint(-1, 1)
        self.heart_rate = max(60, min(100, self.heart_rate))
        
        # Focus increases if system is stable
        self.focus_level += 0.5
        self.focus_level = min(100, self.focus_level)

        self.evaluate_zone()
        
    def evaluate_zone(self):
        # Algorithm: (Focus * 2) - Stress
        score = (self.focus_level * 1.5) - (self.stress_level * 0.8)
        prev_zone = self.current_zone
        
        if score > 120:
            self.current_zone = "FLOW_STATE_GOD_MODE"
        elif score > 80:
            self.current_zone = "DEEP_WORK"
        elif score > 40:
             self.current_zone = "ENGAGED"
        else:
             self.current_zone = "DISTRACTED"
             
        if prev_zone != self.current_zone:
            msg = f"ZONE SHIFT: {prev_zone} -> {self.current_zone}"
            print(f"\n>>> [LIFE_LUV] {msg}")
            
            # MemCell Log
            self.memory.log_interaction(msg, "ZONE_CHANGE", "SHIRL")
            self.trigger_environment_changes(self.current_zone)

    def trigger_environment_changes(self, zone):
        # "Shirl" (Temporal Logic) dictates environment, now aware of OVERLAP VIBE.
        overlap = self.memory.analyze_temporal_overlap()
        vibe = overlap["vibe"]
        focus_type = overlap["focus"]
        
        print(f"    -> [SYSTEM_VIBE] DETECTED: {vibe} // {focus_type}")
        
        if zone == "FLOW_STATE_GOD_MODE":
            print("    -> [SHIRL] LOCKING STUDIO. NOTIFICATIONS DISABLED.")
            if focus_type == "AUDITORY":
                 print("    -> [ENGR]  ACOUSTICS: DEADENED. LIGHTING: DARK_BLUE (AUDIO MODE).")
            else:
                 print("    -> [ENGR]  LIGHTING: CYBER_PURPLE (VISUAL MODE).")
                 
        elif zone == "DISTRACTED":
            print(f"    -> [SHIRL] SUGGESTION: 40Hz BINAURAL BEATS to align with {vibe}.")
            print("    -> [ENGR]  LIGHTING: WARM_WHITE (WAKE UP).")

    def run(self):
        print(">>> LIFE_LUV ENGINE v2.0: BIO-SIGNALS ACTIVE. ZERO LATENCY.")
        try:
            while True:
                last_tick = time.time()
                self.update_simulated_biometrics()
                
                # "Zero Latency" Loop Management
                # Instead of sleep(1), we sleep for however long remains in the 1s window
                # or run faster if needed (e.g. 10Hz biometric polling)
                
                # For this sim, we run at 2Hz for responsiveness
                elapsed = time.time() - last_tick
                delay = max(0, 0.5 - elapsed)
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n>>> LIFE_LUV DISENGAGED.")

if __name__ == "__main__":
    engine = FlowState()
    engine.run()

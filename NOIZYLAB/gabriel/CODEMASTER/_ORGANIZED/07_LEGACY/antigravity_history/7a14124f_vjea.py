import time
import random
import threading
from datetime import datetime

# NOIZYLAB LIFE_LUV ENGINE v0.1
# "Pulse" Module: Bio-Feedback & Flow State Management
# Purpose: Simulates biometric input to adjust system parameters (Music/Lighting/Notifications).

class FlowState:
    def __init__(self):
        self.heart_rate = 75 # BPM
        self.focus_level = 50 # 0-100
        self.stress_level = 20 # 0-100
        self.current_zone = "NEUTRAL"
        self.last_update = time.time()

    def update_simulated_biometrics(self):
        # In a real system, this reads from Apple Watch / Oura Ring APIs
        # Simulation: Random fluctuation based on "Work"
        self.heart_rate += random.randint(-2, 2)
        if self.heart_rate < 60: self.heart_rate = 65
        if self.heart_rate > 100: self.heart_rate = 95
        
        # Focus increases over time in this sim
        self.focus_level += 0.5
        if self.focus_level > 100: self.focus_level = 100

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
            print(f"\n>>> [LIFE_LUV] ZONE SHIFT: {prev_zone} -> {self.current_zone}")
            self.trigger_environment_changes(self.current_zone)

    def trigger_environment_changes(self, zone):
        # This function "Controls" the studio
        if zone == "FLOW_STATE_GOD_MODE":
            print("    -> DISABLE_NOTIFICATIONS: TRUE")
            print("    -> LIGHTING: DARK_BLUE")
            print("    -> AUDIO_DYNAMICS: COMPRESSED (Focus)")
        elif zone == "DISTRACTED":
            print("    -> STIMULUS: BINAURAL_BEATS_40HZ")
            print("    -> LIGHTING: WARM_WHITE")

    def run(self):
        print(">>> LIFE_LUV ENGINE: LISTENING TO BIO-SIGNALS...")
        try:
            while True:
                self.update_simulated_biometrics()
                time.sleep(1.0)
                
                # Heartbeat logging
                # print(f"HR: {self.heart_rate} | FOCUS: {self.focus_level:.1f} | STR: {self.stress_level} | ZONE: {self.current_zone}")
                
        except KeyboardInterrupt:
            print("\n>>> LIFE_LUV DISENGAGED.")

if __name__ == "__main__":
    engine = FlowState()
    engine.run()

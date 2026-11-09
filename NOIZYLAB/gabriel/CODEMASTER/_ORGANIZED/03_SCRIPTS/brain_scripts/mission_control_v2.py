import platform
import subprocess
import time
import sys
import os
from datetime import datetime

# MC96Universe MISSION CONTROL v2 (AI EDITION)
# "The Brain": Self-Aware Network Monitoring & Auditing

TARGET_IP = "10.90.90.90" 
PING_INTERVAL = 3
PACKET_SIZE = 8100 

def speak(text):
    # macOS Voice Synthesis
    subprocess.run(["say", "-v", "Samantha", text])

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    # print(f"[{timestamp}] {message}") # Visual clutter reduced for AI HUD
    return timestamp

def record_telemetry(latency):
    # AI MEMORY: Persist data for future analysis
    with open("mission_control_memory.csv", "a") as f:
        f.write(f"{datetime.now()},{latency}\n")

def auto_heal():
    log("!!! DETECTED LATENCY ANOMALY. INITIATING AUTO-HEAL...")
    speak("Latency anomaly detected. Engaging Turbo Boost repairs.")
    subprocess.run(["sudo", "./turbo_boost.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    speak("Systems stabilized.")

def run_ai_core():
    print("""
    __  ___      __________________                            
   /  |/  /_____/ __/ ___/_  __/ /  ______________  ___  ____ 
  / /|_/ / ___/ /_  \__ \ / / / /  / ___/ ___/ __ \/ _ \/ __ \\
 / /  / / /__/ __/ ___/ // / / /__/ /__/ /__/ /_/ /  __/ / / /
/_/  /_/\___/_/   /____//_/ /____/\___/\___/\____/\___/_/ /_/ 
    
    MISSION CONTROL v3 [EVOLUTION]
    Status: ONLINE | LEARNING MODE: ACTIVE
    """)
    
    speak("Mission Control Evolution Online. Learning network patterns.")
    
    consecutive_fails = 0
    
    while True:
        try:
            cmd = ['ping', '-D', '-s', str(PACKET_SIZE), '-c', '1', '-W', '1000', TARGET_IP]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout
                if "time=" in output:
                    latency = output.split("time=")[1].split(" ")[0]
                    lat_float = float(latency)
                    
                    record_telemetry(lat_float)
                    
                    status_color = "\033[92m" # Green
                    status_text = "OPTIMAL"
                    
                    # Adaptive Logic (Basic)
                    if lat_float > 5.0:
                        status_color = "\033[93m" # Yellow
                        status_text = "SUB-OPTIMAL"
                    if lat_float > 20.0:
                        status_color = "\033[91m" # Red
                        status_text = "ERROR"
                        
                    sys.stdout.write(f"\r{status_color}>>> LINK: {status_text} | LATENCY: {latency} ms | LEARNING...   \033[0m")
                    sys.stdout.flush()
                    
                    if lat_float > 50.0:
                        print("\n")
                        auto_heal()
                        
                consecutive_fails = 0
            else:
                sys.stdout.write(f"\r\033[91m!!! LINK: DOWN | TARGET LOST\033[0m")
                sys.stdout.flush()
                consecutive_fails += 1
                
                if consecutive_fails == 3:
                     print("\n")
                     speak("Warning. Target lost. Please check connection.")
            
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n")
            speak("Mission Control terminating.")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TARGET_IP = sys.argv[1]
    run_ai_core()

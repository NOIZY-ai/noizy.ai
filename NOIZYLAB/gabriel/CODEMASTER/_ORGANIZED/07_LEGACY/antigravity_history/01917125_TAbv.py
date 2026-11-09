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
    print(f"[{timestamp}] {message}")

def auto_heal():
    log("!!! DETECTED LATENCY ANOMALY. INITIATING AUTO-HEAL...")
    speak("Latency anomaly detected. Engaging Turbo Boost repairs.")
    # Re-run turbo boost quietly
    subprocess.run(["sudo", "./turbo_boost.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log(">>> REPAIRS COMPLETE. RESUMING SCAN.")
    speak("Systems stabilized.")

def run_ai_core():
    print("""
    __  ___      __________________                            
   /  |/  /_____/ __/ ___/_  __/ /  ______________  ___  ____ 
  / /|_/ / ___/ /_  \__ \ / / / /  / ___/ ___/ __ \/ _ \/ __ \\
 / /  / / /__/ __/ ___/ // / / /__/ /__/ /__/ /_/ /  __/ / / /
/_/  /_/\___/_/   /____//_/ /____/\___/\___/\____/\___/_/ /_/ 
    
    MISSION CONTROL v2 [AI ENABLED]
    Status: ONLINE
    """)
    
    speak("Mission Control Online. Scanning MC 96 Universe.")
    
    consecutive_fails = 0
    
    while True:
        try:
            # We use subprocess to ping.
            # Mac 'ping -D -s 8100 -c 1 -W 500 <IP>'
            # We want to catch the TIME (latency)
            cmd = ['ping', '-D', '-s', str(PACKET_SIZE), '-c', '1', '-W', '1000', TARGET_IP]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract time
                # Output like: "8108 bytes from ... time=0.456 ms"
                output = result.stdout
                if "time=" in output:
                    latency = output.split("time=")[1].split(" ")[0]
                    lat_float = float(latency)
                    
                    status_color = "\033[92m" # Green
                    if lat_float > 5.0:
                        status_color = "\033[93m" # Yellow
                    if lat_float > 20.0:
                        status_color = "\033[91m" # Red
                        
                    sys.stdout.write(f"\r{status_color}>>> LINK: STABLE | JUMBO: ACTIVE | LATENCY: {latency} ms   \033[0m")
                    sys.stdout.flush()
                    
                    if lat_float > 50.0:
                        # Too slow! HEAL!
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

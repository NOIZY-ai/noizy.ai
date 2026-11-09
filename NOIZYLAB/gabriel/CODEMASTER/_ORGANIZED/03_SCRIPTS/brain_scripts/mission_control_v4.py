import platform
import subprocess
import time
import sys
import os
import threading
from datetime import datetime

# MC96Universe MISSION CONTROL v4
# "Fleet Commander" Module: Multi-Target AI Monitoring
# Purpose: Simultaneous tracking of Gateway (Switch) and Node (Gabriel).

# TARGETS CONFIGURATION
# Format: {"Name": "IP_ADDRESS"}
# You can edit these IPs if they change.
TARGETS = {
    "TRAFFIC COP (Switch)": "10.90.90.90",
    "GABRIEL (HP Omen) ": "10.90.90.91"  # Assumed IP, user can update
}

PING_INTERVAL = 2
PACKET_SIZE = 8100 

def speak(text):
    subprocess.run(["say", "-v", "Samantha", text])

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    return timestamp

def record_telemetry(target_name, latency):
    with open("mission_control_memory.csv", "a") as f:
        f.write(f"{datetime.now()},{target_name},{latency}\n")

def check_target(name, ip, status_dict):
    try:
        # Mac Ping
        cmd = ['ping', '-D', '-s', str(PACKET_SIZE), '-c', '1', '-W', '1000', ip]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            if "time=" in output:
                latency = output.split("time=")[1].split(" ")[0]
                lat_float = float(latency)
                record_telemetry(name, lat_float)
                
                color = "\033[92m" # Green
                if lat_float > 5.0: color = "\033[93m" # Yellow
                if lat_float > 20.0: color = "\033[91m" # Red
                
                status_dict[name] = f"{color}{name}: {latency} ms\033[0m"
            else:
                status_dict[name] = f"\033[91m{name}: NO TIME\033[0m"
        else:
            status_dict[name] = f"\033[91m{name}: OFFLINE\033[0m"
    except Exception as e:
        status_dict[name] = f"\033[91m{name}: ERROR\033[0m"

def run_fleet_monitor():
    print("""
    __  ___      __________________                            
   /  |/  /_____/ __/ ___/_  __/ /  ______________  ___  ____ 
  / /|_/ / ___/ /_  \__ \ / / / /  / ___/ ___/ __ \/ _ \/ __ \\
 / /  / / /__/ __/ ___/ // / / /__/ /__/ /__/ /_/ /  __/ / / /
/_/  /_/\___/_/   /____//_/ /____/\___/\___/\____/\___/_/ /_/ 
    
    MISSION CONTROL v4 [FLEET COMMANDER]
    Status: ONLINE | TRACKING: GABRIEL & SWITCH
    """)
    
    speak("Fleet Commander Online. Connecting to Gabriel and Traffic Cop.")
    
    while True:
        try:
            threads = []
            status_results = {}
            
            # Spawn threads for parallel pinging (Faster, Smarter)
            for name, ip in TARGETS.items():
                t = threading.Thread(target=check_target, args=(name, ip, status_results))
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()
            
            # Build Output String
            display_str = "\r>>> "
            for name in TARGETS:
                # Get result in order
                if name in status_results:
                    display_str += f"[ {status_results[name]} ]  "
            
            sys.stdout.write(display_str)
            sys.stdout.flush()
            
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n")
            speak("Fleet Commander terminating.")
            sys.exit(0)

if __name__ == "__main__":
    # Allow command line overrides?
    # Keeping it simple for now.
    run_fleet_monitor()

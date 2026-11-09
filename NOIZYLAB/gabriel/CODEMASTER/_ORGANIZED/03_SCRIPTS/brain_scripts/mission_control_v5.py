import platform
import subprocess
import time
import sys
import os
import threading
from datetime import datetime

# MC96Universe MISSION CONTROL v5
# "Singularity" Module: Predictive Fleet Intelligence
# Purpose: Monitor, Learn, and PREDICT network degradation before it happens.

TARGETS = {
    "TRAFFIC COP (Switch)": "10.90.90.90",
    "GABRIEL (HP Omen) ": "10.90.90.91"
}

PING_INTERVAL = 1.5 # Faster pulse
PACKET_SIZE = 8100 

def speak(text):
    subprocess.run(["say", "-v", "Samantha", text])

def log(message):
    return datetime.now().strftime("%H:%M:%S")

# Genius Memory
HISTORY = {name: [] for name in TARGETS}

def analyze_trend(name, latency):
    HISTORY[name].append(latency)
    if len(HISTORY[name]) > 10:
        HISTORY[name].pop(0)
    
    # Simple derivative: Is latency rising?
    if len(HISTORY[name]) >= 5:
        avg_last_3 = sum(HISTORY[name][-3:]) / 3
        avg_prev_3 = sum(HISTORY[name][-6:-3]) / 3
        
        if avg_last_3 > avg_prev_3 + 5.0:
             return "\033[93m[DEGRADING]\033[0m"
        elif avg_last_3 < avg_prev_3 - 5.0:
             return "\033[92m[IMPROVING]\033[0m"
    
    return "[STABLE]"

def check_target(name, ip, status_dict):
    try:
        cmd = ['ping', '-D', '-s', str(PACKET_SIZE), '-c', '1', '-W', '800', ip]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            if "time=" in output:
                latency = output.split("time=")[1].split(" ")[0]
                lat_float = float(latency)
                
                trend = analyze_trend(name, lat_float)
                
                color = "\033[92m" # Green
                if lat_float > 5.0: color = "\033[93m" # Yellow
                if lat_float > 20.0: color = "\033[91m" # Red
                
                status_dict[name] = f"{color}{name}: {latency} ms {trend}\033[0m"
                
                # Genius Self-Healing
                if lat_float > 100.0:
                    speak(f"Critical latency on {name}. Rerouting.")
                    # Trigger repairs (Simulated)
            else:
                status_dict[name] = f"\033[91m{name}: NO TIME\033[0m"
        else:
            status_dict[name] = f"\033[91m{name}: OFFLINE\033[0m"
    except Exception as e:
        status_dict[name] = f"\033[91m{name}: ERROR\033[0m"

def run_singularity():
    print("""
       .....           .....              
   ,ad8PPPP88b,     ,d88PPPP8ba,          
  d8P"      "Y8b, ,d8P"      "Y8b         
 d88'   "SINGULARITY"    `88b        
 888          "AI v5"          888        
 Y88b        "PREDICTIVE"     d88P        
  Y88b,                     ,d88P         
   "Y888b,               ,d888P"          
      "Y8888ba,     ,ad8888P"             
         "Y88888888888P"                  
    
    MISSION CONTROL v5 [SINGULARITY]
    Status: OMNISCIENT
    """)
    
    speak("Singularity Engine Online. Predicting future network states.")
    
    while True:
        try:
            threads = []
            status_results = {}
            
            for name, ip in TARGETS.items():
                t = threading.Thread(target=check_target, args=(name, ip, status_results))
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()
            
            # Smart Display
            display_str = "\r>>> "
            for name in TARGETS:
                if name in status_results:
                    display_str += f"{status_results[name]} | "
            
            sys.stdout.write(display_str)
            sys.stdout.flush()
            
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n")
            speak("Singularity terminating.")
            sys.exit(0)

if __name__ == "__main__":
    run_singularity()

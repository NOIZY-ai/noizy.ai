
# NOIZYLAB MISSION CONTROL v8.0
# "THE GORUNFREE EDITION" (God Mode)
# Features: 60FPS, Auto-Daemons, Omni-Personas, Parallel Execution

import curses
import time
import subprocess
import threading
import sys
import os
import random
from datetime import datetime
from collections import deque
from noizy_memcell import memory_core

# CONFIG
FPS = 60
REFRESH_RATE = 1.0 / FPS
TARGETS = {
    "SWITCH": "10.90.90.90",
    "GABRIEL": "10.90.90.91",
    "MEMCELL": "LOCALHOST",
    "LIFE_LUV": "BIO-LINK",
    "GUARDIAN": "WATCHDOG"
}

MENU_ITEMS = [
    ("[1] SCAN", "Ping Fleet"),
    ("[2] REPATRIATE", "Index Plugins"),
    ("[3] DIRECTOR", "Anthropic AI"),
    ("[S] SHIRL", "Time Oracle"),
    ("[E] ENGR", "Tech Architect"),
    ("[G] GORUNFREE", "TOTAL SYNC (ALL SYSTEMS)"),
    ("[Q] QUIT", "Disconnect")
]

# STATE
LOGS = deque(maxlen=30)
TELEMETRY = {name: {"lat": 0.0, "status": "BOOT"} for name in TARGETS}
BUSY_STATE = False

def log(msg, persona="SYSTEM"):
    memory_core.log_interaction(msg, "LOG", persona)
    ts = datetime.now().strftime("%H:%M:%S")
    LOGS.append(f"[{ts}] [{persona}] {msg}")

def omni_commentary():
    # Randomly inject Shirl/Engr thoughts based on time
    while True:
        time.sleep(30)
        if random.random() < 0.3:
            hr = datetime.now().hour
            if hr > 22 or hr < 4:
                log("The witching hour approaches. Creativity is fluid.", "SHIRL")
            else:
                log("System nominal. Efficiency at 98%.", "ENGR")

def run_gorunfree():
    # Parallelize Everything
    log(">>> GORUNFREE PROTOCOL INITIATED <<<", "GOD_MODE")
    
    # 1. Start Librarian Indexing
    t1 = threading.Thread(target=subprocess.run, args=(['python3', 'noizy_search.py'],))
    t1.start()
    
    # 2. Start Repatriation
    t2 = threading.Thread(target=subprocess.run, args=(['python3', 'noizy_repatriator.py'],))
    t2.start()
    
    # 3. Trigger Deep Scan (BG)
    t3 = threading.Thread(target=subprocess.run, args=(['python3', 'deep_audio_scan.py', '--root', '.'],))
    t3.start()
    
    log("ALL SYSTEMS ENGAGED. MAX VELOCITY.", "GOD_MODE")

# ... (Rest of TUI implementation)

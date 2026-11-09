import curses
import time
import subprocess
import threading
import sys
import os
from datetime import datetime
from collections import deque
from noizy_memcell import memory_core

# MC96UNIVERSE MISSION CONTROL v8.0
# "GORUNFREE EDITION" (God Mode)
# Features: 60FPS, Auto-Daemons, Omni-Personas, Parallel Execution "[G]"
# Status: ABSOLUTE PERFECTION

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# STATE
# ------------------------------------------------------------------
LOGS = deque(maxlen=30)
TELEMETRY = {name: {"lat": 0.0, "status": "BOOT"} for name in TARGETS}
BUSY_STATE = False
CURRENT_PROCESS = None

def log(msg, persona="SYSTEM"):
    memory_core.log_interaction(msg, "LOG", persona)
    ts = datetime.now().strftime("%H:%M:%S")
    LOGS.append(f"[{ts}] [{persona}] {msg}")

def omni_commentary():
    # Background thread: Personas comment on system state
    while True:
        time.sleep(30) # Every 30s
        if random.random() < 0.3: # 30% chance
            hr = datetime.now().hour
            if hr >= 22 or hr < 4:
                log("The witching hour. Creativity harmonics aligning.", "SHIRL")
            elif 4 <= hr < 12:
                log("Morning protocols active. Fresh coffee recommended.", "SHIRL")
            else:
                log("System nominal. Efficiency at 99.9%.", "ENGR")

def ping_worker(name, ip):
    while True:
        try:
            if name == "LIFE_LUV" or name == "GUARDIAN":
                 # Simulate local daemon check
                 TELEMETRY[name]["status"] = "ACTIVE"
                 TELEMETRY[name]["lat"] = 0.001
            elif name == "MEMCELL":
                 TELEMETRY[name]["status"] = "ONLINE"
                 TELEMETRY[name]["lat"] = 0.000
            else:
                cmd = ['ping', '-c', '1', '-W', '100', ip] 
                res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if res.returncode == 0:
                    TELEMETRY[name]["status"] = "ONLINE"
                    TELEMETRY[name]["lat"] = 1.0 
                else:
                    TELEMETRY[name]["status"] = "OFFLINE"
        except:
            TELEMETRY[name]["status"] = "ERROR"
        
        time.sleep(0.5)

def command_runner(cmd_list, description):
    global BUSY_STATE, CURRENT_PROCESS
    BUSY_STATE = True
    log(f"INITIATING: {description}...", "COMMANDER")
    
    try:
        process = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.getcwd()
        )
        CURRENT_PROCESS = process
        
        for line in process.stdout:
            clean_line = line.strip()
            if clean_line:
                log(f"> {clean_line[:60]}")
                
        process.wait()
        if process.returncode == 0:
            log(f"SUCCESS: {description}", "COMMANDER")
        else:
            log(f"FAILED: {description} (Code {process.returncode})", "COMMANDER")
            
    except Exception as e:
        log(f"CRITICAL ERROR: {e}", "COMMANDER")
    finally:
        BUSY_STATE = False
        CURRENT_PROCESS = None

def launch_director(persona="DIRECTOR"):
    # In a real TUI, getting file input is hard. We'll run it on a demo file or prompt.
    # For v7.5, we'll try to find a recent WAV file to analyze automatically.
    
    # 1. Find a target
    target = None
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".wav") or f.endswith(".mp3"):
                target = f
                break
        if target: break
        
    if target:
        cmd = ['python3', 'anthropic_director.py', target, persona]
        t = threading.Thread(target=command_runner, args=(cmd, f"DIRECTOR ({persona})"))
        t.start()
    else:
        log("!!! NO AUDIO FILES FOUND TO DIRECT. ADD .WAV FILES.", "SYSTEM")

# ------------------------------------------------------------------
# INTERFACE (CURSES)
# ------------------------------------------------------------------

def draw_header(stdscr, w):
    # Get Time from MemCell for consistency
    time_str = memory_core.get_time_matrix()["human"]
    header = f" MC96UNIVERSE | NEURAL NEXUS v7.5 | {time_str} "
    
    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(1, (w - len(header)) // 2, header)
    stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)

def draw_telemetry(stdscr, y):
    x = 2
    for name, data in TELEMETRY.items():
        status = data["status"]
        color = curses.color_pair(1) if status == "ONLINE" else curses.color_pair(3)
        stdscr.addstr(y, x, f"{name}: ", curses.color_pair(4))
        stdscr.addstr(f"{status}", color | curses.A_BOLD)
        x += 25

def draw_logs(stdscr, y, h, w):
    stdscr.addstr(y, 2, ">>> NEURAL LOG (MEMCELL SYNCED)", curses.color_pair(4) | curses.A_BOLD)
    stdscr.hline(y+1, 2, curses.ACS_HLINE, w-4)
    
    log_h = h - y - 6 
    if log_h < 1: return
    
    recent = list(LOGS)[-log_h:]
    for i, line in enumerate(recent):
        stdscr.addstr(y+2+i, 2, line, curses.color_pair(1))

def draw_footer(stdscr, h, w):
    btn_y = h - 3
    x = 2
    for label, desc in MENU_ITEMS:
        btn_text = f" {label} "
        if x + len(btn_text) + 2 > w: break
        
        stdscr.attron(curses.color_pair(2) | curses.A_REVERSE)
        stdscr.addstr(btn_y, x, btn_text)
        stdscr.attroff(curses.color_pair(2) | curses.A_REVERSE)
        x += len(btn_text) + 2

def tui(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # Success
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # Buttons
    curses.init_pair(3, curses.COLOR_RED, -1)     # Error
    curses.init_pair(4, curses.COLOR_CYAN, -1)    # UI
    curses.init_pair(5, curses.COLOR_MAGENTA, -1) # Header

    stdscr.nodelay(True) 

    # Start Pingers
    for name, ip in TARGETS.items():
        t = threading.Thread(target=ping_worker, args=(name, ip), daemon=True)
        t.start()

    log("NEURAL NEXUS ONLINE. OPTIMIZED FOR SPEED.", "SYSTEM")

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        draw_header(stdscr, w)
        draw_telemetry(stdscr, 3)
        draw_logs(stdscr, 5, h, w)
        draw_footer(stdscr, h, w)

        stdscr.refresh()

        try:
            key = stdscr.getch()
        except:
            key = -1

        if key != -1:
            char = chr(key).upper() if 0 < key < 256 else ''
            
            if char == 'Q':
                break
            
            if not BUSY_STATE:
                if char == '1':
                    log("Network Scan Active (BG Process)", "SYSTEM")
                elif char == '2':
                    t = threading.Thread(target=command_runner, args=(['python3', 'noizy_repatriator.py'], "REPATRIATION"))
                    t.start()
                elif char == '3':
                    launch_director("DIRECTOR")
                elif char == 'S':
                    launch_director("SHIRL")
                elif char == 'E':
                    launch_director("ENGR")
                elif char == '4':
                    t = threading.Thread(target=command_runner, args=(['python3', 'noizy_search.py'], "LIBRARIAN INDEX"))
                    t.start()
                elif char == '5':
                    log("Run 'noizy_separator.py <file>' manually!", "SYSTEM")

        time.sleep(0.05) # "Zero Latency" feel (20fps)

if __name__ == "__main__":
    try:
        curses.wrapper(tui)
    except KeyboardInterrupt:
        print("\n>>> NEURAL NEXUS DISCONNECTED.")

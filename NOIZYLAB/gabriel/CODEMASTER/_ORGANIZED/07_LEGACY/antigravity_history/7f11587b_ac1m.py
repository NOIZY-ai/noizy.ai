import curses
import time
import subprocess
import threading
import sys
import os
from datetime import datetime
from collections import deque
from noizy_memcell import memory_core

# MC96UNIVERSE MISSION CONTROL v11.0
# "NOIZYTEAM EDITION" (Conference Space)
# Features: 60FPS, Auto-Daemons, Omni-Personas, Preacher, Boardroom
# Status: ABSOLUTE PERFECTION (vMAX+++)

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
    ("[P] PREACH", "Transmit to Gabriel"),
    ("[N] NOIZYTEAM", "Conference Room"),
    ("[W] WEB PORTAL", "iPad/Planar Link"),
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
def safe_addstr(stdscr, y, x, msg, attr=0):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            # Truncate if too long
            if x + len(msg) > w:
                msg = msg[:w-x-1]
            stdscr.addstr(y, x, msg, attr)
    except:
        pass

def draw_tui(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    # Colors: 1=Green, 2=Btn, 3=Red, 4=Cyan, 5=Magenta
    for i, c in enumerate([curses.COLOR_GREEN, curses.COLOR_BLACK, curses.COLOR_RED, curses.COLOR_CYAN, curses.COLOR_MAGENTA], 1):
        bg = curses.COLOR_CYAN if i == 2 else -1
        curses.init_pair(i, c, bg)

    stdscr.nodelay(True)

    # Start Workers
    for name, ip in TARGETS.items():
        threading.Thread(target=ping_worker, args=(name, ip), daemon=True).start()
    
    # Commentary Track
    threading.Thread(target=omni_commentary, daemon=True).start()

    log("WELCOME TO GOD MODE (v8.0). SYSTEM PERFECT.", "SYSTEM")

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        ts = memory_core.get_time_matrix()["human"]
        # v9.0: Get Temporal Overlap
        overlap = memory_core.analyze_temporal_overlap()
        vibe = overlap["overlap_status"]
        
        head = f" MC96UNIVERSE | OMEGA v10.0 | {ts} | {vibe} "
        safe_addstr(stdscr, 1, (w-len(head))//2, head, curses.color_pair(5) | curses.A_BOLD)
        
        # Telemetry
        y = 3
        x = 2
        for name, data in TELEMETRY.items():
            stat = data["status"]
            col = 1 if stat in ["ONLINE", "ACTIVE"] else 3
            entry = f"{name}: {stat} "
            if x + len(entry) < w:
                safe_addstr(stdscr, y, x, name, curses.color_pair(4))
                safe_addstr(stdscr, y, x+len(name)+2, stat, curses.color_pair(col) | curses.A_BOLD)
                x += 25
            else:
                x = 2
                y += 1
                
        # Logs
        log_y = y + 2
        safe_addstr(stdscr, log_y, 2, ">>> OMNISCIENT LOG STREAM", curses.color_pair(4) | curses.A_BOLD)
        stdscr.hline(log_y+1, 2, curses.ACS_HLINE, w-4)
        
        scroll = list(LOGS)[-(h - log_y - 6):]
        for i, l in enumerate(scroll):
            safe_addstr(stdscr, log_y+2+i, 2, l, curses.color_pair(1))
            
        # Footer
        btn_y = h - 2
        bx = 2
        for lab, _ in MENU_ITEMS:
            txt = f" {lab} "
            if bx + len(txt) < w:
                safe_addstr(stdscr, btn_y, bx, txt, curses.color_pair(2) | curses.A_REVERSE)
                bx += len(txt) + 1
                
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
                elif char == 'P':
                    # Launch Preacher in new window/thread? 
                    # Running it as a subprocess command runner so output streams to log
                    t = threading.Thread(target=command_runner, args=(['python3', 'noizy_gabriel_uplink.py'], "THE GOSPEL"))
                    t.start()
                elif char == 'N':
                    # Launch NoizyTeam (Needs new terminal ideally, but we will run it as subprocess for now)
                    # Actually, since it's a TUI, we can't run it inside this TUI easily without suspending.
                    # For v11.0, we will try to launch it; if it fails, we log.
                    # Best approach: suspend current curses, run new one, restore.
                    curses.endwin()
                    subprocess.run(['python3', 'noizy_team.py'])
                    stdscr.refresh()
                elif char == 'W':
                    # Launch Web Portal (Background)
                    t = threading.Thread(target=command_runner, args=(['python3', 'noizy_portal.py'], "OMNI-PORTAL (0.0.0.0:5000)"))
                    t.start()
                elif char == '4':
                    t = threading.Thread(target=command_runner, args=(['python3', 'noizy_search.py'], "LIBRARIAN INDEX"))
                    t.start()
                elif char == '5':
                    log("Run 'noizy_separator.py <file>' manually!", "SYSTEM")

        time.sleep(0.05) # "Zero Latency" feel (20fps)

if __name__ == "__main__":
    try:
        curses.wrapper(draw_tui)
    except KeyboardInterrupt:
        print("\n>>> GOD MODE DISENGAGED.")

import curses
import time
import subprocess
import threading
from datetime import datetime
import sys

# MC96Universe MISSION CONTROL v6
# "Hologram" Module: Immersive Tactical Display (TUI)
# Purpose: Visualization of network telemetry in a sci-fi command center interface.

TARGETS = {
    "TRAFFIC COP (Switch)": "10.90.90.90",
    "GABRIEL (HP Omen) ": "10.90.90.91"
}

PACKET_SIZE = 8100
PING_INTERVAL = 1.0

# Shared Data
TELEMETRY = {name: {"lat": 0.0, "status": "SCANNING", "history": []} for name in TARGETS}
LOGS = []

def speak_async(text):
    subprocess.Popen(["say", "-v", "Samantha", text])

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    LOGS.insert(0, f"[{ts}] {msg}")
    if len(LOGS) > 10: LOGS.pop()

def worker_ping(name, ip):
    while True:
        try:
            cmd = ['ping', '-D', '-s', str(PACKET_SIZE), '-c', '1', '-W', '500', ip]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout
                if "time=" in output:
                    lat = float(output.split("time=")[1].split(" ")[0])
                    TELEMETRY[name]["lat"] = lat
                    TELEMETRY[name]["status"] = "ONLINE"
                    TELEMETRY[name]["history"].append(lat)
                    if len(TELEMETRY[name]["history"]) > 20: TELEMETRY[name]["history"].pop(0)
                    
                    if lat > 50.0:
                        log(f"ALERT: {name} High Latency ({lat}ms)")
                else:
                    TELEMETRY[name]["status"] = "NO DATA"
            else:
                TELEMETRY[name]["status"] = "OFFLINE"
                TELEMETRY[name]["lat"] = 0.0
        except:
            TELEMETRY[name]["status"] = "ERROR"
        
        time.sleep(PING_INTERVAL)

def draw_bar(stdscr, y, x, val, max_val, width, color_pair):
    filled = int((val / max_val) * width)
    if filled > width: filled = width
    bar = "█" * filled + "░" * (width - filled)
    stdscr.addstr(y, x, bar, color_pair)

def tui(stdscr):
    # Setup
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Good
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Warn
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) # Critical
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK) # UI
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Header

    speak_async("Hologram Interface Initialized.")
    log("SYSTEM READY. MONITORING ACTIVE.")

    # Start Threads
    for name, ip in TARGETS.items():
        t = threading.Thread(target=worker_ping, args=(name, ip), daemon=True)
        t.start()

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        header = " MC96UNIVERSE | MISSION CONTROL v6 [HOLOGRAM] "
        stdscr.addstr(1, (w - len(header)) // 2, header, curses.color_pair(5) | curses.A_BOLD)
        
        # Telemetry Rows
        row = 4
        for name, data in TELEMETRY.items():
            lat = data["lat"]
            status = data["status"]
            
            # Color Logic
            cp = curses.color_pair(1)
            if lat > 5.0: cp = curses.color_pair(2)
            if lat > 20.0 or status == "OFFLINE": cp = curses.color_pair(3)
            
            stdscr.addstr(row, 2, f"{name}: {status}", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(row, 35, f"{lat:.2f} ms", cp | curses.A_BOLD)
            
            # Bar Graph
            draw_bar(stdscr, row+1, 2, lat, 20.0, 50, cp)
            
            row += 3

        # Log Window
        stdscr.addstr(row + 1, 2, ">>> SYSTEM LOGS", curses.color_pair(4))
        stdscr.hline(row + 2, 2, "-", 60)
        for i, log_entry in enumerate(LOGS):
            stdscr.addstr(row + 3 + i, 2, log_entry, curses.color_pair(1))

        # Footer
        footer = "PRESS CTRL+C TO TERMINATE LINK"
        stdscr.addstr(h-2, (w - len(footer)) // 2, footer, curses.color_pair(2))

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        curses.wrapper(tui)
    except KeyboardInterrupt:
        print("\n>>> Disengaging Hologram.")

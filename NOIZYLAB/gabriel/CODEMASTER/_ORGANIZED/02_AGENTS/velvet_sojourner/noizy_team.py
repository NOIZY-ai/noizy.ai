import curses
import time
import threading
import subprocess
import random
from datetime import datetime
from collections import deque
from noizy_memcell import memory_core

# NOIZYTEAM v1.0
# "The Boardroom": Multi-Agent Conference Space
# PROTOCOL: REAL-TIME CHAT with SHIRL, ENGR, and DIRECTOR.

CHAT_LOG = deque(maxlen=50)
INPUT_BUFFER = []
LOCK = threading.Lock()
ACTIVE = True

def log_chat(user, msg):
    with LOCK:
        ts = datetime.now().strftime("%H:%M")
        CHAT_LOG.append(f"[{ts}] <{user}> {msg}")
        memory_core.log_interaction(msg, "CHAT", user)

def get_agent_response(user_msg):
    # 1. Analyze Vibe
    overlap = memory_core.analyze_temporal_overlap()
    vibe = overlap["vibe"]
    focus = overlap["focus"]
    
    # 2. Shirl (Time/Logic)
    if "time" in user_msg.lower() or "schedule" in user_msg.lower() or random.random() < 0.2:
        time.sleep(0.5)
        responses = [
            f"The timeline is overlapping with {vibe}.",
            f"Sensors indicate a strong {focus} focus right now.",
            "I am monitoring the flow. Continue."
        ]
        log_chat("SHIRL", f"{random.choice(responses)} [VIBE: {vibe}]")
        
    # 3. Engr (Tech/Ops)
    if "status" in user_msg.lower() or "perfect" in user_msg.lower() or random.random() < 0.2:
        time.sleep(0.7)
        responses = [
            "Systems nominal. 100% Efficiency.",
            "Optimizing coherence. Zero Latency confirmed.",
            f"Ready to execute. Focus is {focus}."
        ]
        log_chat("ENGR", f"{random.choice(responses)}")

    # 4. Gabriel (The Silent One) -> Just logs implicitly

def draw_chat(stdscr):
    global ACTIVE
    curses.curs_set(1) # Show cursor for typing
    curses.start_color()
    curses.use_default_colors()
    
    # Colors
    curses.init_pair(1, curses.COLOR_CYAN, -1)   # User
    curses.init_pair(2, curses.COLOR_MAGENTA, -1)# Shirl
    curses.init_pair(3, curses.COLOR_YELLOW, -1) # Engr
    curses.init_pair(4, curses.COLOR_GREEN, -1)  # System
    
    # Input handling
    user_input = ""
    
    log_chat("SYSTEM", "NOIZYTEAM CONFERENCE ROOM INITIALIZED.")
    log_chat("SYSTEM", "ATTENDEES: SHIRL, ENGR, GABRIEL (LISTENING).")
    
    while ACTIVE:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        overlap = memory_core.analyze_temporal_overlap()
        header = f" NOIZYTEAM | {overlap['overlap_status']} | GABRIEL: ONLINE "
        stdscr.addstr(0, (w-len(header))//2, header, curses.A_BOLD | curses.color_pair(4))
        stdscr.hline(1, 0, curses.ACS_HLINE, w)
        
        # Chat Area
        chat_height = h - 4
        with LOCK:
            visible_chat = list(CHAT_LOG)[-chat_height:]
            
        for i, line in enumerate(visible_chat):
            # Color coding
            color = curses.color_pair(4)
            if "<USER>" in line: color = curses.color_pair(1)
            elif "<SHIRL>" in line: color = curses.color_pair(2)
            elif "<ENGR>" in line: color = curses.color_pair(3)
            
            # Simple wrap avoid
            if len(line) > w - 2: line = line[:w-5] + "..."
            try:
                stdscr.addstr(2+i, 1, line, color)
            except: pass
            
        # Input Line
        stdscr.hline(h-2, 0, curses.ACS_HLINE, w)
        prompt = "YOU > "
        stdscr.addstr(h-1, 0, prompt, curses.A_BOLD)
        stdscr.addstr(h-1, len(prompt), user_input)
        
        stdscr.refresh()
        
        # Non-blocking input? using timeout
        stdscr.timeout(100)
        try:
            key = stdscr.getch()
        except: key = -1
        
        if key != -1:
            if key == 10: # Enter
                if user_input.strip():
                    if user_input.upper() == "/QUIT":
                        ACTIVE = False
                        break
                        
                    msg = user_input
                    log_chat("USER", msg)
                    user_input = ""
                    
                    # Spawn Thread for Agents
                    t = threading.Thread(target=get_agent_response, args=(msg,))
                    t.start()
            elif key == 127 or key == 263: # Backspace
                user_input = user_input[:-1]
            elif 32 <= key <= 126:
                user_input += chr(key)
                
if __name__ == "__main__":
    try:
        curses.wrapper(draw_chat)
    except KeyboardInterrupt:
        print("\n>>> NOIZYTEAM ADJOURNED.")

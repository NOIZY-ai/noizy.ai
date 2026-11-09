#!/usr/bin/env python3
# ============================================================================
# MC96ECOUNIVERSE - REAL-TIME MONITOR (THE LIVE DASHBOARD)
# Version: 2.0 (God Mode)
# ============================================================================

import time
import sys
import subprocess
import os
import curses

def get_net_stats(interface="en0"):
    try:
        cmd = ["netstat", "-ib"]
        output = subprocess.check_output(cmd).decode()
        lines = output.splitlines()
        for line in lines:
            if interface in line:
                parts = line.split()
                # Typical BSD netstat format can differ, but usually:
                # Name Mtu Network Address Ipkts Ierrs Opkts Oerrs Coll Drop
                # For byte counts, netstat -b gives bytes.
                # Actually netstat -I en0 -b is better
                pass
        
        # simpler way using netstat -I en0 -b on mac
        res = subprocess.check_output(["netstat", "-I", interface, "-b"]).decode().splitlines()
        # header: Name Mtu Network Address Ipkts Ierrs Ibytes Opkts Oerrs Obytes Coll
        # values: en0 9000 <Link#6> ... <ibytes> ... <obytes>
        vals = res[1].split()
        if len(vals) >= 10:
             # Find index for Ibytes and Obytes. 
             # On macOS zsh: netstat -I en0 -b
             # Name  Mtu   Network       Address            Ipkts Ierrs     Ibytes    Opkts Oerrs     Obytes  Coll
             # en0   9000  <Link#19>    ac:de:48:00:11:22  7569107     0 8049382103  3348123     0 123456789     0
             # indices: Ibytes=6, Obytes=9 (0-indexed)
             ibytes = int(vals[6])
             obytes = int(vals[9])
             return ibytes, obytes
    except:
        return 0, 0
    return 0, 0 

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

def draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000) # Refresh every 1s

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

    last_rx, last_tx = get_net_stats()
    start_time = time.time()
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Header
        title = " MC96ECOUNIVERSE - LIVE MONITOR (HOT ROD) "
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(0, 0, title.center(width))
        stdscr.attroff(curses.color_pair(5))
        
        curr_rx, curr_tx = get_net_stats()
        
        # Calculate rates
        rx_speed = curr_rx - last_rx
        tx_speed = curr_tx - last_tx
        
        # Avoid negative spikes on reset
        if rx_speed < 0: rx_speed = 0
        if tx_speed < 0: tx_speed = 0

        last_rx, last_tx = curr_rx, curr_tx
        
        # Interface Info
        stdscr.addstr(2, 2, "INTERFACE: en0 (M2 Ultra)", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 2, "MTU STATUS: 9000 (JUMBO FRAMES)", curses.color_pair(2))
        
        # Bandwidth Stats
        stdscr.addstr(5, 4, f"🔻 DOWNLOAD SPEED: {format_bytes(rx_speed)}/s", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(6, 4, f"🔺 UPLOAD SPEED:   {format_bytes(tx_speed)}/s", curses.color_pair(3) | curses.A_BOLD)
        
        stdscr.addstr(8, 4, f"TOTAL RX: {format_bytes(curr_rx)}")
        stdscr.addstr(9, 4, f"TOTAL TX: {format_bytes(curr_tx)}")
        
        # Visual Bar
        bar_len = width - 20
        rx_percent = min(1.0, rx_speed / (100 * 1024 * 1024)) # Max scale 100MB/s
        fill = int(bar_len * rx_percent)
        bar_str = "█" * fill + "░" * (bar_len - fill)
        stdscr.addstr(11, 4, f"LOAD: [{bar_str}]", curses.color_pair(1))
        
        # Footer
        stdscr.addstr(height-1, 2, "Press 'q' to exit", curses.color_pair(4))
        
        stdscr.refresh()
        
        # Input Check
        c = stdscr.getch()
        if c == ord('q'):
            break
            
        # time.sleep(1) # handled by timeout

def main():
    try:
        curses.wrapper(draw_dashboard)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

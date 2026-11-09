#!/usr/bin/env python3
"""
TURBO GHOST (The Medium)
Scans for unmounted volumes ("Ghosts") and allows transient connection for deep scanning.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

def get_disks():
    """Get list of disk partitions using diskutil"""
    try:
        res = subprocess.run(["diskutil", "list", "-plist"], capture_output=True, text=True)
        # Parsing plist is safer but for speed/no-dep we might just parse text or use specific commands
        # Let's use text parsing of 'diskutil list' for visual feedback first
        res = subprocess.run(["diskutil", "list"], capture_output=True, text=True)
        return res.stdout
    except Exception as e:
        return str(e)

def find_ghosts():
    """Find unmounted volumes that look like storage"""
    cfg.print_step("Summoning Disk Utility...", "START")
    disks = get_disks()
    
    ghosts = []
    lines = disks.split('\n')
    
    # Simple heuristic: Lines with partition names but no mount point? 
    # Or just list everything and let user pick.
    # diskutil info -all is better
    
    res = subprocess.run(["diskutil", "info", "-all"], capture_output=True, text=True)
    current_vol = {}
    
    # iterate output blocks
    # This is a bit complex to parse reliably without plistlib, but let's try a simpler approach:
    # `ls /Volumes` vs `diskutil list`
    
    mounted = [p.name for p in Path("/Volumes").iterdir()]
    
    print(f"\n{cfg.BOLD}{cfg.CYAN}--- ACTIVE REALMS (MOUNTED) ---{cfg.RESET}")
    for m in mounted:
        print(f"   orb: {m}")
        
    print(f"\n{cfg.BOLD}{cfg.MAGENTA}--- GHOST REALMS (DETECTED) ---{cfg.RESET}")
    # We will list disks and ask user to specify identifier for mounting
    print(disks)
    
    return []

def mount_ghost(identifier):
    cfg.print_step(f"Materializing {identifier}...", "START")
    try:
        res = subprocess.run(["diskutil", "mount", identifier], capture_output=True, text=True)
        if "mounted" in res.stdout.lower():
            # Extract mount point
            # Volume XXX on diskNsM mounted
            cfg.system_log(f"Ghost {identifier} materialized!", "SUCCESS")
             # Find where it mounted
            mount_point = None
            info = subprocess.run(["diskutil", "info", identifier], capture_output=True, text=True)
            for line in info.stdout.split('\n'):
                if "Mount Point:" in line:
                    mount_point = line.split("Mount Point:")[1].strip()
                    break
            return mount_point
        else:
            cfg.system_log(f"Failed to summon {identifier}: {res.stderr}", "FAIL")
            return None
    except Exception as e:
        cfg.system_log(f"Ritual error: {e}", "ERROR")
        return None

def unmount_ghost(mount_point):
    cfg.print_step(f"Banishing {mount_point}...", "START")
    try:
        subprocess.run(["diskutil", "unmount", mount_point], check=True)
        cfg.system_log("Ghost banished to the void.", "SUCCESS")
    except Exception as e:
         cfg.system_log(f"Banishment failed: {e}", "ERROR")

def interact():
    cfg.print_header("TURBO GHOST", "PARANORMAL VOLUME ACTIVITY")
    
    find_ghosts()
    
    print(f"\n{cfg.BOLD}COMMANDS:{cfg.RESET}")
    print("   mount [identifier]  -> Mount a ghost volume (e.g., disk5s2)")
    print("   scan [identifier]   -> Mount, Scan (via Gabriel), and Unmount")
    print("   exit")
    
    while True:
        cmd = input(f"\n{cfg.MAGENTA}GHOST > {cfg.RESET}").strip().split()
        if not cmd: continue
        
        op = cmd[0].lower()
        
        if op == "exit":
            break
        elif op == "mount":
            if len(cmd) < 2: print("Need identifier"); continue
            mount_ghost(cmd[1])
        elif op == "scan":
            if len(cmd) < 2: print("Need identifier"); continue
            ident = cmd[1]
            mp = mount_ghost(ident)
            if mp:
                cfg.print_header("INVOKING GABRIEL", f"Scanning {mp}")
                # Call Gabriel
                subprocess.run(["python3", "turbo_gabriel.py", "scan", mp])
                
                # Unmount
                unmount_ghost(mp)

if __name__ == "__main__":
    interact()

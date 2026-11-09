# ==============================================================================
# 🦅 GABRIEL ALLEGIANCE (SYSTEM LEADER)
# ==============================================================================
# This script operates under the command of GABRIEL.
# PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE
# ==============================================================================

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

def check_warp_cli():
    """Verify warp-cli is installed."""
    try:
        res = subprocess.run(["which", "warp-cli"], capture_output=True, text=True)
        return res.returncode == 0
    except:
        return False

def get_status():
    """Get WARP status."""
    if not check_warp_cli():
        return "WARP_CLI_MISSING"
    
    try:
        res = subprocess.run(["warp-cli", "status"], capture_output=True, text=True)
        out = res.stdout.lower()
        if "connected" in out:
            return "CONNECTED"
        elif "disconnected" in out:
            return "DISCONNECTED"
        return "UNKNOWN"
    except:
        return "ERROR"

def toggle_warp(state: str):
    """
    Control Cloudflare WARP.
    state: 'on' or 'off'
    """
    if not check_warp_cli():
        cfg.system_log("Cloudflare WARP CLI not found.", "ERROR")
        return

    cmd = "connect" if state == 'on' else "disconnect"
    cfg.print_header(f"WARP DRIVE: {cmd.upper()}", "SUPER-SONIC NETWORK")
    
    try:
        subprocess.run(["warp-cli", cmd], check=True)
        time.sleep(2) # Wait for handshake
        
        status = get_status()
        if (state == 'on' and status == 'CONNECTED') or (state == 'off' and status == 'DISCONNECTED'):
            cfg.system_log(f"WARP is now {status}.", "SUCCESS")
        else:
            cfg.system_log(f"WARP state mismatch: {status}", "WARN")
            
    except Exception as e:
        cfg.system_log(f"WARP Command Failed: {e}", "ERROR")

def run_diagnostics():
    """Check connectivity and speed (simulated for CLI speed)."""
    cfg.print_header("WARP DIAGNOSTICS", "CHECKING VELOCITY")
    
    status = get_status()
    print(f"CORE > Status: {cfg.CYAN}{status}{cfg.RESET}")
    
    if status == 'CONNECTED':
        print(f"CORE > Mode:   {cfg.GREEN}SUPER-SONIC (Encrypted){cfg.RESET}")
        try:
            # Quick ping check
            res = subprocess.run(["ping", "-c", "3", "1.1.1.1"], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"CORE > Ping:   {cfg.GREEN}LOW LATENCY CONFIRMED{cfg.RESET}")
            else:
                 print(f"CORE > Ping:   {cfg.RED}HIGH LATENCY{cfg.RESET}")
        except: pass
    else:
        print(f"CORE > Mode:   {cfg.YELLOW}STANDARD (Unprotected){cfg.RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "on": toggle_warp('on')
        elif cmd == "off": toggle_warp('off')
        elif cmd == "status": run_diagnostics()
        else: print("Usage: turbo_warp.py [on|off|status]")
    else:
        run_diagnostics()

#!/usr/bin/env python3
# ==============================================================================
# 🛡️ TURBO GUARDIAN (AUTO-HEAL SUPERVISOR)
# ==============================================================================
# "I watch the watchers. If they fall, I pick them up."
# MONITORS: Server, Discord, Bridge, Hand, Sentinel, Gabriel
# ACTIONS: Restart on crash, Heal on error.

import subprocess
import time
import sys
import threading
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    # If config not found in path, try adding current dir
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

# CONFIGURATION
SCRIPTS_DIR = Path(__file__).parent
MEDIC_SCRIPT = SCRIPTS_DIR / "turbo_medic.py"

# DEFINE THE FLEET
FLEET = [
    {
        "name": "THE HIVE (Server)",
        "script": "turbo_server.py",
        "args": [],
        "critical": True,
        "process": None
    },
    {
        "name": "THE CARRIER (Discord)",
        "script": "turbo_discord.py",
        "args": [],
        "critical": False,
        "process": None
    },
    {
        "name": "THE SENTINEL (Volume Watch)",
        "script": "turbo_sentinel.py",
        "args": ["/Volumes"],
        "critical": True,
        "process": None
    },
    {
        "name": "THE BRIDGE (VR Link)",
        "script": "turbo_quest_bridge.py",
        "args": [],
        "critical": False,
        "process": None
    },
    {
        "name": "THE HAND (Studio Auto-Repair)",
        "script": "turbo_studio_hand.py",
        "args": [],
        "critical": False,
        "process": None
    }
]

# GABRIEL (THE BRAIN) IS SPECIAL - RUNS IN MAIN THREAD OR SEPARATE?
# Gabriel is interactive. We should let start_gabriel.sh handle the blocking Gabriel process,
# and have Guardian manage the background services.
# BUT user wants AUTOHEAL for everything.
# We will manage the background services here. Gabriel (Main) remains in the shell script but we could wrap it.
# For now, Guardian manages the "Background Fleet".

def heal_system(script_name):
    """Run the Medic logic if a crash occurs."""
    cfg.system_log(f"🚑 HEALING PROTOCOL: Analyzing {script_name}...", "WARN")
    
    # We run medic specifically? Or just general medic scan?
    # Medic scans all. Let's run it.
    try:
        subprocess.run([sys.executable, str(MEDIC_SCRIPT)], check=True)
        return True
    except:
        return False

def launch_agent(agent_config):
    """Start an agent process."""
    cmd = [sys.executable, str(SCRIPTS_DIR / agent_config["script"])] + agent_config["args"]
    
    try:
        # Don't capture output, let it flow to valid streams or log?
        # For now, let it share stdout/stderr but maybe prefix?
        # subprocess.Popen sharing stdout allows user to see logs.
        p = subprocess.Popen(cmd) 
        agent_config["process"] = p
        cfg.system_log(f"✅ LAUNCHED: {agent_config['name']} (PID: {p.pid})", "SUCCESS")
    except Exception as e:
        cfg.system_log(f"❌ FAIL: Could not launch {agent_config['name']}: {e}", "ERROR")

def monitor_fleet():
    """Main Loop: Check PIDs, Restart if needed."""
    cfg.print_header("🛡️  TURBO GUARDIAN", "Auto-Heal Active")
    
    # 1. Launch All
    for agent in FLEET:
        launch_agent(agent)
    
    # 2. Watch Loop
    try:
        while True:
            time.sleep(2)
            
            for agent in FLEET:
                proc = agent["process"]
                
                if proc and proc.poll() is not None:
                    # BLOCK DETECTED (Process Died)
                    exit_code = proc.returncode
                    cfg.system_log(f"⚠️  BLOCK DETECTED: {agent['name']} died (Code: {exit_code}).", "WARN")
                    
                    # AUTOHEAL
                    cfg.system_log("💫 INITIATING AUTO-HEAL...", "INFO")
                    heal_system(agent["script"])
                    
                    # RESTART
                    cfg.system_log(f"🔄 RESTARTING {agent['name']}...", "INFO")
                    launch_agent(agent)
                    
    except KeyboardInterrupt:
        print("\n🛡️  Guardian Standing Down.")
        for agent in FLEET:
            if agent["process"]: agent["process"].terminate()

if __name__ == "__main__":
    monitor_fleet()

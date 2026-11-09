#!/usr/bin/env python3
"""
🧠 GABRIEL UNIFIED LAUNCHER
The One Command to Rule Them All.

Starts all Gabriel subsystems:
- Server (HTTP API)
- Voice Listener (Speech Recognition)
- MemCell (Brain)
- Sentinel (File Watcher)

Usage:
    python3 gabriel_unified.py          # Start everything
    python3 gabriel_unified.py --voice  # With voice activation
    python3 gabriel_unified.py stop     # Stop everything
"""

import os
import sys
import subprocess
import time
import signal
import json
from pathlib import Path

# ==============================================================================
# PATHS
# ==============================================================================
SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
DASHBOARD_DIR = ROOT_DIR / "Dashboard"
LOG_DIR = SCRIPTS_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Process tracking
PIDS_FILE = SCRIPTS_DIR / ".gabriel_pids.json"

# ==============================================================================
# SUBSYSTEMS
# ==============================================================================
SUBSYSTEMS = {
    "server": {
        "name": "🌐 Gabriel Server",
        "script": "turbo_server.py",
        "port": 8080,
        "required": True
    },
    "sentinel": {
        "name": "👁️ Sentinel",
        "script": "turbo_sentinel.py",
        "required": False
    },
    "ghost": {
        "name": "👻 Ghost Scanner",
        "script": "turbo_ghost.py",
        "required": False
    }
}

# ==============================================================================
# PROCESS MANAGEMENT
# ==============================================================================
def save_pids(pids: dict):
    with open(PIDS_FILE, 'w') as f:
        json.dump(pids, f)

def load_pids() -> dict:
    if PIDS_FILE.exists():
        try:
            with open(PIDS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def kill_process(pid: int, name: str):
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.5)
        if is_running(pid):
            os.kill(pid, signal.SIGKILL)
        print(f"   ✅ Stopped {name} (PID {pid})")
    except:
        pass

# ==============================================================================
# START GABRIEL
# ==============================================================================
def start_gabriel(voice_mode=False):
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗                            ║
║  ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║                            ║
║  ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║                            ║
║  ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║                            ║
║  ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗                       ║
║   ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝                       ║
║                                                                              ║
║                    🧠 UNIFIED SYSTEM LAUNCHER                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    pids = {}
    
    # 1. Kill any existing Gabriel processes
    print("🔄 Checking for existing processes...")
    old_pids = load_pids()
    for name, pid in old_pids.items():
        if is_running(pid):
            kill_process(pid, name)
    
    # 2. Start each subsystem
    for key, config in SUBSYSTEMS.items():
        script_path = SCRIPTS_DIR / config["script"]
        
        if not script_path.exists():
            if config["required"]:
                print(f"   ❌ MISSING: {config['script']}")
            continue
        
        print(f"   🚀 Starting {config['name']}...")
        
        log_file = LOG_DIR / f"{key}.log"
        
        with open(log_file, 'w') as log:
            proc = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=log,
                stderr=subprocess.STDOUT,
                cwd=str(SCRIPTS_DIR)
            )
            pids[key] = proc.pid
            print(f"      PID: {proc.pid} | Log: {log_file.name}")
    
    # 3. Save PIDs
    save_pids(pids)
    
    # 4. Wait for server to be ready
    print("\n⏳ Waiting for server to initialize...")
    server_ready = False
    for _ in range(30):
        try:
            import urllib.request
            with urllib.request.urlopen("http://localhost:8080/api/status", timeout=1) as r:
                if r.status == 200:
                    server_ready = True
                    break
        except:
            pass
        time.sleep(0.5)
    
    if server_ready:
        print("✅ Server is ONLINE!")
    else:
        print("⚠️  Server may still be starting...")
    
    # 5. Voice Mode
    if voice_mode:
        print("\n🎤 Starting Voice Listener...")
        try:
            voice_script = SCRIPTS_DIR / "turbo_ears.py"
            if voice_script.exists():
                proc = subprocess.Popen(
                    [sys.executable, str(voice_script)],
                    cwd=str(SCRIPTS_DIR)
                )
                pids["voice"] = proc.pid
                save_pids(pids)
                print(f"   🎤 Voice Active (PID {proc.pid})")
            else:
                print("   ⚠️  Voice script not found, skipping...")
        except Exception as e:
            print(f"   ❌ Voice Error: {e}")
    
    # 6. Summary
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🟢 GABRIEL IS ONLINE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Portal:    http://localhost:8080                                            ║
║  Chat:      http://localhost:8080/chat.html                                  ║
║  API:       http://localhost:8080/api/status                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Commands:                                                                   ║
║    python3 gabriel_unified.py stop     # Stop all                            ║
║    python3 turbo_gabriel.py status     # Check subsystems                    ║
║    python3 turbo_gabriel.py chat       # Neural chat                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

# ==============================================================================
# STOP GABRIEL
# ==============================================================================
def stop_gabriel():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🛑 STOPPING GABRIEL SYSTEM                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    pids = load_pids()
    
    if not pids:
        print("   No running Gabriel processes found.")
        # Try to kill by name anyway
        subprocess.run(["pkill", "-f", "turbo_server.py"], capture_output=True)
        subprocess.run(["pkill", "-f", "turbo_sentinel.py"], capture_output=True)
        subprocess.run(["pkill", "-f", "turbo_ears.py"], capture_output=True)
        print("   Cleaned up any orphan processes.")
    else:
        for name, pid in pids.items():
            if is_running(pid):
                kill_process(pid, name)
            else:
                print(f"   ⚪ {name} already stopped")
    
    # Clear PID file
    if PIDS_FILE.exists():
        PIDS_FILE.unlink()
    
    print("\n✅ Gabriel system stopped.")

# ==============================================================================
# STATUS CHECK
# ==============================================================================
def check_status():
    print("\n🔍 GABRIEL SYSTEM STATUS\n")
    
    pids = load_pids()
    
    for key, config in SUBSYSTEMS.items():
        pid = pids.get(key)
        if pid and is_running(pid):
            print(f"   🟢 {config['name']}: Running (PID {pid})")
        else:
            print(f"   🔴 {config['name']}: Stopped")
    
    # Check server
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:8080/api/status", timeout=2) as r:
            data = json.loads(r.read().decode())
            print(f"\n   🌐 Server Mode: {data.get('mode', 'UNKNOWN')}")
    except:
        print("\n   ⚠️  Server not responding")

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "stop":
            stop_gabriel()
        elif cmd == "status":
            check_status()
        elif cmd == "--voice":
            start_gabriel(voice_mode=True)
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python3 gabriel_unified.py [stop|status|--voice]")
    else:
        start_gabriel()

if __name__ == "__main__":
    main()

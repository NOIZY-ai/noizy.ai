#!/usr/bin/env python3
"""
GABRIEL AUTO-HEALING WATCHDOG
==============================
Monitors system health and auto-restarts failed services.
- Monitors ULTRAFAST server (port 5174)
- Monitors Network Bridge (port 5175)
- Auto-restarts on failure
- Logs all events
"""

import time
import json
import subprocess
import os
import sys
from datetime import datetime
import requests

# Configuration
SERVER_URL = "http://localhost:5174"
BRIDGE_URL = "http://localhost:5175"
CHECK_INTERVAL = 5  # seconds
MAX_FAILURES = 3
LOG_FILE = os.path.join(os.path.dirname(__file__), "watchdog.log")
GABRIEL_DIR = os.path.dirname(os.path.abspath(__file__))

# State
server_failures = 0
bridge_failures = 0
restart_count = 0

def log(message, level="INFO"):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    except:
        pass

def check_server():
    """Check if ULTRAFAST server is healthy"""
    try:
        resp = requests.get(f"{SERVER_URL}/api/health", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("healthy"):
                return True, None
        return False, f"Status {resp.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def check_bridge():
    """Check if Network Bridge is healthy"""
    try:
        resp = requests.get(f"{BRIDGE_URL}/api/bridge/status", timeout=5)
        if resp.status_code == 200:
            return True, None
        return False, f"Status {resp.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def get_metrics():
    """Get current system metrics"""
    try:
        resp = requests.get(f"{SERVER_URL}/api/metrics", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def restart_server():
    """Restart the ULTRAFAST server"""
    global restart_count
    log("RESTARTING ULTRAFAST SERVER...", "WARN")
    
    try:
        # Kill existing
        subprocess.run(["pkill", "-f", "mc96_server"], capture_output=True)
        time.sleep(2)
        
        # Start new
        python_path = os.path.join(GABRIEL_DIR, "venv", "bin", "python3")
        server_path = os.path.join(GABRIEL_DIR, "mc96_server_ULTRAFAST.py")
        log_path = os.path.join(GABRIEL_DIR, "server.log")
        
        with open(log_path, "a") as log_file:
            subprocess.Popen(
                [python_path, server_path],
                stdout=log_file,
                stderr=log_file,
                cwd=GABRIEL_DIR
            )
        
        restart_count += 1
        log(f"Server restart initiated (total restarts: {restart_count})", "INFO")
        time.sleep(5)  # Wait for startup
        return True
    except Exception as e:
        log(f"Failed to restart server: {e}", "ERROR")
        return False

def restart_bridge():
    """Restart the Network Bridge"""
    log("RESTARTING NETWORK BRIDGE...", "WARN")
    
    try:
        # Kill existing
        subprocess.run(["pkill", "-f", "network_bridge"], capture_output=True)
        time.sleep(2)
        
        # Start new
        python_path = os.path.join(GABRIEL_DIR, "venv", "bin", "python3")
        bridge_path = os.path.join(GABRIEL_DIR, "network_bridge.py")
        log_path = os.path.join(GABRIEL_DIR, "bridge.log")
        
        with open(log_path, "a") as log_file:
            subprocess.Popen(
                [python_path, bridge_path],
                stdout=log_file,
                stderr=log_file,
                cwd=GABRIEL_DIR
            )
        
        log("Bridge restart initiated", "INFO")
        time.sleep(3)
        return True
    except Exception as e:
        log(f"Failed to restart bridge: {e}", "ERROR")
        return False

def monitor_loop():
    """Main monitoring loop"""
    global server_failures, bridge_failures
    
    log("=" * 60)
    log("GABRIEL AUTO-HEALING WATCHDOG STARTED")
    log(f"Server: {SERVER_URL}")
    log(f"Bridge: {BRIDGE_URL}")
    log(f"Check interval: {CHECK_INTERVAL}s")
    log(f"Max failures before restart: {MAX_FAILURES}")
    log("=" * 60)
    
    while True:
        try:
            # Check server
            server_ok, server_error = check_server()
            if server_ok:
                if server_failures > 0:
                    log("Server recovered!", "INFO")
                server_failures = 0
            else:
                server_failures += 1
                log(f"Server check failed ({server_failures}/{MAX_FAILURES}): {server_error}", "WARN")
                
                if server_failures >= MAX_FAILURES:
                    restart_server()
                    server_failures = 0
            
            # Check bridge
            bridge_ok, bridge_error = check_bridge()
            if bridge_ok:
                if bridge_failures > 0:
                    log("Bridge recovered!", "INFO")
                bridge_failures = 0
            else:
                bridge_failures += 1
                log(f"Bridge check failed ({bridge_failures}/{MAX_FAILURES}): {bridge_error}", "WARN")
                
                if bridge_failures >= MAX_FAILURES:
                    restart_bridge()
                    bridge_failures = 0
            
            # Log status every 60 seconds
            if int(time.time()) % 60 < CHECK_INTERVAL:
                metrics = get_metrics()
                if metrics:
                    sys_metrics = metrics.get("system", {})
                    log(f"STATUS: CPU={sys_metrics.get('cpu_percent', 0):.1f}% "
                        f"RAM={sys_metrics.get('ram_percent', 0):.1f}% "
                        f"WS_Clients={metrics.get('server', {}).get('connected_ws_clients', 0)}")
        
        except Exception as e:
            log(f"Monitor error: {e}", "ERROR")
        
        time.sleep(CHECK_INTERVAL)

def get_status():
    """Get current status as JSON"""
    server_ok, server_error = check_server()
    bridge_ok, bridge_error = check_bridge()
    metrics = get_metrics()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "server": {
            "healthy": server_ok,
            "error": server_error,
            "failures": server_failures,
            "url": SERVER_URL
        },
        "bridge": {
            "healthy": bridge_ok,
            "error": bridge_error,
            "failures": bridge_failures,
            "url": BRIDGE_URL
        },
        "restarts": restart_count,
        "metrics": metrics
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print(json.dumps(get_status(), indent=2))
        elif sys.argv[1] == "check":
            status = get_status()
            if status["server"]["healthy"] and status["bridge"]["healthy"]:
                print("ALL SYSTEMS OPERATIONAL")
                sys.exit(0)
            else:
                print("SYSTEMS DEGRADED")
                if not status["server"]["healthy"]:
                    print(f"  Server: {status['server']['error']}")
                if not status["bridge"]["healthy"]:
                    print(f"  Bridge: {status['bridge']['error']}")
                sys.exit(1)
        else:
            print("Usage: watchdog.py [status|check]")
            print("  (no args) - Start continuous monitoring")
            print("  status    - Get current status as JSON")
            print("  check     - Quick health check")
    else:
        monitor_loop()

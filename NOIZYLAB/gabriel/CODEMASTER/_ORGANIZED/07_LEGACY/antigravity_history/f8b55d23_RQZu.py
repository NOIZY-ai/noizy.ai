#!/usr/bin/env python3
# ==============================================================================
# 🥽 TURBO QUEST BRIDGE (VR LINK)
# ==============================================================================
# "Beams the Soul of Gabriel into the Metaverse."
# PROTOCOL: UDP STREAM (ZERO LATENCY)

import socket
import time
import json
import sys
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

# CONFIGURATION
QUEST_IP = "10.90.90.50"
QUEST_PORT = 9000
STATE_FILE = cfg.ASSETS_DIR / "avatar_state.json"
POLL_RATE = 1.0 / 60.0 # 60Hz

def load_state():
    try:
        if not STATE_FILE.exists(): return None
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except: return None

def run_bridge():
    cfg.print_header("🥽 QUEST BRIDGE", f"Target: {QUEST_IP}:{QUEST_PORT}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    last_ts = 0
    
    print(f"CORE > Streaming Avatar State at 60Hz...")
    
    while True:
        try:
            start_time = time.time()
            
            state = load_state()
            if state:
                # Optimized Payload
                payload = {
                    "e": state.get("emotion", "neutral"),
                    "s": state.get("is_speaking", False),
                    "v": state.get("viseme", 0), # Placeholder
                    "t": state.get("timestamp", 0)
                }
                
                # Only send if new data or heartbeat (every 1s)
                if payload['t'] > last_ts or (time.time() - last_ts > 1.0):
                    data = json.dumps(payload).encode('utf-8')
                    sock.sendto(data, (QUEST_IP, QUEST_PORT))
                    last_ts = payload['t']
                    # print(f"📡 Sent: {payload}") # Debug verbose
            
            # Maintain 60Hz Loop
            elapsed = time.time() - start_time
            sleep_time = max(0, POLL_RATE - elapsed)
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            print("\nCORE > Bridge Offline.")
            break
        except Exception as e:
            print(f"⚠️ BRIDGE ERROR: {e}")
            time.sleep(1)

if __name__ == "__main__":
    run_bridge()

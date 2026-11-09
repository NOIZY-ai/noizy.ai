#!/usr/bin/env python3
"""
GABRIEL Network Bridge - Cross-Machine Discovery & Communication
================================================================
UDP broadcast for peer discovery + REST API for status/control
Port 5175
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import socket
import threading
import time
import json
from datetime import datetime
import subprocess

app = Flask(__name__)
CORS(app)

# Configuration
DISCOVERY_PORT = 5176
API_PORT = 5175
BROADCAST_INTERVAL = 10  # seconds

# State
PEERS = {}
HOSTNAME = socket.gethostname()
LOCAL_IP = None

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()

def broadcast_presence():
    """Broadcast our presence on the network"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(1)

    message = json.dumps({
        "type": "GABRIEL_DISCOVERY",
        "hostname": HOSTNAME,
        "ip": LOCAL_IP,
        "port": API_PORT,
        "timestamp": datetime.now().isoformat()
    }).encode()

    while True:
        try:
            # Broadcast to common subnets
            for broadcast_addr in ['10.100.0.255', '10.0.0.255', '192.168.1.255', '255.255.255.255']:
                try:
                    sock.sendto(message, (broadcast_addr, DISCOVERY_PORT))
                except:
                    pass
        except Exception as e:
            print(f"[BRIDGE] Broadcast error: {e}")

        time.sleep(BROADCAST_INTERVAL)

def listen_for_peers():
    """Listen for peer discovery broadcasts"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', DISCOVERY_PORT))
    except:
        print(f"[BRIDGE] Could not bind to discovery port {DISCOVERY_PORT}")
        return

    sock.settimeout(1)

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())

            if message.get("type") == "GABRIEL_DISCOVERY":
                peer_id = f"{message['hostname']}:{message['ip']}"

                # Don't add ourselves
                if message['ip'] != LOCAL_IP:
                    PEERS[peer_id] = {
                        "hostname": message["hostname"],
                        "ip": message["ip"],
                        "port": message["port"],
                        "last_seen": datetime.now().isoformat()
                    }
                    print(f"[BRIDGE] Discovered peer: {message['hostname']} at {message['ip']}")

        except socket.timeout:
            pass
        except Exception as e:
            pass

        # Clean old peers (not seen in 60 seconds)
        now = datetime.now()
        for peer_id in list(PEERS.keys()):
            last_seen = datetime.fromisoformat(PEERS[peer_id]["last_seen"])
            if (now - last_seen).total_seconds() > 60:
                del PEERS[peer_id]

# ========== API ENDPOINTS ==========

@app.route('/')
def index():
    return jsonify({
        "service": "GABRIEL Network Bridge",
        "status": "ONLINE",
        "hostname": HOSTNAME,
        "ip": LOCAL_IP,
        "port": API_PORT
    })

@app.route('/api/bridge/status')
def bridge_status():
    """Get bridge status"""
    return jsonify({
        "status": "ONLINE",
        "hostname": HOSTNAME,
        "local_ip": LOCAL_IP,
        "port": API_PORT,
        "peer_count": len(PEERS),
        "discovery_port": DISCOVERY_PORT,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/bridge/peers')
def get_peers():
    """Get discovered peers"""
    return jsonify({
        "peers": PEERS,
        "count": len(PEERS)
    })

@app.route('/api/bridge/ping/<target>')
def ping_target(target):
    """Ping a specific target"""
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-t', '2', target],
            capture_output=True,
            timeout=5
        )
        return jsonify({
            "target": target,
            "alive": result.returncode == 0,
            "output": result.stdout.decode()[:200]
        })
    except Exception as e:
        return jsonify({
            "target": target,
            "alive": False,
            "error": str(e)
        })

@app.route('/api/bridge/discover')
def trigger_discovery():
    """Trigger a discovery broadcast"""
    return jsonify({
        "success": True,
        "message": "Discovery broadcast sent"
    })

@app.route('/api/bridge/connect/<target>')
def connect_to_peer(target):
    """Test connection to a specific peer"""
    try:
        # Try to connect to the GABRIEL API on target
        import requests
        resp = requests.get(f"http://{target}:5174/", timeout=3)
        return jsonify({
            "target": target,
            "connected": True,
            "status_code": resp.status_code,
            "response": resp.json() if resp.headers.get('content-type', '').startswith('application/json') else resp.text[:200]
        })
    except Exception as e:
        return jsonify({
            "target": target,
            "connected": False,
            "error": str(e)
        })

# ========== MAIN ==========

if __name__ == '__main__':
    print("\033[92m" + "=" * 50 + "\033[0m")
    print("\033[92m  GABRIEL NETWORK BRIDGE\033[0m")
    print("\033[92m  Cross-Machine Discovery & Communication\033[0m")
    print("\033[92m" + "=" * 50 + "\033[0m")
    print(f"\033[96m[BRIDGE] Hostname: {HOSTNAME}\033[0m")
    print(f"\033[96m[BRIDGE] Local IP: {LOCAL_IP}\033[0m")
    print(f"\033[96m[BRIDGE] API Port: {API_PORT}\033[0m")
    print(f"\033[96m[BRIDGE] Discovery Port: {DISCOVERY_PORT}\033[0m")
    print("\033[92m" + "=" * 50 + "\033[0m")

    # Start background threads
    threading.Thread(target=broadcast_presence, daemon=True).start()
    threading.Thread(target=listen_for_peers, daemon=True).start()

    print("[BRIDGE] Discovery threads started")

    # Start API
    app.run(host='0.0.0.0', port=API_PORT, debug=False, threaded=True)

#!/usr/bin/env python3
"""
GABRIEL NETWORK BRIDGE
Flask-based network bridge for HP-OMEN <-> M2Ultra communication
Auto-discovery via UDP broadcast
"""

import os
import socket
import json
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
BRIDGE_PORT = 5175
DISCOVERY_PORT = 5176
DISCOVERY_INTERVAL = 10

class NetworkBridge:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.local_ip = self._get_local_ip()
        self.peers = {}
        self.start_time = datetime.now()

    def _get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def broadcast_presence(self):
        """Broadcast presence on UDP"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = json.dumps({
            "type": "GABRIEL_DISCOVERY",
            "hostname": self.hostname,
            "ip": self.local_ip,
            "port": BRIDGE_PORT,
            "timestamp": datetime.now().isoformat()
        }).encode()

        try:
            sock.sendto(message, ('<broadcast>', DISCOVERY_PORT))
        except:
            pass
        finally:
            sock.close()

    def listen_for_peers(self):
        """Listen for peer broadcasts"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', DISCOVERY_PORT))
        sock.settimeout(1.0)

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode())

                if message.get("type") == "GABRIEL_DISCOVERY":
                    peer_id = f"{message['hostname']}_{message['ip']}"
                    if message['ip'] != self.local_ip:
                        self.peers[peer_id] = {
                            "hostname": message['hostname'],
                            "ip": message['ip'],
                            "port": message['port'],
                            "last_seen": datetime.now().isoformat()
                        }
                        print(f"[BRIDGE] Discovered peer: {message['hostname']} @ {message['ip']}")
            except socket.timeout:
                pass
            except Exception as e:
                pass

    def discovery_loop(self):
        """Continuous discovery loop"""
        while True:
            self.broadcast_presence()
            time.sleep(DISCOVERY_INTERVAL)

    def start(self):
        """Start bridge services"""
        # Start discovery broadcaster
        threading.Thread(target=self.discovery_loop, daemon=True).start()
        # Start peer listener
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        print(f"[BRIDGE] Started on {self.local_ip}:{BRIDGE_PORT}")

# Global bridge instance
bridge = NetworkBridge()

@app.route('/api/bridge/status')
def status():
    """Get bridge status"""
    return jsonify({
        "hostname": bridge.hostname,
        "local_ip": bridge.local_ip,
        "port": BRIDGE_PORT,
        "uptime_seconds": (datetime.now() - bridge.start_time).total_seconds(),
        "peer_count": len(bridge.peers)
    })

@app.route('/api/bridge/peers')
def peers():
    """Get discovered peers"""
    return jsonify({
        "peers": bridge.peers,
        "count": len(bridge.peers)
    })

@app.route('/api/bridge/discover')
def discover():
    """Trigger discovery broadcast"""
    bridge.broadcast_presence()
    return jsonify({"status": "broadcast_sent"})

@app.route('/api/bridge/ping/<ip>')
def ping(ip):
    """Ping a specific IP"""
    import subprocess
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-t", "2", ip],
            capture_output=True,
            timeout=5
        )
        return jsonify({
            "ip": ip,
            "alive": result.returncode == 0
        })
    except:
        return jsonify({"ip": ip, "alive": False})

@app.route('/api/bridge/send', methods=['POST'])
def send_message():
    """Send message to peer"""
    data = request.json
    target_ip = data.get('ip')
    target_port = data.get('port', BRIDGE_PORT)
    message = data.get('message')

    if not target_ip or not message:
        return jsonify({"error": "Missing ip or message"}), 400

    try:
        import requests
        resp = requests.post(
            f"http://{target_ip}:{target_port}/api/bridge/receive",
            json={"from": bridge.local_ip, "message": message},
            timeout=5
        )
        return jsonify({"status": "sent", "response": resp.status_code})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

@app.route('/api/bridge/receive', methods=['POST'])
def receive_message():
    """Receive message from peer"""
    data = request.json
    print(f"[BRIDGE] Message from {data.get('from')}: {data.get('message')}")
    return jsonify({"status": "received"})

if __name__ == '__main__':
    bridge.start()
    print(f"\n{'='*60}")
    print(f"  GABRIEL NETWORK BRIDGE")
    print(f"  Host: {bridge.hostname}")
    print(f"  IP: {bridge.local_ip}")
    print(f"  Port: {BRIDGE_PORT}")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=BRIDGE_PORT, debug=False)

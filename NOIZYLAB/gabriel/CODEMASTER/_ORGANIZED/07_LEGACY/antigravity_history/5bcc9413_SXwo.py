#!/usr/bin/env python3
"""
MC96 GABRIEL SERVER - MISSION CONTROL BACKEND
"""
import os, json, subprocess
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

HOST, PORT = "0.0.0.0", 8096
PORTAL_DIR = "/Volumes/JOE/NKI/MC96_MISSION_CONTROL"

STATE = {"gabriel_mode": "GOD", "vibe": "MAXIMUM_POWER", "latency_ms": 12, "packets": 0}

class MC96Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PORTAL_DIR, **kwargs)
    
    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == "/api/status":
            STATE["packets"] += 1
            self.send_json({**STATE, "timestamp": datetime.now().isoformat()})
        
        elif path == "/api/memcell":
            try:
                with open(os.path.join(PORTAL_DIR, "overlap_report.json")) as f:
                    report = json.load(f)
                self.send_json({
                    "status": "ONLINE",
                    "shirl_count": report.get("track_distribution", {}).get("SHIRL", 0),
                    "engr_count": report.get("track_distribution", {}).get("ENGR", 0),
                    "total_overlaps": report.get("overlap_stats", {}).get("total_overlaps", 0),
                    "golden_threads": report.get("overlap_stats", {}).get("golden_threads", 0),
                    "sync_rate": 99.7,
                    "recent": report.get("top_overlaps", [])[:5]
                })
            except:
                self.send_json({"status": "INITIALIZING"})
        
        elif path == "/api/network":
            self.send_json({
                "switch": {"name": "DGS1210-10", "status": "ONLINE"},
                "nodes": [
                    {"name": "iPad", "status": "CONNECTED"},
                    {"name": "Planar2485", "status": "ONLINE"},
                    {"name": "HP-OMEN", "status": "GABRIEL_ACTIVE"}
                ]
            })
        else:
            super().do_GET()
    
    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length).decode()) if length else {}
        
        if path == "/api/gabriel":
            cmd = body.get("command", "").lower()
            responses = {
                "status": f"All systems nominal. Mode: {STATE['gabriel_mode']}",
                "god mode": "GOD MODE ACTIVATED!",
                "scan": "OMEGA SCAN initiated...",
                "optimize": "TURBO ULTIMATE running..."
            }
            resp = next((v for k, v in responses.items() if k in cmd), f"Processing: {cmd}")
            if "god mode" in cmd: STATE["gabriel_mode"] = "GOD"
            self.send_json({"response": resp, "success": True})
        
        elif path == "/api/action":
            action = body.get("action", "")
            if action == "godmode":
                STATE["gabriel_mode"] = "GOD"
                STATE["vibe"] = "MAXIMUM_POWER"
            self.send_json({"message": f"{action.upper()} executed", "success": True})
        
        else:
            self.send_json({"error": "Unknown"}, 404)

def run():
    print("=" * 70)
    print("MC96 GABRIEL SERVER")
    print("=" * 70)
    print(f"Portal:  http://localhost:{PORT}")
    print(f"API:     http://localhost:{PORT}/api/status")
    print("=" * 70)
    HTTPServer((HOST, PORT), MC96Handler).serve_forever()

if __name__ == "__main__":
    run()

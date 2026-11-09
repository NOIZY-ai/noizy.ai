#!/usr/bin/env python3
import os, json
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

HOST, PORT = "0.0.0.0", 8096
PORTAL = "/Volumes/JOE/NKI/MC96_MISSION_CONTROL"
STATE = {"mode": "GOD", "vibe": "MAXIMUM_POWER", "latency": 12}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw): super().__init__(*a, directory=PORTAL, **kw)
    def log_message(self, f, *a): print(f"[{datetime.now():%H:%M:%S}] {a[0]}")
    def send_json(self, d, s=200):
        self.send_response(s)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())
    def do_OPTIONS(self):
        self.send_response(200)
        for h in [("Access-Control-Allow-Origin", "*"), ("Access-Control-Allow-Methods", "GET,POST,OPTIONS"), ("Access-Control-Allow-Headers", "Content-Type")]: self.send_header(*h)
        self.end_headers()
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/status": self.send_json({**STATE, "ts": datetime.now().isoformat()})
        elif p == "/api/memcell":
            try:
                with open(f"{PORTAL}/overlap_report.json") as f: r = json.load(f)
                self.send_json({"status": "ONLINE", "shirl": r.get("types",{}).get("SHIRL",0), "engr": r.get("types",{}).get("ENGR",0), "overlaps": r.get("overlaps",0), "golden": r.get("golden",0)})
            except: self.send_json({"status": "INIT"})
        elif p == "/api/network": self.send_json({"switch": "DGS1210-10", "nodes": ["iPad", "Planar2485", "HP-OMEN"]})
        else: super().do_GET()
    def do_POST(self):
        p = urlparse(self.path).path
        l = int(self.headers.get('Content-Length', 0))
        d = json.loads(self.rfile.read(l).decode()) if l else {}
        if p == "/api/gabriel": self.send_json({"response": f"Processed: {d.get('command','')}", "ok": True})
        else: self.send_json({"error": 1}, 404)

if __name__ == "__main__":
    print("="*60 + "\nMC96 GABRIEL SERVER\n" + "="*60)
    print(f"Portal: http://localhost:{PORT}\nAPI: http://localhost:{PORT}/api/status")
    print("="*60)
    HTTPServer((HOST, PORT), Handler).serve_forever()

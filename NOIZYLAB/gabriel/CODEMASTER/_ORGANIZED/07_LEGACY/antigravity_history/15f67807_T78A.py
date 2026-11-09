import http.server
import socketserver
import json
import sqlite3
import time
from pathlib import Path
from urllib.parse import urlparse

# CONFIG
# CONFIG
PORT = 8090
try:
    import func_timeout
except: pass

import sys
sys.path.append(str(Path(__file__).parent)) # Add Scripts dir to path
try:
    import turbo_config as cfg
    DB_PATH = Path(cfg.UNIVERSE_DB_PATH)
except:
    DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe_db.sqlite")

print(f"DEBUG: Using DB at {DB_PATH}")

class TurboHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default logs to keep stdout clean unless error
        return

    def do_GET(self):
        print(f"DEBUG: Handling Request for {self.path}")
        parsed = urlparse(self.path)
        
        # API: Realtime Data
        if parsed.path == '/api/live':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = self.get_system_status()
            self.wfile.write(json.dumps(data).encode())
            return

        # UI: Dashboard HTML
        if parsed.path == '/' or parsed.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                target_html = Path("/Users/m2ultra/.gemini/antigravity/brain/ed2f88a9-b13b-4002-b8ce-0901e78d8ba8/mission_control.html")
                with open(target_html, 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(f"Error loading dashboard: {e}".encode())
            return

        # CSS
        if parsed.path == '/mission_control.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            try:
                target_css = Path("/Users/m2ultra/.gemini/antigravity/brain/ed2f88a9-b13b-4002-b8ce-0901e78d8ba8/mission_control.css")
                with open(target_css, 'rb') as f:
                    self.wfile.write(f.read())
            except: pass
            return

        super().do_GET()

    def get_system_status(self):
        # ... (Same as before)
        try:
            if not DB_PATH.exists():
                return {"error": "DB Not Found", "status": "Error", "vibe": 0, "logs": [], "cells": []}
                
            conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # 1. Vibe Score
            cursor.execute("SELECT AVG(vibe_score) FROM memory_events ORDER BY id DESC LIMIT 10")
            res = cursor.fetchone()
            vibe = res[0] if res and res[0] else 50
            
            # 2. Recent Logs
            cursor.execute("SELECT timestamp, author, event_type, content, vibe_score FROM memory_events ORDER BY id DESC LIMIT 8")
            logs = []
            for row in cursor.fetchall():
                ts = row[0].split("T")[1][:8] if "T" in row[0] else row[0]
                logs.append({
                    "time": ts,
                    "author": row[1],
                    "type": row[2],
                    "msg": row[3],
                    "vibe": row[4]
                })
                
            # 3. Active Cells
            cursor.execute("SELECT topic, status FROM memcells WHERE status='ACTIVE' ORDER BY id DESC LIMIT 5")
            cells = [{"topic": r[0], "status": r[1]} for r in cursor.fetchall()]
            
            conn.close()
            
            return {
                "vibe": round(vibe, 1),
                "logs": logs,
                "cells": cells,
                "status": "ONLINE",
                "latency": "0ms" 
            }
        except Exception as e:
            return {"error": str(e), "status": "OFFLINE", "vibe": 0, "logs": [], "cells": []}

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    print(f"🚀 TURBO DASHBOARD LIVE: http://localhost:{PORT}")
    print(f"📡 API ENDPOINT: http://localhost:{PORT}/api/live")
    with ReusableTCPServer(("", PORT), TurboHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

import http.server
import socketserver
import json
import sqlite3
import time
from pathlib import Path
from urllib.parse import urlparse

# CONFIG
PORT = 8080
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe_db.sqlite")
HTML_PATH = Path(__file__).parent / "mission_control.html"
CSS_PATH = Path(__file__).parent / "mission_control.css"

class TurboHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
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
                # If artifact exists, serve it. If not, fallback.
                # We need to find where the mission_control.html actually lives.
                # Assuming it's in the same dir as script or Artifacts dir.
                # The prompt said "build the local demo dashboard", I'll serve the one I'm about to write/update.
                # For now, let's look in valid paths.
                target_html = Path("mission_control.html")
                if not target_html.exists():
                     # Fallback to absolute artifact path if running from elsewhere
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
                target_css = Path("mission_control.css")
                if not target_css.exists():
                     target_css = Path("/Users/m2ultra/.gemini/antigravity/brain/ed2f88a9-b13b-4002-b8ce-0901e78d8ba8/mission_control.css")
                with open(target_css, 'rb') as f:
                    self.wfile.write(f.read())
            except: pass
            return

        super().do_GET()

    def get_system_status(self):
        """Query MemCell for realtime state."""
        try:
            conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) # Read-Only mode
            cursor = conn.cursor()
            
            # 1. Vibe Score (Last 10 avg)
            cursor.execute("SELECT AVG(vibe_score) FROM memory_events ORDER BY id DESC LIMIT 10")
            vibe = cursor.fetchone()[0] or 50
            
            # 2. Recent Logs
            cursor.execute("SELECT timestamp, author, event_type, content, vibe_score FROM memory_events ORDER BY id DESC LIMIT 8")
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    "time": row[0].split("T")[1][:8],
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

if __name__ == "__main__":
    print(f"🚀 TURBO DASHBOARD LIVE: http://localhost:{PORT}")
    print(f"📡 API ENDPOINT: http://localhost:{PORT}/api/live")
    with socketserver.TCPServer(("", PORT), TurboHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

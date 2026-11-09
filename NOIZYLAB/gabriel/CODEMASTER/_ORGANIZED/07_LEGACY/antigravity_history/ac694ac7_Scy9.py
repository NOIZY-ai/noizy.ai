import http.server
import socketserver
import json
import sqlite3
import subprocess
import os
import urllib.parse
from pathlib import Path

# Config
PORT = 8080
DB_PATH = Path("Audio_Unitor/Database/universe.db")
SCRIPTS_DIR = Path("Audio_Unitor/Scripts")
HTML_FILE = "nexus.html"
MAP_FILE = "system_map.html"

class NexusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # API: Stats
        if path == "/api/stats":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            stats = {"files": 0, "size": 0, "waste": 0}
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("SELECT count(*), sum(size) FROM files")
                row = c.fetchone()
                stats["files"] = row[0] or 0
                stats["size"] = row[1] or 0
                
                # Waste calc
                c.execute("SELECT sum(size * (count - 1)) FROM (SELECT size, count(*) as count FROM files GROUP BY hash HAVING count > 1)")
                waste = c.fetchone()[0]
                stats["waste"] = waste or 0
                conn.close()
            except Exception as e:
                print(f"DB Error: {e}")
                
            self.wfile.write(json.dumps(stats).encode())
            return

        # API: Search
        elif path == "/api/search":
            term = query.get("q", [""])[0]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            results = []
            if term:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    # Neural Search (Filename OR Tags OR Key OR BPM)
                    sql = """
                        SELECT filename, path, size, bpm, key, tags 
                        FROM files 
                        WHERE filename LIKE ? OR tags LIKE ? OR key LIKE ? 
                        LIMIT 50
                    """
                    wild = f"%{term}%"
                    c.execute(sql, (wild, wild, wild))
                    rows = c.fetchall()
                    for r in rows:
                        results.append({
                            "name": r[0], "path": r[1], "size": r[2], 
                            "bpm": r[3], "key": r[4], "tags": r[5]
                        })
                    conn.close()
                except Exception as e:
                    print(f"Search Error: {e}")
            
            self.wfile.write(json.dumps(results).encode())
            return
            
            
        # API: Sentinel Logs
        elif path == "/api/sentinel":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            log_path = Path("sentinel.log")
            if log_path.exists():
                # Read last 10 lines
                try:
                    lines = log_path.read_text().splitlines()[-10:]
                    self.wfile.write("\n".join(lines).encode())
                except: self.wfile.write(b"Error reading logs.")
            else:
                self.wfile.write(b"Sentinel Log not found.")
            return

        # API: Action Trigger
        elif path == "/api/action":
            action = query.get("cmd", [""])[0]
            self.send_response(200)
            self.end_headers()
            
            if action == "ingest":
                # Run in background? or wait? For now, simplistic wait.
                # In real app, use threading.
                print("Running Ingest...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_ingest.py")])
                self.wfile.write(json.dumps({"status": "ingest_started"}).encode())
                return
            elif action == "dedup":
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_dedup.py")])
                self.wfile.write(json.dumps({"status": "dedup_started"}).encode())
                return
            elif action == "sentinel_start":
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "sentinel.py"), str(Path.expanduser(Path("~/Downloads")))])
                self.wfile.write(json.dumps({"status": "sentinel_started"}).encode())
                return
            
            self.wfile.write(json.dumps({"status": "unknown"}).encode())
            return

        # Serve UI
        if path == "/" or path == "/index.html":
            if os.path.exists(HTML_FILE):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(HTML_FILE, 'rb') as f:
                    self.wfile.write(f.read())
                return

        # Fallback to serving files (for CSS/JS/Map)
        return super().do_GET()

print(f"🌐 NEXUS ONLINE: http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), NexusHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Nexus Offline.")

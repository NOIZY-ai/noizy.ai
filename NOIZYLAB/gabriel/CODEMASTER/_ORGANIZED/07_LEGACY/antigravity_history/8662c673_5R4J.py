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
HTML_FILE = "turbo_server.html"
MAP_FILE = "turbo_map.html"

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
                
                stats["waste"] = waste or 0
                
                # --- MEMCELL CHRONOS DATA (INTELLIGENCE) ---
                try:
                    # 1. Temporal Heatmap (Activity by Hour)
                    # Initialize 24h array
                    heatmap = [0] * 24
                    c.execute("SELECT substr(timestamp, 12, 2) as hour, COUNT(*) FROM memory_events GROUP BY hour")
                    rows = c.fetchall()
                    for r in rows:
                        if r[0]:
                            h = int(r[0])
                            if 0 <= h < 24: heatmap[h] = r[1]
                    stats["heatmap"] = heatmap

                    # 2. Identity Matrix (Author Stats)
                    identities = {}
                    c.execute("SELECT author, COUNT(*) FROM memory_events GROUP BY author")
                    rows = c.fetchall()
                    for r in rows:
                        identities[r[0]] = r[1]
                    stats["identities"] = identities

                    # 3. Active Subjects (Tags)
                    c.execute("SELECT tags FROM memory_events ORDER BY timestamp DESC LIMIT 20")
                    rows = c.fetchall()
                    all_tags = []
                    for r in rows:
                        if r[0]: all_tags.extend([t.strip() for t in r[0].split(',')])
                    
                    from collections import Counter
                    common = Counter(all_tags).most_common(5)
                    stats["subjects"] = ", ".join([f"#{t[0]}" for t in common])

                except Exception as e:
                    print(f"CORE > MemCell Chronos Error: {e}")
                    stats["heatmap"] = []
                    stats["identities"] = {}
                    stats["subjects"] = "Offline"
            
                conn.close()
            except Exception as e:
                print(f"CORE > DB Error: {e}")
                
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
                    print(f"CORE > Search Error: {e}")
            
            self.wfile.write(json.dumps(results).encode())
            return
            
            
        # API: Sentinel Logs
        elif path == "/api/sentinel":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            log_path = Path("turbo_sentinel.log")
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
                print("CORE > 🚀 Running Ingest...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_ingest.py")])
                self.wfile.write(json.dumps({"status": "ingest_started"}).encode())
                return
            elif action == "dedup":
                print("CORE > 🧬 Running Dedup...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_dedup.py")])
                self.wfile.write(json.dumps({"status": "dedup_started"}).encode())
                return
            elif action == "sentinel_start":
                print("CORE > 🛡️  Starting Sentinel...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_sentinel.py"), str(Path.expanduser(Path("~/Downloads")))])
                self.wfile.write(json.dumps({"status": "sentinel_started"}).encode())
                return
            elif action == "convert":
                vault = Path.home() / "Universal"
                print("CORE > ⚗️  Starting Transmutation...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_converter.py"), str(vault)])
                self.wfile.write(json.dumps({"status": "transmutation_started"}).encode())
                return
            elif action == "black_hole":
                print("CORE > 🕳️  Opening Black Hole (Vacuum + Dedup Nuke)...")
                vault = Path.home() / "Universal"
                cmd = f"python3 {SCRIPTS_DIR}/turbo_vacuum.py {vault} && python3 {SCRIPTS_DIR}/turbo_dedup.py --nuke"
                subprocess.Popen(cmd, shell=True)
                self.wfile.write(json.dumps({"status": "black_hole_opened"}).encode())
                return
            elif action == "inject_metadata":
                vault = Path.home() / "Universal"
                print("CORE > 💉 Injecting Soul...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_librarian.py"), str(vault)])
                self.wfile.write(json.dumps({"status": "soul_injection_started"}).encode())
                return
            elif action == "omega_start":
                vault = Path.home() / "Universal"
                print("CORE > Ω OMEGA PROTOCOL INITIATED")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / "turbo_omega.py"), str(vault)])
                self.wfile.write(json.dumps({"status": "omega_protocol_initiated"}).encode())
                return
            elif action == "open_time_machine":
                tm_path = os.path.expanduser("~/Universal/Time_Machine")
                subprocess.Popen(["open", tm_path])
                self.wfile.write(json.dumps({"status": "success", "message": "Time Machine Opened"}).encode())
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

print(f"CORE > 🌐 NEXUS ONLINE: http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), NexusHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCORE > 🛑 Nexus Offline.")

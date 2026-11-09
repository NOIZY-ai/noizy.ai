#!/usr/bin/env python3
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

class GodModeHandler(http.server.SimpleHTTPRequestHandler):
    """
    ⚡ GOD MODE SERVER HANDLER
    Supports:
    - /api/stats (System Vitals)
    - /api/search (Neural Search)
    - /api/generate/audio (Audio Chains)
    - /api/generate/video (Video AI)
    - /api/memcell/golden_thread (Intelligence)
    """
    
    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # ---------------------------------------------------------
        # 1. API: GENERATION (THE FORGE)
        # ---------------------------------------------------------
        if path.startswith("/api/generate/audio"):
            # Usage: /api/generate/audio?type=scene&prompt=...
            gen_type = query.get("type", ["sfx"])[0]
            prompt = query.get("prompt", [""])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if not prompt:
                self.wfile.write(json.dumps({"status": "error", "message": "Prompt required"}).encode())
                return

            print(f"CORE > 🎹 FORGE REQUEST: {gen_type.upper()} '{prompt}'")
            
            if gen_type == "scene":
                cmd = ["python3", str(SCRIPTS_DIR / "turbo_audio_gen.py"), "scene", prompt]
            elif gen_type == "sfx":
                cmd = ["python3", str(SCRIPTS_DIR / "turbo_audio_gen.py"), "sfx", prompt]
            else:
                cmd = ["python3", str(SCRIPTS_DIR / "turbo_audio_gen.py"), "sfx", prompt] # default
            
            # Fire and forget (Async)
            subprocess.Popen(cmd)
            self.wfile.write(json.dumps({"status": "started", "job": f"{gen_type}: {prompt}"}).encode())
            return
            
        elif path.startswith("/api/generate/video"):
            # Usage: /api/generate/video?model=runway&prompt=...
            model = query.get("model", ["runway"])[0]
            prompt = query.get("prompt", [""])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            print(f"CORE > 🎥 FORGE REQUEST: {model.upper()} '{prompt}'")
            
            cmd = ["python3", str(SCRIPTS_DIR / "turbo_video_ai.py"), model, prompt]
            subprocess.Popen(cmd)
            self.wfile.write(json.dumps({"status": "started", "job": f"{model}: {prompt}"}).encode())
            return

        # ---------------------------------------------------------
        # 2. API: SYSTEM VITALS (MISSION CONTROL)
        # ---------------------------------------------------------
        elif path == "/api/stats":
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
                
                # CHRONOS DATA (MemCell)
                try:
                    # Heatmap
                    heatmap = [0] * 24
                    c.execute("SELECT substr(timestamp, 12, 2) as hour, COUNT(*) FROM memory_events GROUP BY hour")
                    for r in c.fetchall():
                        if r[0]:
                            h = int(r[0])
                            if 0 <= h < 24: heatmap[h] = r[1]
                    stats["heatmap"] = heatmap
                    
                    # Identities
                    identities = {}
                    c.execute("SELECT author, COUNT(*) FROM memory_events GROUP BY author")
                    for r in c.fetchall(): identities[r[0]] = r[1]
                    stats["identities"] = identities
                    
                    # Subjects
                    c.execute("SELECT tags FROM memory_events ORDER BY timestamp DESC LIMIT 20")
                    all_tags = []
                    for r in c.fetchall():
                        if r[0]: all_tags.extend([t.strip() for t in r[0].split(',')])
                    from collections import Counter
                    stats["subjects"] = ", ".join([f"#{t[0]}" for t in Counter(all_tags).most_common(5)])
                    
                except: pass
                conn.close()
            except: pass
                
            self.wfile.write(json.dumps(stats).encode())
            return

        # ---------------------------------------------------------
        # 3. API: NEURAL SEARCH (THE DECK)
        # ---------------------------------------------------------
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
                    sql = "SELECT filename, path, size, bpm, key, tags FROM files WHERE filename LIKE ? OR tags LIKE ? LIMIT 50"
                    wild = f"%{term}%"
                    c.execute(sql, (wild, wild))
                    for r in c.fetchall():
                        results.append({"name": r[0], "path": r[1], "size": r[2], "bpm": r[3], "key": r[4], "tags": r[5]})
                    conn.close()
                except: pass
            self.wfile.write(json.dumps(results).encode())
            return
            
        # ---------------------------------------------------------
        # 4. API: ACTIONS (COMMAND CENTER)
        # ---------------------------------------------------------
        elif path == "/api/action":
            action = query.get("cmd", [""])[0]
            self.send_response(200)
            self.end_headers()
            
            script_map = {
                "ingest": "turbo_ingest.py",
                "dedup": "turbo_dedup.py",
                "sentinel_start": "turbo_sentinel.py",
                "convert": "turbo_converter.py",
                "run_vis": "turbo_vis.py",
                "omega_start": "turbo_omega.py"
            }
            
            if action in script_map:
                print(f"CORE > 🚀 Executing {script_map[action]}...")
                subprocess.Popen(["python3", str(SCRIPTS_DIR / script_map[action])])
                self.wfile.write(json.dumps({"status": "started"}).encode())
            else:
                 self.wfile.write(json.dumps({"status": "unknown"}).encode())
            return

        # ---------------------------------------------------------
        # 5. STATIC FILES HANDLING (ROBUST)
        # ---------------------------------------------------------
        # Serve from Dashboard/ if exists, else root
        # Prioritize "Noizy Portal" files
        
        # Check Dashboard Dir
        dash_path = SCRIPTS_DIR.parent / "Dashboard" / path.lstrip("/")
        
        # Special Case: Root -> portal_index.html (if exists) else mission_control
        if path == "/" or path == "/index.html":
             if (SCRIPTS_DIR.parent / "Dashboard" / "portal_index.html").exists():
                 self.serve_file(SCRIPTS_DIR.parent / "Dashboard" / "portal_index.html", 'text/html')
                 return
             elif (SCRIPTS_DIR.parent / "Dashboard" / "mission_control.html").exists():
                 self.serve_file(SCRIPTS_DIR.parent / "Dashboard" / "mission_control.html", 'text/html')
                 return

        # Serve requested file
        if dash_path.exists() and dash_path.is_file():
            # Determine mime
            mime = "text/plain"
            if path.endswith(".html"): mime = "text/html"
            elif path.endswith(".css"): mime = "text/css"
            elif path.endswith(".js"): mime = "application/javascript"
            elif path.endswith(".json"): mime = "application/json"
            
            self.serve_file(str(dash_path), mime)
            return

        # Fallback to SimpleHTTP default (Current Directory)
        return super().do_GET()

print(f"CORE > 🌐 GOD MODE SERVER ONLINE: http://localhost:{PORT}")
print(f"CORE > 🏠 Serving Portal from: {SCRIPTS_DIR.parent / 'Dashboard'}")
with socketserver.TCPServer(("", PORT), GodModeHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCORE > 🛑 Server Offline.")

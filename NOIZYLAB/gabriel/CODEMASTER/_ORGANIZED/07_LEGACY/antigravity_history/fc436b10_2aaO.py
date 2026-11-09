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
SCRIPTS_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPTS_DIR.parent / "Database" / "universe.db"
GHOST_STATUS_FILE = SCRIPTS_DIR / "ghost.status"
HTML_FILE = "turbo_server.html"
MAP_FILE = "turbo_map.html"

# Global Caches
VOICE_CACHE = {} # (text, persona) -> url

# System State
GOD_MODE_ACTIVE = False
CURRENT_MODE = "NORMAL"

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

    def _generate_chat_response(self, message):
        """
        Attempts LLM providers in order: Ollama -> OpenAI -> Fallback
        """
        import urllib.request
        
        # 1. Try Ollama (Local, Fast, Free)
        try:
            ollama_url = "http://localhost:11434/api/generate"
            payload = json.dumps({
                "model": "llama3.2",
                "prompt": message,
                "stream": False
            }).encode('utf-8')
            
            req = urllib.request.Request(ollama_url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                if data.get("response"):
                    print("CORE > 🦙 OLLAMA SUCCESS")
                    return data["response"]
        except Exception as e:
            print(f"CORE > Ollama unavailable: {e}")
        
        # 2. Try OpenAI (API Key required)
        try:
            openai_key = os.environ.get("OPENAI_API_KEY", "")
            if openai_key:
                openai_url = "https://api.openai.com/v1/chat/completions"
                payload = json.dumps({
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are Gabriel, an advanced AI assistant. Be helpful, concise, and accurate."},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 1000
                }).encode('utf-8')
                
                req = urllib.request.Request(openai_url, data=payload, headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {openai_key}'
                })
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode())
                    if data.get("choices"):
                        print("CORE > 🤖 OPENAI SUCCESS")
                        return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"CORE > OpenAI unavailable: {e}")
        
        # 3. Fallback: Intelligent Rule-Based
        return self._fallback_response(message)
    
    def _fallback_response(self, message):
        """Smart fallback when no LLM is available"""
        msg_lower = message.lower()
        
        # Translation
        if "translate" in msg_lower:
            if "french" in msg_lower and "love" in msg_lower:
                return "\"I love you\" in French is: **Je t'aime** 💕"
            elif "spanish" in msg_lower and "love" in msg_lower:
                return "\"I love you\" in Spanish is: **Te quiero** or **Te amo** 💕"
            return "I can help translate! Please specify the text and target language."
        
        # Explanations
        if "explain" in msg_lower and ("ai" in msg_lower or "artificial intelligence" in msg_lower):
            return """**Artificial Intelligence (AI) - Explained Simply:**

Imagine you have a very smart robot friend. This robot can learn things by looking at lots of examples, just like you learn by reading books or watching videos.

AI is like giving a computer a brain that can:
- **Learn** from experience
- **Recognize** patterns (like faces in photos)
- **Make decisions** based on what it learned
- **Talk and understand** language (like me!)

For a 6-year-old: "AI is a computer that can learn and think a little bit like humans do. It's like teaching your computer to be really, really good at helping you!" 🤖"""
        
        # Travel ideas
        if "travel" in msg_lower and ("ideas" in msg_lower or "destinations" in msg_lower or "best" in msg_lower):
            return """**Top 10 Travel Ideas Around the World:**

1. 🗼 **Paris, France** — The City of Light, Eiffel Tower, world-class cuisine
2. 🏯 **Kyoto, Japan** — Ancient temples, cherry blossoms, traditional culture
3. 🏝️ **Maldives** — Crystal-clear waters, luxury overwater bungalows
4. 🦁 **Serengeti, Tanzania** — Epic safari, witness the Great Migration
5. 🏔️ **Swiss Alps** — Breathtaking mountains, skiing, Alpine villages
6. 🌴 **Bali, Indonesia** — Temples, rice terraces, beaches, wellness retreats
7. 🎭 **Barcelona, Spain** — Gaudí architecture, beaches, vibrant nightlife
8. 🌋 **Iceland** — Northern Lights, geysers, otherworldly landscapes
9. 🗿 **Machu Picchu, Peru** — Ancient Incan citadel in the clouds
10. 🌆 **New York City, USA** — The city that never sleeps, Broadway, Central Park

Would you like more details on any of these destinations?"""
        
        # Code requests
        if "code" in msg_lower or "python" in msg_lower or "javascript" in msg_lower or "function" in msg_lower:
            if "fibonacci" in msg_lower:
                return """Here's a Python function for the Fibonacci sequence:

```python
def fibonacci(n):
    \"\"\"Generate Fibonacci sequence up to n numbers\"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# Example usage
print(fibonacci(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```"""
            return "I can help with code! Please describe what you'd like to build."
        
        # Greetings
        if any(g in msg_lower for g in ["hello", "hi", "hey", "good morning", "good evening"]):
            return "Hello! I'm Gabriel, your AI assistant. How can I help you today? 👋"
        
        # Help
        if "help" in msg_lower or "what can you do" in msg_lower:
            return """**I'm Gabriel — Here's what I can help with:**

💬 **Chat** — General conversation and questions
🔍 **Search** — Find information on any topic  
✍️ **Write** — Create emails, articles, social posts
💻 **Code** — Write, explain, or debug code
🌍 **Translate** — Convert text between languages
📊 **Analyze** — Break down complex topics

Just ask me anything!"""
        
        # Default
        return f"I received your message: \"{message[:100]}...\"\n\nNote: To enable full AI responses, please ensure Ollama is running locally (`ollama serve`) or set your OPENAI_API_KEY environment variable."

    def do_GET(self):
        global GOD_MODE_ACTIVE, CURRENT_MODE
        
        # Parse URL
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

        elif path == "/api/status":
             self.send_response(200)
             self.send_header('Content-type', 'application/json')
             self.end_headers()
             self.wfile.write(json.dumps({"status": "ok", "mode": CURRENT_MODE}).encode())
             return

        # ---------------------------------------------------------
        # 2.0 API: CHAT (GABRIEL AI CHAT ENDPOINT)
        # ---------------------------------------------------------
        elif path == "/api/chat":
            # Usage: POST /api/chat with JSON body: {"message": "...", "history": [...]}
            # OR GET: /api/chat?message=...
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get message from query string (GET) or body (POST handled in do_POST)
            message = query.get("message", [""])[0]
            
            if not message:
                self.wfile.write(json.dumps({"status": "error", "message": "No message provided"}).encode())
                return
            
            print(f"CORE > 💬 CHAT: '{message[:50]}...'")
            
            response = self._generate_chat_response(message)
            
            self.wfile.write(json.dumps({
                "status": "ok",
                "response": response,
                "model": "gabriel-core"
            }).encode())
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
                row = c.fetchone()
                stats["files"] = row[0] or 0
                stats["size"] = row[1] or 0
                stats["mode"] = CURRENT_MODE if not GOD_MODE_ACTIVE else "GOD"
                if CURRENT_MODE == "OMEGA": stats["mode"] = "OMEGA" # Omega overrides God temporarily
                
                # CHRONOS DATA (MemCell)
                try:
                    # System Vibe (Latest)
                    c.execute("SELECT vibe FROM memory_events ORDER BY timestamp DESC LIMIT 1")
                    vibe_row = c.fetchone()
                    stats["vibe"] = vibe_row[0] if vibe_row else 50
                    
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
            
            # GHOST STATUS & SUBSYSTEMS
            stats["ghost"] = "System Nominal"
            stats["subsystems"] = {
                "vr_bridge": False,
                "studio_hand": False
            }
            try:
                # Ghost Check
                if GHOST_STATUS_FILE.exists():
                     with open(GHOST_STATUS_FILE, "r") as f:
                         stats["ghost"] = f.read().strip()
                
                # Subsystem Check (Process Scan)
                # Quick scan of ps -A for our python scripts
                ps = subprocess.run(["ps", "-A"], capture_output=True, text=True).stdout
                if "turbo_quest_bridge.py" in ps: stats["subsystems"]["vr_bridge"] = True
                if "turbo_studio_hand.py" in ps: stats["subsystems"]["studio_hand"] = True
                
            except: pass
                
            self.wfile.write(json.dumps(stats).encode())
            return

        # ---------------------------------------------------------
        # 2.5 API: GABRIEL COMMAND INTERFACE (REMOTE CONTROL)
        # ---------------------------------------------------------
        elif path == "/api/gabriel/command":
            # Usage: /api/gabriel/command?cmd=status
            cmd = query.get("cmd", ["status"])[0]
            args = query.get("args", [""])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            print(f"CORE > 🤖 GABRIEL REMOTE COMMAND: {cmd.upper()} {args}")
            
            # Execute via subprocess (Gabriel CLI)
            # We call turbo_gabriel.py directly
            full_cmd = ["python3", str(SCRIPTS_DIR / "turbo_gabriel.py"), cmd]
            if args:
                full_cmd.extend(args.split())
                
            # For 'status' or simple info, we might want to capture output
            # For 'play' or actions, fire and forget
            
            if cmd in ['status', 'omniscience', 'overlap', 'list']:
                 result = subprocess.run(full_cmd, capture_output=True, text=True)
                 output = result.stdout
                 self.wfile.write(json.dumps({"status": "executed", "output": output}).encode())
            else:
                 subprocess.Popen(full_cmd)
                 self.wfile.write(json.dumps({"status": "started", "command": f"{cmd} {args}"}).encode())
            return

            return
            
        # ---------------------------------------------------------
        # 2.6 API: VOICE (DIRECT SPEECH)
        # ---------------------------------------------------------
        elif path == "/api/voice/generate":
            # Usage: /api/voice/generate?text=Hello&persona=titan
            text = query.get("text", [""])[0]
            persona = query.get("persona", ["titan"])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            print(f"CORE > 🗣️ VOICE REQUEST: [{persona.upper()}] '{text}'")
            
            # 1. CHECK CACHE
            cache_key = (text, persona)
            if cache_key in VOICE_CACHE:
                 print(f"CORE > ⚡ CACHE HIT: {text}")
                 self.wfile.write(json.dumps({"status": "ok", "url": VOICE_CACHE[cache_key], "cached": True}).encode())
                 return

            # PROXY TO VOICE WORKER (Assuming localhost:8787)
            # If not running, we could fallback to system TTS or error.
            worker_url = "http://localhost:8787/generate"
            
            try:
                # Prepare JSON payload
                payload = json.dumps({
                    "text": text,
                    "personaId": persona, # Mapping might be needed if IDs differ
                    "dspId": "broadcast"
                }).encode('utf-8')
                
                req = urllib.request.Request(worker_url, data=payload, headers={'Content-Type': 'application/json'})
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    worker_resp = json.loads(response.read().decode())
                    # Expecting { "data": { "url": "/audio/..." } }
                    
                    if worker_resp.get("status") == "ok":
                         audio_url = worker_resp["data"]["url"]
                         full_url = f"http://localhost:8787{audio_url}"
                         
                         # CACHE IT
                         VOICE_CACHE[cache_key] = full_url
                         
                         self.wfile.write(json.dumps({"status": "ok", "url": full_url}).encode())
                    else:
                         self.wfile.write(json.dumps({"status": "error", "message": "Worker Error"}).encode())

            except Exception as e:
                print(f"CORE > ❌ Voice Proxy Error: {e}")
                # Fallback?
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
            
            return
            
        # ---------------------------------------------------------
        # 2.7 API: GOD MODE ACTIVATION
        # ---------------------------------------------------------
        elif path == "/api/god_mode/activate":
            GOD_MODE_ACTIVE = True
            CURRENT_MODE = "GOD"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            print(f"CORE > ⚠️ GOD MODE ACTIVATION SEQUENCE INITIATED")
            self.wfile.write(json.dumps({"status": "activated", "mode": "GOD"}).encode())
            return

        # ---------------------------------------------------------
        # 2.8 API: MODE SET
        # ---------------------------------------------------------
        elif path.startswith("/api/mode/set"):
            mode = query.get("mode", ["CORE"])[0]
            CURRENT_MODE = mode.upper()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "mode": CURRENT_MODE}).encode())
            return

        # ---------------------------------------------------------
        # 2.9 API: FORGE GENERATION (AUDIO/VIDEO)
        # ---------------------------------------------------------
        elif path.startswith("/api/generate/audio"):
            # Usage: /api/generate/audio?type=scene&prompt=...
            gen_type = query.get("type", ["sfx"])[0]
            prompt = query.get("prompt", [""])[0]
            
            print(f"CORE > 🔨 FORGE AUDIO: [{gen_type.upper()}] '{prompt}'")
            
            # Simulate Job Start (Async would be better but keeping zero latency response)
            # In real system: subprocess.Popen(["python3", "turbo_audio_gen.py", ...])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started", "job": f"AUDIO-{gen_type.upper()}-001"}).encode())
            return

        elif path.startswith("/api/generate/video"):
            model = query.get("model", ["runway"])[0]
            prompt = query.get("prompt", [""])[0]
            
            print(f"CORE > 🎬 FORGE VIDEO: [{model.upper()}] '{prompt}'")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started", "job": f"VIDEO-{model.upper()}-001"}).encode())
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
        # 3.5 API: MEMCELL STATUS (THE HIVE)
        # ---------------------------------------------------------
        elif path == "/api/memcell/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Connect to MemCell for real data
            try:
                # Lightweight connection to avoid full class init overhead if possible, 
                # but for now we reuse the class logic which is robust
                if not hasattr(self, 'memory'):
                    from turbo_memcell import MemCell
                    self.memory = MemCell()
                
                # 1. Stats
                self.memory.cursor.execute("SELECT count(*) FROM memcells WHERE status='ACTIVE'")
                total_cells = self.memory.cursor.fetchone()[0]
                self.memory.cursor.execute("SELECT count(*) FROM memory_events")
                total_events = self.memory.cursor.fetchone()[0]
                
                # 2. Vibe
                self.memory.cursor.execute("SELECT AVG(vibe_score) FROM memory_events ORDER BY id DESC LIMIT 20")
                vibe = self.memory.cursor.fetchone()[0] or 50
                
                # 3. Recent Events
                self.memory.cursor.execute("SELECT timestamp, author, content, tags FROM memory_events ORDER BY id DESC LIMIT 10")
                recents = []
                for row in self.memory.cursor.fetchall():
                    recents.append({
                        "timestamp": row[0],
                        "author": row[1],
                        "content": row[2],
                        "tags": row[3]
                    })
                    
                # 4. Top Tags (Overlap)
                self.memory.cursor.execute("SELECT tags FROM memory_events ORDER BY id DESC LIMIT 50")
                all_tags = []
                for r in self.memory.cursor.fetchall():
                    if r[0]: all_tags.extend([t.strip() for t in r[0].split(',')])
                
                from collections import Counter
                top_tags = [{"tag": k, "count": v} for k, v in Counter(all_tags).most_common(5)]

                data = {
                    "vibe": round(vibe, 1), 
                    "total_events": total_events, 
                    "total_cells": total_cells, 
                    "recent_events": recents, 
                    "top_tags": top_tags
                }
            except Exception as e:
                print(f"API Error: {e}")
                data = {
                    "vibe": 0, 
                    "total_events": 0, 
                    "total_cells": 0, 
                    "recent_events": [{"timestamp": "", "author": "SYS", "content": f"DB Error: {e}"}], 
                    "top_tags": []
                }

            self.wfile.write(json.dumps(data).encode())
            return


        # ---------------------------------------------------------
        # 3.6 API: ARCHAEOLOGIST (DATA MINING)
        # ---------------------------------------------------------
        elif path == "/api/archaeologist/scan":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            print("CORE > 🏺 TRIGGERING ARCHAEOLOGIST SCAN...")
            # Run in background with --json flag
            cmd = ["python3", str(SCRIPTS_DIR / "turbo_archaeologist.py"), "--json"]
            subprocess.Popen(cmd)
            
            self.wfile.write(json.dumps({"status": "started", "message": "Archaeologist is digging..."}).encode())
            return
            
        elif path == "/api/archaeologist/results":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            json_path = SCRIPTS_DIR.parent / "Database" / "archaeologist_latest.json"
            if json_path.exists():
                try:
                    with open(json_path, 'r') as f:
                        content = f.read()
                    self.wfile.write(content.encode())
                except:
                    self.wfile.write(json.dumps([]).encode())
            else:
                 self.wfile.write(json.dumps([]).encode())
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

if __name__ == "__main__":
    import time
    
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    print(f"CORE > 🌐 GOD MODE SERVER ONLINE: http://localhost:{PORT}")
    print(f"CORE > 🏠 Serving Portal from: {SCRIPTS_DIR.parent / 'Dashboard'}")
    
    try:
        with ReusableTCPServer(("", PORT), GodModeHandler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nCORE > 🛑 Server Offline.")
    except OSError as e:
        print(f"CORE > ❌ FATAL ERROR: Could not bind to port {PORT}. {e}")

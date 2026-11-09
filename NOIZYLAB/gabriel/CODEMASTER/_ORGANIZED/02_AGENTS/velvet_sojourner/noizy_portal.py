import os
import sys
import threading
import subprocess
import json
import time
from flask import Flask, render_template_string, jsonify, request
from noizy_memcell import memory_core

# NOIZYLAB OMNI-PORTAL v1.0
# "The Glass Interface" for iPad & Planar2485
# TARGET: 0.0.0.0:5000

app = Flask(__name__)

# --- HTML TEMPLATE (EMBEDDED FOR PORTABILITY) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MC96 MISSION CONTROL</title>
    <style>
        :root { --neon: #00ff9d; --bg: #050505; --panel: #111; --text: #eee; --alert: #ff0055; }
        body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; margin: 0; padding: 20px; overflow: hidden; }
        #header { border-bottom: 2px solid var(--neon); padding-bottom: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        #vibe-box { font-size: 1.2rem; font-weight: bold; color: var(--neon); text-shadow: 0 0 10px var(--neon); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 80vh; }
        .panel { background: var(--panel); border: 1px solid #333; padding: 15px; border-radius: 4px; display: flex; flex-direction: column; }
        h2 { margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 5px; font-size: 1rem; color: #888; text-transform: uppercase; }
        
        button { background: #222; border: 1px solid var(--neon); color: var(--neon); padding: 15px; margin: 5px 0; font-family: inherit; font-size: 1rem; cursor: pointer; transition: 0.2s; }
        button:active { background: var(--neon); color: var(--bg); }
        button.alert { border-color: var(--alert); color: var(--alert); }
        
        #chat-log { flex: 1; overflow-y: auto; font-size: 0.9rem; line-height: 1.4; opacity: 0.8; }
        .log-entry { margin-bottom: 4px; }
        .user-SHIRL { color: #d6f; }
        .user-ENGR { color: #fd0; }
        .user-USER { color: #0ff; }
        
        input[type="text"] { background: #000; border: 1px solid #444; color: #fff; padding: 10px; font-family: inherit; width: 100%; box-sizing: border-box; margin-top: 10px; }
    </style>
</head>
<body>
    <div id="header">
        <div>MC96 MISSION CONTROL <span style="font-size:0.8rem; color:#666;">v1.0</span></div>
        <div id="vibe-box">CONNECTING...</div>
    </div>

    <div class="grid">
        <!-- LEFT: COMMANDS -->
        <div class="panel">
            <h2>Operations</h2>
            <button onclick="cmd('SCAN')">[1] SCAN FLEET</button>
            <button onclick="cmd('REPATRIATE')">[2] REPATRIATE</button>
            <button onclick="cmd('TEAM')">[N] NOIZYTEAM</button>
            <div style="flex:1"></div>
            <button class="alert" onclick="cmd('PREACH')">[P] PREACH TO GABRIEL</button>
        </div>

        <!-- RIGHT: CHAT / FEED -->
        <div class="panel">
            <h2>Neural Log</h2>
            <div id="chat-log"></div>
            <input type="text" id="preach-input" placeholder="Type to Preach..." onkeypress="handleInput(event)">
        </div>
    </div>

    <script>
        function updateVibe() {
            fetch('/api/vibe').then(r => r.json()).then(data => {
                document.getElementById('vibe-box').innerText = data.vibe;
                renderChat(data.logs);
            });
        }
        
        function renderChat(logs) {
            const logDiv = document.getElementById('chat-log');
            logDiv.innerHTML = logs.map(l => `<div class="log-entry user-${l.user}">[${l.pid}] ${l.msg}</div>`).join('');
            // Auto scroll? Only if near bottom.
        }

        function cmd(action) {
            fetch('/api/cmd/' + action, {method: 'POST'});
        }

        function handleInput(e) {
            if (e.key === 'Enter') {
                const txt = e.target.value;
                fetch('/api/preach', {
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: txt})
                });
                e.target.value = '';
            }
        }

        // Zero Latency Polling (500ms)
        setInterval(updateVibe, 500);
        updateVibe();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/vibe')
def get_vibe():
    overlap = memory_core.analyze_temporal_overlap()
    # Get last 20 logs from MemCell (simulated via raw read or memory_core if it had a fetch)
    # Since memory_core doesn't expose a 'read logs' easily yet, lets just show the status
    # Actually, let's peek at the log file for the chat feed
    logs = []
    if os.path.exists("noizy_memcell.json"):
        try:
            with open("noizy_memcell.json", 'r') as f:
                data = json.load(f)
                # Just grab last 10 interactions
                for i in data.get("interactions", [])[-15:]:
                    logs.append({"user": i.get("persona", "SYS"), "msg": i.get("action", ""), "pid": i.get("timestamp", "")[-8:]})
        except: pass
        
    return jsonify({
        "vibe": overlap["overlap_status"],
        "logs": list(reversed(logs))
    })

@app.route('/api/cmd/<action>', methods=['POST'])
def run_cmd(action):
    # Fire and forget commands
    print(f">>> [PORTAL] COMMAND RECEIVED: {action}")
    memory_core.log_interaction(f"Portal Command: {action}", "REMOTE_CMD", "USER")
    
    if action == "PREACH":
        subprocess.Popen(['python3', 'noizy_gabriel_uplink.py'])
    elif action == "SCAN":
        subprocess.Popen(['python3', 'deep_audio_scan.py'])
    elif action == "REPATRIATE":
        subprocess.Popen(['python3', 'noizy_repatriator.py'])
    elif action == "TEAM":
        # Launching Team in headless mode? 
        pass 
        
    return jsonify({"status": "OK"})

@app.route('/api/preach', methods=['POST'])
def preach_text():
    data = request.json
    text = data.get("text", "")
    if text:
        # Transmit directly via Preacher logic? 
        # Or just log it and spawn an uplink?
        # Let's spawn a one-off transmit script or use socket here?
        # For simplicity/speed: Log it, Gabriel Uplink will see it if we modify Uplink to watch logs, 
        # But Uplink v1.0 is Audio -> TCP.
        # Let's just create a quick socket sender here for Zero Latency.
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                s.connect(("10.90.90.91", 9999))
                s.sendall(f"SERMON|{text}".encode('utf-8'))
            memory_core.log_interaction(f"Preached (Text): {text}", "UPLINK_SUCCESS", "USER")
        except:
            memory_core.log_interaction(f"Preached (Text-Fail): {text}", "UPLINK_FAIL", "USER")
            
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    print(">>> [OMNI-PORTAL v1.0] LISTENING ON 0.0.0.0:5000")
    print(">>> ACCESS VIA IPAD: http://<THIS_IP>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

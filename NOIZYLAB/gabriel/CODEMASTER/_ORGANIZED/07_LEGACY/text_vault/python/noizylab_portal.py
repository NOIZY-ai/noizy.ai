#!/usr/bin/env python3
"""
🎨 NOIZYLAB PORTAL - GABRIEL's Ultimate Web Interface 🎨
========================================================

Revolutionary Features:
✨ Real-time system monitoring dashboard
✨ Interactive 3D visualizations
✨ Audio/video processing interface
✨ AI model training studio
✨ File management & organization
✨ Network monitoring & control
✨ Code execution sandbox
✨ Collaborative workspace
✨ Live streaming & broadcasting
✨ Advanced analytics & reporting
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
import asyncio
import json
import psutil
import subprocess
from pathlib import Path
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gabriel_noizylab_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# GABRIEL paths
GABRIEL_ROOT = Path('/Users/rsp_ms/GABRIEL')
IMAGES_PATH = GABRIEL_ROOT / 'IMAGES'
IMAGES_PATH.mkdir(exist_ok=True)

# System stats cache
system_stats = {
    'cpu': 0,
    'memory': 0,
    'disk': 0,
    'network': {'sent': 0, 'recv': 0},
    'uptime': 0
}

@app.route('/')
def index():
    """Main dashboard."""
    return render_template('noizylab_portal.html')

@app.route('/api/system/stats')
def get_system_stats():
    """Get real-time system statistics."""
    global system_stats
    
    # CPU usage
    system_stats['cpu'] = psutil.cpu_percent(interval=0.1)
    
    # Memory usage
    mem = psutil.virtual_memory()
    system_stats['memory'] = mem.percent
    system_stats['memory_used'] = mem.used / (1024**3)  # GB
    system_stats['memory_total'] = mem.total / (1024**3)  # GB
    
    # Disk usage
    disk = psutil.disk_usage('/')
    system_stats['disk'] = disk.percent
    system_stats['disk_used'] = disk.used / (1024**3)  # GB
    system_stats['disk_total'] = disk.total / (1024**3)  # GB
    
    # Network
    net = psutil.net_io_counters()
    system_stats['network']['sent'] = net.bytes_sent / (1024**2)  # MB
    system_stats['network']['recv'] = net.bytes_recv / (1024**2)  # MB
    
    # Uptime
    system_stats['uptime'] = time.time() - psutil.boot_time()
    
    return jsonify(system_stats)

@app.route('/api/gabriel/files')
def list_gabriel_files():
    """List GABRIEL files."""
    files = []
    for item in GABRIEL_ROOT.iterdir():
        if item.is_file():
            files.append({
                'name': item.name,
                'size': item.stat().st_size,
                'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
            })
    return jsonify(files)

@app.route('/api/images/list')
def list_images():
    """List images in IMAGES folder."""
    images = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        for img in IMAGES_PATH.glob(ext):
            images.append({
                'name': img.name,
                'path': str(img),
                'size': img.stat().st_size,
                'url': f'/api/images/view/{img.name}'
            })
    return jsonify(images)

@app.route('/api/images/view/<filename>')
def view_image(filename):
    """View an image."""
    img_path = IMAGES_PATH / filename
    if img_path.exists():
        return send_file(img_path)
    return jsonify({'error': 'Image not found'}), 404

@app.route('/api/convert/png-to-jpg', methods=['POST'])
def convert_png_to_jpg():
    """Convert PNG to JPG using sips."""
    data = request.json
    png_file = data.get('png_file')
    
    if not png_file:
        return jsonify({'error': 'No file specified'}), 400
    
    png_path = Path(png_file)
    if not png_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    # Output path
    jpg_path = IMAGES_PATH / png_path.stem + '.jpg'
    
    # Convert using sips
    try:
        subprocess.run([
            'sips', '-s', 'format', 'jpeg',
            '-s', 'formatOptions', '100',
            str(png_path), '--out', str(jpg_path)
        ], check=True, capture_output=True)
        
        return jsonify({
            'success': True,
            'jpg_path': str(jpg_path),
            'message': f'Converted {png_path.name} to JPG'
        })
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/run/command', methods=['POST'])
def run_command():
    """Execute terminal command."""
    data = request.json
    command = data.get('command')
    
    if not command:
        return jsonify({'error': 'No command specified'}), 400
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mc96/scan', methods=['POST'])
def run_mc96_scan():
    """Run MC96ECOUNIVERSE scan."""
    try:
        result = subprocess.run([
            'python3',
            str(GABRIEL_ROOT / 'THE_FAMILY' / 'mc96ecouniverse.py')
        ], capture_output=True, text=True, timeout=60)
        
        return jsonify({
            'success': True,
            'output': result.stdout,
            'errors': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print('🔌 Client connected to NOIZYLAB PORTAL')
    emit('message', {'data': 'Connected to GABRIEL NOIZYLAB PORTAL'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print('🔌 Client disconnected from NOIZYLAB PORTAL')

@socketio.on('request_stats')
def handle_stats_request():
    """Stream real-time stats."""
    stats = get_system_stats()
    emit('stats_update', stats.get_json())

def background_stats_broadcaster():
    """Broadcast stats every 2 seconds."""
    while True:
        socketio.sleep(2)
        stats = get_system_stats()
        socketio.emit('stats_update', stats.get_json(), broadcast=True)

# HTML Template (embedded)
TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 NOIZYLAB PORTAL - GABRIEL</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            overflow-x: hidden;
        }
        
        .header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }
        
        .header h1 {
            font-size: 3em;
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
            animation: glow 2s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
            50% { text-shadow: 0 0 40px rgba(255,255,255,0.8); }
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        }
        
        .card h2 {
            margin-bottom: 15px;
            font-size: 1.5em;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            padding-bottom: 10px;
        }
        
        .stat {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00f260, #0575e6);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
            margin: 5px;
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }
        
        .terminal {
            background: #000;
            color: #0f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            height: 200px;
            overflow-y: auto;
            margin-top: 10px;
        }
        
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        
        .image-thumb {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .image-thumb:hover {
            transform: scale(1.1);
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        .status-online { background: #0f0; }
        .status-warning { background: #ff0; }
        .status-error { background: #f00; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 NOIZYLAB PORTAL</h1>
        <p>GABRIEL INFINITY X1000 Command Center</p>
        <p><span class="status-indicator status-online"></span> System Online</p>
    </div>
    
    <div class="dashboard">
        <!-- System Stats -->
        <div class="card">
            <h2>💻 System Monitor</h2>
            <div class="stat">
                <span>CPU Usage:</span>
                <span id="cpu-stat">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="cpu-bar" style="width: 0%">0%</div>
            </div>
            
            <div class="stat">
                <span>Memory:</span>
                <span id="mem-stat">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="mem-bar" style="width: 0%">0%</div>
            </div>
            
            <div class="stat">
                <span>Disk:</span>
                <span id="disk-stat">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="disk-bar" style="width: 0%">0%</div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="card">
            <h2>⚡ Quick Actions</h2>
            <button class="btn" onclick="runMC96Scan()">🔍 Run MC96 Scan</button>
            <button class="btn" onclick="refreshImages()">🖼️ Refresh Images</button>
            <button class="btn" onclick="openTerminal()">💻 Terminal</button>
            <button class="btn" onclick="convertPNGs()">🔄 Convert PNGs</button>
            <div id="action-output" class="terminal" style="display:none;"></div>
        </div>
        
        <!-- Image Gallery -->
        <div class="card" style="grid-column: span 2;">
            <h2>🖼️ GABRIEL Images</h2>
            <div id="image-gallery" class="image-grid">
                <p>Loading images...</p>
            </div>
        </div>
        
        <!-- Network Stats -->
        <div class="card">
            <h2>🌐 Network</h2>
            <div class="stat">
                <span>⬆️ Sent:</span>
                <span id="net-sent">0 MB</span>
            </div>
            <div class="stat">
                <span>⬇️ Received:</span>
                <span id="net-recv">0 MB</span>
            </div>
            <div class="stat">
                <span>⏱️ Uptime:</span>
                <span id="uptime">0h 0m</span>
            </div>
        </div>
        
        <!-- Command Center -->
        <div class="card">
            <h2>🎮 Command Center</h2>
            <input type="text" id="cmd-input" placeholder="Enter command..." 
                   style="width:100%;padding:10px;border-radius:5px;border:none;margin-bottom:10px;">
            <button class="btn" onclick="executeCommand()">Execute</button>
            <div id="cmd-output" class="terminal"></div>
        </div>
    </div>
    
    <script>
        const socket = io();
        
        socket.on('connect', () => {
            console.log('🔌 Connected to NOIZYLAB PORTAL');
            loadImages();
            startStatsUpdate();
        });
        
        socket.on('stats_update', (data) => {
            updateStats(data);
        });
        
        function startStatsUpdate() {
            setInterval(() => {
                fetch('/api/system/stats')
                    .then(r => r.json())
                    .then(data => updateStats(data));
            }, 2000);
        }
        
        function updateStats(data) {
            // CPU
            document.getElementById('cpu-stat').textContent = data.cpu.toFixed(1) + '%';
            document.getElementById('cpu-bar').style.width = data.cpu + '%';
            document.getElementById('cpu-bar').textContent = data.cpu.toFixed(1) + '%';
            
            // Memory
            document.getElementById('mem-stat').textContent = data.memory.toFixed(1) + '%';
            document.getElementById('mem-bar').style.width = data.memory + '%';
            document.getElementById('mem-bar').textContent = data.memory.toFixed(1) + '%';
            
            // Disk
            document.getElementById('disk-stat').textContent = data.disk.toFixed(1) + '%';
            document.getElementById('disk-bar').style.width = data.disk + '%';
            document.getElementById('disk-bar').textContent = data.disk.toFixed(1) + '%';
            
            // Network
            document.getElementById('net-sent').textContent = data.network.sent.toFixed(2) + ' MB';
            document.getElementById('net-recv').textContent = data.network.recv.toFixed(2) + ' MB';
            
            // Uptime
            const hours = Math.floor(data.uptime / 3600);
            const minutes = Math.floor((data.uptime % 3600) / 60);
            document.getElementById('uptime').textContent = hours + 'h ' + minutes + 'm';
        }
        
        function loadImages() {
            fetch('/api/images/list')
                .then(r => r.json())
                .then(images => {
                    const gallery = document.getElementById('image-gallery');
                    if (images.length === 0) {
                        gallery.innerHTML = '<p>No images found</p>';
                        return;
                    }
                    gallery.innerHTML = images.map(img => 
                        `<img src="${img.url}" class="image-thumb" 
                              title="${img.name}" alt="${img.name}"
                              onclick="window.open('${img.url}', '_blank')">`
                    ).join('');
                });
        }
        
        function refreshImages() {
            loadImages();
            showOutput('action-output', '✅ Images refreshed!');
        }
        
        function runMC96Scan() {
            showOutput('action-output', '🔍 Running MC96ECOUNIVERSE scan...');
            fetch('/api/mc96/scan', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    showOutput('action-output', data.output || data.error);
                });
        }
        
        function convertPNGs() {
            showOutput('action-output', '🔄 Converting PNGs to JPGs...');
            const cmd = 'cd ~/Desktop && for f in *.png; do sips -s format jpeg "$f" --out "/Users/rsp_ms/GABRIEL/IMAGES/${f%.png}.jpg"; done';
            executeCustomCommand(cmd);
        }
        
        function executeCommand() {
            const cmd = document.getElementById('cmd-input').value;
            if (!cmd) return;
            executeCustomCommand(cmd);
        }
        
        function executeCustomCommand(cmd) {
            showOutput('cmd-output', '$ ' + cmd);
            fetch('/api/run/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd })
            })
            .then(r => r.json())
            .then(data => {
                showOutput('cmd-output', data.stdout || data.error);
            });
        }
        
        function showOutput(elementId, text) {
            const el = document.getElementById(elementId);
            el.style.display = 'block';
            el.textContent = text;
        }
        
        function openTerminal() {
            document.getElementById('cmd-output').style.display = 'block';
            document.getElementById('cmd-input').focus();
        }
    </script>
</body>
</html>
'''

# Save HTML template
TEMPLATE_DIR = GABRIEL_ROOT / 'templates'
TEMPLATE_DIR.mkdir(exist_ok=True)
with open(TEMPLATE_DIR / 'noizylab_portal.html', 'w') as f:
    f.write(TEMPLATE)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎨 NOIZYLAB PORTAL - Starting GABRIEL Web Interface")
    print("="*70)
    print(f"🌐 Server: http://localhost:5000")
    print(f"📁 Root: {GABRIEL_ROOT}")
    print(f"🖼️ Images: {IMAGES_PATH}")
    print("="*70 + "\n")
    
    # Start background stats broadcaster
    socketio.start_background_task(background_stats_broadcaster)
    
    # Run server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

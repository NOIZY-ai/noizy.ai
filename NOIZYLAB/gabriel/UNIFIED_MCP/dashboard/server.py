#!/usr/bin/env python3
"""
🧠 NOIZYLAB Dashboard Server
REST API backend for the web dashboard
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

NOIZYLAB_ROOT = Path("/Users/m2ultra/NOIZYLAB")
CONFIG_DIR = Path.home() / ".noizylab"
KEYS_FILE = CONFIG_DIR / "api_keys.json"
MEMORY_FILE = CONFIG_DIR / "memory.json"
INTELLIGENCE_FILE = NOIZYLAB_ROOT / "GABRIEL" / "intelligence_report.json"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "hostname": run_cmd("hostname"),
        "uptime": run_cmd("uptime"),
        "cpu": run_cmd("sysctl -n machdep.cpu.brand_string"),
    })


@app.route('/api/scan', methods=['GET', 'POST'])
def scan_codebase():
    from collections import defaultdict
    
    stats = {
        'files': 0,
        'lines': 0,
        'bytes': 0,
        'languages': defaultdict(lambda: {'files': 0, 'lines': 0}),
    }
    
    lang_map = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.go': 'Go', '.rs': 'Rust', '.sh': 'Shell', '.md': 'Markdown'}
    skip = {'.git', 'node_modules', 'venv', '__pycache__'}
    
    for root, dirs, files in os.walk(NOIZYLAB_ROOT):
        dirs[:] = [d for d in dirs if d not in skip]
        for file in files:
            if file.startswith('.'):
                continue
            fp = Path(root) / file
            try:
                ext = fp.suffix.lower()
                size = fp.stat().st_size
                stats['files'] += 1
                stats['bytes'] += size
                
                if ext in lang_map:
                    lines = len(fp.read_text(errors='ignore').split('\n'))
                    stats['lines'] += lines
                    stats['languages'][lang_map[ext]]['files'] += 1
                    stats['languages'][lang_map[ext]]['lines'] += lines
            except:
                continue
    
    stats['languages'] = dict(stats['languages'])
    
    INTELLIGENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    save_json(INTELLIGENCE_FILE, stats)
    
    return jsonify(stats)


@app.route('/api/keys', methods=['GET', 'POST'])
def api_keys():
    keys = load_json(KEYS_FILE)
    
    if request.method == 'POST':
        data = request.json
        keys[data['service']] = data['key']
        save_json(KEYS_FILE)
        os.chmod(KEYS_FILE, 0o600)
        return jsonify({"saved": data['service']})
    
    return jsonify({k: bool(v) for k, v in keys.items()})


@app.route('/api/memory', methods=['GET', 'POST', 'DELETE'])
def memory():
    mem = load_json(MEMORY_FILE)
    
    if request.method == 'POST':
        data = request.json
        mem[data['key']] = {
            'value': data['value'],
            'created': datetime.now().isoformat(),
        }
        save_json(MEMORY_FILE, mem)
        return jsonify({"stored": data['key']})
    
    if request.method == 'DELETE':
        key = request.args.get('key')
        if key in mem:
            del mem[key]
            save_json(MEMORY_FILE, mem)
            return jsonify({"deleted": key})
        return jsonify({"error": "Not found"}), 404
    
    return jsonify({"count": len(mem), "keys": list(mem.keys())})


@app.route('/api/network')
def network():
    result = run_cmd("arp -a")
    return jsonify({"devices": result.split('\n')})


@app.route('/api/volumes')
def volumes():
    result = run_cmd("ls /Volumes")
    return jsonify({"volumes": result.split('\n')})


@app.route('/api/processes')
def processes():
    pattern = request.args.get('filter', '')
    if pattern:
        result = run_cmd(f"ps aux | grep -i '{pattern}' | head -20")
    else:
        result = run_cmd("ps aux | head -30")
    return jsonify({"processes": result.split('\n')})


@app.route('/api/generate/video', methods=['POST'])
def generate_video():
    data = request.json
    return jsonify({
        "status": "queued",
        "provider": data.get('provider', 'runway'),
        "prompt": data.get('prompt', ''),
        "message": "Video generation queued"
    })


@app.route('/api/generate/audio', methods=['POST'])
def generate_audio():
    data = request.json
    return jsonify({
        "status": "queued",
        "provider": data.get('provider', 'suno'),
        "prompt": data.get('prompt', ''),
        "message": "Audio generation queued"
    })


@app.route('/api/generate/avatar', methods=['POST'])
def generate_avatar():
    data = request.json
    return jsonify({
        "status": "queued",
        "script": data.get('script', ''),
        "message": "Avatar creation queued"
    })


if __name__ == '__main__':
    print("🧠 NOIZYLAB Dashboard Server starting...")
    print("   http://localhost:5175")
    app.run(host='0.0.0.0', port=5175, debug=False)

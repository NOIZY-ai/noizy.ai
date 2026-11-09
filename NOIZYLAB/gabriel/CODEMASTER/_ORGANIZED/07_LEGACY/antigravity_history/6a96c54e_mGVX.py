#!/usr/bin/env python3
"""
turbo_bridge.py
The Crystal Smooth Link between Python (Brain) and Unity (Body).
"""
import sys
import json
import logging
from flask import Flask, request, jsonify
from pathlib import Path

# Import MemCell V2
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
try:
    from MemCell import MemCell
    mc = MemCell()
except ImportError:
    mc = None

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Quiet mode for speed

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "mode": "god_mode"})

@app.route('/api/initialize', methods=['POST'])
def initialize():
    data = request.json
    if mc:
        mc.track("initialize", "gabriel_avatar", data)
    return jsonify({"status": "initialized", "vibe": "aligned"})

@app.route('/api/context', methods=['POST'])
def update_context():
    data = request.json
    ctx = data.get("context", {})
    if mc:
        # High frequency update - keep log minimal
        # Only log if emotion changed significantly? 
        # For now, just logging to memory.
        pass 
    return jsonify({"status": "ack"})

@app.route('/api/interact', methods=['POST'])
def interact():
    data = request.json
    user_text = data.get("text", "")
    
    # FUTURE: Connect to LLM here.
    # For now, return a placeholder "God Mode" response.
    
    response = {
        "response_text": f"I heard: {user_text}. My neural core is active.",
        "emotion": "confident",
        "voice_file": "", # TTS would go here
        "sentiment_analysis": {"score": 0.9, "label": "positive"}
    }
    
    if mc:
        mc.track("interaction", "user", {"input": user_text, "response": response})
        
    return jsonify(response)

if __name__ == "__main__":
    print("⚡ TURBO BRIDGE: ACT II STARTING...")
    print("🔌 Listening on port 8000...")
    # Threaded=True for concurrent requests (Unity limitation avoidance)
    app.run(host='0.0.0.0', port=8000, threaded=True)

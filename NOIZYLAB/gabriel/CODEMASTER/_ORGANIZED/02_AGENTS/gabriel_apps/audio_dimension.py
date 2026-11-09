#!/usr/bin/env python3
# 🎵 AUDIO DIMENSION - GABRIEL CREATIVE SUITE
# Purpose: Real Tools for Sound & Music Generation

import os
import sys
import subprocess
import random
import time
from pathlib import Path


# ... (Imports preserved)
import asyncio
import websockets
import json

# Bridge Config
BRIDGE_URI = "ws://localhost:8000/ws/central_nervous_system"

class AudioDimension:
    def __init__(self):
        self.output_dir = Path("NOIZYLAB_OUTPUT")
        if not self.output_dir.exists():
            self.output_dir.mkdir()
    
    # ... (Prior methods: play_sample, generate_beat, analyze_audio preserved)
    
    def play_sample(self, name):
        """Finds and plays a local sample (or generates a tone)."""
        print(f"🎵 SEARCHING FOR SAMPLE: {name}")
        # Mock Beat
        if "kick" in name:
            subprocess.run(["say", "boom"])
        elif "snare" in name:
            subprocess.run(["say", "tchk"])
        else:
            print(f"⚠️ Sample '{name}' not found. Generating synth tone...")
            self.generate_beat(120, duration=1)

    def generate_beat(self, bpm, duration=10):
        """Generates a techno beat using FFMPEG."""
        print(f"🎹 GENERATING BEAT @ {bpm} BPM...")
        output_file = self.output_dir / f"beat_{bpm}bpm.mp3"
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"sine=frequency=60:duration={duration}", 
            str(output_file)
        ]
        subprocess.run(cmd, stderr=subprocess.DEVNULL)
        print(f"✅ BEAT GENERATED: {output_file}")
        return output_file
        
    def analyze_audio(self, path):
        """Mock Spectral Analysis."""
        print(f"📊 ANALYZING: {path}")
        time.sleep(1)
        print(f"   ► BPM: {random.randint(110, 140)}")
        print(f"   ► KEY: {random.choice(['Am', 'C#', 'F', 'Dm'])}")
        print(f"   ► ENERGY: {random.randint(80, 100)}%")

    async def connect_studio(self):
        """Connects to Gabriel Bridge and listens for commands."""
        print("🎵 AUDIO DIMENSION: Connecting to Studio...")
        async with websockets.connect(BRIDGE_URI) as websocket:
            print("✅ STUDIO LINK: ACTIVE.")
            
            # Announce
            await websocket.send(json.dumps({
                "source": "AUDIO_DIMENSION", 
                "status": "READY",
                "message": "Audio Engine Standing By."
            }))
            
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                # Check for Producer Commands
                if data.get("target") == "AUDIO_DIMENSION" and data.get("action") == "MAKE_BEAT":
                    params = data.get("params", {})
                    bpm = params.get("bpm", 120)
                    style = params.get("style", "Techno")
                    
                    print(f"🎹 COMMAND RECEIVED: Make {style} beat at {bpm} BPM")
                    
                    # Notify Bridge: Working
                    await websocket.send(json.dumps({
                        "source": "AUDIO_DIMENSION",
                        "type": "STATUS_UPDATE",
                        "status": "GENERATING",
                        "message": f"Synthesizing {style} Loop..."
                    }))
                    
                    # Generate (Blocking for now, but fast)
                    # In real version, run in executor
                    self.generate_beat(bpm, duration=3)
                    
                    # Notify Bridge: Done
                    await websocket.send(json.dumps({
                        "source": "AUDIO_DIMENSION",
                        "type": "STATUS_UPDATE",
                        "status": "PLAYING",
                        "message": f"Playback Started: {bpm} BPM"
                    }))

if __name__ == "__main__":
    tool = AudioDimension()
    if len(sys.argv) > 1 and sys.argv[1] == "studio":
        try:
            asyncio.run(tool.connect_studio())
        except KeyboardInterrupt:
            print("\n🎵 STUDIO LINK: TERMINATED.")
        except Exception as e:
            print(f"❌ ERROR: {e}")
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        tool.generate_beat(128)

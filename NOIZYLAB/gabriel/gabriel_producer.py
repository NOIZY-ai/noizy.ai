#!/usr/bin/env python3
# 🎬 THE PRODUCER - GABRIEL CREATIVE INTELLIGENCE
# Role: Autonomous Creative Director
# Protocol: ZERO LATENCY WEBSOCKETS

import asyncio
import json
import random
import sys
import websockets
from pathlib import Path

# Bridge Configuration
BRIDGE_URI = "ws://localhost:8000/ws/central_nervous_system"

class GabrielProducer:
    def __init__(self):
        self.genres = ["Techno", "Ambient", "Drum & Bass", "Classical", "Glitch"]
        self.moods = ["Energetic", "Dark", "Ethereal", "Industrial"]
        
    async def connect_and_produce(self):
        print("🎬 PRODUCER: Connecting to Studio Bridge...")
        async with websockets.connect(BRIDGE_URI) as websocket:
            print("✅ PRODUCER: ONLINE & CONNECTED.")
            
            # Announce Self
            await websocket.send(json.dumps({
                "source": "PRODUCER",
                "status": "ONLINE",
                "message": "Creative Core Active. Scanning for inspiration."
            }))
            
            # Production Loop
            while True:
                # 1. Wait/Think (Simulated Creative Pause)
                await asyncio.sleep(8) 
                
                # 2. Generate Brief
                genre = random.choice(self.genres)
                mood = random.choice(self.moods)
                bpm = random.randint(70, 140)
                
                brief = {
                    "source": "PRODUCER",
                    "type": "CREATIVE_BRIEF",
                    "data": {
                        "genre": genre,
                        "mood": mood,
                        "bpm": bpm,
                        "message": f"Generating {mood} {genre} Track at {bpm} BPM."
                    }
                }
                
                print(f"💡 IDEA: {brief['data']['message']}")
                await websocket.send(json.dumps(brief))
                
                # 3. Trigger Audio Tool (Studio Command)
                command = {
                    "source": "PRODUCER",
                    "target": "AUDIO_DIMENSION",
                    "action": "MAKE_BEAT",
                    "params": {"bpm": bpm, "style": genre}
                }
                await websocket.send(json.dumps(command))
                
                # 4. Wait for production
                await asyncio.sleep(5)

if __name__ == "__main__":
    producer = GabrielProducer()
    try:
        asyncio.run(producer.connect_and_produce())
    except KeyboardInterrupt:
        print("\n🎬 PRODUCER: Session Ended.")
    except Exception as e:
        print(f"❌ PRODUCER ERROR: {e}")

#!/usr/bin/env python3
# 🌉 GABRIEL BRIDGE - CENTRAL NERVOUS SYSTEM
# Protocol: ZERO LATENCY WEBSOCKETS
# Purpose: Connect Brain, Voice, and Avatar in real-time.

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

# Allow CORS for Avatar (Browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔌 NEW CONNECTION: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ DISCONNECTED: {websocket.client}")

    async def broadcast(self, message: dict):
        """Send message to all connected clients (Avatar, Tools, etc)"""
        if not self.active_connections:
            return
            
        print(f"📡 BROADCAST: {message}")
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"⚠️ Broadcast Error: {e}")

manager = ConnectionManager()

@app.websocket("/ws/central_nervous_system")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Listen for messages from Clients (e.g. Brain or Tools)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Re-broadcast to everyone (Simple Bus)
            await manager.broadcast(message)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"⚠️ WS Error: {e}")
        manager.disconnect(websocket)

@app.get("/")
def read_root():
    return {"status": "GABRIEL BRIDGE ONLINE", "connections": len(manager.active_connections)}

# Standalone Runner
if __name__ == "__main__":
    print("🌉 STARTING GABRIEL BRIDGE (Port 8000)...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

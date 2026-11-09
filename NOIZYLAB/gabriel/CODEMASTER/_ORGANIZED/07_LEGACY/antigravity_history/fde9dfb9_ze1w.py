#!/usr/bin/env python3
"""
NOIZYLAB WEBRTC SIGNALING SERVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enables real peer-to-peer video calls between portal users
Uses WebSocket for signaling exchange

Port: 5181
"""

import asyncio
import json
import sys
import subprocess
from datetime import datetime
from typing import Dict, Set

# Install dependencies if needed
try:
    from aiohttp import web
    import aiohttp
except ImportError:
    print("Installing aiohttp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp", "--quiet"])
    from aiohttp import web
    import aiohttp

# ============================================================================
# CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """Manages WebRTC peer connections and signaling"""
    
    def __init__(self):
        self.rooms: Dict[str, Set[web.WebSocketResponse]] = {}
        self.peers: Dict[str, dict] = {}  # ws_id -> peer info
        
    def get_room(self, room_id: str) -> Set[web.WebSocketResponse]:
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        return self.rooms[room_id]
    
    async def join_room(self, room_id: str, ws: web.WebSocketResponse, peer_info: dict):
        room = self.get_room(room_id)
        
        # Notify existing peers
        for peer_ws in room:
            await peer_ws.send_json({
                'type': 'peer_joined',
                'peer_id': peer_info.get('peer_id'),
                'name': peer_info.get('name', 'Unknown')
            })
        
        room.add(ws)
        self.peers[id(ws)] = peer_info
        
        # Send room state to new peer
        await ws.send_json({
            'type': 'room_joined',
            'room_id': room_id,
            'peers': [self.peers.get(id(p), {}).get('peer_id') for p in room if p != ws]
        })
    
    async def leave_room(self, room_id: str, ws: web.WebSocketResponse):
        if room_id in self.rooms:
            self.rooms[room_id].discard(ws)
            peer_info = self.peers.pop(id(ws), {})
            
            # Notify remaining peers
            for peer_ws in self.rooms[room_id]:
                await peer_ws.send_json({
                    'type': 'peer_left',
                    'peer_id': peer_info.get('peer_id')
                })
            
            # Clean up empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]
    
    async def relay_signal(self, room_id: str, ws: web.WebSocketResponse, message: dict):
        """Relay WebRTC signaling (offer/answer/ICE candidates) to peers"""
        room = self.get_room(room_id)
        target_id = message.get('target')
        
        for peer_ws in room:
            if peer_ws != ws:
                peer_info = self.peers.get(id(peer_ws), {})
                if target_id is None or peer_info.get('peer_id') == target_id:
                    await peer_ws.send_json(message)

manager = ConnectionManager()

# ============================================================================
# WEBSOCKET HANDLER
# ============================================================================

async def websocket_handler(request):
    """Handle WebSocket connections for signaling"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    room_id = None
    peer_id = None
    
    print(f"[SIGNAL] New WebSocket connection")
    
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    msg_type = data.get('type')
                    
                    if msg_type == 'join':
                        room_id = data.get('room', 'default')
                        peer_id = data.get('peer_id', f"peer_{id(ws)}")
                        peer_info = {
                            'peer_id': peer_id,
                            'name': data.get('name', 'Unknown'),
                            'joined_at': datetime.now().isoformat()
                        }
                        await manager.join_room(room_id, ws, peer_info)
                        print(f"[SIGNAL] {peer_id} joined room {room_id}")
                        
                    elif msg_type in ('offer', 'answer', 'ice_candidate'):
                        if room_id:
                            data['from'] = peer_id
                            await manager.relay_signal(room_id, ws, data)
                            print(f"[SIGNAL] Relaying {msg_type} from {peer_id}")
                            
                    elif msg_type == 'leave':
                        if room_id:
                            await manager.leave_room(room_id, ws)
                            print(f"[SIGNAL] {peer_id} left room {room_id}")
                            
                except json.JSONDecodeError:
                    await ws.send_json({'type': 'error', 'message': 'Invalid JSON'})
                    
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f"[SIGNAL] WebSocket error: {ws.exception()}")
                
    finally:
        if room_id:
            await manager.leave_room(room_id, ws)
    
    return ws

# ============================================================================
# HTTP HANDLERS
# ============================================================================

async def handle_status(request):
    """Server status endpoint"""
    return web.json_response({
        'status': 'online',
        'service': 'NOIZYLAB WebRTC Signaling',
        'rooms': len(manager.rooms),
        'total_peers': sum(len(r) for r in manager.rooms.values()),
        'timestamp': datetime.now().isoformat()
    })

async def handle_rooms(request):
    """List active rooms"""
    rooms_info = {}
    for room_id, peers in manager.rooms.items():
        rooms_info[room_id] = {
            'peer_count': len(peers),
            'peers': [manager.peers.get(id(p), {}).get('name', 'Unknown') for p in peers]
        }
    return web.json_response(rooms_info)

# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

@web.middleware
async def cors_middleware(request, handler):
    if request.method == 'OPTIONS':
        return web.Response(headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        })
    
    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ============================================================================
# MAIN
# ============================================================================

async def main():
    app = web.Application(middlewares=[cors_middleware])
    
    # HTTP routes
    app.router.add_get('/status', handle_status)
    app.router.add_get('/rooms', handle_rooms)
    
    # WebSocket route
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/signal', websocket_handler)  # Alias
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5181)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║        NOIZYLAB WEBRTC SIGNALING SERVER - ONLINE             ║
╠══════════════════════════════════════════════════════════════╣
║  🎥 WebSocket:  ws://localhost:5181/ws                       ║
║  📡 Status:     http://localhost:5181/status                 ║
║  🏠 Rooms:      http://localhost:5181/rooms                  ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    await site.start()
    
    # Keep running
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    print("Starting WebRTC Signaling Server...")
    asyncio.run(main())

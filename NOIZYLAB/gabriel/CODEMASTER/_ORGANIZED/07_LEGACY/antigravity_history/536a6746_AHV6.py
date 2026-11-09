# 🤖 SYSTEM FILE: neural_link.py
# Purpose: Real-time WebSocket bridge between Python and WebGL Avatar
# Tech: aiohttp, AsyncIO

import asyncio
import threading
import json
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeuralLink")

class NeuralLink:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.router.add_get('/', self.handle_websocket)
        self.clients = set()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.active = False

    def start(self):
        """Starts the WebSocket server in a background thread."""
        if not self.active:
            self.active = True
            self.thread.start()
            logger.info(f"🧠 NEURAL LINK: Server starting on ws://{self.host}:{self.port}")

    def _run_server(self):
        asyncio.set_event_loop(self.loop)
        runner = web.AppRunner(self.app)
        self.loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, self.host, self.port)
        self.loop.run_until_complete(site.start())
        self.loop.run_forever()

    async def handle_websocket(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.clients.add(ws)
        logger.info("🧠 NEURAL LINK: New Synapse Connected.")
        
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    # Echo or process if needed
                    pass
                elif msg.type == web.WSMsgType.ERROR:
                    logger.error(f'ws connection closed with exception {ws.exception()}')
        finally:
            self.clients.remove(ws)
            logger.info("🧠 NEURAL LINK: Synapse Disconnected.")
        
        return ws

    def broadcast(self, event_type, data=None):
        """Send data to all connected clients (Thread-Safe)"""
        if not self.clients: return
        
        payload = json.dumps({"type": event_type, "data": data or {}})
        
        async def _send():
            to_remove = set()
            for ws in self.clients:
                try:
                    await ws.send_str(payload)
                except Exception:
                    to_remove.add(ws)
            for ws in to_remove:
                self.clients.discard(ws)
                
        asyncio.run_coroutine_threadsafe(_send(), self.loop)

# Singleton
_link_instance = None
def get_neural_link():
    global _link_instance
    if _link_instance is None:
        _link_instance = NeuralLink()
    return _link_instance

if __name__ == "__main__":
    # Test
    link = NeuralLink()
    link.start()
    print("Link active. Press Ctrl+C to stop.")
    try:
        while True:
            cmd = input("Command > ")
            link.broadcast("cmd", {"payload": cmd})
    except KeyboardInterrupt:
        pass

#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    UNIFIED API v1.0                                          ║
║                    GORUNFREE REST ENDPOINT                                   ║
║                                                                              ║
║  Single HTTP endpoint for all GABRIEL operations.                            ║
║  Deploy anywhere. Access everything. Zero latency.                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Any
from urllib.parse import urlparse, parse_qs
import threading


class GabrielAPIHandler(BaseHTTPRequestHandler):
    """HTTP handler for GABRIEL API"""
    
    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _read_body(self) -> dict:
        """Read and parse JSON body"""
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        try:
            return json.loads(body.decode())
        except:
            return {}
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self._send_json({})
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path)
        route = path.path
        
        if route == '/':
            self._send_json({
                "service": "GABRIEL API",
                "version": "1.0.0",
                "status": "ONLINE",
                "gorunfree": "x1000"
            })
        
        elif route == '/health':
            self._send_json({"status": "healthy"})
        
        elif route == '/status':
            from .turbo_dispatcher import dispatch
            result = dispatch("status")
            self._send_json(result)
        
        elif route == '/agents':
            from .agents import AGENT_PROMPTS, AGENT_INFO
            agents = [
                {"name": name, "info": AGENT_INFO.get(name, {})}
                for name in AGENT_PROMPTS.keys()
            ]
            self._send_json({"agents": agents})
        
        elif route == '/memcells':
            from .memcell import MemCellStore
            store = MemCellStore()
            cells = store.list_recent(20)
            self._send_json({"memcells": [c.__dict__ for c in cells]})
        
        elif route == '/graph':
            from .knowledge_graph import get_graph
            graph = get_graph()
            self._send_json({
                "entities": len(graph.entities),
                "relations": len(graph.relations)
            })
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path)
        route = path.path
        body = self._read_body()
        
        if route == '/ask':
            prompt = body.get('prompt', '')
            provider = body.get('provider', 'Claude')
            
            if not prompt:
                self._send_json({"error": "Missing prompt"}, 400)
                return
            
            from .turbo_dispatcher import dispatch
            result = dispatch("ask", prompt, provider)
            self._send_json(result)
        
        elif route == '/dream':
            prompt = body.get('prompt', '')
            providers = body.get('providers', ['Claude', 'Gemini'])
            
            if not prompt:
                self._send_json({"error": "Missing prompt"}, 400)
                return
            
            from .turbo_dispatcher import dispatch
            result = dispatch("dream", prompt, providers)
            self._send_json(result)
        
        elif route == '/flow':
            prompt = body.get('prompt', '')
            
            if not prompt:
                self._send_json({"error": "Missing prompt"}, 400)
                return
            
            from .turbo_dispatcher import dispatch
            result = dispatch("flow", prompt)
            self._send_json(result)
        
        elif route == '/dispatch':
            command = body.get('command', '')
            args = body.get('args', [])
            kwargs = body.get('kwargs', {})
            
            if not command:
                self._send_json({"error": "Missing command"}, 400)
                return
            
            from .turbo_dispatcher import dispatch
            result = dispatch(command, *args, **kwargs)
            self._send_json(result)
        
        elif route == '/memcell':
            content = body.get('content', '')
            tags = body.get('tags', [])
            
            if not content:
                self._send_json({"error": "Missing content"}, 400)
                return
            
            from .memcell import MemCell, MemCellStore
            cell = MemCell(content=content, tags=tags)
            store = MemCellStore()
            store.store(cell)
            self._send_json({"id": cell.id, "stored": True})
        
        elif route == '/graph/learn':
            text = body.get('text', '')
            
            if not text:
                self._send_json({"error": "Missing text"}, 400)
                return
            
            from .knowledge_graph import get_graph
            graph = get_graph()
            entities = graph.extract_and_add(text)
            self._send_json({
                "entities_added": len(entities),
                "total_entities": len(graph.entities)
            })
        
        elif route == '/slack':
            message = body.get('message', '')
            channel = body.get('channel', '#social')
            
            if not message:
                self._send_json({"error": "Missing message"}, 400)
                return
            
            from .slack_bridge import create_slack_bridge
            bridge = create_slack_bridge()
            result = bridge.send_message(message, channel)
            self._send_json(result)
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def log_message(self, format, *args):
        """Log requests"""
        print(f"[API] {args[0]}")


class GabrielAPI:
    """
    GABRIEL Unified API Server
    
    Single endpoint for all operations.
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8888):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
    
    def start(self, blocking: bool = True):
        """Start the API server"""
        self.server = HTTPServer((self.host, self.port), GabrielAPIHandler)
        
        print(f"🚀 GABRIEL API Server started on http://{self.host}:{self.port}")
        print()
        print("Endpoints:")
        print("  GET  /           - API info")
        print("  GET  /status     - System status")
        print("  GET  /agents     - List agents")
        print("  GET  /memcells   - List memcells")
        print("  GET  /graph      - Graph stats")
        print("  POST /ask        - Ask AI (prompt, provider)")
        print("  POST /dream      - Multi-AI dream (prompt, providers)")
        print("  POST /flow       - Full flow (prompt)")
        print("  POST /dispatch   - Run command (command, args)")
        print("  POST /memcell    - Store memcell (content, tags)")
        print("  POST /graph/learn - Learn entities (text)")
        print("  POST /slack      - Send to Slack (message, channel)")
        print()
        
        if blocking:
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.stop()
        else:
            self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self._thread.start()
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            print("🛑 GABRIEL API stopped")


def create_api(port: int = 8888) -> GabrielAPI:
    """Create API server"""
    return GabrielAPI(port=port)


__all__ = ['GabrielAPI', 'GabrielAPIHandler', 'create_api']


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              GABRIEL UNIFIED API v1.0                        ║")
    print("║              GORUNFREE REST ENDPOINT                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    api = create_api(8888)
    api.start()

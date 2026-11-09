#!/usr/bin/env python3
"""
REAL-TIME MONITORING DASHBOARD - MC96ECOUNIVERSE Live Monitoring
WebSocket-based real-time volume and system monitoring
"""

import asyncio
import json
import websockets
from datetime import datetime
from typing import Dict, Set
from pathlib import Path

try:
    from aiohttp import web
    from aiohttp.web_runner import GracefulExit
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call(["pip3", "install", "aiohttp"])
    from aiohttp import web

from volume_monitor_UPGRADED import VolumeMonitorUpgraded

class RealtimeMonitor:
    """Real-time monitoring server"""
    
    def __init__(self, port: int = 8888):
        self.port = port
        self.monitor = VolumeMonitorUpgraded()
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.running = False
        
    async def monitor_loop(self):
        """Continuous monitoring loop"""
        while self.running:
            try:
                # Scan volumes
                volumes = await self.monitor.scan_volumes_async()
                
                # Get critical volumes
                critical = self.monitor.get_critical_volumes()
                
                # Get network volumes
                network = self.monitor.get_network_volumes()
                
                # Create update message
                update = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "volume_update",
                    "data": {
                        "volumes": {
                            name: {
                                "mount": info["mount"],
                                "percent": info["percent"],
                                "status": info["status"],
                                "available": info["available"],
                                "is_network": info.get("is_network", False)
                            }
                            for name, info in volumes.items()
                        },
                        "critical_count": len(critical),
                        "critical_volumes": critical,
                        "network_count": len(network),
                        "total_volumes": len(volumes)
                    }
                }
                
                # Broadcast to all clients
                if self.clients:
                    message = json.dumps(update)
                    disconnected = set()
                    for client in self.clients:
                        try:
                            await client.send(message)
                        except:
                            disconnected.add(client)
                    
                    # Remove disconnected clients
                    self.clients -= disconnected
                
                # Wait before next update
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"Monitor loop error: {e}")
                await asyncio.sleep(5)
    
    async def websocket_handler(self, websocket, path):
        """Handle WebSocket connections"""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
        try:
            # Send initial data
            volumes = await self.monitor.scan_volumes_async()
            initial_data = {
                "timestamp": datetime.now().isoformat(),
                "type": "initial",
                "data": {
                    "volumes": {
                        name: {
                            "mount": info["mount"],
                            "percent": info["percent"],
                            "status": info["status"],
                            "available": info["available"]
                        }
                        for name, info in volumes.items()
                    },
                    "total_volumes": len(volumes)
                }
            }
            await websocket.send(json.dumps(initial_data))
            
            # Keep connection alive
            async for message in websocket:
                # Echo back or handle commands
                if message == "ping":
                    await websocket.send(json.dumps({"type": "pong"}))
                elif message.startswith("command:"):
                    # Handle commands
                    await websocket.send(json.dumps({
                        "type": "command_response",
                        "message": "Command received"
                    }))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def start(self):
        """Start monitoring server"""
        self.running = True
        
        # Start monitor loop
        monitor_task = asyncio.create_task(self.monitor_loop())
        
        # Start WebSocket server
        server = await websockets.serve(
            self.websocket_handler,
            "localhost",
            self.port
        )
        
        print(f"╔══════════════════════════════════════════════════════════════╗")
        print(f"║       REAL-TIME MC96ECOUNIVERSE MONITORING                   ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🌐 WebSocket server running on ws://localhost:{self.port}")
        print(f"📊 Monitoring all volumes...")
        print(f"🔄 Update interval: 5 seconds")
        print(f"\nPress Ctrl+C to stop\n")
        
        try:
            await server.wait_closed()
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.running = False
            monitor_task.cancel()
            server.close()
            await server.wait_closed()

async def main():
    """Start real-time monitor"""
    monitor = RealtimeMonitor(port=8888)
    await monitor.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


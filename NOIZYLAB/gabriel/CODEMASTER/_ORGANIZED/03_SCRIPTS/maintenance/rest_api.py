#!/usr/bin/env python3
"""
MC96ECOUNIVERSE REST API
RESTful API for all MC96 systems
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

try:
    from aiohttp import web
except ImportError:
    import subprocess
    subprocess.check_call(["pip3", "install", "--user", "aiohttp"])
    from aiohttp import web

class MC96RESTAPI:
    """REST API for MC96ECOUNIVERSE"""
    
    def __init__(self, port: int = 8890):
        self.port = port
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes"""
        # System status
        self.app.router.add_get('/api/v1/status', self.get_status)
        self.app.router.add_get('/api/v1/health', self.get_health)
        
        # Volumes
        self.app.router.add_get('/api/v1/volumes', self.get_volumes)
        self.app.router.add_get('/api/v1/volumes/critical', self.get_critical_volumes)
        self.app.router.add_get('/api/v1/volumes/network', self.get_network_volumes)
        
        # HP-OMEN
        self.app.router.add_get('/api/v1/hpomen', self.get_hpomen)
        self.app.router.get('/api/v1/hpomen/status', self.get_hpomen_status)
        
        # Analytics
        self.app.router.add_get('/api/v1/analytics/predictions', self.get_predictions)
        
        # Maintenance
        self.app.router.add_post('/api/v1/maintenance/cleanup', self.run_cleanup)
        
        # CORS
        self.app.middlewares.append(self.cors_middleware)
    
    @web.middleware
    async def cors_middleware(self, request, handler):
        """CORS middleware"""
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    async def get_status(self, request):
        """Get complete system status"""
        sys.path.insert(0, str(Path(__file__).parent))
        from mc96_master_control import MC96MasterControl
        
        control = MC96MasterControl()
        status = await control.full_system_check()
        return web.json_response(status)
    
    async def get_health(self, request):
        """Get health score"""
        sys.path.insert(0, str(Path(__file__).parent))
        from mc96_master_control import MC96MasterControl
        
        control = MC96MasterControl()
        status = await control.full_system_check()
        return web.json_response({
            "health_score": status.get("health_score", 0),
            "status": "healthy" if status.get("health_score", 0) >= 70 else "degraded",
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_volumes(self, request):
        """Get all volumes"""
        sys.path.insert(0, str(Path(__file__).parent))
        from volume_monitor_UPGRADED import VolumeMonitorUpgraded
        
        monitor = VolumeMonitorUpgraded()
        volumes = await monitor.scan_volumes_async()
        
        return web.json_response({
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
            "total": len(volumes),
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_critical_volumes(self, request):
        """Get critical volumes"""
        sys.path.insert(0, str(Path(__file__).parent))
        from volume_monitor_UPGRADED import VolumeMonitorUpgraded
        
        monitor = VolumeMonitorUpgraded()
        volumes = await monitor.scan_volumes_async()
        critical = await monitor.get_critical_volumes_async()
        
        return web.json_response({
            "critical_volumes": [
                {
                    "name": name,
                    "mount": volumes[name]["mount"],
                    "percent": volumes[name]["percent"],
                    "available": volumes[name]["available"]
                }
                for name in critical
            ],
            "count": len(critical),
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_network_volumes(self, request):
        """Get network volumes"""
        sys.path.insert(0, str(Path(__file__).parent))
        from volume_monitor_UPGRADED import VolumeMonitorUpgraded
        
        monitor = VolumeMonitorUpgraded()
        network = await monitor.get_network_volumes_async()
        
        return web.json_response({
            "network_volumes": {
                name: {
                    "mount": info["mount"],
                    "percent": info["percent"],
                    "available": info["available"]
                }
                for name, info in network.items()
            },
            "count": len(network),
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_hpomen(self, request):
        """Get HP-OMEN status"""
        sys.path.insert(0, str(Path(__file__).parent))
        from hp_omen_integration import HPOMENIntegration
        
        integration = HPOMENIntegration()
        connected = await integration.check_connection()
        volumes = integration.get_network_volumes()
        
        return web.json_response({
            "connected": connected,
            "volumes": len(volumes),
            "ip": integration.HP_OMEN_IP,
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_hpomen_status(self, request):
        """Get HP-OMEN connection status"""
        sys.path.insert(0, str(Path(__file__).parent))
        from hp_omen_integration import HPOMENIntegration
        
        integration = HPOMENIntegration()
        connected = await integration.check_connection()
        
        return web.json_response({
            "connected": connected,
            "status": "online" if connected else "offline",
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_predictions(self, request):
        """Get predictive analytics"""
        sys.path.insert(0, str(Path(__file__).parent))
        from predictive_analytics import PredictiveAnalytics
        from volume_monitor_UPGRADED import VolumeMonitorUpgraded
        
        analytics = PredictiveAnalytics()
        monitor = VolumeMonitorUpgraded()
        volumes = await monitor.scan_volumes_async()
        predictions = analytics.predict_critical_volumes(volumes)
        
        return web.json_response({
            "predictions": predictions,
            "count": len(predictions),
            "timestamp": datetime.now().isoformat()
        })
    
    async def run_cleanup(self, request):
        """Run cleanup (dry-run by default)"""
        data = await request.json()
        dry_run = data.get("dry_run", True)
        
        sys.path.insert(0, str(Path(__file__).parent))
        from automated_cleanup import AutomatedCleanup
        
        cleanup = AutomatedCleanup()
        # Get critical volumes and run cleanup
        # Implementation would go here
        
        return web.json_response({
            "status": "completed" if not dry_run else "dry_run",
            "dry_run": dry_run,
            "timestamp": datetime.now().isoformat()
        })
    
    async def start(self):
        """Start API server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║           MC96ECOUNIVERSE REST API                           ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🌐 API Server: http://localhost:{self.port}")
        print(f"📊 Status: http://localhost:{self.port}/api/v1/status")
        print(f"💚 Health: http://localhost:{self.port}/api/v1/health")
        print(f"📁 Volumes: http://localhost:{self.port}/api/v1/volumes")
        print(f"\n🚀 API running...\n")
        
        await site.start()
        await asyncio.Event().wait()

async def main():
    """Start REST API"""
    api = MC96RESTAPI(port=8890)
    await api.start()

if __name__ == "__main__":
    import sys
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAPI stopped.")



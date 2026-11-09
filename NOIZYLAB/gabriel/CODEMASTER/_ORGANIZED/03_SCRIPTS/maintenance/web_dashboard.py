#!/usr/bin/env python3
"""
MC96ECOUNIVERSE WEB DASHBOARD
Beautiful real-time web interface for all systems
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

try:
    from aiohttp import web
    from aiohttp.web_runner import GracefulExit
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call(["pip3", "install", "--user", "aiohttp"])
    from aiohttp import web

from mc96_master_control import MC96MasterControl
from volume_monitor_UPGRADED import VolumeMonitorUpgraded

class WebDashboard:
    """Web dashboard for MC96ECOUNIVERSE"""
    
    def __init__(self, port: int = 8889):
        self.port = port
        self.control = MC96MasterControl()
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup web routes"""
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/api/status', self.api_status)
        self.app.router.add_get('/api/volumes', self.api_volumes)
        self.app.router.add_get('/api/health', self.api_health)
        self.app.router.add_get('/api/hpomen', self.api_hpomen)
        self.app.router.add_static('/static', Path(__file__).parent / 'static')
    
    async def index(self, request):
        """Main dashboard page"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>MC96ECOUNIVERSE Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .card h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .stat:last-child { border-bottom: none; }
        .stat-label { font-weight: 600; }
        .stat-value { font-weight: 300; }
        .health-score {
            font-size: 4em;
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
        }
        .critical { color: #ff6b6b; }
        .warning { color: #ffd93d; }
        .good { color: #6bcf7f; }
        .refresh-btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 10px;
            color: #fff;
            font-size: 1.1em;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s;
        }
        .refresh-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        .timestamp {
            text-align: center;
            opacity: 0.8;
            margin-top: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MC96ECOUNIVERSE DASHBOARD</h1>
        <div id="dashboard" class="dashboard"></div>
        <button class="refresh-btn" onclick="loadDashboard()">🔄 Refresh</button>
        <div class="timestamp" id="timestamp"></div>
    </div>
    
    <script>
        async function loadDashboard() {
            try {
                const [status, volumes, health, hpomen] = await Promise.all([
                    fetch('/api/status').then(r => r.json()),
                    fetch('/api/volumes').then(r => r.json()),
                    fetch('/api/health').then(r => r.json()),
                    fetch('/api/hpomen').then(r => r.json())
                ]);
                
                const healthScore = status.health_score || 0;
                const scoreClass = healthScore >= 80 ? 'good' : healthScore >= 60 ? 'warning' : 'critical';
                
                document.getElementById('dashboard').innerHTML = `
                    <div class="card">
                        <h2>💚 Health Score</h2>
                        <div class="health-score ${scoreClass}">${healthScore}/100</div>
                        <div class="stat">
                            <span class="stat-label">Status:</span>
                            <span class="stat-value">${status.volumes?.status || 'UNKNOWN'}</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>📁 Volumes</h2>
                        <div class="stat">
                            <span class="stat-label">Total:</span>
                            <span class="stat-value">${volumes.total || 0}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Critical:</span>
                            <span class="stat-value ${volumes.critical > 0 ? 'critical' : 'good'}">${volumes.critical || 0}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Network:</span>
                            <span class="stat-value">${volumes.network || 0}</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>🖥️ HP-OMEN</h2>
                        <div class="stat">
                            <span class="stat-label">Connected:</span>
                            <span class="stat-value ${hpomen.connected ? 'good' : 'critical'}">${hpomen.connected ? '✅' : '❌'}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Volumes:</span>
                            <span class="stat-value">${hpomen.volumes || 0}</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>⚡ Performance</h2>
                        <div class="stat">
                            <span class="stat-label">Disk I/O:</span>
                            <span class="stat-value">${health.disk_io_ms || 'N/A'}ms</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Status:</span>
                            <span class="stat-value ${health.status === 'OK' ? 'good' : 'warning'}">${health.status || 'UNKNOWN'}</span>
                        </div>
                    </div>
                `;
                
                document.getElementById('timestamp').textContent = `Last updated: ${new Date().toLocaleString()}`;
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        // Load on page load
        loadDashboard();
        
        // Auto-refresh every 30 seconds
        setInterval(loadDashboard, 30000);
    </script>
</body>
</html>
        """
        return web.Response(text=html, content_type='text/html')
    
    async def api_status(self, request):
        """API endpoint for system status"""
        results = await self.control.full_system_check()
        return web.json_response(results)
    
    async def api_volumes(self, request):
        """API endpoint for volumes"""
        monitor = VolumeMonitorUpgraded()
        volumes = await monitor.scan_volumes_async()
        critical = await monitor.get_critical_volumes_async()
        network = await monitor.get_network_volumes_async()
        
        return web.json_response({
            "total": len(volumes),
            "critical": len(critical),
            "network": len(network),
            "critical_volumes": critical
        })
    
    async def api_health(self, request):
        """API endpoint for health metrics"""
        results = await self.control.full_system_check()
        return web.json_response({
            "health_score": results.get("health_score", 0),
            "disk_io_ms": results.get("performance", {}).get("disk_io_ms", 0),
            "status": results.get("performance", {}).get("status", "UNKNOWN")
        })
    
    async def api_hpomen(self, request):
        """API endpoint for HP-OMEN status"""
        results = await self.control.full_system_check()
        hpomen = results.get("hpomen", {})
        return web.json_response({
            "connected": hpomen.get("connected", False),
            "volumes": hpomen.get("volumes", 0),
            "status": hpomen.get("status", "UNKNOWN")
        })
    
    async def start(self):
        """Start web server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║         MC96ECOUNIVERSE WEB DASHBOARD                        ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🌐 Dashboard: http://localhost:{self.port}")
        print(f"📊 API: http://localhost:{self.port}/api/status")
        print(f"\n🚀 Server running...\n")
        
        await site.start()
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            await runner.cleanup()

async def main():
    """Start web dashboard"""
    dashboard = WebDashboard(port=8889)
    await dashboard.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDashboard stopped.")



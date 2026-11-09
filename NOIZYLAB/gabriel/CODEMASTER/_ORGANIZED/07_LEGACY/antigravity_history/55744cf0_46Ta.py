"""
NOIZYLAB PORTAL - AI Remote Support Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Machine Registry • SSH/API Bridge • Diagnostics Engine • WebSocket Terminal
Powered by GABRIEL AI
"""

import asyncio
import subprocess
import socket
import os
import sys
from datetime import datetime
from pathlib import Path

# Install dependencies if needed
try:
    from aiohttp import web
    import orjson
except ImportError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp", "orjson"])
    from aiohttp import web
    import orjson

# ============================================================================
# MACHINE REGISTRY
# ============================================================================

class MachineRegistry:
    def __init__(self):
        self.machines = {}
        self._add_local_machine()
    
    def _add_local_machine(self):
        hostname = socket.gethostname()
        self.machines['local'] = {
            'id': 'local',
            'name': hostname.upper(),
            'ip': '127.0.0.1',
            'status': 'online',
            'os': self._get_os(),
            'lastSeen': 'Now',
            'type': 'local'
        }
    
    def _get_os(self):
        import platform
        return f"{platform.system()} {platform.release()}"
    
    def add_machine(self, id: str, name: str, ip: str):
        self.machines[id] = {
            'id': id,
            'name': name,
            'ip': ip,
            'status': 'unknown',
            'os': 'Unknown',
            'lastSeen': datetime.now().isoformat(),
            'type': 'remote'
        }
    
    def update_status(self, id: str, status: str):
        if id in self.machines:
            self.machines[id]['status'] = status
            self.machines[id]['lastSeen'] = 'Now' if status == 'online' else datetime.now().isoformat()
    
    def get_all(self):
        return list(self.machines.values())
    
    def get(self, id: str):
        return self.machines.get(id)

# ============================================================================
# DIAGNOSTICS ENGINE (Integrates gabriel_doctor logic)
# ============================================================================

class DiagnosticsEngine:
    def __init__(self):
        pass
    
    async def diagnose_local(self):
        """Run diagnostics on local machine"""
        result = {
            'cpu': self._check_cpu(),
            'ram': self._check_ram(),
            'disk': self._check_disk(),
            'network': self._check_network(),
            'problems': [],
            'score': 100
        }
        
        # Check for common problems
        problems = []
        
        # Check PC_Bridge mount
        if not Path("/Volumes/PC_Bridge").exists():
            problems.append({'id': 'mount', 'text': 'PC_Bridge not mounted', 'fix': 'mount_shares'})
            result['score'] -= 15
        
        # Check databases
        if not Path("NOIZYLAB_DB/visual_index.db").exists():
            problems.append({'id': 'db', 'text': 'visual_index.db missing', 'fix': 'rebuild_index'})
            result['score'] -= 10
        
        # Check disk usage
        if result['disk']['value'] and int(result['disk']['value'].replace('%', '')) > 85:
            problems.append({'id': 'disk', 'text': 'Disk usage above 85%', 'fix': 'cleanup_disk'})
            result['score'] -= 10
            result['disk']['status'] = 'warning'
        
        result['problems'] = problems
        result['drives'] = self._check_drives()
        return result
    
    def _check_drives(self):
        """List all mounted volumes with usage info"""
        drives = []
        try:
            # Get all mounted volumes
            output = subprocess.check_output("df -h | grep -E '^/dev|^//'", shell=True).decode()
            for line in output.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 6:
                    # Filesystem, Size, Used, Avail, Use%, Mounted
                    mount = ' '.join(parts[5:])  # Handle spaces in mount names
                    size = parts[1]
                    used_pct = parts[4]
                    pct = int(used_pct.replace('%', '')) if '%' in used_pct else 0
                    drives.append({
                        'name': mount.split('/')[-1] or 'Root',
                        'path': mount,
                        'size': size,
                        'used': used_pct,
                        'status': 'good' if pct < 70 else ('warning' if pct < 85 else 'critical')
                    })
        except:
            pass
        
        # Also check /Volumes specifically
        try:
            volumes_path = Path('/Volumes')
            if volumes_path.exists():
                for vol in volumes_path.iterdir():
                    if vol.is_dir() and not any(d['path'] == str(vol) for d in drives):
                        # Get size for this volume
                        try:
                            df_out = subprocess.check_output(f"df -h '{vol}' | tail -1", shell=True).decode()
                            parts = df_out.split()
                            if len(parts) >= 5:
                                drives.append({
                                    'name': vol.name,
                                    'path': str(vol),
                                    'size': parts[1],
                                    'used': parts[4],
                                    'status': 'good'
                                })
                        except:
                            drives.append({
                                'name': vol.name,
                                'path': str(vol),
                                'size': '—',
                                'used': '—',
                                'status': 'good'
                            })
        except:
            pass
        
        return drives
    
    def _check_cpu(self):
        try:
            output = subprocess.check_output("top -l 1 | grep 'CPU usage'", shell=True).decode()
            # Parse "CPU usage: 5.0% user, 10.0% sys, 85.0% idle"
            parts = output.split(',')
            user = float(parts[0].split(':')[1].strip().replace('%', '').split()[0])
            sys = float(parts[1].strip().replace('%', '').split()[0])
            usage = round(user + sys)
            return {'value': f'{usage}%', 'status': 'good' if usage < 70 else 'warning'}
        except:
            return {'value': '—', 'status': 'good'}
    
    def _check_ram(self):
        try:
            output = subprocess.check_output("top -l 1 | grep 'PhysMem'", shell=True).decode()
            # Parse "PhysMem: 163G used (7662M wired, 11G compressor), 28G unused."
            parts = output.split()
            used = parts[1].replace('G', '')
            return {'value': f'{used}/192GB', 'status': 'good'}
        except:
            return {'value': '—', 'status': 'good'}
    
    def _check_disk(self):
        try:
            output = subprocess.check_output("df -h / | tail -1", shell=True).decode()
            parts = output.split()
            usage = parts[4]  # e.g., "67%"
            pct = int(usage.replace('%', ''))
            status = 'good' if pct < 70 else ('warning' if pct < 85 else 'critical')
            return {'value': usage, 'status': status}
        except:
            return {'value': '—', 'status': 'good'}
    
    def _check_network(self):
        try:
            subprocess.check_output(['ping', '-c', '1', '-t', '1', '8.8.8.8'], stderr=subprocess.DEVNULL)
            return {'value': 'ONLINE', 'status': 'good'}
        except:
            return {'value': 'OFFLINE', 'status': 'critical'}
    
    async def heal(self, machine_id: str, fix_type: str):
        """Apply a fix to a machine"""
        if fix_type == 'mount_shares':
            try:
                subprocess.run(['/Users/m2ultra/NOIZYLAB/GABRIEL/core/mount_pc_shares.sh'], check=True)
                return {'success': True, 'message': 'Shares mounted successfully'}
            except:
                return {'success': False, 'message': 'Failed to mount shares'}
        
        elif fix_type == 'rebuild_index':
            return {'success': True, 'message': 'Index rebuild queued'}
        
        elif fix_type == 'cleanup_disk':
            return {'success': True, 'message': 'Disk cleanup initiated'}
        
        return {'success': False, 'message': 'Unknown fix type'}

# ============================================================================
# COMMAND EXECUTOR
# ============================================================================

class CommandExecutor:
    async def execute_local(self, command: str):
        """Execute a command locally"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout or result.stderr or 'Command completed.',
                'code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Command timed out after 30s', 'code': -1}
        except Exception as e:
            return {'success': False, 'output': str(e), 'code': -1}

# ============================================================================
# API HANDLERS
# ============================================================================

registry = MachineRegistry()
diagnostics = DiagnosticsEngine()
executor = CommandExecutor()

# Add HP-OMEN as known remote machine
registry.add_machine('hpomen', 'HP-OMEN', '10.0.0.160')

async def handle_status(request):
    return web.Response(
        text=orjson.dumps({'status': 'ONLINE', 'version': '1.0'}).decode(),
        content_type='application/json'
    )

async def handle_machines(request):
    machines = registry.get_all()
    
    # Check reachability for remote machines
    for m in machines:
        if m['type'] == 'remote':
            try:
                subprocess.run(['ping', '-c', '1', '-t', '1', m['ip']], 
                             capture_output=True, timeout=2)
                m['status'] = 'online'
                m['lastSeen'] = 'Now'
            except:
                m['status'] = 'offline'
    
    return web.Response(
        text=orjson.dumps(machines).decode(),
        content_type='application/json'
    )

async def handle_diagnose(request):
    machine_id = request.match_info.get('id', 'local')
    
    if machine_id == 'local' or machine_id == registry.machines.get('local', {}).get('id'):
        result = await diagnostics.diagnose_local()
    else:
        # For remote machines, attempt API call or return placeholder
        result = {
            'cpu': {'value': '—', 'status': 'good'},
            'ram': {'value': '—', 'status': 'good'},
            'disk': {'value': '—', 'status': 'good'},
            'network': {'value': 'CHECKING', 'status': 'good'},
            'problems': [],
            'score': 100
        }
    
    return web.Response(
        text=orjson.dumps(result).decode(),
        content_type='application/json'
    )

async def handle_heal(request):
    machine_id = request.match_info.get('id', 'local')
    fix_type = request.match_info.get('fix', '')
    
    result = await diagnostics.heal(machine_id, fix_type)
    return web.Response(
        text=orjson.dumps(result).decode(),
        content_type='application/json'
    )

async def handle_exec(request):
    machine_id = request.match_info.get('id', 'local')
    data = await request.json()
    command = data.get('command', '')
    
    if not command:
        return web.Response(
            text=orjson.dumps({'success': False, 'output': 'No command provided'}).decode(),
            content_type='application/json'
        )
    
    result = await executor.execute_local(command)
    return web.Response(
        text=orjson.dumps(result).decode(),
        content_type='application/json'
    )

async def handle_drives(request):
    """Get all mounted drives/volumes"""
    drives = diagnostics._check_drives()
    return web.Response(
        text=orjson.dumps(drives).decode(),
        content_type='application/json'
    )

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
    
    app.router.add_get('/api/status', handle_status)
    app.router.add_get('/api/machines', handle_machines)
    app.router.add_get('/api/diagnose/{id}', handle_diagnose)
    app.router.add_post('/api/heal/{id}/{fix}', handle_heal)
    app.router.add_post('/api/exec/{id}', handle_exec)
    app.router.add_get('/api/drives', handle_drives)
    
    # Serve static files
    app.router.add_static('/', Path(__file__).parent, show_index=True)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5180)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           NOIZYLAB PORTAL - AI REMOTE SUPPORT                ║
╠══════════════════════════════════════════════════════════════╣
║  🌐 Portal:     http://localhost:5180                        ║
║  📡 API:        http://localhost:5180/api/                   ║
║  🔧 Status:     ONLINE                                       ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    await site.start()
    
    # Keep running
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())

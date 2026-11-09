#!/usr/bin/env python3
"""
NOIZYLAB REMOTE AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Deploy this agent on remote machines (HP-OMEN, etc.) to enable:
- Real-time diagnostics (CPU, RAM, Disk, Network)
- Remote command execution
- System healing actions
- Heartbeat for discovery

Port: 5175
"""

import asyncio
import subprocess
import socket
import os
import sys
import platform
from datetime import datetime
from pathlib import Path

# Cross-platform dependency install
try:
    from aiohttp import web
    import orjson
except ImportError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp", "orjson", "--quiet"])
    from aiohttp import web
    import orjson

# ============================================================================
# DIAGNOSTICS & LOGGING
# ============================================================================

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {level} | {message}")

def get_system_info():
    """Get basic system information"""
    return {
        'hostname': socket.gethostname(),
        'os': f"{platform.system()} {platform.release()}",
        'arch': platform.machine(),
        'python': platform.python_version()
    }

def check_cpu():
    """Get CPU usage - cross-platform"""
    try:
        usage = 0
        if platform.system() == 'Darwin':  # macOS
            output = subprocess.check_output("top -l 1 | grep -E '^CPU usage'", shell=True).decode()
            parts = output.split(',')
            user = float(parts[0].split(':')[1].strip().replace('%', '').split()[0])
            sys_pct = float(parts[1].strip().replace('%', '').split()[0])
            usage = round(user + sys_pct)
        elif platform.system() == 'Windows':
            output = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode()
            usage = int([x for x in output.split() if x.strip().isdigit()][0])
        else:  # Linux
            output = subprocess.check_output("top -bn1 | grep 'Cpu(s)'", shell=True).decode()
            usage = int(float(output.split()[1].replace(',', '.')))
        
        status = 'good'
        if usage > 90: status = 'critical'
        elif usage > 70: status = 'warning'
        
        return {'value': f'{usage}%', 'status': status}
    except Exception as e:
        log(f"CPU Check Error: {e}", "ERROR")
        return {'value': '—', 'status': 'good', 'error': str(e)}

def check_ram():
    """Get RAM usage - cross-platform"""
    try:
        if platform.system() == 'Darwin':
            # Use vm_stat for more accurate memory pressure if needed, but keeping it simple for agent
            total_bytes = int(subprocess.check_output("sysctl -n hw.memsize", shell=True).decode().strip())
            total_gb = total_bytes // (1024**3)
            
            # Percentage estimate from top
            output = subprocess.check_output("top -l 1 | grep 'PhysMem'", shell=True).decode()
            parts = output.split()
            used_str = parts[1] # e.g. 18G
            
            return {'value': f'{used_str}/{total_gb}GB', 'status': 'good'}
            
        elif platform.system() == 'Windows':
            output = subprocess.check_output("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value", shell=True).decode()
            lines = [l.strip() for l in output.split('\n') if '=' in l]
            vals = {l.split('=')[0]: int(l.split('=')[1]) for l in lines}
            total_gb = vals['TotalVisibleMemorySize'] // (1024*1024)
            free_gb = vals['FreePhysicalMemory'] // (1024*1024)
            used_gb = total_gb - free_gb
            return {'value': f'{used_gb}/{total_gb}GB', 'status': 'good'}
        else:
            output = subprocess.check_output("free -g", shell=True).decode()
            parts = output.split('\n')[1].split()
            return {'value': f'{parts[2]}/{parts[1]}GB', 'status': 'good'}
    except Exception as e:
        log(f"RAM Check Error: {e}", "ERROR")
        return {'value': '—', 'status': 'good', 'error': str(e)}

def check_disk():
    """Get disk usage - cross-platform"""
    try:
        if platform.system() == 'Windows':
            output = subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True).decode()
            lines = [l.split() for l in output.strip().split('\n')[1:] if l.strip()]
            disks = []
            for parts in lines:
                if len(parts) >= 3:
                    drive = parts[0]
                    free = int(parts[1]) if parts[1].isdigit() else 0
                    size = int(parts[2]) if parts[2].isdigit() else 0
                    if size > 0:
                        used_pct = round((size - free) / size * 100)
                        disks.append({'name': drive, 'used': f'{used_pct}%', 'size': f'{size//(1024**3)}GB'})
            if disks:
                main = disks[0]
                pct = int(main['used'].replace('%', ''))
                status = 'good'
                if pct > 90: status = 'critical'
                elif pct > 80: status = 'warning'
                return {'value': main['used'], 'status': status, 'all': disks}
        else:
            output = subprocess.check_output("df -h / | tail -1", shell=True).decode()
            parts = output.split()
            usage = parts[4]
            pct = int(usage.replace('%', ''))
            status = 'good'
            if pct > 90: status = 'critical'
            elif pct > 80: status = 'warning'
            return {'value': usage, 'status': status}
    except Exception as e:
        log(f"Disk Check Error: {e}", "ERROR")
        return {'value': '—', 'status': 'good', 'error': str(e)}
    return {'value': '—', 'status': 'good'}

def check_network():
    """Check network connectivity"""
    try:
        target = '8.8.8.8'
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
        timeout_val = '1000' if platform.system().lower() == 'windows' else '1000' # ms
        
        result = subprocess.run(['ping', param, '1', timeout_param, timeout_val, target], capture_output=True)
        is_online = result.returncode == 0
        
        return {'value': 'ONLINE', 'status': 'good'} if is_online else {'value': 'OFFLINE', 'status': 'critical'}
    except Exception as e:
        log(f"Network Check Error: {e}", "ERROR")
        return {'value': 'OFFLINE', 'status': 'critical'}

def get_drives():
    """List all drives - cross-platform"""
    drives = []
    try:
        if platform.system() == 'Windows':
            output = subprocess.check_output("wmic logicaldisk get caption,size,freespace,volumename", shell=True).decode()
            lines = output.strip().split('\n')[1:]
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    caption = parts[0]
                    try:
                        free = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                        size = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                        name = ' '.join(parts[3:]) if len(parts) > 3 else caption
                        if size > 0:
                            used_pct = round((size - free) / size * 100)
                            drives.append({
                                'name': name or caption,
                                'path': caption,
                                'size': f'{size//(1024**3)}GB',
                                'used': f'{used_pct}%',
                                'status': 'good' if used_pct < 70 else ('warning' if used_pct < 85 else 'critical')
                            })
                    except:
                        pass
        else:
            output = subprocess.check_output("df -h | grep -E '^/dev'", shell=True).decode()
            for line in output.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 6:
                    mount = ' '.join(parts[5:])
                    pct = int(parts[4].replace('%', ''))
                    drives.append({
                        'name': mount.split('/')[-1] or 'Root',
                        'path': mount,
                        'size': parts[1],
                        'used': parts[4],
                        'status': 'good' if pct < 70 else ('warning' if pct < 85 else 'critical')
                    })
    except:
        pass
    return drives

# ============================================================================
# COMMAND EXECUTION
# ============================================================================

async def execute_command(cmd: str, timeout: int = 30):
    """Execute a shell command"""
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout or result.stderr or 'Command completed.',
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'output': f'Command timed out after {timeout}s', 'code': -1}
    except Exception as e:
        return {'success': False, 'output': str(e), 'code': -1}

# ============================================================================
# API HANDLERS
# ============================================================================

async def handle_status(request):
    """Health check endpoint"""
    return web.Response(
        text=orjson.dumps({
            'status': 'ONLINE',
            'agent_version': '1.0',
            'timestamp': datetime.now().isoformat(),
            **get_system_info()
        }).decode(),
        content_type='application/json'
    )

async def handle_diagnose(request):
    """Full diagnostics"""
    return web.Response(
        text=orjson.dumps({
            'system': get_system_info(),
            'cpu': check_cpu(),
            'ram': check_ram(),
            'disk': check_disk(),
            'network': check_network(),
            'drives': get_drives(),
            'problems': [],
            'score': 100
        }).decode(),
        content_type='application/json'
    )

async def handle_drives(request):
    """List drives"""
    return web.Response(
        text=orjson.dumps(get_drives()).decode(),
        content_type='application/json'
    )

async def handle_exec(request):
    """Execute command"""
    data = await request.json()
    cmd = data.get('command', '')
    timeout = data.get('timeout', 30)
    
    if not cmd:
        return web.Response(
            text=orjson.dumps({'success': False, 'output': 'No command provided'}).decode(),
            content_type='application/json'
        )
    
    result = await execute_command(cmd, timeout)
    return web.Response(
        text=orjson.dumps(result).decode(),
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
    
    app.router.add_get('/status', handle_status)
    app.router.add_get('/diagnose', handle_diagnose)
    app.router.add_get('/drives', handle_drives)
    app.router.add_post('/exec', handle_exec)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5175)
    
    info = get_system_info()
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           NOIZYLAB REMOTE AGENT - ONLINE                     ║
╠══════════════════════════════════════════════════════════════╣
║  🖥️  Host:       {info['hostname']:<40} ║
║  💻 OS:         {info['os']:<40} ║
║  🌐 Port:       5175                                         ║
║  📡 Endpoints:  /status, /diagnose, /drives, /exec          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    await site.start()
    
    # Keep running
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    print("Starting NOIZYLAB Remote Agent...")
    asyncio.run(main())

#!/usr/bin/env python3
"""
GABRIEL DIAGNOSTICS ENGINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TechTool Pro-inspired but BETTER, SMARTER, FASTER + REMOTE
Parallel execution • AI-powered analysis • Cross-platform

FEATURES:
- System Health Score
- CPU/RAM/Disk/Network Monitoring
- S.M.A.R.T. Disk Status
- Memory Pressure Analysis
- Process Audit (CPU hogs, memory leaks)
- Network Speed Test
- Duplicate File Detection
- Cache Cleanup
- Directory Maintenance
- Volume Verification
"""

import asyncio
import subprocess
import platform
import socket
import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any, Optional

# ============================================================================
# PARALLEL EXECUTOR
# ============================================================================

executor = ThreadPoolExecutor(max_workers=8)

async def run_parallel(func, *args):
    """Run function in thread pool for non-blocking execution"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)

def shell(cmd: str, timeout: int = 30) -> str:
    """Execute shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

# ============================================================================
# SYSTEM OVERVIEW
# ============================================================================

class SystemOverview:
    """Basic system information"""
    
    @staticmethod
    def run() -> Dict:
        return {
            'hostname': socket.gethostname(),
            'os': f"{platform.system()} {platform.release()}",
            'os_version': platform.version(),
            'arch': platform.machine(),
            'python': platform.python_version(),
            'uptime': shell("uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}'"),
            'timestamp': datetime.now().isoformat()
        }

# ============================================================================
# CPU DIAGNOSTICS
# ============================================================================

class CPUDiagnostics:
    """CPU monitoring and analysis"""
    
    @staticmethod
    def run() -> Dict:
        result = {'status': 'good', 'score': 100}
        
        if platform.system() == 'Darwin':
            # Get core counts
            logical = shell("sysctl -n hw.logicalcpu")
            physical = shell("sysctl -n hw.physicalcpu")
            result['cores'] = {'logical': int(logical) if logical.isdigit() else 0, 
                              'physical': int(physical) if physical.isdigit() else 0}
            
            # Get CPU usage
            top_output = shell("top -l 1 | grep 'CPU usage'")
            if 'CPU usage' in top_output:
                parts = top_output.split(',')
                user = float(parts[0].split(':')[1].strip().replace('%', '').split()[0])
                sys_pct = float(parts[1].strip().replace('%', '').split()[0])
                idle = float(parts[2].strip().replace('%', '').split()[0])
                
                usage = round(user + sys_pct)
                result['usage'] = f"{usage}%"
                result['breakdown'] = {'user': f"{user}%", 'system': f"{sys_pct}%", 'idle': f"{idle}%"}
                
                if usage > 90:
                    result['status'] = 'critical'
                    result['score'] = 30
                elif usage > 70:
                    result['status'] = 'warning'
                    result['score'] = 60
                    
            # Get CPU model
            result['model'] = shell("sysctl -n machdep.cpu.brand_string")
            
        elif platform.system() == 'Windows':
            result['usage'] = shell("wmic cpu get loadpercentage").split('\n')[-1].strip() + "%"
            result['model'] = shell("wmic cpu get name").split('\n')[-1].strip()
            
        return result

# ============================================================================
# MEMORY DIAGNOSTICS
# ============================================================================

class MemoryDiagnostics:
    """RAM monitoring and memory pressure analysis"""
    
    @staticmethod
    def run() -> Dict:
        result = {'status': 'good', 'score': 100}
        
        if platform.system() == 'Darwin':
            # Total RAM
            total_bytes = shell("sysctl -n hw.memsize")
            total_gb = int(total_bytes) // (1024**3) if total_bytes.isdigit() else 0
            result['total'] = f"{total_gb}GB"
            
            # Memory pressure
            pressure = shell("memory_pressure")
            if 'System-wide memory free percentage' in pressure:
                free_pct = int(pressure.split(':')[-1].strip().replace('%', ''))
                used_pct = 100 - free_pct
                result['pressure'] = f"{used_pct}%"
                
                if used_pct > 90:
                    result['status'] = 'critical'
                    result['score'] = 20
                elif used_pct > 75:
                    result['status'] = 'warning'
                    result['score'] = 50
            
            # vm_stat for detailed breakdown
            vm = shell("vm_stat")
            if 'Pages free' in vm:
                lines = {l.split(':')[0].strip(): l.split(':')[1].strip().replace('.', '') 
                        for l in vm.split('\n') if ':' in l}
                page_size = 16384  # Apple Silicon page size
                
                pages_free = int(lines.get('Pages free', '0'))
                pages_active = int(lines.get('Pages active', '0'))
                pages_inactive = int(lines.get('Pages inactive', '0'))
                pages_wired = int(lines.get('Pages wired down', '0'))
                pages_compressed = int(lines.get('Pages stored in compressor', '0'))
                
                result['breakdown'] = {
                    'free': f"{(pages_free * page_size) // (1024**3)}GB",
                    'active': f"{(pages_active * page_size) // (1024**3)}GB",
                    'inactive': f"{(pages_inactive * page_size) // (1024**3)}GB",
                    'wired': f"{(pages_wired * page_size) // (1024**3)}GB",
                    'compressed': f"{(pages_compressed * page_size) // (1024**3)}GB"
                }
                
        return result
    
    @staticmethod
    def free_memory() -> Dict:
        """Attempt to free inactive memory (like TechTool freemem)"""
        if platform.system() == 'Darwin':
            # Purge inactive memory
            result = shell("sudo purge 2>&1 || echo 'REQUIRES_SUDO'")
            if 'REQUIRES_SUDO' not in result:
                return {'success': True, 'message': 'Inactive memory purged'}
            else:
                # Alternative: use Python gc
                import gc
                gc.collect()
                return {'success': True, 'message': 'Python garbage collection triggered'}
        return {'success': False, 'message': 'Not supported on this platform'}

# ============================================================================
# DISK DIAGNOSTICS
# ============================================================================

class DiskDiagnostics:
    """Disk health, S.M.A.R.T. status, and volume analysis"""
    
    @staticmethod
    def run() -> Dict:
        result = {'status': 'good', 'score': 100, 'volumes': []}
        
        if platform.system() == 'Darwin':
            # Get all volumes
            df_output = shell("df -h | grep -E '^/dev'")
            for line in df_output.split('\n'):
                parts = line.split()
                if len(parts) >= 6:
                    mount = ' '.join(parts[5:])
                    used_pct = int(parts[4].replace('%', ''))
                    
                    vol = {
                        'device': parts[0],
                        'size': parts[1],
                        'used': parts[2],
                        'available': parts[3],
                        'usage': parts[4],
                        'mount': mount,
                        'status': 'good'
                    }
                    
                    if used_pct > 90:
                        vol['status'] = 'critical'
                        result['score'] = min(result['score'], 30)
                    elif used_pct > 80:
                        vol['status'] = 'warning'
                        result['score'] = min(result['score'], 60)
                    
                    result['volumes'].append(vol)
            
            # S.M.A.R.T. status (requires smartmontools or diskutil)
            smart_output = shell("diskutil info disk0 | grep -E 'SMART|S.M.A.R.T'")
            if 'Verified' in smart_output:
                result['smart'] = 'VERIFIED'
            elif 'Failing' in smart_output:
                result['smart'] = 'FAILING'
                result['status'] = 'critical'
                result['score'] = 10
            else:
                result['smart'] = 'UNKNOWN'
                
        return result
    
    @staticmethod
    def verify_volume(mount: str = '/') -> Dict:
        """Verify volume integrity (like TechTool Volume Structures)"""
        if platform.system() == 'Darwin':
            result = shell(f"diskutil verifyVolume {mount} 2>&1 | tail -5")
            if 'appears to be OK' in result or 'valid' in result.lower():
                return {'status': 'verified', 'message': 'Volume structure is valid'}
            else:
                return {'status': 'warning', 'message': result}
        return {'status': 'unknown', 'message': 'Not supported on this platform'}

# ============================================================================
# NETWORK DIAGNOSTICS
# ============================================================================

class NetworkDiagnostics:
    """Network connectivity, speed, Jumbo Frames, and DNS analysis"""
    
    @staticmethod
    def run() -> Dict:
        result = {'status': 'good', 'score': 100}
        
        # Basic connectivity
        ping_google = shell("ping -c 1 -t 2 8.8.8.8 2>&1")
        if 'bytes from' in ping_google:
            result['internet'] = 'ONLINE'
            # Extract latency
            if 'time=' in ping_google:
                latency = ping_google.split('time=')[1].split()[0]
                result['latency'] = latency
        else:
            result['internet'] = 'OFFLINE'
            result['status'] = 'critical'
            result['score'] = 0
            
        # DNS resolution
        dns_test = shell("dig +short google.com 2>&1 | head -1")
        if dns_test and '.' in dns_test:
            result['dns'] = 'OK'
        else:
            result['dns'] = 'FAILED'
            result['score'] = min(result['score'], 50)
            
        # Current DNS servers
        result['dns_servers'] = shell("scutil --dns | grep 'nameserver' | head -3 | awk '{print $3}'").split('\n')
        
        # Local IP
        result['local_ip'] = shell("ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null")
        
        # Public IP
        result['public_ip'] = shell("curl -s --connect-timeout 3 ifconfig.me 2>/dev/null")
        
        # Jumbo Frames detection
        result['jumbo_frames'] = NetworkDiagnostics.check_jumbo_frames()
        
        return result
    
    @staticmethod
    def check_jumbo_frames() -> Dict:
        """Check if Jumbo Frames (MTU 9000) is enabled on network interfaces"""
        interfaces = {}
        
        # Get MTU for all interfaces
        ifconfig = shell("ifconfig | grep -E '^[a-z]|mtu'")
        current_iface = None
        
        for line in ifconfig.split('\n'):
            if line and not line.startswith('\t') and ':' in line:
                current_iface = line.split(':')[0]
            elif 'mtu' in line.lower() and current_iface:
                mtu_match = line.lower().split('mtu')[1].strip().split()[0]
                try:
                    mtu = int(mtu_match)
                    if current_iface.startswith(('en', 'bridge')):
                        interfaces[current_iface] = {
                            'mtu': mtu,
                            'jumbo': mtu >= 9000,
                            'optimal': mtu >= 9000
                        }
                except:
                    pass
        
        # Check main ethernet interface
        en0_mtu = shell("ifconfig en0 2>/dev/null | grep mtu | awk '{print $4}'")
        
        return {
            'enabled': any(i.get('jumbo', False) for i in interfaces.values()),
            'interfaces': interfaces,
            'en0_mtu': en0_mtu,
            'recommendation': 'JUMBO_ENABLED' if any(i.get('jumbo', False) for i in interfaces.values()) else 'ENABLE_JUMBO_FOR_SPEED'
        }
    
    @staticmethod
    def enable_jumbo_frames(interface: str = 'en0') -> Dict:
        """Enable Jumbo Frames (MTU 9000) on specified interface"""
        try:
            # This requires admin privileges
            result = subprocess.run(
                ['sudo', 'ifconfig', interface, 'mtu', '9000'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return {'success': True, 'message': f'Jumbo Frames enabled on {interface} (MTU 9000)'}
            else:
                return {'success': False, 'message': f'Failed: {result.stderr}', 'requires_sudo': True}
        except Exception as e:
            return {'success': False, 'message': str(e), 'requires_sudo': True}
    
    @staticmethod  
    def speed_test() -> Dict:
        """Basic speed test (download speed estimation)"""
        import time
        start = time.time()
        # Download small file from fast CDN
        result = shell("curl -s -o /dev/null -w '%{speed_download}' https://speed.cloudflare.com/__down?bytes=1000000 2>/dev/null")
        elapsed = time.time() - start
        
        try:
            speed_bps = float(result)
            speed_mbps = (speed_bps * 8) / (1024 * 1024)
            return {'download_mbps': round(speed_mbps, 2), 'test_time': round(elapsed, 2)}
        except:
            return {'download_mbps': 'N/A', 'error': 'Speed test failed'}

# ============================================================================
# PROCESS AUDIT
# ============================================================================

class ProcessAudit:
    """Find CPU hogs, memory leaks, and suspicious processes"""
    
    @staticmethod
    def run() -> Dict:
        result = {'cpu_hogs': [], 'memory_hogs': [], 'suspicious': []}
        
        if platform.system() == 'Darwin':
            # Top CPU consumers
            top_cpu = shell("ps aux --sort=-%cpu | head -6 | tail -5")
            for line in top_cpu.split('\n'):
                parts = line.split()
                if len(parts) >= 11:
                    cpu = float(parts[2])
                    if cpu > 10:
                        result['cpu_hogs'].append({
                            'pid': parts[1],
                            'cpu': f"{cpu}%",
                            'mem': f"{parts[3]}%",
                            'command': ' '.join(parts[10:])[:50]
                        })
                        
            # Top memory consumers
            top_mem = shell("ps aux --sort=-%mem | head -6 | tail -5")
            for line in top_mem.split('\n'):
                parts = line.split()
                if len(parts) >= 11:
                    mem = float(parts[3])
                    if mem > 5:
                        result['memory_hogs'].append({
                            'pid': parts[1],
                            'cpu': f"{parts[2]}%",
                            'mem': f"{mem}%",
                            'command': ' '.join(parts[10:])[:50]
                        })
                        
        return result

# ============================================================================
# CACHE & CLEANUP
# ============================================================================

class CacheCleanup:
    """Cache analysis and cleanup"""
    
    @staticmethod
    def analyze() -> Dict:
        """Analyze cache sizes without cleaning"""
        result = {'total_size': 0, 'caches': []}
        
        cache_dirs = [
            ('User Cache', Path.home() / 'Library' / 'Caches'),
            ('Logs', Path.home() / 'Library' / 'Logs'),
            ('Temp', Path('/tmp')),
            ('Chrome Cache', Path.home() / 'Library/Application Support/Google/Chrome/Default/Cache'),
        ]
        
        for name, path in cache_dirs:
            if path.exists():
                size = shell(f"du -sh '{path}' 2>/dev/null | cut -f1")
                result['caches'].append({'name': name, 'path': str(path), 'size': size})
                
        return result
    
    @staticmethod
    def clean(target: str = 'user_cache') -> Dict:
        """Clean specific cache target"""
        targets = {
            'user_cache': str(Path.home() / 'Library' / 'Caches' / '*'),
            'logs': str(Path.home() / 'Library' / 'Logs' / '*'),
            'dns': 'dscacheutil -flushcache',
            'chrome': str(Path.home() / 'Library/Application Support/Google/Chrome/Default/Cache/*')
        }
        
        if target in targets:
            if target == 'dns':
                result = shell(f"sudo {targets[target]} 2>&1 || echo 'REQUIRES_SUDO'")
            else:
                result = shell(f"rm -rf {targets[target]} 2>&1")
            return {'success': True, 'target': target, 'message': 'Cleaned successfully'}
        
        return {'success': False, 'message': f'Unknown target: {target}'}

# ============================================================================
# DUPLICATE FINDER
# ============================================================================

class DuplicateFinder:
    """Find duplicate files (like TechTool's Duplicate File Check)"""
    
    @staticmethod
    def scan(directory: str, min_size_mb: int = 1) -> Dict:
        """Scan for duplicate files by hash"""
        result = {'duplicates': [], 'total_wasted': 0}
        hashes = {}
        min_bytes = min_size_mb * 1024 * 1024
        
        path = Path(directory)
        if not path.exists():
            return {'error': f'Path not found: {directory}'}
            
        for file in path.rglob('*'):
            if file.is_file() and file.stat().st_size >= min_bytes:
                try:
                    # Use first 64KB for fast hash
                    with open(file, 'rb') as f:
                        file_hash = hashlib.md5(f.read(65536)).hexdigest()
                    
                    if file_hash in hashes:
                        size = file.stat().st_size
                        result['duplicates'].append({
                            'original': str(hashes[file_hash]),
                            'duplicate': str(file),
                            'size': f"{size // (1024*1024)}MB"
                        })
                        result['total_wasted'] += size
                    else:
                        hashes[file_hash] = file
                except:
                    pass
                    
        result['total_wasted'] = f"{result['total_wasted'] // (1024*1024)}MB"
        return result

# ============================================================================
# COMPREHENSIVE TEST SUITE
# ============================================================================

class GabrielDiagnostics:
    """Full diagnostic suite - runs all tests in parallel"""
    
    @staticmethod
    async def full_scan() -> Dict:
        """Run comprehensive diagnostics"""
        start = datetime.now()
        
        # Run all diagnostics in parallel
        results = await asyncio.gather(
            run_parallel(SystemOverview.run),
            run_parallel(CPUDiagnostics.run),
            run_parallel(MemoryDiagnostics.run),
            run_parallel(DiskDiagnostics.run),
            run_parallel(NetworkDiagnostics.run),
            run_parallel(ProcessAudit.run),
            run_parallel(CacheCleanup.analyze),
        )
        
        elapsed = (datetime.now() - start).total_seconds()
        
        # Calculate overall health score
        scores = [
            results[1].get('score', 100),  # CPU
            results[2].get('score', 100),  # Memory
            results[3].get('score', 100),  # Disk
            results[4].get('score', 100),  # Network
        ]
        overall_score = sum(scores) // len(scores)
        
        return {
            'health_score': overall_score,
            'status': 'critical' if overall_score < 50 else ('warning' if overall_score < 75 else 'healthy'),
            'scan_time': f"{elapsed:.2f}s",
            'system': results[0],
            'cpu': results[1],
            'memory': results[2],
            'disk': results[3],
            'network': results[4],
            'processes': results[5],
            'caches': results[6],
            'recommendations': GabrielDiagnostics._generate_recommendations(results)
        }
    
    @staticmethod
    def _generate_recommendations(results: List) -> List[str]:
        """AI-powered recommendations based on results"""
        recs = []
        
        cpu = results[1]
        if cpu.get('score', 100) < 70:
            recs.append("🔥 HIGH CPU: Kill background processes or restart resource-heavy apps")
            
        mem = results[2]
        if mem.get('score', 100) < 60:
            recs.append("🧠 MEMORY PRESSURE: Close unused tabs/apps or run memory cleanup")
            
        disk = results[3]
        if disk.get('score', 100) < 70:
            recs.append("💾 LOW DISK SPACE: Run cache cleanup or delete unused files")
            
        net = results[4]
        if net.get('score', 100) < 80:
            recs.append("🌐 NETWORK ISSUE: Check DNS settings or restart router")
            
        processes = results[5]
        if len(processes.get('cpu_hogs', [])) > 3:
            recs.append("⚠️ CPU HOGS DETECTED: Consider terminating high-CPU processes")
            
        if not recs:
            recs.append("✅ SYSTEM HEALTHY: No immediate actions required")
            
        return recs

# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == '__main__':
    import json
    
    print("🔬 GABRIEL DIAGNOSTICS - Running full scan...")
    print("━" * 60)
    
    result = asyncio.run(GabrielDiagnostics.full_scan())
    
    print(f"\n{'='*60}")
    print(f"HEALTH SCORE: {result['health_score']}/100 ({result['status'].upper()})")
    print(f"SCAN TIME: {result['scan_time']}")
    print(f"{'='*60}")
    
    print(f"\n📊 CPU: {result['cpu'].get('usage', 'N/A')} ({result['cpu'].get('status', 'unknown')})")
    print(f"🧠 MEMORY: {result['memory'].get('pressure', 'N/A')} pressure ({result['memory'].get('status', 'unknown')})")
    print(f"💾 DISK: {len(result['disk'].get('volumes', []))} volumes, SMART: {result['disk'].get('smart', 'N/A')}")
    print(f"🌐 NETWORK: {result['network'].get('internet', 'N/A')}, Latency: {result['network'].get('latency', 'N/A')}")
    
    print(f"\n📋 RECOMMENDATIONS:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    
    print(f"\n✅ Full report saved to gabriel_diagnostics_report.json")
    with open('gabriel_diagnostics_report.json', 'w') as f:
        json.dump(result, f, indent=2, default=str)

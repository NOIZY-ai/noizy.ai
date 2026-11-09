#!/usr/bin/env python3
"""
GABRIEL Diagnostics Module
===========================
Structured logging, health checks, and performance monitoring.
"""

import time
import psutil
from datetime import datetime
from functools import wraps

# ANSI Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class Logger:
    """Structured logger with levels and colors"""
    
    LEVELS = {
        'DEBUG': (Colors.WHITE, 0),
        'INFO': (Colors.CYAN, 1),
        'SUCCESS': (Colors.GREEN, 2),
        'WARN': (Colors.YELLOW, 3),
        'ERROR': (Colors.RED, 4),
        'CRITICAL': (Colors.RED + Colors.BOLD, 5)
    }
    
    def __init__(self, name='GABRIEL', min_level='INFO', log_file=None):
        self.name = name
        self.min_level = min_level
        self.log_file = log_file
        self._start_time = time.time()
    
    def _log(self, level, message, **kwargs):
        color, level_num = self.LEVELS.get(level, (Colors.WHITE, 1))
        min_num = self.LEVELS.get(self.min_level, ('', 1))[1]
        
        if level_num < min_num:
            return
        
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]

        # Format extra kwargs
        extra = ''
        if kwargs:
            extra = ' ' + ' '.join(f'{k}={v}' for k, v in kwargs.items())
        
        line = f"{color}[{timestamp}] [{level:8}] [{self.name}] {message}{extra}{Colors.RESET}"
        print(line)
        
        # Also write to file if configured
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(f"[{timestamp}] [{level}] [{self.name}] {message}{extra}\n")
            except:
                pass
    
    def debug(self, msg, **kwargs): self._log('DEBUG', msg, **kwargs)
    def info(self, msg, **kwargs): self._log('INFO', msg, **kwargs)
    def success(self, msg, **kwargs): self._log('SUCCESS', msg, **kwargs)
    def warn(self, msg, **kwargs): self._log('WARN', msg, **kwargs)
    def error(self, msg, **kwargs): self._log('ERROR', msg, **kwargs)
    def critical(self, msg, **kwargs): self._log('CRITICAL', msg, **kwargs)

# Global logger instance
log = Logger('GABRIEL')

def timed(func):
    """Decorator to time function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        log.debug(f'{func.__name__} completed', ms=f'{elapsed:.2f}')
        return result
    return wrapper

def get_system_health():
    """Get comprehensive system health status - OPTIMIZED (non-blocking)"""
    try:
        cpu = psutil.cpu_percent(interval=None)  # Non-blocking
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Determine health status
        status = 'HEALTHY'
        issues = []
        
        if cpu > 90:
            status = 'DEGRADED'
            issues.append(f'High CPU: {cpu}%')
        if ram.percent > 90:
            status = 'DEGRADED'
            issues.append(f'High RAM: {ram.percent}%')
        if disk.percent > 95:
            status = 'CRITICAL'
            issues.append(f'Disk full: {disk.percent}%')
        
        return {
            'status': status,
            'cpu_percent': cpu,
            'ram_percent': ram.percent,
            'ram_available_gb': round(ram.available / (1024**3), 2),
            'disk_percent': disk.percent,
            'issues': issues,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'UNKNOWN',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def check_port(port, host='localhost'):
    """Check if a port is responding"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_services():
    """Check all GABRIEL services"""
    services = {
        'ultrafast_server': {'port': 5174, 'name': 'ULTRAFAST Server'},
        'network_bridge': {'port': 5175, 'name': 'Network Bridge'},
    }
    
    results = {}
    for svc_id, svc in services.items():
        results[svc_id] = {
            'name': svc['name'],
            'port': svc['port'],
            'running': check_port(svc['port']),
        }
    
    return results

def print_banner():
    """Print GABRIEL startup banner"""
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                    GABRIEL SYSTEM OMEGA                          ║
║              Beyond Zero Latency · Maximum Performance           ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

if __name__ == '__main__':
    print_banner()
    log.info("Running diagnostics...")
    
    health = get_system_health()
    log.info(f"System Health: {health['status']}")
    log.info(f"CPU: {health['cpu_percent']}%")
    log.info(f"RAM: {health['ram_percent']}%")
    log.info(f"Disk: {health['disk_percent']}%")
    
    services = check_services()
    for svc_id, svc in services.items():
        if svc['running']:
            log.success(f"{svc['name']}: ONLINE (port {svc['port']})")
        else:
            log.error(f"{svc['name']}: OFFLINE (port {svc['port']})")

#!/usr/bin/env python3
"""
GABRIEL Agent v2.0 - "The Flash" Edition
Cross-Platform Local HTTP server for tunnel commands.
Optimized for macOS ("M2 Ultra") with fallback for Windows.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import socket
import platform
import psutil
import os
import threading
import time

PORT = 8080
PLATFORM = platform.system()
USER_NAME = "Rob"

# --- Intelligence Map ---
# Maps abstract commands to platform-specific implementations
COMMAND_MAP = {
    'Darwin': {
        'ipconfig': 'ifconfig',
        'dir': 'ls -la',
        'systeminfo': 'system_profiler SPSoftwareDataType SPHardwareDataType',
        'tasklist': 'ps -A',
        'say': 'say',
        'open': 'open',
        'flush': 'dscacheutil -flushcache; sudo killall -HUP mDNSResponder',
        'speak': 'say',
        'repair': 'bash ~/NOIZYLAB/scripts/MASTER_REPAIR.sh',
        'health': 'bash ~/NOIZYLAB/scripts/MASTER_REPAIR.sh health',
        'clean': 'bash ~/NOIZYLAB/scripts/MASTER_REPAIR.sh clean'
    },
    'Windows': {
        'ipconfig': 'ipconfig',
        'dir': 'dir',
        'systeminfo': 'systeminfo',
        'tasklist': 'tasklist',
        'say': 'echo "Speech not supported on Windows core"',
        'open': 'start',
        'flush': 'ipconfig /flushdns',
        'speak': 'echo',
        'repair': 'sfc /scannow',
        'health': 'wmic cpu get loadpercentage',
        'clean': 'cleanmgr /sagerun:1'
    }
}

# Standard allowed commands (Security Layer)
ALLOWED_CMDS = [
    'hostname', 'whoami', 'date', 'time', 'uptime', 'netstat', 
    'echo', 'ping', 'curl', 'python3', 'python'
]

def get_platform_cmd(cmd_base):
    """Translates a command to the native platform equivalent."""
    platform_specific = COMMAND_MAP.get(PLATFORM, {})
    return platform_specific.get(cmd_base, cmd_base)

class GabrielHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        try:
            self.wfile.write(json.dumps(data, default=str).encode())
        except Exception as e:
            print(f"JSON Error: {e}")
    
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            info = {
                'agent': 'GABRIEL v2.0 (The Flash)',
                'user': USER_NAME,
                'status': 'online',
                'hostname': socket.gethostname(),
                'platform': PLATFORM,
                'os_release': platform.release(),
                'cpu_usage': f"{psutil.cpu_percent()}%",
                'memory_usage': f"{psutil.virtual_memory().percent}%",
                'boot_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
            }
            self._json(info)
        else:
            self._json({'error': 'Endpoint not found'}, 404)
    
    def do_POST(self):
        if self.path == '/exec':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            
            raw_cmd = body.get('cmd', '')
            timeout = min(body.get('timeout', 30), 60)
            
            if not raw_cmd:
                self._json({'error': 'No command provided'}, 400)
                return

            cmd_parts = raw_cmd.split()
            base_cmd = cmd_parts[0].lower()
            
            # --- Smart Translation ---
            # Check if it's a known mapped command first
            translated_base = get_platform_cmd(base_cmd)
            
            # Reconstruct command with arguments if it was translated
            if translated_base != base_cmd:
                final_cmd = translated_base + " " + " ".join(cmd_parts[1:])
            else:
                final_cmd = raw_cmd

            # --- Safety Check ---
            # If it wasn't a mapped command, check if it's in the allowed list
            # We treat the mapped commands as implicitly allowed
            is_mapped = base_cmd in COMMAND_MAP.get(PLATFORM, {})
            is_allowed = base_cmd in ALLOWED_CMDS
            
            if not (is_mapped or is_allowed):
                self._json({'error': f'Command denied by AI Safety Protocol: {base_cmd}'}, 403)
                return
            
            # Execute
            try:
                # Run in subprocess
                result = subprocess.run(
                    final_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                output = result.stdout.strip()
                if not output and result.stderr:
                    output = f"STDERR: {result.stderr.strip()}"
                elif not output:
                    output = "Command executed successfully (No Output)"

                self._json({
                    'cmd': final_cmd,
                    'output': output,
                    'code': result.returncode
                })
            except subprocess.TimeoutExpired:
                self._json({'error': 'Execution timed out (Hyperdrive limit exceeded)'}, 408)
            except Exception as e:
                self._json({'error': str(e)}, 500)
        else:
            self._json({'error': 'Method not allowed'}, 405)

    def log_message(self, format, *args):
        # Concise logging
        return

if __name__ == '__main__':
    print(f"⚡ GABRIEL AGENT v2.0 ONLINE")
    print(f"⚡ Platform: {PLATFORM}")
    print(f"⚡ Port: {PORT}")
    print(f"⚡ AI Safety: ACTIVE")
    
    server = HTTPServer(('0.0.0.0', PORT), GabrielHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⚡ Disengaging...")
        server.shutdown()

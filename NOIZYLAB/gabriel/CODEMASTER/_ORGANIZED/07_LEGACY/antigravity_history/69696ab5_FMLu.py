#!/usr/bin/env python3
"""
turbo_net_check.py
Instant Network Health Verification for MC96ECOUNIVERSE
"""

import sys
import subprocess
import time
import socket

# Emojis
CHECK = "✅"
FAIL = "❌"
WARN = "⚠️"
INFO = "ℹ️"

def print_status(message, status=INFO):
    print(f"{status} {message}")

def ping(host, count=1, timeout=2):
    """Ping a host and return True if reachable."""
    try:
        # macOS ping flags: -c count, -t timeout (seconds)
        cmd = ["ping", "-c", str(count), "-t", str(timeout), host]
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def check_dns(domain):
    """Try to resolve a domain."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def get_default_gateway():
    """Get default gateway IP."""
    try:
        # netstat -rn | grep default
        cmd = "netstat -rn | grep default | awk '{print $2}' | head -n 1"
        gateway = subprocess.check_output(cmd, shell=True).decode().strip()
        return gateway
    except:
        return None

def main():
    print("========================================")
    print("🚀 TURBO NETWORK DIAGNOSTIC v1.0")
    print("========================================")
    
    # 1. Local Gateway
    gateway = get_default_gateway()
    if gateway:
        if ping(gateway):
            print_status(f"Router ({gateway}) is REACHABLE", CHECK)
        else:
            print_status(f"Router ({gateway}) is UNREACHABLE", FAIL)
    else:
        print_status("Could not determine Default Gateway", WARN)

    # 2. Public Internet Ping
    if ping("8.8.8.8"):
        print_status("Internet Connection (Ping 8.8.8.8)", CHECK)
    else:
        print_status("Internet Connection (Ping 8.8.8.8)", FAIL)

    # 3. DNS Resolution
    domains = ["google.com", "netflix.com", "apple.com"]
    success_count = 0
    for d in domains:
        if check_dns(d):
            success_count += 1
    
    if success_count == len(domains):
        print_status("DNS Resolution (Core Services)", CHECK)
    elif success_count > 0:
        print_status("DNS Resolution (Partial)", WARN)
    else:
        print_status("DNS Resolution (FAILED)", FAIL)

    # 4. Detailed Speed/Latency (Optional expansion)
    # Kept simple for speed.
    
    print("========================================")
    if success_count == len(domains) and ping("8.8.8.8"):
        print("✨ NETWORK STATUS: OPTIMAL")
        sys.exit(0)
    else:
        print("💀 NETWORK STATUS: DEGRADED")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# ============================================================================
# MC96ECOUNIVERSE - DEVICE SCANNER (THE INTELLIGENT RADAR)
# Version: 2.0 (God Mode)
# ============================================================================

import sys
import subprocess
import threading
import json
import time
import socket
import os
from concurrent.futures import ThreadPoolExecutor

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
ENDC = '\033[0m'

NETWORK_PREFIX = "10.0.0" # Adjust based on actual network
SCAN_RANGE = range(1, 255)
MAX_THREADS = 50
TIMEOUT = 0.5 

DEVICES = []
LOCK = threading.Lock()

def get_vendor(mac):
    # Simplified vendor lookup map
    # In a real "God Mode" script, we might query an API or huge local DB
    vendors = {
        "ac:de:48": "Private",
        "00:0c:29": "VMware",
        "00:50:56": "VMware",
        "b8:27:eb": "Raspberry Pi",
        "dc:a6:32": "Raspberry Pi",
        "e4:5f:01": "Raspberry Pi",
        "00:11:32": "Synology",
        "00:11" : "Apple", # Fallback for many Apple prefixes
        "28:cf:e9": "Apple",
        "14:98:77": "Apple",
        "c8:89:f3": "Apple",
        "f0:18:98": "Apple",
        "7c:1e:52": "Sonos",
        "48:a6:b8": "Sonos",
        "b4:fb:e4": "Nest",
        "18:b4:30": "Nest",
        "68:D6:ED": "D-Link", # DGS-1210-10 likely
    }
    
    prefix = mac.lower().replace("-", ":")[0:8]
    short_prefix = mac.lower().replace("-", ":")[0:5]
    
    if prefix in vendors: return vendors[prefix]
    if short_prefix in vendors: return vendors[short_prefix]
    
    return "Unknown"

def ping_host(ip):
    try:
        # Use simple ping command
        # -c 1 = count 1, -W 500 = wait 500ms
        cmd = ["ping", "-c", "1", "-W", "500", ip]
        start = time.time()
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.time()
        
        if res.returncode == 0:
            latency = (end - start) * 1000 # ms
            return latency
        return None
    except:
        return None

def scan_ip(ip):
    latency = ping_host(ip)
    if latency is not None:
        # Try to resolve hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"
            
        # Try to get MAC address (from arp table after ping)
        mac = "Unknown"
        try:
            arp_res = subprocess.check_output(f"arp {ip}", shell=True).decode()
            if "at" in arp_res:
                mac = arp_res.split("at")[1].split()[0]
        except:
            pass

        vendor = get_vendor(mac)
        
        device = {
            "ip": ip,
            "hostname": hostname,
            "latency_ms": round(latency, 2),
            "mac": mac,
            "vendor": vendor,
            "status": "Online"
        }
        
        with LOCK:
            DEVICES.append(device)
            status_color = GREEN if latency < 10 else YELLOW
            print(f"{GREEN}✓ FOUND:{ENDC} {ip:<15} | {status_color}{latency:>6.2f}ms{ENDC} | {hostname}")

def main():
    print(f"{BLUE}")
    print("================================================================")
    print("   📡 MC96ECOUNIVERSE DEVICE SCANNER - RADAR ACTIVE           ")
    print("================================================================")
    print(f"{ENDC}")
    print(f"Scanning {NETWORK_PREFIX}.1-254...")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for i in SCAN_RANGE:
            ip = f"{NETWORK_PREFIX}.{i}"
            executor.submit(scan_ip, ip)
            
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{BLUE}Scan Complete in {duration:.2f}s{ENDC}")
    print(f"{GREEN}Total Devices Found: {len(DEVICES)}{ENDC}")
    
    # Save Report
    report_path = "/Users/m2ultra/NOIZYLAB/docs/mc96_network_report.json"
    with open(report_path, "w") as f:
        json.dump(DEVICES, f, indent=2)
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()

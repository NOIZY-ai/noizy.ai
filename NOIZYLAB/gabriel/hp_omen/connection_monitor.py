#!/usr/bin/env python3
"""
GABRIEL CONNECTION MONITOR - Real-time HP-OMEN detection
Continuously monitors for HP-OMEN connection
"""
import requests
import time
import subprocess
from datetime import datetime

class ConnectionMonitor:
    def __init__(self):
        self.bridge_url = "http://localhost:5175"
        self.targets = {
            'HP-OMEN (VPN)': '10.100.0.2',
            'HP-OMEN (LAN)': '10.0.0.46'
        }
        self.known_peers = set()

    def check_bridge_status(self):
        """Check if network bridge is running"""
        try:
            resp = requests.get(f"{self.bridge_url}/api/bridge/status", timeout=2)
            return resp.json() if resp.status_code == 200 else None
        except:
            return None

    def ping_target(self, ip):
        """Check if target is reachable"""
        try:
            resp = requests.get(f"{self.bridge_url}/api/bridge/ping/{ip}", timeout=3)
            if resp.status_code == 200:
                return resp.json().get('alive', False)
        except:
            pass
        return False

    def trigger_discovery(self):
        """Broadcast discovery"""
        try:
            requests.get(f"{self.bridge_url}/api/bridge/discover", timeout=2)
            return True
        except:
            return False

    def get_peers(self):
        """Get discovered peers"""
        try:
            resp = requests.get(f"{self.bridge_url}/api/bridge/peers", timeout=2)
            if resp.status_code == 200:
                return resp.json().get('peers', {})
        except:
            pass
        return {}

    def monitor(self, interval=5):
        """Continuous monitoring loop"""
        print("\n" + "="*70)
        print("  🔍 GABRIEL CONNECTION MONITOR - HP-OMEN DETECTION")
        print("="*70 + "\n")

        # Check bridge
        status = self.check_bridge_status()
        if not status:
            print("❌ Network bridge is not running!")
            print("   Run: ./connect_hp_omen.sh")
            return

        print(f"✅ Network bridge ONLINE")
        print(f"   Hostname: {status['hostname']}")
        print(f"   Local IP: {status['local_ip']}")
        print(f"   Bridge Port: {status['port']}")
        print()

        print("🎯 Monitoring targets:")
        for name, ip in self.targets.items():
            print(f"   → {name}: {ip}")
        print()
        print("Press Ctrl+C to stop...")
        print("="*70)
        print()

        iteration = 0
        try:
            while True:
                iteration += 1
                timestamp = datetime.now().strftime('%H:%M:%S')

                # Trigger discovery every 3rd check
                if iteration % 3 == 0:
                    self.trigger_discovery()

                # Check all targets
                for name, ip in self.targets.items():
                    alive = self.ping_target(ip)

                    if alive:
                        print(f"[{timestamp}] ✅ {name} ({ip}) - CONNECTED!")
                    else:
                        print(f"[{timestamp}] ⏳ {name} ({ip}) - waiting...", end='\r', flush=True)

                # Check for new peers
                peers = self.get_peers()
                for peer_id, peer_data in peers.items():
                    if peer_id not in self.known_peers:
                        self.known_peers.add(peer_id)
                        print(f"\n[{timestamp}] 🌐 NEW PEER DISCOVERED:")
                        print(f"   Hostname: {peer_data['hostname']}")
                        print(f"   IP: {peer_data['ip']}")
                        print(f"   Port: {peer_data['port']}")
                        print()

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("  🛑 Monitoring stopped")
            print("="*70)

if __name__ == '__main__':
    monitor = ConnectionMonitor()
    monitor.monitor(interval=5)

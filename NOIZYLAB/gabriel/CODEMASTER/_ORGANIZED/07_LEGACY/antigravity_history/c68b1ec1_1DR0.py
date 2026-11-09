#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║             GABRIEL SYSTEM OMEGA - TURBO VPN CORE [ZERO LATENCY]             ║
║                           PROTOCOL: WIREGUARD                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Network Topology: Hub (M2 Ultra) <-> Spokes (HP-OMEN, iPad, iPhone)         ║
║  Subnet: 10.100.0.0/24                                                       ║
║  Port: 51820/UDP                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import subprocess
import json
from pathlib import Path

# Configuration
VPN_DIR = Path("/Users/m2ultra/NOIZYLAB/GABRIEL/VPN")
SERVER_IP = "10.100.0.1"
PORT = 51820
# NOTE: Replace with actual Public IP or DDNS if available, otherwise defaulting to local detection or placeholder
ENDPOINT_IP = "YOUR_PUBLIC_IP_OR_DDNS" 
INTERNET_INTERFACE = "en0" # Standard Mac WiFi/Ethernet interface. Adjust if needed.

# Clients
CLIENTS = [
    {"name": "GABRIEL_OMEN", "ip": "10.100.0.2"},
    {"name": "GABRIEL_PORTAL_PAD", "ip": "10.100.0.3"},
    {"name": "GABRIEL_MOBILE", "ip": "10.100.0.4"}
]

def run_cmd(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running '{cmd}': {e.output.decode()}")
        return None

def ensure_dir():
    if not VPN_DIR.exists():
        print(f"📂 Creating VPN Directory: {VPN_DIR}")
        VPN_DIR.mkdir(parents=True, exist_ok=True)

def check_wireguard():
    """Check if wireguard-tools is installed."""
    print("🔍 Checking WireGuard availability...")
    if not run_cmd("which wg"):
        print("❌ WireGuard tools (wg) not found! Please run: brew install wireguard-tools")
        return False
    print("✅ WireGuard tools detected.")
    return True

def generate_keypair():
    """Generate a Curve25519 private/public key pair."""
    priv = run_cmd("wg genkey")
    pub = run_cmd(f"echo '{priv}' | wg pubkey")
    return priv, pub

def setup_vpn():
    ensure_dir()
    
    # 1. Server Keys
    print("\n🔑 Generating SERVER Keys...")
    srv_priv, srv_pub = generate_keypair()
    
    # 2. Client Keys & Configs
    peers_config = ""
    
    for client in CLIENTS:
        print(f"👤 Provisioning Client: {client['name']} ({client['ip']})...")
        c_priv, c_pub = generate_keypair()
        
        # Add peer to Server Config
        peers_config += f"""
# Peer: {client['name']}
[Peer]
PublicKey = {c_pub}
AllowedIPs = {client['ip']}/32
"""

        # Generate Client Config File
        client_conf = f"""[Interface]
PrivateKey = {c_priv}
Address = {client['ip']}/24
DNS = 1.1.1.1

[Peer]
PublicKey = {srv_pub}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = {ENDPOINT_IP}:{PORT}
PersistentKeepalive = 25
"""
        client_file = VPN_DIR / f"{client['name']}.conf"
        with open(client_file, "w") as f:
            f.write(client_conf)
        print(f"   └── Config saved: {client_file}")

    # 3. Server Config (wg0.conf)
    print(f"\n🖥️  Generating SERVER Config (wg0.conf)...")
    
    # Simple PostUp/PostDown for macOS NAT (adjust directory for pf.conf if needed, usually requires more setup on mac)
    # For simplicity/safety, we are just bringing up the interface. Full NAT requires enabling packet forwarding in sysctl.
    
    server_conf = f"""[Interface]
Address = {SERVER_IP}/24
ListenPort = {PORT}
PrivateKey = {srv_priv}
MTU = 1360
# PostUp/Down can be added here for NAT masquerading if sharing internet
# PostUp = /usr/local/bin/wg-quick-masquerade up %i
# PostDown = /usr/local/bin/wg-quick-masquerade down %i

{peers_config}
"""
    server_file = VPN_DIR / "wg0.conf"
    with open(server_file, "w") as f:
        f.write(server_conf)
    print(f"✅ Server config saved: {server_file}")
    
    print("\n════════════════════════════════════════════════════════════════")
    print("🚀 VPN SETUP COMPLETE")
    print(f"📂 All configuration files are in: {VPN_DIR}")
    print("⚠️  IMPORTANT STEPS:")
    print(f"1. Enable IP Forwarding: sudo sysctl -w net.inet.ip.forwarding=1")
    print(f"2. Start Server: sudo wg-quick up {server_file}")
    print(f"3. Port Forward {PORT}/UDP on your Router to this machine.")
    print("════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    if check_wireguard():
        setup_vpn()

#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🚀 GABRIEL REMOTE AGENT DEPLOYMENT
# ═══════════════════════════════════════════════════════════════
# Target: HP-OMEN (10.100.0.2 VPN / 10.0.0.160 LAN)
# User: m2ultra

# Try VPN first, fallback to LAN
TARGET_VPN="10.100.0.2"
TARGET_LAN="10.0.0.160"
TARGET_USER="m2ultra"
AGENT_SRC="$(dirname "$0")/network_bridge.py"

echo -e "\n\033[1;36m🔵 GABRIEL DEPLOYMENT SYSTEM ACTIVATED\033[0m"

# Determine which IP is reachable
if ping -c 1 -t 2 "$TARGET_VPN" &>/dev/null; then
    TARGET_IP="$TARGET_VPN"
    echo "Using VPN connection: $TARGET_IP"
elif ping -c 1 -t 2 "$TARGET_LAN" &>/dev/null; then
    TARGET_IP="$TARGET_LAN"
    echo "Using LAN connection: $TARGET_IP"
else
    echo -e "\033[1;31m❌ HP-OMEN not reachable on VPN or LAN\033[0m"
    exit 1
fi

echo "Targeting: $TARGET_USER@$TARGET_IP"

# 1. Keys
echo -e "\n\033[1;33m🔑 PHASE 1: KEY EXCHANGE\033[0m"
echo "Attempting to copy SSH identity. You may be asked for the password."
ssh-copy-id -o StrictHostKeyChecking=no "$TARGET_USER@$TARGET_IP" 2>/dev/null || true

# 2. Copy
echo -e "\n\033[1;33m📦 PHASE 2: PAYLOAD TRANSMISSION\033[0m"
if [ -f "$AGENT_SRC" ]; then
    scp -o StrictHostKeyChecking=no "$AGENT_SRC" "$TARGET_USER@$TARGET_IP:~/network_bridge.py"
    echo "✅ Network bridge transferred successfully."
else
    echo "⚠️  network_bridge.py not found, copying requirements only"
fi

scp -o StrictHostKeyChecking=no "$(dirname "$0")/requirements.txt" "$TARGET_USER@$TARGET_IP:~/"

# 3. Ignite
echo -e "\n\033[1;33m🔥 PHASE 3: IGNITION\033[0m"
ssh -o StrictHostKeyChecking=no "$TARGET_USER@$TARGET_IP" "
    echo 'Installing Dependencies...'
    pip3 install flask flask-cors requests aiohttp orjson --user --quiet 2>/dev/null || true

    echo 'Stopping existing instances...'
    pkill -f network_bridge.py || true

    echo 'Starting Network Bridge...'
    nohup python3 ~/network_bridge.py > ~/gabriel_bridge.log 2>&1 &

    echo '✅ GABRIEL NETWORK BRIDGE ACTIVE'
"

echo -e "\n\033[1;32m🏁 DEPLOYMENT SEQUENCE COMPLETE\033[0m"
echo "Verify at: http://$TARGET_IP:5175/api/bridge/status"

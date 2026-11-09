#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🚀 GABRIEL REMOTE AGENT DEPLOYMENT
# ═══════════════════════════════════════════════════════════════
# Target: HP-OMEN (10.0.0.160)
# User: m2ultra

TARGET_IP="10.0.0.160"
TARGET_USER="m2ultra"
AGENT_SRC="/Users/m2ultra/NOIZYLAB/PORTAL/remote_agent.py"

echo -e "\n\033[1;36m🔵 GABRIEL DEPLOYMENT SYSTEM ACTIVATED\033[0m"
echo "Targeting: $TARGET_USER@$TARGET_IP"

# 1. keys
echo -e "\n\033[1;33m🔑 PHASE 1: KEY EXCHANGE\033[0m"
echo "Attempting to copy SSH identity. You may be asked for the password."
ssh-copy-id -o StrictHostKeyChecking=no "$TARGET_USER@$TARGET_IP"

if [ $? -ne 0 ]; then
    echo -e "\033[1;31m❌ SSH Key Exchange Failed. Deployment Aborted.\033[0m"
    exit 1
fi

# 2. copy
echo -e "\n\033[1;33m📦 PHASE 2: PAYLOAD TRANSMISSION\033[0m"
if [ -f "$AGENT_SRC" ]; then
    scp -o StrictHostKeyChecking=no "$AGENT_SRC" "$TARGET_USER@$TARGET_IP:~/remote_agent.py"
    echo "✅ Agent transferred successfully."
else
    echo -e "\033[1;31m❌ Source file not found: $AGENT_SRC\033[0m"
    exit 1
fi

# 3. ignite
echo -e "\n\033[1;33m🔥 PHASE 3: IGNITION\033[0m"
ssh -o StrictHostKeyChecking=no "$TARGET_USER@$TARGET_IP" "
    echo 'Installing Dependencies...'
    python3 -m pip install aiohttp orjson --user --quiet
    
    echo 'Stopping existing instances...'
    pkill -f remote_agent.py || true
    
    echo 'Starting Agent...'
    nohup python3 ~/remote_agent.py > ~/agent.log 2>&1 &
    
    echo '✅ REMOTE AGENT ACTIVE'
"

echo -e "\n\033[1;32m🏁 DEPLOYMENT SEQUENCE COMPLETE\033[0m"
echo "Verify at: http://$TARGET_IP:5175/status"

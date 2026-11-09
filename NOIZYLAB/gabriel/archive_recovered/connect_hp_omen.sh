#!/bin/bash
#
# CONNECT TO HP-OMEN GABRIEL INSTANCE
# Network bridge launcher
#
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo "${PURPLE}║  🌐 GABRIEL NETWORK BRIDGE - HP-OMEN CONNECTION              ║${NC}"
echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""

cd "$(dirname "$0")"

# Get local IP
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")

echo "${CYAN}📍 MBP13 Information:${NC}"
echo "   Hostname: $(hostname)"
echo "   Local IP: $LOCAL_IP"
echo "   Bridge Port: 5175"
echo ""

# Check if bridge is already running
if lsof -ti:5175 > /dev/null 2>&1; then
    echo "${YELLOW}⚠️  Network bridge already running${NC}"
    echo "${CYAN}→ Stopping old instance...${NC}"
    lsof -ti:5175 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start network bridge
echo "${CYAN}🚀 Starting network bridge...${NC}"

if [[ -f "venv/bin/python3" ]]; then
    PYTHON="venv/bin/python3"
else
    PYTHON="python3"
fi

$PYTHON network_bridge.py > network_bridge.log 2>&1 &
BRIDGE_PID=$!

sleep 3

# Check if bridge started
if lsof -ti:5175 > /dev/null 2>&1; then
    echo "${GREEN}✅ Network bridge ONLINE (PID: $BRIDGE_PID)${NC}"
    echo ""

    # Get bridge status
    echo "${CYAN}📊 Bridge Status:${NC}"
    curl -s http://localhost:5175/api/bridge/status | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"   Hostname: {data['hostname']}\")
print(f\"   Local IP: {data['local_ip']}\")
print(f\"   Peers: {data['peer_count']}\")
" 2>/dev/null || echo "   Initializing..."

    echo ""
    echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo "${GREEN}  ✅ GABRIEL NETWORK BRIDGE ACTIVE${NC}"
    echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo ""
    echo "${CYAN}📡 To connect from HP-OMEN:${NC}"
    echo ""
    echo "   1. Copy network_bridge.py to HP-OMEN"
    echo "   2. Run: python3 network_bridge.py"
    echo "   3. Both machines will auto-discover each other"
    echo ""
    echo "${CYAN}🌐 API Endpoints:${NC}"
    echo "   → http://$LOCAL_IP:5175/api/bridge/status"
    echo "   → http://$LOCAL_IP:5175/api/bridge/peers"
    echo "   → http://$LOCAL_IP:5175/api/bridge/discover"
    echo ""
    echo "${CYAN}📝 Logs:${NC}"
    echo "   → tail -f network_bridge.log"
    echo ""
    echo "${GREEN}⚡ GORUNFREE NETWORK ACTIVE ⚡${NC}"
    echo ""
else
    echo "${YELLOW}⚠️  Bridge failed to start - check logs:${NC}"
    echo "   → tail network_bridge.log"
fi

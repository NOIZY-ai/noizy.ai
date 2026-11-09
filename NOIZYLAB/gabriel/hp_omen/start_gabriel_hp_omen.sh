#!/bin/bash
#
# START GABRIEL ON HP-OMEN
#
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo "${PURPLE}║  🌐 GABRIEL NETWORK BRIDGE - HP-OMEN                        ║${NC}"
echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""

cd "$(dirname "$0")"

# Install dependencies
if ! python3 -c "import flask" 2>/dev/null; then
    echo "${CYAN}📦 Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

# Kill existing
pkill -f "network_bridge.py" 2>/dev/null || true
sleep 1

# Start network bridge
echo "${CYAN}🚀 Starting GABRIEL network bridge...${NC}"
python3 network_bridge.py > network_bridge.log 2>&1 &
BRIDGE_PID=$!

sleep 3

# Check if running
if ps -p $BRIDGE_PID > /dev/null 2>&1; then
    echo "${GREEN}✅ GABRIEL Network Bridge ONLINE (PID: $BRIDGE_PID)${NC}"
    echo ""
    echo "${CYAN}📡 Bridge will auto-discover MBP13 GABRIEL${NC}"
    echo "${CYAN}📝 Logs: tail -f network_bridge.log${NC}"
    echo ""
else
    echo "${YELLOW}⚠️  Bridge failed to start - check logs${NC}"
fi

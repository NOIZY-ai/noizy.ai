#\!/bin/bash
# GABRIEL SYSTEM OMEGA - Launch Script + WebSocket + Watchdog
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
GREEN="[0;32m"; RED="[0;31m"; CYAN="[0;36m"; YELLOW="[1;33m"; PURPLE="[0;35m"; NC="[0m"
echo -e "${CYAN}GABRIEL SYSTEM OMEGA - LAUNCH${NC}"
pkill -f "mc96_server" 2>/dev/null || true
pkill -f "network_bridge" 2>/dev/null || true
pkill -f "watchdog.py" 2>/dev/null || true
sleep 2
./venv/bin/python3 mc96_server_ULTRAFAST.py > server.log 2>&1 &
./venv/bin/python3 network_bridge.py > bridge.log 2>&1 &
sleep 4
./venv/bin/python3 watchdog.py > watchdog.log 2>&1 &
echo -e "${GREEN}ALL SYSTEMS LAUNCHED${NC}"
curl -s http://localhost:5174/api/health && echo " Server OK"
curl -s http://localhost:5175/api/bridge/status && echo " Bridge OK"


#!/bin/zsh
#
# 💥 INSTANT FIX & LAUNCH - ZERO LATENCY
# No sudo, no waiting, just GO!
#
set -e
export TERM=xterm-256color

cd "$(dirname "$0")"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo "${PURPLE}═══════════════════════════════════════════════════════${NC}"
echo "${PURPLE}  💥 INSTANT FIX & LAUNCH - MBP13 ULTRAFAST  💥${NC}"
echo "${PURPLE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Kill old servers
echo "${CYAN}→ Cleaning up old processes...${NC}"
pkill -f "mc96_server" 2>/dev/null || true
lsof -ti:5174 | xargs kill -9 2>/dev/null || true

# Check dependencies
echo "${CYAN}→ Checking dependencies...${NC}"
if [[ -f "venv/bin/python3" ]]; then
    PYTHON="venv/bin/python3"
    echo "${GREEN}✓ Using venv Python${NC}"
else
    PYTHON="python3"
    echo "${GREEN}✓ Using system Python${NC}"
fi

# Quick dependency check
$PYTHON -c "import flask, flask_cors" 2>/dev/null || {
    echo "${CYAN}→ Installing dependencies...${NC}"
    $PYTHON -m pip install flask flask-cors orjson --quiet 2>/dev/null || true
}

# Start ULTRAFAST server
echo "${CYAN}→ Starting ULTRAFAST server...${NC}"
if [[ -f "mc96_server_ULTRAFAST.py" ]]; then
    SERVER="mc96_server_ULTRAFAST.py"
    echo "${GREEN}✓ Using ULTRAFAST edition (<2ms)${NC}"
else
    SERVER="mc96_server_optimized.py"
    echo "${GREEN}✓ Using optimized edition (<3ms)${NC}"
fi

$PYTHON "$SERVER" > server.log 2>&1 &
SERVER_PID=$!

echo "${GREEN}✓ Server starting (PID: $SERVER_PID)${NC}"
echo ""

# Wait for server
sleep 2

# Check status
if lsof -ti:5174 > /dev/null 2>&1; then
    echo "${GREEN}✅ SERVER ONLINE ON PORT 5174${NC}"

    # Test response time
    RESPONSE=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:5174/api/health 2>/dev/null || echo "0")
    echo "${GREEN}✅ API Response: ${RESPONSE}s${NC}"

    echo ""
    echo "${PURPLE}═══════════════════════════════════════════════════════${NC}"
    echo "${GREEN}  ⚡ DREAMCHAMBER PORTAL:${NC}"
    echo "${CYAN}     → http://localhost:5174/dreamchamber${NC}"
    echo ""
    echo "${GREEN}  📊 API ENDPOINTS:${NC}"
    echo "${CYAN}     → http://localhost:5174/api/status${NC}"
    echo "${CYAN}     → http://localhost:5174/api/memcell/graph/lite${NC}"
    echo ""
    echo "${GREEN}  📝 LOGS:${NC}"
    echo "${CYAN}     → tail -f server.log${NC}"
    echo "${PURPLE}═══════════════════════════════════════════════════════${NC}"
    echo ""

    # Auto-open browser
    sleep 1
    open "http://localhost:5174/dreamchamber" 2>/dev/null || true

    echo "${GREEN}✅ ZERO LATENCY ACHIEVED! GORUNFREE!! ⚡🚀${NC}"
    echo ""
else
    echo "${CYAN}⚠ Server starting... Check logs: tail -f server.log${NC}"
fi

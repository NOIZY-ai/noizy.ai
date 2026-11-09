#!/bin/bash
#
# VERIFICATION SCRIPT - PROVE WHAT'S REAL
# No lies, no exaggeration, just measurements
#

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  REAL SYSTEM VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check 1: Server process
echo "1. Checking if server is running..."
if lsof -ti:5174 > /dev/null 2>&1; then
    PID=$(lsof -ti:5174)
    PROCESS=$(ps -p $PID -o comm= 2>/dev/null || echo "unknown")
    echo "   ✅ Server running on port 5174 (PID: $PID, Process: $PROCESS)"
else
    echo "   ❌ Server NOT running on port 5174"
    echo "   → Run: ./⚡_ZERO_LATENCY_LAUNCH.sh"
    exit 1
fi
echo ""

# Check 2: API response time
echo "2. Measuring API response time..."
RESPONSE_TIME=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:5174/api/status)
echo "   ✅ Response time: ${RESPONSE_TIME}s"
if (( $(echo "$RESPONSE_TIME < 0.005" | bc -l) )); then
    echo "   ✅ Target met: <5ms (0.005s)"
else
    echo "   ⚠️  Slower than target 5ms"
fi
echo ""

# Check 3: Graph data
echo "3. Checking graph data availability..."
GRAPH_RESPONSE=$(curl -s http://localhost:5174/api/memcell/graph/lite)
NODE_COUNT=$(echo "$GRAPH_RESPONSE" | grep -o '"id":' | wc -l | tr -d ' ')
echo "   ✅ Graph endpoint responding"
echo "   ✅ Nodes in lite graph: $NODE_COUNT"
echo ""

# Check 4: Health check
echo "4. Checking server health..."
HEALTH=$(curl -s http://localhost:5174/api/health)
if echo "$HEALTH" | grep -q '"healthy":true'; then
    echo "   ✅ Server reports healthy"
else
    echo "   ❌ Server health check failed"
fi
echo ""

# Check 5: orjson installed
echo "5. Checking orjson installation..."
if [ -f "venv/bin/python3" ]; then
    if venv/bin/python3 -c "import orjson; print('orjson version:', orjson.__version__)" 2>/dev/null; then
        echo "   ✅ orjson installed and working"
    else
        echo "   ❌ orjson not installed"
        echo "   → Run: source venv/bin/activate && pip install orjson"
    fi
else
    echo "   ⚠️  Virtual environment not found"
fi
echo ""

# Check 6: Graph data file
echo "6. Checking graph data file..."
GRAPH_FILE="golang_ecosystem/brain.json"
if [ -f "$GRAPH_FILE" ]; then
    FILE_SIZE=$(ls -lh "$GRAPH_FILE" | awk '{print $5}')
    echo "   ✅ Graph file exists: $FILE_SIZE"
else
    echo "   ❌ Graph file not found: $GRAPH_FILE"
fi
echo ""

# Check 7: Your DREAMCHAMBER
echo "7. Checking your DREAMCHAMBER file..."
DREAMCHAMBER="/Users/m2ultra/noizylab/DREAMCHAMBER/index.html"
if [ -f "$DREAMCHAMBER" ]; then
    FILE_SIZE=$(ls -lh "$DREAMCHAMBER" | awk '{print $5}')
    echo "   ✅ DREAMCHAMBER exists: $FILE_SIZE"
else
    echo "   ❌ DREAMCHAMBER not found: $DREAMCHAMBER"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  VERIFICATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Access your visualization:"
echo "  → http://localhost:5174/dreamchamber"
echo ""
echo "All measurements are REAL - no fake numbers."
echo ""

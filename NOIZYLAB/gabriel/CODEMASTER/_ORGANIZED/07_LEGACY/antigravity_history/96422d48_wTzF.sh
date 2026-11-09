#!/bin/bash
# GABRIEL SYSTEM OMEGA - Complete Launch Script
# Starts all GABRIEL services including voice and API

GABRIEL_DIR="/Users/m2ultra/NOIZYLAB/GABRIEL"
DREAMCHAMBER_DIR="/Users/m2ultra/noizylab/DREAMCHAMBER"

echo "⚡ GABRIEL SYSTEM OMEGA - LAUNCHING..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Kill any existing processes
pkill -f "gabriel_voice.py" 2>/dev/null
pkill -f "mc96_server.py" 2>/dev/null
lsof -ti:5174 | xargs kill -9 2>/dev/null
lsof -ti:5176 | xargs kill -9 2>/dev/null
sleep 1

# 1. Start GABRIEL API Server (port 5174)
echo "🔧 Starting GABRIEL API Server..."
cd "$GABRIEL_DIR"
nohup python3 mc96_server.py > /tmp/gabriel_api.log 2>&1 &
sleep 2

if curl -s "http://localhost:5174/api/status" > /dev/null 2>&1; then
    echo "   ✅ API Server: http://localhost:5174"
else
    echo "   ⚠️  API Server may be starting..."
fi

# 2. Start Voice Server (port 5176)
echo "🎤 Starting Neural Voice Server..."
nohup python3 "$GABRIEL_DIR/gabriel_voice.py" > /tmp/gabriel_voice.log 2>&1 &
sleep 3

if curl -s "http://localhost:5176/" > /dev/null 2>&1; then
    echo "   ✅ Voice Server: http://localhost:5176"
else
    echo "   ⚠️  Voice Server may be starting..."
fi

# 3. Open Dreamchamber
echo "🌌 Opening Dreamchamber..."
open "http://localhost:5174/dreamchamber"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ GABRIEL SYSTEM OMEGA - ONLINE"
echo ""
echo "📡 API:   http://localhost:5174"
echo "🎤 Voice: http://localhost:5176"
echo "🌌 UI:    http://localhost:5174/dreamchamber"
echo ""

# Announce
sleep 2
curl -s "http://localhost:5176/speak?text=GABRIEL%20System%20Omega%20fully%20operational.%20All%20services%20online." > /dev/null 2>&1 &

echo "🔮 GABRIEL is ready for commands."

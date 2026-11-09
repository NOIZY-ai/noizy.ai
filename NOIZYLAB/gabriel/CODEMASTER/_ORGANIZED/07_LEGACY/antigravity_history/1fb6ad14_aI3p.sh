#!/bin/bash
# GABRIEL SYSTEM OMEGA - Zero Latency Launch
# All services optimized for maximum performance

GABRIEL="/Users/m2ultra/NOIZYLAB/GABRIEL"
PY="$GABRIEL/venv/bin/python3"

echo "⚡ GABRIEL SYSTEM OMEGA - ZERO LATENCY"
echo "═══════════════════════════════════════"

# Kill existing
pkill -f "gabriel_voice.py" 2>/dev/null
pkill -f "mc96_server.py" 2>/dev/null
sleep 1

# Start API (high priority)
echo "🔧 API Server..."
cd "$GABRIEL" && nice -n -10 "$PY" mc96_server.py &
sleep 2

# Start Voice (high priority)
echo "🎤 Voice Server..."
nice -n -10 "$PY" "$GABRIEL/gabriel_voice.py" &
sleep 3

# Status check
echo ""
echo "═══════════════════════════════════════"

API_LAT=$(curl -s -w "%{time_total}" -o /dev/null "http://localhost:5174/api/status" 2>/dev/null)
VOICE_LAT=$(curl -s -w "%{time_total}" -o /dev/null "http://localhost:5176/" 2>/dev/null)

echo "📡 API:   http://localhost:5174  (${API_LAT}s)"
echo "🎤 Voice: http://localhost:5176  (${VOICE_LAT}s)"
echo "🌌 UI:    http://localhost:5174/dreamchamber"
echo ""
echo "⚡ ZERO LATENCY - 100% OPTIMIZED"

# Open Dreamchamber
open "http://localhost:5174/dreamchamber"

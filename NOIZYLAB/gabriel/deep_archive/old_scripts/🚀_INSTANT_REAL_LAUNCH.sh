#!/bin/zsh
# 🚀 INSTANT REAL LAUNCH - ZERO LATENCY
set -e
export TERM=xterm-256color

# Kill existing server
pkill -f "mc96_server" 2>/dev/null || true

# Start optimized server
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || true
python3 mc96_server_optimized.py > server.log 2>&1 &

echo "⚡ ZERO LATENCY SERVER STARTING..."
sleep 2

# Open DREAMCHAMBER
open "http://localhost:5174/dreamchamber" 2>/dev/null || \
xdg-open "http://localhost:5174/dreamchamber" 2>/dev/null || \
echo "Open manually: http://localhost:5174/dreamchamber"

echo "✅ LAUNCHED!"
echo "📊 Server logs: tail -f server.log"

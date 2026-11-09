#!/bin/bash
# GABRIEL SYSTEM STARTUP SCRIPT
# ==============================
# This script handles the environment setup and orchestrates the startup
# of the Gabriel Portal and Signaling Server.

# Set Environment Variables
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export NOIZYLAB_HOME="/Users/m2ultra/NOIZYLAB"
export PYTHON_EXEC="/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/.venv/bin/python3"

# Logging setup
LOG_DIR="$NOIZYLAB_HOME/logs"
mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_DIR/gabriel_service.log") 2>&1

echo "[$(date)] 🚀 GABRIEL SERVICE STARTING..."

# Ensure we are in the right directory
cd "$NOIZYLAB_HOME" || exit 1

# Kill existing instances to prevent zombies/port conflicts
echo "[$(date)] 🧹 Cleaning up previous instances..."
pkill -f "portal_server.py"
pkill -f "signaling_server.py"
sleep 2

# Start Signaling Server (Background)
echo "[$(date)] 📡 Starting WebRTC Signaling Server..."
nohup $PYTHON_EXEC "$NOIZYLAB_HOME/PORTAL/signaling_server.py" > "$LOG_DIR/signaling.log" 2>&1 &
PID_SIGNAL=$!
echo "[$(date)]    PID: $PID_SIGNAL"

# Wait for Signaling Server to initialize
sleep 2

# Start Portal Server (Background)
echo "[$(date)] 🌐 Starting Portal Server..."
export GABRIEL_KEY="noizylab_god_mode_v1"
nohup $PYTHON_EXEC "$NOIZYLAB_HOME/PORTAL/portal_server.py" > "$LOG_DIR/portal.log" 2>&1 &
PID_PORTAL=$!
echo "[$(date)]    PID: $PID_PORTAL"
echo "[$(date)]    KEY: $GABRIEL_KEY"

# Start Cloudflare Tunnel (Quick Tunnel)
echo "[$(date)] 🚇 establishing Cloudflare Tunnel..."
rm -f "$LOG_DIR/tunnel.log"
nohup cloudflared tunnel --url http://localhost:5173 > "$LOG_DIR/tunnel.log" 2>&1 &
PID_TUNNEL=$!
echo "[$(date)]    PID: $PID_TUNNEL"

# Trigger Infinity Link Update (Background)
nohup "$NOIZYLAB_HOME/bin/update_slack_link.sh" > "$LOG_DIR/infinity_link.log" 2>&1 &

# Wait loop
echo "[$(date)] ✅ Services initiated. Monitoring..."
wait $PID_PORTAL

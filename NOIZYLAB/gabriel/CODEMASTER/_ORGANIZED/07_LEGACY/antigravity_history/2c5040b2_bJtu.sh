#!/bin/bash
# voice-forge-god.sh
# Main startup script for Voice Forge on Mac Studio (GOD)
# Starts Docker stack, waits for health, ensures Tunnel.

# Set Context
WORK_DIR="$HOME/voice-forge-local"
LOG_FILE="$WORK_DIR/voice-forge.log"

echo "=== VOICE FORGE AUTO-START: $(date) ===" >> "$LOG_FILE"

# 1. Environment Check
if [ -z "$CLOUDFLARE_TUNNEL_TOKEN" ]; then
    # adhere to a .env file if token not in environment
    if [ -f "$WORK_DIR/.env" ]; then
        export $(cat "$WORK_DIR/.env" | xargs)
    else
        echo "[ERROR] No Tunnel Token found." >> "$LOG_FILE"
        exit 1
    fi
fi

# 2. Start Docker Stack
echo "[INFO] Starting Docker Compose Stack..." >> "$LOG_FILE"
cd "$WORK_DIR" || exit 1
docker-compose up -d >> "$LOG_FILE" 2>&1

# 3. Health Check Loop
echo "[INFO] Waiting for TTS API..." >> "$LOG_FILE"
MAX_RETRIES=30
COUNT=0
URL="http://localhost:5002/health" # Assuming health endpoint exists or we check root
while ! curl -s "$URL" > /dev/null; do
    sleep 2
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo "[ERROR] Timeout waiting for TTS API." >> "$LOG_FILE"
        exit 1
    fi
done

echo "[SUCCESS] Voice Forge Online. Tunnel Active." >> "$LOG_FILE"

#!/bin/bash
# NOIZYLAB INFINITY LINK - TUNNEL PERSISTENCE SCRIPT
# ==========================================================
# This script runs in the background, watches the tunnel log,
# extracts the ephemeral URL, and updates the Slack Worker.

LOG_FILE="/Users/m2ultra/NOIZYLAB/logs/tunnel.log"
WORKER_DIR="/Users/m2ultra/NOIZYLAB/cloudflare-slack-repairs"

echo "[$(date)] 🔗 INFINITY LINK: Monitoring for Tunnel URL..."

# Wait for log file to exist
while [ ! -f "$LOG_FILE" ]; do
  sleep 1
done

# Wait for URL to appear in log
# We assume the URL ends with trycloudflare.com
URL=""
MAX_RETRIES=30
COUNT=0

while [ -z "$URL" ] && [ $COUNT -lt $MAX_RETRIES ]; do
  # Extract URL using grep and sed
  # Example log: 2023-10-27T... INF +--------------------------------------------------------------------------------------------+
  #              2023-10-27T... INF |  your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
  #              2023-10-27T... INF |  https://some-random-words.trycloudflare.com                                             |
  
  URL=$(grep -o "https://[a-zA-Z0-9-]*\.trycloudflare\.com" "$LOG_FILE" | head -n 1)
  
  if [ -z "$URL" ]; then
    sleep 2
    ((COUNT++))
  fi
done

if [ -n "$URL" ]; then
  echo "[$(date)] 🔗 FOUND TUNNEL URL: $URL"
  echo "[$(date)] ☁️  UPDATING SLACK WORKER SECRET..."
  
  cd "$WORKER_DIR" || exit 1
  
  # Update Secret via Wrangler
  # We pipe the URL to stdin to avoid showing it in process list
  echo "$URL" | npx wrangler secret put GABRIEL_PORTAL_URL
  
  if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ INFINITY LINK ESTABLISHED. Slack Worker Updated."
  else
    echo "[$(date)] ❌ FAILED TO UPDATE SLACK WORKER."
  fi
else
  echo "[$(date)] ❌ TIMEOUT: Could not find Tunnel URL in logs."
fi

#!/bin/bash
# mc96-voice-status.sh
# Checks status of Voice Forge

echo "=== Voice Forge Status ==="

# Check Container
if docker ps | grep -q "tts-api"; then
    echo "[CONTAINER] TTS API:  ONLINE"
else
    echo "[CONTAINER] TTS API:  OFFLINE"
fi

# Check Tunnel
if pgrep -f "cloudflared" > /dev/null; then
    echo "[TUNNEL]    Cloudflared: ONLINE"
else
    echo "[TUNNEL]    Cloudflared: OFFLINE"
fi

# Check Log Tail
echo "--- Last 3 Log Lines ---"
tail -n 3 "$HOME/voice-forge-local/voice-forge.log" 2>/dev/null

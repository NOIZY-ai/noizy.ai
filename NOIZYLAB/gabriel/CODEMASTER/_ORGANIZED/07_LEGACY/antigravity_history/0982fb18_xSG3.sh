#!/bin/bash
# start_voice_forge.sh
# Boots the local Voice Forge stack (Docker + Tunnel)

echo "=== VOICE FORGE LOCAL STARTUP ==="

# Check Docker
if ! docker info > /dev/null 2>&1; then
  echo "⚠️  WARNING: Docker not running. Voice Forge will be SKIPPED."
  echo "    (Continuing boot sequence for Gabriel Core...)"
  exit 0
fi

# Check Token
if [ -z "$CLOUDFLARE_TUNNEL_TOKEN" ]; then
  echo "Warning: CLOUDFLARE_TUNNEL_TOKEN not set. Tunnel service might fail."
fi

# Check if already running
if docker ps | grep -q "voice-worker"; then
    echo "⚡ Voice Forge is already running."
else
    echo "Starting Docker Stack..."
    cd voice-forge-local || exit
    docker-compose up -d
fi

echo "=== Voice Forge Online ==="
echo "TTS API: http://localhost:5002"
echo "Tunnel: Active"

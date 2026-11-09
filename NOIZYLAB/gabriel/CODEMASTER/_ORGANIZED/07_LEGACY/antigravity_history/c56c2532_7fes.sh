#!/bin/bash
# start_voice_forge.sh
# Boots the local Voice Forge stack (Docker + Tunnel)

echo "=== VOICE FORGE LOCAL STARTUP ==="

# Check Docker
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker not running."
  exit 1
fi

# Check Token
if [ -z "$CLOUDFLARE_TUNNEL_TOKEN" ]; then
  echo "Warning: CLOUDFLARE_TUNNEL_TOKEN not set. Tunnel service might fail."
fi

echo "Starting Docker Stack..."
cd voice-forge-local
docker-compose up -d

echo "=== Voice Forge Online ==="
echo "TTS API: http://localhost:5002"
echo "Tunnel: Active"

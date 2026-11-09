#!/bin/bash
# turbo_boot_god_mode.sh
# 🚀 GABRIEL GOD MODE LAUNCH SEQUENCER
# Unifies Voice Forge, Server, and Portal into one atomic launch.

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
RESET='\033[0m'

echo -e "${MAGENTA}"
echo "=================================================="
echo "      🌀 GABRIEL SYSTEM: GOD MODE INITIATED      "
echo "=================================================="
echo -e "${RESET}"

# Paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DASHBOARD_DIR="$ROOT_DIR/Audio_Unitor/Dashboard"

# 1. IGNITE VOICE FORGE (Docker)
echo -e "${CYAN}STEP 1: Igniting Voice Forge...${RESET}"
"$ROOT_DIR/start_voice_forge.sh"

# 2. START GABRIEL SERVER
echo -e "${CYAN}STEP 2: Awakening Gabriel Core (Server)...${RESET}"
# Check if port 8080 is in use
if lsof -i :8080 >/dev/null; then
    echo -e "${GREEN}✓ Server is already running on Port 8080.${RESET}"
else
    # Start Server in background
    cd "$DASHBOARD_DIR" || exit
    nohup python3 "$SCRIPT_DIR/turbo_server.py" > "$SCRIPT_DIR/server.log" 2>&1 &
    SERVER_PID=$!
    echo -e "${GREEN}✓ Server ignited (PID: $SERVER_PID). Log: server.log${RESET}"
    
    # Wait for server warmup
    echo "Waiting for core connection..."
    sleep 2
fi

# 3. OPEN PORTAL
echo -e "${CYAN}STEP 3: Opening Portal...${RESET}"
open "http://localhost:8080/portal_index.html"
echo -e "${GREEN}✓ Portal Access Granted.${RESET}"

# 4. TRIGGER GOD MODE
echo -e "${CYAN}STEP 4: ACTIVATING GOD MODE SEQUENCE...${RESET}"
# Give the browser a moment to load so the visual aligns with the sound
sleep 3
cd "$SCRIPT_DIR" || exit
python3 turbo_gabriel.py god_mode

echo -e "${MAGENTA}"
echo "=================================================="
echo "      ✨ SYSTEM STATE: ABSOLUTE PERFECTION ✨      "
echo "=================================================="
echo -e "${RESET}"

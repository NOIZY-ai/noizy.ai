#!/bin/bash
# ============================================================
#
#   ██████╗  ██████╗ ██████╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗
#  ██╔════╝ ██╔═══██╗██╔══██╗    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
#  ██║  ███╗██║   ██║██║  ██║    ██╔████╔██║██║   ██║██║  ██║█████╗  
#  ██║   ██║██║   ██║██║  ██║    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  
#  ╚██████╔╝╚██████╔╝██████╔╝    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗
#   ╚═════╝  ╚═════╝ ╚═════╝     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
#
#   GABRIEL INFINITY: UNIFIED LAUNCH SYSTEM (v3.0)
#   Dual-Boot Architecture: Hypervelocity (BG) + Infinity Kernel (FG)
#
# ============================================================

set -e

# --- CONFIGURATION ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# --- 1. ENVIRONMENT LOADING ---
echo ""
echo -e "${CYAN}[1/5] LOADING ENVIRONMENT...${NC}"

if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo -e "  ${GREEN}Loaded .env file${NC}"
fi

# Fallback checks (User feedback if missing)
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}  WARNING: GEMINI_API_KEY not found (Voice/Vision disabled)${NC}"
fi
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo -e "${YELLOW}  NOTE: ELEVENLABS_API_KEY not found (Using Standard Voice)${NC}"
fi

# --- 2. KERNEL & RAM DISK ---
echo ""
echo -e "${CYAN}[2/5] SYSTEM OPTIMIZATION...${NC}"

if [ "$EUID" -eq 0 ]; then
    # Kernel Tuning
    sysctl -w net.inet.tcp.sendspace=1048576 >/dev/null 2>&1 || true
    sysctl -w kern.maxfiles=65536 >/dev/null 2>&1 || true
    echo -e "  ${GREEN}Kernel Tuned (Root Mode)${NC}"
    
    # RAM Disk
    RAMDISK_NAME="GabrielVol"
    if [ ! -d "/Volumes/${RAMDISK_NAME}" ]; then
        diskutil erasevolume APFS "${RAMDISK_NAME}" $(hdiutil attach -nomount ram://131072000) >/dev/null
        mkdir -p "/Volumes/${RAMDISK_NAME}/cache" "/Volumes/${RAMDISK_NAME}/models"
        echo -e "  ${GREEN}RAM Disk Created (64GB)${NC}"
    else
        echo -e "  ${GREEN}RAM Disk Active${NC}"
    fi
else
    echo -e "  ${YELLOW}Skipped Kernel/RAM Disk (Run with sudo for max performance)${NC}"
fi

# --- 3. PYTHON ENVIRONMENT ---
echo ""
echo -e "${CYAN}[3/5] RUNTIME ENVIRONMENT...${NC}"

if [ ! -d "venv" ]; then
    echo "  Creating venv..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q uvloop orjson fastapi uvicorn websockets sounddevice mido numpy google-genai elevenlabs
else
    source venv/bin/activate
fi
echo -e "  ${GREEN}Virtual Environment Active${NC}"

# --- 4. CLEANUP ---
echo ""
echo -e "${CYAN}[4/5] PROCESS CLEANUP...${NC}"
pkill -f "gabriel_hypervelocity" 2>/dev/null || true
pkill -f "gabriel_infinity" 2>/dev/null || true
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
echo -e "  ${GREEN}Ports Cleared${NC}"

# --- 5. DUAL BOOT ---
echo ""
echo -e "${CYAN}[5/5] IGNITING DUAL-CORE ENGINE...${NC}"

# TRAP: Ensure Server dies when Kernel exits
trap "kill 0" EXIT

# A. LAUNCH SERVER (BACKGROUND)
echo -e "  ${YELLOW}Starting Hypervelocity Server (HTTPS/WSS)...${NC}"
# Use uvicorn with SSL for iOS compatibility
python3 -m uvicorn core.gabriel_hypervelocity:app --host 0.0.0.0 --port 8000 --ssl-keyfile configs/key.pem --ssl-certfile configs/cert.pem > hypervelocity.log 2>&1 &
SERVER_PID=$!

# Wait for Health Check
echo -n "  Waiting for Server Connection..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health >/dev/null; then
        echo -e "${GREEN} OK${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# --- 5. UNIVERSE FLOW (WATCHER & DASHBOARD) ---
echo ""
echo -e "${CYAN}[5/7] IGNITING UNIVERSE FLOW...${NC}"

# Kill existing to prevent duplicates
pkill -f "visual_scanner.py" || true
pkill -f "streamlit run app.py" || true

# Launch Watcher in Background
echo -e "  ${GREEN}Starting Fishnet (Watch Mode)...${NC}"
# CHECK FOR GO CORE
if [ -f "core/go_core/fishnet" ]; then
    echo -e "  🚀 GO-VELOCITY CORE DETECTED"
    cd core/go_core
    nohup ./fishnet > /dev/null 2>&1 &
    cd ../..
else
    echo -e "  ⚠️ FALBACK TO PYTHON SCANNER"
    nohup python3 core/visual_scanner.py --watch > /dev/null 2>&1 &
fi
SCANNER_PID=$!
echo -e "  PID: $SCANNER_PID"

# Launch Dashboard in Background
echo -e "  ${GREEN}Starting Universal Dashboard...${NC}"
nohup streamlit run ../app.py > /dev/null 2>&1 &
DASH_PID=$!
echo -e "  PID: $DASH_PID"

echo ""
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          ⚡ GABRIEL SYSTEM OMEGA: FLOW STATE ONLINE  ⚡      ║"
echo "║                                                              ║"
echo "║   DASHBOARD:    http://localhost:8501                        ║"
echo "║   WATCHER:      ACTIVE (PID $SCANNER_PID)                        ║"
echo "║   SERVER:       ACTIVE (PID $SERVER_PID)                        ║"
echo "║   KERNEL:       READY                                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# VOICE ANNOUNCEMENT
curl -X POST -H "Content-Type: application/json" -d '{"text": "Gabriel Omega System Online. Infinite Energy Detected."}' http://localhost:8000/api/speak > /dev/null 2>&1 &

# B. LAUNCH KERNEL (FOREGROUND / INTERACTIVE)
# The script will wait here until "exit" is typed in Infinity
python3 core/gabriel_infinity.py

# Cleanup handled by trap
echo ""
echo -e "${RED}SYSTEM SHUTDOWN${NC}"

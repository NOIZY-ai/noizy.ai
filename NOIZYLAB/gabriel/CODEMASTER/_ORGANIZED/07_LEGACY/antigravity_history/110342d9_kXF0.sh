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
#   GABRIEL M2 ULTRA GOD MODE LAUNCHER
#   Full Stack: Kernel + RAM Disk + Hypervelocity + Web Interface
#
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║         ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗       ║"
echo "║        ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║       ║"
echo "║        ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║       ║"
echo "║        ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║       ║"
echo "║        ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗  ║"
echo "║         ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝  ║"
echo "║                                                              ║"
echo "║                    ⚡ GOD MODE v1.0 ⚡                        ║"
echo "║                                                              ║"
echo "║    M2 ULTRA • 192GB UNIFIED • 24-CORE GPU • 76-CORE CPU     ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# ============================================================
# CHECK REQUIREMENTS
# ============================================================
echo -e "${YELLOW}[1/6] CHECKING REQUIREMENTS...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 not found${NC}"
    exit 1
fi
echo "  Python: $(python3 --version)"

# Check for API keys
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}  WARNING: GEMINI_API_KEY not set${NC}"
    echo -e "  Set with: export GEMINI_API_KEY='your-key'"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}  INFO: OPENAI_API_KEY not set (optional fallback)${NC}"
fi

echo ""

# ============================================================
# KERNEL TUNING (if sudo)
# ============================================================
echo -e "${YELLOW}[2/6] KERNEL TUNING...${NC}"

if [ "$EUID" -eq 0 ]; then
    echo "  Running as root - applying kernel optimizations..."
    
    # Network stack
    sysctl -w net.inet.tcp.sendspace=1048576 >/dev/null 2>&1 || true
    sysctl -w net.inet.tcp.recvspace=1048576 >/dev/null 2>&1 || true
    sysctl -w kern.ipc.maxsockbuf=16777216 >/dev/null 2>&1 || true
    sysctl -w net.inet.tcp.delayed_ack=0 >/dev/null 2>&1 || true
    echo "    TCP buffers: 1MB"
    echo "    Socket buffer: 16MB"
    echo "    Delayed ACK: DISABLED"
    
    # File descriptors
    sysctl -w kern.maxfiles=65536 >/dev/null 2>&1 || true
    sysctl -w kern.maxfilesperproc=32768 >/dev/null 2>&1 || true
    echo "    Max files: 65536"
    
    # GPU memory
    sysctl -w iogpu.wired_limit_mb=128000 >/dev/null 2>&1 || true
    echo "    GPU wired: 128GB"
    
    echo -e "  ${GREEN}KERNEL TUNED${NC}"
else
    echo -e "  ${YELLOW}Skipped (run with sudo for kernel tuning)${NC}"
fi

echo ""

# ============================================================
# RAM DISK
# ============================================================
echo -e "${YELLOW}[3/6] RAM DISK...${NC}"

RAMDISK_NAME="GabrielVol"
RAMDISK_SIZE_MB=65536  # 64GB

if [ "$EUID" -eq 0 ]; then
    if [ ! -d "/Volumes/${RAMDISK_NAME}" ]; then
        echo "  Creating 64GB RAM disk..."
        RAMDISK_SECTORS=$((RAMDISK_SIZE_MB * 2048))
        DEVICE=$(hdiutil attach -nomount ram://${RAMDISK_SECTORS})
        diskutil erasevolume APFS "${RAMDISK_NAME}" ${DEVICE} >/dev/null
        
        # Create directories
        mkdir -p "/Volumes/${RAMDISK_NAME}/cache"
        mkdir -p "/Volumes/${RAMDISK_NAME}/temp"
        mkdir -p "/Volumes/${RAMDISK_NAME}/audio"
        mkdir -p "/Volumes/${RAMDISK_NAME}/models"
        
        echo -e "  ${GREEN}RAM DISK CREATED: /Volumes/${RAMDISK_NAME}${NC}"
    else
        echo -e "  ${GREEN}RAM DISK EXISTS: /Volumes/${RAMDISK_NAME}${NC}"
    fi
else
    if [ -d "/Volumes/${RAMDISK_NAME}" ]; then
        echo -e "  ${GREEN}RAM DISK EXISTS: /Volumes/${RAMDISK_NAME}${NC}"
    else
        echo -e "  ${YELLOW}Skipped (run with sudo to create RAM disk)${NC}"
    fi
fi

echo ""

# ============================================================
# VIRTUAL ENVIRONMENT
# ============================================================
echo -e "${YELLOW}[4/6] VIRTUAL ENVIRONMENT...${NC}"

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Core dependencies
echo "  Installing dependencies..."
pip install -q \
    uvloop \
    orjson \
    httptools \
    google-genai \
    google-generativeai \
    fastapi \
    'uvicorn[standard]' \
    websockets \
    numpy \
    python-multipart \
    sounddevice \
    mido \
    2>/dev/null || true

# Try MLX (Apple Silicon)
pip install -q mlx mlx-lm 2>/dev/null || echo "  MLX: Not available on this platform"

echo -e "  ${GREEN}ENVIRONMENT READY${NC}"
echo ""

# ============================================================
# KILL EXISTING PROCESSES
# ============================================================
echo -e "${YELLOW}[5/6] CLEANING UP...${NC}"

pkill -f "gabriel_hypervelocity" 2>/dev/null || true
pkill -f "gabriel_hyper_local" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

sleep 1
echo -e "  ${GREEN}CLEANUP COMPLETE${NC}"
echo ""

# ============================================================
# LAUNCH GABRIEL
# ============================================================
echo -e "${YELLOW}[6/6] LAUNCHING GABRIEL...${NC}"
echo ""

# Determine which mode to use
if [ -n "$GEMINI_API_KEY" ]; then
    MODE="CLOUD"
    SCRIPT="core/gabriel_hypervelocity.py"
else
    MODE="LOCAL"
    SCRIPT="core/gabriel_hyper_local.py"
fi

echo -e "  Mode: ${CYAN}${MODE}${NC}"
echo ""

# Launch in background
python3 $SCRIPT &
GABRIEL_PID=$!

# Set priority if root
if [ "$EUID" -eq 0 ]; then
    renice -20 -p $GABRIEL_PID 2>/dev/null || true
    taskpolicy -c interactive -p $GABRIEL_PID 2>/dev/null || true
    echo "  Priority: REAL-TIME"
fi

sleep 2

# Check if running
if kill -0 $GABRIEL_PID 2>/dev/null; then
    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              ⚡ GOD MODE ACTIVATED ⚡                        ║"
    echo "║                                                              ║"
    echo "║  PID:          $GABRIEL_PID                                          ║"
    echo "║  Mode:         $MODE                                         ║"
    echo "║  Interface:    http://localhost:8000                         ║"
    echo "║  WebSocket:    ws://localhost:8000/ws/hypervelocity          ║"
    echo "║  RAM Disk:     /Volumes/GabrielVol                           ║"
    echo "║                                                              ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                                                              ║"
    echo "║  FEATURES:                                                   ║"
    echo "║    • Gemini 2.0 Flash Live API                               ║"
    echo "║    • OpenAI Realtime (fallback)                              ║"
    echo "║    • MLX Local LLM (70B/8B)                                  ║"
    echo "║    • Metal FFT Audio Analysis                                ║"
    echo "║    • 3D Avatar with Lip Sync                                 ║"
    echo "║    • Camera + Microphone Input                               ║"
    echo "║    • Google Search Grounding                                 ║"
    echo "║    • Creative Arsenal (Video/Audio/Image)                    ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Press Ctrl+C to stop"
    echo ""
    
    # Wait for process
    wait $GABRIEL_PID
else
    echo -e "${RED}ERROR: Gabriel failed to start${NC}"
    exit 1
fi

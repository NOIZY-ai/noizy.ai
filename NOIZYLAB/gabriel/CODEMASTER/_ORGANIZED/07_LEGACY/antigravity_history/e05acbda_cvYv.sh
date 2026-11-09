#!/bin/bash
# ============================================================
# GABRIEL INFINITY LAUNCHER
# The Temporal Operating System
# GORUNFREE - Limits Removed
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ██╗███╗   ██╗███████╗██╗███╗   ██╗██╗████████╗██╗   ██╗   ║"
echo "║   ██║████╗  ██║██╔════╝██║████╗  ██║██║╚══██╔══╝╚██╗ ██╔╝   ║"
echo "║   ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║   ██║    ╚████╔╝    ║"
echo "║   ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║   ██║     ╚██╔╝     ║"
echo "║   ██║██║ ╚████║██║     ██║██║ ╚████║██║   ██║      ██║      ║"
echo "║   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝      ║"
echo "║                                                              ║"
echo "║              GABRIEL TEMPORAL OPERATING SYSTEM               ║"
echo "║                       GORUNFREE                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check/Create venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q uvloop orjson numpy sounddevice mido 2>/dev/null || true
pip install -q mlx mlx-lm 2>/dev/null || echo "MLX: Not available"
pip install -q audiocraft 2>/dev/null || echo "AudioCraft: Not available"

# Check RAM disk
if [ ! -d "/Volumes/GabrielVol" ]; then
    echo ""
    echo "WARNING: RAM disk not found"
    echo "Creating local cache directory..."
    mkdir -p ~/.gabriel/cache
    export GABRIEL_VOL="$HOME/.gabriel/cache"
else
    export GABRIEL_VOL="/Volumes/GabrielVol"
fi

echo ""
echo "Configuration:"
echo "  Cache: $GABRIEL_VOL"
echo "  uvloop: $(python3 -c 'import uvloop; print("OK")' 2>/dev/null || echo "Not found")"
echo "  orjson: $(python3 -c 'import orjson; print("OK")' 2>/dev/null || echo "Not found")"
echo "  MLX: $(python3 -c 'import mlx; print("OK")' 2>/dev/null || echo "Not found")"
echo ""

# Launch
echo "Launching GABRIEL INFINITY..."
echo ""

python3 core/gabriel_infinity.py

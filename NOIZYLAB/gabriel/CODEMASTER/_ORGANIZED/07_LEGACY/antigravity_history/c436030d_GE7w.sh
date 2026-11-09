#!/bin/bash
# ============================================================
# GABRIEL HYPERVELOCITY LAUNCHER (P-CORE PRIORITY)
# Sets real-time priority and forces P-cores on M2 Ultra
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo ""
echo "========================================"
echo "  GABRIEL HYPERVELOCITY LAUNCHER"
echo "  P-Core Priority + Real-time Scheduling"
echo "========================================"
echo ""

# Check for venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q uvloop orjson numpy sounddevice mido 2>/dev/null || true

# Try to install MLX (Apple Silicon only)
pip install -q mlx mlx-lm 2>/dev/null || echo "MLX not available on this platform"

# Check RAM disk
if [ ! -d "/Volumes/GabrielVol" ]; then
    echo ""
    echo "WARNING: RAM disk not mounted"
    echo "Run: sudo ./configs/m2_ultra_kernel.sh"
    echo ""
fi

# Launch Gabriel in background
echo ""
echo "Launching GABRIEL..."
python3 core/gabriel_hyper_local.py &
GABRIEL_PID=$!

echo "GABRIEL LAUNCHED (PID: $GABRIEL_PID)"

# Set real-time priority (requires sudo for full effect)
if [ "$EUID" -eq 0 ]; then
    echo "Setting real-time priority..."
    renice -20 -p $GABRIEL_PID 2>/dev/null || true
    
    # Force interactive QoS (keeps on P-cores)
    taskpolicy -c interactive -p $GABRIEL_PID 2>/dev/null || true
    
    echo "Priority: REAL-TIME (-20)"
    echo "QoS: INTERACTIVE (P-cores)"
else
    echo ""
    echo "TIP: Run with sudo for maximum priority:"
    echo "  sudo ./configs/run_hyper_local.sh"
fi

echo ""
echo "Press Ctrl+C to stop"
echo ""

# Wait for process
wait $GABRIEL_PID

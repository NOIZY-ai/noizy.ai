#!/usr/bin/env bash
# ============================================================
# GABRIEL HYPERVELOCITY LAUNCHER
# Zero Latency • uvloop • orjson • GC Frozen
# ============================================================

cd "$(dirname "$0")/.."

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ⚡ GABRIEL HYPERVELOCITY ⚡                      ║"
echo "║                                                              ║"
echo "║    Zero Latency • uvloop • orjson • GC Frozen                ║"
echo "║    High-Frequency Trading Grade Optimization                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check for venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install hypervelocity dependencies
echo "📦 Installing HYPERVELOCITY dependencies..."
pip install -q -U \
    uvloop \
    orjson \
    httptools \
    google-genai \
    fastapi \
    'uvicorn[standard]' \
    websockets \
    numpy \
    python-multipart

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "⚠️  GEMINI_API_KEY not set!"
    echo "   Set with: export GEMINI_API_KEY='your-key'"
    echo ""
fi

# Optional: Kernel tuning (requires sudo)
if [ "$1" == "--kernel" ]; then
    echo "🔧 Running kernel tuning (requires sudo)..."
    sudo ./configs/hypervelocity_kernel.sh
fi

# Launch
echo ""
echo "🚀 IGNITING HYPERVELOCITY ENGINE..."
echo "   Interface: http://localhost:8000"
echo "   WebSocket: ws://localhost:8000/ws/hypervelocity"
echo ""

python3 core/gabriel_hypervelocity.py

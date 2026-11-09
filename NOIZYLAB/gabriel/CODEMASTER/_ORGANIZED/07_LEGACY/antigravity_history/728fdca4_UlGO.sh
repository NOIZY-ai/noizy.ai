#!/bin/bash
# GABRIEL V1 - Launch Script
# Optimized for M2 Ultra

cd "$(dirname "$0")"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗       ║"
echo "║        ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║       ║"
echo "║        ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║       ║"
echo "║        ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║       ║"
echo "║        ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗  ║"
echo "║         ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝  ║"
echo "║                                                              ║"
echo "║                         V1.0                                 ║"
echo "║              M2 ULTRA • GEMINI 2.0 FLASH                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check for venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -U google-genai fastapi uvicorn[standard] websockets numpy python-multipart

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "⚠️  WARNING: GEMINI_API_KEY not set!"
    echo "   Set it with: export GEMINI_API_KEY='your-key'"
    echo "   Get a key at: https://aistudio.google.com"
    echo ""
fi

# Launch
echo ""
echo "🚀 IGNITION..."
echo "   Interface: http://localhost:8000"
echo ""

python3 gabriel_core.py

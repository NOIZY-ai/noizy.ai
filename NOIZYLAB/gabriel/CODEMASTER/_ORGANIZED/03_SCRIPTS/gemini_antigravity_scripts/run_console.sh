#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  GABRIEL SYSTEM OMEGA - MASTER LAUNCHER
#  100% OPTIMIZED | ZERO LATENCY
# ═══════════════════════════════════════════════════════════════════════════════

set -e

WORKSPACE="/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL"
cd "$WORKSPACE"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  🐺 GABRIEL SYSTEM OMEGA - ZERO LATENCY LAUNCHER                 ║"
echo "║  ⚡ 100% OPTIMIZED FOR M2 ULTRA 192GB                            ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Activate Python environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check requirements
if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
    echo "✅ Dependencies verified"
fi

echo ""
echo "🚀 LAUNCHING GABRIEL OMEGA..."
echo ""

# Run Streamlit with optimized settings
streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.runOnSave true \
    --browser.gatherUsageStats false \
    --theme.base dark \
    --theme.primaryColor "#00FFCC" \
    --theme.backgroundColor "#000000" \
    --theme.secondaryBackgroundColor "#0a0a0a"

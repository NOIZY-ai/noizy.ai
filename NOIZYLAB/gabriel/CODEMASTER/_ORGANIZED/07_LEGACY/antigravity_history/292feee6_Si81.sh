#!/bin/bash
# NOIZYLAB CODEMASTER LAUNCHER
# Run with: ./launch.sh

cd "$(dirname "$0")"

echo "⚔️ STARTING GABRIEL SYSTEM OMEGA"
echo "================================"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Installing streamlit..."
    pip3 install streamlit google-generativeai
fi

# Launch console
streamlit run core/console.py --server.port 8501

echo "⚔️ GORUNFREE"

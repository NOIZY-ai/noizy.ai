#!/bin/bash
# NOIZYLAB LAUNCHER - GORUNFREE
set -e

echo "🔥 NOIZYLAB MASTER CELL"
echo "========================"

cd "$(dirname "$0")"

# Check for venv
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Install deps if needed
pip install -q -r requirements.txt 2>/dev/null || true

# Launch
if [ "$1" == "console" ]; then
    streamlit run ../AI_COMPLETE_BRAIN/noizylab_console.py
elif [ "$1" == "test" ]; then
    python -c "from core import create_chamber; print('✅ Master Cell OK')"
else
    echo "Usage: ./launch.sh [console|test]"
    echo ""
    echo "  console  - Launch Streamlit console"
    echo "  test     - Test Master Cell import"
fi

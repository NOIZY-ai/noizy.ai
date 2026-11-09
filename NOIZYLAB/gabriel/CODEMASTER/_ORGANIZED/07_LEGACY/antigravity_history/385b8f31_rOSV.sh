#!/bin/zsh
#
# 🩺 SYSTEM DOCTOR LAUNCHER
# Part of GABRIEL SYSTEM OMEGA - MC96DIGIUNIVERSE
#
# Usage:
#   ./launcher.sh              # Full scan
#   ./launcher.sh --disk       # Disk scan only
#   ./launcher.sh --export     # Full scan with JSON export
#

SCRIPT_DIR="${0:A:h}"
cd "$SCRIPT_DIR"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    exit 1
fi

# Check for Rich (optional but recommended)
if ! python3 -c "import rich" 2>/dev/null; then
    echo "⚠️  Rich not installed. Install for better output: pip3 install rich"
    echo ""
fi

# Run System Doctor
python3 -m modules.cli "$@"

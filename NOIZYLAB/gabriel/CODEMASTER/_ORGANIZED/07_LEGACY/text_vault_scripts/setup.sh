#!/bin/bash
# GABRIEL File Suite - Quick Setup Script
# Prepares environment and installs dependencies

set -e

echo "=========================================="
echo "GABRIEL File Suite - Setup"
echo "=========================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GABRIEL_HOME="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$GABRIEL_HOME"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Copy config: cp config/config.example.yaml config/config.yaml"
echo "3. Edit config.yaml with your settings"
echo "4. Set API key (if using AI): export ANTHROPIC_API_KEY='your-key'"
echo "5. Run first scan: ./gabriel.py scan /Volumes/GABRIEL --database gabriel.db"
echo ""
echo "Optional - Start dashboard:"
echo "  API:       python dashboard/api.py"
echo "  Streamlit: streamlit run dashboard/streamlit_app.py"
echo ""
echo "Optional - Setup automation:"
echo "  chmod +x scripts/nightly_automation.sh"
echo "  crontab -e"
echo "  Add: 0 2 * * * /path/to/scripts/nightly_automation.sh"
echo ""

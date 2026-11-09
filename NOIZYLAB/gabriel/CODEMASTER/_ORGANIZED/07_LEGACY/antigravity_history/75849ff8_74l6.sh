#!/bin/bash

# NOIZYLAB ENVIRONMENT SETUP
# Purpose: Create a clean Python Virtual Environment (venv) to bypass system lock (PEP 668).

echo ">>> INITIATING NOIZYLAB ENVIRONMENT PROTOCOL..."

# 1. Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "    -> Creating virtual environment 'venv'..."
    python3 -m venv venv
else
    echo "    -> 'venv' detected. Proceeding..."
fi

# 2. Activate venv
echo "    -> Activating venv..."
source venv/bin/activate

# 3. Upgrade pip
echo "    -> Upgrading core tools..."
pip install --upgrade pip

# 4. Install Dependencies
echo "    -> Installing NOIZYLAB INTELLIGENCE (Anthropic, Spleeter, Whisper)..."
# We handle the complex installs step-by-step to avoid freezing
pip install python-dotenv anthropic numpy librosa soundfile

echo "    -> Installing Heavy Weights (This may take a moment)..."
pip install openai-whisper moviepy spleeter pandas

# Note: AudioCraft is git-based, installing separately to ensure it works
echo "    -> Installing Meta AudioCraft..."
# pip install git+https://github.com/facebookresearch/audiocraft.git

echo ""
echo ">>> SETUP COMPLETE."
echo ">>> TO ACTIVATE THE LAB, RUN:"
echo "    source venv/bin/activate"
echo "    python3 mission_control_v8.py"
python3 -c "import sys; print(f'>>> Python Core Active: {sys.executable}')"

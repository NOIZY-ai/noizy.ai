#!/bin/bash
# Startup script for NoizyLab Console
cd "$(dirname "$0")"

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Checking and installing dependencies..."
pip install -r requirements.txt

# Run the app
echo "Launching NOIZYLAB CONSOLE..."
streamlit run app.py

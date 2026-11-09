#!/bin/bash
echo "🧹 CLEANING GABRIEL PROCESSES..."
pkill -f "visual_scanner.py"
pkill -f "streamlit run app.py"
pkill -f "gabriel_infinity.py"
echo "✅ All Systems Halted."

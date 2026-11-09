#!/bin/bash
# ==============================================================================
# ⛩️  THE TRUTH GATE: GABRIEL STARTUP SEQUENCE
# ==============================================================================
# "One Truth. One Source. Zero Friction."

# 1. Environment Setup
export PYTHONPATH=$PYTHONPATH:$(pwd)/Audio_Unitor/Scripts
export DEVICE_NAME="M2_ULTRA_GOD_MODE"

# 2. Safety Checks
if [ ! -d "/Volumes/GabrielVol" ]; then
    echo "⚠️  RAM Disk 'GabrielVol' not found!"
    echo "    Creating it now..."
    diskutil erasevolume HFS+ "GabrielVol" `hdiutil attach -nomount ram://134217728`
fi

# 3. Launch Gabriel
echo "💎 OPENING THE TRUTH GATE..."
echo "⚡ SYSTEM: GABRIEL OMEGA"
echo "🧠 CORTEX: LLAMA-3-70B (4-bit)"
echo "👂 EARS:   UNIVERSAL AUDIO APOLLO"
echo "=============================================================================="

python3 Audio_Unitor/Scripts/turbo_gabriel_omega.py

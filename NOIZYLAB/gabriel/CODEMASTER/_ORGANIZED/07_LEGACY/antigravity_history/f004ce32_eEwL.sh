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

# 3. Launch The Carrier (Discord Bot)
if [ -n "$DISCORD_TOKEN" ]; then
    echo "🦅 LAUNCHING THE CARRIER (Discord Relay)..."
    python3 Audio_Unitor/Scripts/turbo_discord.py &
    CARRIER_PID=$!
else
    echo "⚠️  DISCORD_TOKEN not set. The Carrier will remain dormant."
fi

# 4. Launch The Hive Backend (Server)
echo "🧬 ACTIVATING THE HIVE (API Server)..."
python3 Audio_Unitor/Scripts/turbo_server.py &
SERVER_PID=$!

# 5. Launch Volume Sentinel (Dynamic Mount Watcher)
echo "🛡️  ACTIVATING SENTINEL (Watching /Volumes)..."
python3 Audio_Unitor/Scripts/turbo_sentinel.py /Volumes &
SENTINEL_PID=$!

# 6. Launch Gabriel (The Brain) - Foreground
echo "💎 OPENING THE TRUTH GATE..."
echo "⚡ SYSTEM: GABRIEL OMEGA"
echo "🧠 CORTEX: LLAMA-3-70B (4-bit)"
echo "👂 EARS:   UNIVERSAL AUDIO APOLLO"
echo "=============================================================================="

# Trap Ctrl+C to kill background processes
trap "kill $CARRIER_PID $SERVER_PID $SENTINEL_PID; exit" INT

python3 Audio_Unitor/Scripts/turbo_gabriel_omega.py

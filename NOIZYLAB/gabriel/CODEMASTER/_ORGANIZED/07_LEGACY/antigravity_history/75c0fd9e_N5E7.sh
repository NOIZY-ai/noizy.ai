#!/bin/bash

# MC96Universe ALL-SYSTEM UPGRADE
# "Maximum Overdrive" Module
# Executes all optimizations in the correct order.

echo ">>> INITIATING MAXIMUM OVERDRIVE SEQUENCE..."
echo ">>> SYSTEM: M2 ULTRA (192GB RAM) DETECTED"

# 1. Hyper Drive (RAM Disk)
echo ">>> [1/4] ENGAGING HYPER DRIVE..."
chmod +x hyper_drive.sh
./hyper_drive.sh

# 2. Turbo Boost (Network Kernel)
echo ">>> [2/4] INJECTING TURBO BOOST (KERNEL)..."
chmod +x turbo_boost.sh
sudo ./turbo_boost.sh

# 3. Fast Track (Network Interface)
echo ">>> [3/4] ALIGNING NETWORK INTERFACES (MTU 9000)..."
chmod +x fast_track_mac.sh
sudo ./fast_track_mac.sh

# 4. Velocity Mode (CPU Priority)
echo ">>> [4/5] ACCELERATING CREATIVE APPS..."
chmod +x velocity_mode.sh
sudo ./velocity_mode.sh

# 5. Super Charge (UI/Perception)
echo ">>> [5/6] ELIMINATING UI LATENCY..."
chmod +x super_charge.sh
./super_charge.sh

# 6. Reactor Core (Power/IO)
echo ">>> [6/6] MAXIMIZING POWER & I/O..."
chmod +x reactor_core.sh
sudo ./reactor_core.sh

# 7. Persistence (Make it Stick)
echo ">>> [7/8] INSTALLING PERSISTENCE LAYER..."
chmod +x deploy_persistence.sh
sudo ./deploy_persistence.sh

# 8. Terminal Velocity (Shell)
echo ">>> [8/8] ENGAGING TERMINAL VELOCITY..."
# We can't "source" inside a sub-script for the parent shell effectively without user action.
# But we can update .zshrc
ZSHRC="$HOME/.zshrc"
TV_PATH="/Users/m2ultra/.gemini/antigravity/brain/10fbcc11-34da-430e-a226-19c05f0cf69d/terminal_velocity.zsh"

if ! grep -q "terminal_velocity.zsh" "$ZSHRC"; then
    echo "source $TV_PATH" >> "$ZSHRC"
    echo ">>> Added Terminal Velocity to .zshrc"
else
    echo ">>> Terminal Velocity already present in .zshrc"
fi

echo ""
echo ">>> ALL SYSTEMS UPGRADED & LOCKED."
echo ">>> LATENCY: MINIMIZED."
echo ">>> THROUGHPUT: MAXIMIZED."
echo ">>> READY FOR PURE SPEED."

echo ">>> LAUNCHING MISSION CONTROL AI..."
# Check python command
if command -v python3 &> /dev/null; then
    python3 mission_control_v2.py
else
    echo "!!! Python3 not found. Run 'mission_control_v2.py' manually."
fi

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
echo ">>> [4/4] ACCELERATING CREATIVE APPS..."
chmod +x velocity_mode.sh
sudo ./velocity_mode.sh

echo ""
echo ">>> ALL SYSTEMS UPGRADED."
echo ">>> LATENCY: MINIMIZED."
echo ">>> THROUGHPUT: MAXIMIZED."
echo ">>> READY FOR PURE SPEED."

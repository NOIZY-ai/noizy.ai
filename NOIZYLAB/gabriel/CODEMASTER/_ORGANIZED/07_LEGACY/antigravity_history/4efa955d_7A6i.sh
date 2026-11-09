#!/bin/bash

# Network Healing Script - Enable Jumbo Frames
# Targets specific interfaces identified as having MTU 1500

echo "Healing the Network... Engaging Jumbo Frames (MTU 9000)"

# Interfaces to update
INTERFACES=("en15" "en16" "en17" "en18")

for INTF in "${INTERFACES[@]}"; do
    echo "Configuring $INTF..."
    if sudo networksetup -setMTU "$INTF" 9000; then
        echo "✅ $INTF set to 9000"
    else
        echo "❌ Failed to set $INTF (Hardware might not support 9000 or sudo required)"
    fi
done

# Verification
echo "---------------------------------------------------"
echo "Verification Status:"
networksetup -getMTU en0
networksetup -getMTU en12
networksetup -getMTU en13
networksetup -getMTU en14
for INTF in "${INTERFACES[@]}"; do
    networksetup -getMTU "$INTF"
done
echo "---------------------------------------------------"
echo "MC96UNIVERSE High Speed Transfer Mode: PARTIALLY ENGAGED (Local Mac)"
echo "Please ensure DGS1210-10 Switch is also configured via Web Interface."

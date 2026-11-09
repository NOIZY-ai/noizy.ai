#!/bin/bash

# MC96Universe Fast Track Script for macOS
# "AI Intuition" Module: Detects active high-speed link and maximizes throughput.

echo ">>> MC96Universe AI System Initializing..."
echo ">>> Scanning for TCAT Cables..."

# Detect the active network interface (excluding loopback, awdl, etc.)
# We look for the interface with the default route first, as that is likely the primary connection.
GATEWAY_IFACE=$(netstat -rn | grep default | grep en | head -1 | awk '{print $4}')

if [ -z "$GATEWAY_IFACE" ]; then
    echo "!!! Warning: No active internet connection detected on standard interfaces."
    echo ">>> Scanning for any connected Ethernet port..."
    # Fallback: Find any service named "Ethernet"
    SERVICE_NAME=$(networksetup -listallnetworkservices | grep "Ethernet" | head -1)
else
    # Get the friendly name for the interface
    SERVICE_NAME=$(networksetup -listnetworkserviceorder | grep -B 1 "$GATEWAY_IFACE" | head -1 | cut -d' ' -f2-)
    # Remove trailing comma if present from the cut command
    SERVICE_NAME="${SERVICE_NAME%,}"
    # Cleaning up the name might be tricky depending on output format, let's try a safer way.
    # Actually, simpler approach: iterate services and check device.
    FOUND_SERVICE=""
    while read -r line; do
        if [[ $line != *"*"* ]]; then
            S_NAME=$line
            DEVICE=$(networksetup -getnetworkserviceenabled "$S_NAME" 2>/dev/null)
            if [ "$DEVICE" == "Enabled" ]; then
                 DEV_ID=$(networksetup -listallhardwareports | grep -A 1 "$S_NAME" | grep "Device" | awk '{print $2}')
                 if [ "$DEV_ID" == "$GATEWAY_IFACE" ]; then
                     FOUND_SERVICE="$S_NAME"
                     break
                 fi
            fi
        fi
    done <<< "$(networksetup -listallnetworkservices)"
    SERVICE_NAME="$FOUND_SERVICE"
fi

if [ -z "$SERVICE_NAME" ]; then
    echo "!!! CRITICAL FAILURE: No suitable Ethernet interface found."
    echo "!!! Manual intervention required."
    exit 1
fi

echo ">>> Target Aquired: $SERVICE_NAME ($GATEWAY_IFACE)"
echo ">>> Engaging JUMBO FRAMES..."

# Check current MTU
CURRENT_MTU=$(networksetup -getMTU "$SERVICE_NAME" | awk '{print $3}')
echo ">>> Current MTU: $CURRENT_MTU"

if [ "$CURRENT_MTU" == "9000" ]; then
    echo ">>> System already optimized for Super-Sonic speeds."
    exit 0
fi

# Set MTU to 9000
echo ">>> Applying Neural Optimization (MTU 9000)..."
# Using sudo since networksetup requires admin privileges for changing settings
# In an actual deployment, user would need to input password or run as root.
sudo networksetup -setMTU "$SERVICE_NAME" 9000

# Verify
NEW_MTU=$(networksetup -getMTU "$SERVICE_NAME" | awk '{print $3}')
if [ "$NEW_MTU" == "9000" ]; then
    echo ">>> SUCCESS: JUMBO FRAMES ACTIVE."
    echo ">>> The MC96Universe is ready."
else
    echo "!!! ERROR: Failed to set MTU. Please run with 'sudo' or check hardware support."
fi

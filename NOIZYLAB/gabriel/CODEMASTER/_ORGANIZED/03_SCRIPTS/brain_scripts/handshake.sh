#!/bin/bash

# MC96Universe HANDSHAKE PROTOCOL
# "First Contact" Module: Connectivity & Mounting
# Purpose: Find 'Gabriel' and initiate high-speed SMB link.

echo ">>> HANDSHAKE PROTOCOL INITIALIZING..."

# 1. Define Gabriel (User may need to edit this IP)
# We assume he is on 10.90.90.91 based on standard sequence.
GABRIEL_IP="10.90.90.91"
GABRIEL_NAME="Gabriel"

echo ">>> SCANNING FOR TARGET: $GABRIEL_NAME ($GABRIEL_IP)..."

# 2. Check Visibility
if ping -c 1 -W 500 $GABRIEL_IP &> /dev/null; then
    echo ">>> TARGET ACQUIRED (ONLINE)."
else
    echo "!!! TARGET OFFLINE."
    echo "    -> Please check that Gabriel has IP $GABRIEL_IP"
    echo "    -> Or edit this script to match his actual IP."
    # Optional: Scan
    # echo ">>> Scanning subnet..."
    # ping_scan_logic_here
    exit 1
fi

# 3. Mount SMB Share
MOUNT_POINT="/Volumes/Gabriel_Link"

echo ">>> INITIATING DOCKING SEQUENCE (SMB MOUNT)..."
mkdir -p "$MOUNT_POINT"

# Attempt mount (Requires credentials usually)
# We use 'mount_smb' for better control.
# If user is same on both, it might auto-auth, otherwise prompt.
mount_smb "//Guest@$GABRIEL_IP/Data" "$MOUNT_POINT" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ">>> CONNECTION SUCCESSFUL. Gabriel is docked."
    open "$MOUNT_POINT"
else
    echo "!!! AUTO-DOCK FAILED (Auth Required?)."
    echo ">>> LAUNCHING MANUAL CONNECT..."
    open "smb://$GABRIEL_IP"
fi

echo ">>> HANDSHAKE COMPLETE."

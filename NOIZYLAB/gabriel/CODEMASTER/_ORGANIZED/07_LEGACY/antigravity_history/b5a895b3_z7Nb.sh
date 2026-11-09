#!/bin/bash
# GABRIEL TOOL: Connect to HP-OMEN (Remote Management)
# TARGET IP: 10.0.0.140 (Auto-Discovered)

TARGET_IP="10.0.0.140"
MOUNT_POINT="/Volumes/OMEN_C"
USER="hp_admin" # Placeholder, user needs to update

echo "⚡ GORUNFREEX1000: CONNECTING TO HP-OMEN [$TARGET_IP]..."

# 1. MOUNT SMB DRIVE (For full file access)
if [ ! -d "$MOUNT_POINT" ]; then
    mkdir -p "$MOUNT_POINT"
fi

if mount | grep "on $MOUNT_POINT" > /dev/null; then
    echo "✅ [SMB] Omen Drive already mounted at $MOUNT_POINT"
else
    echo ">> Mounting C$ Drive (Enter Password if requested)..."
    mount_smbfs "//$USER@$TARGET_IP/C$" "$MOUNT_POINT"
    if [ $? -eq 0 ]; then
        echo "✅ [SMB] SUCCESS: Mounted at $MOUNT_POINT"
    else
        echo "❌ [SMB] FAILED: Could not mount volume."
    fi
fi

# 2. FISHNET SCAN (Remote)
echo ">> running remote fishnet scan payload..."
# ssh $USER@$TARGET_IP "powershell -Command Get-ChildItem -Recurse C:\Users | Measure-Object"

# 3. SSH CONTROL (Interactive)
echo ">> Opening SSH Control Channel..."
ssh "$USER@$TARGET_IP"

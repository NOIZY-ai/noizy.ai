#!/bin/bash
# ============================================================
# DREAMCHAMBER: AUTO-MOUNT PC SHARES
# Mounts Windows PC shares to Mac via SMB (Zero Latency)
# ============================================================

PC_IP="10.90.90.20"
SHARE_NAME="DreamChamber"  # Default share name on Windows
MOUNT_POINT="$HOME/Mounts/PC_Bridge"
USERNAME="ADMIN"           # CHANGE THIS
PASSWORD="PASSWORD"        # CHANGE THIS

# Check if already mounted
if mount | grep "on ${MOUNT_POINT}" > /dev/null; then
    echo "✅ [DreamChamber] PC Bridge already mounted."
    exit 0
fi

# Ensure Mount Point exists
if [ ! -d "${MOUNT_POINT}" ]; then
    echo "📂 Creating mount point: ${MOUNT_POINT}"
    mkdir -p "${MOUNT_POINT}"
fi

echo "🚀 Attempting to mount //${PC_IP}/${SHARE_NAME}..."

# Mount Command (using credentials)
# Note: For security, consider using credentials file or keychain in production
# MOUNT COMMAND (Optimized for High-Speed/Jumbo Frames)
# -o automounted: Hides from desktop if desired (optional)
# -o noaps: Disable Apple Photo streams checks
# -o nosuid: Security
# neg=smb3_only: Force SMB3.1.1 for multichannel support
mount_smbfs -o noaps,nosuid,neg=smb3_only "//${USERNAME}:${PASSWORD}@${PC_IP}/${SHARE_NAME}" "${MOUNT_POINT}"

if [ $? -eq 0 ]; then
    echo "✅ [DreamChamber] MOUNT SUCCESS: ${MOUNT_POINT}"
    open "${MOUNT_POINT}"
else
    echo "❌ [DreamChamber] MOUNT FAILED. Check credentials or network."
    exit 1
fi

#!/bin/bash

# MC96Universe HYPER DRIVE Script
# "Warp Speed" Module: High-Performance RAM Disk Generator
# Purpose: Create a volatile, super-fast storage zone for "Mission Control" production.
# Host: M2 Ultra (192GB RAM detected context)

# Configuration
DRIVE_NAME="HyperDrive"
# Size in Sectors. (2048 sectors = 1MB)
# for 64GB: 64 * 1024 * 2048 = 134217728 sectors
DISK_SIZE=134217728 

echo ">>> MC96Universe HYPER DRIVE Initializing..."
echo ">>> Allocating 64GB of Liquid Memory for Storage..."

# Check if already exists
if [ -d "/Volumes/$DRIVE_NAME" ]; then
    echo "!!! HyperDrive already engaged at /Volumes/$DRIVE_NAME"
    exit 0
fi

# Attach RAM disk
# -nomount: don't mount yet, we want to format it
# ram://$DISK_SIZE: protocol and size
DISK_ID=$(hdiutil attach -nomount ram://$DISK_SIZE)

echo ">>> Memory Block Reserved: $DISK_ID"
echo ">>> Formatting APFS (Apple Filesystem) for Maximum Performance..."

# Format as APFS
diskutil erasevolume APFS "$DRIVE_NAME" "$DISK_ID"

echo ">>> HYPER DRIVE ENGAGED."
echo ">>> Location: /Volumes/$DRIVE_NAME"
echo ">>> Throughput: ~ 5000-7000 MB/s (Estimated)"
echo ">>> WARNING: CONTENTS ARE VOLATILE. LOST ON REBOOT."

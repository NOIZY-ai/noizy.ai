#!/bin/bash

# MC96Universe BLACK HOLE
# "Singularity" Module: Deep System Cleaning
# Purpose: Purge entropy (caches, logs, temp files) to ensure 100% efficiency.

echo ">>> BLACK HOLE INITIALIZING..."
echo ">>> COMPRESSING SPACE-TIME (Deleting junk)..."

# 1. Flush DNS (Instant Network Clarity)
echo "    -> Flushing DNS Cache..."
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# 2. System Caches (The heavy lifting)
echo "    -> Purging User Caches..."
rm -rf ~/Library/Caches/* 2>/dev/null
rm -rf ~/Library/Logs/* 2>/dev/null

# 3. System Logs (Reclaim Space/IO)
echo "    -> Rotation System Logs..."
sudo rm -rf /private/var/log/asl/* 2>/dev/null
sudo rm -rf /Library/Logs/DiagnosticReports/* 2>/dev/null

# 4. RAM Release
echo "    -> Collapsing Memory Waveforms (Purge)..."
sudo purge

# 5. Quick Look Reset
echo "    -> Resetting QuickLook..."
qlmanage -r >/dev/null 2>&1
qlmanage -r cache >/dev/null 2>&1

echo ">>> SYSTEM ENTROPY REDUCED."
echo ">>> The Universe is pure."

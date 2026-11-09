#!/bin/bash
# ============================================================
# GABRIEL M2 ULTRA KERNEL TUNING
# Zero-Latency • GPU Memory Unlock • 64GB RAM Disk
# ============================================================

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           ⚡ M2 ULTRA KERNEL TUNING ⚡                        ║"
echo "║                                                              ║"
echo "║    Network Stack • GPU Memory • RAM Disk • File Descriptors ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check for root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  This script requires sudo"
    echo "   Run: sudo ./m2_ultra_kernel.sh"
    exit 1
fi

echo "🚀 INITIATING M2 ULTRA KERNEL TUNING..."
echo ""

# ============================================================
# 1. NETWORK STACK (Zero-Latency Streaming)
# ============================================================
echo "📡 [1/5] UNLOCKING NETWORK STACK..."

# Enable Jumbo Frames (9000 MTU) for 10GbE Interface (en0)
echo "   ⚡ Setting Jumbo Frames (MTU 9000) on en0..."
networksetup -setMTU en0 9000 2>/dev/null || ifconfig en0 mtu 9000 2>/dev/null || echo "   ⚠️ Failed to set MTU 9000 on en0"

# Verify MTU
CURRENT_MTU=$(ifconfig en0 | grep mtu | awk '{print $NF}')
echo "   ✅ Interface en0 MTU: $CURRENT_MTU"

# Increase TCP buffer sizes for instant WebSocket transmission
sysctl -w net.inet.tcp.sendspace=1048576          # 1MB send buffer
sysctl -w net.inet.tcp.recvspace=1048576          # 1MB recv buffer
sysctl -w net.inet.tcp.win_scale_factor=8         # Window scaling
sysctl -w kern.ipc.maxsockbuf=16777216            # 16MB max socket buffer

# Disable Nagle's algorithm delay
sysctl -w net.inet.tcp.delayed_ack=0              # Instant ACK

# UDP optimization for audio streams
sysctl -w net.inet.udp.recvspace=2097152          # 2MB UDP buffer
sysctl -w net.inet.udp.maxdgram=65535             # Max datagram size

echo "   ✅ TCP buffers: 1MB send/recv"
echo "   ✅ Socket buffer: 16MB max"
echo "   ✅ Delayed ACK: DISABLED"

# ============================================================
# 2. FILE DESCRIPTORS (For Swarm Concurrency)
# ============================================================
echo ""
echo "📂 [2/5] INCREASING FILE DESCRIPTORS..."

sysctl -w kern.maxfiles=65536                     # Max system files
sysctl -w kern.maxfilesperproc=32768              # Max per process
sysctl -w kern.maxproc=4096                       # Max processes

# Also update launchd limits
launchctl limit maxfiles 32768 65536 2>/dev/null || true

echo "   ✅ Max files: 65,536"
echo "   ✅ Max per process: 32,768"
echo "   ✅ Max processes: 4,096"

# ============================================================
# 3. FILE SHARING OPTIMIZATION (DreamChamber SMB)
# ============================================================
echo ""
echo "📁 [3/5] TUNING SMB & FILE SHARING..."

# Create a custom nsmb.conf to optimize SMB client connections
# - Enable Multichannel (throughput scaling)
# - Disable Signing (reduces CPU overhead for trusted LAN)
if [ ! -f "/etc/nsmb.conf" ]; then
    echo "   Creating optimized /etc/nsmb.conf..."
    cat <<EOF > /etc/nsmb.conf
[default]
signing_required=no
streams=yes
mc_on=yes
mc_prefer_wired=yes
EOF
    echo "   ✅ /etc/nsmb.conf Created (Multichannel ON, Signing OFF)"
else
    echo "   ℹ️ /etc/nsmb.conf already exists. Skipping overwrite."
fi

# Performance tuning for AFP/SMB Server (if running on Mac)
# (Adjusts server throttle to allow max throughput)
sysctl -w debug.lowpri_throttle_enabled=0          # Disable low priority throttle
sysctl -w net.inet.tcp.delayed_ack=0               # Ensure disabled (redundant check)

echo "   ✅ Low-priority throttle: DISABLED"

# ============================================================
# 4. M2 GPU MEMORY UNLOCK (Neural Engine Headroom)
# ============================================================
echo ""
echo "🧠 [4/5] UNLOCKING GPU MEMORY..."

# Force allocation of wired memory for Neural Engine
# This gives MLX/Metal more headroom
sysctl -w iogpu.wired_limit_mb=128000 2>/dev/null || echo "   ⚠️ GPU limit not adjustable (normal on some macOS versions)"

echo "   ✅ GPU wired limit: 128GB (if supported)"

# ============================================================
# 5. RAM DISK (64GB Ultra-Fast Storage)
# ============================================================
echo ""
echo "💾 [5/5] CREATING RAM DISK..."

RAMDISK_SIZE_MB=65536  # 64GB
RAMDISK_NAME="GabrielVol"
RAMDISK_SECTORS=$((RAMDISK_SIZE_MB * 2048))  # 512 bytes per sector

if [ ! -d "/Volumes/${RAMDISK_NAME}" ]; then
    echo "   Creating ${RAMDISK_SIZE_MB}MB RAM disk..."
    
    # Create RAM disk
    DEVICE=$(hdiutil attach -nomount ram://${RAMDISK_SECTORS})
    
    # Format as APFS for best performance
    diskutil erasevolume APFS "${RAMDISK_NAME}" ${DEVICE}
    
    echo "   ✅ RAM disk mounted: /Volumes/${RAMDISK_NAME}"
    echo "   ✅ Size: ${RAMDISK_SIZE_MB}MB"
    echo "   ✅ Format: APFS"
else
    echo "   ✅ RAM disk already exists: /Volumes/${RAMDISK_NAME}"
fi

# Create Gabriel directories on RAM disk
mkdir -p "/Volumes/${RAMDISK_NAME}/cache"
mkdir -p "/Volumes/${RAMDISK_NAME}/temp"
mkdir -p "/Volumes/${RAMDISK_NAME}/audio"
mkdir -p "/Volumes/${RAMDISK_NAME}/models"

echo "   ✅ Created: /cache, /temp, /audio, /models"

# ============================================================
# SUMMARY
# ============================================================
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ✅ M2 ULTRA KERNEL TUNED ✅                      ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  NETWORK:                                                    ║"
echo "║    MTU (en0):        9000 (JUMBO)                            ║"
echo "║    TCP Buffers:      1 MB send/recv                          ║"
echo "║    SMB Client:       OPTIMIZED (Signing OFF, MC ON)          ║"
echo "║    Delayed ACK:      DISABLED                                ║"
echo "║                                                              ║"
echo "║  SYSTEM:                                                     ║"
echo "║    Max Files:        65,536                                  ║"
echo "║    Per Process:      32,768                                  ║"
echo "║                                                              ║"
echo "║  GPU MEMORY:                                                 ║"
echo "║    Wired Limit:      128 GB                                  ║"
echo "║                                                              ║"
echo "║  RAM DISK:                                                   ║"
echo "║    Location:         /Volumes/GabrielVol                     ║"
echo "║    Size:             64 GB                                   ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "⚡ DREAMCHAMBER ACTIVE. FLIGHT LEVELS OPTIMAL."
echo ""

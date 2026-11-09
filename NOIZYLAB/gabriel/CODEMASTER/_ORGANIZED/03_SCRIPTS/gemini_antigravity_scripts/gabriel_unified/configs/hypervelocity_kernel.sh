#!/usr/bin/env bash
# ============================================================
# GABRIEL HYPERVELOCITY KERNEL TUNING
# For M2 Ultra - macOS Network & Process Optimization
# ============================================================

echo "⚡ GABRIEL HYPERVELOCITY KERNEL TUNING"
echo "======================================="
echo ""

# Must run as sudo for sysctl changes
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Run with sudo for kernel tuning"
    echo "   sudo ./hypervelocity_kernel.sh"
    exit 1
fi

echo "🔧 Tuning macOS Kernel for Zero Latency..."
echo ""

# --- 1. NETWORK STACK OPTIMIZATION ---
echo "📡 Network Stack Overclock..."

# Increase max socket buffers (faster WebSocket throughput)
sysctl -w kern.ipc.maxsockbuf=16777216          # 16MB socket buffers

# TCP tuning for low latency
sysctl -w net.inet.tcp.recvspace=524288         # 512KB recv buffer
sysctl -w net.inet.tcp.sendspace=524288         # 512KB send buffer
sysctl -w net.inet.tcp.delayed_ack=0            # Disable Nagle delay
sysctl -w net.inet.tcp.mssdflt=1460             # Max segment size
sysctl -w net.inet.tcp.always_keepalive=1       # Keep connections alive

# UDP tuning for audio streams
sysctl -w net.inet.udp.recvspace=1048576        # 1MB UDP recv buffer
sysctl -w net.inet.udp.maxdgram=65535           # Max datagram size

echo "✅ Network stack optimized"

# --- 2. FILE DESCRIPTOR LIMITS ---
echo "📂 Unlocking File Descriptors..."

# Increase max open files (handles more connections)
sysctl -w kern.maxfiles=524288                  # Max files system-wide
sysctl -w kern.maxfilesperproc=262144           # Max files per process

# Update launchd limits
launchctl limit maxfiles 262144 524288 2>/dev/null || true

echo "✅ File descriptors unlocked"

# --- 3. PROCESS PRIORITY ---
echo "⚙️ Process Optimization..."

# Increase max processes
sysctl -w kern.maxproc=4096                     # Max processes
sysctl -w kern.maxprocperuid=2048               # Max per user

echo "✅ Process limits increased"

# --- 4. MEMORY TUNING ---
echo "🧠 Memory Optimization..."

# Disable swap pressure (M2 Ultra has 192GB)
sysctl -w vm.swappiness=0 2>/dev/null || true

echo "✅ Memory optimized"

# --- 5. SUMMARY ---
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              HYPERVELOCITY KERNEL ACTIVE                     ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Socket Buffers:     16 MB                                   ║"
echo "║  TCP Buffers:        512 KB                                  ║"
echo "║  Max Files:          524,288                                 ║"
echo "║  Max Processes:      4,096                                   ║"
echo "║  Nagle Delay:        DISABLED                                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "⚡ Kernel ready for ZERO LATENCY operation"

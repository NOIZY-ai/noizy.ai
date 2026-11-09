#!/bin/bash

# MC96Universe TURBO BOOST Script
# "Unleash the Beast" Module: macOS Network Kernel Tuning
# Optimized for M-Series Chips & High-Speed Networks (1GbE/10GbE)

echo ">>> MC96Universe TURBO BOOST Initializing..."
echo ">>> Tuning Kernel for Super-Sonic Throughput..."

# 1. TCP Window Scaling (RFC 1323) - Essential for LFN (Long Fat Networks)
# Check current
CUR_WIN=$(sysctl -n net.inet.tcp.win_scale_factor)
echo ">>> Current TCP Window Scale: $CUR_WIN"
# Set to 8 (Scale of 256) which is excellent for Gigabit/10GbE
sudo sysctl -w net.inet.tcp.win_scale_factor=8

# 2. Increase TCP Send/Receive Spaces
# Standard macOS is good, but "Turbo" needs more buffer for sustained transfers.
# Send Space (2MB)
sudo sysctl -w net.inet.tcp.sendspace=2097152
# Receive Space (2MB)
sudo sysctl -w net.inet.tcp.recvspace=2097152

# 3. Increase Max Socket Buffer
sudo sysctl -w kern.ipc.maxsockbuf=16777216

# 4. Auto-Tuning Buffers (Allow the OS to go nuts if needed)
# Set max auto-tuning to ~32MB
sudo sysctl -w net.inet.tcp.autorcvbufmax=33554432
sudo sysctl -w net.inet.tcp.autosndbufmax=33554432

# 5. Disable Delayed ACK (Latency Killer)
# 0 = Dispatch packets immediately. Useful for "Mission Control" snappy response.
# 2 = Default (compatibility). 0 is aggressive but faster for high-speed LAN.
sudo sysctl -w net.inet.tcp.delayed_ack=0

echo ">>> TURBO BOOST ENGAGED."
echo ">>> Note: These changes are active until reboot."
echo ">>> To make permanent, add to /etc/sysctl.conf"

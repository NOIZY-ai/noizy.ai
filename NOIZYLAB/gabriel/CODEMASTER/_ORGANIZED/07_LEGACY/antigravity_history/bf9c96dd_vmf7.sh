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
sudo sysctl -w net.inet.tcp.delayed_ack=0

# 6. Disable Nagle's Algorithm (RFC 896) system-wide where possible
# (macOS doesn't have a global TCP_NODELAY sysctl, but we can tune MSS)
# net.inet.tcp.mssdflt is default MSS. safely kept at 512 for conservative, but for Jumbo...
# We stick to delayed_ack=0 as the primary Nagle fighter.

# 7. AGGRESSIVE: Disable Packet Coalescing (TRO/TSO)
# "Pure Speed" means we process packets NOW, not batch them.
# M2 Ultra has CPU to spare, so we disable hardware offloading that adds latency.
# Note: This increases CPU load, but lowers latency.
sudo sysctl -w net.inet.tcp.tso=0
sudo sysctl -w net.inet.tcp.lro=0

# 8. Increase max pending connections (somaxconn)
# Don't let requests wait in line!
sudo sysctl -w kern.ipc.somaxconn=2048

# 9. DANGEROUSLY FAST EXTRAS (Experimental)
# ------------------------------------------
# TCP Blackhole: Drop packets to closed ports without RST. Saves CPU.
sudo sysctl -w net.inet.tcp.blackhole=2
# UDP Blackhole
sudo sysctl -w net.inet.udp.blackhole=1

# Disable Path MTU Discovery (Assume we know the path is 9000/1500)
# This removes the "discovery" overhead. FAST, but relies on your LAN being solid.
sudo sysctl -w net.inet.tcp.path_mtu_discovery=0

# Fast Forwarding (Legacy, but if enabled, speeds up routing)
sudo sysctl -w net.inet.ip.fastforwarding=1

echo ">>> TURBO BOOST v3 (UNLEASHED) ENGAGED."
echo ">>> Note: These changes are active until reboot."
echo ">>> To make permanent, add to /etc/sysctl.conf"

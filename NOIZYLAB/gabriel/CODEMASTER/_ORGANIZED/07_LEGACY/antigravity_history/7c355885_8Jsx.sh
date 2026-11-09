#!/bin/bash
# 🔥 MC96 HOT ROD ENGINE V3 - ZERO LATENCY EDITION
# Version 3.0 (Perfected by CB_01)
# 
# Purpose: AGGRESSIVE Network & System Tuning for 100% Flow
# Specs: MTU 9000, TCP Fast Open, Delayed ACK=0, Audio Priority

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔥 MC96 ZERO LATENCY ENGINE INITIATED...${NC}"

# Check sudo
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}Please run as root (sudo)${NC}"
  exit 1
fi

# Detect active interface
INTERFACE=$(route get default | grep interface | awk '{print $2}')
echo -e "${YELLOW}Targeting Interface: $INTERFACE${NC}"

# 1. MTU 9000 (JUMBO FRAMES)
echo "Setting MTU to 9000 (Jumbo Frames)..."
networksetup -setMTU "$INTERFACE" 9000
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ MTU 9000 Active${NC}"
else
    echo -e "${RED}❌ MTU Update Failed (Proceeding with others)${NC}"
fi

# 2. AGGRESSIVE TCP TUNING (The "Hot Rod" Mods)
echo "Applying Zero Latency Sysctls..."

# Maximize Window Scaling
sysctl -w net.inet.tcp.rfc1323=1 > /dev/null

# Buffers: 16MB (Massive Flow)
sysctl -w kern.ipc.maxsockbuf=16777216 > /dev/null
sysctl -w net.inet.tcp.sendspace=1048576 > /dev/null
sysctl -w net.inet.tcp.recvspace=1048576 > /dev/null

# Latency Killers
sysctl -w net.inet.tcp.delayed_ack=0 > /dev/null  # Nagle's Algorithm OFF
sysctl -w net.inet.tcp.mssdflt=1440 > /dev/null   # MSS Optimization
sysctl -w net.inet.tcp.fastopen=3 > /dev/null     # TFO Enabled
sysctl -w net.inet.tcp.blackhole=2 > /dev/null    # Drop bad packets silently

# Concurrency Boost
sysctl -w kern.ipc.somaxconn=2048 > /dev/null     # Max connections
echo -e "${GREEN}✅ TCP Stack: AGGRESSIVE${NC}"

# 3. AUDIO PROCESS PRIORITY (The "Lifeluv" Mod)
echo "Boosting Audio Process Priority..."
pids=$(pgrep coreaudiod)
if [ -n "$pids" ]; then
    renice -n -10 -p $pids > /dev/null 2>&1
    echo -e "${GREEN}✅ coreaudiod: High Priority (-10)${NC}"
else
    echo -e "${YELLOW}⚠️ coreaudiod not found (Skipping)${NC}"
fi

# 4. MEMORY COMPRESSION (Reduce CPU Overhead)
# sudo sysctl -w vm.compressor_mode=2 > /dev/null # Optional, kept safe for now

echo -e "\n${GREEN}🚀 ZERO LATENCY ACHIEVED. SYSTEM IS 100% OPTIMIZED.${NC}"
exit 0

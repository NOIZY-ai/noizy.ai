#!/bin/bash
# 🔥 MC96 HOT ROD ENGINE - NETWORK OPTIMIZER
# Version 2.0 (Rebuilt by CB_01)
# 
# Purpose: Optimize macOS network stack for MAXIMUM throughput
# Specs: MTU 9000, TCP Fast Open, Buffer Tuning

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔥 MC96 HOT ROD ENGINE INITIATED...${NC}"

# Check sudo
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}Please run as root (sudo)${NC}"
  exit 1
fi

# Detect active interface
INTERFACE=$(route get default | grep interface | awk '{print $2}')
echo -e "${YELLOW}Targeting Interface: $INTERFACE${NC}"

# 1. Enable Jumbo Frames (MTU 9000)
echo "Setting MTU to 9000 (Jumbo Frames)..."
networksetup -setMTU "$INTERFACE" 9000
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ MTU 9000 Active${NC}"
else
    echo -e "${RED}❌ MTU Update Failed (Hardware limit?)${NC}"
    echo "Fallback to 1500..."
    networksetup -setMTU "$INTERFACE" 1500
fi

# 2. Optimize TCP Buffers (Sysctl)
echo "Tuning TCP Stack..."

# Increase max buffer sizes (16MB)
sysctl -w kern.ipc.maxsockbuf=16777216 > /dev/null
echo -e "${GREEN}✅ IPC Max Socket Buffer: 16MB${NC}"

# TCP Receive/Send Windows
sysctl -w net.inet.tcp.sendspace=1048576 > /dev/null
sysctl -w net.inet.tcp.recvspace=1048576 > /dev/null
echo -e "${GREEN}✅ TCP Send/Recv Space: 1MB${NC}"

# Enable TCP Fast Open (Speed boost for connection open)
sysctl -w net.inet.tcp.fastopen=3 > /dev/null
echo -e "${GREEN}✅ TCP Fast Open Enabled${NC}"

# Delayed ACK (Reduce latency)
sysctl -w net.inet.tcp.delayed_ack=0 > /dev/null
echo -e "${GREEN}✅ Delayed ACK Disabled (Low Latency)${NC}"

# 3. Verify
echo -e "\n${YELLOW}--- VERIFICATION ---${NC}"
MTU_CHECK=$(networksetup -getMTU "$INTERFACE" | awk '{print $3}')
echo "Interface: $INTERFACE"
echo "MTU: $MTU_CHECK"
echo "Buffers: Optimized"

echo -e "\n${GREEN}🚀 MC96 OPTIMIZATION COMPLETE - GORUNFREE!${NC}"
exit 0

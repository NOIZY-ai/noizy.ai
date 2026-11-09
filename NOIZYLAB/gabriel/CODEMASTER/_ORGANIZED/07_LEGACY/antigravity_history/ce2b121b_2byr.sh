#!/bin/bash
# ============================================================================
# MC96ECOUNIVERSE - NETWORK OPTIMIZER (HOT ROD ENGINE)
# Version: 2.0 (God Mode)
# Date: 2025-12-16
# ============================================================================

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
INTERFACE="en0" # Default for Mac Studio (usually)
MTU_SIZE="9000"
LOG_FILE="/Users/m2ultra/NOIZYLAB/logs/mc96_network.log"

log() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
    echo "[SUCCESS] $1" >> "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}⚠️ $1${NC}"
    echo "[WARN] $1" >> "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    echo "[ERROR] $1" >> "$LOG_FILE"
}

mkdir -p "$(dirname "$LOG_FILE")"

echo -e "${BLUE}"
echo "================================================================"
echo "   🚀 MC96ECOUNIVERSE NETWORK OPTIMIZER - HOT ROD ENGINE 🚀   "
echo "================================================================"
echo -e "${NC}"

# Check for Root
if [ "$EUID" -ne 0 ]; then 
    warn "Please run as root for full optimization (sudo $0)"
    # We continue, but some commands might fail
fi

log "Starting optimization sequence..."

# 1. MTU Optimization (Jumbo Frames)
log "Configuring MTU to $MTU_SIZE on $INTERFACE..."
if ifconfig "$INTERFACE" mtu "$MTU_SIZE" 2>/dev/null; then
    success "MTU set to $MTU_SIZE on $INTERFACE (Jumbo Frames Active!)"
else
    # Try getting current MTU to see if it's already set or maxed
    CUR_MTU=$(ifconfig "$INTERFACE" | grep mtu | awk '{print $4}')
    warn "Could not set MTU $MTU_SIZE. Current MTU: $CUR_MTU. Hardware might not support 9000."
fi

# 2. SYSCTL Optimization (macOS specific constants)
log "Applying Kernel TCP optimizations..."

# TCP Keepalive (shorter intervals for dead connection cleanup)
sysctl -w net.inet.tcp.keepidle=60000 >/dev/null 2>&1 && success "TCP Keepidle set to 60s"
sysctl -w net.inet.tcp.keepintvl=15000 >/dev/null 2>&1 && success "TCP Keepintvl set to 15s"

# TCP Delayed ACK (reduce latency)
sysctl -w net.inet.tcp.delayed_ack=0 >/dev/null 2>&1 && success "TCP Delayed ACK disabled (Zero Latency)"

# TCP Send/Recv Spaces (Buffer sizes - 256KB target as per docs)
sysctl -w net.inet.tcp.sendspace=262144 >/dev/null 2>&1 && success "TCP Send Space set to 256KB"
sysctl -w net.inet.tcp.recvspace=262144 >/dev/null 2>&1 && success "TCP Recv Space set to 256KB"

# TCP Fast Open
sysctl -w net.inet.tcp.fastopen=3 >/dev/null 2>&1 && success "TCP Fast Open Enabled (Client/Server)"

# 3. DNS Flush
log "Flushing DNS Cache..."
if dscacheutil -flushcache; then
    sudo killall -HUP mDNSResponder 2>/dev/null
    success "DNS Cache Flushed & mDNSResponder Restarted"
else
    warn "DNS Flush required sudo"
fi

# 4. Interface Verification
log "Verifying Interface Stats..."
IF_INFO=$(ifconfig "$INTERFACE")
if [[ "$IF_INFO" == *"media: autoselect (1000baseT <full-duplex>)"* ]]; then
    success "Link Speed: Gigabit Full-Duplex"
else
    # Might be 10G or WiFi
    SPEED=$(echo "$IF_INFO" | grep "media:" | cut -d ':' -f 2 | xargs)
    success "Link Speed: $SPEED"
fi

echo -e "${BLUE}"
echo "================================================================"
echo "   ✨ OPTIMIZATION COMPLETE - SYSTEM READY FOR TAKEOFF ✨    "
echo "================================================================"
echo -e "${NC}"

log "Optimization complete."

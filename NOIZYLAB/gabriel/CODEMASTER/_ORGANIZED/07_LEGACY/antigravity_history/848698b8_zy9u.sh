#!/bin/bash
# ============================================================================
# MC96ECOUNIVERSE - NETWORK OPTIMIZER (HOT ROD ENGINE)
# Version: 3.0 (God Mode / Zero Latency)
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
LOG_FILE="/Users/m2ultra/NOIZYLAB/logs/mc96_network.log"
TARGET_MTU="9000"

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

detect_interface() {
    # Try to find the active interface with an IP address (prioritize Ethernet/10G)
    # This ignores loopback and specific VM bridges if possible
    local iface
    iface=$(route get default 2>/dev/null | grep interface | awk '{print $2}')
    
    if [ -z "$iface" ]; then
        # Fallback detection
        iface=$(netstat -rn | grep default | head -n 1 | awk '{print $NF}')
    fi

    if [ -z "$iface" ]; then
        iface="en0" # Last resort default
    fi
    echo "$iface"
}

check_docker() {
    log "Checking Docker availability..."
    if command -v docker &> /dev/null; then
        success "Docker CLI is available."
    else
        warn "Docker CLI is MISSING in path."
        
        # Auto-Heal attempt: Check common locations
        if [ -f "/Applications/Docker.app/Contents/Resources/bin/docker" ]; then
            log "Found Docker in App bundle. Creating symlink..."
            ln -sf /Applications/Docker.app/Contents/Resources/bin/docker /usr/local/bin/docker 2>/dev/null
            if [ $? -eq 0 ]; then
                success "Symlink created! Docker should work now."
                return
            else
                 warn "Could not create symlink (permission denied?)."
            fi
        fi
        
        echo -e "${YELLOW}>>> ACTION REQUIRED: Install Docker Desktop or fix PATH.${NC}"
    fi
}

mkdir -p "$(dirname "$LOG_FILE")"

echo -e "${BLUE}"
echo "================================================================"
echo "   🚀 MC96ECOUNIVERSE NETWORK OPTIMIZER - HOT ROD ENGINE v3   "
echo "================================================================"
echo -e "${NC}"

# Check for Root
if [ "$EUID" -ne 0 ]; then 
    warn "Running without sudo. Network stack optimizations will fail."
    echo "Please run: sudo $0"
    # We continue to run non-privileged checks
fi

log "Starting optimization sequence..."
INTERFACE=$(detect_interface)
log "Active Interface detected: ${GREEN}$INTERFACE${NC}"

# 1. MTU Optimization (Jumbo Frames)
if [ "$EUID" -eq 0 ]; then
    log "Configuring MTU to $TARGET_MTU on $INTERFACE..."
    if ifconfig "$INTERFACE" mtu "$TARGET_MTU" 2>/dev/null; then
        success "MTU set to $TARGET_MTU on $INTERFACE (Jumbo Frames Active!)"
    else
        CUR_MTU=$(ifconfig "$INTERFACE" | grep mtu | awk '{print $4}')
        warn "Could not set MTU $TARGET_MTU. Current MTU: $CUR_MTU. (Hardware limit?)"
    fi
else
    warn "Skipping MTU set (requires sudo)"
fi

# 2. SYSCTL Optimization (macOS specific constants)
if [ "$EUID" -eq 0 ]; then
    log "Applying Kernel TCP optimizations..."

    # TCP Keepalive (shorter intervals for dead connection cleanup)
    sysctl -w net.inet.tcp.keepidle=60000 >/dev/null 2>&1 && success "TCP Keepidle set to 60s"
    sysctl -w net.inet.tcp.keepintvl=15000 >/dev/null 2>&1 && success "TCP Keepintvl set to 15s"

    # TCP Delayed ACK (reduce latency)
    sysctl -w net.inet.tcp.delayed_ack=0 >/dev/null 2>&1 && success "TCP Delayed ACK disabled (Zero Latency)"

    # TCP Send/Recv Spaces (Buffer sizes - 256KB target as per docs)
    sysctl -w net.inet.tcp.sendspace=524288 >/dev/null 2>&1 && success "TCP Send Space set to 512KB (Boosted)"
    sysctl -w net.inet.tcp.recvspace=524288 >/dev/null 2>&1 && success "TCP Recv Space set to 512KB (Boosted)"

    # TCP Fast Open
    sysctl -w net.inet.tcp.fastopen=3 >/dev/null 2>&1 && success "TCP Fast Open Enabled (Client/Server)"
else
     warn "Skipping sysctl optimizations (requires sudo)"
fi

# 3. DNS Flush
log "Flushing DNS Cache..."
if dscacheutil -flushcache; then
    sudo killall -HUP mDNSResponder 2>/dev/null
    success "DNS Cache Flushed & mDNSResponder Restarted"
else
    warn "DNS Flush might have been incomplete (sudo helps)"
fi

# 4. Tool Verification (Auto-Heal)
check_docker

# 5. Interface Verification
log "Verifying Interface Stats..."
IF_INFO=$(ifconfig "$INTERFACE")
if [[ "$IF_INFO" == *"media: autoselect (1000baseT <full-duplex>)"* ]]; then
    success "Link Speed: Gigabit Full-Duplex"
elif [[ "$IF_INFO" == *"media: autoselect (10Gbase-T <full-duplex>)"* ]]; then
     success "Link Speed: 10 GIGABIT DETECTED (GOD MODE)"
else
    # Might be WiFi
    SPEED=$(echo "$IF_INFO" | grep "media:" | cut -d ':' -f 2 | xargs)
    success "Link Speed: $SPEED"
fi

echo -e "${BLUE}"
echo "================================================================"
echo "   ✨ OPTIMIZATION COMPLETE - SYSTEM READY FOR TAKEOFF ✨    "
echo "================================================================"
echo -e "${NC}"

log "Optimization complete."

#!/bin/bash
# ==============================================================================
#  🏎️  MBP13 HOT ROD SCRIPT (GABRIEL EDITION)
# ==============================================================================
#  Optimizes macOS for:
#  1. 10GbE / High-Speed Networking (Jumbo Frames)
#  2. SMB Performance (No Signing, Multi-Channel)
#  3. UI/System Responsiveness (Disable Animations)
#  4. Developer Performance (Spotlight Tuning)
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "   __  _______  ____  ____ ____  "
echo "  /  |/  / __ )/ __ \/ __ \__  | "
echo " / /|_/ / __  / /_/ / / / //_ <  "
echo "/ /  / / /_/ / ____/ /_/ /__/ /  "
echo "/_/  /_/_____/_/    \____/____/   "
echo "                                   "
echo "   >>> HOT ROD GABRIEL EDITION <<< "
echo -e "${NC}"

if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}Please run as root (sudo).${NC}"
  exit 1
fi

# 1. NETWORK OPTIMIZATION (Jumbo Frames & TCP)
echo -e "${GREEN}[1/4] TUNING NETWORK STACK...${NC}"

# Detect active interface (Wifi or Ethernet)
# Assuming Ethernet dongle en* usually (often en4, en6 on hubs). 
# We'll try to set MTU 9000 on all active Ethernet interfaces.
for iface in $(networksetup -listallhardwareports | grep -A 1 "Hardware Port:.*Ethernet" | grep "Device: en" | awk '{print $2}'); do
    echo "  - Setting MTU 9000 on $iface..."
    networksetup -setMTU $iface 9000 2>/dev/null || echo "    (Failed, hardware might not support it)"
done

# Sysctl TCP Tuning for 10GbE/High-Bandwidth
sysctl -w net.inet.tcp.win_scale_factor=8
sysctl -w net.inet.tcp.sendspace=4194304
sysctl -w net.inet.tcp.recvspace=4194304
sysctl -w net.inet.tcp.delayed_ack=0  # Reduce latency
sysctl -w net.inet.tcp.mssdflt=8960   # If Jumbo is active
echo "  - TCP Window Scaling & Buffers optimized."


# 2. SMB OPTIMIZATION
echo -e "${GREEN}[2/4] TURBOCHARGING SMB...${NC}"
SMB_CONF="/etc/nsmb.conf"
cat > $SMB_CONF <<EOF
[default]
signing_required=no
validate_neg_off=yes
dir_cache_max_cnt=4096
dir_cache_max=60
streams=no
soft=yes
EOF
echo "  - /etc/nsmb.conf updated for raw speed."


# 3. SPOTLIGHT TUNING (No External Indexing)
echo -e "${GREEN}[3/4] SILENCING SPOTLIGHT...${NC}"
mdutil -i off /Volumes/* 2>/dev/null
echo "  - Spotlight disabled on external volumes (prevents 'mds' cpu hog)."


# 4. UI ANIMATION KILLER (Make it Snappy)
echo -e "${GREEN}[4/4] ACCELERATING UI...${NC}"
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001
defaults write com.apple.finder DisableAllAnimations -bool true
defaults write com.apple.dock launchanim -bool false
defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false
killall Finder Dock

echo ""
echo -e "${CYAN}>>> MBP13 IS NOW HOT RODDED. <<<${NC}"
echo "Reboot recommended for all changes to take full effect."

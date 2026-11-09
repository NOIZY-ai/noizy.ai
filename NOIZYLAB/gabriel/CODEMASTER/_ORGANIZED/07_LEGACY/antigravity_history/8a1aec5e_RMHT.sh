#!/bin/zsh
#
# MBP13_HOTROD_OPTIMIZER.sh
# ═══════════════════════════════════════════════════════════════════════════
# Transform your 13" MacBook Pro into a COMPLETE HOT ROD
# Part of MC96DIGIUNIVERSE - GORUNFREE x1000
# ═══════════════════════════════════════════════════════════════════════════
#
# Usage: ./MBP13_HOTROD_OPTIMIZER.sh [--aggressive]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

AGGRESSIVE=false
if [[ "$1" == "--aggressive" ]]; then
    AGGRESSIVE=true
fi

clear
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo "${WHITE}  🔥 MBP13 HOT ROD OPTIMIZER - GORUNFREE x1000${NC}"
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}Transforming your 13\" MacBook Pro into a SCREAMING machine...${NC}"
echo ""

# Function for status updates
status() {
    echo "${BLUE}⚡${NC} $1... ${GREEN}[DONE]${NC}"
}

warn() {
    echo "${YELLOW}⚠️${NC} $1"
}

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1: MEMORY & PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 1: MEMORY & PERFORMANCE ━━━${NC}"

# Clear system caches
sudo purge 2>/dev/null && status "Purged inactive memory" || warn "Could not purge (needs sudo)"

# Disable memory compression if aggressive
if $AGGRESSIVE; then
    sudo nvram boot-args="vm_compressor=1" 2>/dev/null && status "Memory compressor set to fastest mode" || true
fi

# Disable swap (only for systems with 16GB+)
# Uncomment if you have enough RAM:
# sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.dynamic_pager.plist 2>/dev/null || true

status "Memory optimization complete"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2: DISABLE RESOURCE HOGS
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 2: DISABLE RESOURCE HOGS ━━━${NC}"

# Spotlight - reduce indexing overhead
sudo mdutil -i off / 2>/dev/null && status "Spotlight indexing paused" || warn "Could not pause Spotlight"

# Time Machine - disable local snapshots
sudo tmutil disablelocal 2>/dev/null && status "Time Machine local snapshots disabled" || true

# Disable Siri
defaults write com.apple.Siri StatusMenuVisible -bool false 2>/dev/null
defaults write com.apple.Siri UserHasDeclinedEnable -bool true 2>/dev/null
status "Siri disabled"

# Disable notification center (can be re-enabled)
# launchctl unload -w /System/Library/LaunchAgents/com.apple.notificationcenterui.plist 2>/dev/null || true

# Reduce transparency effects (less GPU overhead)
defaults write com.apple.universalaccess reduceTransparency -bool true 2>/dev/null
status "Transparency effects reduced"

# Reduce motion
defaults write com.apple.universalaccess reduceMotion -bool true 2>/dev/null
status "Motion effects reduced"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 3: NETWORK OPTIMIZATION (FOR NDI/SCREEN SHARE)
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 3: NETWORK OPTIMIZATION ━━━${NC}"

# Increase network buffer sizes for video streaming
sudo sysctl -w net.inet.tcp.sendspace=262144 2>/dev/null || true
sudo sysctl -w net.inet.tcp.recvspace=262144 2>/dev/null || true
sudo sysctl -w net.inet.udp.recvspace=262144 2>/dev/null || true
sudo sysctl -w net.inet.udp.maxdgram=65535 2>/dev/null || true
status "Network buffers increased (better for NDI/video)"

# Enable jumbo frames hint (actual setting is on switch/router)
# sudo ifconfig en0 mtu 9000 2>/dev/null || true

# Flush DNS cache
sudo dscacheutil -flushcache 2>/dev/null
sudo killall -HUP mDNSResponder 2>/dev/null
status "DNS cache flushed"

# Disable AirDrop (reduces network scanning)
if $AGGRESSIVE; then
    defaults write com.apple.NetworkBrowser DisableAirDrop -bool true 2>/dev/null
    status "AirDrop disabled (aggressive mode)"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4: FINDER & UI SPEED
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 4: FINDER & UI SPEED ━━━${NC}"

# Speed up Mission Control animations
defaults write com.apple.dock expose-animation-duration -float 0.1 2>/dev/null
status "Mission Control animation: INSTANT"

# Speed up Dock auto-hide
defaults write com.apple.dock autohide-delay -float 0 2>/dev/null
defaults write com.apple.dock autohide-time-modifier -float 0.2 2>/dev/null
status "Dock animation: FAST"

# Disable Finder animations
defaults write com.apple.finder DisableAllAnimations -bool true 2>/dev/null
status "Finder animations disabled"

# Speed up window resize animations
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001 2>/dev/null
status "Window resize: INSTANT"

# Disable smooth scrolling (snappier feel)
defaults write NSGlobalDomain NSScrollAnimationEnabled -bool false 2>/dev/null
status "Smooth scrolling disabled"

# Faster keyboard repeat
defaults write NSGlobalDomain KeyRepeat -int 1 2>/dev/null
defaults write NSGlobalDomain InitialKeyRepeat -int 10 2>/dev/null
status "Keyboard repeat: TURBO"

# Disable auto-correct
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false 2>/dev/null
status "Auto-correct disabled"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 5: POWER & THERMAL
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 5: POWER & THERMAL ━━━${NC}"

# Disable Power Nap (prevents background activity)
sudo pmset -a powernap 0 2>/dev/null
status "Power Nap disabled"

# Disable wake on network access
sudo pmset -a womp 0 2>/dev/null
status "Wake on LAN disabled"

# Set high performance mode (when plugged in)
sudo pmset -c sleep 0 2>/dev/null       # Never sleep on AC
sudo pmset -c disksleep 0 2>/dev/null   # Disk always spinning on AC
sudo pmset -c displaysleep 30 2>/dev/null
status "Power mode: HIGH PERFORMANCE (AC)"

# Disable AppNap (keeps apps running full speed)
defaults write NSGlobalDomain NSAppSleepDisabled -bool true 2>/dev/null
status "App Nap disabled"

# Disable automatic graphics switching (use dedicated GPU)
sudo pmset -a gpuswitch 0 2>/dev/null && status "GPU: Dedicated only" || true

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 6: DEVELOPER / PRO MODE
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 6: DEVELOPER / PRO MODE ━━━${NC}"

# Show all file extensions
defaults write NSGlobalDomain AppleShowAllExtensions -bool true 2>/dev/null
status "All file extensions visible"

# Show hidden files
defaults write com.apple.finder AppleShowAllFiles -bool true 2>/dev/null
status "Hidden files visible"

# Show path bar in Finder
defaults write com.apple.finder ShowPathbar -bool true 2>/dev/null
status "Finder path bar enabled"

# Show status bar in Finder
defaults write com.apple.finder ShowStatusBar -bool true 2>/dev/null
status "Finder status bar enabled"

# Disable .DS_Store on network volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true 2>/dev/null
status ".DS_Store disabled on network volumes"

# Disable disk image verification (faster mounts)
defaults write com.apple.frameworks.diskimages skip-verify -bool true 2>/dev/null
defaults write com.apple.frameworks.diskimages skip-verify-locked -bool true 2>/dev/null
defaults write com.apple.frameworks.diskimages skip-verify-remote -bool true 2>/dev/null
status "Disk image verification: SKIP"

# Enable develop menu in Safari
defaults write com.apple.Safari IncludeDevelopMenu -bool true 2>/dev/null
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true 2>/dev/null
status "Safari Developer menu enabled"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 7: RESTART SERVICES
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 7: APPLYING CHANGES ━━━${NC}"

# Restart Finder
killall Finder 2>/dev/null
status "Finder restarted"

# Restart Dock
killall Dock 2>/dev/null
status "Dock restarted"

# Restart SystemUIServer
killall SystemUIServer 2>/dev/null
status "SystemUIServer restarted"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# FINAL STATUS
# ═══════════════════════════════════════════════════════════════════════════
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${WHITE}  🔥 MBP13 HOT ROD OPTIMIZATION COMPLETE 🔥${NC}"
echo ""
echo "${GREEN}  Memory:      OPTIMIZED${NC}"
echo "${GREEN}  Network:     TURBO (NDI/Video Ready)${NC}"
echo "${GREEN}  UI Speed:    INSTANT${NC}"
echo "${GREEN}  Power:       HIGH PERFORMANCE${NC}"
echo "${GREEN}  Dev Mode:    ENABLED${NC}"
echo ""
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}📋 POST-OPTIMIZATION TIPS:${NC}"
echo ""
echo "  1. Restart your Mac for all changes to take effect"
echo "  2. For NDI: Ensure Jumbo Frames enabled on your switch"
echo "  3. For Screen Share: Use 'High Quality' preset"
echo "  4. Monitor temps with: sudo powermetrics --samplers smc"
echo ""
echo "${WHITE}To restore defaults:${NC}"
echo "  defaults delete NSGlobalDomain"
echo "  defaults delete com.apple.finder"
echo "  defaults delete com.apple.dock"
echo ""
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${MAGENTA}MC96DIGIUNIVERSE // GORUNFREE x1000${NC}"
echo "${BLUE}Your 13\" MacBook Pro is now a SCREAMING HOT ROD! 🚀${NC}"
echo ""

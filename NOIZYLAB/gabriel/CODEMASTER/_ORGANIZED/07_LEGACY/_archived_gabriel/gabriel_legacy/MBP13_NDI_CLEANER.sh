#!/bin/zsh
#
# MBP13_NDI_CLEANER.sh
# ═══════════════════════════════════════════════════════════════════════════
# Clean up NDI/Screen Share signal from 13" MacBook Pro
# Optimizes video stream quality and removes artifacts
# ═══════════════════════════════════════════════════════════════════════════
#

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "${CYAN}━━━ MBP13 SCREEN SHARE / NDI CLEANER ━━━${NC}"
echo ""

# Kill any stuck screen sharing processes
echo "${YELLOW}Cleaning up screen share processes...${NC}"
killall "Screen Sharing" 2>/dev/null && echo "${GREEN}✅ Screen Sharing app closed${NC}" || echo "No Screen Sharing app running"

# Restart screen capture services
echo "${YELLOW}Restarting capture services...${NC}"
killall screencaptureui 2>/dev/null || true
killall -HUP WindowServer 2>/dev/null || true

# Clear screen sharing cache
echo "${YELLOW}Clearing screen share cache...${NC}"
rm -rf ~/Library/Caches/com.apple.screensharing* 2>/dev/null
rm -rf /tmp/com.apple.screensharing* 2>/dev/null
echo "${GREEN}✅ Cache cleared${NC}"

# Optimize network for video streaming
echo "${YELLOW}Optimizing network for clean signal...${NC}"
sudo sysctl -w net.inet.tcp.delayed_ack=0 2>/dev/null && echo "${GREEN}✅ TCP delay disabled (lower latency)${NC}"
sudo sysctl -w net.inet.tcp.mssdflt=1440 2>/dev/null && echo "${GREEN}✅ TCP MSS optimized${NC}"

# Flush routing table cache
sudo route -n flush 2>/dev/null && echo "${GREEN}✅ Route cache flushed${NC}" || true

# Restart mDNS (helps with Bonjour/network discovery)
sudo killall -HUP mDNSResponder 2>/dev/null
echo "${GREEN}✅ mDNS responder restarted${NC}"

echo ""
echo "${CYAN}━━━ CLEANUP COMPLETE ━━━${NC}"
echo ""
echo "For best screen share quality from MBP13:"
echo "  1. Use wired Ethernet if possible"
echo "  2. Set resolution to match source (no scaling)"
echo "  3. Use 'Adaptive Quality' in Screen Sharing prefs"
echo ""
echo "${GREEN}🔥 Signal should now be CLEAN!${NC}"

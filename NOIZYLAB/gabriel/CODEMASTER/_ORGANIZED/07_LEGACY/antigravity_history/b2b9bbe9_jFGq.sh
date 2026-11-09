#!/bin/bash
# ============================================================================
# MC96ECOUNIVERSE - INTEGRATIONS MANAGER
# Use this to verify and setup external connections
# ============================================================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

check_cmd() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓ $1 is installed${NC}"
        return 0
    else
        echo -e "${RED}✗ $1 not found${NC}"
        return 1
    fi
}

echo "================================================================="
echo "   🔗 SYSTEM INTEGRATION CHECK"
echo "================================================================="

# 1. VPN (Cloudflare WARP)
echo -e "\n--- Checking VPN (Cloudflare WARP) ---"
if check_cmd "warp-cli"; then
    STATUS=$(warp-cli status 2>/dev/null)
    if [[ "$STATUS" == *"Connected"* ]]; then
        echo -e "${GREEN}✓ WARP is Connected${NC}"
    else
        echo -e "${YELLOW}⚠️ WARP is installed but maybe disconnected.${NC}"
        echo "Status: $STATUS"
    fi
else
    echo -e "${YELLOW}Install Cloudflare WARP for 'Hot Rod' secure tunneling.${NC}"
fi

# 2. Discord
echo -e "\n--- Checking Discord ---"
if [ -d "/Applications/Discord.app" ]; then
    echo -e "${GREEN}✓ Discord App found${NC}"
else
    echo -e "${YELLOW}⚠️ Discord App not found in /Applications${NC}"
fi

# 3. GitHub
echo -e "\n--- Checking GitHub ---"
if check_cmd "gh"; then
    AUTH_STATUS=$(gh auth status 2>&1)
    if [[ "$AUTH_STATUS" == *"Logged in"* ]]; then
        echo -e "${GREEN}✓ GitHub CLI authenticated${NC}"
    else
        echo -e "${YELLOW}⚠️ GitHub CLI not logged in. Run 'gh auth login'${NC}"
    fi
fi
if [ -f "$HOME/.ssh/id_ed25519" ] || [ -f "$HOME/.ssh/id_rsa" ]; then
    echo -e "${GREEN}✓ SSH Keys detected${NC}"
else
    echo -e "${RED}✗ No SSH keys found in ~/.ssh${NC}"
fi

# 4. Google Drive
echo -e "\n--- Checking Google Drive ---"
DRIVE_PATH="$HOME/Library/CloudStorage/GoogleDrive-rsplowman@icloud.com" # Guessing based on email
ALT_PATH="$HOME/Google Drive"

if [ -d "$DRIVE_PATH" ] || [ -d "/Volumes/GoogleDrive" ]; then
    echo -e "${GREEN}✓ Google Drive mount detected${NC}"
else
    echo -e "${YELLOW}⚠️ Google Drive not mounted or path unknown.${NC}"
    echo "Check /Volumes or CloudStorage."
fi

# 5. DGS1210-10 Switch (Network Reachability)
echo -e "\n--- Checking DGS1210-Switch ---"
SWITCH_IP="10.0.0.132" # From legacy doc
if ping -c 1 -W 500 "$SWITCH_IP" &> /dev/null; then
    echo -e "${GREEN}✓ Switch ($SWITCH_IP) is reachable${NC}"
else
    echo -e "${YELLOW}⚠️ Switch ($SWITCH_IP) not reachable. Check IP or connection.${NC}"
fi

echo -e "\nDone."

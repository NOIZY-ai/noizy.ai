#!/bin/bash
################################################################################
#
#   ██████╗  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗███████╗██████╗ ███████╗███████╗
#  ██╔════╝ ██╔═══██╗██╔══██╗██║   ██║████╗  ██║██╔════╝██╔══██╗██╔════╝██╔════╝
#  ██║  ███╗██║   ██║██████╔╝██║   ██║██╔██╗ ██║█████╗  ██████╔╝█████╗  █████╗
#  ██║   ██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗██╔══╝  ██╔══╝
#  ╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║██║     ██║  ██║███████╗███████╗
#   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
#
#  GABRIEL UNIFIED - ULTIMATE LAUNCHER
#  UPGRADE & IMPROVE!! KEEP GOING!!
#
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ██████╗  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗           ║
║ ██╔════╝ ██╔═══██╗██╔══██╗██║   ██║████╗  ██║           ║
║ ██║  ███╗██║   ██║██████╔╝██║   ██║██╔██╗ ██║           ║
║ ██║   ██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║           ║
║ ╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║           ║
║  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝           ║
║                                                          ║
║        GABRIEL UNIFIED - ULTIMATE LAUNCHER               ║
║        UPGRADE & IMPROVE!! KEEP GOING!!                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Detect Python
PYTHON=""
if command -v /opt/homebrew/bin/python3 &> /dev/null; then
    PYTHON="/opt/homebrew/bin/python3"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo -e "${RED}❌ Python not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Using Python: ${PYTHON}${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Function to run a script
run_script() {
    local script=$1
    local name=$2

    if [ -f "$script" ]; then
        echo -e "\n${MAGENTA}🚀 Launching: ${name}${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        $PYTHON "$script"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}✅ ${name} - COMPLETE!${NC}"
    else
        echo -e "${YELLOW}⚠️  ${name} not found: ${script}${NC}"
    fi
}

# Main menu
echo -e "\n${WHITE}Select an action:${NC}"
echo -e "${CYAN}1)${NC} Run Visual Scanner"
echo -e "${CYAN}2)${NC} Run All Systems"
echo -e "${CYAN}3)${NC} Quick System Status"
echo -e "${CYAN}4)${NC} Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        run_script "GABRIEL_UNIFIED/core/visual_scanner.py" "Visual Scanner X1000"
        ;;
    2)
        echo -e "\n${MAGENTA}🚀 RUNNING ALL SYSTEMS - GORUNFREE!!${NC}\n"
        run_script "GABRIEL_UNIFIED/core/visual_scanner.py" "Visual Scanner X1000"
        ;;
    3)
        echo -e "\n${CYAN}📊 Quick System Status:${NC}\n"
        echo -e "${WHITE}Hostname:${NC} $(hostname)"
        echo -e "${WHITE}User:${NC} $(whoami)"
        echo -e "${WHITE}Uptime:${NC} $(uptime)"
        echo -e "${WHITE}Disk Usage:${NC}"
        df -h | head -5
        ;;
    4)
        echo -e "\n${GREEN}Goodbye! GORUNFREE!!${NC}\n"
        exit 0
        ;;
    *)
        echo -e "\n${RED}Invalid choice!${NC}\n"
        exit 1
        ;;
esac

echo -e "\n${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          GABRIEL UNIFIED - MISSION COMPLETE!!            ║${NC}"
echo -e "${GREEN}║              GORUNFREE!! KEEP GOING!!                    ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}\n"

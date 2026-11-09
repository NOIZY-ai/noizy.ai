#!/bin/bash
# ============================================================================
# MC96ECOUNIVERSE - LAUNCHER (MISSION CONTROL)
# ============================================================================

SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR" || exit

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

while true; do
    clear
    echo -e "${CYAN}"
    echo "================================================================="
    echo "       🌌 MC96ECOUNIVERSE - MISSION CONTROL CENTER 🌌 "
    echo "================================================================="
    echo -e "${NC}"
    echo -e "   ${GREEN}[1] 🚀 OPTIMIZE NETWORK (Hot Rod Mode)${NC}"
    echo -e "   ${GREEN}[2] 📡 SCAN DEVICES (Radar Scan)${NC}"
    echo -e "   ${GREEN}[3] 📊 LIVE MONITOR (Dashboard)${NC}"
    echo -e "   ${YELLOW}[4] 🔗 INTEGRATIONS (VPN/Discord/Git)${NC}"
    echo -e "   ${BLUE}[5] 🩺 AUTO-HEAL (Quick Fix)${NC}"
    echo ""
    echo -e "   ${RED}[X] EXIT${NC}"
    echo "================================================================="
    echo -n "   Select Option: "
    read -r choice

    case $choice in
        1)
            echo "Running Optimization..."
            sudo ./mc96_optimize.sh
            echo "Press any key to return..."
            read -n 1
            ;;
        2)
            python3 mc96_scan.py
            echo "Press any key to return..."
            read -n 1
            ;;
        3)
            python3 mc96_monitor.py
            ;;
        4)
            ./setup_integrations.sh
            echo "Press any key to return..."
            read -n 1
            ;;
        5)
            echo "Auto-Heal not yet implemented independently. Running Optimizer..."
            sudo ./mc96_optimize.sh
            read -n 1
            ;;
        x|X)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid Option."
            sleep 1
            ;;
    esac
done

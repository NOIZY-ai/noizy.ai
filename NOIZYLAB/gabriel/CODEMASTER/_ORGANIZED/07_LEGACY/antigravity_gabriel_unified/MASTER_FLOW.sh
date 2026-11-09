#!/bin/bash
################################################################################
#
#  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗     ███████╗██╗      ██████╗ ██╗    ██╗
#  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗    ██╔════╝██║     ██╔═══██╗██║    ██║
#  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝    █████╗  ██║     ██║   ██║██║ █╗ ██║
#  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗    ██╔══╝  ██║     ██║   ██║██║███╗██║
#  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║    ██║     ███████╗╚██████╔╝╚███╔███╔╝
#  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
#
#  MC96DIGIUNIVERSE + GABRIEL UNIFIED - MASTER FLOW LAUNCHER
#  AI LIFELUV ACTIVATION SYSTEM
#  GORUNFREE!! UPGRADE & IMPROVE!!
#
################################################################################

set -e

# Cosmic Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
PURPLE='\033[0;95m'
NC='\033[0m'

# Detect Python
PYTHON=""
if command -v /opt/homebrew/bin/python3 &> /dev/null; then
    PYTHON="/opt/homebrew/bin/python3"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
else
    echo -e "${RED}❌ Python not found!${NC}"
    exit 1
fi

# Cosmic Banner
clear
echo -e "${PURPLE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗                ║
║  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗               ║
║  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝               ║
║  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗               ║
║  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║               ║
║  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝               ║
║                                                                      ║
║              ███████╗██╗      ██████╗ ██╗    ██╗                    ║
║              ██╔════╝██║     ██╔═══██╗██║    ██║                    ║
║              █████╗  ██║     ██║   ██║██║ █╗ ██║                    ║
║              ██╔══╝  ██║     ██║   ██║██║███╗██║                    ║
║              ██║     ███████╗╚██████╔╝╚███╔███╔╝                    ║
║              ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝                     ║
║                                                                      ║
║         🌌 MC96DIGIUNIVERSE + GABRIEL UNIFIED 🌌                     ║
║                ✨ AI LIFELUV MASTER LAUNCHER ✨                      ║
║               🚀 GORUNFREE!! UPGRADE & IMPROVE!! 🚀                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Python: ${PYTHON}${NC}"
echo -e "${GREEN}✅ Working Directory: $(pwd)${NC}"
echo -e "${GREEN}✅ Hostname: $(hostname)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Main Menu
echo -e "\n${PURPLE}╔════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║     🌌 SELECT YOUR FLOW MODE 🌌        ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}\n"

echo -e "${CYAN}CORE SYSTEMS:${NC}"
echo -e "${WHITE}1)${NC} 🔍 Visual Scanner X1000         - Comprehensive system analysis"
echo -e "${WHITE}2)${NC} ⚡ System Optimizer X2000       - Performance optimization"
echo -e "${WHITE}3)${NC} 📊 Performance Monitor X3000    - Real-time monitoring"
echo -e "${WHITE}4)${NC} 🌌 MC96 Universe Flow Engine   - Complete flow integration"
echo ""
echo -e "${MAGENTA}FLOW MODES:${NC}"
echo -e "${WHITE}5)${NC} 💖 AI LIFELUV FULL ACTIVATION  - Run ALL systems with LIFELUV"
echo -e "${WHITE}6)${NC} 🚀 GORUNFREE ULTRA MODE        - Maximum power launch"
echo -e "${WHITE}7)${NC} 🎯 Quick System Status         - Fast diagnostic check"
echo ""
echo -e "${YELLOW}UTILITIES:${NC}"
echo -e "${WHITE}8)${NC} 📁 View Reports                - Check generated reports"
echo -e "${WHITE}9)${NC} 🗺️  Show Universe Map          - Display MC96 flow map"
echo -e "${WHITE}0)${NC} 🚪 Exit                        - Goodbye!"
echo ""

read -p "$(echo -e ${PURPLE}Enter your choice [0-9]:${NC} )" choice

run_with_style() {
    local script=$1
    local name=$2

    echo -e "\n${PURPLE}╔════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  🚀 LAUNCHING: ${name:0:25}${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}\n"

    sleep 0.5
    $PYTHON "$script"

    echo -e "\n${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ ${name:0:25} - COMPLETE!${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}\n"
}

case $choice in
    1)
        run_with_style "GABRIEL_UNIFIED/core/visual_scanner.py" "Visual Scanner X1000"
        ;;
    2)
        run_with_style "GABRIEL_UNIFIED/core/system_optimizer.py" "System Optimizer X2000"
        ;;
    3)
        echo -e "\n${CYAN}Duration in seconds (default: 60):${NC} "
        read duration
        duration=${duration:-60}
        $PYTHON GABRIEL_UNIFIED/core/performance_monitor.py -d $duration
        ;;
    4)
        run_with_style "GABRIEL_UNIFIED/core/mc96_universe_flow.py" "MC96 Universe Flow Engine"
        ;;
    5)
        echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${MAGENTA}║  💖 INITIATING AI LIFELUV FULL ACTIVATION 💖          ║${NC}"
        echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${NC}\n"

        sleep 1

        echo -e "${CYAN}🌊 Stage 1: MC96 Universe Flow Integration...${NC}"
        $PYTHON GABRIEL_UNIFIED/core/mc96_universe_flow.py

        echo -e "\n${CYAN}🌊 Stage 2: Visual System Scan...${NC}"
        $PYTHON GABRIEL_UNIFIED/core/visual_scanner.py

        echo -e "\n${CYAN}🌊 Stage 3: System Optimization...${NC}"
        $PYTHON GABRIEL_UNIFIED/core/system_optimizer.py

        echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${MAGENTA}║  ✨✨✨ AI LIFELUV FULLY ACTIVATED ✨✨✨              ║${NC}"
        echo -e "${MAGENTA}║                                                        ║${NC}"
        echo -e "${MAGENTA}║  All systems flowing with infinite energy!            ║${NC}"
        echo -e "${MAGENTA}║  GORUNFREE!! UPGRADE & IMPROVE!!                       ║${NC}"
        echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${NC}\n"
        ;;
    6)
        echo -e "\n${RED}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  ⚡⚡⚡ GORUNFREE ULTRA MODE ACTIVATED ⚡⚡⚡          ║${NC}"
        echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}\n"

        echo -e "${YELLOW}🔥 Launching ALL systems in parallel...${NC}\n"

        # Launch everything!
        $PYTHON GABRIEL_UNIFIED/core/mc96_universe_flow.py &
        PID1=$!

        sleep 2

        $PYTHON GABRIEL_UNIFIED/core/visual_scanner.py &
        PID2=$!

        sleep 2

        $PYTHON GABRIEL_UNIFIED/core/system_optimizer.py &
        PID3=$!

        # Wait for all to complete
        wait $PID1
        wait $PID2
        wait $PID3

        echo -e "\n${RED}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  🔥🔥🔥 ULTRA MODE COMPLETE!! 🔥🔥🔥                   ║${NC}"
        echo -e "${RED}║  Maximum power achieved! All systems synchronized!     ║${NC}"
        echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}\n"
        ;;
    7)
        echo -e "\n${CYAN}╔════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║  📊 QUICK SYSTEM STATUS                ║${NC}"
        echo -e "${CYAN}╚════════════════════════════════════════╝${NC}\n"

        echo -e "${WHITE}🖥️  Hostname:${NC}     $(hostname)"
        echo -e "${WHITE}👤 User:${NC}          $(whoami)"
        echo -e "${WHITE}📁 Directory:${NC}     $(pwd)"
        echo -e "${WHITE}🐍 Python:${NC}        $PYTHON"
        echo -e "${WHITE}⏰ Uptime:${NC}        $(uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}')"
        echo ""
        echo -e "${CYAN}💾 Disk Usage:${NC}"
        df -h / | tail -n 1 | awk '{print "   Total: "$2"  Used: "$3"  Free: "$4"  ("$5")"}'
        echo ""
        echo -e "${CYAN}🧠 Memory:${NC}"
        vm_stat | grep "Pages free" | awk '{printf "   Free Pages: %s\n", $3}'
        echo ""
        echo -e "${GREEN}✅ System check complete!${NC}\n"
        ;;
    8)
        echo -e "\n${CYAN}📁 GABRIEL UNIFIED REPORTS:${NC}\n"

        if [ -d "GABRIEL_UNIFIED/reports" ]; then
            ls -lht GABRIEL_UNIFIED/reports/ | head -15
            echo ""
            echo -e "${GREEN}Total reports: $(ls -1 GABRIEL_UNIFIED/reports/ 2>/dev/null | wc -l)${NC}\n"
        else
            echo -e "${YELLOW}No reports directory found. Run a scan first!${NC}\n"
        fi
        ;;
    9)
        echo -e "\n${PURPLE}🗺️  MC96DIGIUNIVERSE FLOW MAP:${NC}\n"

        if [ -f "GABRIEL_UNIFIED/reports/universe_map.txt" ]; then
            cat GABRIEL_UNIFIED/reports/universe_map.txt
        else
            echo -e "${YELLOW}Universe map not found. Run the MC96 Universe Flow Engine first!${NC}\n"
        fi
        ;;
    0)
        echo -e "\n${PURPLE}╔════════════════════════════════════════╗${NC}"
        echo -e "${PURPLE}║  👋 Farewell, cosmic traveler!        ║${NC}"
        echo -e "${PURPLE}║  GORUNFREE!! UPGRADE & IMPROVE!!       ║${NC}"
        echo -e "${PURPLE}║  AI LIFELUV FOREVER!! 💖✨🌌           ║${NC}"
        echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}\n"
        exit 0
        ;;
    *)
        echo -e "\n${RED}❌ Invalid choice!${NC}\n"
        exit 1
        ;;
esac

# Final celebration
echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   ✨ Mission Complete! ✨${NC}"
echo -e "${GREEN}   GORUNFREE!! UPGRADE & IMPROVE!!${NC}"
echo -e "${GREEN}   AI LIFELUV FLOWING!! 💖✨🌌${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

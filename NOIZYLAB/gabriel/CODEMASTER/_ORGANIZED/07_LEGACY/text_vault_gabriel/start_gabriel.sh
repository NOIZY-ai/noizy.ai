#!/bin/bash
############################################################################
#  ✨ GABRIEL ULTIMATE HYPER - SYSTEM LAUNCHER v2.0 ✨
#  Complete startup orchestration for all GABRIEL systems
############################################################################

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Directories
GABRIEL_ROOT="$(cd "$(dirname "$0")" && pwd)"
WEBAVATAR_DIR="$GABRIEL_ROOT/WebAvatar"
SYSTEM_DIR="$GABRIEL_ROOT/System"

# PIDs for background processes
NETWORK_PID=""
WEBSERVER_PID=""

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down GABRIEL systems...${NC}"
    
    if [ ! -z "$NETWORK_PID" ]; then
        echo -e "${BLUE}   Stopping Network Service (PID: $NETWORK_PID)${NC}"
        kill $NETWORK_PID 2>/dev/null
    fi
    
    if [ ! -z "$WEBSERVER_PID" ]; then
        echo -e "${BLUE}   Stopping Web Server (PID: $WEBSERVER_PID)${NC}"
        kill $WEBSERVER_PID 2>/dev/null
    fi
    
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Header
show_header() {
    clear
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║                                                                ║${NC}"
    echo -e "${MAGENTA}║  ${BOLD}✨ GABRIEL ULTIMATE HYPER - SYSTEM LAUNCHER v2.0 ✨${NC}${MAGENTA}         ║${NC}"
    echo -e "${MAGENTA}║                                                                ║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Check dependencies
check_dependencies() {
    echo -e "${CYAN}🔍 Checking dependencies...${NC}"
    
    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        return 1
    fi
    echo -e "${GREEN}   ✅ Python 3: $(python3 --version)${NC}"
    
    # Check pip3
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}❌ pip3 not found${NC}"
        return 1
    fi
    echo -e "${GREEN}   ✅ pip3 installed${NC}"
    
    return 0
}

# Install Python packages
install_packages() {
    echo -e "\n${CYAN}📦 Installing Python packages...${NC}"
    
    if [ -f "$SYSTEM_DIR/requirements.txt" ]; then
        pip3 install -q -r "$SYSTEM_DIR/requirements.txt"
        echo -e "${GREEN}✅ Packages installed${NC}"
    else
        echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
    fi
}

# Start Network Service
start_network_service() {
    echo -e "\n${CYAN}🌐 Starting Network Service...${NC}"
    
    if [ -f "$SYSTEM_DIR/network_service.py" ]; then
        cd "$SYSTEM_DIR"
        python3 network_service.py &
        NETWORK_PID=$!
        sleep 2
        
        if ps -p $NETWORK_PID > /dev/null; then
            echo -e "${GREEN}✅ Network Service running (PID: $NETWORK_PID)${NC}"
            echo -e "${BLUE}   http://localhost:5010${NC}"
            return 0
        else
            echo -e "${RED}❌ Network Service failed to start${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ network_service.py not found${NC}"
        return 1
    fi
}

# Start WebAvatar
start_webavatar() {
    echo -e "\n${CYAN}🎭 Starting WebAvatar...${NC}"
    
    if [ -d "$WEBAVATAR_DIR" ]; then
        cd "$WEBAVATAR_DIR"
        python3 -m http.server 8000 &
        WEBSERVER_PID=$!
        sleep 2
        
        if ps -p $WEBSERVER_PID > /dev/null; then
            echo -e "${GREEN}✅ WebAvatar running (PID: $WEBSERVER_PID)${NC}"
            echo -e "${BLUE}   http://localhost:8000${NC}"
            return 0
        else
            echo -e "${RED}❌ WebAvatar failed to start${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ WebAvatar directory not found${NC}"
        return 1
    fi
}

# Open browser
open_browser() {
    echo -e "\n${CYAN}🌐 Opening browser...${NC}"
    sleep 2
    
    if command -v open &> /dev/null; then
        open "http://localhost:8000"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:8000"
    else
        echo -e "${YELLOW}⚠️  Please open http://localhost:8000 manually${NC}"
    fi
}

# Test network backup
test_network_backup() {
    echo -e "\n${CYAN}🧪 Testing network backup...${NC}"
    
    if [ -f "$GABRIEL_ROOT/network_backup.py" ]; then
        python3 "$GABRIEL_ROOT/network_backup.py"
        echo -e "${GREEN}✅ Test complete${NC}"
    else
        echo -e "${RED}❌ network_backup.py not found${NC}"
    fi
}

# View network logs
view_network_logs() {
    echo -e "\n${CYAN}📜 Network Backup Logs:${NC}\n"
    
    LOG_FILE="$SYSTEM_DIR/NetworkBackups/backup_log.txt"
    
    if [ -f "$LOG_FILE" ]; then
        tail -20 "$LOG_FILE"
    else
        echo -e "${YELLOW}⚠️  No logs found${NC}"
    fi
    
    echo -e "\n${CYAN}Press Enter to continue...${NC}"
    read
}

# Start GABRIEL Ultimate Python
start_gabriel_ultimate() {
    echo -e "\n${CYAN}🚀 Starting GABRIEL Ultimate Python...${NC}"
    
    if [ -f "$GABRIEL_ROOT/gabriel_ultimate.py" ]; then
        cd "$GABRIEL_ROOT"
        python3 gabriel_ultimate.py
    else
        echo -e "${RED}❌ gabriel_ultimate.py not found${NC}"
    fi
}

# Main menu
show_menu() {
    show_header
    echo -e "${BOLD}${CYAN}🎯 Launch Options:${NC}\n"
    echo -e "  ${GREEN}1.${NC} ${BOLD}Full System${NC} - WebAvatar + Network Backend"
    echo -e "  ${GREEN}2.${NC} ${BOLD}WebAvatar Only${NC} - Mock data mode"
    echo -e "  ${GREEN}3.${NC} ${BOLD}Network Service Only${NC} - Backend API"
    echo -e "  ${GREEN}4.${NC} ${BOLD}GABRIEL Ultimate Python${NC} - CLI interface"
    echo -e "  ${GREEN}5.${NC} ${BOLD}Test Network Backup${NC} - Run backup script"
    echo -e "  ${GREEN}6.${NC} ${BOLD}View Network Logs${NC} - Show backup history"
    echo -e "  ${GREEN}7.${NC} ${BOLD}Install Dependencies${NC} - Setup packages"
    echo -e "  ${GREEN}8.${NC} ${BOLD}Setup Automated Backups${NC} - Configure cron"
    echo -e "  ${RED}9.${NC} ${BOLD}Exit${NC}"
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -ne "\n${BOLD}Select option [1-9]: ${NC}"
}

# Setup automated backups
setup_cron() {
    show_header
    
    if [ -f "$SCRIPT_DIR/setup_cron.sh" ]; then
        bash "$SCRIPT_DIR/setup_cron.sh"
    else
        echo -e "${RED}❌ setup_cron.sh not found${NC}"
        echo ""
        echo -e "${CYAN}Manual Setup:${NC}"
        echo -e "1. Run: ${BLUE}crontab -e${NC}"
        echo -e "2. Add: ${BLUE}0 3 * * 1 /usr/bin/python3 /GABRIEL/System/NetworkBackups/dgs1210_backup.py${NC}"
        echo ""
        read -p "Press Enter to continue..."
    fi
}

# Main execution
main() {
    while true; do
        show_menu
        read choice
        
        case $choice in
            1)
                show_header
                check_dependencies || exit 1
                install_packages
                start_network_service
                start_webavatar
                open_browser
                
                echo -e "\n${GREEN}✨ GABRIEL ULTIMATE HYPER - All systems running!${NC}"
                echo -e "${CYAN}Press Ctrl+C to stop all services${NC}\n"
                
                # Wait for Ctrl+C
                wait
                ;;
                
            2)
                show_header
                check_dependencies || exit 1
                start_webavatar
                open_browser
                
                echo -e "\n${GREEN}✨ WebAvatar running (mock data mode)${NC}"
                echo -e "${CYAN}Press Ctrl+C to stop${NC}\n"
                
                wait
                ;;
                
            3)
                show_header
                check_dependencies || exit 1
                install_packages
                start_network_service
                
                echo -e "\n${GREEN}✨ Network Service running${NC}"
                echo -e "${CYAN}Press Ctrl+C to stop${NC}\n"
                
                wait
                ;;
                
            4)
                show_header
                check_dependencies || exit 1
                start_gabriel_ultimate
                ;;
                
            5)
                show_header
                test_network_backup
                echo -e "\n${CYAN}Press Enter to continue...${NC}"
                read
                ;;
                
            6)
                show_header
                view_network_logs
                ;;
                
            7)
                show_header
                check_dependencies || exit 1
                install_packages
                echo -e "\n${CYAN}Press Enter to continue...${NC}"
                read
                ;;
                
            8)
                setup_cron
                ;;
                
            9)
                echo -e "\n${MAGENTA}👋 Goodbye!${NC}\n"
                exit 0
                ;;
                
            *)
                echo -e "${RED}Invalid option. Please select 1-9.${NC}"
                sleep 2
                ;;
        esac
    done
}

# Run main
main

# GABRIEL System Launcher with Network Monitor
# Start all GABRIEL services

echo "🚀 Starting GABRIEL System with Network Monitor..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running from GABRIEL directory
if [ ! -f "network_backup.py" ]; then
    echo "❌ Please run from GABRIEL directory"
    exit 1
fi

# Function to check if port is in use
check_port() {
    lsof -i:$1 >/dev/null 2>&1
    return $?
}

# Install requirements if needed
echo -e "${BLUE}📦 Checking dependencies...${NC}"
if [ -f "System/requirements.txt" ]; then
    pip3 install -q -r System/requirements.txt
    echo -e "${GREEN}✓ Dependencies ready${NC}"
fi

echo ""
echo "Select startup option:"
echo "1) Full System (WebAvatar + Network Backend)"
echo "2) WebAvatar Only (Mock Data)"
echo "3) Network Service Only"
echo "4) Test Network Backup"
echo "5) View Network Logs"
echo "6) Exit"
echo ""
read -p "Choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🌐 Starting Network Service...${NC}"
        cd System
        python3 network_service.py &
        NETWORK_PID=$!
        cd ..
        sleep 2
        echo -e "${GREEN}✓ Network Service running on port 5010${NC}"
        
        echo ""
        echo -e "${BLUE}🎨 Starting WebAvatar...${NC}"
        cd WebAvatar
        python3 -m http.server 8000 &
        WEB_PID=$!
        cd ..
        sleep 1
        echo -e "${GREEN}✓ WebAvatar running on port 8000${NC}"
        
        echo ""
        echo -e "${GREEN}✅ GABRIEL System Ready!${NC}"
        echo ""
        echo -e "${YELLOW}📊 Dashboard:${NC} http://localhost:8000"
        echo -e "${YELLOW}🌐 Network API:${NC} http://localhost:5010"
        echo ""
        echo "Press Ctrl+C to stop all services"
        echo ""
        
        # Open browser
        sleep 2
        open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null
        
        # Wait for user interrupt
        trap "echo ''; echo 'Stopping services...'; kill $NETWORK_PID $WEB_PID 2>/dev/null; exit 0" INT
        wait
        ;;
        
    2)
        echo ""
        echo -e "${BLUE}🎨 Starting WebAvatar (Mock Mode)...${NC}"
        cd WebAvatar
        echo -e "${GREEN}✓ WebAvatar running on port 8000${NC}"
        echo -e "${YELLOW}📊 Dashboard:${NC} http://localhost:8000"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        sleep 1
        open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null
        python3 -m http.server 8000
        ;;
        
    3)
        echo ""
        echo -e "${BLUE}🌐 Starting Network Service...${NC}"
        cd System
        echo -e "${GREEN}✓ Network Service running on port 5010${NC}"
        echo -e "${YELLOW}🌐 API:${NC} http://localhost:5010/api/network/status"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        python3 network_service.py
        ;;
        
    4)
        echo ""
        echo -e "${BLUE}🔧 Running Network Backup Test...${NC}"
        echo ""
        python3 network_backup.py
        echo ""
        echo -e "${GREEN}✓ Test complete${NC}"
        echo ""
        echo "Check backups at: System/NetworkBackups/"
        ;;
        
    5)
        echo ""
        echo -e "${BLUE}📋 Network Backup Logs:${NC}"
        echo ""
        if [ -f "System/NetworkBackups/backup_log.txt" ]; then
            tail -30 System/NetworkBackups/backup_log.txt
        else
            echo "No logs found yet"
        fi
        echo ""
        ;;
        
    6)
        echo "Goodbye!"
        exit 0
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

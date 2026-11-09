#!/bin/bash
# 🧠 NOIZYLAB UNIFIED COMMAND CENTER
# Master control script for all services

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

ROOT="/Users/m2ultra/NOIZYLAB/UNIFIED_MCP"
GABRIEL_ROOT="/Users/m2ultra/NOIZYLAB/GABRIEL"
LOG_DIR="$HOME/.noizylab/logs"
PLIST_DIR="$ROOT/production"

mkdir -p "$LOG_DIR"

print_header() {
    echo -e "${CYAN}${BOLD}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🧠 NOIZYLAB UNIFIED COMMAND CENTER                          ║
║                                                               ║
║   MCP Server + Dashboard + Agent                              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

check_deps() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}❌ Python3 not found${NC}"
        exit 1
    fi
    
    python3 -c "import flask" 2>/dev/null || {
        echo -e "${YELLOW}Installing Flask...${NC}"
        pip3 install flask flask-cors
    }
    
    python3 -c "import mcp" 2>/dev/null || {
        echo -e "${YELLOW}Installing MCP SDK...${NC}"
        pip3 install mcp
    }
    
    echo -e "${GREEN}✓ All dependencies installed${NC}"
}

start_dashboard() {
    echo -e "${CYAN}Starting Dashboard Server...${NC}"
    
    if pgrep -f "dashboard/server.py" > /dev/null; then
        echo -e "${YELLOW}Dashboard already running${NC}"
    else
        cd "$ROOT/dashboard"
        python3 server.py > "$LOG_DIR/dashboard.log" 2>&1 &
        echo $! > "$ROOT/.dashboard.pid"
        echo -e "${GREEN}✓ Dashboard started (PID: $!)${NC}"
        echo -e "   http://localhost:5175"
    fi
}

start_agent() {
    echo -e "${CYAN}Starting GABRIEL Agent...${NC}"
    
    if pgrep -f "gabriel_agent.py" > /dev/null; then
        echo -e "${YELLOW}Agent already running${NC}"
    else
        cd "$GABRIEL_ROOT"
        python3 gabriel_agent.py > "$LOG_DIR/agent.log" 2>&1 &
        echo $! > "$ROOT/.agent.pid"
        echo -e "${GREEN}✓ Agent started (PID: $!)${NC}"
    fi
}

stop_all() {
    echo -e "${YELLOW}Stopping all services...${NC}"
    
    pkill -f "dashboard/server.py" 2>/dev/null || true
    pkill -f "gabriel_agent.py" 2>/dev/null || true
    pkill -f "noizylab_mcp.py" 2>/dev/null || true
    
    rm -f "$ROOT/.dashboard.pid" "$ROOT/.agent.pid"
    
    echo -e "${GREEN}✓ All services stopped${NC}"
}

show_status() {
    echo -e "\n${BOLD}SERVICE STATUS:${NC}\n"
    
    if pgrep -f "noizylab_mcp.py" > /dev/null; then
        echo -e "  MCP Server:    ${GREEN}● RUNNING${NC}"
    else
        echo -e "  MCP Server:    ${RED}○ STOPPED${NC} (starts via Windsurf)"
    fi
    
    if pgrep -f "dashboard/server.py" > /dev/null; then
        echo -e "  Dashboard:     ${GREEN}● RUNNING${NC} (http://localhost:5175)"
    else
        echo -e "  Dashboard:     ${RED}○ STOPPED${NC}"
    fi
    
    if pgrep -f "gabriel_agent.py" > /dev/null; then
        echo -e "  Agent:         ${GREEN}● RUNNING${NC}"
    else
        echo -e "  Agent:         ${RED}○ STOPPED${NC}"
    fi
    
    echo -e "\n${BOLD}LOG FILES:${NC}\n"
    echo -e "  Dashboard: $LOG_DIR/dashboard.log"
    echo -e "  Agent:     $LOG_DIR/agent.log"
    echo -e "  MCP:       $LOG_DIR/mcp.log"
    
    echo ""
}

install_launchd() {
    echo -e "${CYAN}Installing launchd services...${NC}"
    
    mkdir -p ~/Library/LaunchAgents
    
    cp "$PLIST_DIR/com.noizylab.dashboard.plist" ~/Library/LaunchAgents/
    cp "$PLIST_DIR/com.noizylab.agent.plist" ~/Library/LaunchAgents/
    
    launchctl load ~/Library/LaunchAgents/com.noizylab.dashboard.plist 2>/dev/null || true
    launchctl load ~/Library/LaunchAgents/com.noizylab.agent.plist 2>/dev/null || true
    
    echo -e "${GREEN}✓ Services installed and will start on login${NC}"
}

uninstall_launchd() {
    echo -e "${YELLOW}Uninstalling launchd services...${NC}"
    
    launchctl unload ~/Library/LaunchAgents/com.noizylab.dashboard.plist 2>/dev/null || true
    launchctl unload ~/Library/LaunchAgents/com.noizylab.agent.plist 2>/dev/null || true
    
    rm -f ~/Library/LaunchAgents/com.noizylab.*.plist
    
    echo -e "${GREEN}✓ Services uninstalled${NC}"
}

show_mcp_config() {
    echo -e "\n${BOLD}MCP CONFIG (add to Windsurf):${NC}\n"
    echo -e "${CYAN}"
    cat << 'EOF'
{
  "mcpServers": {
    "noizylab": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/UNIFIED_MCP/noizylab_mcp.py"]
    }
  }
}
EOF
    echo -e "${NC}"
}

open_dashboard() {
    if pgrep -f "dashboard/server.py" > /dev/null; then
        open "http://localhost:5175"
    else
        echo -e "${YELLOW}Starting dashboard first...${NC}"
        start_dashboard
        sleep 2
        open "http://localhost:5175"
    fi
}

case "${1:-help}" in
    start)
        print_header
        check_deps
        start_dashboard
        start_agent
        show_mcp_config
        echo -e "\n${GREEN}✓ NOIZYLAB started!${NC}"
        echo -e "  Dashboard: ${CYAN}http://localhost:5175${NC}"
        echo -e "  Restart Windsurf to activate MCP"
        ;;
    stop)
        print_header
        stop_all
        ;;
    restart)
        print_header
        stop_all
        sleep 1
        check_deps
        start_dashboard
        start_agent
        echo -e "\n${GREEN}✓ NOIZYLAB restarted!${NC}"
        ;;
    status)
        print_header
        show_status
        ;;
    dashboard)
        start_dashboard
        open_dashboard
        ;;
    agent)
        start_agent
        ;;
    install)
        print_header
        check_deps
        install_launchd
        show_mcp_config
        ;;
    uninstall)
        print_header
        stop_all
        uninstall_launchd
        ;;
    config)
        show_mcp_config
        ;;
    logs)
        tail -f "$LOG_DIR"/*.log
        ;;
    *)
        print_header
        echo -e "${BOLD}USAGE:${NC} $0 {command}\n"
        echo -e "${BOLD}COMMANDS:${NC}"
        echo -e "  ${GREEN}start${NC}      Start dashboard + agent"
        echo -e "  ${GREEN}stop${NC}       Stop all services"
        echo -e "  ${GREEN}restart${NC}    Restart all services"
        echo -e "  ${GREEN}status${NC}     Show service status"
        echo -e "  ${GREEN}dashboard${NC}  Start and open dashboard"
        echo -e "  ${GREEN}agent${NC}      Start agent only"
        echo -e "  ${GREEN}install${NC}    Install as system service (auto-start)"
        echo -e "  ${GREEN}uninstall${NC}  Remove system service"
        echo -e "  ${GREEN}config${NC}     Show MCP config for Windsurf"
        echo -e "  ${GREEN}logs${NC}       Tail all log files"
        echo ""
        ;;
esac

#!/bin/bash
# 🧠 GABRIEL UNIFIED LAUNCHER
# Starts both MCP Server + Autonomous Agent

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

GABRIEL_ROOT="/Users/m2ultra/NOIZYLAB/GABRIEL"
cd "$GABRIEL_ROOT"

echo -e "${CYAN}${BOLD}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🧠 GABRIEL UNIFIED SYSTEM                                   ║
║                                                               ║
║   MCP Server + Autonomous Agent                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check for existing processes
if pgrep -f "gabriel_mcp_v2.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  MCP Server already running${NC}"
else
    echo -e "${GREEN}Starting MCP Server...${NC}"
fi

if pgrep -f "gabriel_agent.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  Agent already running${NC}"
else
    echo -e "${GREEN}Starting Autonomous Agent...${NC}"
fi

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

MODE="${1:-all}"

case "$MODE" in
    mcp)
        echo -e "\n${CYAN}▶ Starting MCP Server only...${NC}\n"
        python3 gabriel_mcp_v2.py
        ;;
    agent)
        echo -e "\n${CYAN}▶ Starting Agent only...${NC}\n"
        python3 gabriel_agent.py
        ;;
    all)
        echo -e "\n${CYAN}▶ Starting both MCP + Agent...${NC}\n"
        
        # Start agent in background
        python3 gabriel_agent.py &
        AGENT_PID=$!
        echo -e "${GREEN}✓${NC} Agent started (PID: $AGENT_PID)"
        
        # Save PIDs
        echo "$AGENT_PID" > "$GABRIEL_ROOT/.agent.pid"
        
        echo -e "\n${YELLOW}MCP Server ready for Windsurf connection${NC}"
        echo -e "Add to your MCP config:"
        echo -e "${CYAN}\"gabriel\": {\"command\": \"python3\", \"args\": [\"$GABRIEL_ROOT/gabriel_mcp_v2.py\"]}${NC}\n"
        
        # Wait for agent
        wait $AGENT_PID
        ;;
    stop)
        echo -e "${YELLOW}Stopping GABRIEL...${NC}"
        pkill -f "gabriel_mcp_v2.py" 2>/dev/null || true
        pkill -f "gabriel_agent.py" 2>/dev/null || true
        rm -f "$GABRIEL_ROOT/.agent.pid"
        echo -e "${GREEN}✓ GABRIEL stopped${NC}"
        ;;
    status)
        echo -e "\n${BOLD}GABRIEL STATUS:${NC}\n"
        
        if pgrep -f "gabriel_mcp_v2.py" > /dev/null; then
            echo -e "  MCP Server:  ${GREEN}RUNNING${NC}"
        else
            echo -e "  MCP Server:  ${RED}STOPPED${NC}"
        fi
        
        if pgrep -f "gabriel_agent.py" > /dev/null; then
            echo -e "  Agent:       ${GREEN}RUNNING${NC}"
        else
            echo -e "  Agent:       ${RED}STOPPED${NC}"
        fi
        
        if [ -f "$GABRIEL_ROOT/agent_status.json" ]; then
            echo -e "\n${BOLD}Agent Status:${NC}"
            cat "$GABRIEL_ROOT/agent_status.json"
        fi
        ;;
    *)
        echo "Usage: $0 {mcp|agent|all|stop|status}"
        exit 1
        ;;
esac

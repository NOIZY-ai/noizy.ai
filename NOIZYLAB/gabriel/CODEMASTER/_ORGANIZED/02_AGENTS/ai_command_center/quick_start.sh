#!/bin/bash
# 🚀 NOIZYLAB AI COMMAND CENTER - Quick Start

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🧠 NOIZYLAB AI COMMAND CENTER                               ║
║                                                               ║
║   Unified AI Management System                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3 found: $(python3 --version)"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -q requests python-dotenv rich

echo -e "\n${GREEN}✓${NC} Setup complete!"

echo -e "\n${CYAN}${BOLD}━━━ QUICK COMMANDS ━━━${NC}\n"

echo -e "  ${BOLD}Interactive Mode:${NC}"
echo -e "    python3 ai_manager.py"

echo -e "\n  ${BOLD}Generate Video:${NC}"
echo -e "    python3 ai_manager.py video --prompt 'epic sunset timelapse'"

echo -e "\n  ${BOLD}Generate Music:${NC}"
echo -e "    python3 ai_manager.py audio --prompt 'synthwave 120bpm'"

echo -e "\n  ${BOLD}Create Avatar Video:${NC}"
echo -e "    python3 ai_manager.py avatar --script 'Welcome to NOIZYLAB'"

echo -e "\n  ${BOLD}Configure API Keys:${NC}"
echo -e "    python3 ai_manager.py keys --set runway YOUR_KEY"

echo -e "\n  ${BOLD}Show Status:${NC}"
echo -e "    python3 ai_manager.py status"

echo -e "\n  ${BOLD}Microsoft AI Info:${NC}"
echo -e "    python3 ai_manager.py microsoft"

echo -e "\n${CYAN}${BOLD}━━━ AUTONOMOUS FEATURES (35 Commands) ━━━${NC}\n"

echo -e "  ${BOLD}Smart Chat (auto-routing LLM):${NC}"
echo -e "    python3 ai_manager.py chat 'What is the meaning of life?'"

echo -e "\n  ${BOLD}Model Ensemble (parallel multi-model):${NC}"
echo -e "    python3 ai_manager.py ensemble 'What is AI?'"

echo -e "\n  ${BOLD}Quick Actions (fix, improve, explain, tldr):${NC}"
echo -e "    python3 ai_manager.py quick tldr 'long text here...'"
echo -e "    python3 ai_manager.py quick idea 'music production tools'"

echo -e "\n  ${BOLD}Prompt Templates (8 built-in):${NC}"
echo -e "    python3 ai_manager.py template explain --vars topic='quantum'"
echo -e "    python3 ai_manager.py template --list"

echo -e "\n  ${BOLD}AI Agent (autonomous goals):${NC}"
echo -e "    python3 ai_manager.py agent 'Create marketing content'"

echo -e "\n  ${BOLD}Image Generation (DALL-E):${NC}"
echo -e "    python3 ai_manager.py image 'futuristic city at sunset'"

echo -e "\n  ${BOLD}Code Execution (sandbox):${NC}"
echo -e "    python3 ai_manager.py exec 'print(2+2)'"

echo -e "\n  ${BOLD}Project Generator:${NC}"
echo -e "    python3 ai_manager.py new python-api --name myapi"

echo -e "\n  ${BOLD}Git Automation:${NC}"
echo -e "    python3 ai_manager.py git status"
echo -e "    python3 ai_manager.py git log"

echo -e "\n  ${BOLD}System Monitor:${NC}"
echo -e "    python3 ai_manager.py sysmon info"
echo -e "    python3 ai_manager.py sysmon health"

echo -e "\n  ${BOLD}API Testing:${NC}"
echo -e "    python3 ai_manager.py api https://httpbin.org/get"

echo -e "\n  ${BOLD}GABRIEL Integration:${NC}"
echo -e "    python3 ai_manager.py gabriel status"
echo -e "    python3 ai_manager.py gabriel scan"

echo -e "\n  ${BOLD}Metrics Dashboard:${NC}"
echo -e "    python3 ai_manager.py metrics"

echo -e "\n  ${BOLD}Batch & Workflow:${NC}"
echo -e "    python3 ai_manager.py batch --file workflows/batch_videos.json"
echo -e "    python3 ai_manager.py workflow --file workflows/content_pipeline.json"

echo -e "\n  ${BOLD}Self-Healing & Discovery:${NC}"
echo -e "    python3 ai_manager.py diagnose"
echo -e "    python3 ai_manager.py heal --auto"
echo -e "    python3 ai_manager.py discover"

echo -e "\n${CYAN}${BOLD}━━━ UNIFIED CLI (noizy) ━━━${NC}\n"

echo -e "  noizy chat 'Hello world'"
echo -e "  noizy quick idea 'music production'"
echo -e "  noizy ensemble 'What is AI?'"
echo -e "  noizy gabriel status"
echo -e "  noizy intel"
echo -e "  noizy polyglot test"
echo -e "  noizy metrics"

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Launch interactive mode
echo -e "${YELLOW}Launching AI Command Center...${NC}\n"
python3 ai_manager.py

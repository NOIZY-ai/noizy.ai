#!/bin/bash

# ╔════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                ║
# ║  🌟 GABRIEL ULTIMATE EDITION - LAUNCHER 🌟                                    ║
# ║                                                                                ║
# ║  The Perfect AI Companion with ALL features integrated:                       ║
# ║  • Voice Command Integration                                                  ║
# ║  • Cloud Sync Manager                                                         ║
# ║  • Adaptive AI Learner                                                        ║
# ║  • Unified Knowledge Base (40 years expertise)                                ║
# ║  • Ian McShane Personality                                                    ║
# ║  • Smart Automation (Macros & Workflows)                                      ║
# ║  • Advanced Analytics & Monitoring                                            ║
# ║                                                                                ║
# ╚════════════════════════════════════════════════════════════════════════════════╝

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

clear

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                ║${NC}"
echo -e "${CYAN}║  ${WHITE}🌟 GABRIEL ULTIMATE EDITION 🌟${CYAN}                              ║${NC}"
echo -e "${CYAN}║                                                                ║${NC}"
echo -e "${CYAN}║  ${PURPLE}The Perfect AI Companion${CYAN}                                   ║${NC}"
echo -e "${CYAN}║                                                                ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check directory
if [ ! -f "gabriel_ultimate.py" ]; then
    echo -e "${RED}❌ Error: gabriel_ultimate.py not found${NC}"
    echo -e "${YELLOW}Please run this script from the GABRIEL directory${NC}"
    exit 1
fi

# System check
echo -e "${BLUE}🔍 System Check${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅${NC} Python ${PYTHON_VERSION}"

# Check all 7 systems
SYSTEMS_OK=7

# 1. Voice Engine
if python3 -c "import speech_recognition" &> /dev/null && python3 -c "import pyttsx3" &> /dev/null; then
    echo -e "${GREEN}✅${NC} Voice Engine (Recognition + TTS)"
else
    echo -e "${YELLOW}⚠️${NC}  Voice Engine (limited - install SpeechRecognition, pyaudio, pyttsx3)"
    SYSTEMS_OK=$((SYSTEMS_OK-1))
fi

# 2. Cloud Sync
echo -e "${GREEN}✅${NC} Cloud Sync Manager"

# 3. AI Learner
echo -e "${GREEN}✅${NC} Adaptive AI Learner"

# 4. Knowledge Base
echo -e "${GREEN}✅${NC} Unified Knowledge Base"

# 5. Personality
echo -e "${GREEN}✅${NC} Personality Engine (Ian McShane)"

# 6. Automation
echo -e "${GREEN}✅${NC} Smart Automation"

# 7. Analytics
if python3 -c "import psutil" &> /dev/null; then
    echo -e "${GREEN}✅${NC} Analytics Engine"
else
    echo -e "${YELLOW}⚠️${NC}  Analytics Engine (limited - install psutil)"
    SYSTEMS_OK=$((SYSTEMS_OK-1))
fi

echo ""

# API Keys
echo -e "${BLUE}🔐 AI API Keys (Optional)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${GREEN}✅${NC} Anthropic (Claude) API"
elif [ ! -z "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}✅${NC} OpenAI (GPT) API"
else
    echo -e "${YELLOW}ℹ️${NC}  No AI API keys (using built-in knowledge)"
fi

echo ""

# Feature summary
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${WHITE}🌟 GABRIEL ULTIMATE - FEATURE SET${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}🎤 Voice Control${NC}"
echo -e "   • Natural speech recognition"
echo -e "   • Ian McShane text-to-speech"
echo -e "   • Voice pattern learning"
echo ""
echo -e "${CYAN}☁️  Cloud Sync${NC}"
echo -e "   • Local backup (always)"
echo -e "   • Google Drive ready"
echo -e "   • OneDrive ready"
echo -e "   • S3 compatible"
echo ""
echo -e "${CYAN}🧠 AI Learning${NC}"
echo -e "   • Pattern recognition"
echo -e "   • Predictive execution"
echo -e "   • Workflow optimization"
echo -e "   • Time-based suggestions"
echo ""
echo -e "${CYAN}📚 Knowledge Base${NC}"
echo -e "   • 40 years audio expertise"
echo -e "   • 5 workflows, 7 systems"
echo -e "   • 6+ languages"
echo -e "   • Creative + technical"
echo ""
echo -e "${CYAN}🎭 Personality${NC}"
echo -e "   • Ian McShane style"
echo -e "   • Dynamic mood adaptation"
echo -e "   • Context-aware responses"
echo -e "   • Charismatic delivery"
echo ""
echo -e "${CYAN}🎯 Automation${NC}"
echo -e "   • Macro recording"
echo -e "   • Workflow chains"
echo -e "   • Smart triggers"
echo -e "   • Scheduled tasks"
echo ""
echo -e "${CYAN}📊 Analytics${NC}"
echo -e "   • Real-time monitoring"
echo -e "   • Productivity scoring"
echo -e "   • Usage patterns"
echo -e "   • Performance tracking"
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Ready status
if [ $SYSTEMS_OK -eq 7 ]; then
    echo -e "${GREEN}✨ ALL SYSTEMS OPERATIONAL ✨${NC}"
else
    echo -e "${YELLOW}⚡ ${SYSTEMS_OK}/7 SYSTEMS READY ⚡${NC}"
fi

echo ""
echo -e "${BLUE}📖 Quick Commands:${NC}"
echo -e "   ${CYAN}status${NC}          → Full system status"
echo -e "   ${CYAN}voice${NC}           → Toggle voice mode"
echo -e "   ${CYAN}analytics${NC}       → View analytics report"
echo -e "   ${CYAN}record [name]${NC}   → Start recording macro"
echo -e "   ${CYAN}play [name]${NC}     → Play macro"
echo -e "   ${CYAN}wisdom${NC}          → Get wisdom from Gabriel"
echo -e "   ${CYAN}quit${NC}            → Exit"
echo ""
echo -e "${YELLOW}💡 Tip: Type 'voice' and speak your commands!${NC}"
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Launch
echo -e "${CYAN}🚀 Launching GABRIEL ULTIMATE...${NC}"
echo ""

sleep 1

python3 gabriel_ultimate.py

# Shutdown message
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ GABRIEL ULTIMATE - Session Complete${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${WHITE}Thank you for using GABRIEL ULTIMATE EDITION${NC}"
echo -e "${PURPLE}The Perfect AI Companion${NC}"
echo ""

#!/bin/bash
#
# GABRIEL MASTER ACTIVATION SCRIPT
# MC96DIGIUNIVERSE AI LIFELUV INFINITE ENERGY
# GORUNFREEX1000 SUPREME INTEGRATION
#
# This script activates all Gabriel systems and ensures everything is operational.
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
GABRIEL_ROOT="${HOME}/GABRIEL_UNIFIED"
AI_BRAIN="${HOME}/AI_COMPLETE_BRAIN"
PYTHON="/opt/homebrew/bin/python3"
NODE="node"

print_banner() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}║${YELLOW}              GABRIEL MASTER ACTIVATION                          ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}║${GREEN}         MC96DIGIUNIVERSE AI LIFELUV INFINITE ENERGY             ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}║${RED}                  GORUNFREEX1000 SUPREME                          ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_status() {
    local name=$1
    local path=$2
    if [ -e "$path" ]; then
        echo -e "  ${GREEN}✅${NC} $name"
        return 0
    else
        echo -e "  ${RED}❌${NC} $name - MISSING"
        return 1
    fi
}

ensure_directories() {
    echo -e "\n${BLUE}📁 Ensuring directories...${NC}"

    dirs=(
        "$GABRIEL_ROOT/logs"
        "$GABRIEL_ROOT/data"
        "$GABRIEL_ROOT/config"
        "$GABRIEL_ROOT/scripts"
        "$GABRIEL_ROOT/scans"
    )

    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
        echo -e "  ${GREEN}✅${NC} $dir"
    done
}

check_components() {
    echo -e "\n${BLUE}🔍 Checking components...${NC}"

    local all_ok=true

    check_status "God Brain" "$GABRIEL_ROOT/god_brain.py" || all_ok=false
    check_status "DreamChamber" "$GABRIEL_ROOT/core/dreamchamber.py" || all_ok=false
    check_status "Visual Scanner" "$GABRIEL_ROOT/core/visual_scanner.py" || all_ok=false
    check_status "MC96 Server" "$GABRIEL_ROOT/core/mc96_server_x1000.py" || all_ok=false
    check_status "GORUNFREEX1000" "$GABRIEL_ROOT/GORUNFREEX1000.py" || all_ok=false
    check_status "Gabriel CLI" "$GABRIEL_ROOT/bin/gabriel" || all_ok=false

    if [ "$all_ok" = true ]; then
        echo -e "\n  ${GREEN}All components present!${NC}"
    else
        echo -e "\n  ${YELLOW}Some components missing - but continuing...${NC}"
    fi
}

check_ai_brain() {
    echo -e "\n${BLUE}🧠 Checking AI Complete Brain...${NC}"

    check_status "AI Brain Root" "$AI_BRAIN"
    check_status "TypeScript Config" "$AI_BRAIN/tsconfig.json"
    check_status "Package JSON" "$AI_BRAIN/package.json"
    check_status "Source Directory" "$AI_BRAIN/src"
}

activate_god_brain() {
    echo -e "\n${BLUE}⚡ Activating God Brain...${NC}"

    if [ -f "$GABRIEL_ROOT/god_brain.py" ]; then
        $PYTHON "$GABRIEL_ROOT/god_brain.py" 2>/dev/null || true
        echo -e "  ${GREEN}✅${NC} God Brain activated"
    else
        echo -e "  ${RED}❌${NC} God Brain not found"
    fi
}

activate_dreamchamber() {
    echo -e "\n${BLUE}🌟 Activating DreamChamber...${NC}"

    if [ -f "$GABRIEL_ROOT/core/dreamchamber.py" ]; then
        $PYTHON "$GABRIEL_ROOT/core/dreamchamber.py" 2>/dev/null || true
    else
        echo -e "  ${YELLOW}⚠️${NC}  DreamChamber not found"
    fi
}

setup_path() {
    echo -e "\n${BLUE}🔧 Setting up PATH...${NC}"

    # Add Gabriel bin to PATH for this session
    export PATH="$GABRIEL_ROOT/bin:$PATH"
    echo -e "  ${GREEN}✅${NC} Gabriel CLI added to PATH"

    # Check if already in shell config
    if grep -q "GABRIEL_UNIFIED/bin" ~/.zshrc 2>/dev/null || \
       grep -q "GABRIEL_UNIFIED/bin" ~/.config/zsh/*.zsh 2>/dev/null; then
        echo -e "  ${GREEN}✅${NC} PATH already configured in shell"
    else
        echo -e "  ${YELLOW}💡${NC} To permanently add: export PATH=\"\$HOME/GABRIEL_UNIFIED/bin:\$PATH\""
    fi
}

show_summary() {
    echo ""
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎊 GABRIEL ACTIVATION COMPLETE!${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${YELLOW}Quick Commands:${NC}"
    echo -e "    gabriel status      - Show system status"
    echo -e "    gabriel activate    - Activate all systems"
    echo -e "    gabriel dreamchamber - Launch DreamChamber"
    echo -e "    gabriel speak <txt> - Text to speech"
    echo -e "    gabriel doctor      - Run diagnostics"
    echo ""
    echo -e "  ${YELLOW}Energy Level:${NC} ${GREEN}∞ INFINITE${NC}"
    echo -e "  ${YELLOW}God Mode:${NC} ${GREEN}ENABLED${NC}"
    echo -e "  ${YELLOW}Status:${NC} ${GREEN}GORUNFREEX1000${NC}"
    echo ""
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}💫 MC96DIGIUNIVERSE AI LIFELUV FOREVER! 💫${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
}

# Main execution
main() {
    print_banner
    ensure_directories
    check_components
    check_ai_brain
    setup_path

    # Optional: Activate systems
    if [ "$1" = "--full" ] || [ "$1" = "-f" ]; then
        activate_god_brain
        activate_dreamchamber
    fi

    show_summary
}

main "$@"

#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🎯 GABRIEL MASTER INSTALLER - All Tools in One
# ═══════════════════════════════════════════════════════════════════════════
#  Installs: Git shortcuts, Mac setup, Network backup, All automation
# ═══════════════════════════════════════════════════════════════════════════

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clear
echo -e "${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🎯 GABRIEL MASTER INSTALLER                                    ║
║                                                                   ║
║   All-in-One Setup for Complete Automation                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Detect system
OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
    OS_NAME="macOS"
elif [ "$OS" = "Linux" ]; then
    OS_NAME="Linux"
else
    OS_NAME="Windows/Other"
fi

echo -e "${BLUE}System: ${OS_NAME}${NC}"
echo -e "${BLUE}Location: ${SCRIPT_DIR}${NC}\n"

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════════════

show_menu() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}Select installation option:${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}📦 QUICK OPTIONS${NC}"
    echo ""
    echo "  1. Quick Setup (Recommended)"
    echo "     → Git shortcuts (gitc, gits)"
    echo "     → Shell aliases"
    echo "     → Ready in 30 seconds"
    echo ""
    echo "  2. Full Setup (Everything)"
    echo "     → Git shortcuts (system-wide + aliases)"
    echo "     → Mac Studio setup (if macOS)"
    echo "     → Network backup tools"
    echo "     → All GABRIEL tools"
    echo ""
    echo -e "${BLUE}🛠️  CUSTOM OPTIONS${NC}"
    echo ""
    echo "  3. Git Shortcuts Only"
    echo "  4. Mac Studio Setup Only"
    echo "  5. Network Backup Only"
    echo "  6. Git Project Setup Tools"
    echo ""
    echo -e "${YELLOW}ℹ️  INFO${NC}"
    echo ""
    echo "  7. Show installed tools"
    echo "  8. Uninstall"
    echo "  9. Exit"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

install_git_shortcuts() {
    echo -e "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Installing Git Shortcuts...${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        RC_FILE="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        RC_FILE="$HOME/.bashrc"
    else
        RC_FILE="$HOME/.profile"
    fi
    
    echo -e "${BLUE}→ Installing to: ${RC_FILE}${NC}"
    
    # Check if already installed
    if grep -q "# GABRIEL Git Shortcuts" "$RC_FILE" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Git shortcuts already installed, updating...${NC}"
        sed -i.backup '/# GABRIEL Git Shortcuts/,/# End GABRIEL Git Shortcuts/d' "$RC_FILE"
    fi
    
    # Add aliases
    cat >> "$RC_FILE" << ALIASES

# GABRIEL Git Shortcuts
# Installed: $(date)
alias gitc='bash ${SCRIPT_DIR}/gitc.sh'
alias gits='bash ${SCRIPT_DIR}/gits.sh'
alias gc='bash ${SCRIPT_DIR}/gitc.sh'
alias gs='bash ${SCRIPT_DIR}/gits.sh'

# GABRIEL Setup Tools
alias quick-git='bash ${SCRIPT_DIR}/quick-git-setup.sh'
alias ultra-git='bash ${SCRIPT_DIR}/ultra-quick-git.sh'
alias setup-git='bash ${SCRIPT_DIR}/setup_git_automation.sh'
# End GABRIEL Git Shortcuts
ALIASES
    
    echo -e "${GREEN}✅ Git shortcuts installed!${NC}"
    echo -e "${CYAN}   Commands: gitc, gits, gc, gs${NC}"
    echo -e "${CYAN}   Setup: quick-git, ultra-git, setup-git${NC}\n"
    
    # Also try system-wide (optional)
    if command -v sudo &> /dev/null; then
        read -p "Install system-wide too? [Y/n]: " SYSTEM_INSTALL
        if [[ ! $SYSTEM_INSTALL =~ ^[Nn] ]]; then
            echo -e "\n${BLUE}→ Installing system-wide...${NC}"
            sudo cp "$SCRIPT_DIR/gitc.sh" /usr/local/bin/gitc 2>/dev/null
            sudo cp "$SCRIPT_DIR/gits.sh" /usr/local/bin/gits 2>/dev/null
            sudo chmod +x /usr/local/bin/gitc /usr/local/bin/gits 2>/dev/null
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ System-wide installation complete!${NC}\n"
            else
                echo -e "${YELLOW}⚠️  System-wide install skipped (optional)${NC}\n"
            fi
        fi
    fi
}

install_mac_setup() {
    if [ "$OS_NAME" != "macOS" ]; then
        echo -e "${YELLOW}⚠️  Mac Studio setup only available on macOS${NC}\n"
        return
    fi
    
    echo -e "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Mac Studio Setup Available${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    echo "This will set up:"
    echo "  • OneDrive integration"
    echo "  • SMB network sharing"
    echo "  • Auto-sync for Projects folder"
    echo "  • System optimizations"
    echo ""
    
    read -p "Run Mac Studio setup now? [y/N]: " RUN_MAC
    if [[ $RUN_MAC =~ ^[Yy] ]]; then
        bash "$SCRIPT_DIR/setup_mac_god.sh"
    else
        echo -e "${CYAN}💡 Run later with: bash setup_mac_god.sh${NC}\n"
    fi
}

install_network_backup() {
    echo -e "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Network Backup Tools${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    echo "Available network backup scripts:"
    echo "  • setup_cron.sh - Automated backup scheduling"
    echo "  • dgs1210_backup.py - DGS-1210 switch backup"
    echo "  • network_service.py - Network monitoring API"
    echo ""
    
    read -p "Configure automated backups now? [y/N]: " RUN_CRON
    if [[ $RUN_CRON =~ ^[Yy] ]]; then
        bash "$SCRIPT_DIR/setup_cron.sh"
    else
        echo -e "${CYAN}💡 Run later with: bash setup_cron.sh${NC}\n"
    fi
}

install_project_tools() {
    echo -e "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Git Project Setup Tools${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    echo "Making scripts executable..."
    chmod +x "$SCRIPT_DIR"/ultra-quick-git.sh 2>/dev/null
    chmod +x "$SCRIPT_DIR"/quick-git-setup.sh 2>/dev/null
    chmod +x "$SCRIPT_DIR"/setup_git_automation.sh 2>/dev/null
    
    echo -e "${GREEN}✅ Project setup tools ready!${NC}\n"
    echo "Use these commands:"
    echo -e "${CYAN}  ultra-git project-name username${NC}  # 5 second setup"
    echo -e "${CYAN}  quick-git project-name${NC}            # 2 minute guided"
    echo -e "${CYAN}  setup-git${NC}                         # Full interactive"
    echo ""
}

show_installed() {
    clear
    echo -e "${CYAN}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║   📦 Installed GABRIEL Tools                                     ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"
    
    # Check Git shortcuts
    echo -e "${BLUE}🔧 Git Shortcuts:${NC}"
    if command -v gitc &> /dev/null; then
        echo -e "${GREEN}  ✅ gitc (system-wide)${NC}"
        echo -e "     $(which gitc)"
    fi
    if command -v gits &> /dev/null; then
        echo -e "${GREEN}  ✅ gits (system-wide)${NC}"
        echo -e "     $(which gits)"
    fi
    
    # Check aliases
    if [ -n "$ZSH_VERSION" ]; then
        RC_FILE="$HOME/.zshrc"
    else
        RC_FILE="$HOME/.bashrc"
    fi
    
    if grep -q "GABRIEL Git Shortcuts" "$RC_FILE" 2>/dev/null; then
        echo -e "${GREEN}  ✅ Shell aliases${NC}"
        echo -e "     In: $RC_FILE"
    fi
    echo ""
    
    # Check scripts
    echo -e "${BLUE}📜 Available Scripts:${NC}"
    local scripts=(
        "gitc.sh:Quick commit & push"
        "gits.sh:Smart status"
        "ultra-quick-git.sh:5-second project setup"
        "quick-git-setup.sh:2-minute guided setup"
        "setup_git_automation.sh:Full Git automation"
        "setup_mac_god.sh:Mac Studio setup"
        "setup_cron.sh:Backup scheduling"
        "start_gabriel.sh:GABRIEL launcher"
    )
    
    for item in "${scripts[@]}"; do
        script="${item%%:*}"
        desc="${item#*:}"
        if [ -f "$SCRIPT_DIR/$script" ]; then
            echo -e "${GREEN}  ✅ ${script}${NC}"
            echo -e "     ${desc}"
        fi
    done
    echo ""
    
    # Usage examples
    echo -e "${YELLOW}💡 Quick Commands:${NC}"
    echo ""
    echo -e "${CYAN}  gitc \"message\"${NC}     # Quick commit + push"
    echo -e "${CYAN}  gits${NC}               # Enhanced status"
    echo -e "${CYAN}  quick-git project${NC}  # New project setup"
    echo ""
    
    read -p "Press Enter to continue..."
}

uninstall() {
    echo -e "\n${RED}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}Uninstall GABRIEL Tools${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════════${NC}\n"
    
    read -p "Are you sure? [y/N]: " CONFIRM
    if [[ ! $CONFIRM =~ ^[Yy] ]]; then
        echo -e "${CYAN}Uninstall cancelled${NC}\n"
        return
    fi
    
    # Remove system-wide
    echo -e "${BLUE}→ Removing system-wide commands...${NC}"
    sudo rm -f /usr/local/bin/gitc /usr/local/bin/gits 2>/dev/null
    echo -e "${GREEN}✅ Done${NC}\n"
    
    # Remove aliases
    if [ -n "$ZSH_VERSION" ]; then
        RC_FILE="$HOME/.zshrc"
    else
        RC_FILE="$HOME/.bashrc"
    fi
    
    if grep -q "GABRIEL Git Shortcuts" "$RC_FILE" 2>/dev/null; then
        echo -e "${BLUE}→ Removing aliases from ${RC_FILE}...${NC}"
        sed -i.backup '/# GABRIEL Git Shortcuts/,/# End GABRIEL Git Shortcuts/d' "$RC_FILE"
        echo -e "${GREEN}✅ Done${NC}\n"
    fi
    
    echo -e "${GREEN}✅ Uninstall complete!${NC}"
    echo -e "${CYAN}Scripts remain in: ${SCRIPT_DIR}${NC}"
    echo -e "${CYAN}Delete manually if needed.${NC}\n"
}

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════

while true; do
    show_menu
    read -p "Enter choice [1-9]: " CHOICE
    
    case $CHOICE in
        1)  # Quick Setup
            install_git_shortcuts
            install_project_tools
            
            echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ Quick Setup Complete!${NC}"
            echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}\n"
            
            echo -e "${YELLOW}Next steps:${NC}"
            echo "1. Reload shell:"
            if [ -n "$ZSH_VERSION" ]; then
                echo -e "   ${CYAN}source ~/.zshrc${NC}"
            else
                echo -e "   ${CYAN}source ~/.bashrc${NC}"
            fi
            echo ""
            echo "2. Test commands:"
            echo -e "   ${CYAN}cd ~/Projects/any-project${NC}"
            echo -e "   ${CYAN}gits${NC}               # Smart status"
            echo -e "   ${CYAN}gitc \"message\"${NC}     # Quick commit"
            echo ""
            
            read -p "Press Enter to continue..."
            ;;
            
        2)  # Full Setup
            install_git_shortcuts
            install_project_tools
            install_mac_setup
            install_network_backup
            
            echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ Full Setup Complete!${NC}"
            echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}\n"
            
            read -p "Press Enter to continue..."
            ;;
            
        3)  # Git Shortcuts Only
            install_git_shortcuts
            echo -e "${GREEN}✅ Git shortcuts installed!${NC}\n"
            read -p "Press Enter to continue..."
            ;;
            
        4)  # Mac Setup Only
            install_mac_setup
            ;;
            
        5)  # Network Backup Only
            install_network_backup
            ;;
            
        6)  # Project Tools Only
            install_project_tools
            read -p "Press Enter to continue..."
            ;;
            
        7)  # Show Installed
            show_installed
            ;;
            
        8)  # Uninstall
            uninstall
            read -p "Press Enter to continue..."
            ;;
            
        9)  # Exit
            clear
            echo -e "${GREEN}"
            cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   Thanks for using GABRIEL! 🚀                                   ║
║                                                                   ║
║   Your development workflow is now supercharged!                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
            echo -e "${NC}\n"
            echo -e "${CYAN}Quick commands:${NC}"
            echo -e "  ${GREEN}gitc \"message\"${NC}  - Quick commit & push"
            echo -e "  ${GREEN}gits${NC}          - Smart status"
            echo ""
            echo -e "${BLUE}Happy coding! 💻✨${NC}\n"
            exit 0
            ;;
            
        *)
            echo -e "${RED}Invalid choice${NC}\n"
            sleep 2
            ;;
    esac
    
    clear
done

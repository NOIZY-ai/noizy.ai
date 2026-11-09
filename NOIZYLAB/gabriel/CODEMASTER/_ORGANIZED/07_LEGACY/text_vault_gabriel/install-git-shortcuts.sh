#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🔧 GIT SHORTCUTS INSTALLER
# ═══════════════════════════════════════════════════════════════════════════
#  Installs gitc and gits commands system-wide
# ═══════════════════════════════════════════════════════════════════════════

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🔧 Git Shortcuts Installer                                     ║
║                                                                   ║
║   gitc - Quick commit & push                                     ║
║   gits - Smart status                                            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Detect shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_NAME="zsh"
    RC_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_NAME="bash"
    RC_FILE="$HOME/.bashrc"
else
    SHELL_NAME="sh"
    RC_FILE="$HOME/.profile"
fi

echo -e "${BLUE}Detected shell: ${SHELL_NAME}${NC}"
echo -e "${BLUE}Config file: ${RC_FILE}${NC}\n"

# Installation method
echo "Choose installation method:"
echo ""
echo "  1. Aliases (Quick, user-only)"
echo "     → gitc and gits work in current shell"
echo ""
echo "  2. System-wide (Requires sudo)"
echo "     → gitc and gits work everywhere"
echo ""
echo "  3. Both (Recommended)"
echo "     → Maximum compatibility"
echo ""
read -p "Select [1-3]: " METHOD

case $METHOD in
    1)
        INSTALL_ALIASES=true
        INSTALL_SYSTEM=false
        ;;
    2)
        INSTALL_ALIASES=false
        INSTALL_SYSTEM=true
        ;;
    3)
        INSTALL_ALIASES=true
        INSTALL_SYSTEM=true
        ;;
    *)
        echo -e "${RED}Invalid selection${NC}"
        exit 1
        ;;
esac

echo ""

# ═══════════════════════════════════════════════════════════════════════════
#  SYSTEM-WIDE INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════

if [ "$INSTALL_SYSTEM" = true ]; then
    echo -e "${BLUE}Installing system-wide...${NC}"
    
    # Check if scripts exist
    if [ ! -f "$SCRIPT_DIR/gitc.sh" ] || [ ! -f "$SCRIPT_DIR/gits.sh" ]; then
        echo -e "${RED}❌ Scripts not found in: $SCRIPT_DIR${NC}"
        exit 1
    fi
    
    # Copy to /usr/local/bin
    echo "  Copying scripts to /usr/local/bin..."
    sudo cp "$SCRIPT_DIR/gitc.sh" /usr/local/bin/gitc
    sudo cp "$SCRIPT_DIR/gits.sh" /usr/local/bin/gits
    
    # Make executable
    sudo chmod +x /usr/local/bin/gitc
    sudo chmod +x /usr/local/bin/gits
    
    echo -e "${GREEN}  ✅ System-wide installation complete${NC}\n"
fi

# ═══════════════════════════════════════════════════════════════════════════
#  ALIAS INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════

if [ "$INSTALL_ALIASES" = true ]; then
    echo -e "${BLUE}Installing aliases to ${RC_FILE}...${NC}"
    
    # Check if aliases already exist
    if grep -q "# Git Shortcuts - GABRIEL" "$RC_FILE" 2>/dev/null; then
        echo -e "${YELLOW}  ⚠️  Aliases already exist, updating...${NC}"
        
        # Remove old aliases
        sed -i.backup '/# Git Shortcuts - GABRIEL/,/# End Git Shortcuts/d' "$RC_FILE"
    fi
    
    # Add new aliases
    cat >> "$RC_FILE" << ALIASES

# Git Shortcuts - GABRIEL
# Added by setup script on $(date)
alias gitc='bash ${SCRIPT_DIR}/gitc.sh'
alias gits='bash ${SCRIPT_DIR}/gits.sh'

# Ultra-short aliases (optional)
alias gc='bash ${SCRIPT_DIR}/gitc.sh'
alias gs='bash ${SCRIPT_DIR}/gits.sh'
# End Git Shortcuts
ALIASES
    
    echo -e "${GREEN}  ✅ Aliases added to ${RC_FILE}${NC}\n"
fi

# ═══════════════════════════════════════════════════════════════════════════
#  VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}Verifying installation...${NC}\n"

# Test system-wide
if [ "$INSTALL_SYSTEM" = true ]; then
    if command -v gitc &> /dev/null && command -v gits &> /dev/null; then
        echo -e "${GREEN}✅ System commands:${NC}"
        echo "   $(which gitc)"
        echo "   $(which gits)"
    else
        echo -e "${YELLOW}⚠️  System commands not in PATH yet${NC}"
    fi
fi

# Test aliases
if [ "$INSTALL_ALIASES" = true ]; then
    echo -e "${GREEN}✅ Aliases added to: ${RC_FILE}${NC}"
    echo "   Reload with: source ${RC_FILE}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
#  COMPLETION
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  ✅ Installation Complete!                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}📝 Next steps:${NC}"
echo ""

if [ "$INSTALL_ALIASES" = true ]; then
    echo "1. Reload shell configuration:"
    echo "   ${CYAN}source ${RC_FILE}${NC}"
    echo ""
fi

echo "2. Test the commands:"
echo "   ${CYAN}gits${NC}              # Smart status"
echo "   ${CYAN}gitc \"message\"${NC}    # Quick commit"
echo ""

echo "3. Start using in your projects:"
echo "   ${CYAN}cd ~/Projects/my-project${NC}"
echo "   ${CYAN}vim myfile.js${NC}"
echo "   ${CYAN}gitc \"Add feature X\"${NC}"
echo "   ${GREEN}✅ Auto-pushed to GitHub!${NC}"
echo ""

echo -e "${YELLOW}💡 Tip: Use 'gc' and 'gs' for even faster typing!${NC}"
echo ""

# Offer to reload now
if [ "$INSTALL_ALIASES" = true ]; then
    read -p "Reload shell now? [Y/n]: " RELOAD
    if [[ ! $RELOAD =~ ^[Nn] ]]; then
        echo ""
        echo -e "${BLUE}Reloading ${RC_FILE}...${NC}"
        source "$RC_FILE"
        echo -e "${GREEN}✅ Reloaded! Try: gits${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🚀 Happy coding!${NC}"

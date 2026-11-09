#!/bin/bash
# VS Code + macOS Shell Repair Script for user: rsp_ms
# This script fixes shell configuration issues and optimizes VS Code settings

set -e  # Exit on error

echo "=========================================="
echo "🔧 VS Code + macOS Shell Repair"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 0. Verify username
USER_NAME=$(whoami)
echo -e "${BLUE}[0/10] Verifying user...${NC}"
if [ "$USER_NAME" != "rsp_ms" ]; then
    echo -e "${RED}❌ Current user is $USER_NAME, expected rsp_ms.${NC}"
    echo "Please run this script as the correct user."
    exit 1
fi
echo -e "${GREEN}✓ User verified: $USER_NAME${NC}\n"

# 1. Backup VS Code settings
echo -e "${BLUE}[1/10] Backing up VS Code settings...${NC}"
BACKUP_DIR=~/vscode_backup/backup_$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
if [ -d ~/Library/Application\ Support/Code/User ]; then
    cp -r ~/Library/Application\ Support/Code/User "$BACKUP_DIR/"
    echo -e "${GREEN}✓ Backup created at: $BACKUP_DIR${NC}\n"
else
    echo -e "${YELLOW}⚠ VS Code User directory not found, skipping backup${NC}\n"
fi

# 2. Remove broken shell references
echo -e "${BLUE}[2/10] Searching for broken shell paths...${NC}"
if [ -d ~/Library/Application\ Support/Code/User ]; then
    BROKEN_FILES=$(grep -rl "/Users/rob/lucy.zsh" ~/Library/Application\ Support/Code/User 2>/dev/null || echo "")
    if [ -n "$BROKEN_FILES" ]; then
        echo "Found broken references in:"
        echo "$BROKEN_FILES"
        echo "$BROKEN_FILES" | xargs sed -i '' 's|/Users/rob/lucy.zsh|/bin/zsh|g'
        echo -e "${GREEN}✓ Fixed broken shell paths${NC}\n"
    else
        echo -e "${GREEN}✓ No broken shell paths found${NC}\n"
    fi
else
    echo -e "${YELLOW}⚠ VS Code directory not found${NC}\n"
fi

# 3. Fix settings.json (preserve existing settings, just fix shell)
echo -e "${BLUE}[3/10] Fixing VS Code settings.json...${NC}"
SETTINGS_FILE=~/Library/Application\ Support/Code/User/settings.json
if [ -f "$SETTINGS_FILE" ]; then
    # Remove old shell configurations
    sed -i '' '/terminal.integrated.shell.osx/d' "$SETTINGS_FILE"
    
    # Check if defaultProfile is already set
    if ! grep -q "terminal.integrated.defaultProfile.osx" "$SETTINGS_FILE"; then
        # Add before the last closing brace
        sed -i '' '$d' "$SETTINGS_FILE"  # Remove last }
        echo '  "terminal.integrated.defaultProfile.osx": "zsh"' >> "$SETTINGS_FILE"
        echo '}' >> "$SETTINGS_FILE"
    fi
    echo -e "${GREEN}✓ Settings.json updated${NC}\n"
else
    echo -e "${YELLOW}⚠ settings.json not found, skipping${NC}\n"
fi

# 4. Clear VS Code cache
echo -e "${BLUE}[4/10] Clearing VS Code cache...${NC}"
CACHE_CLEANED=0
for cache_dir in "Cache" "CachedData" "GPUCache" "Code Cache"; do
    if [ -d ~/Library/Application\ Support/Code/"$cache_dir" ]; then
        rm -rf ~/Library/Application\ Support/Code/"$cache_dir"
        ((CACHE_CLEANED++))
    fi
done
echo -e "${GREEN}✓ Cleared $CACHE_CLEANED cache directories${NC}\n"

# 5. Verify shell (don't change unless necessary)
echo -e "${BLUE}[5/10] Checking default shell...${NC}"
CURRENT_SHELL=$(dscl . -read ~/ UserShell | awk '{print $2}')
echo "Current shell: $CURRENT_SHELL"
if [[ "$CURRENT_SHELL" != *"zsh"* ]]; then
    echo "Setting default shell to zsh..."
    chsh -s /bin/zsh
    echo -e "${GREEN}✓ Shell changed to zsh${NC}\n"
else
    echo -e "${GREEN}✓ Shell is already zsh${NC}\n"
fi

# 6. Optimize .zshrc (backup first)
echo -e "${BLUE}[6/10] Optimizing .zshrc...${NC}"
if [ -f ~/.zshrc ]; then
    cp ~/.zshrc ~/.zshrc.backup_$(date +%Y%m%d_%H%M%S)
    
    # Remove duplicate nvm loading if exists
    if grep -q "nvm.sh" ~/.zshrc; then
        sed -i '' '/nvm.sh/d' ~/.zshrc
    fi
    
    # Add optimized nvm loading
    if [ -d ~/.nvm ]; then
        cat >> ~/.zshrc << 'ZSHRC'

# Optimized NVM loading (lazy load)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" --no-use  # Lazy load
ZSHRC
    fi
    echo -e "${GREEN}✓ .zshrc optimized${NC}\n"
else
    echo -e "${YELLOW}⚠ .zshrc not found, skipping${NC}\n"
fi

# 7. Check for VS Code updates (optional)
echo -e "${BLUE}[7/10] Checking for VS Code updates...${NC}"
if command -v brew &> /dev/null; then
    if brew list --cask visual-studio-code &> /dev/null; then
        echo "VS Code installed via Homebrew"
        read -p "Upgrade VS Code? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            brew upgrade --cask visual-studio-code
            echo -e "${GREEN}✓ VS Code upgraded${NC}\n"
        else
            echo -e "${YELLOW}⊘ Skipped VS Code upgrade${NC}\n"
        fi
    else
        echo -e "${YELLOW}⊘ VS Code not installed via Homebrew${NC}\n"
    fi
else
    echo -e "${YELLOW}⊘ Homebrew not found${NC}\n"
fi

# 8. Install useful zsh tools (optional)
echo -e "${BLUE}[8/10] Checking for zsh enhancements...${NC}"
if command -v brew &> /dev/null; then
    read -p "Install zsh-autosuggestions and zsh-syntax-highlighting? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        brew install zsh-autosuggestions zsh-syntax-highlighting 2>/dev/null || echo "Already installed"
        
        # Add to .zshrc if not present
        if ! grep -q "zsh-autosuggestions" ~/.zshrc; then
            echo "source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ~/.zshrc
        fi
        if ! grep -q "zsh-syntax-highlighting" ~/.zshrc; then
            echo "source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
        fi
        echo -e "${GREEN}✓ Zsh enhancements installed${NC}\n"
    else
        echo -e "${YELLOW}⊘ Skipped zsh enhancements${NC}\n"
    fi
else
    echo -e "${YELLOW}⊘ Homebrew not found${NC}\n"
fi

# 9. GPU fix for VS Code (if needed)
echo -e "${BLUE}[9/10] Adding GPU fix alias...${NC}"
if ! grep -q "alias code=" ~/.zshrc; then
    echo "" >> ~/.zshrc
    echo "# VS Code GPU fix (uncomment if experiencing blank screens)" >> ~/.zshrc
    echo "# alias code='code --disable-gpu'" >> ~/.zshrc
    echo -e "${GREEN}✓ GPU fix alias added (commented out)${NC}\n"
else
    echo -e "${GREEN}✓ VS Code alias already exists${NC}\n"
fi

# 10. Final verification
echo -e "${BLUE}[10/10] Final verification...${NC}"
echo "User: $(whoami)"
echo "Shell: $SHELL"
echo "VS Code settings backup: $BACKUP_DIR"
echo "Zsh config: ~/.zshrc"

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Repair Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. 🔄 Restart VS Code completely (Cmd+Q then reopen)"
echo "2. 🖥️  Open a new terminal in VS Code (Cmd+Shift+\`)"
echo "3. ✅ Test with: echo \"Terminal working: \$SHELL\""
echo "4. 📂 Your old settings are backed up in: $BACKUP_DIR"
echo ""
echo "If terminal still doesn't work:"
echo "- Run: code --disable-extensions"
echo "- Check: VS Code → Preferences → Settings → Terminal"
echo "- Verify: terminal.integrated.defaultProfile.osx = \"zsh\""
echo ""

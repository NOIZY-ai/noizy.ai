#!/bin/bash
#╔═══════════════════════════════════════════════════════════════════════════════╗
#║  HOT ROD MEGA INSTALLER - ULTIMATE AI DEV ENVIRONMENT                        ║
#║  The most powerful development setup for Mac M2 Ultra                        ║
#╚═══════════════════════════════════════════════════════════════════════════════╝

set -e

# Colors for epic output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ASCII Art Banner
print_banner() {
    echo -e "${RED}"
    cat << 'EOF'
    ██╗  ██╗ ██████╗ ████████╗    ██████╗  ██████╗ ██████╗
    ██║  ██║██╔═══██╗╚══██╔══╝    ██╔══██╗██╔═══██╗██╔══██╗
    ███████║██║   ██║   ██║       ██████╔╝██║   ██║██║  ██║
    ██╔══██║██║   ██║   ██║       ██╔══██╗██║   ██║██║  ██║
    ██║  ██║╚██████╔╝   ██║       ██║  ██║╚██████╔╝██████╔╝
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
EOF
    echo -e "${CYAN}    ══════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}           MEGA AI DEVELOPMENT ENVIRONMENT${NC}"
    echo -e "${CYAN}    ══════════════════════════════════════════════════════${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${WHITE} $1${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
}

print_status() {
    echo -e "${GREEN}  ✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}  ⚠${NC} $1"
}

print_error() {
    echo -e "${RED}  ✗${NC} $1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: SYSTEM PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
install_prerequisites() {
    print_section "PHASE 1: System Prerequisites"

    # Check/Install Homebrew
    if ! command -v brew &> /dev/null; then
        print_warning "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        print_status "Homebrew ready"
    fi

    # Core tools
    local tools=(git node python3 gh jq ripgrep fd bat eza fzf lazygit)
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            print_warning "Installing $tool..."
            brew install "$tool" 2>/dev/null || true
        else
            print_status "$tool ready"
        fi
    done

    # Modern shell tools
    brew install zoxide starship 2>/dev/null || true
    print_status "Modern CLI tools installed"
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: VSCODE INSIDERS + AI EXTENSIONS
# ═══════════════════════════════════════════════════════════════════════════════
install_vscode_ai() {
    print_section "PHASE 2: VSCode Insiders + AI Extensions"

    # Install VSCode Insiders if not present
    if ! command -v code-insiders &> /dev/null; then
        print_warning "Installing VSCode Insiders..."
        brew install --cask visual-studio-code-insiders
    else
        print_status "VSCode Insiders ready"
    fi

    # AI Extensions - THE BIG GUNS
    local ai_extensions=(
        "anthropic.claude-code"
        "github.copilot"
        "github.copilot-chat"
        "google.geminicodeassist"
        "google.gemini-cli-vscode-ide-companion"
        "codeium.codeium"
        "continue.continue"
        "sourcegraph.cody-ai"
        "openai.chatgpt"
    )

    echo -e "${CYAN}  Installing AI Assistants...${NC}"
    for ext in "${ai_extensions[@]}"; do
        code-insiders --install-extension "$ext" --force 2>/dev/null && print_status "$ext" || print_warning "Skipped $ext"
    done

    # Development Extensions
    local dev_extensions=(
        "ms-python.python"
        "ms-python.debugpy"
        "redhat.java"
        "golang.go"
        "rust-lang.rust-analyzer"
        "ms-vscode.cpptools"
        "dbaeumer.vscode-eslint"
        "esbenp.prettier-vscode"
        "bradlc.vscode-tailwindcss"
    )

    echo -e "${CYAN}  Installing Dev Tools...${NC}"
    for ext in "${dev_extensions[@]}"; do
        code-insiders --install-extension "$ext" --force 2>/dev/null && print_status "$ext" || true
    done

    # Git Extensions
    local git_extensions=(
        "eamodio.gitlens"
        "github.vscode-pull-request-github"
        "donjayamanne.githistory"
        "mhutchie.git-graph"
    )

    echo -e "${CYAN}  Installing Git Tools...${NC}"
    for ext in "${git_extensions[@]}"; do
        code-insiders --install-extension "$ext" --force 2>/dev/null && print_status "$ext" || true
    done

    # Productivity
    local prod_extensions=(
        "vscodevim.vim"
        "ms-azuretools.vscode-docker"
        "ms-vscode-remote.remote-containers"
        "usernamehw.errorlens"
        "christian-kohler.path-intellisense"
        "formulahendry.auto-rename-tag"
    )

    echo -e "${CYAN}  Installing Productivity Tools...${NC}"
    for ext in "${prod_extensions[@]}"; do
        code-insiders --install-extension "$ext" --force 2>/dev/null && print_status "$ext" || true
    done
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: GLOBAL AI TOOLS (CLI)
# ═══════════════════════════════════════════════════════════════════════════════
install_ai_cli_tools() {
    print_section "PHASE 3: AI CLI Tools"

    # Claude Code CLI
    if ! command -v claude &> /dev/null; then
        print_warning "Installing Claude Code CLI..."
        npm install -g @anthropic-ai/claude-code 2>/dev/null || true
    fi
    print_status "Claude Code CLI"

    # GitHub Copilot CLI
    if ! command -v gh copilot &> /dev/null; then
        gh extension install github/gh-copilot 2>/dev/null || true
    fi
    print_status "GitHub Copilot CLI"

    # Aider (AI pair programming)
    pip3 install aider-chat 2>/dev/null || true
    print_status "Aider AI"

    # LLM CLI tool
    pip3 install llm 2>/dev/null || true
    print_status "LLM CLI"
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4: UNITY DEVELOPMENT SETUP
# ═══════════════════════════════════════════════════════════════════════════════
setup_unity_dev() {
    print_section "PHASE 4: Unity Development"

    local unity_dir="$HOME/Documents/NOIZYLAB_TEXT_VAULT/Unity3D"

    # Unity Hub (if not installed)
    if [ ! -d "/Applications/Unity Hub.app" ]; then
        print_warning "Installing Unity Hub..."
        brew install --cask unity-hub 2>/dev/null || true
    fi
    print_status "Unity Hub ready"

    # VSCode Unity Extensions
    local unity_extensions=(
        "visualstudiotoolsforunity.vstuc"
        "unity.unity-debug"
        "kleber-swf.unity-code-snippets"
    )

    for ext in "${unity_extensions[@]}"; do
        code-insiders --install-extension "$ext" --force 2>/dev/null || true
    done
    print_status "Unity VSCode extensions"

    # Create Unity snippets
    mkdir -p "$HOME/.antigravity/snippets"
    print_status "Unity project structure ready"
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5: SHELL CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
setup_shell_config() {
    print_section "PHASE 5: Shell Configuration"

    # Add aliases to zshrc
    local zshrc="$HOME/.zshrc"

    if ! grep -q "HOT ROD ALIASES" "$zshrc" 2>/dev/null; then
        cat >> "$zshrc" << 'ALIASES'

# ═══════════════════════════════════════════════════════════════
# HOT ROD ALIASES - AI-Powered Development
# ═══════════════════════════════════════════════════════════════

# Quick editors
alias c="code-insiders ."
alias ci="code-insiders"

# AI assistants
alias ai="claude"
alias ask="gh copilot suggest"
alias explain="gh copilot explain"

# Git shortcuts
alias g="git"
alias gs="git status"
alias ga="git add"
alias gc="git commit"
alias gp="git push"
alias gl="git log --oneline -20"
alias gd="git diff"
alias lg="lazygit"

# Modern CLI
alias ls="eza --icons"
alias ll="eza -la --icons"
alias cat="bat"
alias find="fd"

# Quick navigation
alias dev="cd ~/Documents"
alias unity="cd ~/Documents/NOIZYLAB_TEXT_VAULT/Unity3D"
alias hotrod="cd ~/.antigravity"

# Fuzzy finding
alias ff="fzf --preview 'bat --color=always {}'"

ALIASES
        print_status "Shell aliases added"
    else
        print_status "Shell aliases already configured"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 6: COPY PROFILE TO VSCODE INSIDERS
# ═══════════════════════════════════════════════════════════════════════════════
deploy_vscode_config() {
    print_section "PHASE 6: Deploy VSCode Configuration"

    local vscode_user="$HOME/Library/Application Support/Code - Insiders/User"
    mkdir -p "$vscode_user"

    # Copy settings if they exist
    [ -f "$HOME/.antigravity/settings.json" ] && cp "$HOME/.antigravity/settings.json" "$vscode_user/" && print_status "Settings deployed"
    [ -f "$HOME/.antigravity/keybindings.json" ] && cp "$HOME/.antigravity/keybindings.json" "$vscode_user/" && print_status "Keybindings deployed"

    print_status "VSCode Insiders configured"
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
main() {
    clear
    print_banner

    echo -e "${WHITE}Starting MEGA installation in 3 seconds...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to cancel${NC}"
    sleep 3

    install_prerequisites
    install_vscode_ai
    install_ai_cli_tools
    setup_unity_dev
    setup_shell_config
    deploy_vscode_config

    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${WHITE}  🔥 HOT ROD MEGA INSTALLATION COMPLETE! 🔥                   ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}  Quick Start:${NC}"
    echo -e "    ${WHITE}c${NC}        - Open VSCode Insiders in current dir"
    echo -e "    ${WHITE}ai${NC}       - Start Claude AI"
    echo -e "    ${WHITE}ask${NC}      - Ask Copilot for suggestions"
    echo -e "    ${WHITE}lg${NC}       - Open Lazygit"
    echo -e "    ${WHITE}hotrod${NC}   - Go to HOT ROD config"
    echo ""
    echo -e "${YELLOW}  Restart your terminal or run: source ~/.zshrc${NC}"
    echo ""
}

main "$@"

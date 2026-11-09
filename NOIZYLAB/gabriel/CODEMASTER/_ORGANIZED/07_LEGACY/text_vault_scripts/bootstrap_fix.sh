#!/bin/bash
# GABRIEL macOS Bootstrap Fix
# Requires: bash (always available on macOS)
# Purpose: Fix VS Code shell configuration without relying on zsh

set -e

echo "🔧 GABRIEL macOS Bootstrap Fix"
echo "======================================"
echo ""

# Detect current user
CURRENT_USER=$(id -un)
HOME_DIR=$(eval echo ~$CURRENT_USER)

echo "📋 System Information:"
echo "   User: $CURRENT_USER"
echo "   Home: $HOME_DIR"
echo "   OS: $(uname -s)"
echo "   Shell: $(echo $SHELL)"
echo ""

# Step 1: Create clean .zshrc
echo "✅ Step 1: Creating clean shell configuration..."

cat > "$HOME_DIR/.zshrc" << 'ZSHRC_EOF'
# GABRIEL CODEMASTER - Clean zsh Configuration
# Created: 2025-11-12
# For: rsp_ms user

# Enforce zsh as the shell
export SHELL=/bin/zsh
export TERM=xterm-256color

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Homebrew (Apple Silicon)
if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Homebrew (Intel)
if [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
fi

# Python 3
export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"
export PATH="/usr/local/opt/python@3.12/bin:$PATH"
export PATH="/usr/bin/python3:$PATH"

# Local binaries
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/bin:$PATH"

# =============================================================================
# PYTHON CONFIGURATION
# =============================================================================

export PYTHONHOME=""
export PYTHONWARNINGS="ignore"

# =============================================================================
# ALIASES
# =============================================================================

alias ll='ls -lah'
alias la='ls -A'
alias python='python3'
alias pip='pip3'
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'

# =============================================================================
# HISTORY
# =============================================================================

HISTSIZE=50000
SAVEHIST=50000
HISTFILE="$HOME/.zsh_history"
setopt APPEND_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE

# =============================================================================
# PROMPT
# =============================================================================

PROMPT='%B%F{blue}rsp_ms%f:%F{cyan}%~%f%b $ '

# =============================================================================
# COMPLETION
# =============================================================================

autoload -Uz compinit && compinit -u 2>/dev/null || true

# =============================================================================
# STARTUP
# =============================================================================

echo "✅ GABRIEL Environment Ready"
echo "User: $(whoami) | Shell: $SHELL | Python: $(python3 --version 2>&1 | cut -d' ' -f2)"
ZSHRC_EOF

chmod 644 "$HOME_DIR/.zshrc"
echo "   ✅ Created: $HOME_DIR/.zshrc"
echo ""

# Step 2: Create VS Code settings backup
echo "✅ Step 2: Backing up VS Code settings..."

VSCODE_SETTINGS="$HOME_DIR/Library/Application Support/Code/User/settings.json"
if [[ -f "$VSCODE_SETTINGS" ]]; then
    BACKUP_FILE="$HOME_DIR/Library/Application Support/Code/User/settings.json.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$VSCODE_SETTINGS" "$BACKUP_FILE"
    echo "   ✅ Backup: $(basename "$BACKUP_FILE")"
else
    echo "   ℹ️  No existing settings found (fresh install)"
fi
echo ""

# Step 3: Create fixed VS Code settings
echo "✅ Step 3: Installing fixed VS Code settings..."

FIXED_JSON="$HOME_DIR/vscode_settings_fixed.json"
if [[ -f "$FIXED_JSON" ]]; then
    cp "$FIXED_JSON" "$VSCODE_SETTINGS"
    echo "   ✅ Installed: $(basename "$VSCODE_SETTINGS")"
else
    echo "   ⚠️  Note: Fixed settings file not found at $FIXED_JSON"
    echo "      You can copy it manually later"
fi
echo ""

# Step 4: Summary
echo "======================================"
echo "✨ Bootstrap Complete!"
echo ""
echo "Next steps:"
echo "1. Close all VS Code windows (CMD+Q)"
echo "2. Wait 3 seconds"
echo "3. Reopen VS Code"
echo "4. Open terminal in VS Code"
echo ""
echo "Verify the fix:"
echo "  • Run: whoami (should show: rsp_ms)"
echo "  • Run: echo \$SHELL (should show: /bin/zsh)"
echo "  • Run: python3 --version (should work)"
echo ""
echo "======================================"
echo ""

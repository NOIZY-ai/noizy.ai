#!/bin/bash
# VS Code Shell Fix for rsp_ms
# This script fixes the broken shell environment issue

# Create a clean zsh configuration
cat > ~/.zshrc_clean << 'ZSHRC_EOF'
# GABRIEL CODEMASTER SHELL - Clean Configuration
export SHELL=/bin/zsh
export TERM=xterm-256color

# Homebrew
if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Python
export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"
export PATH="/usr/bin/python3:$PATH"

# Aliases
alias python='python3'
alias pip='pip3'
alias ll='ls -lah'

# History
HISTSIZE=50000
SAVEHIST=50000
HISTFILE=$HOME/.zsh_history

# Prompt
PROMPT='%B%F{blue}rsp_ms%f:%F{cyan}%~%f%b $ '

echo "✅ GABRIEL Environment Ready | User: $(whoami) | Shell: $SHELL"
ZSHRC_EOF

# Backup existing .zshrc if different
if [[ -f ~/.zshrc ]]; then
    echo "Backing up existing .zshrc..."
    cp ~/.zshrc ~/.zshrc.backup_$(date +%Y%m%d_%H%M%S)
fi

# Use the clean version
echo "Creating clean .zshrc for rsp_ms..."
cp ~/.zshrc_clean ~/.zshrc
chmod 644 ~/.zshrc

echo "✅ Shell configuration fixed!"
echo "Current user: $(whoami)"
echo "Shell: $(which zsh)"
echo ""
echo "Next steps:"
echo "1. Close all VS Code terminal windows"
echo "2. Restart VS Code"
echo "3. Open a new terminal"

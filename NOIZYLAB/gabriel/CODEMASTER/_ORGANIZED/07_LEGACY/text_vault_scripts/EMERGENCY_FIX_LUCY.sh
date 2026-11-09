#!/bin/bash
# EMERGENCY FIX - Remove rob/lucy.sh Corruption
# Fixes rsp_ms account issues

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║  EMERGENCY FIX - rob/lucy.sh Corruption            ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

BACKUP_DIR="$HOME/CODE_MASTER/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Backup location: $BACKUP_DIR"
echo ""

# PHASE 1: KILL ALL lucy PROCESSES
echo "🔍 PHASE 1: Stopping lucy processes..."
pkill -f lucy 2>/dev/null || true
pkill -f "rob/lucy" 2>/dev/null || true
sleep 2
echo "✓ Stopped lucy processes"
echo ""

# PHASE 2: DISABLE rob/lucy.sh
echo "🔍 PHASE 2: Disabling rob/lucy.sh..."
if [ -f "$HOME/rob/lucy.sh" ]; then
    mv "$HOME/rob/lucy.sh" "$HOME/rob/lucy.sh.DISABLED_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
    echo "✓ Disabled rob/lucy.sh"
elif [ -d "$HOME/rob" ]; then
    if [ -f "$HOME/rob/lucy.sh" ]; then
        mv "$HOME/rob/lucy.sh" "$HOME/rob/lucy.sh.DISABLED_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
        echo "✓ Disabled rob/lucy.sh"
    else
        echo "✓ rob/lucy.sh not found"
    fi
else
    echo "✓ rob directory not found"
fi
echo ""

# PHASE 3: CLEAN .zshrc
echo "🔍 PHASE 3: Cleaning .zshrc..."
if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" "$BACKUP_DIR/.zshrc.backup"
    
    # Remove lucy references
    sed -i.bak '/lucy\.sh/d' "$HOME/.zshrc" 2>/dev/null || true
    sed -i.bak '/rob\/lucy/d' "$HOME/.zshrc" 2>/dev/null || true
    sed -i.bak '/source.*lucy/d' "$HOME/.zshrc" 2>/dev/null || true
    sed -i.bak '/\.\/lucy\.sh/d' "$HOME/.zshrc" 2>/dev/null || true
    
    echo "✓ Cleaned .zshrc"
else
    echo "⚠️  .zshrc not found, creating clean version..."
    cat > "$HOME/.zshrc" << 'EOF'
# GABRIEL CODEMASTER - Clean zsh Configuration
# Fixed: $(date)
# Removed: rob/lucy.sh corruption

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
EOF
    echo "✓ Created clean .zshrc"
fi
echo ""

# PHASE 4: CLEAN OTHER STARTUP FILES
echo "🔍 PHASE 4: Cleaning startup files..."
for file in .zshenv .zprofile .bash_profile .bashrc; do
    if [ -f "$HOME/$file" ]; then
        if grep -q "lucy" "$HOME/$file" 2>/dev/null; then
            cp "$HOME/$file" "$BACKUP_DIR/${file}.backup"
            sed -i.bak '/lucy/d' "$HOME/$file" 2>/dev/null || true
            echo "  ✓ Cleaned $file"
        fi
    fi
done
echo ""

# PHASE 5: REMOVE FROM CRONTAB
echo "🔍 PHASE 5: Checking crontab..."
if crontab -l 2>/dev/null | grep -q "lucy"; then
    crontab -l > "$BACKUP_DIR/crontab.backup"
    crontab -l | grep -v "lucy" | crontab -
    echo "  ✓ Removed lucy from crontab"
else
    echo "  ✓ No lucy in crontab"
fi
echo ""

# PHASE 6: DISABLE .lucy DIRECTORY (if problematic)
echo "🔍 PHASE 6: Checking .lucy directory..."
if [ -d "$HOME/.lucy" ]; then
    echo "  Found .lucy directory"
    echo "  Consider: mv ~/.lucy ~/.lucy.DISABLED if causing issues"
fi
echo ""

# SUMMARY
echo "╔════════════════════════════════════════════════════╗"
echo "║  FIX COMPLETE                                     ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "✅ NEXT STEPS:"
echo "  1. Close ALL terminal windows"
echo "  2. Open a NEW terminal"
echo "  3. Test: whoami (should show: rsp_ms)"
echo "  4. Test: echo \$SHELL (should show: /bin/zsh)"
echo "  5. If issues persist, restore from: $BACKUP_DIR"
echo ""
echo "🔥 rsp_ms corruption fixed! 🚀"


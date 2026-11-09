#!/bin/bash
# COMPLETE LUCY DISABLE - Emergency Fix
# Disables .lucy directory and all lucy-related issues

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║  COMPLETE LUCY DISABLE                             ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

BACKUP_DIR="$HOME/CODE_MASTER/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# DISABLE .lucy DIRECTORY
if [ -d "$HOME/.lucy" ]; then
    echo "🔍 Found .lucy directory - Disabling..."
    mv "$HOME/.lucy" "$HOME/.lucy.DISABLED_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
    echo "✓ .lucy directory disabled"
else
    echo "✓ .lucy directory not found"
fi

# REMOVE FROM ALL STARTUP FILES
echo ""
echo "🔍 Cleaning all startup files..."

for file in .zshrc .zshenv .zprofile .bash_profile .bashrc; do
    if [ -f "$HOME/$file" ]; then
        if grep -q "lucy\|\.lucy" "$HOME/$file" 2>/dev/null; then
            cp "$HOME/$file" "$BACKUP_DIR/${file}.backup"
            sed -i.bak '/lucy/d' "$HOME/$file" 2>/dev/null || true
            sed -i.bak '/\.lucy/d' "$HOME/$file" 2>/dev/null || true
            echo "  ✓ Cleaned $file"
        fi
    fi
done

# KILL ALL LUCY PROCESSES
echo ""
echo "🔍 Stopping all lucy processes..."
pkill -9 -f lucy 2>/dev/null || true
pkill -9 -f "\.lucy" 2>/dev/null || true
sleep 1
echo "✓ Processes stopped"

# REMOVE FROM ENVIRONMENT
echo ""
echo "🔍 Cleaning environment..."
unset LUCY_PATH 2>/dev/null || true
unset LUCY_HOME 2>/dev/null || true
echo "✓ Environment cleaned"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  LUCY COMPLETELY DISABLED                         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "✅ NEXT STEPS:"
echo "  1. Close ALL terminal windows"
echo "  2. Restart your Mac (recommended)"
echo "  3. Open a NEW terminal"
echo "  4. Test: whoami (should show: rsp_ms)"
echo ""
echo "🔥 rsp_ms should now be clean! 🚀"


#!/bin/bash
# GABRIEL macOS Shell Fix - Apply Now
# This script applies the VS Code settings fix and restarts

set -e

echo "🔧 Applying GABRIEL macOS Shell Fix..."
echo ""

# Step 1: Backup current settings
echo "📋 Backing up current settings..."
BACKUP_FILE="$HOME/Library/Application Support/Code/User/settings.json.backup.$(date +%Y%m%d_%H%M%S)"
cp "$HOME/Library/Application Support/Code/User/settings.json" "$BACKUP_FILE"
echo "   ✅ Backup created: $(basename "$BACKUP_FILE")"
echo ""

# Step 2: Copy fixed settings
echo "✨ Installing fixed VS Code settings..."
cp /Users/rsp_ms/vscode_settings_fixed.json \
   "$HOME/Library/Application Support/Code/User/settings.json"
echo "   ✅ Settings updated"
echo ""

# Step 3: Close VS Code
echo "🛑 Closing VS Code..."
killall "Visual Studio Code" 2>/dev/null || echo "   (VS Code not running)"
echo "   ✅ Closed"
echo ""

# Step 4: Wait
echo "⏳ Waiting 3 seconds..."
sleep 3
echo "   ✅ Ready"
echo ""

# Step 5: Reopen VS Code
echo "🚀 Launching VS Code..."
open /Applications/Visual\ Studio\ Code.app
echo "   ✅ Launched"
echo ""

echo "════════════════════════════════════════"
echo "✅ FIX APPLIED!"
echo "════════════════════════════════════════"
echo ""
echo "VS Code is opening now. Once it loads:"
echo ""
echo "1. Open a terminal (CTRL+`)"
echo "2. Run these commands:"
echo "   • whoami          (should show: rsp_ms)"
echo "   • echo \$SHELL    (should show: /bin/zsh)"
echo "   • python3 -v     (should work)"
echo ""
echo "All working = SUCCESS! 🎉"
echo ""

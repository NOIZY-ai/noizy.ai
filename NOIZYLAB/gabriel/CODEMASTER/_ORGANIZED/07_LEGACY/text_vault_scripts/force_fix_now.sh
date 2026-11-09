#!/bin/bash
# GABRIEL macOS Shell Fix - Force Apply
# Directly updates VS Code settings with proper terminal profiles

echo "🔧 Force-applying GABRIEL macOS Shell Fix..."
echo ""

SETTINGS_PATH="$HOME/Library/Application Support/Code/User/settings.json"

# Step 1: Backup
echo "📋 Backing up current settings..."
BACKUP_FILE="${SETTINGS_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$SETTINGS_PATH" "$BACKUP_FILE"
echo "   ✅ Backup: $BACKUP_FILE"
echo ""

# Step 2: Copy corrected settings
echo "✨ Copying corrected settings..."
cp /Users/rsp_ms/vscode_settings_fixed.json "$SETTINGS_PATH"
echo "   ✅ Settings file updated"
echo ""

# Step 3: Verify the fix was applied
echo "🔍 Verifying fix..."
if grep -q '"terminal.integrated.profiles.osx"' "$SETTINGS_PATH"; then
  echo "   ✅ Terminal profiles found"
fi
if grep -q '"/bin/zsh"' "$SETTINGS_PATH"; then
  echo "   ✅ Correct shell path (/bin/zsh) found"
fi
echo ""

# Step 4: Close all VS Code instances
echo "🛑 Closing all VS Code instances..."
killall "Visual Studio Code" 2>/dev/null || true
killall "code" 2>/dev/null || true
sleep 2
echo "   ✅ Closed"
echo ""

# Step 5: Reopen
echo "🚀 Launching VS Code..."
open /Applications/Visual\ Studio\ Code.app &
sleep 2

echo "════════════════════════════════════════"
echo "✅ FIX FORCE-APPLIED!"
echo "════════════════════════════════════════"
echo ""
echo "VS Code is opening. Once ready:"
echo ""
echo "1. Open a NEW terminal in VS Code (Ctrl+`)"
echo "2. These commands should now work:"
echo ""
echo "   whoami              # Should show: rsp_ms"
echo "   echo \$SHELL         # Should show: /bin/zsh"
echo "   python3 -v          # Should show Python version"
echo ""
echo "If the terminal still shows shell errors, try:"
echo "   • Quit VS Code completely (Cmd+Q)"
echo "   • Open it again"
echo ""

#!/bin/bash
# install-god-autostart.sh
# Installs the LaunchAgent and Helper Aliases for Voice Forge

APP_DIR="$HOME/voice-forge-local"
SCRIPTS_DIR="$APP_DIR/scripts"
PLIST_NAME="com.fishmusicinc.voiceforge.plist"
PLIST_SOURCE="$SCRIPTS_DIR/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "=== Installing Voice Forge Auto-Start on GOD ==="

# 1. Setup Permissions
chmod +x "$SCRIPTS_DIR"/*.sh

# 2. Install LaunchAgent
echo "[INSTALL] copying plist to LaunchAgents..."
cp "$PLIST_SOURCE" "$PLIST_DEST"

# 3. Load Agent
echo "[INSTALL] Loading LaunchAgent..."
launchctl unload "$PLIST_DEST" 2>/dev/null
launchctl load "$PLIST_DEST"

# 4. Add Aliases to Zshrc
echo "[INSTALL] Adding aliases to ~/.zshrc..."
# Check if alias already exists to avoid duplication
if ! grep -q "alias vf=" "$HOME/.zshrc"; then
    echo "" >> "$HOME/.zshrc"
    echo "# Voice Forge Aliases" >> "$HOME/.zshrc"
    echo "alias vf='$SCRIPTS_DIR/voice-forge-god.sh'" >> "$HOME/.zshrc"
    echo "alias vf-stop='docker-compose -f $APP_DIR/docker-compose.yml down'" >> "$HOME/.zshrc"
    echo "alias vf-status='$SCRIPTS_DIR/mc96-voice-status.sh'" >> "$HOME/.zshrc"
    echo "alias vf-logs='tail -f $APP_DIR/voice-forge.log'" >> "$HOME/.zshrc"
    echo "Aliases installed: vf, vf-stop, vf-status, vf-logs"
else
    echo "Aliases already exist."
fi

echo "=== Installation Complete ==="
echo "Voice Forge will now start on login."

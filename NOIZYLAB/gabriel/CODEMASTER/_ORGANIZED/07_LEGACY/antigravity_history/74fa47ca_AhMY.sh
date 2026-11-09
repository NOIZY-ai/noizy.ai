#!/bin/bash
# HAMMERSPOON SPOTIFY CONTROLLER - GOD MODE SETUP
# Optimized for Zero Latency & Robustness

set -e

echo "🚀 Starting God Mode Setup for Spotify Volume Control..."

# 1. Check/Install Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install Homebrew first."
    exit 1
fi

# 2. Install Hammerspoon
if [ ! -d "/Applications/Hammerspoon.app" ]; then
    echo "📦 Installing Hammerspoon..."
    brew install --cask hammerspoon
else
    echo "✅ Hammerspoon already installed."
fi

# 3. Create Config Directory
mkdir -p ~/.hammerspoon

# 4. Backup Existing Config
if [ -f ~/.hammerspoon/init.lua ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    echo "⚠️  Backing up existing init.lua to init.lua.backup_$TIMESTAMP"
    cp ~/.hammerspoon/init.lua ~/.hammerspoon/init.lua.backup_$TIMESTAMP
fi

# 5. Write Optimized Config
echo "⚡ Writing Zero-Latency Config..."
cat > ~/.hammerspoon/init.lua << 'EOF'
-- Spotify Volume Control (Zero Latency)
-- F11 = Volume Down | F12 = Volume Up

local function showVol()
    -- Get volume delay-check to ensure Spotify updated internally
    hs.timer.doAfter(0.1, function()
        local vol = hs.spotify.getVolume()
        if vol then
            hs.alert.show(string.format("🎵 Volume: %d%%", vol), 0.5)
        end
    end)
end

hs.hotkey.bind({}, "F11", function()
    hs.spotify.volumeDown()
    showVol()
end)

hs.hotkey.bind({}, "F12", function()
    hs.spotify.volumeUp()
    showVol()
end)

hs.alert.show("🚀 Spotify Volume Control Loaded")
EOF

# 6. Launch/Reload Hammerspoon
if pgrep "Hammerspoon" > /dev/null; then
    echo "🔄 Reloading Hammerspoon Config..."
    # Try using AppleScript to reload config gracefully
    osascript -e 'tell application "Hammerspoon" to execute lua code "hs.reload()"' || echo "⚠️  Manual reload might be needed."
else
    echo "🚀 Starting Hammerspoon..."
    open -a Hammerspoon
fi

echo "✅ Setup Complete! F11/F12 are now live."

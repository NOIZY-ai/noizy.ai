#!/bin/bash
# ============================================
# COMPLETE macOS SEQUOIA FACTORY RESET
# GOD - Mac Studio M2 Ultra
# GORUNFREE - ONE COMMAND FIXES EVERYTHING
# ============================================

echo "=========================================="
echo "FULL SYSTEM RESET - APPLE DEFAULTS"
echo "=========================================="

# Stop all user apps
killall "System Settings" 2>/dev/null
killall "System Preferences" 2>/dev/null

echo "Resetting ALL preferences to Apple defaults..."

# ============================================
# NUKE ALL USER PREFERENCES
# ============================================

# Global settings
defaults delete -g 2>/dev/null

# Dock
defaults delete com.apple.dock 2>/dev/null

# Finder  
defaults delete com.apple.finder 2>/dev/null

# Menu bar / Control Center
defaults delete com.apple.controlcenter 2>/dev/null
defaults delete com.apple.systemuiserver 2>/dev/null

# Keyboard
defaults delete com.apple.keyboard 2>/dev/null
defaults delete com.apple.HIToolbox 2>/dev/null
defaults delete com.apple.keyboardservicesd 2>/dev/null

# Mouse / Trackpad
defaults delete com.apple.AppleMultitouchMouse 2>/dev/null
defaults delete com.apple.AppleMultitouchTrackpad 2>/dev/null
defaults delete com.apple.driver.AppleBluetoothMultitouch.mouse 2>/dev/null
defaults delete com.apple.driver.AppleBluetoothMultitouch.trackpad 2>/dev/null
defaults delete com.apple.mouse 2>/dev/null

# Sound
defaults delete com.apple.sound.beep 2>/dev/null
defaults delete com.apple.systemsound 2>/dev/null
defaults delete com.apple.audio.AudioMIDISetup 2>/dev/null
defaults delete com.apple.coreaudio 2>/dev/null

# Display
defaults delete com.apple.windowserver 2>/dev/null
defaults delete com.apple.displays 2>/dev/null

# Accessibility
defaults delete com.apple.Accessibility 2>/dev/null
defaults delete com.apple.universalaccess 2>/dev/null
defaults delete com.apple.accessibility.heard 2>/dev/null
defaults delete com.apple.VoiceOverUtility 2>/dev/null

# Network
defaults delete com.apple.networkConnect 2>/dev/null
defaults delete com.apple.wifi.proxy 2>/dev/null
defaults delete com.apple.Bluetooth 2>/dev/null

# Spotlight
defaults delete com.apple.Spotlight 2>/dev/null

# Siri
defaults delete com.apple.Siri 2>/dev/null
defaults delete com.apple.assistant.support 2>/dev/null

# Safari
defaults delete com.apple.Safari 2>/dev/null

# Mail
defaults delete com.apple.mail 2>/dev/null

# Messages
defaults delete com.apple.MobileSMS 2>/dev/null

# Calendar
defaults delete com.apple.iCal 2>/dev/null

# Notes
defaults delete com.apple.Notes 2>/dev/null

# Photos
defaults delete com.apple.Photos 2>/dev/null

# Music
defaults delete com.apple.Music 2>/dev/null

# Terminal
defaults delete com.apple.Terminal 2>/dev/null

# Screen Saver
defaults delete com.apple.screensaver 2>/dev/null

# Desktop
defaults delete com.apple.desktop 2>/dev/null

# Login Items
defaults delete com.apple.loginitems 2>/dev/null

# Notifications
defaults delete com.apple.ncprefs 2>/dev/null

# Energy / Battery
defaults delete com.apple.PowerManagement 2>/dev/null

# Security
defaults delete com.apple.security 2>/dev/null

# Time Machine
defaults delete com.apple.TimeMachine 2>/dev/null

# Sharing
defaults delete com.apple.preferences.sharing 2>/dev/null

# ============================================
# CLEAR CACHES
# ============================================

echo "Clearing preference caches..."

rm -rf ~/Library/Preferences/ByHost/* 2>/dev/null
rm -rf ~/Library/Caches/com.apple.* 2>/dev/null
rm -rf ~/Library/Saved\ Application\ State/com.apple.* 2>/dev/null

# ============================================
# RESTART SERVICES
# ============================================

echo "Restarting system services..."

killall Dock 2>/dev/null
killall Finder 2>/dev/null
killall SystemUIServer 2>/dev/null
killall ControlCenter 2>/dev/null
killall cfprefsd 2>/dev/null

echo ""
echo "=========================================="
echo "✅ RESET COMPLETE"
echo "=========================================="
echo ""
echo "RESTART NOW - paste this:"
echo ""
echo "sudo shutdown -r now"
echo ""
echo "=========================================="

#!/bin/bash
"""
🔊 GABRIEL - System Sound Configuration
Changes the Enter/Return key sound from negative beep to simple click
"""

echo "🔊 GABRIEL System Sound Configuration"
echo "======================================"
echo ""

# Disable the error/negative sound for common actions
echo "Disabling negative error sounds..."

# Turn off the system beep/alert sound
defaults write NSGlobalDomain com.apple.sound.beep.volume -float 0.0

# Disable the "bonk" sound when invalid key is pressed
defaults write NSGlobalDomain com.apple.sound.uiaudio.enabled -int 0

# Set alert sound to a simple click
defaults write NSGlobalDomain com.apple.sound.beep.sound -string "/System/Library/Sounds/Tink.aiff"

# Alternative: Use Morse for an even softer click
# defaults write NSGlobalDomain com.apple.sound.beep.sound -string "/System/Library/Sounds/Morse.aiff"

# Reduce system alert volume
defaults write NSGlobalDomain com.apple.sound.beep.volume -float 0.1

# Disable feedback when volume is changed
defaults write NSGlobalDomain com.apple.sound.beep.feedback -int 0

# Apply changes
killall SystemUIServer 2>/dev/null

echo ""
echo "✅ Sound settings updated!"
echo ""
echo "Changes made:"
echo "  • System beep volume: Set to minimal (0.1)"
echo "  • Alert sound: Changed to 'Tink' (simple click)"
echo "  • UI audio feedback: Disabled"
echo "  • Volume feedback: Disabled"
echo ""
echo "To revert these changes, run:"
echo "  defaults delete NSGlobalDomain com.apple.sound.beep.volume"
echo "  defaults delete NSGlobalDomain com.apple.sound.uiaudio.enabled"
echo "  defaults delete NSGlobalDomain com.apple.sound.beep.sound"
echo ""
echo "Available soft click sounds (pick one):"
echo "  • Tink (current) - High pitched click"
echo "  • Morse - Soft beep"
echo "  • Pop - Bubble pop"
echo "  • Purr - Gentle vibration"
echo ""
echo "To change to another sound, use:"
echo "  defaults write NSGlobalDomain com.apple.sound.beep.sound -string '/System/Library/Sounds/[Name].aiff'"
echo ""

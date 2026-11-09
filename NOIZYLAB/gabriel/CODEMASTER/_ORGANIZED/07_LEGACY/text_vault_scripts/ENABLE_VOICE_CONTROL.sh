#!/bin/bash
# ENABLE_VOICE_CONTROL.sh
# Opens Accessibility settings to enable Voice Control

echo "🎤 Enabling Voice Control..."
echo ""

# Open Accessibility settings
open "x-apple.systempreferences:com.apple.preference.universalaccess"

echo "📋 INSTRUCTIONS:"
echo ""
echo "1. Accessibility settings opened"
echo "2. Find 'Voice Control' in the list"
echo "3. Click to enable it"
echo ""
echo "OR use voice:"
echo "   Say: 'Hey Siri, enable Voice Control'"
echo ""

say "Accessibility settings opened. Enable Voice Control to use voice commands for everything."


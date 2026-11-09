#!/bin/bash
# ENABLE_ACCESSIBILITY_PERMISSIONS.sh
# Grants necessary permissions for automation

echo "🔐 Enabling Accessibility Permissions..."
echo ""
echo "This will open System Preferences so you can grant permissions."
echo ""

# Open Accessibility settings
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"

echo "📋 Please grant access to:"
echo "   • Terminal"
echo "   • Script Editor"
echo "   • System Events (if needed)"
echo ""
echo "Then enable Voice Control:"
echo "   Accessibility → Voice Control → Enable"
echo ""
echo "Press Enter when done..."
read

echo "✅ Permissions configured!"
echo ""



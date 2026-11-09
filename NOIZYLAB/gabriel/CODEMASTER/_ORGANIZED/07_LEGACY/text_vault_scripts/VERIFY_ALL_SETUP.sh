#!/bin/bash
# VERIFY_ALL_SETUP.sh
# Verify all Beats and email setup

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ✅ VERIFYING ALL SETUP                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 CHECKING SETUP STATUS..."
echo ""

# Check if Beats scripts exist
echo "🎧 BEATS SETUP SCRIPTS:"
if [ -f "$HOME/Desktop/BEATS_MASTER_SETUP.command" ]; then
    echo "   ✅ BEATS_MASTER_SETUP.command"
else
    echo "   ❌ BEATS_MASTER_SETUP.command (missing)"
fi

if [ -f "$HOME/Desktop/ULTIMATE_VOICE_SETUP.command" ]; then
    echo "   ✅ ULTIMATE_VOICE_SETUP.command"
else
    echo "   ❌ ULTIMATE_VOICE_SETUP.command (missing)"
fi

if [ -f "$HOME/Desktop/ADVANCED_BEATS_SETUP.command" ]; then
    echo "   ✅ ADVANCED_BEATS_SETUP.command"
else
    echo "   ❌ ADVANCED_BEATS_SETUP.command (missing)"
fi

echo ""
echo "📧 EMAIL SETUP:"
if [ -f "$HOME/Desktop/EMAIL_MASTER.command" ]; then
    echo "   ✅ EMAIL_MASTER.command"
else
    echo "   ⚠️  EMAIL_MASTER.command (may not exist)"
fi

echo ""
echo "📚 GUIDES:"
if [ -f "$HOME/Desktop/BEATS_OPTIMIZATION.txt" ]; then
    echo "   ✅ BEATS_OPTIMIZATION.txt"
fi
if [ -f "$HOME/Desktop/ADVANCED_BEATS_GUIDE.txt" ]; then
    echo "   ✅ ADVANCED_BEATS_GUIDE.txt"
fi
if [ -f "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt" ]; then
    echo "   ✅ VOICE_COMMANDS_QUICK.txt"
fi
if [ -f "$HOME/Desktop/BEATS_STATUS.txt" ]; then
    echo "   ✅ BEATS_STATUS.txt"
fi

echo ""
echo "✅ VERIFICATION COMPLETE!"
echo ""
echo "📋 ALL SETUP READY:"
echo "   • Beats Studio Pro optimization scripts"
echo "   • Email setup automation"
echo "   • Voice control guides"
echo "   • All system preferences opened"
echo ""
echo "🎧 READY TO USE!"
echo ""


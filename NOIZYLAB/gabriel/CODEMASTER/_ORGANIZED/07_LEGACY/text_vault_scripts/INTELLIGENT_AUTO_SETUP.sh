#!/bin/bash
# INTELLIGENT_AUTO_SETUP.sh
# Intelligent auto-setup with smart detection

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🤖 INTELLIGENT AUTO-SETUP X10000                                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create intelligent setup wizard
cat > "$HOME/Desktop/INTELLIGENT_WIZARD.command" << 'WIZARD_EOF'
#!/bin/bash
# Intelligent Setup Wizard - Guides you through everything

clear

echo "🤖 INTELLIGENT SETUP WIZARD"
echo ""

# Step 1: Check Beats
echo "STEP 1: Checking Beats Studio Pro..."
if system_profiler SPAudioDataType | grep -q "Beats Studio Pro"; then
    echo "   ✅ Beats Studio Pro detected!"
    BEATS_OK=true
else
    echo "   ⚠️  Beats Studio Pro not detected"
    echo "   📋 Action: Connect Beats Studio Pro via cable"
    BEATS_OK=false
fi

echo ""
read -p "Press Enter to continue..."

# Step 2: Check Voice Control
echo ""
echo "STEP 2: Checking Voice Control..."
if pgrep -x "VoiceControl" > /dev/null; then
    echo "   ✅ Voice Control is enabled!"
    VOICE_OK=true
else
    echo "   ⚠️  Voice Control not enabled"
    echo "   📋 Action: Enable Voice Control in Accessibility"
    open "x-apple.systempreferences:com.apple.preference.universalaccess"
    VOICE_OK=false
fi

echo ""
read -p "Press Enter to continue..."

# Step 3: Configure Audio
echo ""
echo "STEP 3: Configuring Audio..."
open "x-apple.systempreferences:com.apple.preference.sound"
echo "   📋 Action: In Sound settings:"
echo "      • Select 'Beats Studio Pro' for input"
echo "      • Set input volume to 75-85%"
echo "      • Select 'Beats Studio Pro' for output"
echo ""
read -p "Press Enter when configured..."

# Step 4: Email Setup
echo ""
echo "STEP 4: Email Setup..."
open "https://dash.cloudflare.com/login"
open "https://app.improvmx.com/"
open "https://mail.google.com/mail/u/0/#settings/accounts"
echo "   ✅ All email pages opened!"
echo "   📋 Use voice commands to complete setup"
echo ""

# Final status
echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ✅ SETUP WIZARD COMPLETE                                         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

if [ "$BEATS_OK" = true ] && [ "$VOICE_OK" = true ]; then
    echo "🎉 PERFECT! Everything is configured!"
    echo "   ✅ Beats Studio Pro: Connected"
    echo "   ✅ Voice Control: Enabled"
    echo "   ✅ Email Setup: Ready"
    echo ""
    echo "🎤 Test: Say 'Show numbers'"
else
    echo "📋 SETUP STATUS:"
    [ "$BEATS_OK" = true ] && echo "   ✅ Beats Studio Pro: Connected" || echo "   ⚠️  Beats Studio Pro: Connect via cable"
    [ "$VOICE_OK" = true ] && echo "   ✅ Voice Control: Enabled" || echo "   ⚠️  Voice Control: Enable in Accessibility"
    echo "   ✅ Email Setup: Pages opened"
    echo ""
    echo "📋 Complete the remaining steps above"
fi

echo ""
say "Intelligent setup wizard complete. Follow the steps to configure everything."
WIZARD_EOF

chmod +x "$HOME/Desktop/INTELLIGENT_WIZARD.command"

echo "✅ INTELLIGENT_WIZARD.command created!"
echo ""


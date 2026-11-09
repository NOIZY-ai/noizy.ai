#!/bin/bash
# ULTIMATE_BEATS_EMAIL_INTEGRATION.sh
# Complete integration: Beats Studio Pro + Email Setup

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎧⚡ ULTIMATE BEATS + EMAIL INTEGRATION                         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create ultimate integration script
cat > "$HOME/Desktop/ULTIMATE_VOICE_SETUP.command" << 'ULTIMATE_EOF'
#!/bin/bash
# Ultimate Voice Setup - Beats + Email

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎧⚡ ULTIMATE VOICE SETUP                                        ║"
echo "║     Beats Studio Pro + Email Configuration                           ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 COMPLETE SETUP PROCESS:"
echo ""

echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 1: CONNECT BEATS STUDIO PRO"
echo "══════════════════════════════════════════════════════════════════════"
echo ""
echo "  • Connect via USB-C cable (best)"
echo "  • OR connect via 3.5mm cable"
echo "  • Make sure cable is fully inserted"
echo ""
read -p "Press Enter when Beats Studio Pro is connected..."

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 2: CONFIGURE AUDIO SETTINGS"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

open "x-apple.systempreferences:com.apple.preference.sound"
sleep 2

echo "✅ Sound settings opened!"
echo ""
echo "CONFIGURE:"
echo "  • Input tab: Select 'Beats Studio Pro'"
echo "  • Input Volume: 75-85% (optimal)"
echo "  • Output tab: Select 'Beats Studio Pro'"
echo "  • Output Volume: Comfortable level"
echo ""
read -p "Press Enter when audio is configured..."

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 3: ENABLE VOICE CONTROL"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

open "x-apple.systempreferences:com.apple.preference.universalaccess"
sleep 2

echo "✅ Accessibility settings opened!"
echo ""
echo "ENABLE:"
echo "  • Find 'Voice Control'"
echo "  • Click to enable"
echo "  • It will use Beats Studio Pro mic automatically"
echo ""
read -p "Press Enter when Voice Control is enabled..."

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 4: TEST VOICE CONTROL"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

echo "TEST:"
echo "  Say: 'Show numbers'"
echo "  If numbers appear → Voice Control working! ✅"
echo ""
read -p "Press Enter after testing Voice Control..."

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 5: EMAIL SETUP (Voice-Controlled)"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

echo "Opening email setup pages..."
echo ""

# Open Cloudflare
open "https://dash.cloudflare.com/login"
sleep 1

# Open ImprovMX
open "https://app.improvmx.com/"
sleep 1

# Open Gmail
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 1

echo ""
echo "✅ All email setup pages opened!"
echo ""
echo "📋 VOICE COMMANDS FOR EMAIL SETUP:"
echo ""
echo "  Say: 'Show numbers' - See clickable numbers"
echo "  Say: 'Click [number]' - Click on numbered item"
echo "  Say: 'Go to [page name]' - Navigate"
echo "  Say: 'Type [text]' - Type text"
echo "  Say: 'Press return' - Press Enter"
echo ""
echo "📋 EMAIL SETUP STEPS (Voice-Controlled):"
echo ""
echo "1. Cloudflare (DNS):"
echo "   • Add MX records for ImprovMX"
echo "   • Add SPF record"
echo ""
echo "2. ImprovMX:"
echo "   • Add domain: fishmusicinc.com"
echo "   • Create aliases: rp@, rsp@, help@"
echo "   • Forward to: rsplowman@gmail.com"
echo ""
echo "3. Gmail:"
echo "   • Settings → Accounts → Send mail as"
echo "   • Add: rp@fishmusicinc.com"
echo "   • Add: rsp@noizylab.ca"
echo "   • Add: help@noizylab.ca"
echo ""

say "Ultimate voice setup complete. Beats Studio Pro is configured. Voice Control is enabled. All email setup pages are open. Use voice commands to complete the email setup."

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ✅ ULTIMATE VOICE SETUP COMPLETE!                               ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎤 READY FOR VOICE CONTROL!"
echo "📧 EMAIL SETUP PAGES OPEN!"
echo ""
echo "Say 'Show numbers' to start!"
echo ""
ULTIMATE_EOF

chmod +x "$HOME/Desktop/ULTIMATE_VOICE_SETUP.command"

# Create quick reference card
cat > "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt" << 'QUICK_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎤 VOICE COMMANDS - QUICK REFERENCE                              ║
╚══════════════════════════════════════════════════════════════════════╝

BASIC COMMANDS:
───────────────

"Show numbers"          - Show clickable numbers on screen
"Hide numbers"          - Hide numbers
"Click [number]"        - Click on numbered item
"Double click [number]" - Double-click
"Right click [number]"  - Right-click

NAVIGATION:
───────────

"Go to [page name]"     - Navigate to page
"Scroll down"           - Scroll down
"Scroll up"             - Scroll up
"Go back"               - Browser back
"Go forward"            - Browser forward

TYPING:
───────

"Type [text]"           - Type text
"Press return"          - Press Enter
"Press tab"             - Press Tab
"Press space"           - Press Space
"Delete"                - Delete character
"Select all"            - Select all text

EMAIL SETUP:
───────────

"Show numbers"          - Start (see clickable items)
"Click [number]"        - Click buttons/links
"Type [email]"          - Type email addresses
"Press return"          - Submit forms

══════════════════════════════════════════════════════════════════════

QUICK_EOF

echo "✅ Ultimate integration complete!"
echo ""
echo "📋 NEW SHORTCUT:"
echo "   ✅ ULTIMATE_VOICE_SETUP.command - Complete Beats + Email setup"
echo ""
echo "🚀 ONE-COMMAND SETUP:"
echo "   1. Connect Beats Studio Pro via cable"
echo "   2. Double-click: ULTIMATE_VOICE_SETUP.command"
echo "   3. Follow all steps"
echo "   4. Complete email setup with voice commands!"
echo ""

say "Ultimate Beats and email integration complete. Connect your headphones and run Ultimate Voice Setup for complete voice-controlled configuration."


#!/bin/bash
# AUTO_EXECUTE_ALL_BEATS.sh
# Automatically execute all Beats setup scripts

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎧⚡ AUTO-EXECUTING ALL BEATS SETUP                             ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 EXECUTING ALL SETUP SCRIPTS..."
echo ""

# Open all system preferences
echo "1. Opening Sound settings..."
open "x-apple.systempreferences:com.apple.preference.sound"
sleep 2

echo "2. Opening Accessibility settings..."
open "x-apple.systempreferences:com.apple.preference.universalaccess"
sleep 2

echo "3. Opening Audio MIDI Setup..."
open -a "Audio MIDI Setup" 2>/dev/null || echo "   (Audio MIDI Setup not available)"
sleep 1

# Open all email setup pages
echo "4. Opening Cloudflare..."
open "https://dash.cloudflare.com/login"
sleep 1

echo "5. Opening ImprovMX..."
open "https://app.improvmx.com/"
sleep 1

echo "6. Opening Gmail settings..."
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 1

# Open all guides
echo "7. Opening guides..."
if [ -f "$HOME/Desktop/BEATS_OPTIMIZATION.txt" ]; then
    open "$HOME/Desktop/BEATS_OPTIMIZATION.txt"
fi
sleep 1

if [ -f "$HOME/Desktop/ADVANCED_BEATS_GUIDE.txt" ]; then
    open "$HOME/Desktop/ADVANCED_BEATS_GUIDE.txt"
fi
sleep 1

if [ -f "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt" ]; then
    open "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt"
fi
sleep 1

# Create status check
cat > "$HOME/Desktop/BEATS_STATUS.txt" << 'STATUS_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎧 BEATS STUDIO PRO - SETUP STATUS                               ║
╚══════════════════════════════════════════════════════════════════════╝

✅ ALL SETTINGS OPENED:
   • Sound settings - Configure Beats Studio Pro
   • Accessibility settings - Enable Voice Control
   • Audio MIDI Setup - Advanced settings
   • Cloudflare - DNS configuration
   • ImprovMX - Email forwarding
   • Gmail - Email aliases

📋 NEXT STEPS:
   1. Connect Beats Studio Pro via USB-C or 3.5mm cable
   2. In Sound settings:
      • Input tab: Select "Beats Studio Pro"
      • Input Volume: 75-85%
      • Output tab: Select "Beats Studio Pro"
   3. In Accessibility settings:
      • Enable "Voice Control"
   4. Test: Say "Show numbers"
   5. Complete email setup using voice commands

🎤 VOICE COMMANDS READY:
   • "Show numbers" - See clickable items
   • "Click [number]" - Click items
   • "Type [text]" - Type text
   • "Press return" - Submit

══════════════════════════════════════════════════════════════════════

STATUS_EOF

open "$HOME/Desktop/BEATS_STATUS.txt"

echo ""
echo "✅ ALL SETUP SCRIPTS EXECUTED!"
echo ""
echo "📋 STATUS:"
echo "   ✅ Sound settings opened"
echo "   ✅ Accessibility settings opened"
echo "   ✅ Email setup pages opened"
echo "   ✅ All guides opened"
echo ""
echo "🎧 NEXT:"
echo "   1. Connect Beats Studio Pro via cable"
echo "   2. Configure in Sound settings (already open)"
echo "   3. Enable Voice Control (already open)"
echo "   4. Test: Say 'Show numbers'"
echo ""

say "All Beats Studio Pro setup scripts executed. Connect your headphones via cable. Configure in Sound settings. Enable Voice Control. Then say Show numbers to test."


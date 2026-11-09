#!/bin/bash
# SETUP_EXTERNAL_MIC.sh
# Setup Voice Control with iPhone or Beats Studio Pro microphone

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎤 SETUP EXTERNAL MICROPHONE                                    ║"
echo "║     iPhone or Beats Studio Pro                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create guide for external mic setup
cat > "$HOME/Desktop/EXTERNAL_MIC_SETUP.txt" << 'MIC_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎤 EXTERNAL MICROPHONE SETUP                                     ║
║     iPhone or Beats Studio Pro                                        ║
╚══════════════════════════════════════════════════════════════════════╝

YOU HAVE:
──────────

• iPhone microphone (via Continuity)
• Beats Studio Pro headphones (built-in mic)

Both can work with Voice Control on your Mac!

══════════════════════════════════════════════════════════════════════
OPTION 1: USE IPHONE MICROPHONE
══════════════════════════════════════════════════════════════════════

SETUP:
──────

1. Make sure iPhone and Mac are on same Wi-Fi
2. Make sure both are signed into same Apple ID
3. On iPhone: Settings → General → AirPlay & Handoff
   → Enable "Continuity Camera" and "Handoff"

4. On Mac: System Preferences → Sound → Input
   → Select "iPhone Microphone" (if available)

5. Enable Voice Control:
   • System Preferences → Accessibility → Voice Control
   • Click "Enable"
   • Microphone will use iPhone automatically if connected

USE:
────

• Just speak into your iPhone
• Voice Control on Mac will hear you
• Works wirelessly!

══════════════════════════════════════════════════════════════════════
OPTION 2: USE BEATS STUDIO PRO HEADPHONES
══════════════════════════════════════════════════════════════════════

SETUP:
──────

1. Connect Beats Studio Pro to Mac:
   • Bluetooth: Pair in System Preferences → Bluetooth
   • Wired: Plug in USB-C or 3.5mm cable

2. Set as input device:
   • System Preferences → Sound → Input
   • Select "Beats Studio Pro" from list

3. Enable Voice Control:
   • System Preferences → Accessibility → Voice Control
   • Click "Enable"
   • It will use Beats mic automatically

USE:
────

• Put on your Beats Studio Pro headphones
• Speak normally
• Voice Control will hear you through the mic

══════════════════════════════════════════════════════════════════════
QUICK SETUP STEPS
══════════════════════════════════════════════════════════════════════

FOR IPHONE MIC:
───────────────

1. Say: "Hey Siri, open Sound settings"
   OR
   System Preferences → Sound → Input

2. Look for "iPhone Microphone" in the list
3. Select it
4. Test by speaking (you should see the level meter move)

FOR BEATS STUDIO PRO:
──────────────────────

1. Connect headphones (Bluetooth or wired)
2. Say: "Hey Siri, open Sound settings"
   OR
   System Preferences → Sound → Input

3. Select "Beats Studio Pro" from list
4. Test by speaking (you should see the level meter move)

THEN ENABLE VOICE CONTROL:
──────────────────────────

1. Say: "Hey Siri, open Accessibility settings"
   OR
   System Preferences → Accessibility

2. Find "Voice Control"
3. Click "Enable"
4. It will use your selected microphone automatically

══════════════════════════════════════════════════════════════════════
TESTING YOUR MIC
══════════════════════════════════════════════════════════════════════

After setting up:

1. Enable Voice Control
2. Say: "Show numbers"
3. If numbers appear on screen → Mic is working! ✅
4. If nothing happens → Check mic selection

TROUBLESHOOTING:
────────────────

If iPhone mic doesn't appear:
  • Make sure both devices on same Wi-Fi
  • Make sure both signed into same Apple ID
  • Try restarting both devices

If Beats mic doesn't work:
  • Check Bluetooth connection
  • Try wired connection instead
  • Check battery level
  • Make sure mic is enabled on headphones

══════════════════════════════════════════════════════════════════════
VOICE COMMANDS (Once Set Up)
══════════════════════════════════════════════════════════════════════

Once Voice Control is enabled with your mic:

"Show numbers" - Shows numbers on clickable items
"Click [number]" - Clicks numbered item
"Click [button name]" - Clicks button
"Type [text]" - Types text
"Scroll down" - Scrolls page
"Go back" - Browser back

══════════════════════════════════════════════════════════════════════

MIC_EOF

# Create quick setup script
cat > "$HOME/Desktop/SETUP_MIC.command" << 'SETUP_MIC_EOF'
#!/bin/bash
# Quick mic setup

clear

echo "🎤 SETTING UP EXTERNAL MICROPHONE..."
echo ""

echo "Opening Sound settings..."
open "x-apple.systempreferences:com.apple.preference.sound"

sleep 2

echo ""
echo "📋 INSTRUCTIONS:"
echo ""
echo "1. Sound settings opened"
echo "2. Click 'Input' tab"
echo "3. Select your microphone:"
echo "   • iPhone Microphone (if using iPhone)"
echo "   • Beats Studio Pro (if using headphones)"
echo "4. Test by speaking (see level meter)"
echo ""
echo "Then enable Voice Control:"
echo "   System Preferences → Accessibility → Voice Control → Enable"
echo ""

say "Sound settings opened. Select your microphone from the input list. Then enable Voice Control in Accessibility settings."
SETUP_MIC_EOF

chmod +x "$HOME/Desktop/SETUP_MIC.command"

# Create Voice Control enabler
cat > "$HOME/Desktop/ENABLE_VOICE_CONTROL.command" << 'ENABLE_EOF'
#!/bin/bash
# Enable Voice Control

clear

echo "🎤 ENABLING VOICE CONTROL..."
echo ""

open "x-apple.systempreferences:com.apple.preference.universalaccess"

echo "📋 INSTRUCTIONS:"
echo ""
echo "1. Accessibility settings opened"
echo "2. Find 'Voice Control' in the list"
echo "3. Click to enable it"
echo ""
echo "Voice Control will use your selected microphone automatically!"
echo ""

say "Accessibility settings opened. Find Voice Control and enable it. It will use your selected microphone."
ENABLE_EOF

chmod +x "$HOME/Desktop/ENABLE_VOICE_CONTROL.command"

# Open the guide
open "$HOME/Desktop/EXTERNAL_MIC_SETUP.txt"

echo "✅ External mic setup guide created!"
echo ""
echo "📋 GUIDE: EXTERNAL_MIC_SETUP.txt on Desktop"
echo ""
echo "🚀 QUICK SETUP:"
echo "   1. Double-click: SETUP_MIC.command (select your mic)"
echo "   2. Double-click: ENABLE_VOICE_CONTROL.command (enable Voice Control)"
echo ""
echo "✅ Then you can use voice commands with your iPhone or Beats mic!"
echo ""

say "External microphone setup guide created. Follow the steps to use your iPhone or Beats Studio Pro microphone with Voice Control."


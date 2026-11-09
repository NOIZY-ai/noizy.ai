#!/bin/bash
# WHAT_NOW_ACTION_PLAN.sh
# Clear action plan for next steps

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎯 WHAT NOW - ACTION PLAN                                        ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create simple action plan
cat > "$HOME/Desktop/DO_THIS_NOW.txt" << 'PLAN_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎯 WHAT TO DO NOW - SIMPLE STEPS                                ║
╚══════════════════════════════════════════════════════════════════════╝

STEP 1: ENABLE VOICE CONTROL (2 minutes)
─────────────────────────────────────────

✅ Accessibility settings should be open
✅ Find "Voice Control" in the list
✅ Click the checkbox to enable it
✅ It will automatically use your Beats Studio Pro mic

STEP 2: CONFIGURE BEATS (1 minute)
───────────────────────────────────

✅ Sound settings should be open
✅ Click "Input" tab
✅ Select "Beats Studio Pro"
✅ Set input volume to 75-85%
✅ Click "Output" tab
✅ Select "Beats Studio Pro"

STEP 3: TEST VOICE CONTROL (30 seconds)
────────────────────────────────────────

✅ Say: "Show numbers"
✅ If numbers appear on screen → PERFECT! ✅
✅ If not → Check Voice Control is enabled

STEP 4: COMPLETE EMAIL SETUP (5-10 minutes)
───────────────────────────────────────────

✅ Use voice commands to complete:
   • Cloudflare: Add MX records
   • ImprovMX: Set up forwarding
   • Gmail: Add email aliases

══════════════════════════════════════════════════════════════════════

🎤 VOICE COMMANDS TO USE:
─────────────────────────

"Show numbers"     - See clickable items
"Click [number]"   - Click on numbered item
"Type [text]"      - Type text
"Press return"     - Submit

══════════════════════════════════════════════════════════════════════

✅ YOU'RE 75% DONE!
✅ Just complete these 4 steps and you're finished!

══════════════════════════════════════════════════════════════════════
PLAN_EOF

open "$HOME/Desktop/DO_THIS_NOW.txt"

# Open all necessary windows
echo "📋 OPENING ALL NECESSARY WINDOWS..."
open "x-apple.systempreferences:com.apple.preference.universalaccess"
open "x-apple.systempreferences:com.apple.preference.sound"
open "https://dash.cloudflare.com/login"
open "https://app.improvmx.com/"
open "https://mail.google.com/mail/u/0/#settings/accounts"

# Create quick enable script
cat > "$HOME/Desktop/ENABLE_VOICE_NOW.command" << 'ENABLE_EOF'
#!/bin/bash
# Quick enable Voice Control

clear

echo "🎤 ENABLING VOICE CONTROL..."
echo ""

open "x-apple.systempreferences:com.apple.preference.universalaccess"

sleep 2

echo "✅ Accessibility settings opened!"
echo ""
echo "📋 DO THIS:"
echo "   1. Find 'Voice Control' in the list"
echo "   2. Click the checkbox to enable"
echo "   3. It will use your Beats Studio Pro automatically"
echo ""
echo "Then test by saying: 'Show numbers'"
echo ""

say "Accessibility settings opened. Enable Voice Control by clicking the checkbox. Then say Show numbers to test."
ENABLE_EOF

chmod +x "$HOME/Desktop/ENABLE_VOICE_NOW.command"

echo ""
echo "✅ ACTION PLAN CREATED!"
echo ""
echo "📋 WHAT TO DO:"
echo "   1. Double-click: ENABLE_VOICE_NOW.command"
echo "   2. Enable Voice Control in Accessibility"
echo "   3. Configure Beats in Sound settings"
echo "   4. Test: Say 'Show numbers'"
echo "   5. Complete email setup!"
echo ""

say "Action plan created. Open Enable Voice Now to start. Then follow the simple steps."


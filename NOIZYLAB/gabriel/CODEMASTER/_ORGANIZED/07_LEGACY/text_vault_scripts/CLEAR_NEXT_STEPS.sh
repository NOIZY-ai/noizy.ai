#!/bin/bash
# CLEAR_NEXT_STEPS.sh
# Super clear next steps

clear

cat > "$HOME/Desktop/NEXT_STEP.txt" << 'NEXT_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎯 WHAT TO DO NOW - SUPER SIMPLE                               ║
╚══════════════════════════════════════════════════════════════════════╝

YOU'RE 75% DONE! Just do these 3 things:

══════════════════════════════════════════════════════════════════════

STEP 1: ENABLE VOICE CONTROL (1 click)
───────────────────────────────────────

✅ Accessibility window should be open
✅ Find "Voice Control" in the left sidebar
✅ Click the checkbox next to "Voice Control"
✅ DONE! It will use your Beats Studio Pro automatically

STEP 2: CONFIGURE BEATS (2 clicks)
───────────────────────────────────

✅ Sound window should be open
✅ Click "Input" tab
✅ Select "Beats Studio Pro" from the list
✅ Set the volume slider to about 75%
✅ Click "Output" tab
✅ Select "Beats Studio Pro"
✅ DONE!

STEP 3: TEST IT (Say 2 words)
──────────────────────────────

✅ Say: "Show numbers"
✅ If numbers appear on your screen → PERFECT! ✅
✅ If not → Make sure Voice Control checkbox is checked

══════════════════════════════════════════════════════════════════════

THEN: Complete Email Setup (5-10 minutes)
──────────────────────────────────────────

✅ All email pages are open (Cloudflare, ImprovMX, Gmail)
✅ Use voice commands:
   • Say "Show numbers" to see clickable items
   • Say "Click [number]" to click
   • Say "Type [text]" to type
   • Say "Press return" to submit

══════════════════════════════════════════════════════════════════════

THAT'S IT! You're done after these steps!

══════════════════════════════════════════════════════════════════════
NEXT_EOF

open "$HOME/Desktop/NEXT_STEP.txt"

echo "✅ NEXT_STEP.txt created and opened!"
echo ""
echo "📋 SUPER SIMPLE:"
echo "   1. Enable Voice Control (1 click)"
echo "   2. Configure Beats (2 clicks)"
echo "   3. Test: Say 'Show numbers'"
echo "   4. Complete email setup with voice!"
echo ""

say "Next steps guide created. Enable Voice Control with one click. Configure Beats with two clicks. Then test by saying Show numbers."


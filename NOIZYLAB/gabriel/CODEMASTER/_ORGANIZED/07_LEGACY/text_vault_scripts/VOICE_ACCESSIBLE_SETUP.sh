#!/bin/bash
# VOICE_ACCESSIBLE_SETUP.sh
# Make setup voice-accessible

clear

cat > "$HOME/Desktop/VOICE_DO_THIS.txt" << 'VOICE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎤 VOICE-ACCESSIBLE SETUP                                        ║
╚══════════════════════════════════════════════════════════════════════╝

USE VOICE CONTROL TO DO THIS:

══════════════════════════════════════════════════════════════════════

STEP 1: CLOUDFLARE (Say these commands)
─────────────────────────────────────────

Say: "Show numbers"
→ Numbers will appear on clickable items

Say: "Click [number for fishmusicinc.com]"
→ Click on your domain

Say: "Click [number for DNS]"
→ Go to DNS settings

Say: "Click [number for Add record]"
→ Add new record

Say: "Click [number for Type dropdown]"
→ Select MX

Say: "Type mx1.improvmx.com"
→ Type the mail server

Say: "Type 10"
→ Type priority

Say: "Click [number for Save]"
→ Save the record

Repeat for mx2.improvmx.com with Priority 20

══════════════════════════════════════════════════════════════════════

STEP 2: IMPROVMX (Say these commands)
──────────────────────────────────────

Say: "Show numbers"
→ See clickable items

Say: "Type rp"
→ Type in alias field

Say: "Type rsplowman@gmail.com"
→ Type in forward field

Say: "Click [number for ADD button]"
→ Add the alias

══════════════════════════════════════════════════════════════════════

STEP 3: GMAIL (Say these commands)
───────────────────────────────────

Say: "Show numbers"
→ See clickable items

Say: "Click [number for Settings]"
→ Open settings

Say: "Click [number for Accounts]"
→ Go to accounts

Say: "Click [number for Send mail as]"
→ Add email address

Say: "Type rp@fishmusicinc.com"
→ Type email

Say: "Click [number for Next]"
→ Continue

══════════════════════════════════════════════════════════════════════

VOICE COMMANDS TO USE:
───────────────────────

"Show numbers" - See clickable items
"Click [number]" - Click on numbered item
"Type [text]" - Type text
"Press return" - Press Enter
"Press tab" - Press Tab

══════════════════════════════════════════════════════════════════════
VOICE_EOF

open "$HOME/Desktop/VOICE_DO_THIS.txt"

echo "✅ VOICE_DO_THIS.txt created!"
echo ""
echo "🎤 VOICE-ACCESSIBLE SETUP:"
echo "   ✅ Use Voice Control to complete everything"
echo "   ✅ Say 'Show numbers' to see clickable items"
echo "   ✅ Say 'Click [number]' to click"
echo "   ✅ Say 'Type [text]' to type"
echo ""

say "Voice accessible setup created. Use Voice Control to complete everything. Say Show numbers to see clickable items, then say Click and the number to click on things."


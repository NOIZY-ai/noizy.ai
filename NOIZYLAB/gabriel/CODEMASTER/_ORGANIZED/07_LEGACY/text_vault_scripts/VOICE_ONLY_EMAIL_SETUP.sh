#!/bin/bash
# VOICE_ONLY_EMAIL_SETUP.sh
# Maximum automation for voice-only operation

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎤 VOICE-ONLY EMAIL SETUP                                        ║"
echo "║     Maximum Automation - Voice Commands Only                         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create voice command script
cat > "$HOME/Desktop/VOICE_EMAIL_SETUP.command" << 'VOICE_EOF'
#!/bin/bash
# Voice-Only Email Setup

clear

echo "🎤 VOICE-ONLY EMAIL SETUP"
echo ""
echo "Everything is voice-controlled!"
echo ""

# Open all pages
open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"
sleep 2
open "https://app.improvmx.com/"
sleep 2
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 1

# Create voice command guide
cat > "$HOME/Desktop/VOICE_COMMANDS.txt" << 'COMMANDS_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎤 VOICE COMMANDS - EMAIL SETUP                                  ║
╚══════════════════════════════════════════════════════════════════════╝

ENABLE VOICE CONTROL FIRST:
────────────────────────────

Say: "Hey Siri, open Accessibility settings"
Then enable: "Voice Control"

OR

System Preferences → Accessibility → Voice Control → Enable

══════════════════════════════════════════════════════════════════════
STEP 1: CLOUDFLARE (Page 1)
══════════════════════════════════════════════════════════════════════

Say these commands:

"Show numbers"
  → Shows numbers on all clickable items

"Click [number]"
  → Clicks the numbered item (find "Add record" button)

"Click Add record"
  → Opens the form

"Select MX"
  → Selects MX from dropdown

"Type @"
  → Types @ in name field

"Type 10"
  → Types 10 in priority field

"Type mx1.improvmx.com."
  → Types the mail server (include the dot!)

"Click Save"
  → Saves first record

REPEAT for second MX record:
"Click Add record"
"Select MX"
"Type @"
"Type 20"
"Type mx2.improvmx.com."
"Click Save"

REPEAT for TXT record:
"Click Add record"
"Select TXT"
"Type @"
"Type v=spf1 include:spf.improvmx.com ~all"
"Click Save"

══════════════════════════════════════════════════════════════════════
STEP 2: IMPROVMX (Page 2)
══════════════════════════════════════════════════════════════════════

Say these commands:

"Click fishmusicinc.com"
  → Selects the domain

"Click Aliases"
  → Opens aliases tab

"Click Add alias"
  → Opens alias form

"Type rp"
  → Types alias name

"Type rsplowman@gmail.com"
  → Types forwarding address

"Click Save"
  → Saves alias

══════════════════════════════════════════════════════════════════════
STEP 3: GMAIL (Page 3)
══════════════════════════════════════════════════════════════════════

Say these commands:

"Press Command F"
  → Opens search

"Type Send mail as"
  → Searches for section

"Press Return"
  → Finds the section

"Click Add another email address"
  → Opens form

"Type rp@fishmusicinc.com"
  → Types email address

"Click Next"
  → Submits form

"Check email"
  → Check rsplowman@gmail.com for verification

"Click verification link"
  → Verifies address

══════════════════════════════════════════════════════════════════════
ALL VOICE COMMANDS:
══════════════════════════════════════════════════════════════════════

"Show numbers" - Shows numbers on clickable items
"Click [number]" - Clicks numbered item
"Click [button name]" - Clicks button by name
"Type [text]" - Types text
"Press [key]" - Presses keyboard key
"Scroll down" - Scrolls page
"Go back" - Browser back
"Switch to tab [number]" - Switches browser tabs

══════════════════════════════════════════════════════════════════════

COMMANDS_EOF

open "$HOME/Desktop/VOICE_COMMANDS.txt"

say "Voice email setup activated. All pages opened. Voice commands guide is ready. Enable Voice Control in Accessibility settings to use voice commands."
VOICE_EOF

chmod +x "$HOME/Desktop/VOICE_EMAIL_SETUP.command"

# Create Siri shortcuts
cat > "$HOME/Desktop/SIRI_SHORTCUTS_SETUP.txt" << 'SIRI_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎤 SIRI SHORTCUTS FOR EMAIL SETUP                                ║
╚══════════════════════════════════════════════════════════════════════╝

CREATE THESE SIRI SHORTCUTS:
────────────────────────────

1. "Setup Email"
   → Opens all 3 pages
   → Opens voice commands guide
   → Say: "Hey Siri, setup email"

2. "Open Cloudflare"
   → Opens Cloudflare DNS page
   → Say: "Hey Siri, open Cloudflare"

3. "Open ImprovMX"
   → Opens ImprovMX
   → Say: "Hey Siri, open ImprovMX"

4. "Open Gmail Settings"
   → Opens Gmail settings
   → Say: "Hey Siri, open Gmail settings"

HOW TO CREATE:
  1. Open Shortcuts app
  2. Click "+" to create new shortcut
  3. Add "Run Shell Script" action
  4. Add the command
  5. Name it
  6. Say "Hey Siri, [name]"

══════════════════════════════════════════════════════════════════════

SIRI_EOF

# Run the voice setup
bash "$HOME/Desktop/VOICE_EMAIL_SETUP.command"

echo ""
echo "✅ Voice-only setup activated!"
echo ""
echo "📋 VOICE COMMANDS GUIDE:"
echo "   VOICE_COMMANDS.txt on Desktop"
echo ""
echo "🎤 ENABLE VOICE CONTROL:"
echo "   Say: 'Hey Siri, open Accessibility settings'"
echo "   Then enable: Voice Control"
echo ""
echo "✅ All pages opened - use voice commands!"


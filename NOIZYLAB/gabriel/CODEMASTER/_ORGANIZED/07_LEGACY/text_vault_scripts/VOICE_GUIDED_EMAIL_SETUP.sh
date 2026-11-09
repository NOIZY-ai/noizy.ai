#!/bin/bash
# VOICE_GUIDED_EMAIL_SETUP.sh
# Voice-guided email setup with Beats mic

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎤 VOICE-GUIDED EMAIL SETUP                                     ║"
echo "║     Beats Studio Pro Ready!                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create voice-guided workflow
cat > "$HOME/Desktop/VOICE_EMAIL_SETUP.command" << 'VOICE_EOF'
#!/bin/bash
# Voice-Guided Email Setup

clear

echo "🎤 VOICE-GUIDED EMAIL SETUP"
echo ""
echo "Your Beats Studio Pro are ready!"
echo ""

# Check if Voice Control is enabled
echo "📋 First, let's make sure Voice Control is enabled..."
echo ""

open "x-apple.systempreferences:com.apple.preference.universalaccess"

sleep 2

echo ""
echo "✅ Accessibility settings opened"
echo ""
echo "📋 CHECK:"
echo "   • Find 'Voice Control' in the list"
echo "   • Make sure it's enabled (toggle should be ON)"
echo ""
echo "If not enabled, say: 'Click Voice Control' then 'Click Enable'"
echo ""

# Open all pages
echo "🚀 Opening all setup pages..."
open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"
sleep 2
open "https://app.improvmx.com/"
sleep 2
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 1

# Create voice command guide
cat > "$HOME/Desktop/VOICE_STEPS.txt" << 'STEPS_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎤 VOICE STEPS - EMAIL SETUP                                     ║
║     Use Your Beats Studio Pro Mic                                    ║
╚══════════════════════════════════════════════════════════════════════╝

FIRST: ENABLE VOICE CONTROL
────────────────────────────

Say: "Show numbers"
→ If numbers appear → Voice Control is working! ✅
→ If nothing happens → Enable Voice Control first

══════════════════════════════════════════════════════════════════════
STEP 1: CLOUDFLARE (Page 1 - Tab 1)
══════════════════════════════════════════════════════════════════════

Say these commands (speak into your Beats mic):

"Show numbers"
→ Shows numbers on all buttons

"Click [number for Add record]"
OR
"Click Add record"
→ Opens the form

"Select MX"
→ Selects MX from dropdown

"Type @"
→ Types @ in name field

"Type 10"
→ Types 10 in priority field

"Type mx1.improvmx.com."
→ Types mail server (include the dot!)

"Click Save"
→ Saves first record

REPEAT for second record:
"Click Add record"
"Select MX"
"Type @"
"Type 20"
"Type mx2.improvmx.com."
"Click Save"

REPEAT for third record:
"Click Add record"
"Select TXT"
"Type @"
"Type v=spf1 include:spf.improvmx.com ~all"
"Click Save"

THAT'S IT FOR STEP 1! Wait 2 minutes, then go to Step 2.

══════════════════════════════════════════════════════════════════════
STEP 2: IMPROVMX (Page 2 - Tab 2)
══════════════════════════════════════════════════════════════════════

Say these commands:

"Switch to tab 2"
→ Switches to ImprovMX tab

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

THAT'S IT FOR STEP 2!

══════════════════════════════════════════════════════════════════════
STEP 3: GMAIL (Page 3 - Tab 3)
══════════════════════════════════════════════════════════════════════

Say these commands:

"Switch to tab 3"
→ Switches to Gmail tab

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

THAT'S IT! YOU'RE DONE!

══════════════════════════════════════════════════════════════════════
ALL VOICE COMMANDS:
══════════════════════════════════════════════════════════════════════

"Show numbers" - Shows numbers on buttons
"Click [number]" - Clicks numbered item
"Click [button name]" - Clicks button
"Type [text]" - Types text
"Press [key]" - Presses key (Command, Return, etc.)
"Switch to tab [number]" - Switches browser tabs
"Scroll down" - Scrolls page
"Go back" - Browser back

══════════════════════════════════════════════════════════════════════

STEPS_EOF

open "$HOME/Desktop/VOICE_STEPS.txt"

echo ""
echo "✅ All pages opened!"
echo "✅ Voice steps guide opened!"
echo ""
echo "📋 NEXT:"
echo "   1. Make sure Voice Control is enabled"
echo "   2. Put on your Beats Studio Pro"
echo "   3. Follow the voice steps in: VOICE_STEPS.txt"
echo ""

say "Voice guided email setup ready. All pages opened. Put on your Beats Studio Pro headphones. Follow the voice steps guide. Say Show numbers to test Voice Control."
VOICE_EOF

chmod +x "$HOME/Desktop/VOICE_EMAIL_SETUP.command"

# Run it
bash "$HOME/Desktop/VOICE_EMAIL_SETUP.command"

echo ""
echo "✅ Voice-guided setup ready!"
echo ""
echo "🎤 PUT ON YOUR BEATS STUDIO PRO:"
echo "   Then say: 'Show numbers'"
echo "   If numbers appear → Voice Control is working!"
echo ""
echo "📋 FOLLOW: VOICE_STEPS.txt on Desktop"
echo ""

say "Beats Studio Pro setup complete. Voice guided email setup ready. Put on your headphones and say Show numbers to test."


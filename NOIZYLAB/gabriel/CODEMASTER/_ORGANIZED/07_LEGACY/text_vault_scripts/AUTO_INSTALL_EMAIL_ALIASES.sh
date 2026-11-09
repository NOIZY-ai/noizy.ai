#!/bin/bash
# AUTO_INSTALL_EMAIL_ALIASES.sh
# Attempts to automate email alias installation as much as possible

set -e

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🤖 AUTOMATED EMAIL ALIASES INSTALLATION                         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

PRIMARY_EMAIL="rsplowman@gmail.com"
ALIASES=(
    "rp@fishmusicinc.com"
    "rsp@noizylab.ca"
    "help@noizylab.ca"
)

echo "🚀 Starting automated installation..."
echo ""

# Step 1: Open Gmail settings
echo "📧 Step 1: Opening Gmail settings..."
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 3

# Step 2: Open ImprovMX
echo "📧 Step 2: Opening ImprovMX..."
open "https://improvmx.com/"
sleep 2

# Step 3: Create configuration file for reference
echo "📧 Step 3: Creating configuration file..."
CONFIG_FILE="$HOME/NOIZYLAB/email/aliases_config.txt"

cat > "$CONFIG_FILE" << EOF
EMAIL ALIASES CONFIGURATION
===========================

Primary Email: $PRIMARY_EMAIL

Aliases to Configure:
  1. rp@fishmusicinc.com
  2. rsp@noizylab.ca
  3. help@noizylab.ca

GMAIL SETUP:
  URL: https://mail.google.com/mail/u/0/#settings/accounts
  Section: "Send mail as"
  Action: Add each alias above
  Verification: Check email for each alias

IMPROVMX SETUP:
  URL: https://improvmx.com/
  Action: Sign up (free), add domains, set forwarding
  Forwarding:
    rp@fishmusicinc.com → $PRIMARY_EMAIL
    rsp@noizylab.ca → $PRIMARY_EMAIL
    help@noizylab.ca → $PRIMARY_EMAIL

Created: $(date)
EOF

echo "✅ Configuration saved: $CONFIG_FILE"

# Step 4: Create macOS Mail configuration script
echo "📧 Step 4: Creating macOS Mail configuration..."
MAIL_SCRIPT="$HOME/NOIZYLAB/email/automation/configure_mail.sh"

cat > "$MAIL_SCRIPT" << 'MAIL_SCRIPT_EOF'
#!/bin/bash
# Configure macOS Mail with aliases

echo "📧 Configuring macOS Mail..."
echo ""
echo "This will open Mail preferences."
echo "Please add the aliases manually:"
echo "  1. Mail → Preferences (CMD+,)"
echo "  2. Accounts tab"
echo "  3. Select Gmail account"
echo "  4. Click 'Edit Email Addresses'"
echo "  5. Add: rp@fishmusicinc.com"
echo "  6. Add: rsp@noizylab.ca"
echo "  7. Add: help@noizylab.ca"
echo ""

# Open Mail app
open -a Mail

# Wait a moment
sleep 2

# Open preferences
osascript << APPLESCRIPT
tell application "Mail"
    activate
    delay 1
end tell
tell application "System Events"
    tell process "Mail"
        keystroke "," using {command down}
    end tell
end tell
APPLESCRIPT

echo "✅ Mail preferences opened"
echo "📋 Follow the instructions above to add aliases"
MAIL_SCRIPT_EOF

chmod +x "$MAIL_SCRIPT"

# Step 5: Create verification checklist
echo "📧 Step 5: Creating verification checklist..."
CHECKLIST="$HOME/Desktop/EMAIL_ALIASES_CHECKLIST.txt"

cat > "$CHECKLIST" << EOF
╔══════════════════════════════════════════════════════════════════════╗
║     EMAIL ALIASES INSTALLATION CHECKLIST                            ║
╚══════════════════════════════════════════════════════════════════════╝

GMAIL "SEND AS" SETUP:
───────────────────────
□ Opened Gmail settings (should be open now)
□ Scrolled to "Send mail as" section
□ Clicked "Add another email address"
□ Added: rp@fishmusicinc.com
□ Verified via email
□ Added: rsp@noizylab.ca
□ Verified via email
□ Added: help@noizylab.ca
□ Verified via email

IMPROVMX SETUP (For Receiving):
───────────────────────────────
□ Opened ImprovMX (should be open now)
□ Signed up for free account
□ Added domain: fishmusicinc.com
□ Added domain: noizylab.ca
□ Set forwarding: rp@fishmusicinc.com → rsplowman@gmail.com
□ Set forwarding: rsp@noizylab.ca → rsplowman@gmail.com
□ Set forwarding: help@noizylab.ca → rsplowman@gmail.com

MACOS MAIL (Optional):
──────────────────────
□ Opened Mail app
□ Opened Preferences (CMD+,)
□ Added aliases to Gmail account
□ Tested sending from alias

VERIFICATION:
─────────────
□ Sent test email TO rp@fishmusicinc.com
□ Received in rsplowman@gmail.com inbox
□ Sent test email FROM rp@fishmusicinc.com
□ Recipient sees custom domain address
□ Tested other aliases

══════════════════════════════════════════════════════════════════════

All pages should be open now!
Follow the checklist above to complete setup.

EOF

echo "✅ Checklist created: $CHECKLIST"

# Step 6: Open checklist
open "$CHECKLIST"

# Step 7: Speak instructions
say "Email setup pages opened. Gmail settings and ImprovMX are ready. Follow the checklist on your desktop."

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          ✅ AUTOMATED INSTALLATION STARTED                            ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 WHAT'S BEEN DONE:"
echo ""
echo "✅ Gmail settings page opened"
echo "✅ ImprovMX page opened"
echo "✅ Configuration file created"
echo "✅ macOS Mail script created"
echo "✅ Checklist created and opened"
echo ""
echo "📋 NEXT STEPS (Minimal Interaction Required):"
echo ""
echo "1. In Gmail (already open):"
echo "   • Scroll to 'Send mail as' section"
echo "   • Add each alias (use keyboard: TAB, SPACE, RETURN)"
echo "   • Verify via email"
echo ""
echo "2. In ImprovMX (already open):"
echo "   • Sign up (free, 2 minutes)"
echo "   • Add domains and forwarding"
echo ""
echo "3. Check checklist: EMAIL_ALIASES_CHECKLIST.txt on Desktop"
echo ""
echo "🎤 Voice commands available:"
echo "   Say: 'Click [button name]'"
echo "   Say: 'Type [text]'"
echo "   Say: 'Scroll down'"
echo ""
echo "⌨️  Keyboard shortcuts:"
echo "   TAB: Navigate"
echo "   SPACE: Click"
echo "   RETURN: Submit"
echo ""
echo "⚡⚡⚡ Installation in progress! ⚡⚡⚡"
echo ""


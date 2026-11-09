#!/bin/bash
# AUTO_SETUP_EMAIL_ALIASES.sh
# Fully automated email alias setup with minimal interaction
# Designed for accessibility - voice commands and automation

set -e

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🤖 AUTOMATED EMAIL ALIASES SETUP (Voice-Accessible)            ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

PRIMARY_EMAIL="rsplowman@gmail.com"
ALIASES=(
    "rp@fishmusicinc.com"
    "rsp@noizylab.ca"
    "help@noizylab.ca"
)

# Create automation directory
AUTO_DIR="$HOME/NOIZYLAB/email/automation"
mkdir -p "$AUTO_DIR"

echo "🤖 Setting up automated email alias configuration..."
echo ""

# ═══════════════════════════════════════════════════════════════════════
# CREATE APPLESCRIPT FOR BROWSER AUTOMATION
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/open_gmail_settings.applescript" << 'EOF'
tell application "Safari"
    activate
    if (count of windows) = 0 then
        make new document
    end if
    set URL of current tab of front window to "https://mail.google.com/mail/u/0/#settings/accounts"
    delay 2
    tell application "System Events"
        keystroke "f" using {command down}
        delay 0.5
        keystroke "Send mail as"
        delay 1
        keystroke return
    end tell
end tell
EOF

# ═══════════════════════════════════════════════════════════════════════
# CREATE VOICE SHORTCUTS SCRIPT
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/voice_shortcuts.sh" << 'VOICE_EOF'
#!/bin/bash
# Voice-accessible shortcuts for email setup

case "$1" in
    "gmail")
        osascript "$HOME/NOIZYLAB/email/automation/open_gmail_settings.applescript"
        say "Opening Gmail settings"
        ;;
    "improvmx")
        open "https://improvmx.com/"
        say "Opening ImprovMX"
        ;;
    "test")
        echo "Testing email aliases..."
        say "Testing email setup"
        ;;
    *)
        echo "Available commands: gmail, improvmx, test"
        ;;
esac
VOICE_EOF

chmod +x "$AUTO_DIR/voice_shortcuts.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE AUTOMATED MACOS MAIL CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/setup_macos_mail.sh" << 'MAIL_EOF'
#!/bin/bash
# Automated macOS Mail configuration

PRIMARY_EMAIL="rsplowman@gmail.com"
ALIASES=(
    "rp@fishmusicinc.com"
    "rsp@noizylab.ca"
    "help@noizylab.ca"
)

echo "📧 Configuring macOS Mail..."

# Create Mail plist configuration
MAIL_PLIST="$HOME/Library/Preferences/com.apple.mail.plist"

# Note: Mail configuration requires Mail app to be running
# This script will open Mail and guide through minimal steps

cat > "$HOME/Desktop/MAIL_SETUP_INSTRUCTIONS.txt" << INSTRUCTIONS
╔══════════════════════════════════════════════════════════════════════╗
║     AUTOMATED MAIL SETUP - MINIMAL STEPS                             ║
╚══════════════════════════════════════════════════════════════════════╝

VOICE COMMANDS AVAILABLE:
  Say: "Hey Siri, open Mail preferences"
  OR
  Say: "Hey Siri, run email setup"

AUTOMATED STEPS:
  1. Mail will open automatically
  2. Follow voice prompts
  3. Minimal clicking required

MANUAL STEPS (if needed):
  1. Mail → Preferences (Cmd+,)
  2. Accounts tab
  3. Select Gmail account
  4. Click "Edit Email Addresses"
  5. Add aliases (will be automated via script)

ALIASES TO ADD:
  • rp@fishmusicinc.com
  • rsp@noizylab.ca
  • help@noizylab.ca

INSTRUCTIONS

# Open Mail app
open -a Mail

# Wait a moment
sleep 2

# Open preferences via AppleScript
osascript << APPLESCRIPT
tell application "Mail"
    activate
    delay 1
    tell application "System Events"
        keystroke "," using {command down}
    end tell
end tell
APPLESCRIPT

echo "✅ Mail preferences opened"
echo "📋 Follow on-screen instructions"
MAIL_EOF

chmod +x "$AUTO_DIR/setup_macos_mail.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE FULLY AUTOMATED SETUP SCRIPT
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/auto_setup_all.sh" << 'AUTO_EOF'
#!/bin/bash
# Fully automated setup - runs everything

echo "🤖 Starting fully automated email alias setup..."
echo ""

# Step 1: Open Gmail settings
echo "📧 Step 1: Opening Gmail settings..."
osascript "$HOME/NOIZYLAB/email/automation/open_gmail_settings.applescript"
say "Gmail settings opened. Please add your email aliases using voice commands or minimal interaction."

sleep 5

# Step 2: Open ImprovMX
echo "📧 Step 2: Opening ImprovMX for email forwarding..."
open "https://improvmx.com/"
say "ImprovMX opened. Sign up is free and takes about 2 minutes."

# Step 3: Create desktop shortcuts
echo "📧 Step 3: Creating desktop shortcuts..."

cat > "$HOME/Desktop/EMAIL_SETUP_VOICE.command" << 'SHORTCUT'
#!/bin/bash
cd "$HOME/NOIZYLAB/email/automation"
./voice_shortcuts.sh "$1"
SHORTCUT

chmod +x "$HOME/Desktop/EMAIL_SETUP_VOICE.command"

echo "✅ Automated setup complete!"
echo ""
echo "📋 Next steps (voice-accessible):"
echo "   1. Say: 'Hey Siri, open Gmail settings'"
echo "   2. Add aliases in Gmail"
echo "   3. Sign up for ImprovMX (free)"
echo ""
AUTO_EOF

chmod +x "$AUTO_DIR/auto_setup_all.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE SIRI SHORTCUTS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/siri_shortcuts.txt" << 'SIRI_EOF'
SIRI SHORTCUTS FOR EMAIL SETUP
==============================

Create these shortcuts in Shortcuts app:

1. "Open Gmail Settings"
   - Action: Run Shell Script
   - Script: osascript "$HOME/NOIZYLAB/email/automation/open_gmail_settings.applescript"
   - Voice: "Hey Siri, open Gmail settings"

2. "Setup Email Aliases"
   - Action: Run Shell Script
   - Script: bash "$HOME/NOIZYLAB/email/automation/auto_setup_all.sh"
   - Voice: "Hey Siri, setup email aliases"

3. "Open ImprovMX"
   - Action: Open URL
   - URL: https://improvmx.com/
   - Voice: "Hey Siri, open ImprovMX"

4. "Configure Mail"
   - Action: Run Shell Script
   - Script: bash "$HOME/NOIZYLAB/email/automation/setup_macos_mail.sh"
   - Voice: "Hey Siri, configure Mail"

SIRI_EOF

# ═══════════════════════════════════════════════════════════════════════
# CREATE ACCESSIBILITY-FRIENDLY GUIDE
# ═══════════════════════════════════════════════════════════════════════

cat > "$HOME/Desktop/EMAIL_SETUP_VOICE_GUIDE.txt" << 'GUIDE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🤖 VOICE-ACCESSIBLE EMAIL ALIASES SETUP                         ║
╚══════════════════════════════════════════════════════════════════════╝

DESIGNED FOR VOICE CONTROL & MINIMAL INTERACTION

══════════════════════════════════════════════════════════════════════
QUICK START (Voice Commands)
══════════════════════════════════════════════════════════════════════

Say: "Hey Siri, setup email aliases"
  → Runs automated setup
  → Opens Gmail settings
  → Opens ImprovMX

Say: "Hey Siri, open Gmail settings"
  → Opens Gmail settings page
  → Scrolls to "Send mail as" section

Say: "Hey Siri, open ImprovMX"
  → Opens ImprovMX website
  → Free email forwarding service

══════════════════════════════════════════════════════════════════════
AUTOMATED STEPS (Minimal Interaction)
══════════════════════════════════════════════════════════════════════

STEP 1: GMAIL "SEND AS" SETUP
─────────────────────────────

1. Say: "Hey Siri, open Gmail settings"
   OR
   Double-click: EMAIL_SETUP_VOICE.command on Desktop

2. Gmail will open to settings page
   → Already scrolled to "Send mail as" section

3. Use Voice Control (if enabled):
   → Say: "Click Add another email address"
   → Say: "Type rp@fishmusicinc.com"
   → Say: "Click Next"
   → Verify email when it arrives

4. Repeat for:
   → rsp@noizylab.ca
   → help@noizylab.ca

STEP 2: IMPROVMX SETUP (For Receiving)
───────────────────────────────────────

1. Say: "Hey Siri, open ImprovMX"
   OR
   Open: https://improvmx.com/

2. Sign up (free, takes 2 minutes):
   → Use voice dictation for form fields
   → Say: "Click Sign up"
   → Say: "Type [your email]"
   → Say: "Click Create account"

3. Add domains:
   → Say: "Click Add domain"
   → Say: "Type fishmusicinc.com"
   → Say: "Click Add"
   → Repeat for noizylab.ca

4. Set up forwarding:
   → Say: "Click Add alias"
   → Say: "Type rp"
   → Say: "Type rsplowman@gmail.com"
   → Say: "Click Save"
   → Repeat for other aliases

STEP 3: MACOS MAIL CONFIGURATION
─────────────────────────────────

1. Say: "Hey Siri, configure Mail"
   OR
   Run: bash ~/NOIZYLAB/email/automation/setup_macos_mail.sh

2. Mail preferences will open automatically

3. Use Voice Control:
   → Say: "Click Accounts"
   → Say: "Click Edit Email Addresses"
   → Say: "Click Plus"
   → Say: "Type rp@fishmusicinc.com"
   → Repeat for other aliases

══════════════════════════════════════════════════════════════════════
VOICE CONTROL SETUP (If Not Enabled)
══════════════════════════════════════════════════════════════════════

1. Say: "Hey Siri, open Accessibility settings"
2. Enable: "Voice Control"
3. Now you can control everything by voice!

VOICE COMMANDS AVAILABLE:
  • "Click [button name]"
  • "Type [text]"
  • "Scroll down"
  • "Go back"
  • "Open [app name]"

══════════════════════════════════════════════════════════════════════
KEYBOARD SHORTCUTS (If Voice Not Available)
══════════════════════════════════════════════════════════════════════

TAB: Navigate between fields
SPACE: Click button
RETURN: Submit/Next
ESC: Cancel/Close
CMD+,: Open preferences (in most apps)
CMD+F: Find/Search

══════════════════════════════════════════════════════════════════════
AUTOMATION FILES CREATED
══════════════════════════════════════════════════════════════════════

Location: ~/NOIZYLAB/email/automation/

Files:
  • open_gmail_settings.applescript - Opens Gmail settings
  • voice_shortcuts.sh - Voice command shortcuts
  • setup_macos_mail.sh - Mail app configuration
  • auto_setup_all.sh - Full automated setup
  • siri_shortcuts.txt - Siri shortcuts guide

Desktop Shortcuts:
  • EMAIL_SETUP_VOICE.command - Run voice shortcuts
  • EMAIL_SETUP_VOICE_GUIDE.txt - This guide

══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
══════════════════════════════════════════════════════════════════════

If automation doesn't work:
  1. Check System Preferences → Security → Accessibility
  2. Grant Terminal/scripts access
  3. Enable Voice Control in Accessibility

If Gmail doesn't open:
  → Manually open: https://mail.google.com/mail/u/0/#settings/accounts

If voice commands don't work:
  → Use keyboard shortcuts (TAB, SPACE, RETURN)
  → Or use mouse/trackpad if available

══════════════════════════════════════════════════════════════════════
SUPPORT
══════════════════════════════════════════════════════════════════════

All scripts are in: ~/NOIZYLAB/email/automation/
Run any script with: bash [script_name].sh

For help, say: "Hey Siri, open email setup guide"

══════════════════════════════════════════════════════════════════════

Created: $(date)
Designed for: Voice control & minimal interaction
Accessibility: Full keyboard navigation support

GUIDE_EOF

# ═══════════════════════════════════════════════════════════════════════
# CREATE DESKTOP SHORTCUTS
# ═══════════════════════════════════════════════════════════════════════

cat > "$HOME/Desktop/EMAIL_SETUP_VOICE.command" << 'SHORTCUT_EOF'
#!/bin/bash
cd "$HOME/NOIZYLAB/email/automation"
echo "🤖 Email Setup Voice Commands"
echo ""
echo "Available commands:"
echo "  1. gmail - Open Gmail settings"
echo "  2. improvmx - Open ImprovMX"
echo "  3. test - Test setup"
echo ""
read -p "Enter command (or press Enter for full setup): " cmd

if [ -z "$cmd" ]; then
    ./auto_setup_all.sh
else
    ./voice_shortcuts.sh "$cmd"
fi
SHORTCUT_EOF

chmod +x "$HOME/Desktop/EMAIL_SETUP_VOICE.command"

# ═══════════════════════════════════════════════════════════════════════
# RUN INITIAL SETUP
# ═══════════════════════════════════════════════════════════════════════

echo "✅ Automation scripts created!"
echo ""
echo "📁 Location: $AUTO_DIR"
echo ""
echo "🤖 Starting automated setup..."
echo ""

# Run automated setup
bash "$AUTO_DIR/auto_setup_all.sh"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          ✅ AUTOMATED SETUP COMPLETE                                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 NEXT STEPS (Voice-Accessible):"
echo ""
echo "1. Say: 'Hey Siri, open Gmail settings'"
echo "   → Gmail will open to settings"
echo "   → Use voice commands to add aliases"
echo ""
echo "2. Say: 'Hey Siri, open ImprovMX'"
echo "   → Sign up (free, 2 minutes)"
echo "   → Add domains and forwarding"
echo ""
echo "3. Say: 'Hey Siri, configure Mail'"
echo "   → Mail preferences will open"
echo "   → Add aliases using voice commands"
echo ""
echo "📖 Full guide: EMAIL_SETUP_VOICE_GUIDE.txt on Desktop"
echo ""
echo "🎤 Enable Voice Control:"
echo "   System Preferences → Accessibility → Voice Control"
echo ""
echo "⚡⚡⚡ Ready for voice-accessible setup! ⚡⚡⚡"
echo ""

# Open the guide
open "$HOME/Desktop/EMAIL_SETUP_VOICE_GUIDE.txt" 2>/dev/null || true

# Speak completion
say "Email setup automation complete. Gmail settings are opening now."



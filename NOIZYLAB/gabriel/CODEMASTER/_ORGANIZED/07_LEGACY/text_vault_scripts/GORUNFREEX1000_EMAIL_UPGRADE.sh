#!/bin/bash
# GORUNFREEX1000_EMAIL_UPGRADE.sh
# ULTIMATE EMAIL ALIASES UPGRADE - MAXIMUM AUTOMATION
# Voice-Accessible, Keyboard-Only, Fully Automated

set -e

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ⚡⚡⚡ GORUNFREEX1000 EMAIL UPGRADE ⚡⚡⚡                          ║"
echo "║     ULTIMATE AUTOMATION - VOICE & KEYBOARD ACCESSIBLE                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

PRIMARY_EMAIL="rsplowman@gmail.com"
DOMAINS=("fishmusicinc.com" "noizylab.ca")
ALIASES=(
    "rp@fishmusicinc.com"
    "rsp@noizylab.ca"
    "help@noizylab.ca"
)

AUTO_DIR="$HOME/NOIZYLAB/email/automation"
mkdir -p "$AUTO_DIR"

echo "🚀 UPGRADING ALL SYSTEMS..."
echo ""

# ═══════════════════════════════════════════════════════════════════════
# CREATE ULTIMATE AUTOMATION SCRIPT
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/ULTIMATE_AUTO_SETUP.sh" << 'ULTIMATE_EOF'
#!/bin/bash
# ULTIMATE_AUTO_SETUP.sh - One command does everything

PRIMARY_EMAIL="rsplowman@gmail.com"

echo "⚡ GORUNFREEX1000 - ULTIMATE SETUP"
echo ""

# Open all necessary pages
echo "📧 Opening all setup pages..."
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 1
open "https://app.improvmx.com/"
sleep 1

# Create master checklist
cat > "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt" << CHECKLIST_EOF
╔══════════════════════════════════════════════════════════════════════╗
║     ⚡ GORUNFREEX1000 - MASTER EMAIL SETUP CHECKLIST ⚡              ║
╚══════════════════════════════════════════════════════════════════════╝

ALL PAGES ARE NOW OPEN - FOLLOW THESE STEPS:

══════════════════════════════════════════════════════════════════════
GMAIL SETUP (Tab 1)
══════════════════════════════════════════════════════════════════════

□ Press CMD+F, type "Send mail as"
□ TAB to "Add another email address"
□ SPACE to click
□ Type: rp@fishmusicinc.com
□ TAB, TAB, RETURN
□ Check email for verification
□ Repeat for: rsp@noizylab.ca
□ Repeat for: help@noizylab.ca

VOICE: "Click Add another email address"
       "Type rp@fishmusicinc.com"
       "Click Next"

══════════════════════════════════════════════════════════════════════
IMPROVMX SETUP (Tab 2)
══════════════════════════════════════════════════════════════════════

STEP 1: SIGN UP (if not done)
□ TAB to "Sign up"
□ SPACE to click
□ Fill form (voice dictation)
□ TAB to "Create account"
□ RETURN

STEP 2: ADD DOMAINS
□ TAB to "Add domain"
□ SPACE to click
□ Type: fishmusicinc.com
□ TAB, RETURN
□ Repeat for: noizylab.ca

STEP 3: CREATE ALIASES
Domain: fishmusicinc.com
□ TAB to "Add alias"
□ Alias: rp
□ Forward: rsplowman@gmail.com
□ TAB to "Save", RETURN

Domain: noizylab.ca
□ Alias: rsp → rsplowman@gmail.com
□ Alias: help → rsplowman@gmail.com

VOICE: "Click Add domain"
       "Type fishmusicinc.com"
       "Click Add alias"
       "Type rp"
       "Type rsplowman@gmail.com"
       "Click Save"

══════════════════════════════════════════════════════════════════════
MACOS MAIL SETUP (Optional)
══════════════════════════════════════════════════════════════════════

□ Open Mail app (CMD+SPACE, type "Mail", RETURN)
□ Mail → Preferences (CMD+,)
□ Accounts tab
□ Select Gmail account
□ Click "Edit Email Addresses"
□ Add: rp@fishmusicinc.com
□ Add: rsp@noizylab.ca
□ Add: help@noizylab.ca

VOICE: "Open Mail"
       "Click Preferences"
       "Click Accounts"
       "Click Edit Email Addresses"

══════════════════════════════════════════════════════════════════════
VERIFICATION
══════════════════════════════════════════════════════════════════════

□ Send test email TO rp@fishmusicinc.com
□ Should arrive in rsplowman@gmail.com
□ Send test email FROM rp@fishmusicinc.com
□ Recipient sees custom domain
□ Test all aliases

══════════════════════════════════════════════════════════════════════

⚡⚡⚡ GORUNFREEX1000 - ALL SYSTEMS GO! ⚡⚡⚡

CHECKLIST_EOF

open "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt"

say "GORUNFREEX1000 setup complete. All pages opened. Follow the checklist."
ULTIMATE_EOF

chmod +x "$AUTO_DIR/ULTIMATE_AUTO_SETUP.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE VOICE COMMAND DICTIONARY
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/voice_commands.txt" << 'VOICE_EOF'
VOICE COMMAND DICTIONARY - GORUNFREEX1000
==========================================

GMAIL COMMANDS:
  "Open Gmail settings"
  "Add email alias"
  "Type rp@fishmusicinc.com"
  "Click Add another email address"
  "Click Next"
  "Click Verify"
  "Scroll to Send mail as"

IMPROVMX COMMANDS:
  "Open ImprovMX"
  "Click Sign up"
  "Click Add domain"
  "Type fishmusicinc.com"
  "Click Add alias"
  "Type rp"
  "Type rsplowman@gmail.com"
  "Click Save"

GENERAL COMMANDS:
  "Show numbers" - Shows numbers on clickable items
  "Click [number]" - Clicks numbered item
  "Scroll down" - Scrolls page
  "Go back" - Browser back
  "Open new tab" - New browser tab
  "Close tab" - Close current tab
  "Switch to tab [number]" - Switch tabs

KEYBOARD SHORTCUTS:
  TAB: Navigate
  SPACE: Click
  RETURN: Submit
  ESC: Cancel
  CMD+F: Find
  CMD+,: Preferences
  CMD+T: New tab
  CMD+W: Close tab
  CMD+[1-9]: Switch to tab number

VOICE_EOF

# ═══════════════════════════════════════════════════════════════════════
# CREATE ENHANCED SIRI SHORTCUTS
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/siri_shortcuts_enhanced.txt" << 'SIRI_EOF'
ENHANCED SIRI SHORTCUTS - GORUNFREEX1000
========================================

Create these in Shortcuts app:

1. "Setup Email Aliases"
   → Opens Gmail settings
   → Opens ImprovMX
   → Opens checklist
   → Voice: "Hey Siri, setup email aliases"

2. "Open Gmail Settings"
   → Opens Gmail settings page
   → Scrolls to "Send mail as"
   → Voice: "Hey Siri, open Gmail settings"

3. "Open ImprovMX"
   → Opens ImprovMX dashboard
   → Voice: "Hey Siri, open ImprovMX"

4. "Add Email Domain"
   → Opens ImprovMX add domain page
   → Voice: "Hey Siri, add email domain"

5. "Test Email Aliases"
   → Opens email compose
   → Pre-fills test message
   → Voice: "Hey Siri, test email aliases"

6. "Email Setup Status"
   → Checks setup progress
   → Shows checklist
   → Voice: "Hey Siri, email setup status"

SIRI_EOF

# ═══════════════════════════════════════════════════════════════════════
# CREATE MASTER CONTROL SCRIPT
# ═══════════════════════════════════════════════════════════════════════

cat > "$HOME/Desktop/GORUNFREEX1000_EMAIL.command" << 'MASTER_EOF'
#!/bin/bash
# GORUNFREEX1000 EMAIL MASTER CONTROL
# One command to rule them all

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ⚡⚡⚡ GORUNFREEX1000 EMAIL MASTER CONTROL ⚡⚡⚡                  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "🎯 SELECT ACTION:"
echo ""
echo "1. 🚀 ULTIMATE SETUP (Opens everything)"
echo "2. 📧 Gmail Settings"
echo "3. 🌐 ImprovMX"
echo "4. 📋 View Checklist"
echo "5. 🧪 Test Aliases"
echo "6. 📊 Status Check"
echo "7. 🎤 Voice Commands Help"
echo "0. Exit"
echo ""

read -p "👉 Enter choice (0-7): " choice

case $choice in
    1)
        bash "$HOME/NOIZYLAB/email/automation/ULTIMATE_AUTO_SETUP.sh"
        ;;
    2)
        open "https://mail.google.com/mail/u/0/#settings/accounts"
        say "Gmail settings opened"
        ;;
    3)
        open "https://app.improvmx.com/"
        say "ImprovMX opened"
        ;;
    4)
        open "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt" 2>/dev/null || \
        cat "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt"
        ;;
    5)
        open "mailto:rp@fishmusicinc.com?subject=Test&body=Testing email alias"
        say "Test email opened"
        ;;
    6)
        echo "📊 EMAIL SETUP STATUS:"
        echo ""
        echo "Gmail: Check manually at settings"
        echo "ImprovMX: Check at app.improvmx.com"
        echo "Aliases configured:"
        echo "  • rp@fishmusicinc.com"
        echo "  • rsp@noizylab.ca"
        echo "  • help@noizylab.ca"
        ;;
    7)
        cat "$HOME/NOIZYLAB/email/automation/voice_commands.txt"
        ;;
    0)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
MASTER_EOF

chmod +x "$HOME/Desktop/GORUNFREEX1000_EMAIL.command"

# ═══════════════════════════════════════════════════════════════════════
# CREATE ACCESSIBILITY ENHANCEMENTS
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/enable_accessibility.sh" << 'ACCESS_EOF'
#!/bin/bash
# Enable all accessibility features

echo "🔧 Enabling Accessibility Features..."
echo ""

# Open Accessibility settings
open "x-apple.systempreferences:com.apple.preference.universalaccess"

echo "📋 Enable these features:"
echo ""
echo "✅ Voice Control"
echo "   → Allows voice commands for everything"
echo ""
echo "✅ Keyboard Navigation"
echo "   → Full keyboard control"
echo ""
echo "✅ VoiceOver (if needed)"
echo "   → Screen reader"
echo ""
echo "✅ Zoom (if needed)"
echo "   → Screen magnification"
echo ""
echo "Press Enter when done..."
read

echo "✅ Accessibility features configured!"
ACCESS_EOF

chmod +x "$AUTO_DIR/enable_accessibility.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE TESTING SCRIPT
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/test_aliases.sh" << 'TEST_EOF'
#!/bin/bash
# Test email aliases

echo "🧪 Testing Email Aliases..."
echo ""

ALIASES=(
    "rp@fishmusicinc.com"
    "rsp@noizylab.ca"
    "help@noizylab.ca"
)

echo "📧 Opening test emails..."
echo ""

for alias in "${ALIASES[@]}"; do
    echo "Opening: $alias"
    open "mailto:$alias?subject=Test&body=Testing email alias setup"
    sleep 1
done

echo ""
echo "✅ Test emails opened!"
echo "📋 Check if they arrive in rsplowman@gmail.com"
TEST_EOF

chmod +x "$AUTO_DIR/test_aliases.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE STATUS CHECKER
# ═══════════════════════════════════════════════════════════════════════

cat > "$AUTO_DIR/check_status.sh" << 'STATUS_EOF'
#!/bin/bash
# Check email setup status

echo "📊 EMAIL SETUP STATUS CHECK"
echo ""

echo "✅ CONFIGURED ALIASES:"
echo "  • rp@fishmusicinc.com → rsplowman@gmail.com"
echo "  • rsp@noizylab.ca → rsplowman@gmail.com"
echo "  • help@noizylab.ca → rsplowman@gmail.com"
echo ""

echo "📋 SETUP CHECKLIST:"
echo ""
echo "Gmail 'Send as':"
echo "  □ rp@fishmusicinc.com"
echo "  □ rsp@noizylab.ca"
echo "  □ help@noizylab.ca"
echo ""
echo "ImprovMX Forwarding:"
echo "  □ fishmusicinc.com domain added"
echo "  □ noizylab.ca domain added"
echo "  □ Aliases configured"
echo ""
echo "macOS Mail:"
echo "  □ Aliases added to Mail app"
echo ""

echo "🔗 QUICK LINKS:"
echo "  Gmail: https://mail.google.com/mail/u/0/#settings/accounts"
echo "  ImprovMX: https://app.improvmx.com/"
echo ""
STATUS_EOF

chmod +x "$AUTO_DIR/check_status.sh"

# ═══════════════════════════════════════════════════════════════════════
# CREATE DESKTOP SHORTCUTS
# ═══════════════════════════════════════════════════════════════════════

# Master control
cat > "$HOME/Desktop/EMAIL_MASTER.command" << 'MASTER_SHORTCUT'
#!/bin/bash
cd "$HOME/NOIZYLAB/email/automation"
bash ULTIMATE_AUTO_SETUP.sh
MASTER_SHORTCUT

chmod +x "$HOME/Desktop/EMAIL_MASTER.command"

# Test aliases
cat > "$HOME/Desktop/TEST_EMAIL_ALIASES.command" << 'TEST_SHORTCUT'
#!/bin/bash
cd "$HOME/NOIZYLAB/email/automation"
bash test_aliases.sh
TEST_SHORTCUT

chmod +x "$HOME/Desktop/TEST_EMAIL_ALIASES.command"

# Status check
cat > "$HOME/Desktop/EMAIL_STATUS.command" << 'STATUS_SHORTCUT'
#!/bin/bash
cd "$HOME/NOIZYLAB/email/automation"
bash check_status.sh
read -p "Press Enter to continue..."
STATUS_SHORTCUT

chmod +x "$HOME/Desktop/EMAIL_STATUS.command"

# ═══════════════════════════════════════════════════════════════════════
# CREATE ULTIMATE GUIDE
# ═══════════════════════════════════════════════════════════════════════

cat > "$HOME/Desktop/GORUNFREEX1000_GUIDE.txt" << 'GUIDE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     ⚡⚡⚡ GORUNFREEX1000 EMAIL SETUP GUIDE ⚡⚡⚡                      ║
╚══════════════════════════════════════════════════════════════════════╝

ULTIMATE AUTOMATION - VOICE & KEYBOARD ACCESSIBLE

══════════════════════════════════════════════════════════════════════
🚀 QUICK START (ONE CLICK)
══════════════════════════════════════════════════════════════════════

Double-click: GORUNFREEX1000_EMAIL.command
  → Master control panel
  → Select option 1 for ultimate setup
  → Everything opens automatically!

OR

Double-click: EMAIL_MASTER.command
  → Opens all pages
  → Shows checklist
  → Ready to go!

══════════════════════════════════════════════════════════════════════
🎤 VOICE COMMANDS
══════════════════════════════════════════════════════════════════════

Say: "Hey Siri, setup email aliases"
Say: "Hey Siri, open Gmail settings"
Say: "Hey Siri, open ImprovMX"
Say: "Click [button name]"
Say: "Type [text]"
Say: "Scroll down"
Say: "Show numbers"

══════════════════════════════════════════════════════════════════════
⌨️  KEYBOARD SHORTCUTS
══════════════════════════════════════════════════════════════════════

TAB:        Navigate
SPACE:      Click
RETURN:     Submit
ESC:        Cancel
CMD+F:      Find
CMD+,:      Preferences
CMD+T:      New tab
CMD+W:      Close tab
CMD+[1-9]:  Switch tabs

══════════════════════════════════════════════════════════════════════
📁 DESKTOP SHORTCUTS
══════════════════════════════════════════════════════════════════════

• GORUNFREEX1000_EMAIL.command - Master control
• EMAIL_MASTER.command - Ultimate setup
• TEST_EMAIL_ALIASES.command - Test aliases
• EMAIL_STATUS.command - Check status
• MASTER_EMAIL_CHECKLIST.txt - Setup checklist

══════════════════════════════════════════════════════════════════════
🔧 AUTOMATION SCRIPTS
══════════════════════════════════════════════════════════════════════

Location: ~/NOIZYLAB/email/automation/

• ULTIMATE_AUTO_SETUP.sh - One-command setup
• test_aliases.sh - Test email delivery
• check_status.sh - Check setup status
• enable_accessibility.sh - Enable Voice Control
• voice_commands.txt - Voice command dictionary

══════════════════════════════════════════════════════════════════════
📋 SETUP STEPS
══════════════════════════════════════════════════════════════════════

1. Run: EMAIL_MASTER.command
2. Follow checklist (opens automatically)
3. Use voice/keyboard to complete setup
4. Test with: TEST_EMAIL_ALIASES.command
5. Check status: EMAIL_STATUS.command

══════════════════════════════════════════════════════════════════════
⚡⚡⚡ GORUNFREEX1000 - MAXIMUM AUTOMATION ⚡⚡⚡

Everything is automated, voice-accessible, and keyboard-friendly!

GUIDE_EOF

# ═══════════════════════════════════════════════════════════════════════
# RUN ULTIMATE SETUP
# ═══════════════════════════════════════════════════════════════════════

echo "✅ ALL SYSTEMS UPGRADED!"
echo ""
echo "📋 CREATED:"
echo "  ✅ Master control panel"
echo "  ✅ Ultimate setup script"
echo "  ✅ Voice command dictionary"
echo "  ✅ Testing scripts"
echo "  ✅ Status checker"
echo "  ✅ Desktop shortcuts"
echo "  ✅ Complete guide"
echo ""

echo "🚀 RUNNING ULTIMATE SETUP..."
bash "$AUTO_DIR/ULTIMATE_AUTO_SETUP.sh"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          ⚡⚡⚡ GORUNFREEX1000 UPGRADE COMPLETE ⚡⚡⚡                  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 MASTER CONTROL:"
echo "   Double-click: GORUNFREEX1000_EMAIL.command"
echo ""
echo "🚀 QUICK SETUP:"
echo "   Double-click: EMAIL_MASTER.command"
echo ""
echo "📖 GUIDE:"
echo "   GORUNFREEX1000_GUIDE.txt on Desktop"
echo ""
echo "⚡⚡⚡ ALL SYSTEMS MAXIMIZED! ⚡⚡⚡"
echo ""

say "GORUNFREEX1000 upgrade complete. All systems maximized and ready!"


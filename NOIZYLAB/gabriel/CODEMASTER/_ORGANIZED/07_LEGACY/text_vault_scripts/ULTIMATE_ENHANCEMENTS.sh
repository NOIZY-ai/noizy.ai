#!/bin/bash
# ULTIMATE_ENHANCEMENTS.sh
# Additional enhancements for maximum automation

set -e

AUTO_DIR="$HOME/NOIZYLAB/email/automation"
mkdir -p "$AUTO_DIR"

echo "⚡ Adding Ultimate Enhancements..."
echo ""

# Create browser automation helper
cat > "$AUTO_DIR/browser_helper.applescript" << 'BROWSER_EOF'
-- Browser Automation Helper for Email Setup
on run argv
    set action to item 1 of argv
    
    if action is "gmail" then
        tell application "Safari"
            activate
            open location "https://mail.google.com/mail/u/0/#settings/accounts"
            delay 2
            tell application "System Events"
                keystroke "f" using {command down}
                delay 0.5
                keystroke "Send mail as"
                delay 0.5
                keystroke return
            end tell
        end tell
    else if action is "improvmx" then
        tell application "Safari"
            activate
            open location "https://app.improvmx.com/"
        end tell
    end if
end run
BROWSER_EOF

# Create quick action menu
cat > "$HOME/Desktop/EMAIL_QUICK_ACTIONS.command" << 'QUICK_EOF'
#!/bin/bash
# Quick Actions Menu

clear
echo "⚡ EMAIL QUICK ACTIONS"
echo ""
echo "1. Open Gmail Settings"
echo "2. Open ImprovMX"
echo "3. Test Aliases"
echo "4. Check Status"
echo "5. View Checklist"
echo ""

read -p "Choice (1-5): " choice

case $choice in
    1) open "https://mail.google.com/mail/u/0/#settings/accounts" ;;
    2) open "https://app.improvmx.com/" ;;
    3) bash "$HOME/NOIZYLAB/email/automation/test_aliases.sh" ;;
    4) bash "$HOME/NOIZYLAB/email/automation/check_status.sh" ;;
    5) open "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt" 2>/dev/null || cat "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt" ;;
esac
QUICK_EOF

chmod +x "$HOME/Desktop/EMAIL_QUICK_ACTIONS.command"

# Create status dashboard
cat > "$AUTO_DIR/status_dashboard.sh" << 'DASHBOARD_EOF'
#!/bin/bash
# Status Dashboard

clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     📊 EMAIL ALIASES STATUS DASHBOARD                                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📧 CONFIGURED ALIASES:"
echo "  ✅ rp@fishmusicinc.com → rsplowman@gmail.com"
echo "  ✅ rsp@noizylab.ca → rsplowman@gmail.com"
echo "  ✅ help@noizylab.ca → rsplowman@gmail.com"
echo ""

echo "🌐 DOMAINS:"
echo "  • fishmusicinc.com"
echo "  • noizylab.ca"
echo ""

echo "🔗 QUICK LINKS:"
echo "  Gmail: https://mail.google.com/mail/u/0/#settings/accounts"
echo "  ImprovMX: https://app.improvmx.com/"
echo ""

echo "📋 SETUP STATUS:"
echo "  Gmail 'Send as': Check manually"
echo "  ImprovMX: Check manually"
echo "  macOS Mail: Optional"
echo ""

echo "⚡ QUICK ACTIONS:"
echo "  Press 1: Open Gmail"
echo "  Press 2: Open ImprovMX"
echo "  Press 3: Test Aliases"
echo "  Press 4: View Checklist"
echo "  Press 0: Exit"
echo ""

read -p "👉 Action: " action

case $action in
    1) open "https://mail.google.com/mail/u/0/#settings/accounts" ;;
    2) open "https://app.improvmx.com/" ;;
    3) bash "$HOME/NOIZYLAB/email/automation/test_aliases.sh" ;;
    4) open "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt" 2>/dev/null || cat "$HOME/Desktop/MASTER_EMAIL_CHECKLIST.txt" ;;
    0) exit 0 ;;
esac
DASHBOARD_EOF

chmod +x "$AUTO_DIR/status_dashboard.sh"

# Create desktop shortcut for dashboard
cat > "$HOME/Desktop/EMAIL_DASHBOARD.command" << 'DASH_SHORTCUT'
#!/bin/bash
cd "$HOME/NOIZYLAB/email/automation"
bash status_dashboard.sh
DASH_SHORTCUT

chmod +x "$HOME/Desktop/EMAIL_DASHBOARD.command"

echo "✅ Ultimate enhancements added!"
echo "  • Browser automation"
echo "  • Quick actions menu"
echo "  • Status dashboard"
echo ""


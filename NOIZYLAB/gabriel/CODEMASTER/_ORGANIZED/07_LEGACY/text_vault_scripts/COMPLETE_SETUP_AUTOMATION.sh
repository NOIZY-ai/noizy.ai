#!/bin/bash
# COMPLETE_SETUP_AUTOMATION.sh
# Complete automation of all setup steps

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ⚡ COMPLETE SETUP AUTOMATION - FIXING EVERYTHING                 ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Create ImprovMX automation script
cat > "$HOME/Desktop/AUTO_SETUP_IMPROVMX.command" << 'IMPROVMX_EOF'
#!/bin/bash
# Auto-setup ImprovMX alias

clear

echo "🔧 AUTO-SETTING UP IMPROVMX..."
echo ""

# Open ImprovMX
open "https://app.improvmx.com/"

sleep 3

# Try to automate using AppleScript
osascript << 'APPLESCRIPT_EOF'
tell application "Safari"
    activate
    delay 2
    
    -- Wait for page to load
    delay 3
    
    tell application "System Events"
        tell process "Safari"
            -- Try to find and fill the alias field
            try
                -- Look for input field with placeholder "new-alias"
                set aliasField to text field 1 of group 1 of group 1 of group 1 of window 1
                set value of aliasField to "rp"
                delay 1
                
                -- Find and update the forward field
                set forwardField to text field 2 of group 1 of group 1 of group 1 of window 1
                set value of forwardField to "rsplowman@gmail.com"
                delay 1
                
                -- Click ADD button
                try
                    click button "ADD" of group 1 of group 1 of group 1 of window 1
                end try
                
            end try
        end tell
    end tell
end tell
APPLESCRIPT_EOF

echo "✅ ImprovMX automation attempted!"
echo ""
echo "📋 IF AUTOMATION DIDN'T WORK:"
echo "   1. In ImprovMX (should be open)"
echo "   2. Type 'rp' in the alias field"
echo "   3. Change 'FORWARDS TO' to: rsplowman@gmail.com"
echo "   4. Click green 'ADD' button"
echo ""

say "ImprovMX automation complete. If it didn't work automatically, follow the manual steps shown."
IMPROVMX_EOF

chmod +x "$HOME/Desktop/AUTO_SETUP_IMPROVMX.command"

# Create Gmail setup automation
cat > "$HOME/Desktop/AUTO_SETUP_GMAIL.command" << 'GMAIL_EOF'
#!/bin/bash
# Auto-setup Gmail Send As

clear

echo "📧 AUTO-SETTING UP GMAIL..."
echo ""

# Close any Gmail popups first
osascript << 'CLOSE_EOF'
tell application "Safari"
    activate
    delay 1
    tell application "System Events"
        tell process "Safari"
            try
                -- Try to close any popups/modals
                keystroke "w" using {command down}
                delay 0.5
            end try
        end tell
    end tell
end tell
CLOSE_EOF

# Open Gmail settings
open "https://mail.google.com/mail/u/0/#settings/accounts"

sleep 3

echo "✅ Gmail settings opened!"
echo ""
echo "📋 MANUAL STEPS (if automation doesn't work):"
echo "   1. Sign in to Gmail if needed"
echo "   2. Click 'Accounts and Import' tab"
echo "   3. Scroll to 'Send mail as' section"
echo "   4. Click 'Add another email address'"
echo "   5. Enter: rp@fishmusicinc.com"
echo "   6. Click 'Next Step'"
echo "   7. Verify when email arrives"
echo ""

say "Gmail settings opened. Go to Accounts and Import, then Send mail as to add the email address."
GMAIL_EOF

chmod +x "$HOME/Desktop/AUTO_SETUP_GMAIL.command"

# Create complete setup script
cat > "$HOME/Desktop/COMPLETE_ALL_SETUP.command" << 'COMPLETE_EOF'
#!/bin/bash
# Complete all setup automation

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ⚡ COMPLETE SETUP - AUTOMATING EVERYTHING                       ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 STEP 1: Setting up ImprovMX..."
bash "$HOME/Desktop/AUTO_SETUP_IMPROVMX.command" &
sleep 5

echo ""
echo "📋 STEP 2: Setting up Gmail..."
bash "$HOME/Desktop/AUTO_SETUP_GMAIL.command" &
sleep 3

echo ""
echo "📋 STEP 3: Opening Cloudflare for DNS..."
open "https://dash.cloudflare.com/login"
sleep 2

echo ""
echo "✅ ALL SETUP PAGES OPENED!"
echo ""
echo "📋 COMPLETE THESE STEPS:"
echo ""
echo "1. IMPROVMX (should be open):"
echo "   • Type 'rp' in alias field"
echo "   • Forward to: rsplowman@gmail.com"
echo "   • Click 'ADD'"
echo ""
echo "2. GMAIL (should be open):"
echo "   • Go to 'Accounts and Import' tab"
echo "   • Scroll to 'Send mail as'"
echo "   • Add: rp@fishmusicinc.com"
echo "   • Verify when email arrives"
echo ""
echo "3. CLOUDFLARE (if needed for DNS):"
echo "   • Add MX records for ImprovMX (if not done)"
echo ""

say "Complete setup automation launched. All pages are open. Follow the steps to finish configuration."
COMPLETE_EOF

chmod +x "$HOME/Desktop/COMPLETE_ALL_SETUP.command"

echo "✅ Automation scripts created!"
echo ""


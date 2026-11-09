#!/bin/bash
# FIX_GMAIL_LOOP.sh
# Fix Gmail redirect loop and open correct settings page

clear

echo "🔧 FIXING GMAIL LOOP..."
echo ""

# Close browsers first
osascript -e 'tell application "Safari" to quit' 2>/dev/null
osascript -e 'tell application "Chrome" to quit' 2>/dev/null
sleep 2

echo "✅ Browsers closed"
echo ""
echo "📋 OPENING GMAIL CORRECTLY..."
echo ""

# Open Gmail main page first (let it load)
open "https://mail.google.com/mail/u/0/"

sleep 3

echo "✅ Gmail main page opened"
echo ""
echo "📋 NOW DO THIS:"
echo ""
echo "1. Sign in to Gmail (if needed)"
echo "2. Wait for Gmail to fully load"
echo "3. Then click: Settings (gear icon) → See all settings"
echo "4. Or use this direct link after signing in:"
echo "   https://mail.google.com/mail/u/0/#settings/general"
echo ""

# Create alternative method
cat > "$HOME/Desktop/GMAIL_SETTINGS_DIRECT.command" << 'GMAIL_EOF'
#!/bin/bash
# Gmail Settings Direct Access

clear

echo "📧 OPENING GMAIL SETTINGS DIRECTLY..."
echo ""

# Try the direct settings URL
open "https://mail.google.com/mail/u/0/#settings/general"

sleep 2

echo "✅ Gmail settings page opened!"
echo ""
echo "📋 IF IT STILL LOOPS:"
echo "   1. Sign in to Gmail first: https://mail.google.com"
echo "   2. Wait for Gmail to fully load"
echo "   3. Then manually go to: Settings → See all settings"
echo "   4. Click 'Accounts and Import' tab"
echo ""

say "Gmail settings opened. If it loops, sign in to Gmail first, then go to settings."
GMAIL_EOF

chmod +x "$HOME/Desktop/GMAIL_SETTINGS_DIRECT.command"

echo "✅ GMAIL_SETTINGS_DIRECT.command created!"
echo ""
echo "📋 ALTERNATIVE METHOD:"
echo "   Double-click: GMAIL_SETTINGS_DIRECT.command"
echo ""

say "Gmail loop fix complete. Sign in to Gmail first, then access settings."


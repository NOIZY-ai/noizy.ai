#!/bin/bash
# CHECK_EXISTING_SETUP.sh
# Check what's already configured

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🔍 CHECKING EXISTING EMAIL SETUP                                 ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📧 Checking noizylab.ca setup..."
echo ""

# Check if domain is configured in various places
echo "🔍 CHECKING CONFIGURATIONS:"
echo ""

echo "1. Gmail 'Send as' aliases:"
echo "   → Check: https://mail.google.com/mail/u/0/#settings/accounts"
echo "   → Look for: rsp@noizylab.ca, help@noizylab.ca"
echo ""

echo "2. ImprovMX:"
echo "   → Check: https://app.improvmx.com/"
echo "   → Look for: noizylab.ca domain"
echo "   → Check aliases: rsp, help"
echo ""

echo "3. macOS Mail:"
if [ -f "$HOME/Library/Preferences/com.apple.mail.plist" ]; then
    echo "   ✅ Mail preferences found"
    echo "   → Check Mail → Preferences → Accounts → Email Addresses"
else
    echo "   ⚠️  Mail not configured yet"
fi
echo ""

echo "📋 WHAT TO CHECK:"
echo ""
echo "If noizylab.ca is already set up, verify:"
echo ""
echo "✅ Domain added in ImprovMX:"
echo "   • noizylab.ca should appear in domains list"
echo ""
echo "✅ Aliases configured:"
echo "   • rsp@noizylab.ca → rsplowman@gmail.com"
echo "   • help@noizylab.ca → rsplowman@gmail.com"
echo ""
echo "✅ Gmail 'Send as' configured:"
echo "   • rsp@noizylab.ca added"
echo "   • help@noizylab.ca added"
echo ""

echo "🔗 QUICK LINKS:"
echo "   ImprovMX: https://app.improvmx.com/"
echo "   Gmail: https://mail.google.com/mail/u/0/#settings/accounts"
echo ""

echo "🧪 TEST SETUP:"
echo "   Send test email TO: rsp@noizylab.ca"
echo "   Should arrive in: rsplowman@gmail.com"
echo ""

# Open ImprovMX to check
echo "📧 Opening ImprovMX to verify..."
open "https://app.improvmx.com/"

sleep 2

echo ""
echo "✅ ImprovMX opened - check your domains and aliases"
echo ""
echo "💡 If noizylab.ca is already there:"
echo "   1. Verify aliases are correct"
echo "   2. Check forwarding to rsplowman@gmail.com"
echo "   3. Test email delivery"
echo ""

say "Checking existing setup. ImprovMX opened for verification."


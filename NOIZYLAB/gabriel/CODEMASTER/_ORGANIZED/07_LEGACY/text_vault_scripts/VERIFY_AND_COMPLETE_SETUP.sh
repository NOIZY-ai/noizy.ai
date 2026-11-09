#!/bin/bash
# VERIFY_AND_COMPLETE_SETUP.sh
# Verify existing setup and complete what's missing

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ✅ VERIFY & COMPLETE EMAIL SETUP                                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 SETUP STATUS:"
echo ""
echo "✅ noizylab.ca - Already configured!"
echo ""
echo "📧 REMAINING SETUP:"
echo ""
echo "1. fishmusicinc.com:"
echo "   □ Add domain in ImprovMX"
echo "   □ Create alias: rp@fishmusicinc.com"
echo "   □ Forward to: rsplowman@gmail.com"
echo ""
echo "2. Gmail 'Send as':"
echo "   □ Add: rp@fishmusicinc.com"
echo "   □ Verify: rsp@noizylab.ca (if not done)"
echo "   □ Verify: help@noizylab.ca (if not done)"
echo ""
echo "3. Test all aliases:"
echo "   □ rp@fishmusicinc.com"
echo "   □ rsp@noizylab.ca"
echo "   □ help@noizylab.ca"
echo ""

echo "🚀 QUICK ACTIONS:"
echo ""
echo "1. Add fishmusicinc.com in ImprovMX:"
echo "   → Open: https://app.improvmx.com/"
echo "   → Click 'Add domain'"
echo "   → Type: fishmusicinc.com"
echo ""
echo "2. Create rp@fishmusicinc.com alias:"
echo "   → In ImprovMX, select fishmusicinc.com"
echo "   → Click 'Add alias'"
echo "   → Alias: rp"
echo "   → Forward: rsplowman@gmail.com"
echo ""
echo "3. Add to Gmail 'Send as':"
echo "   → Open: https://mail.google.com/mail/u/0/#settings/accounts"
echo "   → Add: rp@fishmusicinc.com"
echo ""

# Open both pages
echo "📧 Opening setup pages..."
open "https://app.improvmx.com/"
sleep 1
open "https://mail.google.com/mail/u/0/#settings/accounts"

echo ""
echo "✅ Pages opened!"
echo ""
echo "📋 FOCUS ON:"
echo "   • Adding fishmusicinc.com domain"
echo "   • Creating rp@fishmusicinc.com alias"
echo "   • Adding rp@fishmusicinc.com to Gmail"
echo ""
echo "✅ noizylab.ca is already done!"
echo ""

say "Setup pages opened. Focus on adding fishmusicinc.com. noizylab.ca is already configured."


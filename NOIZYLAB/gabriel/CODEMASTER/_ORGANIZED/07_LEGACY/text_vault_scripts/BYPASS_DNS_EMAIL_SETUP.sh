#!/bin/bash
# BYPASS_DNS_EMAIL_SETUP.sh
# Set up email aliases WITHOUT changing DNS/Cloudflare/GoDaddy
# Uses Gmail "Send as" + optional forwarding services

set -e

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     📧 BYPASS DNS - EMAIL ALIASES SETUP (No Cloudflare/GoDaddy)     ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

PRIMARY_EMAIL="rsplowman@gmail.com"
ALIASES=(
    "rp@fishmusicinc.com"
    "rsp@noizylab.ca"
    "help@noizylab.ca"
)

echo "📧 PRIMARY EMAIL: $PRIMARY_EMAIL"
echo ""
echo "📋 ALIASES TO SET UP (NO DNS CHANGES NEEDED):"
for alias in "${ALIASES[@]}"; do
    echo "   → $alias"
done
echo ""

# Create bypass setup guide
GUIDE="$HOME/Desktop/BYPASS_DNS_EMAIL_SETUP.txt"

cat > "$GUIDE" << EOF
╔══════════════════════════════════════════════════════════════════════╗
║     BYPASS DNS - EMAIL ALIASES SETUP                                ║
║     No Cloudflare/GoDaddy Changes Required                          ║
╚══════════════════════════════════════════════════════════════════════╝

PRIMARY EMAIL: $PRIMARY_EMAIL

ALIASES:
  • rp@fishmusicinc.com
  • rsp@noizylab.ca
  • help@noizylab.ca

══════════════════════════════════════════════════════════════════════
METHOD 1: GMAIL "SEND AS" (Easiest - Sending Only)
══════════════════════════════════════════════════════════════════════

✅ NO DNS CHANGES NEEDED
✅ NO CLOUDFLARE CHANGES
✅ NO GODADDY DNS CHANGES

STEPS:

1. Open Gmail Settings:
   → https://mail.google.com/mail/u/0/#settings/accounts
   OR
   → Gmail → Settings (gear) → See all settings → Accounts and Import

2. Scroll to "Send mail as" section

3. Click "Add another email address"

4. For each alias, enter:
   □ Name: (Your name)
   □ Email: rp@fishmusicinc.com
   □ Uncheck "Treat as an alias" (or leave checked)
   □ Click "Next Step"

5. Gmail will send verification email
   □ Check email at the alias address
   □ Click verification link
   □ Repeat for each alias

6. When sending emails:
   □ Click "From" dropdown in Gmail compose
   □ Select the alias you want
   □ Send email
   □ Recipient sees custom domain address

LIMITATIONS:
  ⚠️  Can SEND from custom addresses ✅
  ⚠️  Cannot RECEIVE at custom addresses ❌
  ⚠️  For receiving, see Method 2 below

══════════════════════════════════════════════════════════════════════
METHOD 2: IMPROVMX (Free - Sending + Receiving)
══════════════════════════════════════════════════════════════════════

✅ NO DNS CHANGES NEEDED
✅ FREE (up to 5 aliases)
✅ HANDLES SENDING + RECEIVING

WHAT IT DOES:
  • Provides email forwarding service
  • Handles MX records on their end
  • Forwards emails to your Gmail
  • No DNS changes needed on your side

STEPS:

1. Sign up for ImprovMX:
   → https://improvmx.com/
   → Free tier: Up to 5 aliases

2. Add your domains:
   □ Add: fishmusicinc.com
   □ Add: noizylab.ca
   □ Follow verification steps (usually just clicking a link)

3. Set up forwarding:
   □ Forward: rp@fishmusicinc.com → $PRIMARY_EMAIL
   □ Forward: rsp@noizylab.ca → $PRIMARY_EMAIL
   □ Forward: help@noizylab.ca → $PRIMARY_EMAIL

4. Configure Gmail "Send as":
   □ Follow Method 1 steps above
   □ Use ImprovMX SMTP settings if needed
   □ Or just use Gmail "Send as" (works with forwarding)

5. Test:
   □ Send email TO rp@fishmusicinc.com
   □ Should arrive in $PRIMARY_EMAIL inbox
   □ Send email FROM rp@fishmusicinc.com
   □ Should show custom domain as sender

ALTERNATIVE SERVICES:
  • ForwardMX (similar to ImprovMX)
  • Email forwarding services (various providers)

══════════════════════════════════════════════════════════════════════
METHOD 3: GODADDY EMAIL FORWARDING (If Available)
══════════════════════════════════════════════════════════════════════

✅ NO DNS CHANGES NEEDED
✅ USES GODADDY DASHBOARD ONLY

STEPS:

1. Log into GoDaddy:
   → https://www.godaddy.com/
   → My Products → Domains

2. Find email forwarding option:
   □ Go to domain settings
   □ Look for "Email" or "Email Forwarding"
   □ Some plans include basic forwarding

3. Set up forwarding:
   □ Forward: rp@fishmusicinc.com → $PRIMARY_EMAIL
   □ Forward: rsp@noizylab.ca → $PRIMARY_EMAIL
   □ Forward: help@noizylab.ca → $PRIMARY_EMAIL

4. Configure Gmail "Send as":
   □ Follow Method 1 steps
   □ Verify addresses via forwarded emails

NOTE: Not all GoDaddy plans include email forwarding.
      If not available, use Method 2 (ImprovMX).

══════════════════════════════════════════════════════════════════════
QUICK START (Recommended)
══════════════════════════════════════════════════════════════════════

FOR SENDING ONLY (5 minutes):
  1. Use Method 1 (Gmail "Send as")
  2. Verify via GoDaddy forwarding (if available)
  3. Done! ✅

FOR SENDING + RECEIVING (15 minutes):
  1. Sign up for ImprovMX (free)
  2. Add domains and set forwarding
  3. Configure Gmail "Send as"
  4. Done! ✅

══════════════════════════════════════════════════════════════════════
MACOS MAIL APP CONFIGURATION
══════════════════════════════════════════════════════════════════════

Once aliases are set up:

1. Add Gmail account:
   □ Mail → Preferences → Accounts
   □ Add: $PRIMARY_EMAIL

2. Configure "Send As":
   □ Select Gmail account
   □ Click "Email Address" → "Edit Email Addresses"
   □ Add: rp@fishmusicinc.com
   □ Add: rsp@noizylab.ca
   □ Add: help@noizylab.ca

3. When composing:
   □ Click "From" dropdown
   □ Select alias
   □ Send email

══════════════════════════════════════════════════════════════════════
QUICK LINKS
══════════════════════════════════════════════════════════════════════

Gmail Settings:
  https://mail.google.com/mail/u/0/#settings/accounts

ImprovMX (Free Email Forwarding):
  https://improvmx.com/

GoDaddy:
  https://www.godaddy.com/

══════════════════════════════════════════════════════════════════════
SUMMARY
══════════════════════════════════════════════════════════════════════

✅ YES - You can bypass Cloudflare & GoDaddy DNS changes!

OPTIONS:
  1. Gmail "Send as" → Sending only, no DNS changes
  2. ImprovMX → Sending + receiving, no DNS changes
  3. GoDaddy forwarding → If available, no DNS changes

RECOMMENDED:
  • Start with Gmail "Send as" (easiest)
  • Add ImprovMX if you need receiving
  • No DNS changes required! 🎉

══════════════════════════════════════════════════════════════════════

Created: $(date)
Primary Email: $PRIMARY_EMAIL

EOF

echo "✅ Bypass DNS setup guide created:"
echo "   $GUIDE"
echo ""
echo "🎯 RECOMMENDED APPROACH:"
echo ""
echo "1. QUICK START (Sending Only - 5 min):"
echo "   → Use Gmail 'Send as' feature"
echo "   → No DNS changes needed"
echo "   → Open: https://mail.google.com/mail/u/0/#settings/accounts"
echo ""
echo "2. FULL SETUP (Sending + Receiving - 15 min):"
echo "   → Sign up for ImprovMX (free)"
echo "   → Set up forwarding"
echo "   → Configure Gmail 'Send as'"
echo "   → No DNS changes needed"
echo ""
echo "📋 DETAILED GUIDE:"
echo "   → Open: $GUIDE"
echo ""
echo "💡 KEY POINT:"
echo "   You DON'T need to change DNS/Cloudflare/GoDaddy!"
echo "   Use Gmail 'Send as' + forwarding service instead"
echo ""

# Open the guide
open "$GUIDE" 2>/dev/null || echo "   (Open manually: $GUIDE)"

echo ""
echo "⚡⚡⚡ Bypass DNS setup ready ⚡⚡⚡"
echo ""


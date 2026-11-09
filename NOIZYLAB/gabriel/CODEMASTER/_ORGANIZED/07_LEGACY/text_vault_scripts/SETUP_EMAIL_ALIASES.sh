#!/bin/bash
# SETUP_EMAIL_ALIASES.sh
# Guide and checklist for setting up Google email aliases
# For: rsplowman@gmail.com

set -e

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          📧 GOOGLE EMAIL ALIASES SETUP                               ║"
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
echo "📋 ALIASES TO CONFIGURE:"
for alias in "${ALIASES[@]}"; do
    echo "   → $alias"
done
echo ""

# Create setup checklist
CHECKLIST="$HOME/Desktop/EMAIL_ALIASES_SETUP_CHECKLIST.txt"

cat > "$CHECKLIST" << EOF
╔══════════════════════════════════════════════════════════════════════╗
║          GOOGLE EMAIL ALIASES SETUP CHECKLIST                       ║
╚══════════════════════════════════════════════════════════════════════╝

PRIMARY EMAIL: $PRIMARY_EMAIL

ALIASES TO SET UP:
  □ rp@fishmusicinc.com
  □ rsp@noizylab.ca
  □ help@noizylab.ca

══════════════════════════════════════════════════════════════════════
OPTION 1: GOOGLE WORKSPACE (Recommended for Professional Use)
══════════════════════════════════════════════════════════════════════

REQUIREMENTS:
  □ Google Workspace account (~\$6-12/month)
  □ Domain ownership: fishmusicinc.com
  □ Domain ownership: noizylab.ca
  □ DNS access for MX record configuration

STEPS:
  1. Sign up: https://workspace.google.com/
     □ Use $PRIMARY_EMAIL as admin account
  
  2. Add domains in Google Admin Console:
     □ Go to: Admin Console → Domains
     □ Add: fishmusicinc.com
     □ Add: noizylab.ca
     □ Complete domain verification
  
  3. Configure DNS MX Records (at domain registrar):
     
     FOR fishmusicinc.com:
     □ MX Record: Priority 1 → ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 5 → ALT1.ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 5 → ALT2.ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 10 → ALT3.ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 10 → ALT4.ASPMX.L.GOOGLE.COM
     □ TXT Record: v=spf1 include:_spf.google.com ~all
     
     FOR noizylab.ca:
     □ MX Record: Priority 1 → ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 5 → ALT1.ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 5 → ALT2.ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 10 → ALT3.ASPMX.L.GOOGLE.COM
     □ MX Record: Priority 10 → ALT4.ASPMX.L.GOOGLE.COM
     □ TXT Record: v=spf1 include:_spf.google.com ~all
  
  4. Add email aliases in Google Admin:
     □ Go to: Users → Select your user → Email aliases
     □ Add: rp@fishmusicinc.com
     □ Add: rsp@noizylab.ca
     □ Add: help@noizylab.ca
  
  5. Test email delivery:
     □ Send test email to rp@fishmusicinc.com
     □ Send test email to rsp@noizylab.ca
     □ Send test email to help@noizylab.ca
     □ Verify emails arrive in $PRIMARY_EMAIL inbox

══════════════════════════════════════════════════════════════════════
OPTION 2: DOMAIN EMAIL FORWARDING (Free Alternative)
══════════════════════════════════════════════════════════════════════

REQUIREMENTS:
  □ Access to domain registrar DNS/email settings
  □ Email forwarding service (usually free with domain)

STEPS:
  1. Log into domain registrar:
     □ fishmusicinc.com registrar
     □ noizylab.ca registrar
  
  2. Set up email forwarding:
     □ Forward: rp@fishmusicinc.com → $PRIMARY_EMAIL
     □ Forward: rsp@noizylab.ca → $PRIMARY_EMAIL
     □ Forward: help@noizylab.ca → $PRIMARY_EMAIL
  
  3. Configure Gmail "Send mail as":
     □ Gmail → Settings → Accounts → "Send mail as"
     □ Add: rp@fishmusicinc.com
     □ Add: rsp@noizylab.ca
     □ Add: help@noizylab.ca
     □ Verify each via email confirmation
  
  4. Test:
     □ Send test email to each alias
     □ Verify forwarding works
     □ Test sending from Gmail using aliases

══════════════════════════════════════════════════════════════════════
OPTION 3: MACOS MAIL APP CONFIGURATION
══════════════════════════════════════════════════════════════════════

Once aliases are set up (via Workspace or forwarding):

  1. Add Gmail account to macOS Mail:
     □ Mail → Preferences → Accounts
     □ Add: $PRIMARY_EMAIL
  
  2. Configure "Send As" addresses:
     □ Select Gmail account
     □ Click "Email Address" → "Edit Email Addresses"
     □ Add: rp@fishmusicinc.com
     □ Add: rsp@noizylab.ca
     □ Add: help@noizylab.ca
  
  3. Test sending:
     □ Compose new email
     □ Select alias from "From" dropdown
     □ Send test email

══════════════════════════════════════════════════════════════════════
QUICK LINKS
══════════════════════════════════════════════════════════════════════

Google Workspace: https://workspace.google.com/
Google Admin Console: https://admin.google.com/
Gmail Settings: https://mail.google.com/mail/u/0/#settings/accounts

══════════════════════════════════════════════════════════════════════
COST COMPARISON
══════════════════════════════════════════════════════════════════════

Google Workspace:     ~\$6-12/month per user
Domain Forwarding:    FREE (usually included with domain)
Regular Gmail:        FREE (but cannot use custom domains)

══════════════════════════════════════════════════════════════════════
RECOMMENDATION
══════════════════════════════════════════════════════════════════════

For quick setup:      Use domain registrar's email forwarding (FREE)
For professional:     Google Workspace (paid, full control)

══════════════════════════════════════════════════════════════════════

Created: $(date)
Primary Email: $PRIMARY_EMAIL

EOF

echo "✅ Setup checklist created:"
echo "   $CHECKLIST"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Open the checklist:"
echo "   open $CHECKLIST"
echo ""
echo "2. Choose your approach:"
echo "   • Google Workspace (paid, professional)"
echo "   • Domain forwarding (free, simpler)"
echo ""
echo "3. Follow the checklist steps"
echo ""
echo "4. Test email delivery"
echo ""
echo "💡 TIP: Domain forwarding is FREE and works immediately!"
echo "   Google Workspace gives you more control but costs ~\$6-12/month"
echo ""
echo "📧 Need help? Check the detailed guide:"
echo "   SETUP_GOOGLE_EMAIL_ALIASES.md"
echo ""

# Open the checklist
open "$CHECKLIST" 2>/dev/null || echo "   (Open manually: $CHECKLIST)"

echo ""
echo "⚡⚡⚡ Setup guide ready ⚡⚡⚡"
echo ""


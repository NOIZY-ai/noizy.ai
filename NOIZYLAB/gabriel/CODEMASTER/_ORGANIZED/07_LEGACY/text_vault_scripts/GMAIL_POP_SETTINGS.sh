#!/bin/bash
# GMAIL_POP_SETTINGS.sh
# Gmail POP settings information

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     📧 GMAIL POP SETTINGS - PROPER USERNAME                          ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

cat > "$HOME/Desktop/GMAIL_POP_SETTINGS.txt" << 'POP_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📧 GMAIL POP SETTINGS - COMPLETE GUIDE                          ║
╚══════════════════════════════════════════════════════════════════════╝

PROPER POP USERNAME:
────────────────────

✅ POP Username: rsplowman@gmail.com
   (Your FULL Gmail address - this is the correct username)

✅ POP Password: Your Gmail password
   (Or App Password if 2FA is enabled)

══════════════════════════════════════════════════════════════════════

COMPLETE GMAIL POP SETTINGS:
────────────────────────────

Incoming Mail (POP):
  • Server: pop.gmail.com
  • Port: 995
  • Username: rsplowman@gmail.com ✅
  • Password: Your Gmail password
  • Use SSL: Yes ✅
  • Authentication: Password

Outgoing Mail (SMTP):
  • Server: smtp.gmail.com
  • Port: 587 (TLS) or 465 (SSL)
  • Username: rsplowman@gmail.com ✅
  • Password: Your Gmail password
  • Use TLS/SSL: Yes ✅

══════════════════════════════════════════════════════════════════════

FOR YOUR EMAIL ALIASES:
───────────────────────

rp@fishmusicinc.com
rsp@noizylab.ca
help@noizylab.ca

These are FORWARDED to rsplowman@gmail.com through ImprovMX.

They don't have separate POP settings - all emails come into:
  ✅ rsplowman@gmail.com

So use: rsplowman@gmail.com as the POP username for all.

══════════════════════════════════════════════════════════════════════

IF YOU HAVE 2-FACTOR AUTHENTICATION:
────────────────────────────────────

You need an "App Password" instead of your regular password:

1. Go to: https://myaccount.google.com/apppasswords
2. Generate an App Password for "Mail"
3. Use that App Password instead of your regular password

══════════════════════════════════════════════════════════════════════

QUICK ANSWER:
─────────────

POP Username: rsplowman@gmail.com ✅

══════════════════════════════════════════════════════════════════════
POP_EOF

open "$HOME/Desktop/GMAIL_POP_SETTINGS.txt"

echo "✅ GMAIL_POP_SETTINGS.txt created and opened!"
echo ""
echo "📧 PROPER POP USERNAME:"
echo "   ✅ rsplowman@gmail.com"
echo ""
echo "📋 COMPLETE SETTINGS:"
echo "   • POP Server: pop.gmail.com"
echo "   • POP Port: 995"
echo "   • POP Username: rsplowman@gmail.com ✅"
echo "   • Use SSL: Yes"
echo ""
echo "✅ Guide opened on desktop!"


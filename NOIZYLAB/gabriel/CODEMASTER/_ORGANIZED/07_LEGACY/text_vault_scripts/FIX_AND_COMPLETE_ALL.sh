#!/bin/bash
# FIX_AND_COMPLETE_ALL.sh
# Fix all issues and complete setup

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🔧 FIXING ALL & COMPLETING SETUP                               ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Close all browser windows to clear loops
echo "📋 STEP 1: Closing all browsers to clear loops..."
osascript -e 'tell application "Safari" to quit' 2>/dev/null
osascript -e 'tell application "Chrome" to quit' 2>/dev/null
sleep 2
echo "✅ Browsers closed"
echo ""

# Create comprehensive setup guide
cat > "$HOME/Desktop/COMPLETE_SETUP_NOW.txt" << 'SETUP_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     ✅ COMPLETE SETUP - FINAL STEPS                                 ║
╚══════════════════════════════════════════════════════════════════════╝

DO THESE STEPS IN ORDER:

══════════════════════════════════════════════════════════════════════

STEP 1: SET UP IMPROVMX (5 minutes)
────────────────────────────────────

1. Open: https://app.improvmx.com/
2. Sign in if needed
3. Find "fishmusicinc.com" domain
4. In the alias input field, type: rp
   (Delete "new-alias" and type "rp")
5. In "FORWARDS TO" field, change to: rsplowman@gmail.com
   (Change from rsplowman@icloud.com)
6. Click green "ADD" button
7. Wait for confirmation

✅ DONE when you see: "rp@fishmusicinc.com → rsplowman@gmail.com"

══════════════════════════════════════════════════════════════════════

STEP 2: SET UP GMAIL "SEND AS" (5 minutes)
──────────────────────────────────────────

1. Open: https://mail.google.com
2. Sign in to Gmail
3. Click Settings gear icon (top right)
4. Click "See all settings"
5. Click "Accounts and Import" tab
6. Scroll to "Send mail as" section
7. Click "Add another email address"
8. Enter:
   • Name: (Your name)
   • Email: rp@fishmusicinc.com
9. Click "Next Step"
10. Gmail will send verification email
    → This arrives at rsplowman@gmail.com (via ImprovMX)
11. Check your Gmail inbox
12. Click verification link in the email
13. Done! ✅

✅ DONE when rp@fishmusicinc.com appears in "Send mail as" list

══════════════════════════════════════════════════════════════════════

STEP 3: SET UP OTHER ALIASES (if needed)
─────────────────────────────────────────

For rsp@noizylab.ca and help@noizylab.ca:

1. In ImprovMX, add more aliases:
   • rsp → rsplowman@gmail.com
   • help → rsplowman@gmail.com

2. In Gmail "Send mail as", add:
   • rsp@noizylab.ca
   • help@noizylab.ca

3. Verify each one

══════════════════════════════════════════════════════════════════════

STEP 4: CLOUDFLARE DNS (if needed)
───────────────────────────────────

If ImprovMX says "Email forwarding needs setup":

1. Open: https://dash.cloudflare.com/login
2. Select fishmusicinc.com domain
3. Go to DNS settings
4. Add MX records (ImprovMX will show you what to add)
5. Add SPF record if needed

══════════════════════════════════════════════════════════════════════

IMPORTANT NOTES:
────────────────

❌ DON'T use Gmail "Import mail" (POP) - ImprovMX doesn't have POP!
✅ DO use Gmail "Send mail as" - This is the correct method!

How it works:
• ImprovMX FORWARDS emails TO you (automatic)
• Gmail "Send as" lets you SEND FROM the alias

══════════════════════════════════════════════════════════════════════
SETUP_EOF

open "$HOME/Desktop/COMPLETE_SETUP_NOW.txt"

# Open all necessary pages
echo "📋 STEP 2: Opening all setup pages..."
open "https://app.improvmx.com/"
sleep 2
open "https://mail.google.com"
sleep 2
open "https://dash.cloudflare.com/login"
sleep 1

echo "✅ All pages opened!"
echo ""

# Create quick reference
cat > "$HOME/Desktop/QUICK_REFERENCE.txt" << 'REF_EOF'
QUICK REFERENCE:

ImprovMX:
• Alias: rp
• Forward to: rsplowman@gmail.com

Gmail:
• Use "Send mail as" (NOT POP import)
• Add: rp@fishmusicinc.com

That's it!
REF_EOF

echo "✅ Complete setup guide created!"
echo ""
echo "📋 WHAT TO DO NOW:"
echo "   1. Follow COMPLETE_SETUP_NOW.txt (opened)"
echo "   2. Set up ImprovMX first (Step 1)"
echo "   3. Then set up Gmail (Step 2)"
echo "   4. Done!"
echo ""

say "Complete setup guide created. All pages are open. Follow the steps in Complete Setup Now to finish everything."


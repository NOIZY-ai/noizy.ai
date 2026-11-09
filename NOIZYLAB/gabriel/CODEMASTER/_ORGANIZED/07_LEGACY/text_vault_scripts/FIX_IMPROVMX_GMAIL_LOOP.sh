#!/bin/bash
# FIX_IMPROVMX_GMAIL_LOOP.sh
# Fix the ImprovMX + Gmail loop issue

clear

cat > "$HOME/Desktop/FIX_LOOP_NOW.txt" << 'FIX_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🔧 FIX GMAIL LOOP - IMPROVMX SETUP                              ║
╚══════════════════════════════════════════════════════════════════════╝

❌ PROBLEM:
───────────
Gmail is trying to use POP import for rp@fishmusicinc.com
But ImprovMX doesn't provide POP - it only FORWARDS emails!

This causes a loop because:
• Gmail can't find a POP server for rp@fishmusicinc.com
• ImprovMX forwards emails, doesn't provide POP access
• You're trying to import instead of forward

══════════════════════════════════════════════════════════════════════

✅ SOLUTION - DO THIS IN ORDER:
────────────────────────────────

STEP 1: SET UP IMPROVMX FIRST (Do this now!)
─────────────────────────────────────────────

In ImprovMX (should be open):

1. In the alias input field, type: rp
   (NOT "new-alias" - type "rp")

2. The field should show: rp@fishmusicinc.com

3. In the "FORWARDS TO" field, change it to:
   rsplowman@gmail.com
   (NOT rsplowman@icloud.com)

4. Click the green "ADD" button

5. Wait for it to save

══════════════════════════════════════════════════════════════════════

STEP 2: CANCEL GMAIL POP IMPORT
───────────────────────────────

In Gmail (the popup that's looping):

1. Click "Cancel" button
   (Don't try to set up POP import!)

2. Close that popup/window

══════════════════════════════════════════════════════════════════════

STEP 3: USE GMAIL "SEND AS" (NOT POP IMPORT)
───────────────────────────────────────────

After ImprovMX is set up:

1. In Gmail, go to: Settings → Accounts and Import

2. Scroll to "Send mail as" section

3. Click "Add another email address"

4. Enter:
   • Name: (Your name)
   • Email: rp@fishmusicinc.com

5. Click "Next Step"

6. Gmail will send verification email
   → This will arrive at rsplowman@gmail.com (via ImprovMX forwarding)

7. Click the verification link in the email

8. Done! ✅

══════════════════════════════════════════════════════════════════════

HOW IT WORKS:
─────────────

✅ ImprovMX forwards emails TO you:
   rp@fishmusicinc.com → rsplowman@gmail.com
   (Emails arrive automatically at your Gmail)

✅ Gmail "Send as" lets you SEND from:
   You can send emails "as" rp@fishmusicinc.com
   (Recipients see rp@fishmusicinc.com as sender)

❌ DON'T use POP import - ImprovMX doesn't provide POP!

══════════════════════════════════════════════════════════════════════

QUICK FIX CHECKLIST:
────────────────────

□ 1. In ImprovMX: Add alias "rp" → forwards to "rsplowman@gmail.com"
□ 2. In Gmail: Click "Cancel" on POP import popup
□ 3. In Gmail: Use "Send mail as" (not POP import)
□ 4. Verify email address when Gmail sends it

══════════════════════════════════════════════════════════════════════
FIX_EOF

open "$HOME/Desktop/FIX_LOOP_NOW.txt"

echo "✅ FIX_LOOP_NOW.txt created and opened!"
echo ""
echo "📋 QUICK FIX:"
echo ""
echo "1. In ImprovMX:"
echo "   • Type 'rp' in alias field (not 'new-alias')"
echo "   • Change 'FORWARDS TO' to: rsplowman@gmail.com"
echo "   • Click 'ADD'"
echo ""
echo "2. In Gmail:"
echo "   • Click 'Cancel' on the POP import popup"
echo "   • Don't use POP import - use 'Send mail as' instead"
echo ""
echo "3. Then in Gmail Settings:"
echo "   • Go to 'Send mail as' section"
echo "   • Add rp@fishmusicinc.com"
echo "   • Verify when email arrives"
echo ""

say "Fix guide created. Set up the alias in ImprovMX first. Type rp and forward to rsplowman at gmail dot com. Then cancel the Gmail pop import and use send mail as instead."


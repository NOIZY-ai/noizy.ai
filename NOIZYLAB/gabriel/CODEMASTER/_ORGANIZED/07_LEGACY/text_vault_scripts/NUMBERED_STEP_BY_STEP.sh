#!/bin/bash
# NUMBERED_STEP_BY_STEP.sh
# Super simple numbered guide

clear

cat > "$HOME/Desktop/NUMBERED_GUIDE.txt" << 'NUMBERED_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📋 NUMBERED GUIDE - EXACTLY WHERE TO PUT INFO                    ║
╚══════════════════════════════════════════════════════════════════════╝

PAGE 1: CLOUDFLARE
═══════════════════

STEP 1: Click on "fishmusicinc.com"
   → Look for your domain name
   → Click on it

STEP 2: Click "DNS" (on the left side)
   → Look for "DNS" in the left menu
   → Click it

STEP 3: Click "Add record" button
   → Top right of the page
   → Big button that says "Add record"

STEP 4: In the form that appears:
   
   Field 1: "Type" dropdown
   → Click the dropdown
   → Select "MX"
   
   Field 2: "Name" (might be blank or say "fishmusicinc.com")
   → Leave it as is OR type: fishmusicinc.com
   
   Field 3: "Mail server"
   → Type exactly: mx1.improvmx.com
   
   Field 4: "Priority"
   → Type exactly: 10
   
   Field 5: "Proxy" (orange cloud toggle)
   → Make sure it's OFF (gray, not orange)
   
   Field 6: "Save" button
   → Click "Save"

STEP 5: Click "Add record" again
   → Same button as before

STEP 6: Fill the form again:
   
   Field 1: "Type" → Select "MX"
   
   Field 2: "Name" → Leave as is
   
   Field 3: "Mail server"
   → Type exactly: mx2.improvmx.com
   
   Field 4: "Priority"
   → Type exactly: 20
   
   Field 5: "Proxy" → Make sure OFF (gray)
   
   Field 6: "Save" button → Click "Save"

✅ DONE WITH CLOUDFLARE!

══════════════════════════════════════════════════════════════════════

PAGE 2: IMPROVMX
════════════════

STEP 7: Find "fishmusicinc.com" on the page
   → Look for your domain name

STEP 8: Find the input field that says "new-alias"
   → It's in a row with "@fishmusicinc.com" next to it
   → Click in that field

STEP 9: Type in that field:
   → Delete "new-alias" if it's there
   → Type exactly: rp

STEP 10: Find the field that says "FORWARDS TO"
   → It's in the same row
   → It might say "rsplowman@icloud.com"
   → Click in that field

STEP 11: Change that field:
   → Delete what's there
   → Type exactly: rsplowman@gmail.com

STEP 12: Find the green "ADD" button
   → It's on the right side of that row
   → Click it

✅ DONE WITH IMPROVMX!

Wait 5-10 minutes, then:

STEP 13: Find the "CHECK AGAIN" button
   → Click it
   → Should say "Email forwarding is active" ✅

══════════════════════════════════════════════════════════════════════

PAGE 3: GMAIL
══════════════

STEP 14: Sign in to Gmail (if needed)
   → Use your email: rsplowman@gmail.com
   → Enter your password

STEP 15: Find the Settings gear icon
   → Top right of Gmail
   → Looks like a gear/cog
   → Click it

STEP 16: Click "See all settings"
   → In the menu that appears
   → Click it

STEP 17: Click "Accounts and Import" tab
   → Top of the settings page
   → Click that tab

STEP 18: Scroll down to "Send mail as" section
   → Look for "Send mail as"
   → It's in the middle of the page

STEP 19: Click "Add another email address"
   → Next to "Send mail as"
   → Click that link

STEP 20: In the popup that appears:
   
   Field 1: "Name"
   → Type your name (or leave as is)
   
   Field 2: "Email address"
   → Type exactly: rp@fishmusicinc.com
   
   Field 3: "Next Step" button
   → Click it

STEP 21: Gmail will send a verification email
   → Check your Gmail inbox
   → Look for email from Gmail
   → Click the verification link in that email

✅ DONE WITH GMAIL!

══════════════════════════════════════════════════════════════════════

THAT'S IT! 21 STEPS TOTAL.

TAKE YOUR TIME. ONE STEP AT A TIME.

══════════════════════════════════════════════════════════════════════
NUMBERED_EOF

open "$HOME/Desktop/NUMBERED_GUIDE.txt"

echo "✅ NUMBERED_GUIDE.txt created and opened!"
echo ""
echo "📋 SUPER SIMPLE NUMBERED GUIDE:"
echo "   ✅ 21 steps total"
echo "   ✅ Exact field numbers"
echo "   ✅ Exact page locations"
echo "   ✅ Exactly what to type"
echo ""

say "Numbered guide created. Twenty one simple steps with exact field numbers and page locations. Follow it step by step."


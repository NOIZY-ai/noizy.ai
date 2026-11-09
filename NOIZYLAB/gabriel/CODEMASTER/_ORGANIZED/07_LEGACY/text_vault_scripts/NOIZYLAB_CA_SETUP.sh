#!/bin/bash
# NOIZYLAB_CA_SETUP.sh
# Setup guide for noizylab.ca

clear

cat > "$HOME/Desktop/NOIZYLAB_CA_GUIDE.txt" << 'NOIZYLAB_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📋 NOIZYLAB.CA SETUP - NUMBERED GUIDE                            ║
╚══════════════════════════════════════════════════════════════════════╝

PAGE 1: CLOUDFLARE - NOIZYLAB.CA
══════════════════════════════════

STEP 1: Click on "noizylab.ca" domain
   → Look for "noizylab.ca" in Cloudflare
   → Click on it

STEP 2: Click "DNS" (on the left side)
   → Look for "DNS" in the left menu
   → Click it

STEP 3: Check if MX records exist
   → Look for records with Type "MX"
   → If you see mx1.improvmx.com and mx2.improvmx.com → Already done! ✅
   → If not, continue to Step 4

STEP 4: Click "Add record" button
   → Top right of the page
   → Big button that says "Add record"

STEP 5: In the form that appears:
   
   Field 1: "Type" dropdown
   → Click the dropdown
   → Select "MX"
   
   Field 2: "Name" (might be blank or say "noizylab.ca")
   → Leave it as is OR type: noizylab.ca
   
   Field 3: "Mail server"
   → Type exactly: mx1.improvmx.com
   
   Field 4: "Priority"
   → Type exactly: 10
   
   Field 5: "Proxy" (orange cloud toggle)
   → Make sure it's OFF (gray, not orange)
   
   Field 6: "Save" button
   → Click "Save"

STEP 6: Click "Add record" again
   → Same button as before

STEP 7: Fill the form again:
   
   Field 1: "Type" → Select "MX"
   
   Field 2: "Name" → Leave as is
   
   Field 3: "Mail server"
   → Type exactly: mx2.improvmx.com
   
   Field 4: "Priority"
   → Type exactly: 20
   
   Field 5: "Proxy" → Make sure OFF (gray)
   
   Field 6: "Save" button → Click "Save"

✅ DONE WITH CLOUDFLARE FOR NOIZYLAB.CA!

══════════════════════════════════════════════════════════════════════

PAGE 2: IMPROVMX - NOIZYLAB.CA
═══════════════════════════════

STEP 8: Go to ImprovMX: https://app.improvmx.com/

STEP 9: Find "noizylab.ca" on the page
   → Look for your domain name

STEP 10: Check if aliases exist
   → Look for: rsp@noizylab.ca
   → Look for: help@noizylab.ca
   → If they exist → Already done! ✅
   → If not, continue to Step 11

STEP 11: Add "rsp" alias
   → Find the input field that says "new-alias"
   → Click in that field
   → Delete "new-alias" if it's there
   → Type exactly: rsp
   → Find "FORWARDS TO" field
   → Type exactly: rsplowman@gmail.com
   → Click green "ADD" button

STEP 12: Add "help" alias
   → Click "Add record" or find another alias field
   → Type exactly: help
   → Forward to: rsplowman@gmail.com
   → Click green "ADD" button

✅ DONE WITH IMPROVMX FOR NOIZYLAB.CA!

Wait 5-10 minutes, then:

STEP 13: Find the "CHECK AGAIN" button
   → Click it
   → Should say "Email forwarding is active" ✅

══════════════════════════════════════════════════════════════════════

PAGE 3: GMAIL - NOIZYLAB.CA ALIASES
═════════════════════════════════════

STEP 14: Go to Gmail: https://mail.google.com
   → Sign in if needed

STEP 15: Click Settings gear icon (top right)
   → Click it

STEP 16: Click "See all settings"
   → In the menu

STEP 17: Click "Accounts and Import" tab
   → Top of settings page

STEP 18: Scroll to "Send mail as" section

STEP 19: Add "rsp@noizylab.ca"
   → Click "Add another email address"
   → Type: rsp@noizylab.ca
   → Click "Next Step"
   → Verify email when it arrives

STEP 20: Add "help@noizylab.ca"
   → Click "Add another email address" again
   → Type: help@noizylab.ca
   → Click "Next Step"
   → Verify email when it arrives

✅ DONE WITH GMAIL FOR NOIZYLAB.CA!

══════════════════════════════════════════════════════════════════════

SUMMARY FOR NOIZYLAB.CA:
─────────────────────────

✅ MX Records: mx1.improvmx.com and mx2.improvmx.com
✅ Aliases: rsp@noizylab.ca and help@noizylab.ca
✅ Forward to: rsplowman@gmail.com
✅ Gmail "Send as": rsp@noizylab.ca and help@noizylab.ca

══════════════════════════════════════════════════════════════════════
NOIZYLAB_EOF

open "$HOME/Desktop/NOIZYLAB_CA_GUIDE.txt"

echo "✅ NOIZYLAB_CA_GUIDE.txt created and opened!"
echo ""
echo "📋 NOIZYLAB.CA SETUP GUIDE:"
echo "   ✅ 20 steps total"
echo "   ✅ Cloudflare DNS setup"
echo "   ✅ ImprovMX aliases (rsp and help)"
echo "   ✅ Gmail Send as setup"
echo ""

say "Noizylab dot CA setup guide created. Follow the twenty steps to set up email forwarding for noizylab dot CA. Start with Cloudflare DNS, then ImprovMX, then Gmail."


#!/bin/bash
# SLOW_STEP_BY_STEP.sh
# Very slow, simple step-by-step guide

clear

cat > "$HOME/Desktop/STEP_BY_STEP_SLOW.txt" << 'SLOW_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🐢 SLOW STEP-BY-STEP GUIDE                                       ║
╚══════════════════════════════════════════════════════════════════════╝

TAKE YOUR TIME. ONE STEP AT A TIME.

══════════════════════════════════════════════════════════════════════

STEP 1: ADD FIRST MX RECORD
────────────────────────────

1. Look at your Cloudflare DNS page

2. Find the button that says "Add record"
   → It's usually at the top right of the table

3. Click "Add record"

4. A form will appear

5. Find the dropdown that says "Type"
   → Click on it
   → Select "MX"

6. Find the field that says "Name"
   → Type: fishmusicinc.com
   → OR leave it blank

7. Find the field that says "Mail server"
   → Type: mx1.improvmx.com

8. Find the field that says "Priority"
   → Type: 10

9. Find the "Proxy" toggle (orange cloud)
   → Make sure it's OFF (gray, not orange)
   → This is VERY important!

10. Click the "Save" button

✅ DONE! First MX record added!

══════════════════════════════════════════════════════════════════════

STEP 2: ADD SECOND MX RECORD
──────────────────────────────

1. Click "Add record" again

2. Select "MX" from the Type dropdown

3. Name: fishmusicinc.com (or leave blank)

4. Mail server: mx2.improvmx.com

5. Priority: 20

6. Proxy: OFF (gray, not orange)

7. Click "Save"

✅ DONE! Second MX record added!

══════════════════════════════════════════════════════════════════════

STEP 3: WAIT
────────────

Wait 5 minutes.

Go get a drink. Come back.

══════════════════════════════════════════════════════════════════════

STEP 4: CHECK IN IMPROVMX
──────────────────────────

1. Go to: https://app.improvmx.com/

2. Find your domain: fishmusicinc.com

3. Look for a button that says "CHECK AGAIN"

4. Click "CHECK AGAIN"

5. It should now say: "Email forwarding is active" ✅

══════════════════════════════════════════════════════════════════════

THAT'S IT FOR NOW!

You can add other records later if needed.

For now, just these 2 MX records are enough.

══════════════════════════════════════════════════════════════════════
SLOW_EOF

open "$HOME/Desktop/STEP_BY_STEP_SLOW.txt"

echo "✅ STEP_BY_STEP_SLOW.txt created and opened!"
echo ""
echo "📋 SUPER SLOW GUIDE:"
echo ""
echo "STEP 1: Add first MX record"
echo "   • Click 'Add record'"
echo "   • Type: MX"
echo "   • Mail server: mx1.improvmx.com"
echo "   • Priority: 10"
echo "   • Proxy: OFF (gray)"
echo "   • Save"
echo ""
echo "STEP 2: Add second MX record"
echo "   • Click 'Add record' again"
echo "   • Type: MX"
echo "   • Mail server: mx2.improvmx.com"
echo "   • Priority: 20"
echo "   • Proxy: OFF (gray)"
echo "   • Save"
echo ""
echo "STEP 3: Wait 5 minutes"
echo ""
echo "STEP 4: Check in ImprovMX"
echo "   • Click 'CHECK AGAIN'"
echo ""
echo "That's it! Just 2 records."
echo ""

say "Slow step by step guide created. Take your time. Add one MX record at a time. Make sure the proxy is off. Then wait and check in ImprovMX."


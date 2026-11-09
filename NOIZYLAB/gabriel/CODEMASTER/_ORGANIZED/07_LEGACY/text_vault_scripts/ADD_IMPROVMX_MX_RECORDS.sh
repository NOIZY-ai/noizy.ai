#!/bin/bash
# ADD_IMPROVMX_MX_RECORDS.sh
# Add ImprovMX MX records to Cloudflare

clear

cat > "$HOME/Desktop/ADD_MX_RECORDS_NOW.txt" << 'MX_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     ✅ ADD IMPROVMX MX RECORDS - STEP BY STEP                        ║
╚══════════════════════════════════════════════════════════════════════╝

✅ GOOD NEWS:
─────────────
Google MX records are deleted! Now add ImprovMX records.

══════════════════════════════════════════════════════════════════════

STEP 1: ADD FIRST MX RECORD
────────────────────────────

1. In Cloudflare DNS page, click "Add record" button
   (Usually at the top right of the DNS records table)

2. Select record type: "MX"

3. Fill in the fields:
   • Name: fishmusicinc.com (or just leave blank/@)
   • Mail server: mx1.improvmx.com
   • Priority: 10
   • TTL: Auto (or leave default)
   • Proxy status: DNS only (not Proxied)

4. Click "Save"

══════════════════════════════════════════════════════════════════════

STEP 2: ADD SECOND MX RECORD
─────────────────────────────

1. Click "Add record" again

2. Select record type: "MX"

3. Fill in the fields:
   • Name: fishmusicinc.com (or just leave blank/@)
   • Mail server: mx2.improvmx.com
   • Priority: 20
   • TTL: Auto (or leave default)
   • Proxy status: DNS only (not Proxied)

4. Click "Save"

══════════════════════════════════════════════════════════════════════

STEP 3: UPDATE SPF RECORD (Optional but recommended)
──────────────────────────────────────────────────────

1. Find the TXT record for fishmusicinc.com
   (The one with: "v=spf1 include:_spf.webad...")

2. Click "Edit" on that record

3. Change the content to:
   "v=spf1 include:spf.improvmx.com ~all"

   OR if you want to keep Google too:
   "v=spf1 include:spf.improvmx.com include:_netblocks.google.com ~all"

4. Click "Save"

══════════════════════════════════════════════════════════════════════

FINAL RESULT:
─────────────

You should now have:
✅ mx1.improvmx.com (Priority 10)
✅ mx2.improvmx.com (Priority 20)

And NO Google MX records.

══════════════════════════════════════════════════════════════════════

AFTER ADDING MX RECORDS:
─────────────────────────

1. Wait 5-10 minutes for DNS to propagate

2. Go to ImprovMX: https://app.improvmx.com/

3. Click "CHECK AGAIN" button

4. It should now say: "Email forwarding is active" ✅

══════════════════════════════════════════════════════════════════════

IMPORTANT NOTES:
────────────────

• Make sure Proxy status is "DNS only" (not Proxied)
• MX records must be DNS only, not proxied
• Priority 10 is higher priority than 20
• Both MX records are needed for redundancy

══════════════════════════════════════════════════════════════════════
MX_EOF

open "$HOME/Desktop/ADD_MX_RECORDS_NOW.txt"

echo "✅ ADD_MX_RECORDS_NOW.txt created and opened!"
echo ""
echo "📋 ADD THESE 2 MX RECORDS:"
echo ""
echo "Record 1:"
echo "   • Type: MX"
echo "   • Name: fishmusicinc.com (or blank)"
echo "   • Mail server: mx1.improvmx.com"
echo "   • Priority: 10"
echo "   • Proxy: DNS only (NOT Proxied)"
echo ""
echo "Record 2:"
echo "   • Type: MX"
echo "   • Name: fishmusicinc.com (or blank)"
echo "   • Mail server: mx2.improvmx.com"
echo "   • Priority: 20"
echo "   • Proxy: DNS only (NOT Proxied)"
echo ""
echo "✅ Then wait 5-10 minutes and click 'CHECK AGAIN' in ImprovMX"
echo ""

say "Add ImprovMX MX records guide created. Add two MX records - mx1 dot ImprovMX dot com with priority 10, and mx2 dot ImprovMX dot com with priority 20. Make sure they are DNS only, not proxied."


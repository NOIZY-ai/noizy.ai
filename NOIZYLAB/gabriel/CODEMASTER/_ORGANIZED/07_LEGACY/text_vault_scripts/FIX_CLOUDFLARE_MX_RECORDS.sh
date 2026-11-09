#!/bin/bash
# FIX_CLOUDFLARE_MX_RECORDS.sh
# Fix MX records for ImprovMX

clear

cat > "$HOME/Desktop/FIX_MX_RECORDS.txt" << 'MX_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🔧 FIX CLOUDFLARE MX RECORDS FOR IMPROVMX                       ║
╚══════════════════════════════════════════════════════════════════════╝

❌ PROBLEM FOUND:
─────────────────

Your MX records are pointing to Google:
• ASPMX.L.GOOGLE.com
• ALT1.ASPMX.L.GOOGLE.com
• etc.

But you need them to point to ImprovMX for email forwarding to work!

══════════════════════════════════════════════════════════════════════

✅ SOLUTION - CHANGE MX RECORDS:
────────────────────────────────

STEP 1: DELETE OLD GOOGLE MX RECORDS
─────────────────────────────────────

In Cloudflare DNS settings:

1. Delete ALL 5 Google MX records:
   ❌ Priority 1: ASPMX.L.GOOGLE.com
   ❌ Priority 5: ALT1.ASPMX.L.GOOGLE.com
   ❌ Priority 5: ALT2.ASPMX.L.GOOGLE.com
   ❌ Priority 10: ALT3.ASPMX.L.GOOGLE.com
   ❌ Priority 10: ALT4.ASPMX.L.GOOGLE.com

2. Click "Delete" on each one

══════════════════════════════════════════════════════════════════════

STEP 2: ADD IMPROVMX MX RECORDS
────────────────────────────────

Add these 2 MX records for ImprovMX:

Record 1:
• Type: MX
• Name: fishmusicinc.com (or @)
• Priority: 10
• Mail server: mx1.improvmx.com
• TTL: Auto (or 300)

Record 2:
• Type: MX
• Name: fishmusicinc.com (or @)
• Priority: 20
• Mail server: mx2.improvmx.com
• TTL: Auto (or 300)

Click "Save" after adding each one.

══════════════════════════════════════════════════════════════════════

STEP 3: UPDATE SPF RECORD (TXT)
───────────────────────────────

Your current SPF record:
"v=spf1 include:_spf.webador.com include:_netblocks.google.com include:_netblocks2.google.com include:_netblocks3.google.com -all"

Change it to (for ImprovMX):
"v=spf1 include:spf.improvmx.com ~all"

Or keep Google if you want both:
"v=spf1 include:spf.improvmx.com include:_netblocks.google.com ~all"

══════════════════════════════════════════════════════════════════════

FINAL MX RECORDS SHOULD BE:
────────────────────────────

✅ Priority 10: mx1.improvmx.com
✅ Priority 20: mx2.improvmx.com

That's it! Only 2 MX records for ImprovMX.

══════════════════════════════════════════════════════════════════════

HOW TO DO IT IN CLOUDFLARE:
───────────────────────────

1. Go to: https://dash.cloudflare.com
2. Select: fishmusicinc.com domain
3. Click: "DNS" in left sidebar
4. Find all MX records
5. Delete each Google MX record (click trash icon)
6. Click "Add record"
7. Select "MX" type
8. Add mx1.improvmx.com (Priority 10)
9. Click "Add record" again
10. Add mx2.improvmx.com (Priority 20)
11. Update TXT record SPF if needed
12. Done! ✅

══════════════════════════════════════════════════════════════════════

IMPORTANT:
──────────

• DNS changes can take 5-30 minutes to propagate
• After changing MX records, wait a few minutes
• Then go back to ImprovMX and click "CHECK AGAIN"
• It should now say "Email forwarding is active" ✅

══════════════════════════════════════════════════════════════════════
MX_EOF

open "$HOME/Desktop/FIX_MX_RECORDS.txt"

# Open Cloudflare
open "https://dash.cloudflare.com/login"

sleep 2

echo "✅ FIX_MX_RECORDS.txt created and opened!"
echo "✅ Cloudflare opened!"
echo ""
echo "📋 QUICK FIX:"
echo ""
echo "1. In Cloudflare DNS:"
echo "   • Delete ALL 5 Google MX records"
echo "   • Add: mx1.improvmx.com (Priority 10)"
echo "   • Add: mx2.improvmx.com (Priority 20)"
echo ""
echo "2. Update SPF TXT record:"
echo "   • Change to: v=spf1 include:spf.improvmx.com ~all"
echo ""
echo "3. Wait 5-10 minutes for DNS to update"
echo ""
echo "4. In ImprovMX, click 'CHECK AGAIN'"
echo "   • Should now say 'Email forwarding is active' ✅"
echo ""

say "MX records fix guide created. Your MX records are pointing to Google but need to point to ImprovMX. Delete the Google MX records and add ImprovMX MX records instead."


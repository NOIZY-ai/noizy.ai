#!/bin/bash
# CLOUDFLARE_QUICK_SETUP.sh
# Quick setup guide for Cloudflare

clear

cat > "$HOME/Desktop/CLOUDFLARE_DO_THIS.txt" << 'CLOUDFLARE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     ⚡ CLOUDFLARE - DO THIS NOW                                      ║
╚══════════════════════════════════════════════════════════════════════╝

STEP 1: GO TO DNS SETTINGS
───────────────────────────

1. Click on "fishmusicinc.com" domain
2. Click "DNS" in the left sidebar
3. You'll see all your DNS records

══════════════════════════════════════════════════════════════════════

STEP 2: DELETE THESE (if they're still there)
───────────────────────────────────────────────

1. _autodiscover._tcp
   → Click checkbox → Delete

2. mandrill._domainkey
   → Click checkbox → Delete

3. * (wildcard - the star)
   → Click checkbox on all 4 → Delete

══════════════════════════════════════════════════════════════════════

STEP 3: ADD IMPROVMX MX RECORDS
────────────────────────────────

1. Click "Add record" button (top right)

2. FIRST MX RECORD:
   • Type: MX
   • Name: fishmusicinc.com (or leave blank)
   • Mail server: mx1.improvmx.com
   • Priority: 10
   • Proxy: DNS only (turn OFF the orange cloud)
   • Click "Save"

3. Click "Add record" again

4. SECOND MX RECORD:
   • Type: MX
   • Name: fishmusicinc.com (or leave blank)
   • Mail server: mx2.improvmx.com
   • Priority: 20
   • Proxy: DNS only (turn OFF the orange cloud)
   • Click "Save"

══════════════════════════════════════════════════════════════════════

STEP 4: UPDATE SPF RECORD
──────────────────────────

1. Find the TXT record for fishmusicinc.com
   (The one with "v=spf1" in it)

2. Click "Edit" on that record

3. Change the content to:
   "v=spf1 include:spf.improvmx.com ~all"

   OR if you want to keep webador:
   "v=spf1 include:spf.improvmx.com include:_spf.webador.com ~all"

4. Click "Save"

══════════════════════════════════════════════════════════════════════

DONE! ✅
───────

Wait 5-10 minutes, then go to ImprovMX and click "CHECK AGAIN"

══════════════════════════════════════════════════════════════════════
CLOUDFLARE_EOF

open "$HOME/Desktop/CLOUDFLARE_DO_THIS.txt"

echo "✅ CLOUDFLARE_DO_THIS.txt created and opened!"
echo "✅ Cloudflare dashboard opened!"
echo ""
echo "📋 QUICK STEPS:"
echo "   1. Click on fishmusicinc.com domain"
echo "   2. Click 'DNS' in left sidebar"
echo "   3. Delete: _autodiscover, mandrill, * (wildcard)"
echo "   4. Add 2 MX records: mx1.improvmx.com and mx2.improvmx.com"
echo "   5. Update SPF TXT record"
echo ""

say "Cloudflare dashboard opened. Click on your domain, then DNS, then follow the steps to add ImprovMX MX records."


#!/bin/bash
# ADD_BACK_ESSENTIAL_RECORDS.sh
# Add back essential DNS records

clear

cat > "$HOME/Desktop/ADD_BACK_RECORDS.txt" << 'ADD_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     ✅ ADD BACK ESSENTIAL RECORDS                                    ║
╚══════════════════════════════════════════════════════════════════════╝

YOU NEED TO ADD THESE RECORDS BACK:

══════════════════════════════════════════════════════════════════════

STEP 1: ADD IMPROVMX MX RECORDS (MOST IMPORTANT!)
───────────────────────────────────────────────────

1. Click "Add record" button

2. FIRST MX RECORD:
   • Type: MX
   • Name: fishmusicinc.com (or leave blank/@)
   • Mail server: mx1.improvmx.com
   • Priority: 10
   • TTL: Auto
   • Proxy: DNS only (turn OFF orange cloud!)
   • Click "Save"

3. Click "Add record" again

4. SECOND MX RECORD:
   • Type: MX
   • Name: fishmusicinc.com (or leave blank/@)
   • Mail server: mx2.improvmx.com
   • Priority: 20
   • TTL: Auto
   • Proxy: DNS only (turn OFF orange cloud!)
   • Click "Save"

══════════════════════════════════════════════════════════════════════

STEP 2: ADD BACK A RECORDS (if deleted)
─────────────────────────────────────────

If you deleted the A records, add them back:

1. Click "Add record"
   • Type: A
   • Name: fishmusicinc.com (or @)
   • IPv4: 104.21.16.164
   • Proxy: Proxied (orange cloud ON)
   • Click "Save"

2. Click "Add record" again
   • Type: A
   • Name: fishmusicinc.com (or @)
   • IPv4: 172.67.214.218
   • Proxy: Proxied (orange cloud ON)
   • Click "Save"

3. Click "Add record" for www
   • Type: A
   • Name: www
   • IPv4: 104.21.16.164
   • Proxy: Proxied (orange cloud ON)
   • Click "Save"

4. Click "Add record" again for www
   • Type: A
   • Name: www
   • IPv4: 172.67.214.218
   • Proxy: Proxied (orange cloud ON)
   • Click "Save"

══════════════════════════════════════════════════════════════════════

STEP 3: ADD SPF TXT RECORD
───────────────────────────

1. Click "Add record"
   • Type: TXT
   • Name: fishmusicinc.com (or @)
   • Content: "v=spf1 include:spf.improvmx.com ~all"
   • TTL: Auto
   • Proxy: DNS only (turn OFF orange cloud)
   • Click "Save"

══════════════════════════════════════════════════════════════════════

STEP 4: ADD DMARC TXT RECORD (Optional but recommended)
────────────────────────────────────────────────────────

1. Click "Add record"
   • Type: TXT
   • Name: _dmarc
   • Content: "v=DMARC1; p=none"
   • TTL: Auto
   • Proxy: DNS only (turn OFF orange cloud)
   • Click "Save"

══════════════════════════════════════════════════════════════════════

PRIORITY ORDER:
───────────────

1. ✅ ADD MX RECORDS FIRST (most important!)
2. ✅ ADD A RECORDS (if deleted)
3. ✅ ADD SPF TXT RECORD
4. ✅ ADD DMARC (optional)

══════════════════════════════════════════════════════════════════════

AFTER ADDING:
──────────────

1. Wait 5-10 minutes
2. Go to ImprovMX
3. Click "CHECK AGAIN"
4. Should say "Email forwarding is active" ✅

══════════════════════════════════════════════════════════════════════
ADD_EOF

open "$HOME/Desktop/ADD_BACK_RECORDS.txt"

echo "✅ ADD_BACK_RECORDS.txt created and opened!"
echo ""
echo "📋 MOST IMPORTANT - ADD THESE FIRST:"
echo ""
echo "1. MX RECORDS (for email):"
echo "   • mx1.improvmx.com (Priority 10, DNS only)"
echo "   • mx2.improvmx.com (Priority 20, DNS only)"
echo ""
echo "2. A RECORDS (if deleted):"
echo "   • fishmusicinc.com → 104.21.16.164 (Proxied)"
echo "   • fishmusicinc.com → 172.67.214.218 (Proxied)"
echo "   • www → 104.21.16.164 (Proxied)"
echo "   • www → 172.67.214.218 (Proxied)"
echo ""
echo "3. SPF TXT RECORD:"
echo "   • fishmusicinc.com → v=spf1 include:spf.improvmx.com ~all"
echo ""
echo "📋 GUIDE OPENED: ADD_BACK_RECORDS.txt"
echo ""

say "Add back essential records guide created. Most important - add the two ImprovMX MX records first. Then add back A records if you deleted them. Then add SPF record."


#!/bin/bash
# IPV4_ADDRESS_GUIDE.sh
# Guide for IPv4 addresses in Cloudflare

clear

cat > "$HOME/Desktop/IPV4_ADDRESS_INFO.txt" << 'IPV4_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📍 IPv4 ADDRESS GUIDE FOR CLOUDFLARE                            ║
╚══════════════════════════════════════════════════════════════════════╝

FOR IMPROVMX EMAIL SETUP:
─────────────────────────

✅ YOU DON'T NEED TO CHANGE A RECORDS!

Your current A records are fine:
• 172.67.214.218
• 104.21.16.164

These are Cloudflare IPs - keep them as they are!

══════════════════════════════════════════════════════════════════════

WHAT YOU NEED TO CHANGE:
─────────────────────────

ONLY CHANGE MX RECORDS (not A records):

❌ DELETE these MX records:
   • ASPMX.L.GOOGLE.com
   • ALT1.ASPMX.L.GOOGLE.com
   • ALT2.ASPMX.L.GOOGLE.com
   • ALT3.ASPMX.L.GOOGLE.com
   • ALT4.ASPMX.L.GOOGLE.com

✅ ADD these MX records (no IPv4 needed):
   • mx1.improvmx.com (Priority 10)
   • mx2.improvmx.com (Priority 20)

══════════════════════════════════════════════════════════════════════

IF YOU'RE ADDING A NEW A RECORD:
─────────────────────────────────

For the main domain (fishmusicinc.com):
• Keep existing: 172.67.214.218 and 104.21.16.164
• These are Cloudflare's IPs - don't change them!

For a subdomain (like mail.fishmusicinc.com):
• You might need ImprovMX's IP, but usually you don't need A records
• ImprovMX uses MX records, not A records

══════════════════════════════════════════════════════════════════════

YOUR CURRENT A RECORDS (KEEP THESE):
─────────────────────────────────────

fishmusicinc.com → 172.67.214.218 ✅
fishmusicinc.com → 104.21.16.164 ✅

These are correct - don't change them!

══════════════════════════════════════════════════════════════════════

QUICK ANSWER:
─────────────

If Cloudflare is asking for IPv4 address:
• For main domain: Use 172.67.214.218 or 104.21.16.164 (you already have these)
• For email setup: You DON'T need A records - only MX records!
• For ImprovMX: Use MX records (mx1.improvmx.com, mx2.improvmx.com)

══════════════════════════════════════════════════════════════════════

WHAT TO DO:
───────────

1. DON'T change A records - they're fine!
2. ONLY change MX records (delete Google, add ImprovMX)
3. Update SPF TXT record if needed
4. That's it!

══════════════════════════════════════════════════════════════════════
IPV4_EOF

open "$HOME/Desktop/IPV4_ADDRESS_INFO.txt"

echo "✅ IPV4_ADDRESS_INFO.txt created and opened!"
echo ""
echo "📋 QUICK ANSWER:"
echo ""
echo "For ImprovMX email setup:"
echo "   ✅ You DON'T need to change A records"
echo "   ✅ Keep your existing A records as they are"
echo "   ✅ Only change MX records (delete Google, add ImprovMX)"
echo ""
echo "Your current A records are correct:"
echo "   • 172.67.214.218"
echo "   • 104.21.16.164"
echo ""
echo "If Cloudflare is asking for IPv4 address:"
echo "   • You're probably adding a new record"
echo "   • For email setup, you only need MX records (no A records)"
echo ""

say "IPv4 address guide created. For ImprovMX email setup, you don't need to change A records. Only change MX records. Your current A records are correct."


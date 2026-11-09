#!/bin/bash
# ANALYZE_DNS_RECORDS.sh
# Analyze what DNS records can be deleted

clear

cat > "$HOME/Desktop/DNS_CLEANUP_GUIDE.txt" << 'CLEANUP_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🧹 DNS RECORDS CLEANUP - WHAT TO DELETE                          ║
╚══════════════════════════════════════════════════════════════════════╝

YOUR CURRENT DNS RECORDS ANALYSIS:
──────────────────────────────────

══════════════════════════════════════════════════════════════════════

A RECORDS (IPv4) - KEEP THESE:
───────────────────────────────

✅ KEEP:
   • fishmusicinc.com → 104.21.16.164 (Proxied)
   • fishmusicinc.com → 172.67.214.218 (Proxied)
   • www → 104.21.16.164 (Proxied)
   • www → 172.67.214.218 (Proxied)

❓ OPTIONAL - CAN DELETE:
   • * (wildcard) → 104.21.16.164 (Proxied)
   • * (wildcard) → 172.67.214.218 (Proxied)
   
   → Only delete wildcard if you don't need subdomain catch-all

══════════════════════════════════════════════════════════════════════

AAAA RECORDS (IPv6) - KEEP THESE:
───────────────────────────────────

✅ KEEP:
   • fishmusicinc.com → IPv6 addresses (Proxied)
   • www → IPv6 addresses (Proxied)

❓ OPTIONAL - CAN DELETE:
   • * (wildcard) → IPv6 addresses (Proxied)
   
   → Only delete wildcard if you don't need subdomain catch-all

══════════════════════════════════════════════════════════════════════

SRV RECORD - CAN DELETE:
─────────────────────────

❌ DELETE THIS:
   • _autodiscover._tcp → autoconfig.mail...
   
   → This is for Microsoft/Outlook autodiscover
   → Not needed if you're using ImprovMX/Gmail
   → Safe to delete

══════════════════════════════════════════════════════════════════════

TXT RECORDS - REVIEW THESE:
────────────────────────────

1. _dmarc → "v=DMARC1; p=none"
   ❓ KEEP if you want DMARC (email security)
   ❌ DELETE if you don't need it
   → Safe to delete, but recommended to keep

2. fishmusicinc.com → "v=spf1 include:_spf.webad..."
   ⚠️  UPDATE THIS (don't delete):
   → Change to: "v=spf1 include:spf.improvmx.com ~all"
   → Or keep both: "v=spf1 include:spf.improvmx.com include:_spf.webador.com ~all"

3. mandrill._domainkey → "v=DKIM1; k=rsa; p=MIGf..."
   ❓ KEEP if you use Mandrill (email service)
   ❌ DELETE if you don't use Mandrill
   → Safe to delete if not using Mandrill

══════════════════════════════════════════════════════════════════════

RECOMMENDED CLEANUP:
────────────────────

SAFE TO DELETE:
✅ _autodiscover._tcp SRV record (not needed)
✅ mandrill._domainkey TXT record (if not using Mandrill)
✅ * (wildcard) A records (if not needed)
✅ * (wildcard) AAAA records (if not needed)

KEEP:
✅ All fishmusicinc.com A records
✅ All www A records
✅ All fishmusicinc.com AAAA records
✅ All www AAAA records
✅ _dmarc TXT record (recommended)
✅ fishmusicinc.com SPF TXT record (UPDATE it, don't delete)

══════════════════════════════════════════════════════════════════════

WHAT TO DO:
───────────

1. DELETE:
   • _autodiscover._tcp SRV record
   • mandrill._domainkey TXT record (if not using Mandrill)
   • * (wildcard) A/AAAA records (if not needed)

2. UPDATE:
   • fishmusicinc.com SPF TXT record (add ImprovMX)

3. KEEP:
   • All main domain A/AAAA records
   • _dmarc TXT record

══════════════════════════════════════════════════════════════════════

QUICK CLEANUP CHECKLIST:
────────────────────────

□ Delete _autodiscover._tcp SRV record
□ Delete mandrill._domainkey TXT record (if not using Mandrill)
□ Delete * wildcard A records (if not needed)
□ Delete * wildcard AAAA records (if not needed)
□ Update SPF TXT record (add ImprovMX)
□ Keep all main domain records
□ Keep _dmarc TXT record

══════════════════════════════════════════════════════════════════════
CLEANUP_EOF

open "$HOME/Desktop/DNS_CLEANUP_GUIDE.txt"

echo "✅ DNS_CLEANUP_GUIDE.txt created and opened!"
echo ""
echo "📋 SAFE TO DELETE:"
echo ""
echo "1. _autodiscover._tcp SRV record"
echo "   → Not needed for ImprovMX/Gmail"
echo ""
echo "2. mandrill._domainkey TXT record"
echo "   → Only if you don't use Mandrill email service"
echo ""
echo "3. * (wildcard) A/AAAA records"
echo "   → Only if you don't need subdomain catch-all"
echo ""
echo "📋 UPDATE (don't delete):"
echo "   • fishmusicinc.com SPF TXT record"
echo "   → Add ImprovMX: include:spf.improvmx.com"
echo ""
echo "📋 KEEP:"
echo "   • All fishmusicinc.com A/AAAA records"
echo "   • All www A/AAAA records"
echo "   • _dmarc TXT record (recommended)"
echo ""

say "DNS cleanup guide created. Safe to delete autodiscover SRV record, Mandrill DKIM record if not using it, and wildcard records if not needed. Keep all main domain records."


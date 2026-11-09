#!/bin/bash
# ============================================================================
# FIX FISHMUSICINC.COM EMAIL - M365 Business Setup
# ============================================================================
# Run this AFTER setting up M365 Business and getting verification codes
# ============================================================================

# Cloudflare API credentials (set these or use environment variables)
CF_API_TOKEN="${CF_API_TOKEN:-your_cloudflare_api_token}"
CF_ZONE_ID="${CF_ZONE_ID:-your_zone_id_for_fishmusicinc}"

DOMAIN="fishmusicinc.com"

echo "════════════════════════════════════════════════════════════════"
echo "  FISHMUSICINC.COM EMAIL FIX - M365 BUSINESS SETUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Function to add/update DNS record via Cloudflare API
update_dns() {
    local type=$1
    local name=$2
    local content=$3
    local priority=$4

    echo "📝 Setting $type record: $name → $content"

    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records" \
        -H "Authorization: Bearer ${CF_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --data "{
            \"type\": \"$type\",
            \"name\": \"$name\",
            \"content\": \"$content\",
            \"ttl\": 3600,
            \"priority\": $priority
        }"
    echo ""
}

# ============================================================================
# STEP 1: M365 Domain Verification TXT Record
# ============================================================================
echo ""
echo "STEP 1: Add M365 Verification TXT Record"
echo "─────────────────────────────────────────"
echo "Get the MS=msXXXXXXXX code from M365 Admin Center"
read -p "Enter MS verification code (e.g., MS=ms12345678): " MS_CODE

if [ -n "$MS_CODE" ]; then
    update_dns "TXT" "$DOMAIN" "$MS_CODE" 0
    echo "✅ Verification TXT record added"
fi

# ============================================================================
# STEP 2: Delete Old MX Records (Cloudflare Email Routing)
# ============================================================================
echo ""
echo "STEP 2: Remove Old Cloudflare Email Routing MX Records"
echo "─────────────────────────────────────────────────────────"
echo "⚠️  Go to Cloudflare Dashboard → DNS → Delete these MX records:"
echo "   - route1.mx.cloudflare.net"
echo "   - route2.mx.cloudflare.net"
echo "   - route3.mx.cloudflare.net"
echo ""
read -p "Press Enter after deleting old MX records..."

# ============================================================================
# STEP 3: Add M365 MX Record
# ============================================================================
echo ""
echo "STEP 3: Add M365 MX Record"
echo "──────────────────────────"
# M365 MX record format: fishmusicinc-com.mail.protection.outlook.com
MX_HOST="fishmusicinc-com.mail.protection.outlook.com"
update_dns "MX" "$DOMAIN" "$MX_HOST" 0

# ============================================================================
# STEP 4: Update SPF Record for M365
# ============================================================================
echo ""
echo "STEP 4: Update SPF Record"
echo "─────────────────────────"
# First delete old SPF, then add new
SPF_RECORD="v=spf1 include:spf.protection.outlook.com -all"
echo "📝 New SPF: $SPF_RECORD"
echo "⚠️  Delete old SPF record in Cloudflare Dashboard first"
read -p "Press Enter after deleting old SPF..."
update_dns "TXT" "$DOMAIN" "$SPF_RECORD" 0

# ============================================================================
# STEP 5: Add Autodiscover CNAME (for Outlook auto-config)
# ============================================================================
echo ""
echo "STEP 5: Add Autodiscover CNAME"
echo "───────────────────────────────"
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" \
    --data '{
        "type": "CNAME",
        "name": "autodiscover",
        "content": "autodiscover.outlook.com",
        "ttl": 3600,
        "proxied": false
    }'
echo ""

# ============================================================================
# STEP 6: DKIM Setup (After M365 enables it)
# ============================================================================
echo ""
echo "STEP 6: DKIM Setup"
echo "──────────────────"
echo "After M365 domain verification:"
echo "1. Go to: https://security.microsoft.com/dkimv2"
echo "2. Select fishmusicinc.com"
echo "3. Click 'Create DKIM keys'"
echo "4. Add the two CNAME records M365 provides:"
echo ""
echo "   selector1._domainkey → selector1-fishmusicinc-com._domainkey.YOUR_TENANT.onmicrosoft.com"
echo "   selector2._domainkey → selector2-fishmusicinc-com._domainkey.YOUR_TENANT.onmicrosoft.com"
echo ""

# ============================================================================
# STEP 7: DMARC Record
# ============================================================================
echo ""
echo "STEP 7: Add DMARC Record"
echo "────────────────────────"
DMARC_RECORD="v=DMARC1; p=quarantine; rua=mailto:rp@fishmusicinc.com; ruf=mailto:rp@fishmusicinc.com; fo=1"
update_dns "TXT" "_dmarc.$DOMAIN" "$DMARC_RECORD" 0

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  SETUP COMPLETE - VERIFICATION CHECKLIST"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ M365 verification TXT record added"
echo "✅ MX record → M365"
echo "✅ SPF updated for M365"
echo "✅ Autodiscover CNAME added"
echo "⏳ DKIM - Add CNAME records from M365 Security Center"
echo "✅ DMARC record added"
echo ""
echo "NEXT STEPS:"
echo "1. Wait 5-10 minutes for DNS propagation"
echo "2. Complete domain verification in M365 Admin Center"
echo "3. Create mailboxes: rp@fishmusicinc.com, info@fishmusicinc.com"
echo "4. Enable DKIM in M365 Security Center"
echo "5. Test sending/receiving email"
echo ""
echo "TEST COMMANDS:"
echo "  dig fishmusicinc.com MX +short"
echo "  dig fishmusicinc.com TXT +short"
echo "  dig _dmarc.fishmusicinc.com TXT +short"
echo ""
echo "════════════════════════════════════════════════════════════════"

#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# NOIZY DNS AUTHORITY AUDIT — Run on GOD
# Exports NS, MX, WHOIS, and SPF/DKIM for all 5 domains
# ═══════════════════════════════════════════════════════════
set -euo pipefail

REPORT_DIR="${HOME}/noizy_dns_audit/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

DOMAINS=("noizy.ai" "noizylab.ca" "noizyfish.com" "fishmusicinc.com" "noizylab.com")

echo "╔══════════════════════════════════════════════════════╗"
echo "║  NOIZY DNS AUTHORITY AUDIT                           ║"
echo "║  Auditing ${#DOMAINS[@]} domains                     ║"
echo "║  Report: $REPORT_DIR                                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# CSV header
echo "domain,ns1,ns2,mx1,mx_priority,registrar,status,expiry,spf,dmarc" > "$REPORT_DIR/dns_audit.csv"

for domain in "${DOMAINS[@]}"; do
  echo "=== $domain ==="
  DOMAIN_DIR="$REPORT_DIR/$domain"
  mkdir -p "$DOMAIN_DIR"

  # Nameservers
  echo "  NS records..."
  dig NS "$domain" +short > "$DOMAIN_DIR/ns.txt" 2>/dev/null || echo "LOOKUP_FAILED" > "$DOMAIN_DIR/ns.txt"
  NS1=$(head -1 "$DOMAIN_DIR/ns.txt" | tr -d '.')
  NS2=$(sed -n '2p' "$DOMAIN_DIR/ns.txt" | tr -d '.')
  echo "    NS1: $NS1"
  echo "    NS2: $NS2"

  # MX records
  echo "  MX records..."
  dig MX "$domain" +short > "$DOMAIN_DIR/mx.txt" 2>/dev/null || echo "LOOKUP_FAILED" > "$DOMAIN_DIR/mx.txt"
  MX1=$(head -1 "$DOMAIN_DIR/mx.txt" | awk '{print $2}' | tr -d '.')
  MX_PRI=$(head -1 "$DOMAIN_DIR/mx.txt" | awk '{print $1}')
  echo "    MX: $MX_PRI $MX1"

  # A record
  echo "  A record..."
  dig A "$domain" +short > "$DOMAIN_DIR/a.txt" 2>/dev/null || echo "LOOKUP_FAILED" > "$DOMAIN_DIR/a.txt"

  # SPF
  echo "  SPF record..."
  dig TXT "$domain" +short | grep "v=spf1" > "$DOMAIN_DIR/spf.txt" 2>/dev/null || echo "NONE" > "$DOMAIN_DIR/spf.txt"
  SPF=$(head -1 "$DOMAIN_DIR/spf.txt")

  # DMARC
  echo "  DMARC record..."
  dig TXT "_dmarc.$domain" +short > "$DOMAIN_DIR/dmarc.txt" 2>/dev/null || echo "NONE" > "$DOMAIN_DIR/dmarc.txt"
  DMARC=$(head -1 "$DOMAIN_DIR/dmarc.txt")

  # DKIM (common selectors)
  echo "  DKIM records..."
  for selector in google default selector1 selector2; do
    dig TXT "${selector}._domainkey.$domain" +short >> "$DOMAIN_DIR/dkim.txt" 2>/dev/null || true
  done

  # WHOIS
  echo "  WHOIS lookup..."
  whois "$domain" > "$DOMAIN_DIR/whois.txt" 2>/dev/null || echo "WHOIS_FAILED" > "$DOMAIN_DIR/whois.txt"
  REGISTRAR=$(grep -i "Registrar:" "$DOMAIN_DIR/whois.txt" | head -1 | sed 's/.*Registrar: *//' || echo "UNKNOWN")
  STATUS=$(grep -i "Domain Status:" "$DOMAIN_DIR/whois.txt" | head -1 | sed 's/.*Domain Status: *//' || echo "UNKNOWN")
  EXPIRY=$(grep -iE "Expir|Renewal" "$DOMAIN_DIR/whois.txt" | head -1 | sed 's/.*: *//' || echo "UNKNOWN")

  # Full dig export
  echo "  Full DNS export..."
  dig ANY "$domain" > "$DOMAIN_DIR/full_dig.txt" 2>/dev/null || echo "DIG_FAILED" > "$DOMAIN_DIR/full_dig.txt"

  # CSV row
  echo "\"$domain\",\"$NS1\",\"$NS2\",\"$MX1\",\"$MX_PRI\",\"$REGISTRAR\",\"$STATUS\",\"$EXPIRY\",\"$SPF\",\"$DMARC\"" >> "$REPORT_DIR/dns_audit.csv"

  echo "  Done."
  echo ""
done

# Generate summary
echo "=== SUMMARY ==="
echo ""
cat "$REPORT_DIR/dns_audit.csv" | column -t -s ','
echo ""

# Authority check
echo "=== AUTHORITY STATUS ==="
for domain in "${DOMAINS[@]}"; do
  NS1=$(head -1 "$REPORT_DIR/$domain/ns.txt" 2>/dev/null || echo "UNKNOWN")
  if echo "$NS1" | grep -qi "cloudflare"; then
    echo "  ✓ $domain → Cloudflare"
  elif echo "$NS1" | grep -qi "domaincontrol\|godaddy"; then
    echo "  ✗ $domain → GoDaddy (NEEDS TRANSFER)"
  else
    echo "  ? $domain → $NS1 (VERIFY)"
  fi
done

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  AUDIT COMPLETE                                      ║"
echo "║  Report: $REPORT_DIR                                 ║"
echo "║  CSV: $REPORT_DIR/dns_audit.csv                      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Review dns_audit.csv"
echo "  2. For GoDaddy domains: get auth/EPP codes"
echo "  3. For Cloudflare domains: enable email routing"
echo "  4. For drifting domains: re-add zone + lock NS"

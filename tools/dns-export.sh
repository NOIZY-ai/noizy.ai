#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# NOIZY DNS EXPORT — Full DNS backup before migration
# Run on GOD before changing ANY nameservers
# ═══════════════════════════════════════════════════════════
set -euo pipefail

DOMAIN="${1:?Usage: ./dns-export.sh <domain>}"
EXPORT_DIR="${HOME}/noizy_dns_exports/$(date +%Y%m%d)_${DOMAIN}"
mkdir -p "$EXPORT_DIR"

echo "╔══════════════════════════════════════════════════════╗"
echo "║  NOIZY DNS EXPORT                                    ║"
echo "║  Domain: $DOMAIN                                     ║"
echo "║  Export: $EXPORT_DIR                                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# All record types
RECORD_TYPES=("A" "AAAA" "CNAME" "MX" "TXT" "NS" "SOA" "SRV" "CAA" "PTR")

echo "Exporting DNS records..."

for rtype in "${RECORD_TYPES[@]}"; do
  echo "  $rtype..."
  dig "$rtype" "$DOMAIN" +noall +answer > "$EXPORT_DIR/${rtype}.txt" 2>/dev/null || true
done

# Autodiscover (critical for M365 migration)
echo "  autodiscover CNAME..."
dig CNAME "autodiscover.$DOMAIN" +short > "$EXPORT_DIR/autodiscover.txt" 2>/dev/null || true

# DKIM selectors
echo "  DKIM..."
for sel in google default selector1 selector2 s1 s2; do
  result=$(dig TXT "${sel}._domainkey.$DOMAIN" +short 2>/dev/null || true)
  if [ -n "$result" ]; then
    echo "  ${sel}._domainkey: $result" >> "$EXPORT_DIR/dkim_all.txt"
  fi
done

# DMARC
echo "  DMARC..."
dig TXT "_dmarc.$DOMAIN" +short > "$EXPORT_DIR/dmarc.txt" 2>/dev/null || true

# SPF
echo "  SPF..."
dig TXT "$DOMAIN" +short | grep "v=spf1" > "$EXPORT_DIR/spf.txt" 2>/dev/null || true

# BIND-format zone export (best effort)
echo "  BIND zone file..."
dig AXFR "$DOMAIN" > "$EXPORT_DIR/zone_transfer.txt" 2>/dev/null || echo "Zone transfer denied (normal for most registrars)" > "$EXPORT_DIR/zone_transfer.txt"

# Combined export
echo "  Combined record file..."
cat "$EXPORT_DIR"/*.txt > "$EXPORT_DIR/ALL_RECORDS.txt" 2>/dev/null

# WHOIS
echo "  WHOIS..."
whois "$DOMAIN" > "$EXPORT_DIR/whois.txt" 2>/dev/null || true

# Generate BIND-style zone file from dig results
echo "  Generating importable zone file..."
{
  echo "; NOIZY DNS Export for $DOMAIN"
  echo "; Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "; Import this into Cloudflare DNS"
  echo ""
  echo "\$ORIGIN $DOMAIN."
  echo ""
  for rtype in "${RECORD_TYPES[@]}"; do
    if [ -s "$EXPORT_DIR/${rtype}.txt" ]; then
      cat "$EXPORT_DIR/${rtype}.txt"
    fi
  done
} > "$EXPORT_DIR/IMPORT_TO_CLOUDFLARE.zone"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  EXPORT COMPLETE                                     ║"
echo "║                                                      ║"
echo "║  Files:                                              ║"
echo "║    ALL_RECORDS.txt        — every record found       ║"
echo "║    IMPORT_TO_CLOUDFLARE.zone — importable zone file  ║"
echo "║    whois.txt              — registration details     ║"
echo "║    MX.txt                 — mail servers (CRITICAL)  ║"
echo "║    autodiscover.txt       — M365 autodiscover        ║"
echo "║    spf.txt                — SPF record               ║"
echo "║    dkim_all.txt           — DKIM selectors           ║"
echo "║    dmarc.txt              — DMARC policy             ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "BEFORE changing nameservers:"
echo "  1. Review MX.txt — these keep email flowing"
echo "  2. Review autodiscover.txt — M365 needs this"
echo "  3. Copy ALL records into Cloudflare DNS FIRST"
echo "  4. THEN change nameservers at registrar"
echo "  5. NEVER change NS before copying records"

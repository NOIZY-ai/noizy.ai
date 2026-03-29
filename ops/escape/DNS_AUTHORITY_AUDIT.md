# DNS AUTHORITY AUDIT — NOIZY Domains
# Generated: 2026-03-29
# Purpose: Document current DNS authority for all 5 domains
# Status: PENDING VERIFICATION (need dig/whois results from GOD)

## DOMAINS

### noizy.ai
- Registrar: Cloudflare
- Nameservers: Cloudflare (CONFIRMED via MCP access)
- Email Routing: NOT ENABLED (blocked by CF dashboard login)
- Zone Status: ACTIVE
- Custody: CLEAN — Cloudflare controls registrar + DNS

### noizylab.ca
- Registrar: Cloudflare
- Nameservers: Cloudflare (CONFIRMED via domain registry doc)
- Email Routing: NOT CONFIGURED
- Zone Status: ACTIVE
- Custody: CLEAN — Cloudflare controls registrar + DNS

### noizyfish.com
- Registrar: GoDaddy
- Nameservers: GoDaddy (NOT Cloudflare)
- Email: GoDaddy M365 Enterprise (rsp@noizyfish.com)
- Zone Status: NOT IN CLOUDFLARE
- Custody: GODADDY CONTROLS ALL THREE CHAINS
- Action: Transfer registrar + change NS + migrate email

### fishmusicinc.com
- Registrar: GoDaddy
- Nameservers: UNSTABLE (was on Cloudflare, deleted due to NS drift)
- Email: GoDaddy M365 Email Essentials trial
- Zone Status: DELETED FROM CLOUDFLARE (nameserver drift)
- Custody: SPLIT — registrar GoDaddy, DNS drifting, email GoDaddy
- Action: Re-add zone to CF + lock NS + migrate email to Google Workspace

### noizylab.com
- Registrar: GoDaddy
- Nameservers: GoDaddy
- Email: NONE CONFIGURED
- Zone Status: NOT IN CLOUDFLARE
- Custody: GODADDY CONTROLS REGISTRAR + DNS
- Action: Transfer registrar + add zone to CF

## CUSTODY MATRIX

| Domain | Registrar | DNS | Email | Status |
|--------|-----------|-----|-------|--------|
| noizy.ai | CF ✅ | CF ✅ | NOT SET ⏳ | Clean (needs email) |
| noizylab.ca | CF ✅ | CF ✅ | NOT SET ⏳ | Clean (needs email) |
| noizyfish.com | GD ❌ | GD ❌ | GD M365 ❌ | ALL THREE CHAINS |
| fishmusicinc.com | GD ❌ | DRIFT ⚠️ | GD M365 ❌ | UNSTABLE |
| noizylab.com | GD ❌ | GD ❌ | NONE | TWO CHAINS |

## VERIFICATION COMMANDS (run on GOD)

```bash
# Verify nameservers for each domain
for domain in noizy.ai noizylab.ca noizyfish.com fishmusicinc.com noizylab.com; do
  echo "=== $domain ==="
  dig NS $domain +short
  echo ""
done

# Full WHOIS for registrar info
for domain in noizyfish.com fishmusicinc.com noizylab.com; do
  echo "=== WHOIS $domain ==="
  whois $domain | grep -E "Registrar|Name Server|Status|Expir"
  echo ""
done

# MX records (email routing)
for domain in noizy.ai noizylab.ca noizyfish.com fishmusicinc.com; do
  echo "=== MX $domain ==="
  dig MX $domain +short
  echo ""
done
```

# Cloudflare Enterprise — Signup & Migration Guide

> For when you break the GoDaddy lock and need enterprise-grade DNS + email + security.

---

## Why Enterprise (vs Free/Pro)

| Feature | Free | Pro | Enterprise |
|---------|------|-----|-----------|
| Email Routing | ✅ | ✅ | ✅ |
| DNS | ✅ | ✅ | ✅ + DNSSEC + advanced |
| WAF | Basic | Managed | Custom + advanced |
| DDoS | Unmetered | Unmetered | Priority + SLA |
| Workers | 100k req/day | 10M req/month | Unlimited |
| D1 | 5GB | 5GB | 50GB+ |
| R2 | 10GB | 10GB | Custom |
| Support | Community | Email | 24/7 phone + TAM |
| SLA | None | None | 100% uptime SLA |
| Registrar | ✅ at cost | ✅ at cost | ✅ at cost |

**For NOIZY right now: Free plan is sufficient.** Enterprise when you have paying customers and need the SLA.

---

## Current Account Status

- **Account:** Fishmusicinc
- **Plan:** Free
- **Login:** rsp@noizyfish.com (BLOCKED — CryptoTokenKit error)
- **Target login:** rsp@noizy.ai (after email routing is enabled)

---

## Migration Sequence (when CF dashboard access is restored)

### Phase 1: Email Routing on noizy.ai (3 minutes)

1. Dashboard → noizy.ai → Email → Email Routing → Enable
2. Add destination: rsplowman@icloud.com → verify
3. Create rules:
   - rsp → rsplowman@icloud.com
   - gabriel → rsplowman@icloud.com
   - admin → rsplowman@icloud.com
   - support → rsplowman@icloud.com
4. Enable catch-all → rsplowman@icloud.com
5. **Test:** send email to rsp@noizy.ai from a different address
6. **Verify:** email arrives at rsplowman@icloud.com

### Phase 2: Change CF Login Email (1 minute)

1. My Profile → Email Address
2. Change from rsp@noizyfish.com → rsp@noizy.ai
3. Verify via email to rsplowman@icloud.com (forwarded by email routing)
4. **GoDaddy chain breaks permanently**

### Phase 3: Add noizyfish.com Zone (5 minutes)

1. Dashboard → Add Site → noizyfish.com
2. Select Free plan
3. Cloudflare shows new nameservers (e.g., melinda.ns.cloudflare.com, alex.ns.cloudflare.com)
4. **DO NOT change NS at GoDaddy yet**
5. First: run dns-export.sh on GOD to capture all existing records
6. Import the zone file into Cloudflare DNS
7. Verify all records are present (especially MX for M365)
8. THEN change NS at GoDaddy → Cloudflare nameservers
9. Wait 24-48 hours for propagation
10. Verify: dig NS noizyfish.com +short → should show Cloudflare

### Phase 4: Add fishmusicinc.com Zone (5 minutes)

Same process as Phase 3. This domain was previously deleted due to NS drift.

1. Run: `./tools/dns-export.sh fishmusicinc.com` on GOD first
2. Add zone in CF dashboard
3. Import records
4. Change NS at GoDaddy
5. This time: **lock the zone** to prevent drift

### Phase 5: Add noizylab.com Zone (5 minutes)

Same process. Simplest — no email configured.

### Phase 6: Transfer Registrar (per domain, 5-7 days each)

After NS is on Cloudflare and stable for 48+ hours:

1. Get auth/EPP code from GoDaddy for each domain
2. Dashboard → Domain Registration → Transfer → enter code
3. Add payment method if needed
4. Approve transfer at GoDaddy end
5. Wait 5-7 days
6. Verify transfer complete

### Phase 7: Enable R2 (1 minute)

1. Dashboard → R2 → Enable
2. Create bucket: noizy-voice-vault
3. Create bucket: noizy-assets

### Phase 8: Deploy Workers (automatic)

Once CF API token is created and set as GitHub secret:
1. GitHub Actions auto-deploys consent-gateway on push to master
2. GitHub Actions auto-deploys cb01-router on push to master

---

## DNS Records to Preserve During Migration

### For noizyfish.com (M365 email — CRITICAL)

```
MX    noizyfish.com    noizyfish-com.mail.protection.outlook.com    priority 0
TXT   noizyfish.com    v=spf1 include:spf.protection.outlook.com -all
CNAME autodiscover     autodiscover.outlook.com
```

**If these are wrong, email stops working immediately.**

### For fishmusicinc.com (M365 email — migrating to Google)

Current M365 records (will be replaced with Google):
```
MX    fishmusicinc.com    [current M365 MX]
```

Future Google Workspace records:
```
MX    fishmusicinc.com    aspmx.l.google.com         priority 1
MX    fishmusicinc.com    alt1.aspmx.l.google.com    priority 5
MX    fishmusicinc.com    alt2.aspmx.l.google.com    priority 5
MX    fishmusicinc.com    alt3.aspmx.l.google.com    priority 10
MX    fishmusicinc.com    alt4.aspmx.l.google.com    priority 10
TXT   fishmusicinc.com    v=spf1 include:_spf.google.com ~all
```

---

## Emergency Contacts

- **Cloudflare Support:** https://support.cloudflare.com
- **Cloudflare Enterprise Sales:** https://www.cloudflare.com/plans/enterprise/contact/
- **GoDaddy (for auth codes):** 1-480-505-8877
- **Microsoft (for M365 tenant):** 1-800-642-7676
- **Google Workspace:** https://workspace.google.com/signup

---

*GORUNFREE*

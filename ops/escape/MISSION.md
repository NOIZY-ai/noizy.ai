# NOIZY — GoDaddy Detangle: noizyfish.com + fishmusicinc.com

## Objective
Release rsp@noizyfish.com and fishmusicinc.com from GoDaddy forever.
Single custody for: registrar, DNS, mailbox/identity.

## Three Chains to Sever

### 1. Registrar Custody
GoDaddy must not control the domain registration.

### 2. DNS Custody
GoDaddy must not host authoritative DNS.

### 3. Mailbox Custody
GoDaddy must not be the email provider or reseller of identity.

## Evidence
- GoDaddy security notices exist for rsp@noizyfish.com (password reset; recovery email updated)
- GoDaddy order for fishmusicinc.com includes Websites+Marketing + M365 Email Essentials trial
- Cloudflare deleted fishmusicinc.com from account; nameserver drift cited
- AADSTS50020 error on fishmusicinc.com M365 tenant — partner must be removed first
- CryptoTokenKit error -3 blocks M365 SSO on Apple devices

## Non-Negotiables
- No action without a proof artifact
- No internal infrastructure inventory in public docs
- No raw error details in user-facing outputs

## Stop Conditions (Success)
1. GoDaddy has no products remaining for target domains
2. Registrar custody is not GoDaddy (verified)
3. DNS authority is stable and controlled by Cloudflare (verified)
4. Mailbox works and is billed directly — not via GoDaddy reseller
5. Evidence ledger exists for every step

## Proof Ledger
`ops/escape/GODADDY_ESCAPE_LEDGER.jsonl`

## Tools Built
- `tools/freedom.ps1` — one-command PowerShell defederation
- `tools/godaddy-m365-escape.sh` — complete escape tool + guide
- `tools/noizy-browser.sh` — repair portal launcher

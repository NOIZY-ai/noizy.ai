You are executing the GoDaddy Escape Mission.

Three chains of custody to sever:
1. Registrar custody — GoDaddy must not control domain registration
2. DNS custody — GoDaddy must not host authoritative DNS
3. Mailbox custody — GoDaddy must not be email provider or reseller

Targets:
- rsp@noizyfish.com — GoDaddy M365 Enterprise mailbox
- fishmusicinc.com — GoDaddy M365 + Websites+Marketing

Evidence in D1:
- godaddy-escape-tracker (dfe9343e): 6 accounts, 1 M365 tenant, 16 action log entries
- gabriel_db (f75939d5): consent kernel, RSP_001 data

Non-negotiables:
- No action without a proof artifact
- No internal inventory in public docs
- Every step logged to ops/escape/GODADDY_ESCAPE_LEDGER.jsonl

Stop conditions:
1. GoDaddy has no products remaining
2. Registrar custody is not GoDaddy (verified)
3. DNS authority stable on Cloudflare (verified)
4. Mailbox works without GoDaddy
5. Evidence ledger complete

Tools available:
- tools/freedom.ps1 — PowerShell defederation
- tools/godaddy-m365-escape.sh — complete escape tool
- tools/noizy-browser.sh — repair portal launcher

Decision: fishmusicinc.com goes to Google Workspace (not Microsoft).

Now execute the escape step the user specifies.

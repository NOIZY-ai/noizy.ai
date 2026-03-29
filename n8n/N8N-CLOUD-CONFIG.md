# n8n Cloud Configuration — NOIZY

> n8n Cloud instance: `noizy.app.n8n.cloud`
> Replaces self-hosted n8n on GOD for workflow orchestration.

---

## Import Workflows

1. Sign in to `noizy.app.n8n.cloud`
2. **Workflows → Import from File**
3. Import each JSON from `n8n/workflows/`:

| # | Workflow | File | Webhook Path |
|---|---------|------|-------------|
| 1 | Consent Cascade | `consent-cascade.json` | `/webhook/consent-cascade` |
| 2 | Receipt Generator | `receipt-generator.json` | `/webhook/receipt-generator` |
| 3 | Echo Capture | `echo-capture.json` | `/webhook/echo-capture` |
| 4 | Agent Router | `agent-router.json` | `/webhook/agent-router` |
| 5 | Provenance Signer | `provenance-signer.json` | `/webhook/provenance-signer` |
| 6 | Generate Evidence | `generate-evidence.json` | `/webhook/generate-evidence` |
| 7 | Deploy Orchestrator | `deploy-orchestrator.json` | `/webhook/deploy-orchestrator` |

4. Activate each workflow after import

---

## Environment Variables

Set in **Settings → Variables**:

```
CLOUDFLARE_API_URL = https://api.cloudflare.com/client/v4/accounts/2446d788cc4280f5ea22a9948410c355
CLOUDFLARE_API_TOKEN = <create in CF dashboard: Workers + D1 + KV permissions>
CLOUDFLARE_ACCOUNT_ID = 2446d788cc4280f5ea22a9948410c355
CLOUDFLARE_D1_AGENT_MEMORY_ID = 7b813205-fd12-4a23-84a6-ce83bc49ec70
CLOUDFLARE_D1_AQUARIUM_ARCHIVE_ID = e6f98279-656b-4f7a-979d-9197821193f5
CLOUDFLARE_D1_GODADDY_ESCAPE_ID = dfe9343e-c84c-49fd-8a02-052f37a7155b
CLOUDFLARE_KV_CONSENT_GATEWAY_ID = 23c6e0bcdada4915bdf5e0d87b242810
CLOUDFLARE_KV_EMAIL_EMPIRE_ID = ef63d90235ed4faa807e57276e0d450e
CLOUDFLARE_KV_ROYALTIES_ID = 4cf36e4bd1fd44fe802096925413f694
OLLAMA_URL = https://ollama.noizy.ai (via Cloudflare Tunnel — see below)
N8N_BASE_URL = https://noizy.app.n8n.cloud
GITHUB_TOKEN = <GitHub PAT with repo + actions scope>
STRIPE_API_KEY = <Stripe secret key from dashboard.stripe.com>
```

---

## Cloudflare Tunnel → GOD (Required for Ollama Access)

n8n Cloud can't reach `localhost:11434` on GOD directly. Set up a Cloudflare Tunnel:

```bash
# On GOD:
brew install cloudflare/cloudflare/cloudflared

# Create tunnel
cloudflared tunnel create noizy-god

# Configure
cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: noizy-god
credentials-file: ~/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: ollama.noizy.ai
    service: http://localhost:11434
  - hostname: n8n-local.noizy.ai
    service: http://localhost:5678
  - hostname: aquarium-local.noizy.ai
    service: http://localhost:3000
  - service: http_status:404
EOF

# Add DNS records (Cloudflare does this automatically)
cloudflared tunnel route dns noizy-god ollama.noizy.ai
cloudflared tunnel route dns noizy-god n8n-local.noizy.ai

# Run the tunnel
cloudflared tunnel run noizy-god
```

Then set `OLLAMA_URL = https://ollama.noizy.ai` in n8n Cloud variables.

**Add Cloudflare Access** to protect ollama.noizy.ai:
- Dashboard → Zero Trust → Access → Applications
- Add Application → Self-hosted
- Domain: ollama.noizy.ai
- Policy: Allow rsplowman@icloud.com (Google auth)
- Service Auth: use n8n's service token for API access

---

## Architecture (Updated)

```
                    ┌─────────────────────────────┐
                    │    n8n Cloud                 │
                    │    noizy.app.n8n.cloud       │
                    │                              │
                    │    7 workflows               │
                    │    Public webhook URLs        │
                    │    Always on                  │
                    └──────────┬───────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │  Cloudflare  │  │  GOD via     │  │   GitHub     │
   │  KV + D1     │  │  CF Tunnel   │  │   Actions    │
   │  Workers     │  │  Ollama      │  │   Deploy     │
   └──────────────┘  └──────────────┘  └──────────────┘
            │                                    │
            ▼                                    ▼
   ┌──────────────┐                    ┌──────────────┐
   │   Stripe     │                    │   Vercel     │
   │   Payments   │                    │  The Aquarium│
   └──────────────┘                    └──────────────┘
```

---

## Webhook URLs (after activation)

Once workflows are imported and activated, they'll have public URLs:

```
https://noizy.app.n8n.cloud/webhook/consent-cascade
https://noizy.app.n8n.cloud/webhook/receipt-generator
https://noizy.app.n8n.cloud/webhook/echo-capture
https://noizy.app.n8n.cloud/webhook/agent-router
https://noizy.app.n8n.cloud/webhook/provenance-signer
https://noizy.app.n8n.cloud/webhook/generate-evidence
https://noizy.app.n8n.cloud/webhook/deploy-orchestrator
```

The Aquarium dashboard can call these directly. So can the consent-gateway Worker. So can Claude Code. So can the iPhone via Shortcuts.

---

## iPhone Shortcut (Voice-First)

Create an iOS Shortcut that:
1. Records voice → transcribes with Whisper
2. POSTs to `https://noizy.app.n8n.cloud/webhook/agent-router`
3. Gets back the agent response
4. Speaks it aloud

Robert speaks → n8n routes → Ollama responds → iPhone speaks back.

---

*n8n Cloud Config v1.0 — NOIZY.AI*

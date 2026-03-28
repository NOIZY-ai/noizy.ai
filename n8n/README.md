# n8n Workflow Orchestration for NOIZY

n8n is the **nervous system** and workflow orchestrator for the NOIZY consent infrastructure. It serves as the operational backbone until **Lucy** (Creative Director agent) is fully autonomous and capable of managing these pipelines herself. Every consent check, receipt generation, echo capture, and provenance signing flows through n8n as the central dispatch layer.

## Workflows

| Workflow | File | Description |
|----------|------|-------------|
| **Consent Cascade** | `workflows/consent-cascade.json` | Voice Estate verification, consent lookup, scope exclusion check, and clearance token generation. The gatekeeper for all usage requests. |
| **Receipt Generator** | `workflows/receipt-generator.json` | Calculates the 75/25 split, apportions the artist pool among contributors, and emits a `HybridReceipt75_25` record. |
| **Echo Capture** | `workflows/echo-capture.json` | Creates `EchoMoment` records from narrative input -- origin stories, memories, techniques, rituals. Stores to D1 agent-memory and optionally notifies Discord. |
| **Agent Router** | `workflows/agent-router.json` | CB01-style keyword dispatch. Classifies incoming messages and routes them to the correct agent via Ollama on GOD (M2 Ultra). Logs all routing decisions. |
| **Provenance Signer** | `workflows/provenance-signer.json` | Generates `ProvenanceManifest` records with SHA-256 integrity hashes and placeholder Ed25519 signing. Seals the artifact truth chain. |
| **Generate Evidence** | `workflows/generate-evidence.json` | **Gabriel-triggered master pipeline.** Orchestrates all sub-workflows into a single ArtifactTruthBundle: consent cascade → 75/25 receipt → provenance manifest → echo moment → truth strip → D1 storage → Gabriel confirmation via Ollama. 15 nodes, 8 stages. If consent is blocked, pipeline halts and returns evidence of denial. |

## Architecture

```
[The Aquarium (Vercel)]
        |
        v
   [n8n webhooks]
        |
        +---> Cloudflare KV (noizyvox-royalties, voice-estates)
        +---> Cloudflare D1 (consent records, receipts, manifests, agent-memory)
        +---> Ollama on GOD (localhost:11434) -- agent LLM inference
        +---> Discord webhooks -- notifications
```

## Connecting to External Services

### Cloudflare KV / D1

All Cloudflare API calls use environment variables:

- `CLOUDFLARE_API_URL` -- base URL for Cloudflare API (e.g., `https://api.cloudflare.com/client/v4/accounts/{account_id}`)
- `CLOUDFLARE_API_TOKEN` -- Bearer token with KV and D1 permissions
- `CLOUDFLARE_D1_DATABASE_ID` -- D1 database identifier
- `CLOUDFLARE_KV_NAMESPACE_ID` -- KV namespace for voice estates
- `CLOUDFLARE_KV_ROYALTIES_NAMESPACE_ID` -- KV namespace for royalty receipts

### Ollama on GOD (M2 Ultra)

The agent router sends inference requests to Ollama running locally on the GOD machine:

- `OLLAMA_URL` -- typically `http://localhost:11434` when n8n runs on GOD, or the LAN IP if running elsewhere
- Models referenced: `llama3`, `mistral`, `codellama`, `mixtral` (configurable per agent)

### The Aquarium (Vercel Frontend)

- `AQUARIUM_URL` -- base URL for the Vercel-deployed frontend
- Webhooks flow inbound from The Aquarium to n8n; responses return synchronously via `Respond to Webhook` nodes

### Discord

- `DISCORD_WEBHOOK_URL` -- webhook URL for the NOIZY notifications channel

## Setup

### Option A: Self-hosted on GOD (recommended)

Run n8n directly on the M2 Ultra Mac Studio (GOD) for lowest latency to Ollama and local resources:

```bash
# Install via npm
npm install -g n8n

# Or via Docker
docker run -d --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e CLOUDFLARE_API_URL="https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID" \
  -e CLOUDFLARE_API_TOKEN="your-token" \
  -e CLOUDFLARE_D1_DATABASE_ID="your-d1-id" \
  -e CLOUDFLARE_KV_NAMESPACE_ID="your-kv-namespace" \
  -e CLOUDFLARE_KV_ROYALTIES_NAMESPACE_ID="your-royalties-kv-namespace" \
  -e OLLAMA_URL="http://host.docker.internal:11434" \
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..." \
  n8nio/n8n

# Import workflows
n8n import:workflow --input=workflows/consent-cascade.json
n8n import:workflow --input=workflows/receipt-generator.json
n8n import:workflow --input=workflows/echo-capture.json
n8n import:workflow --input=workflows/agent-router.json
n8n import:workflow --input=workflows/provenance-signer.json
```

### Option B: n8n Cloud

Use [n8n.cloud](https://n8n.cloud) for managed hosting. Import each workflow JSON via the n8n UI (Settings > Import from File). Set all environment variables under Settings > Variables.

Note: If using n8n Cloud, Ollama on GOD must be exposed via a tunnel (e.g., Cloudflare Tunnel or Tailscale) since `localhost:11434` won't be reachable from n8n's cloud infrastructure.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLOUDFLARE_API_URL` | Cloudflare account API base URL |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API bearer token |
| `CLOUDFLARE_D1_DATABASE_ID` | D1 database ID for consent/receipts/manifests |
| `CLOUDFLARE_KV_NAMESPACE_ID` | KV namespace ID for voice estates |
| `CLOUDFLARE_KV_ROYALTIES_NAMESPACE_ID` | KV namespace ID for royalty receipts |
| `OLLAMA_URL` | Ollama API base URL |
| `DISCORD_WEBHOOK_URL` | Discord notification webhook |
| `AQUARIUM_URL` | The Aquarium (Vercel frontend) base URL |

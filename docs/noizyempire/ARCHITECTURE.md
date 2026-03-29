# NOIZY ARCHITECTURE

> System map: what exists, how it connects, where it runs.

## Runtime Stack
```
Voice (iPhone) → Google Meet (synapse)
  → n8n Cloud (noizy.app.n8n.cloud) — 8 workflows
    → Ollama on GOD (M2 Ultra) — 8 agents
      → Cloudflare (54 KV, 9 D1, Workers)
        → Stripe (8 products, payment rails)
          → The Aquarium on Vercel (cockpit)
```

## Core Systems

### DreamChamber
The creation environment. Not a platform — a room. Where sound becomes touch, light becomes emotion, AI amplifies human creativity.

### NOIZYVOX
Digital Voice Talent Agency. Curated roster. Characters, not voices. Artist-Centric Discovery. Multilingual character system.

### NOIZY PROOF
Cryptographic provenance. SHA-256 integrity. C2PA-like manifests. Every artifact stamped.

### HEAVEN Worker
The Cloudflare Worker runtime. consent-gateway (verify/revoke/status/health) + cb01-router (keyword dispatch).

### GABRIEL
The conscience of the system. 7 layers: Memory, Routing, Intelligence, Reputation, Protection, Evolution, Interface. Decision Contract v2: GENERATE / ASK_ARTIST / BLOCK / INHERIT.

## Databases
| Database | Role | Tables |
|----------|------|--------|
| agent-memory | Shared agent brain | 273 |
| gabriel_db | Consent Kernel | 75 |
| godaddy-escape-tracker | Migration ops | 16 |
| aquarium-archive | Drive audit | 27 |
| rsp-master-budget | Personal finance | — |
| tencc-pipeline | Sales CRM | 21 |
| mc96-command-central | System ops | 30 |
| subscription-killer | Sub management | 9 |
| noizylab-repairs | Repair tracking | — |

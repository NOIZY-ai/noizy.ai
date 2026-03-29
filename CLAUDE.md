# NOIZY.AI — Claude Code Project Instructions

## What This Is
NOIZY.AI is a consent-native AI agent family and creative infrastructure.
Built by Rob (Robert Stephen Plowman). Powered by GOD (M2 Ultra). Deployed on Cloudflare.

## The Mission
Build what nobody else can, faster than anyone thought possible.
Every artifact carries consent, provenance, authorship, and the 75/25 law.

## Architecture
- **GOD** (M2 Ultra) — Local Ollama inference server
- **Cloudflare** — Edge compute, KV (52 namespaces), D1 (10 databases), Workers, Email Routing
- **Vercel** — Frontend dashboard (The Aquarium, separate repo)
- **n8n** — Workflow orchestration (Lucy stand-in) on GOD
- **Stripe** — Payment infrastructure for 75/25 receipts

## Agent Family (8 agents)
| Agent | Role | Temp | Email |
|-------|------|------|-------|
| GABRIEL | The Voice — Lead Agent, Music | 0.5 | gabriel@noizy.ai |
| LUCY | Creative Director — Design, UX | 0.7 | lucy@noizy.ai |
| SHIRLEY | Business Ops — Legal, Finance | 0.3 | shirley@noizy.ai |
| POPS | Wisdom — Mentorship, Values | 0.6 | pops@noizy.ai |
| ENGR KEITH | Engineering — Code, Infra | 0.2 | keith@noizy.ai |
| DREAM | Visionary — R&D, Moonshots | 0.9 | dream@noizy.ai |
| CB01 | Router — Dispatch, Classification | 0.1 | cb01@noizy.ai |
| AEON | God Kernel — System Overseer | 0.1 | aeon@noizy.ai |

## Key Directories
- `heaven/` — Agent profiles, system prompts, modelfiles, routing matrix
- `schemas/` — JSON Schema v1: EchoMoment, HybridReceipt75_25, ProvenanceManifest, ArtifactTruthBundle
- `examples/` — Working instances of each schema + Dream Chamber origin echoes
- `cloudflare/` — Workers, D1 schemas, KV configs, email routing, DNS
- `n8n/` — Workflow automation templates (consent cascade, receipt generator, agent router, etc.)

## Core Schemas (schemas/)
- **EchoMoment** — Human moments worth preserving (memories, rituals, origins)
- **HybridReceipt75_25** — 75/25 artist-caring economics, enforceable at event level
- **ProvenanceManifest** — C2PA-like truth envelope (consent + attribution + integrity + signature)
- **ArtifactTruthBundle** — Unified validator (echo + receipt + manifest + truth_strip)

## Golden Rules
1. Consent is infrastructure, not a feature
2. 75/25 split — artist_pool 75%, platform_pool 25% — always
3. No artifact leaves without truth inside it (provenance, consent, receipt)
4. Rob has final word on everything
5. Voice Estate (HVS) is immutable biometric identity
6. The 5th Epoch: technology serves human dignity

## Email Empire (noizy.ai)
Primary identity: `rsp@noizy.ai` (replaces rsp@noizyfish.com)
All agents have @noizy.ai addresses via Cloudflare Email Routing.

## Cloudflare Account
- Account: Fishmusicinc (2446d788cc4280f5ea22a9948410c355)
- Domain: noizy.ai (Cloudflare DNS, fully transferred)
- Login: rsp@noizyfish.com (MIGRATING to rsp@noizy.ai)

## Development
- Branch convention: `claude/<feature>-<id>`
- Commit messages: descriptive, include session link
- Push to feature branches, never directly to master

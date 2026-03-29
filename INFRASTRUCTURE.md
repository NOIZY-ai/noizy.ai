# NOIZYEMPIRE — Infrastructure Map

> One repo. One identity. One domain.
> **rsp@noizy.ai** | **noizy.ai** | **NOIZY-ai**

---

## D1 DATABASES (9)

| # | Database | ID | Tables | Size | Role |
|---|----------|----|--------|------|------|
| 1 | **agent-memory** | 7b813205 | 200+ | 2.9MB | Primary agent memory, conversations, AI systems, NOIZYVOX |
| 2 | **gabriel_db** | f75939d5 | 74 | 807KB | **CONSENT KERNEL** — HVS, voice estates, consent records, NCP |
| 3 | **rsp-master-budget** | 74e6b824 | — | 840KB | Rob's personal budget |
| 4 | **godaddy-escape-tracker** | dfe9343e | 16 | 94KB | Domain migration, action log |
| 5 | **aquarium-archive** | e6f98279 | 27 | 254KB | Drive audit, file scanning, archive |
| 6 | **tencc-pipeline** | d1a5c748 | 21 | 250KB | Sales pipeline, CRM, revenue forecast |
| 7 | **mc96-command-central** | ef4eda10 | 30 | 250KB | System ops, device registry, automation |
| 8 | **subscription-killer** | 145b3abb | 9 | 66KB | Subscription management |
| 9 | **noizylab-repairs** | 2bd4aa06 | — | 459KB | Repair business tracking |

## KV NAMESPACES (54)

### Active / Critical
| Namespace | ID | Purpose |
|-----------|----|---------|
| agent-state | 150a3c32 | Agent availability and state |
| consent-gateway-state | 23c6e0bc | Consent clearance token cache |
| noizy-email-empire | ef63d902 | Email routing state |
| GABRIEL_KV | 68710a32 | Gabriel general state |
| GABRIEL_VOICE | 28f2fdce | Gabriel voice/audio configs |
| master-command-log | 99d2dd87 | All routing decisions |
| noizyvox-royalties | 4cf36e4b | Royalty receipt storage |
| noizyvox-manifests | 86da0218 | Provenance manifests |
| noizyvox-artist-profiles | d0054fd9 | Artist profile data |
| noizyvox-guild | 8a15ed31 | Guild membership |
| noizyvox-academy | 9cce0e45 | Academy courses |
| noizyvox-signups | 392c1bf4 | Waitlist signups |
| noizyvox-personas | deed590a | Voice personas |
| feature-flags | 7d688ad2 | Feature toggles |
| god-kernel-state | fa91fd99 | AEON system state |
| api-token-vault | c453c1b2 | Secure token storage |

### Infrastructure
| Namespace | Purpose |
|-----------|---------|
| conductor-locks | CB01 dispatch locks |
| conductor-workers | CB01 worker registry |
| command-queue | Queued commands |
| voice-commands | Voice command buffer |
| voice-command-buffer | Voice input staging |
| session-cache | Session management |
| rate-limiter | Rate limiting |
| emergency-alerts | Alert system |
| realtime-status | Live status |
| memcell-cache | Memory cell cache |
| ai-response-cache | AI response cache |
| cf-proxy-cache | Cloudflare proxy cache |
| model-performance | Model metrics |
| aeon-protocol-state | AEON protocol |

### Business
| Namespace | Purpose |
|-----------|---------|
| noizylab-customers | Customer data |
| noizylab-submissions | Form submissions |
| noizylab-edge-config | Edge configuration |
| noizylab-rate-limiter | Rate limiting |
| noizylab-sessions | Session data |
| noizymem-sessions | Memory sessions |

### Projects
| Namespace | Purpose |
|-----------|---------|
| godaddy-escape-state | Migration state |
| gorunfree-execution-state | Execution tracking |
| mc96-hotrod-cache | MC96 cache |
| antigravity-cache | Antigravity project |
| tencc-locks | 10cc pipeline locks |
| tencc-pipeline-state | Pipeline state |
| dafixer-repair-queue | Repair queue |
| lifeluv-cache | LifeLuv cache |
| hero-voice-kv | Hero voice data |
| VEO3_KV | VEO3 project |
| CRAWLER_KV | Crawler data |

### Comms
| Namespace | Purpose |
|-----------|---------|
| discord-queue | Discord message queue |
| discord-hub-queue | Discord hub queue |

### Flow
| Namespace | Purpose |
|-----------|---------|
| flow-sessions | Flow sessions |
| flow-rate-limits | Flow rate limits |
| flow-checkins | Flow check-ins |
| flow-cases | Flow cases |
| flow-logs | Flow logs |

## WORKERS (1 deployed, 2 ready)

| Worker | Status | Purpose |
|--------|--------|---------|
| deploy | **STUB** (Hello World) | Needs replacement |
| consent-gateway | **CODE READY** (not deployed) | Consent cascade at edge |
| cb01-router | **CODE READY** (not deployed) | Agent dispatch |

## STRIPE (Fish Music Inc)

| Item | Count |
|------|-------|
| Products | 8 |
| Prices | 7 |
| Payment Links | 6 |
| Customers | 1 (RSP_001) |

## DOMAINS

| Domain | Registrar | NS | Status |
|--------|-----------|----|---------|
| noizy.ai | Cloudflare | Cloudflare | **PRIMARY** |
| noizylab.ca | Cloudflare | Cloudflare | Active |
| fishmusicinc.com | GoDaddy | Cloudflare | Transfer pending |
| noizyfish.com | GoDaddy | GoDaddy | Transfer pending |
| noizylab.com | GoDaddy | GoDaddy | Transfer pending |

## IDENTITY

| System | Old | New |
|--------|-----|-----|
| Cloudflare login | rsp@noizyfish.com | → rsp@noizy.ai (pending) |
| GitHub | Noizyfish | NOIZY-ai org |
| Stripe | Fish Music Inc | Fish Music Inc |
| Linear | NOIZYLAB | NOIZYLAB |
| Slack | noizyfishcom | noizyfishcom |
| Google | rsplowman@icloud.com | rsplowman@icloud.com |
| Notion | R.S Plowman's Space HQ | NOIZYEMPIRE |
| n8n | noizy.app.n8n.cloud | noizy.app.n8n.cloud |
| Figma | NoizyFish | Fish Music team |

---

*NOIZYEMPIRE Infrastructure Map v1.0*
*GORUNFREE*

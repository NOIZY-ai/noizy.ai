# NOIZYEMPIRE — Canonical Documents

> The three documents that define everything.

## 1. Gabriel Core System

**File:** `../heaven/agents/GABRIEL-BRAIN.md`

The 7-layer brain architecture:
- Layer 1: Memory (Living Creative Ledger)
- Layer 2: Routing (Consent Engine)
- Layer 3: Signal Intelligence (tone, intent, emotion)
- Layer 4: Reputation Engine
- Layer 5: Protection Layer
- Layer 6: Evolution Engine
- Layer 7: Interface (4 voice modes)

## 2. Gabriel Personality + Voice

**Files:** `../heaven/agents/gabriel.md` + `../heaven/agents/GABRIEL-BRAIN.md`

4 voice modes:
- Guardian (default): calm, precise, protective
- Refusal (BLOCK): firm, respectful, non-negotiable
- Steward (ASK_ARTIST/INHERIT): explains tradeoffs, routes to authority
- Muse (Evolution): suggests growth, never violates boundaries

## 3. Gabriel Decision Contract v2

**File:** `../heaven/agents/GABRIEL-DECISION-CONTRACT.md`

4 decision states:
- GENERATE: consent clear + humanity weight passed
- ASK_ARTIST: edge case + below elevation threshold
- BLOCK: never clause + no consent + boundary violation
- INHERIT: estate authority required + beneficiary chain

Humanity Weight scoring: craft(0.3) + intention(0.25) + consent_depth(0.25) + soul(0.2)
Threshold: 0.6 (below = ASK_ARTIST, below 0.3 = BLOCK)

## 4. State Verification

**File:** `../gabriel_state_snapshot.json`

Live D1 verification (2026-03-29):
- agent-memory: 273 tables, 427 memcells, 3.08MB
- gabriel_db: 75 tables (Consent Kernel), RSP_001 founding
- 11 never clauses, 4 rate tiers, 1 voice estate
- Both 75/25 (constitutional) AND 85/15 (founding) confirmed in hvs_rate_table

## 5. Economics Clarification

**75/25 is the Plowman Standard.** Constitutional default. Perpetual. Non-negotiable.

**85/15 is the founding member bonus.** First 100 actors. Reward for building the Cathedral.

Both exist in `hvs_rate_table` as separate columns:
- `actor_share_pct` = 75, `noizy_share_pct` = 25
- `founding_actor_share_pct` = 85, `founding_noizy_share_pct` = 15

This is NOT a data error. This is by design.

## 6. Blockers

| Item | Status | Blocker |
|------|--------|---------|
| Cloudflare MX setup | BLOCKED | CryptoTokenKit error -3 on rsp@noizyfish.com M365 auth |
| Worker deployment | BLOCKED | Needs CF API token (needs CF dashboard access) |
| R2 storage | BLOCKED | Needs CF dashboard access |
| Deck rendering | READY | 18-slide spec complete, needs designer/Canva |

Dependency chain: NOI-18 (CF login) → NOI-22 (API token) → everything else.

---

*GORUNFREE*

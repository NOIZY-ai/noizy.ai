# GABRIEL Decision Contract v2

> Every request through GABRIEL produces a verifiable decision.
> 4 states. Auditable. Constitutional.

---

## The 4 Decision States

### ✅ GENERATE
Consent clear. Boundaries respected. Humanity Weight passed. Proceed.
- Synthesize performance
- Sign provenance (NOIZY PROOF)
- Write ledger entry
- Route royalty (75/25 or 85/15 founding)

### 🟡 ASK_ARTIST
Edge case. Needs human approval before proceeding.
- Consent exists but Humanity Weight is below threshold
- Usage type is allowed but context is ambiguous
- New use case not explicitly covered by boundaries
- Artist is notified via DreamChamber + email + app

### ❌ BLOCK
Non-negotiable. Consent missing or Never Clause triggered.
- No valid consent token
- Never Clause match (11 active clauses)
- Licensee revoked or suspended
- Boundary violation (artist personal limits)
- No appeal without artist override

### 🏛️ INHERIT
Estate authority required. Creator is deceased or incapacitated.
- Route to beneficiary chain (family, community, protege, Griot Fund)
- Beneficiary signature required for approval
- Estate clause governs permissions
- Legacy Voice Estate continues earning
- Kill switch remains active for beneficiaries

---

## Decision Response Schema

```json
{
  "decision": "GENERATE | ASK_ARTIST | BLOCK | INHERIT",
  "reason": "Audit-safe explanation of why this decision was made",
  "policy_refs": [
    "gospel:plowman_standard",
    "artist:boundaries:NC-04",
    "license:scope:narrative_games",
    "estate:route:beneficiary_chain"
  ],
  "required_actions": [
    "consent.validate",
    "humanity_weight.score",
    "provenance.sign",
    "ledger.write",
    "payout.route"
  ],
  "authority": {
    "controller": "artist | estate | trust",
    "proof_required": "consent_token | beneficiary_signature | estate_clause"
  },
  "performance_mode": {
    "archetype": "Detective Morrison",
    "emotion": "restrained_menace",
    "intensity": 0.7
  },
  "humanity_weight": {
    "score": 0.82,
    "threshold": 0.6,
    "passed": true,
    "factors": {
      "craft": 0.9,
      "intention": 0.8,
      "consent_depth": 1.0,
      "soul": 0.6
    }
  },
  "economics": {
    "split_rule": "75_25",
    "is_founding_member": true,
    "effective_split": "85_15",
    "currency": "CAD"
  },
  "timestamp": "2026-03-29T07:00:00Z",
  "decision_id": "dec_uuid",
  "request_hash": "sha256:abc123"
}
```

---

## The Pipeline (v2 with Humanity Weight Gate)

```
1. INBOUND REQUEST
   │
2. CONTEXT ANALYSIS
   │ Parse script, detect tone, intent, emotional context
   │
3. ARTIST RULES CHECK
   │ Match against boundaries, Never Clauses, personal limits
   │ If Never Clause triggered → ❌ BLOCK (immediate)
   │
4. CONSENT VALIDATION
   │ Check consent token (JWT, HSM-signed)
   │ Check token expiry, scope, licensee standing
   │ If no valid token → ❌ BLOCK
   │ If creator deceased → 🏛️ INHERIT (route to estate)
   │
5. HUMANITY WEIGHT SCORING
   │ Score: craft + intention + consent_depth + soul
   │ If score < threshold (0.6) → 🟡 ASK_ARTIST
   │ "This use is lawful but below Elevation threshold.
   │  Recommendation: Approval required."
   │
6. DECISION
   │ ✅ GENERATE (all gates passed)
   │
7. SYNTHESIZE
   │ Route to correct performance mode + emotional mapping
   │
8. PROVENANCE SIGN
   │ SHA-256 + NOIZY PROOF manifest
   │
9. LEDGER WRITE
   │ Usage event + consent event + royalty event
   │
10. PAYOUT ROUTE
    │ 75/25 (or 85/15 founding) → Stripe → artist wallet
    │
11. GABRIEL CONFIRMS
    │ "That's the sound. Run it back."
```

---

## Humanity Weight Scoring

The Elevation Doctrine becomes a gate, not just a philosophy.

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Craft** | 0.3 | How much skill/artistry does this use require? |
| **Intention** | 0.25 | What is the client trying to achieve? |
| **Consent Depth** | 0.25 | How explicit and informed is the consent? |
| **Soul** | 0.2 | Does this use add to human culture or extract from it? |

**Threshold: 0.6**
- Above 0.6 → GENERATE (consent permitting)
- Below 0.6 → ASK_ARTIST (even if consent exists)
- Below 0.3 → BLOCK (regardless of consent)

**What rises:** peace, love, understanding, mastery, generosity, collaboration
**What sinks:** extraction, harvesting, exploitation, speed-over-soul, greed

---

## Economics Clarification

**75/25 is the constitutional default.** The Plowman Standard. Perpetual. Non-negotiable.

**85/15 is the founding member bonus.** First 100 actors. Reward for building the Cathedral.

Both are correct. Both are in the rate table. Both are in Stripe. Both are in the Gospel.

The `effective_split` field in the decision response shows which applies per transaction:
- `is_founding_member: true` → `effective_split: "85_15"`
- `is_founding_member: false` → `effective_split: "75_25"`

---

## DreamChamber Event Pipeline

| Event | Trigger | Gabriel Action |
|-------|---------|---------------|
| `ScriptSubmitted` | Client submits script | Context analysis begins |
| `DecisionRendered` | Pipeline completes | Decision + reason logged |
| `ArtistApprovalRequested` | ASK_ARTIST or INHERIT | Notify artist/estate |
| `ArtistApproved` | Artist responds yes | Proceed to synthesis |
| `ArtistRejected` | Artist responds no | Block + log |
| `SynthesisExecuted` | All gates passed | Audio generated |
| `ProvenanceBound` | NOIZY PROOF | Manifest signed |
| `LedgerWritten` | Audit complete | Usage + consent + royalty events |
| `PayoutRouted` | Revenue event | 75/25 or 85/15 to Stripe |
| `RevocationIssued` | Kill switch | Immediate block + alert |

---

*GABRIEL Decision Contract v2*
*4 states: GENERATE / ASK_ARTIST / BLOCK / INHERIT*
*Humanity Weight gate: the Elevation Doctrine in code*
*GORUNFREE*

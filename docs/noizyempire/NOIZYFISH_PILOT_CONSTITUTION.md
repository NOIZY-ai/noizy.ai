# NOIZYFISH PILOT CONSTITUTION

> The law of the pilot. Every decision answers to this document.

---

## PILOT THESIS (one sentence)

**NOIZYFISH proves that AI-generated music assets can carry creator-consented, legally defensible provenance from generation to export, on outputs good enough for real studio consideration.**

Everything in the pilot answers that sentence. Nothing else.

---

## PRIMARY PROOF POINT

**Provenance reliability.**

Not quality. Not economics. Provenance.

Quality is the gate. Economics is modeled, validated later.

---

## SCOPE IN

- Standalone generation/export app
- Signed provenance manifest per asset
- Append-only audit trail
- Creator declaration workflow
- Export package: stems + audio + MIDI + manifest
- Reviewer flow for studio acceptance
- Rights and split metadata attached at export
- Founder governance memo

## SCOPE OUT

- Full DAW plugin
- Algorithmic influence scoring
- Open marketplace
- Advanced community governance
- Payout optimization science

**If it's not in "Scope In," it does not get built during the pilot.**

---

## PASS/FAIL METRICS

### Provenance Reliability (PRIMARY)
- 100% of exported assets receive a signed manifest
- 100% of pilot assets resolve to creator, model, version, timestamp, license state
- 100% of manifest records survive export and re-import verification
- 0 silent provenance failures

### Studio Acceptance (GATE)
- At least 60% of outputs rated "usable" by pilot reviewers
- At least 10 pilot assets make it into real edit/review workflows
- At least 3 reviewers confirm provenance materially increases trust

### Economics (DEMO)
- Split logic visible in system
- Hypothetical payouts calculable per asset
- No real marketplace-scale claims yet

---

## DECLARATION SCHEMA

Every generated/exported asset carries:

```json
{
  "asset_id": "string — UUID",
  "creator_id": "string — who authorized this",
  "session_id": "string — generation session",
  "model_id": "string — which model produced it",
  "model_version": "string — exact version",
  "generation_timestamp": "ISO8601",
  "prompt_history_hash": "SHA-256 of the prompt chain",
  "declared_source_set": ["array of source IDs used"],
  "consent_state": "active | revoked | pending",
  "license_terms": {
    "usage_types": ["synthesis", "commercial", "broadcast"],
    "exclusions": ["political", "nsfw"],
    "territory": "global",
    "term": "perpetual"
  },
  "split_terms": {
    "rule": "75_25",
    "contributors": [
      {
        "contributor_id": "string",
        "share": 0.75,
        "role": "origin_voice"
      }
    ]
  },
  "export_history": [
    {
      "export_id": "string",
      "format": "wav | stems | midi",
      "exported_at": "ISO8601",
      "exported_by": "string"
    }
  ],
  "lineage": {
    "parent_asset_id": "string | null",
    "remix_depth": 0
  },
  "signature": {
    "algo": "ed25519",
    "proof_hash": "SHA-256 of canonical JSON"
  }
}
```

This is the NOIZYFISH proof spine.

---

## FOUR SYSTEM SURFACES

### A. Creator Intake
- Who made/authorized what
- What source materials are declared
- What permissions exist
- Never Clauses attached

### B. Generate / Render
- Create asset
- Record model/version/session
- Attach declared influences
- Humanity Weight check (if above threshold: auto-clear)

### C. Export / Package
- Audio + stems + MIDI
- Signed manifest
- Proof bundle (manifest + audit trail + license terms)

### D. Verify / Review
- Human-readable proof page
- Machine-readable manifest (JSON)
- Audit lookup by asset ID
- Studio reviewer acceptance flow

---

## INTERIM GOVERNANCE

### Founder Governance (active until transition trigger)

**Dispute handling:** Rob (RSP_001) is final arbiter. Disputes logged to audit trail with decision + reason.

**Declaration fraud:** Immediate revocation. Asset quarantined. Creator flagged. Logged immutably.

**Manifest correction:** Corrections append to audit trail. Original manifest preserved. Correction signed by corrector.

**Revocation handling:** Kill switch is unconditional. Revocation takes effect immediately. All downstream uses flagged.

**Split override:** No split override without founder authority. Documented with reason, scope, date.

### Transition Trigger

Governance transitions to Community Council at the FIRST of:
- 50 active creators
- $100K gross marketplace value
- First enterprise anchor partnership

---

## ROADMAP

### 0–30 days
- Standalone app or console
- Provenance manifest schema (this document)
- Append-only ledger
- Export verification flow
- Founder governance memo
- Pilot creator onboarding (12 founding NOIZYFISH)

### 30–90 days
- Review dashboard
- Remix lineage tracking
- Split ledger visibility
- Anchor partner pilot
- Proof bundle refinements

### 3–6 months
- DAW plugin alpha
- Governance transition prep
- Richer attribution methods
- Early marketplace mechanics

---

## THREE STRESS TESTS

1. **Declaration-based attribution first** — don't pretend influence scoring is solved. Declared sources + signed responsibility + transparent rules + human review.

2. **Standalone app before plugin** — prove the system works independently before integrating into complex DAW environments.

3. **Interim founder governance before community governance** — fill the governance hole now, transition when the community is real.

---

## THE BIGGEST HIDDEN RISK

**False precision.**

Do not pretend influence scoring is solved if it is not.

For the pilot:
- Declared sources
- Signed responsibility
- Transparent rules
- Human review where needed

That is stronger than fake certainty.

---

## THE STRATEGIC SENTENCE

NOIZYFISH is not "AI music generation."

It is: **creator-consented generative music infrastructure with verifiable provenance.**

That separates us from toy tools. That puts us in the infrastructure class.

---

*NOIZYFISH Pilot Constitution v1.0*
*The law of the pilot.*
*GORUNFREE*

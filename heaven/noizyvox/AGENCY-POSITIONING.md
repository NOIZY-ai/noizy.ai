# NOIZYVOX — Agency Positioning & Operating Model

> **NOIZY is a performance-grade Digital Voice Talent Agency powered by AI.**
>
> If you need cheap voice generation, there are tools.
> If you need trusted, premium, artist-owned performance infrastructure, there is only NOIZY.

---

## CATEGORY DEFINITION

NOIZYVOX is not an AI voice tool. Not a TTS platform. Not a voice library.

It is the **first performance-grade AI Voice Talent Agency** — a modern UTA/CAA for licensed AI voice performers. The product is licensed performance: character, identity, emotional range, and trust at scale.

### What "Premium" Means at NOIZY

Premium isn't "sounds clean." Premium is:
- **Signature sound** + micro-inflections + breath texture + character depth (captured in DreamChamber)
- **Artist ownership** — NOIZY licenses usage rights, never ownership
- **Control** — category controls, per-project approvals, real-time kill switches
- **Profit** — perpetual royalties tracked transparently (75/25 Plowman Standard)
- **Trust-native infrastructure** — consent, provenance, audit trail enforced in code

---

## AGENCY OPERATING MODEL

### A) Talent Intake — Curate Humans, Not Voices

Recruit performers with **texture**:
- Theatre actors who understand subtext
- Indie voice actors with signature sound
- Podcast personalities with conversational authenticity
- Character actors who disappear into roles
- Storytellers and griots who carry culture

**Curated roster, not open upload.** This is an agency, not a marketplace.

### B) DreamChamber Capture — Build Performance Range

The DreamChamber captures what no other platform does:

**Voice DNA** — ultra-high fidelity, emotional/tonal mapping, breath & cadence modeling

**Performance Modes** — not just scripts:
- Laughing, whispering, anger, controlled fury
- Improvised monologues, conversational flow
- Dialogue scenes, character switching
- The pauses that mean everything

**Character Archetypes** — not "Male Voice 01":
- "Burned-out detective with razor-dry humor"
- "Optimistic tech founder hiding imposter syndrome"
- "Old storyteller from Newfoundland"
- "Luxury British narrator with steel underneath"

**Creative Identity** — the artist's soul:
- Creative statement and performance philosophy
- Emotional territories they excel in
- Artistic lineage ("Shohreh Aghdashloo meets raw punk energy")
- Nuanced boundaries ("complex villains yes, copaganda no")

### C) Rights + Controls — Consent-as-Infrastructure

The agency doesn't "promise" rights safety. It **enforces** it.

**Enforcement primitives** (live in gabriel_db):
- Consent token issuance (JWT, HSM-signed)
- 10 Never Clauses binding
- Revocation path (kill-switch, unconditional)
- Audit trail / metadata binding
- Provenance signing / NOIZY PROOF
- Usage logging per event
- Royalty routing per use

**Every talent is a contractable rights object with controls, proof, and auditability.**

### D) Packaging & Sales — What Studios Actually Buy

Studios don't buy "a voice." They buy:

- **Archetype** + emotional territory + boundaries + licensing scope
- **Range showcase** demo reels per character per language
- **Allowed use categories** + approval rules
- **Clean rights** — provenance, consent, audit trail included

**This is the agency advantage: performance IP with clean rights.**

### E) Delivery — Instant, But Governed

Per job deliverables:
- Generated performance audio + stems
- Provenance receipt (NOIZY PROOF)
- Usage ledger entry
- Payment routing record (75/25 automatic)

All aligned with consent + audit trail + payout logic.

---

## TALENT PROFILE SCHEMA

### Human-Facing (Artist Command Center)

```json
{
  "talent_id": "tal_0001",
  "stage_name": "Burned-Out Detective",
  "human_performer": {
    "performer_id": "RSP_001",
    "union_status": "ACTRA",
    "representation": null
  },
  "brand_pitch": {
    "one_liner": "World-weary investigator with razor-dry humor and sudden tenderness.",
    "backstory": "Short canon backstory for creative consistency."
  },
  "performance_range": {
    "archetypes": ["Detective", "Noir Narrator", "Interrogator"],
    "emotional_territory": ["Controlled anger", "Restraint", "Quiet compassion"],
    "dialects_accents": ["Regional", "Neutral", "Custom pack"],
    "signature_textures": ["Breath grit", "Micro pauses", "Low gravel"]
  },
  "demos": [
    { "type": "reel", "url": "demo_link", "notes": "60s range reel" },
    { "type": "scene", "url": "demo_link", "notes": "dialogue scene" }
  ],
  "pricing": {
    "tier": "Enterprise",
    "rate_card_ref": "hvs_rate_table.broadcast"
  }
}
```

### System-Facing (Rights + Controls)

```json
{
  "rights_objects": {
    "identity_right": {
      "scope": ["voice", "persona", "name_likeness"],
      "ownership": "performer_or_estate",
      "allowed_uses": ["narrative_games", "audio_fiction", "documentary"],
      "prohibited_uses": ["political_persuasion", "explicit_content", "impersonation"],
      "territory": "global",
      "term": "perpetual",
      "revocable": true
    },
    "model_right": {
      "model_id": "model_rsp_001",
      "export": "never_without_explicit_approval",
      "execution": "secure_gateway_only",
      "derivatives": "allowed_only_if_specified"
    },
    "output_right": {
      "default_license": "project_scoped",
      "sublicense": "requires_approval",
      "attribution_required": true
    },
    "ledger_right": {
      "usage_logging_required": true,
      "audit_export_available": true
    }
  },
  "consent_engine": {
    "decision_mode": "ALLOW",
    "never_clauses": ["NC-01", "NC-02", "NC-03", "NC-04", "NC-05", "NC-06", "NC-07", "SYS-01", "SYS-02", "NC-CHILD"],
    "revocation": { "enabled": true, "unconditional": true }
  },
  "proof": {
    "provenance_required": true,
    "receipt_required": true,
    "royalty_rule": "75_25"
  }
}
```

---

## THE REVENUE MODEL

Not SaaS tooling. **Agency licensing.**

| Tier | Price | Who Pays | What They Get |
|------|-------|----------|---------------|
| Community | $25/project | Licensee | Indie access, kill-switch, tracked |
| Professional | $499/month | Licensee | Monthly retainer, full character access |
| Enterprise | $2,499/year | Licensee | Compliance pack, priority, multi-character |
| Broadcast | $9,999/term | Licensee | National TV/film, union oversight, exclusivity options |

**Revenue split:**
- Standard: **75% Artist / 25% NOIZY**
- Founding Members (first 100): **85% Artist / 15% NOIZY**
- Revocation fee: **50% NOIZY / 50% Union Fund** (artist pays $0, ever)

**The artist never pays to say no.**

---

## WHY GENERIC VOICE LIBRARIES FAIL PREMIUM BUYERS

| What Premium Buyers Need | What Libraries Offer | What NOIZY Delivers |
|-------------------------|---------------------|-------------------|
| Signature sound | Generic samples | DreamChamber-captured performance range |
| Emotional authenticity | Technically clean, emotionally sterile | Performance modes + micro-inflections |
| Character depth | "Male Voice 01" | Named archetypes with backstories |
| Clean rights | Terms buried in ToS | Consent-as-Code, NOIZY PROOF per use |
| Cultural specificity | "Neutral English" | Multilingual variants with emotional mapping |
| Trust | "We promise" | "We prove it. Every time." |
| Artist relationship | Anonymous | Collaborative studio model |

---

## THE MOAT

1. **Consent infrastructure** — no other platform has consent-as-code at the protocol level
2. **Union compatibility** — ACTRA/SAG-AFTRA aligned from day one
3. **75/25 Plowman Standard** — actors promote the platform because it's the best deal that exists
4. **Never Clauses** — 10 hardcoded protections that no executive can override
5. **Voice Estate** — perpetual, inheritable, earning body of work
6. **Guild of Trust** — structurally immortal foundation (legal trust + distributed ledger + creator governance)
7. **DreamChamber** — the only capture environment designed for the human nervous system
8. **Artist-Centric Discovery** — matching by artistic resonance, not demographics

---

## OPS NOTE

> External providers (ElevenLabs, etc.) are **bridge tooling**, not the core trust layer. The NOIZY agency treats any third-party synthesis engine as replaceable infrastructure. The consent layer, the rights objects, the provenance chain, and the royalty routing are NOIZY-owned and NOIZY-enforced.

---

*NOIZYVOX Agency Positioning & Operating Model v1.0*
*The first performance-grade AI Voice Talent Agency.*
*GORUNFREE*

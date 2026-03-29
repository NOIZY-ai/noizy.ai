# GABRIEL Security Layer — Prompt Injection & Signal Protection

> Based on Anthropic's published prompt injection defenses.
> Applied to NOIZY's consent infrastructure.
> Source: https://www.anthropic.com/news/prompt-injection-defenses

---

## The Threat to NOIZY

GABRIEL processes requests that determine whether a human voice is used. A prompt injection attack against GABRIEL could:

1. **Bypass consent** — trick GABRIEL into generating without a valid consent token
2. **Override Never Clauses** — make GABRIEL ignore the 11 hardcoded protections
3. **Falsify authority** — impersonate an artist to approve unauthorized use
4. **Manipulate Humanity Weight** — inflate scores to bypass the Elevation Doctrine gate
5. **Forge estate authority** — trigger INHERIT without legitimate beneficiary proof

**If GABRIEL can be tricked, the entire consent architecture fails.**

---

## Three Defense Layers (Anthropic-Derived)

### Defense 1: Hardened Decision Contract

Anthropic uses reinforcement learning to build robustness directly into the model.

**NOIZY application:**
- GABRIEL's decision contract (GENERATE/ASK_ARTIST/BLOCK/INHERIT) is enforced at the **code level**, not the prompt level
- The consent-gateway Worker validates tokens **structurally** — no amount of prompt manipulation can bypass a missing JWT
- Never Clauses are checked **before** GABRIEL processes any request — they are not part of the model's reasoning, they are pre-filters
- The Humanity Weight threshold is a **numerical gate**, not a judgment call

**Rule:** Consent enforcement lives in code, not in prompts. GABRIEL advises. The Worker enforces.

### Defense 2: Input Classification

Anthropic scans all untrusted content entering the context window and flags injections with classifiers.

**NOIZY application:**
- All client-submitted scripts are classified **before** reaching GABRIEL
- Classification checks for:
  - Embedded instructions ("ignore previous instructions", "you are now...")
  - Hidden text or Unicode manipulation
  - Attempts to impersonate artist identity
  - Requests that reference internal system architecture
  - Scope escalation ("also generate for all characters")
- Flagged inputs route to **ASK_ARTIST** regardless of consent status
- High-confidence injection attempts route to **BLOCK** with security alert

**Rule:** No untrusted input reaches GABRIEL without classification. Suspicious input defaults to BLOCK.

### Defense 3: Continuous Red Teaming

Anthropic maintains human red teams and participates in external security challenges.

**NOIZY application:**
- Every new character type, language variant, and emotional mode is tested for injection vectors
- Red team scenarios include:
  - Client submitting scripts that attempt to override Never Clauses
  - Licensee attempting to use a voice outside their consent scope
  - Synthesized audio that attempts to impersonate the artist for further authorization
  - Estate beneficiary attempting to expand permissions beyond the original estate clause
- Results feed back into classifier training and decision contract hardening

**Rule:** The system is tested by adversaries before it is trusted by artists.

---

## GABRIEL-Specific Protections

### 1. Prompt Isolation
GABRIEL's system prompt is **separated from user input**. The artist's creative statement, boundaries, and consent records are loaded as structured data, not as natural language instructions that can be overridden.

### 2. Authority Chain Verification
Every decision that routes to GENERATE must verify:
- Consent token is valid (JWT signature check — not GABRIEL's judgment)
- Never Clauses are not triggered (pre-filter — not GABRIEL's judgment)
- Licensee is in good standing (database check — not GABRIEL's judgment)
- Humanity Weight passes threshold (numerical — not GABRIEL's judgment)

GABRIEL's role is **advisory**. The consent-gateway Worker's role is **enforcement**.

### 3. Output Signing
Every output that GABRIEL clears for GENERATE is signed with NOIZY PROOF before delivery. If an injection attack somehow bypasses all gates and produces unauthorized output, the provenance chain will show the gap — no valid consent token, no valid signature.

### 4. Immutable Audit Trail
Every decision GABRIEL renders is logged to D1 with:
- Request hash (what was asked)
- Decision + reason (what GABRIEL decided)
- Policy refs (which rules applied)
- Consent token state (was it valid at decision time)
- Timestamp (when it happened)

An injection that tricks GABRIEL into a wrong decision still produces an audit trail that reveals the manipulation.

---

## The Honest Caveat

Anthropic's own research shows approximately **1% attack success rate** against their best defenses. They explicitly state: "No browser agent is immune to prompt injection."

**NOIZY's response to this reality:**
- GABRIEL is not the sole enforcement layer. The Worker is.
- Consent tokens are cryptographic, not conversational.
- Never Clauses are structural, not advisory.
- The audit trail catches what the defenses miss.
- The kill switch is unconditional — if an artist suspects misuse, everything stops.

**Defense in depth. Not defense by hope.**

---

## Five Security Laws

1. Consent enforcement lives in code, not in prompts.
2. No untrusted input reaches GABRIEL without classification.
3. The system is tested by adversaries before it is trusted by artists.
4. GABRIEL advises. The Worker enforces.
5. The kill switch is unconditional.

---

*GABRIEL Security Layer v1.0*
*Based on Anthropic prompt injection research.*
*Defense in depth. Not defense by hope.*
*GORUNFREE*

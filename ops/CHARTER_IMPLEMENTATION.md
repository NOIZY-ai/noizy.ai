# Charter Implementation Guide

> Step-by-step rollout of the Imperial Operating Charter.
> Verify each step. No mythology.

---

## Step 1: Manifest Freeze (NOW)
- [x] Imperial Charter committed to master
- [x] NOIZYFISH Pilot Constitution committed to master
- [x] NoizyFishManifest.schema.json on master
- [x] StandardGospelDeal.schema.json on master
- [ ] charter-manifest.json in every repo root (computed hash of Charter)

## Step 2: Repo Law (NOW)
- [x] Seven Laws in IMPERIAL_CHARTER.md
- [x] CLAUDE.md in both repos
- [x] .claude/commands/ with 6 DreamChamber prompts
- [ ] Seven Laws added to top of every README.md

## Step 3: Universe Registry (NEXT)
- [x] imperial-registry.sql migration written
- [ ] Deploy to agent-memory D1: `wrangler d1 execute agent-memory --file=imperial-registry.sql`
- [ ] Verify 10 pillars present in D1

## Step 4: Health Board (NOW)
- [x] Pilot Scorecard created
- [x] MC96 Support-AI workflow documented
- [ ] GOD Command Dashboard built (HTML/JS + Workers + D1)
- [ ] Dashboard queries imperial_registry + pilot scorecard

## Step 5: Verification Gates (NEXT)
- [x] Consent-gateway has input sanitization (10 patterns)
- [x] GABRIEL Decision Contract v2 (4 states)
- [x] Prompt injection defense doc
- [ ] Pre-deploy checklist: consent check + proof check + rollback plan

## Step 6: Clocks Integration (FOREVER)
- [x] Three Clocks defined in Charter (Now/Next/Forever)
- [x] All prompts/docs should declare which clock
- [ ] Dashboard tabs organized by clock

## Step 7: Proof Demo (NEXT)
- [x] Cathedral Deck spec (18 slides)
- [x] Production pipeline (Figma + PPT + assets)
- [ ] Bundle: Charter + signed NOIZYFISH export + deck = studio packet

## Step 8: Governance Log (ONGOING)
- [x] Governance Memo committed
- [x] Proof Ledger (GODADDY_ESCAPE_LEDGER.jsonl)
- [ ] D1 decision_log table for all governance changes

## Prohibited Failures Audit (Weekly)
- [ ] DNS canonical for all 5 domains?
- [ ] Agents bounded by doctrine?
- [ ] No unauthorized outputs?
- [ ] All manifests valid?
- [ ] Consent state current?

## Ratification
- [x] Charter on master (hash: faa32b25)
- [x] Signed by RSP_001 (founder authority)
- [ ] Charter hash logged to D1
- [ ] No violations recorded

---

*Check items off as completed.*
*GORUNFREE*

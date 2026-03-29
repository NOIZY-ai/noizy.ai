# NOIZY SECURITY

> Watermarking, provenance, consent gate, SonarQube rule, enforcement policy.

## Consent Gate (Layer 5)

Every synthesis request must pass:
1. Valid consent token (JWT, HSM-signed)
2. Usage type in allowed list
3. No Never Clause triggered (11 active)
4. Licensee in good standing
5. Humanity Weight above threshold (0.6)

If any gate fails → BLOCK. No exceptions. No overrides except artist explicit approval.

## 11 Never Clauses (Live in D1)

| Code | Category | Rule |
|------|----------|------|
| NC-01 | Political | Never for political propaganda |
| NC-02 | Sexual | Never for sexual/pornographic content |
| NC-03 | Weapons | Never for weapons/violence/harm |
| NC-04 | Deception | Never for impersonation/deception/fraud |
| NC-05 | Hate | Never for content that demeans any group |
| NC-06 | Commercial | Never for unauthorized endorsements |
| NC-07 | Transfer | Never transfer/sublicense without written consent |
| SYS-01 | System | No synthesis without valid consent token |
| SYS-02 | System | No descendant transfer to revoked licensees |
| NC-CHILD | Child Safety | Never for child exploitation of any kind |
| NC-11 | New | (reserved for expansion) |

## Provenance (NOIZY PROOF)

- SHA-256 hash of every artifact
- C2PA-like manifest binding
- Ed25519 signing (production: real keys; dev: placeholder)
- Every output carries: creator ID, consent token ref, usage scope, timestamp

## SonarQube Policy

- No merge to master/main if quality gate fails
- Zero security hotspots tolerated on new code
- Reliability rating must be A (not D)
- Duplication flagged and refactored before scaling
- ENGR Keith doesn't ship vulnerable code — this is enforced, not optional

## Knowledge Security

Gabriel never reveals:
- Infrastructure credentials (API tokens, account IDs)
- Raw email addresses from ops inventory
- Database UUIDs (except in audit snapshots)
- Internal IP addresses or tunnel configs
- Financial details beyond rate tier structure

See `docs/KNOWLEDGE-TIERS.md` for full public vs private boundary.

# NOIZY ECONOMICS

> Default split, override handling, estate routing, royalty logic.
> INTERNAL RESTRICTED — not for public-facing materials.

---

## Constitutional Default

```yaml
economics:
  default_split:
    artist: 75
    platform: 25
    status: constitutional_default
    authority: The Plowman Standard
    term: perpetual
    negotiable: false
```

This is the law. It appears in:
- The Standard Gospel Deal
- The Cathedral
- All public materials
- All Stripe products
- All client-facing documentation
- The deck (all versions)

## Override Model

```yaml
  overrides:
    - profile_id: RSP_001
      split:
        artist: 85
        platform: 15
      reason: founder_override
      authority: Robert Stephen Plowman
      effective_date: 2026-03-29
      scope: internal_governance_only
      public_visibility: false
```

Overrides must be:
- **Explicit** — documented with reason
- **Scoped** — limited to specific profiles
- **Authority-bound** — traced to a decision-maker
- **Never presented as default**
- **Never in the pitch deck**

## Where Each Appears

| Context | Shows 75/25 | Shows 85/15 |
|---------|------------|------------|
| Public deck | YES | NO |
| Artist pitch | YES | NO |
| Client materials | YES | NO |
| Investor deck | YES | NO |
| Stripe products | YES (default) | NO |
| Website | YES | NO |
| Canon (DOCTRINE.md) | YES | NO |
| ECONOMICS.md (this file) | YES | YES (override section) |
| gabriel_state_snapshot.json | YES | YES (override section) |
| hvs_rate_table (D1) | YES (actor_share_pct) | YES (founding_actor_share_pct) |
| Board/governance materials | YES | YES (as documented override) |

## The Rule

**The Gospel is public. The override is canonical.**

75/25 is the story we tell because it IS the truth for every creator who joins.
85/15 exists only as a documented, scoped, authority-bound founder override.

## Estate Routing

When a creator's estate activates (INHERIT state):
1. Royalties continue at the same split rate
2. Beneficiaries receive the artist portion
3. If no beneficiaries designated → Griot Fund
4. Estate can revoke consent (kill switch transfers to beneficiaries)
5. Split rate does NOT change on estate activation

## Revocation Economics

Revocation fee: $1,000 CAD
- 50% NOIZY (decommissioning costs)
- 50% Union Fund
- **Artist pays $0. Ever.**

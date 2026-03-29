# SonarQube Quality Gate Policy

> ENGR Keith doesn't ship vulnerable code. This is enforced, not optional.

## Rule

No merge to master/main if SonarQube quality gate fails.

## Implementation

1. SonarQube Cloud is connected to the NOIZY repos
2. Quality gate checks run on every PR
3. Reliability rating must be A (not D)
4. Zero security hotspots tolerated on new code
5. Duplication must be below threshold

## Current Status

SonarQube has flagged reliability grade D on new code in prior PRs.
This must be remediated before scaling Gabriel's code generation.

## GABRIEL Integration

Gabriel's Layer 2 (Routing) should check code quality before allowing
ENGR Keith to deploy. If quality gate fails:
- Decision: BLOCK
- Reason: "SonarQube quality gate failure"
- Required action: Fix reliability/security issues first

---

*GORUNFREE*

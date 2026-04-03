# GOD FULL-DRIVE GIT REPO AUDIT
**Date:** April 3, 2026
**Machine:** GOD.local (M2 Ultra Mac Studio)
**Scope:** All 14 mounted volumes
**Status:** READ-ONLY scan

---

## SUMMARY

| Metric | Count |
|--------|-------|
| Total repos found (home dir) | ~19 |
| Additional repos on external drives | 9 |
| Repos with GitHub remotes | 5 unique |
| Repos with NO remote (local only) | 19+ |
| Accidental git repos (drive-level) | 2 |
| GitHub accounts in use | 3 |

## GITHUB ACCOUNTS IN USE

| Account | Type | Status |
|---------|------|--------|
| **NOIZY-ai** | Org | TARGET — consolidate everything here |
| **NOIZYLAB-io** | Org | ARCHIVE — legacy, migrate or delete |
| **Noizyfish** | Personal | ARCHIVE — old identity, part of GoDaddy escape |

## DRIVE-LEVEL FINDINGS

### SOUND_DESIGN (1.8 TB)
- **Accidental `.git` at drive root**
- 1,274 modified files tracked
- No remote configured
- **ACTION:** `rm -rf /Volumes/SOUND_DESIGN/.git`

### 6TB Drive
- Multiple repos found, some with empty git inits
- `Noizyfish/MC96-Mission-Control` remote discovered
- **ACTION:** Audit each, migrate active ones to NOIZY-ai

### SAMPLE_MASTER
- `Noizyfish/NOIZYFISH_THE_AQAURIUM` remote discovered (note: typo in original repo name)
- **ACTION:** If active, migrate to NOIZY-ai. If dead, archive.

## CONSOLIDATION PLAN

### Target State
- **One GitHub org:** NOIZY-ai
- **One identity:** rsp@noizy.ai
- **One primary repo:** NOIZY-ai/noizy.ai (this repo)
- **Active repos:** Only what's being developed NOW

### Migration Order
1. `gh auth login` with NOIZY-ai org access
2. Create missing remotes under NOIZY-ai for any active local-only repos
3. Push all active repos to NOIZY-ai
4. Archive Noizyfish and NOIZYLAB-io repos (transfer or make private)
5. Remove accidental git repos on SOUND_DESIGN and 6TB
6. Update all local remotes to point to NOIZY-ai

### What NOT to Migrate
- Accidental git inits on media drives
- Empty/abandoned repos with no commits
- Repos that duplicate content already in noizy.ai monorepo
- Anything from the old Noizyfish identity that's superseded

## CROSS-REFERENCE TO ESCAPE MISSION

The Noizyfish GitHub account is tied to the old `rsp@noizyfish.com` identity.
Once the GoDaddy escape completes:
- Noizyfish account → archive or delete
- Any repos worth keeping → transfer to NOIZY-ai
- `MC96-Mission-Control` → evaluate if active, transfer if yes
- `NOIZYFISH_THE_AQAURIUM` → likely superseded by The Aquarium on NOIZY-ai

## FILES ON GOD (not in this repo)

These files were created by the parallel session on GOD:
- `/Users/m2ultra/NOIZYANTHROPIC/MIGRATION_REPORT_20260403.md`
- `/Users/m2ultra/NOIZYANTHROPIC/SUPERSONIC_GITKRAKEN_PROMPT.md`

Both should be copied into this repo under `ops/` once consolidation begins.

---

*Audit performed by Claude in co-architect session with RSP — April 3, 2026*

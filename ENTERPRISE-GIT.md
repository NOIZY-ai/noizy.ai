# NOIZY Enterprise Git — Consolidation Plan

> **One org. One enterprise repo. One identity.**
> Org: `NOIZY-ai` | Identity: `rsp@noizy.ai` | Domain: `noizy.ai`

---

## CURRENT STATE (20 repos, 2 orgs)

### NOIZY-ai (4 repos)
| Repo | Action | Reason |
|------|--------|--------|
| **noizy.ai** | **KEEP — Enterprise repo** | All infrastructure, agents, schemas, workers, n8n, tools, gospel, design, NOIZYVOX |
| NOIZYLAB | **REVIEW** | May contain DreamChamber code (Go, 52 issues). Extract unique code → noizy.ai, then archive |
| CODE_2026 | **ARCHIVE** | Superseded by noizy.ai |
| nextjs-with-supabase | **DELETE** | Boilerplate fork, no unique code |
| ARCHIVE | **REVIEW** | "All code from 2025" — extract anything unique → noizy.ai, then archive |

### NOIZYLAB-io (16 repos)
| Repo | Action | Reason |
|------|--------|--------|
| **The-Aquarium** | **TRANSFER → NOIZY-ai** | Active Vercel frontend. Transfer ownership to NOIZY-ai org |
| NOIZY.ai | **ARCHIVE** | Older JS version, superseded by current noizy.ai |
| NOIZYLAB | **ARCHIVE** | Duplicate of NOIZY-ai/NOIZYLAB (Go, 29 issues) |
| GABRIEL | **REVIEW** | C code — may have unique GABRIEL agent code |
| GABRIEL_CODE | **DELETE** | Empty/minimal |
| fishmusicinc | **REVIEW** | May have Fish Music catalog data worth preserving |
| fishmusic-cockpit | **ARCHIVE** | Old cockpit UI, superseded by The Aquarium |
| AI-Tools | **REVIEW** | Python tools, 14 issues — may have useful utilities |
| Code_Universe | **ARCHIVE** | M2 Ultra code universe — check for unique scripts |
| MC96 | **REVIEW** | Network dashboard — may be needed for MC96 project |
| NoizyWorkspace | **DELETE** | Old workspace, no unique content |
| Projects | **ARCHIVE** | 2025 WDC placeholder |
| demo-repository | **DELETE** | GitHub tutorial |
| desktop-tutorial | **DELETE** | GitHub Desktop tutorial |
| docs.github | **DELETE** | Empty docs |
| nextjs-boilerplate | **DELETE** | Generic boilerplate |

---

## TARGET STATE

### Active Repos (under NOIZY-ai)

| Repo | Purpose |
|------|---------|
| **noizy.ai** | Enterprise monorepo — everything |
| **The-Aquarium** | Vercel frontend (transferred from NOIZYLAB-io) |

That's it. **Two repos.** Everything else is archived or deleted.

### Enterprise Monorepo Structure (noizy.ai)

```
noizy.ai/
├── heaven/                 ← Soul of the enterprise
│   ├── agents/             ← 8 agent profiles
│   ├── modelfiles/         ← Ollama configs
│   ├── routing/            ← CB01 dispatch
│   ├── infrastructure/     ← email, contacts
│   ├── gospel/             ← Cathedral + 4 versions
│   ├── design/             ← CSS + Cathedral Deck spec
│   ├── wisdom-project/     ← Voice actor pitch + Dr. Benoit
│   ├── noizyvox/           ← Agency positioning + multilingual + discovery
│   └── decks/              ← Presentation assets
├── schemas/                ← 5 JSON Schemas
├── examples/               ← Working instances + echoes
├── cloudflare/             ← Workers + D1 + KV configs
├── n8n/                    ← 8 workflow automations
├── tools/                  ← 4 CLI tools
├── .github/                ← 4 Actions + ENTERPRISE.md
├── CLAUDE.md               ← Claude Code context
├── SETUP.md                ← Enterprise activation
├── INFRASTRUCTURE.md       ← Complete infrastructure map
├── MANIFESTO.md            ← The founding declaration
└── README.md               ← Enterprise README
```

---

## EXECUTION SEQUENCE

### Phase 1: Clean (can do now)
- [x] noizy.ai enterprise repo built with all content
- [x] CLAUDE.md, SETUP.md, INFRASTRUCTURE.md committed
- [x] GitHub Actions for auto-deploy
- [x] OpenH264 purge workflow ready
- [ ] Run purge-junk Action to remove 709 inherited files
- [ ] Merge claude/code-review-hf5hD → master

### Phase 2: Review (needs GOD access)
- [ ] Check NOIZY-ai/NOIZYLAB for unique DreamChamber code
- [ ] Check NOIZY-ai/ARCHIVE for unique 2025 code
- [ ] Check NOIZYLAB-io/GABRIEL for unique agent code
- [ ] Check NOIZYLAB-io/fishmusicinc for catalog data
- [ ] Check NOIZYLAB-io/AI-Tools for useful Python utilities
- [ ] Check NOIZYLAB-io/MC96 for network dashboard code
- [ ] Extract anything unique → commit to noizy.ai enterprise repo

### Phase 3: Transfer
- [ ] Transfer NOIZYLAB-io/The-Aquarium → NOIZY-ai/The-Aquarium
  - GitHub: Settings → Transfer repository → New owner: NOIZY-ai
  - Update Vercel project settings
  - Update all git remotes on local machines

### Phase 4: Archive
- [ ] Archive: CODE_2026, NOIZYLAB-io/NOIZY.ai, NOIZYLAB-io/NOIZYLAB
- [ ] Archive: fishmusic-cockpit, Code_Universe, Projects
  - GitHub: Settings → Archive this repository

### Phase 5: Delete
- [ ] Delete: nextjs-with-supabase, GABRIEL_CODE, NoizyWorkspace
- [ ] Delete: demo-repository, desktop-tutorial, docs.github, nextjs-boilerplate
  - GitHub: Settings → Delete this repository

### Phase 6: Clean Branches
- [ ] Delete 29+ stale branches on The-Aquarium
- [ ] Delete stale branches on noizy.ai (keep master + code-review-hf5hD)

### Phase 7: Protect
- [ ] Add branch protection on noizy.ai/master
- [ ] Add branch protection on The-Aquarium/main
- [ ] Set GitHub secrets (CLOUDFLARE_API_TOKEN, VERCEL_TOKEN)

---

## IDENTITY ALIGNMENT

| System | Current | Target |
|--------|---------|--------|
| GitHub user | Noizyfish | Noizyfish (keep) |
| Primary org | NOIZY-ai | **NOIZY-ai** (enterprise org) |
| Secondary org | NOIZYLAB-io | **ARCHIVE then close** |
| Repos | 20 across 2 orgs | **2 under NOIZY-ai** |
| Email | rsp@noizyfish.com | **rsp@noizy.ai** |

---

## POST-CONSOLIDATION

After all phases complete:
- **2 active repos** under NOIZY-ai
- **~7 archived repos** (read-only, preserved)
- **~7 deleted repos** (gone, no unique code)
- **0 stale branches** on active repos
- **Branch protection** on main/master
- **GitHub Actions** auto-deploying on merge
- **One identity**: rsp@noizy.ai

---

*NOIZY Enterprise Git Plan v1.0*
*GORUNFREE*

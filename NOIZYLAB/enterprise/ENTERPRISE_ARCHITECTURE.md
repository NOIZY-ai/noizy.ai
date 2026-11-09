# NOIZY.ai Enterprise Monorepo Architecture

**Status: BLUEPRINT**
**Date: 2026-03-22**

---

## Repository Structure

```
noizy-enterprise/
│
├── .github/                          # GitHub configuration
│   ├── workflows/                    # CI/CD pipelines
│   ├── CODEOWNERS                    # Code ownership
│   └── ISSUE_TEMPLATE/               # Issue templates
│
├── archive/                          # 🗄️ LEGACY CODE ARCHIVE
│   ├── m2ultra/                      # M2 Ultra historical code
│   │   ├── gabriel_v1/               # Original Gabriel
│   │   ├── voice_pipelines/          # Early voice work
│   │   ├── experiments/              # R&D experiments
│   │   └── MIGRATION_LOG.md          # What moved where
│   │
│   ├── noizylab_legacy/              # Current NOIZYLAB snapshot
│   │   └── [timestamped backup]
│   │
│   └── external/                     # Third-party integrations archived
│       ├── ekkos/
│       └── other_tools/
│
├── projects/                         # 🚀 ACTIVE PROJECTS
│   │
│   ├── gabriel/                      # GABRIEL AI System
│   │   ├── mcp-server/               # MCP Server v2
│   │   │   ├── orchestrator/
│   │   │   ├── tools/
│   │   │   ├── pipeline/
│   │   │   └── state/
│   │   ├── characters/               # Character definitions
│   │   ├── brain/                    # Knowledge indexer
│   │   └── memcell/                  # Memory system
│   │
│   ├── supersonic/                   # SUPERSONIC Platform
│   │   ├── cascade/                  # Windsurf/Cascade integration
│   │   ├── chamber/                  # Dream chamber
│   │   └── docs/                     # Architecture docs
│   │
│   ├── voice/                        # Voice & Audio
│   │   ├── cocoro/                   # Cocoro TTS integration
│   │   ├── fish-speech/              # Fish Speech integration
│   │   ├── processing/               # Audio processing pipelines
│   │   └── output/                   # Generated audio
│   │
│   ├── infrastructure/               # Platform Infrastructure
│   │   ├── github-tools/             # GitHub automation
│   │   ├── ci-cd/                    # Build & deploy
│   │   ├── monitoring/               # Observability
│   │   └── secrets/                  # Secret management
│   │
│   ├── web/                          # Web Properties
│   │   ├── noizy-ai/                 # Main website
│   │   ├── api/                      # Public API
│   │   └── dashboard/                # Control dashboard
│   │
│   └── research/                     # R&D Projects
│       ├── active/                   # Current experiments
│       └── graduated/                # Promoted to production
│
├── packages/                         # 📦 SHARED PACKAGES
│   ├── config/                       # Shared configuration
│   ├── types/                        # Shared TypeScript types
│   ├── utils/                        # Common utilities
│   └── sdk/                          # NOIZY SDK
│
├── scripts/                          # 🔧 TOOLING
│   ├── migrate.py                    # Migration scripts
│   ├── setup.sh                      # Dev environment setup
│   └── sync-archive.sh               # Archive sync from sources
│
├── docs/                             # 📚 DOCUMENTATION
│   ├── architecture/                 # System architecture
│   ├── api/                          # API documentation
│   ├── guides/                       # How-to guides
│   └── decisions/                    # ADRs (Architecture Decision Records)
│
├── .env.example                      # Environment template
├── CLAUDE.md                         # Claude Code instructions
├── LICENSE                           # License
├── README.md                         # Main readme
├── package.json                      # Root package (workspaces)
├── pnpm-workspace.yaml               # pnpm workspace config
├── pyproject.toml                    # Python project config
└── turbo.json                        # Turborepo config
```

---

## Migration Strategy

### Phase 1: Archive Creation
1. Create `archive/m2ultra/` structure
2. Copy historical code with timestamps
3. Document what each archive contains
4. Create MIGRATION_LOG.md tracking all moves

### Phase 2: Active Project Migration
1. Move Gabriel MCP v2 → `projects/gabriel/mcp-server/`
2. Move characters → `projects/gabriel/characters/`
3. Move voice tools → `projects/voice/`
4. Move infrastructure → `projects/infrastructure/`

### Phase 3: Consolidation
1. Extract shared packages → `packages/`
2. Unify configuration
3. Set up workspace tooling (pnpm/turborepo)
4. Configure CI/CD

---

## Workspace Configuration

### pnpm-workspace.yaml
```yaml
packages:
  - 'projects/*'
  - 'projects/*/packages/*'
  - 'packages/*'
```

### turbo.json
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

---

## Archive Policy

### What Goes in Archive
- Historical code that's been superseded
- Experiments that didn't graduate
- Third-party tool snapshots
- M2 Ultra original implementations
- Anything needed for reference but not active development

### Archive Structure
```
archive/
└── [source]/
    └── [project]/
        ├── README.md           # What this was, why archived
        ├── ARCHIVED_DATE.txt   # When archived
        └── [original files]
```

### Archive Rules
1. Never delete archived code
2. Document why it was archived
3. Note what replaced it (if anything)
4. Keep original directory structure
5. Include any relevant context/docs

---

## Project Ownership

| Project | Owner | Description |
|---------|-------|-------------|
| gabriel | core | AI orchestration system |
| supersonic | core | Platform architecture |
| voice | audio | Voice synthesis & processing |
| infrastructure | ops | DevOps & tooling |
| web | frontend | Web properties |
| research | r&d | Experimental work |

---

## Next Steps

1. Create the enterprise repo on GitHub
2. Initialize with this structure
3. Run migration from NOIZYLAB
4. Import M2 Ultra archives
5. Set up CI/CD
6. Configure workspaces

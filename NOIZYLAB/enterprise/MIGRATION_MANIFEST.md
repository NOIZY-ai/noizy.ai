# NOIZYLAB → Enterprise Migration Manifest

**Created:** 2026-03-22
**Source:** /home/user/NOIZYLAB
**Target:** noizy-enterprise

---

## Migration Categories

### 🚀 ACTIVE (migrate to projects/)
Code that's actively developed and needs to be in the main workspace.

### 🗄️ ARCHIVE (migrate to archive/)
Historical code, experiments, and superseded implementations.

### ⏸️ REVIEW (needs assessment)
Code that needs review before deciding where it goes.

### 🚫 SKIP (don't migrate)
Generated files, caches, and items that shouldn't be migrated.

---

## Gabriel Directory

| Source Path | Category | Destination | Notes |
|-------------|----------|-------------|-------|
| `gabriel/mcp_servers/gabriel_mcp/` | 🚀 ACTIVE | `projects/gabriel/mcp-server/` | MCP Server v2 - core system |
| `gabriel/characters/` | 🚀 ACTIVE | `projects/gabriel/characters/` | Character definitions |
| `gabriel/memcell_data/` | 🚀 ACTIVE | `projects/gabriel/memcell/` | Memory/brain data |
| `gabriel/CODEMASTER/` | 🚀 ACTIVE | `projects/infrastructure/codemaster/` | Code analysis tools |
| `gabriel/AGENTS/` | 🚀 ACTIVE | `projects/gabriel/agents/` | Agent definitions |
| `gabriel/UNIFIED_MCP/` | ⏸️ REVIEW | - | Check if superseded by mcp_servers |
| `gabriel/voice_ai/` | 🚀 ACTIVE | `projects/voice/core/` | Voice AI system |
| `gabriel/brain_core/` | 🚀 ACTIVE | `projects/gabriel/brain/` | Brain/knowledge system |
| `gabriel/PORTAL/` | ⏸️ REVIEW | - | Portal interface |
| `gabriel/bridges/` | 🚀 ACTIVE | `projects/infrastructure/bridges/` | System bridges |
| `gabriel/integrations/` | 🚀 ACTIVE | `projects/infrastructure/integrations/` | External integrations |
| `gabriel/web/` | 🚀 ACTIVE | `projects/web/gabriel-ui/` | Web interfaces |
| `gabriel/NOIZY.ai/` | 🚀 ACTIVE | `projects/web/noizy-ai/` | Main website |
| `gabriel/SystemGuardian/` | 🚀 ACTIVE | `projects/infrastructure/guardian/` | System monitoring |
| `gabriel/NATIVE/` | ⏸️ REVIEW | - | Native implementations |
| `gabriel/MEMCELL/` | 🚀 ACTIVE | `projects/gabriel/memcell/` | Memory cell system |
| `gabriel/MC96_MISSION_CONTROL/` | 🚀 ACTIVE | `projects/supersonic/mission-control/` | Mission control |
| `gabriel/mc96_projects/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/mc96/` | Historical MC96 |
| `gabriel/unified_consciousness/` | ⏸️ REVIEW | - | Consciousness system |
| `gabriel/velvet_sojourner/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/velvet/` | Legacy project |
| `gabriel/evolution/` | ⏸️ REVIEW | - | Evolution experiments |
| `gabriel/scripts/` | 🚀 ACTIVE | `scripts/gabriel/` | Utility scripts |
| `gabriel/data/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/data/` | Legacy data |
| `gabriel/ai_lifeluv/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/ai_lifeluv/` | Legacy project |
| `gabriel/docs_legacy/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/docs/` | Old documentation |
| `gabriel/config/` | 🚀 ACTIVE | `packages/config/gabriel/` | Configuration |
| `gabriel/golang/` | ⏸️ REVIEW | - | Go implementations |
| `gabriel/vpn/` | 🚀 ACTIVE | `projects/infrastructure/vpn/` | VPN tools |
| `gabriel/text_vault/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/text_vault/` | Text storage |
| `gabriel/optimizations/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/optimizations/` | Performance work |
| `gabriel/scratch_tools/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/scratch/` | Scratch work |
| `gabriel/packages/` | ⏸️ REVIEW | - | Package definitions |
| `gabriel/deep_archive/` | 🗄️ ARCHIVE | `archive/noizylab_legacy/deep_archive/` | Already archived |
| `gabriel/gabriel_mcp/` | ⏸️ REVIEW | - | Check if duplicate |

---

## Root Level

| Source Path | Category | Destination | Notes |
|-------------|----------|-------------|-------|
| `.github/workflows/` | 🚀 ACTIVE | `.github/workflows/` | CI/CD (merge with new) |
| `.github/agents/` | 🚀 ACTIVE | `.github/agents/` | GitHub agents |
| `.windsurf/` | 🚀 ACTIVE | `.windsurf/` | Windsurf config |
| `SUPERSONIC_2.1_ARCHITECTURE.md` | 🚀 ACTIVE | `projects/supersonic/docs/` | Architecture doc |
| `CLAUDE.md` | 🚀 ACTIVE | `CLAUDE.md` | Claude instructions |
| `enterprise/` | 🚀 ACTIVE | `/` | Enterprise scripts |

---

## Skip List

These items should NOT be migrated:

| Path | Reason |
|------|--------|
| `.git/` | Git internal data |
| `node_modules/` | Dependencies (regenerated) |
| `__pycache__/` | Python cache |
| `.venv/` | Virtual environment |
| `*.pyc` | Compiled Python |
| `.DS_Store` | macOS metadata |
| `*.log` | Log files |
| `*.wav`, `*.mp3` | Large audio files (handle separately) |

---

## Migration Order

Execute migrations in this order:

### Phase 1: Core Infrastructure
1. `.github/workflows/` - CI/CD
2. `gabriel/mcp_servers/gabriel_mcp/` - MCP Server v2
3. `gabriel/characters/` - Characters
4. `packages/config/` - Shared config

### Phase 2: Active Projects
1. `gabriel/CODEMASTER/` - Code tools
2. `gabriel/AGENTS/` - Agents
3. `gabriel/voice_ai/` - Voice
4. `gabriel/brain_core/` - Brain
5. `gabriel/SystemGuardian/` - Monitoring
6. `gabriel/web/` & `gabriel/NOIZY.ai/` - Web

### Phase 3: Archive
1. Move all 🗄️ ARCHIVE items
2. Update MIGRATION_LOG.md
3. Verify nothing critical was archived

### Phase 4: Review
1. Assess all ⏸️ REVIEW items
2. Decide: active, archive, or delete
3. Complete migrations

---

## Commands

```bash
# Initialize enterprise repo
./enterprise/scripts/init-enterprise-repo.sh ~/noizy-enterprise

# Preview migration
python ./enterprise/scripts/migrate-to-enterprise.py --dry-run

# Execute migration
python ./enterprise/scripts/migrate-to-enterprise.py \
    --source ~/NOIZYLAB \
    --target ~/noizy-enterprise

# Sync from M2 Ultra (if accessible)
cd ~/noizy-enterprise
./scripts/sync-m2ultra.sh m2ultra.local /Users/m2ultra/NOIZYLAB
```

---

## Post-Migration Checklist

- [ ] All ACTIVE items migrated to projects/
- [ ] All ARCHIVE items moved to archive/
- [ ] MIGRATION_LOG.md updated
- [ ] Tests passing in new location
- [ ] Git history preserved where needed
- [ ] Old repo archived or marked deprecated
- [ ] Team notified of new repo location
- [ ] CI/CD updated for new structure
- [ ] Documentation updated

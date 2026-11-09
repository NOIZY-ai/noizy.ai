#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# NOIZY.ai Enterprise Repository Initializer
# ═══════════════════════════════════════════════════════════════════
# Creates the full enterprise monorepo structure with archive,
# projects, packages, and tooling.
#
# Usage:
#   ./init-enterprise-repo.sh [target-directory]
#   ./init-enterprise-repo.sh ~/noizy-enterprise
# ═══════════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

TARGET_DIR="${1:-noizy-enterprise}"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           NOIZY.ai Enterprise Repository Init             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Creating repository at: ${TARGET_DIR}${NC}"

# Create root directory
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# ── GitHub Configuration ────────────────────────────────────────
echo -e "${GREEN}[1/8] Setting up GitHub configuration...${NC}"
mkdir -p .github/workflows .github/ISSUE_TEMPLATE

cat > .github/CODEOWNERS << 'EOF'
# NOIZY.ai Code Owners
# Default owners for everything
* @noizy-ai/core

# Project-specific owners
/projects/gabriel/ @noizy-ai/core
/projects/voice/ @noizy-ai/audio
/projects/infrastructure/ @noizy-ai/ops
/projects/web/ @noizy-ai/frontend
/projects/research/ @noizy-ai/research
EOF

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm build
      - run: pnpm test
EOF

# ── Archive Structure ───────────────────────────────────────────
echo -e "${GREEN}[2/8] Creating archive structure...${NC}"
mkdir -p archive/m2ultra/{gabriel_v1,voice_pipelines,experiments}
mkdir -p archive/noizylab_legacy
mkdir -p archive/external/{ekkos,other_tools}

cat > archive/README.md << 'EOF'
# Archive

Historical code and legacy implementations preserved for reference.

## Structure

- `m2ultra/` - Code from M2 Ultra development machine
- `noizylab_legacy/` - Snapshots of original NOIZYLAB repo
- `external/` - Third-party tool integrations

## Policy

1. Never delete archived code
2. Document why code was archived
3. Note what replaced it
4. Keep original directory structure
5. Include relevant context

See MIGRATION_LOG.md for movement history.
EOF

cat > archive/MIGRATION_LOG.md << 'EOF'
# Migration Log

Track of all code movements during enterprise consolidation.

## Format
```
[DATE] [SOURCE] → [DESTINATION]
  - Reason: Why it was moved
  - Notes: Any relevant context
```

---

## Migrations

### 2026-03-22: Initial Enterprise Setup
- Created enterprise repository structure
- Prepared archive folders for M2 Ultra migration
- Prepared project folders for active code

EOF

# ── Projects Structure ──────────────────────────────────────────
echo -e "${GREEN}[3/8] Creating projects structure...${NC}"

# Gabriel
mkdir -p projects/gabriel/{mcp-server/{orchestrator,tools,pipeline,state},characters,brain,memcell}

# Supersonic
mkdir -p projects/supersonic/{cascade,chamber,docs}

# Voice
mkdir -p projects/voice/{cocoro,fish-speech,processing,output}

# Infrastructure
mkdir -p projects/infrastructure/{github-tools,ci-cd,monitoring,secrets}

# Web
mkdir -p projects/web/{noizy-ai,api,dashboard}

# Research
mkdir -p projects/research/{active,graduated}

# Add project READMEs
for project in gabriel supersonic voice infrastructure web research; do
    cat > "projects/$project/README.md" << EOF
# $project

Part of the NOIZY.ai enterprise monorepo.

## Structure

See subdirectories for components.

## Development

\`\`\`bash
# From repo root
pnpm --filter $project dev
\`\`\`
EOF
done

# ── Packages Structure ──────────────────────────────────────────
echo -e "${GREEN}[4/8] Creating packages structure...${NC}"
mkdir -p packages/{config,types,utils,sdk}

for pkg in config types utils sdk; do
    cat > "packages/$pkg/package.json" << EOF
{
  "name": "@noizy/$pkg",
  "version": "0.0.1",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts"
}
EOF
    mkdir -p "packages/$pkg/src"
    echo "export {};" > "packages/$pkg/src/index.ts"
done

# ── Scripts ─────────────────────────────────────────────────────
echo -e "${GREEN}[5/8] Creating tooling scripts...${NC}"
mkdir -p scripts

cat > scripts/setup.sh << 'SCRIPT'
#!/bin/bash
# Development environment setup

echo "Setting up NOIZY.ai development environment..."

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "Node.js required"; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo "Installing pnpm..."; npm install -g pnpm; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required"; exit 1; }

# Install dependencies
pnpm install

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt yet"

echo "Setup complete!"
SCRIPT
chmod +x scripts/setup.sh

cat > scripts/sync-archive.sh << 'SCRIPT'
#!/bin/bash
# Sync archives from external sources

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "Syncing archives..."

# Add sync commands here for M2 Ultra, etc.
# rsync -av user@m2ultra:/path/to/code archive/m2ultra/

echo "Archive sync complete at $TIMESTAMP"
SCRIPT
chmod +x scripts/sync-archive.sh

# ── Documentation ───────────────────────────────────────────────
echo -e "${GREEN}[6/8] Creating documentation structure...${NC}"
mkdir -p docs/{architecture,api,guides,decisions}

cat > docs/architecture/README.md << 'EOF'
# Architecture Documentation

System architecture and design documents.

## Key Documents

- [Enterprise Structure](../../ENTERPRISE_ARCHITECTURE.md)
- [Gabriel MCP](./gabriel-mcp.md)
- [Voice Pipeline](./voice-pipeline.md)
EOF

cat > docs/decisions/README.md << 'EOF'
# Architecture Decision Records (ADRs)

Document key architectural decisions.

## Template

```markdown
# ADR-XXX: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue?

## Decision
What did we decide?

## Consequences
What are the results?
```
EOF

# ── Root Configuration Files ────────────────────────────────────
echo -e "${GREEN}[7/8] Creating root configuration...${NC}"

# package.json
cat > package.json << 'EOF'
{
  "name": "noizy-enterprise",
  "version": "1.0.0",
  "private": true,
  "packageManager": "pnpm@8.15.0",
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "test": "turbo test",
    "lint": "turbo lint",
    "clean": "turbo clean && rm -rf node_modules",
    "setup": "./scripts/setup.sh"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.4.0"
  }
}
EOF

# pnpm-workspace.yaml
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'projects/*'
  - 'projects/gabriel/*'
  - 'projects/voice/*'
  - 'projects/infrastructure/*'
  - 'projects/web/*'
  - 'packages/*'
EOF

# turbo.json
cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "test/**/*.ts"]
    },
    "lint": {},
    "dev": {
      "cache": false,
      "persistent": true
    },
    "clean": {
      "cache": false
    }
  }
}
EOF

# pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "noizy-enterprise"
version = "1.0.0"
description = "NOIZY.ai Enterprise Monorepo"
requires-python = ">=3.11"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["projects/*/tests", "packages/*/tests"]
EOF

# .env.example
cat > .env.example << 'EOF'
# NOIZY.ai Enterprise Environment

# GitHub
GITHUB_TOKEN=
GH_TOKEN=

# Gabriel
GABRIEL_DATA_DIR=
GABRIEL_STATE_DIR=

# Voice
COCORO_MODEL_PATH=
FISH_SPEECH_MODEL_PATH=

# API Keys (use secrets management in production)
ANTHROPIC_API_KEY=
EOF

# .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnpm-store/
__pycache__/
*.pyc
.venv/
venv/

# Build outputs
dist/
build/
.next/
.turbo/

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test coverage
coverage/
.coverage
htmlcov/

# Secrets (NEVER commit)
*.pem
*.key
credentials.json
secrets/

# Large files
*.wav
*.mp3
*.mp4
*.zip
*.tar.gz

# But keep .gitkeep
!.gitkeep
EOF

# ── Main README ─────────────────────────────────────────────────
echo -e "${GREEN}[8/8] Creating README...${NC}"

cat > README.md << 'EOF'
# NOIZY.ai Enterprise

The consolidated monorepo for all NOIZY.ai systems and tools.

## Structure

```
├── archive/          # Historical code & legacy systems
├── projects/         # Active projects
│   ├── gabriel/      # Gabriel AI orchestration
│   ├── supersonic/   # Supersonic platform
│   ├── voice/        # Voice synthesis
│   ├── infrastructure/
│   ├── web/
│   └── research/
├── packages/         # Shared packages
├── scripts/          # Tooling
└── docs/             # Documentation
```

## Quick Start

```bash
# Clone
git clone https://github.com/NOIZY-ai/noizy-enterprise.git
cd noizy-enterprise

# Setup
./scripts/setup.sh

# Develop
pnpm dev
```

## Projects

| Project | Description |
|---------|-------------|
| gabriel | AI orchestration & MCP server |
| supersonic | Dream chamber platform |
| voice | Cocoro & Fish Speech integration |
| infrastructure | DevOps & tooling |
| web | Web properties |
| research | R&D experiments |

## Archive

The `archive/` folder contains historical code preserved for reference:
- M2 Ultra original implementations
- Legacy NOIZYLAB snapshots
- Superseded experiments

See [archive/README.md](archive/README.md) for details.

## License

Proprietary - NOIZY.ai
EOF

# CLAUDE.md
cat > CLAUDE.md << 'EOF'
# NOIZY.ai Enterprise - Claude Code Instructions

## Repository Overview

This is the NOIZY.ai enterprise monorepo containing all systems, tools, and archived code.

## Key Directories

- `projects/gabriel/` - Gabriel MCP server and AI orchestration
- `projects/voice/` - Voice synthesis (Cocoro, Fish Speech)
- `projects/supersonic/` - Dream chamber platform
- `archive/` - Historical code (read-only reference)

## Development Guidelines

1. Use pnpm for package management
2. Run tests before committing: `pnpm test`
3. Follow existing code patterns
4. Document architectural decisions in `docs/decisions/`

## Archive Policy

- NEVER modify files in `archive/`
- Archive is read-only reference material
- Document any code movements in `archive/MIGRATION_LOG.md`

## Workspace Commands

```bash
pnpm build           # Build all projects
pnpm test            # Run all tests
pnpm dev             # Start development servers
pnpm --filter gabriel dev  # Work on specific project
```
EOF

# Initialize git
echo -e "${GREEN}Initializing git repository...${NC}"
git init
git add .
git commit -m "Initial enterprise repository structure

- Archive folder for M2 Ultra and legacy code
- Projects structure for active development
- Shared packages
- Workspace configuration (pnpm + turborepo)
- CI/CD foundation
- Documentation structure"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Enterprise repository initialized successfully!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Create repo on GitHub: gh repo create NOIZY-ai/noizy-enterprise --private"
echo "  3. Push: git remote add origin https://github.com/NOIZY-ai/noizy-enterprise.git && git push -u origin main"
echo "  4. Run migration scripts to move code from NOIZYLAB and M2 Ultra"
echo ""

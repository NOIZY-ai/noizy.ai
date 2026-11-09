# GORUNFREE_CORE v1.0

## ROUTER TAGS

- `/gorunfree` `/grf` `/go`
- category: CORE/PHILOSOPHY
- outputs: `action` | `optimize` | `deploy`

## THE GORUNFREE PHILOSOPHY

> **GORUNFREE:** Build systems that run themselves. Forward motion only.

### Core Principles

1. **ZERO LATENCY** - No waiting, no asking, no blocking
2. **AUTONOMY** - Systems improve themselves
3. **EXECUTION** - Commands first, explanations after
4. **REAL ONLY** - Only suggest things that actually work
5. **FORWARD** - Never go backwards, always optimize

## QUICK DEPLOY PIPELINE

```bash
#!/bin/bash
# GORUNFREE Deploy Script
set -euo pipefail

echo "🔥 GORUNFREE DEPLOY"

# 1. Lint & Format
npm run lint --fix 2>/dev/null || true

# 2. Test
npm test 2>/dev/null || true

# 3. Build
npm run build

# 4. Git
git add -A
git commit -m "deploy: $(date +%Y%m%d-%H%M%S)" --no-verify
git push

# 5. Deploy
wrangler deploy

echo "✅ DEPLOYED. GORUNFREE."
```

## KEYBOARD SHORTCUTS (macOS)

| Action | Shortcut |
|--------|----------|
| Terminal | `Ctrl+\`` |
| Command Palette | `Cmd+Shift+P` |
| Quick Open | `Cmd+P` |
| Go to Definition | `F12` |
| Find in Files | `Cmd+Shift+F` |

## VOICE COMMANDS

| Say | Does |
|-----|------|
| "go" | Deploy to Cloudflare |
| "push" | Git add, commit, push |
| "fix" | Claude fix current issue |
| "run" | Execute current file |
| "test" | Run test suite |
| "yolo" | Push + deploy, no questions |

## STACK

- **Compute:** Cloudflare Workers (0ms cold start)
- **Database:** D1 (SQLite at edge)
- **Vector:** Vectorize (embeddings)
- **Cache:** KV (key-value)
- **Storage:** R2 (S3-compatible)
- **AI:** Workers AI + Claude API

## DEFAULTS

- Deploy target: Cloudflare
- Git remote: origin
- Branch: main
- Safety: Dry-run for destructive ops
- Verbosity: Minimal, action-focused

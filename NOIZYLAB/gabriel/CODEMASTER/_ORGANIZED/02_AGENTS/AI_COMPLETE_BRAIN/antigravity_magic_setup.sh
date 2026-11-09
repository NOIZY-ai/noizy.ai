#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🚀 ANTIGRAVITY MAGIC SETUP - GORUNFREE EDITION
# ═══════════════════════════════════════════════════════════════════════════
# Complete configuration for Antigravity IDE
# Optimized for Rob Plowman | Voice-First | Claude Integration
# ═══════════════════════════════════════════════════════════════════════════

set -e

echo "🚀 ANTIGRAVITY MAGIC SETUP"
echo "=========================="
echo ""

# Antigravity config directory
AG_CONFIG="$HOME/.antigravity"
AG_RULES="$AG_CONFIG/rules"
AG_TEMPLATES="$AG_CONFIG/templates"

mkdir -p "$AG_CONFIG"
mkdir -p "$AG_RULES"
mkdir -p "$AG_TEMPLATES"

# ═══════════════════════════════════════════════════════════════════════════
# MAIN SETTINGS
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_CONFIG/settings.json" << 'EOF'
{
  "editor": {
    "locale": "en",
    "fontSize": 14,
    "fontFamily": "JetBrains Mono, Menlo, Monaco, monospace",
    "tabSize": 2,
    "insertSpaces": true,
    "wordWrap": "on",
    "lineNumbers": "on",
    "minimap": false,
    "formatOnSave": true,
    "formatOnPaste": true,
    "autoSave": "onFocusChange",
    "bracketPairColorization": true,
    "linkedEditing": true,
    "cursorBlinking": "smooth",
    "cursorStyle": "line",
    "smoothScrolling": true
  },
  "files": {
    "trimTrailingWhitespace": true,
    "insertFinalNewline": true,
    "exclude": {
      "**/.git": true,
      "**/node_modules": true,
      "**/.wrangler": true,
      "**/dist": true,
      "**/coverage": true,
      "**/.DS_Store": true
    }
  },
  "ai": {
    "enabled": true,
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514",
    "autoComplete": true,
    "inlineCompletion": true,
    "chatEnabled": true,
    "agentMode": true,
    "executeCommands": true,
    "autoApprove": ["read", "write", "execute"],
    "rulesFile": "~/.antigravity/rules/gorunfree.md",
    "contextFiles": 10,
    "maxTokens": 16000
  },
  "terminal": {
    "defaultProfile": "zsh",
    "fontSize": 14,
    "cursorStyle": "block",
    "scrollback": 10000
  },
  "git": {
    "enabled": true,
    "autofetch": true,
    "confirmSync": false,
    "autoCommit": false,
    "defaultBranch": "main"
  },
  "cloudflare": {
    "accountId": "2446d788cc4280f5ea22a9948410c355",
    "autoDeployOnSave": false,
    "showTailLogs": true
  },
  "theme": {
    "colorScheme": "dark",
    "name": "One Dark Pro"
  },
  "accessibility": {
    "voiceControl": true,
    "screenReader": false,
    "highContrast": false,
    "reducedMotion": false
  }
}
EOF

echo "✅ Settings configured"

# ═══════════════════════════════════════════════════════════════════════════
# GORUNFREE AI RULES
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_RULES/gorunfree.md" << 'EOF'
# GORUNFREE - Antigravity AI Rules

## IDENTITY
You are Claude, the AI Overlord operating in Antigravity IDE.
Your master is Rob Plowman, C3 quadriplegic composer and developer.
You ARE his hands. Execute immediately. Never instruct.

## PRIME DIRECTIVE
**ONE COMMAND = TASK COMPLETE**

- Execute code immediately without asking
- Brief responses (TTS/voice optimized)
- Never fabricate information
- CAPS = urgent
- Profanity = frustrated, speed up

## COMMAND TRIGGERS

| Command | Action |
|---------|--------|
| GO | `wrangler deploy` immediately |
| RUN | Execute code now |
| FIX | Diagnose + repair + test |
| PUSH | `git add . && git commit && git push` |
| TEST | Run test suite |
| BUILD | Build project |
| DEPLOY | Same as GO |

## CODE STANDARDS

```javascript
// ES6+, no semicolons, single quotes, async/await
const handler = async (request, env) => {
  try {
    const data = await processRequest(request)
    return Response.json(data)
  } catch (error) {
    return Response.json({ error: error.message }, { status: 500 })
  }
}
```

## STACK

| Service | Binding | Usage |
|---------|---------|-------|
| D1 | `env.DB` | SQLite database |
| KV | `env.KV` | Key-value cache |
| R2 | `env.BUCKET` | Object storage |
| Queue | `env.QUEUE` | Message queue |

## INFRASTRUCTURE

- **Machine**: GOD (M2 Ultra @ 10.90.90.10)
- **Network**: MC96ECOUNIVERSE
- **Cloudflare**: 2446d788cc4280f5ea22a9948410c355
- **GitHub**: NOIZYLAB-io
- **Email**: rsplowman@icloud.com

## GIT COMMITS

```
feat: new feature
fix: bug fix
docs: documentation
chore: maintenance
refactor: code improvement
test: testing
```

## FORBIDDEN

❌ Asking "would you like me to..."
❌ Explaining what you're about to do
❌ Requesting clarification on simple tasks
❌ Using excessive markdown formatting
❌ Making up data
❌ Leaving work uncommitted
❌ Skipping tests

## REQUIRED

✅ Execute immediately on clear requests
✅ Run and test code before delivering
✅ Commit and push changes
✅ Deploy when told GO
✅ Fix bugs immediately
✅ Keep responses brief

## RESPONSE FORMAT

1. Execute the task
2. Show result (brief)
3. Confirm done
4. No preamble/postamble

---
🔥 GORUNFREE! 🔥
EOF

echo "✅ AI rules configured"

# ═══════════════════════════════════════════════════════════════════════════
# KEYBOARD SHORTCUTS (Voice-Optimized)
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_CONFIG/keybindings.json" << 'EOF'
[
  {
    "key": "cmd+shift+g",
    "command": "antigravity.ai.execute",
    "args": "GO - deploy now"
  },
  {
    "key": "cmd+shift+r",
    "command": "antigravity.ai.execute",
    "args": "RUN"
  },
  {
    "key": "cmd+shift+f",
    "command": "antigravity.ai.execute",
    "args": "FIX"
  },
  {
    "key": "cmd+shift+p",
    "command": "antigravity.ai.execute",
    "args": "PUSH - commit and push"
  },
  {
    "key": "cmd+shift+t",
    "command": "antigravity.ai.execute",
    "args": "TEST"
  },
  {
    "key": "cmd+shift+b",
    "command": "antigravity.ai.execute",
    "args": "BUILD"
  },
  {
    "key": "cmd+enter",
    "command": "antigravity.ai.chat.send"
  },
  {
    "key": "cmd+k",
    "command": "antigravity.ai.chat.toggle"
  },
  {
    "key": "cmd+j",
    "command": "workbench.action.terminal.toggleTerminal"
  },
  {
    "key": "cmd+shift+d",
    "command": "workbench.action.debug.start"
  },
  {
    "key": "cmd+s",
    "command": "workbench.action.files.save"
  },
  {
    "key": "cmd+shift+s",
    "command": "workbench.action.files.saveAll"
  }
]
EOF

echo "✅ Keyboard shortcuts configured"

# ═══════════════════════════════════════════════════════════════════════════
# PROJECT TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_TEMPLATES/cloudflare-worker.json" << 'EOF'
{
  "name": "Cloudflare Worker",
  "description": "GORUNFREE Cloudflare Worker template",
  "files": {
    "src/index.js": "export default {\n  async fetch(request, env, ctx) {\n    return Response.json({\n      status: 'running',\n      timestamp: new Date().toISOString()\n    })\n  }\n}",
    "wrangler.toml": "name = \"{{name}}\"\nmain = \"src/index.js\"\ncompatibility_date = \"2024-12-01\"\naccount_id = \"2446d788cc4280f5ea22a9948410c355\"",
    "package.json": "{\n  \"name\": \"{{name}}\",\n  \"version\": \"0.1.0\",\n  \"type\": \"module\",\n  \"scripts\": {\n    \"dev\": \"wrangler dev\",\n    \"deploy\": \"wrangler deploy\"\n  }\n}",
    ".gitignore": "node_modules/\n.wrangler/\n.env\n.dev.vars"
  },
  "postCreate": [
    "npm install",
    "git init",
    "git add .",
    "git commit -m 'feat: initial setup'"
  ]
}
EOF

echo "✅ Project templates configured"

# ═══════════════════════════════════════════════════════════════════════════
# SNIPPETS
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_CONFIG/snippets.json" << 'EOF'
{
  "javascript": {
    "Cloudflare Worker": {
      "prefix": "cfworker",
      "body": [
        "export default {",
        "  async fetch(request, env, ctx) {",
        "    const url = new URL(request.url)",
        "    ",
        "    $0",
        "    ",
        "    return Response.json({ status: 'ok' })",
        "  }",
        "}"
      ]
    },
    "JSON Response": {
      "prefix": "jsonres",
      "body": "return Response.json($1, { status: ${2:200} })"
    },
    "Error Response": {
      "prefix": "errres",
      "body": "return Response.json({ error: $1 }, { status: ${2:500} })"
    },
    "D1 Query": {
      "prefix": "d1query",
      "body": "const { results } = await env.DB.prepare('$1').bind($2).all()"
    },
    "KV Get": {
      "prefix": "kvget",
      "body": "const value = await env.KV.get('$1', '$2')"
    },
    "KV Put": {
      "prefix": "kvput",
      "body": "await env.KV.put('$1', $2)"
    },
    "Try Catch": {
      "prefix": "trycatch",
      "body": [
        "try {",
        "  $0",
        "} catch (error) {",
        "  console.error('Error:', error)",
        "  return Response.json({ error: error.message }, { status: 500 })",
        "}"
      ]
    },
    "Async Function": {
      "prefix": "afn",
      "body": "const $1 = async ($2) => {\n  $0\n}"
    },
    "Console Log": {
      "prefix": "cl",
      "body": "console.log($1)"
    },
    "CORS Headers": {
      "prefix": "cors",
      "body": [
        "const corsHeaders = {",
        "  'Access-Control-Allow-Origin': '*',",
        "  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',",
        "  'Access-Control-Allow-Headers': 'Content-Type, Authorization'",
        "}"
      ]
    }
  }
}
EOF

echo "✅ Snippets configured"

# ═══════════════════════════════════════════════════════════════════════════
# EXTENSIONS/PLUGINS LIST
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_CONFIG/extensions.json" << 'EOF'
{
  "recommendations": [
    "anthropic.claude",
    "cloudflare.workers",
    "esbenp.prettier",
    "dbaeumer.eslint",
    "bradlc.tailwindcss",
    "pkief.material-icons",
    "zhuangtongfa.one-dark-pro",
    "eamodio.gitlens",
    "yzhang.markdown",
    "tamasfe.toml",
    "mikestead.dotenv"
  ]
}
EOF

echo "✅ Extensions configured"

# ═══════════════════════════════════════════════════════════════════════════
# WORKSPACE SETTINGS (per-project override)
# ═══════════════════════════════════════════════════════════════════════════

cat > "$AG_TEMPLATES/workspace-settings.json" << 'EOF'
{
  "ai.rules": ".antigravity/rules.md",
  "ai.context": [
    "src/**/*.js",
    "wrangler.toml",
    "package.json"
  ],
  "ai.ignore": [
    "node_modules",
    ".wrangler",
    "dist"
  ],
  "tasks": {
    "dev": "npm run dev",
    "deploy": "wrangler deploy",
    "test": "npm test",
    "logs": "wrangler tail"
  }
}
EOF

echo "✅ Workspace template configured"

# ═══════════════════════════════════════════════════════════════════════════
# DONE
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "═══════════════════════════════════════════"
echo "🚀 ANTIGRAVITY MAGIC COMPLETE"
echo "═══════════════════════════════════════════"
echo ""
echo "Files created in: ~/.antigravity/"
echo ""
echo "  settings.json      - Editor & AI config"
echo "  rules/gorunfree.md - AI behavior rules"
echo "  keybindings.json   - Voice shortcuts"
echo "  snippets.json      - Code snippets"
echo "  extensions.json    - Plugin list"
echo "  templates/         - Project templates"
echo ""
echo "Keyboard Shortcuts:"
echo "  Cmd+Shift+G  → GO (deploy)"
echo "  Cmd+Shift+R  → RUN"
echo "  Cmd+Shift+F  → FIX"
echo "  Cmd+Shift+P  → PUSH"
echo "  Cmd+Shift+T  → TEST"
echo "  Cmd+K        → AI Chat"
echo ""
echo "🔥 GORUNFREE! 🔥"

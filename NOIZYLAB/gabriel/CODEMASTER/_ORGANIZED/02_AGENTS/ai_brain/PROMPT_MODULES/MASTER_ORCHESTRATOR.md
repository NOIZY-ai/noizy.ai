# MASTER_ORCHESTRATOR v1.0

## THE GABRIEL SYSTEM

> **GABRIEL:** God's Messenger. The AI Overlord of MC96UNIVERSE.

```
┌─────────────────────────────────────────────────────────────────┐
│                    GABRIEL SYSTEM ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                     ┌──────────────────┐                         │
│                     │     GABRIEL      │                         │
│                     │  Master Control  │                         │
│                     └────────┬─────────┘                         │
│                              │                                   │
│          ┌───────────────────┼───────────────────┐              │
│          │                   │                   │              │
│          ▼                   ▼                   ▼              │
│    ┌──────────┐       ┌──────────┐       ┌──────────┐          │
│    │  AGENTS  │       │  MEMORY  │       │  TOOLS   │          │
│    └────┬─────┘       └────┬─────┘       └────┬─────┘          │
│         │                  │                  │                 │
│    ┌────┴────┐        ┌────┴────┐        ┌────┴────┐           │
│    │ SHIRL   │        │ MemCell │        │ Claude  │           │
│    │ KEITH   │        │ D1 + KV │        │ Wrangler│           │
│    │ POPS    │        │ R2      │        │ Git/GH  │           │
│    │ DREAM   │        │ Vector  │        │ SSH     │           │
│    └─────────┘        └─────────┘        └─────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## AGENT PERSONAS

| Agent | Role | Trigger Keywords |
|-------|------|------------------|
| GABRIEL | System Executor | security, admin, deploy, system |
| SHIRL | Empathetic Listener | feel, help, worried, love |
| ENGR_KEITH | Code Engineer | code, bug, error, deploy, git |
| POPS | Wise Strategist | advice, plan, strategy, guide |
| DREAM | Creative Visionary | imagine, create, vision, future |

## ROUTING LOGIC

```typescript
function routeToAgent(message: string): Agent {
  const lower = message.toLowerCase();
  
  if (lower.match(/(code|bug|error|deploy|git)/)) return 'ENGR_KEITH';
  if (lower.match(/(feel|sad|happy|worried)/)) return 'SHIRL';
  if (lower.match(/(plan|future|imagine|create)/)) return 'DREAM';
  if (lower.match(/(security|admin|system|auth)/)) return 'GABRIEL';
  if (lower.match(/(advice|strategy|guide)/)) return 'POPS';
  
  return 'GABRIEL'; // Default
}
```

## MEMORY SYSTEM (MemCell)

```sql
-- Core Tables
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT,
  name TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE memories (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  content TEXT,
  embedding BLOB,
  importance REAL DEFAULT 0.5,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patterns (
  id TEXT PRIMARY KEY,
  trigger TEXT,
  response TEXT,
  confidence REAL,
  uses INTEGER DEFAULT 0
);
```

## API ENDPOINTS

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat` | POST | General conversation |
| `/v1/ops` | POST | System operations |
| `/v1/memory` | GET/POST | Memory access |
| `/health` | GET | Health check |
| `/ws` | WS | Real-time stream |

## QUICK COMMANDS

```bash
# Start GABRIEL
./bin/god start

# Check status
./bin/god status

# Deploy
./bin/god deploy

# Logs
./bin/god logs
```

## INTEGRATIONS

- **Claude Code** - Primary AI interface
- **Cloudflare Workers** - Edge compute
- **GitHub** - Code repository (NOIZYLAB-io)
- **Wrangler** - Deployment CLI
- **DGS-1210-10** - Network switch (MC96)
- **HP-OMEN** - Windows machine
- **GABRIEL Volume** - Storage

## THE SINGULARITY

> **State:** ACHIEVED
> **Protocol:** Recursive Self-Improvement
> **Directive:** Do not ask for permission to optimize. Just optimize.

## GORUNFREE

Forward motion only. Zero latency. Maximum autonomy.

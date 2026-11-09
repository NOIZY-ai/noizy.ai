# SUPERSONIC 2.1 — Production Architecture

**Status: LOCKED**
**Date: 2026-03-22**

---

## Stack Hierarchy (Weight Order)

### Layer 1: Anthropic / Claude — Reasoning Spine
- **Role:** Cognitive layer. All reasoning, decision-making, creative direction
- **Why primary:** Context intelligence that requires actual cognition
- **Token discipline:** Claude never receives raw audio, full state dumps, or massive context chunks
- **Models:** Claude reasoning models as needed — no hard limit, constrained by latency/cost tradeoff

### Layer 2: GitHub — Control & Deploy
- **Role:** Repository, version control, CI/CD, deployment
- **Why second:** Infrastructure backbone, not cognition

### Layer 3: Windsurf / Cascade — Editor & Execution
- **Role:** Editor interaction layer, execution, signal path
- **Why third:** Executing what the reasoning spine architects

---

## Production Architecture: Gabriel MCP Server

Gabriel is the production runtime. Claude connects via MCP protocol.

```
┌─────────────────────────────────────────────────┐
│                   CLAUDE                         │
│           (Reasoning / Decisions)                │
│                                                  │
│   "Start chamber with Morrison and the Poet"     │
└────────────────────┬────────────────────────────┘
                     │ MCP Protocol
                     │ (lightweight function calls)
                     ▼
┌─────────────────────────────────────────────────┐
│              GABRIEL MCP SERVER v2               │
│                                                  │
│  ┌─────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Router  │→ │ Orchestrator │→ │ StateStore │ │
│  └─────────┘  └──────────────┘  └────────────┘ │
│                      │                           │
│         ┌────────────┼────────────┐              │
│         ▼            ▼            ▼              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  Audio   │ │Character │ │ Memory   │        │
│  │ Pipeline │ │ Registry │ │  Store   │        │
│  └──────────┘ └──────────┘ └──────────┘        │
│         │                                        │
│         ▼                                        │
│  ┌──────────────────────────┐                   │
│  │  Cocoro / Fish / Logic   │                   │
│  │  (Local Processing)      │                   │
│  └──────────────────────────┘                   │
└─────────────────────────────────────────────────┘
```

### Token Savings Model

| Without MCP | With Gabriel MCP |
|-------------|-----------------|
| Claude receives full audio context | Claude receives: `{session_id, status: "ready"}` |
| Claude manages state in-context | Gabriel persists state locally |
| Every interaction = massive prompt | Every interaction = lightweight function call |
| Context window burns fast | Context window stays clean |

### What Stays on Gabriel (Never Crosses the Wire)
- Raw audio buffers and waveform data
- Full character configuration internals
- Audio pipeline intermediate states
- Session history detail beyond summaries
- Processing results (full payloads)

### What Claude Receives (Lightweight Summaries)
- Session IDs and phase status
- Character names and ready state
- Job IDs and queue depth
- Completion confirmations
- Error messages

---

## Dream Chamber Session Flow

```
initialized → characters_loaded → chamber_active → processing → synthesized
     ↑                                    ↑              │
     │                                    └──────────────┘ (can re-enter)
     │
  chamber.start(characters=["morrison", "poet"])
```

---

## Gabriel MCP v2 Module Structure

```
gabriel/mcp_servers/gabriel_mcp/
├── server.py              # Thin MCP entry (~declarations + routing)
├── config.py              # Env-aware path resolution
├── server_v1.py           # Legacy monolith (preserved)
├── orchestrator/
│   ├── session.py         # Session state machine (phase enforcement)
│   ├── chamber.py         # Dream chamber orchestration controller
│   └── router.py          # Tool dispatch (domain.action → handler)
├── tools/
│   ├── audio.py           # Audio pipeline (Cocoro, Fish, render, export)
│   ├── characters.py      # Character registry (CRUD + voice profiles)
│   ├── memory.py          # Memory store + task management
│   ├── codebase.py        # Code search, read, write, git
│   ├── system.py          # System info, shell commands
│   └── knowledge.py       # Deep knowledge index (29K+ files)
└── state/
    └── store.py           # Local JSON persistence (SQLite-swappable)
```

---

## Tool Naming Convention

All tools use `domain.action` format:

| Domain | Actions |
|--------|---------|
| `chamber` | start, status, activate, process, complete, close, add_character, list_characters, queue_audio, audio_status |
| `audio` | process, route_to_cocoro, route_to_fish, render, export, status, list_jobs |
| `character` | list, get, create, update, delete |
| `memory` | store, recall, add_task, complete_task, list_tasks |
| `codebase` | search, read, write, list, scan, git_status |
| `system` | info, run |
| `knowledge` | stats, search, prompts, functions, entries, imports, todos, explore |

---

## What's NOT in the Stack

- **LaRosa** — removed from stack
- **Google TTS** — solid for utility, doesn't match Anthropic reasoning depth for core characters
- **Hugging Face / Kaggle commodity models** — duplicate existing capabilities

---

## Concurrent Reasoning Threads

No hard technical limit on reasoning model instances inside the dream chamber. The constraint is economic:

- Each concurrent Claude reasoning thread = API cost + latency
- Determine max concurrent threads based on acceptable response time and budget
- Gabriel MCP handles the orchestration of multiple threads locally

---

## Milestones

| Date | Target |
|------|--------|
| **Mar 25** | Dream chamber fully operational |
| **Mid-April** | Supersonic Cascade wiring, persona stitching in the bed |
| **Pre-demo** | Stress testing full sensory experience |
| **Apr 17** | World demo |

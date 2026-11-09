# 🧠 GABRIEL MCP - SIMPLE POINTS (v2.0)

## ✅ WHAT IT DOES

1. **Deep Knowledge Brain** - 29K files, 8.5M lines indexed!
2. **Codebase Intelligence** - Search & read any file
3. **Memory System** - Remember & recall across sessions
4. **Task Management** - Track todos, priorities
5. **Voice Synthesis** - TTS with GABRIEL voice
6. **System Control** - Run commands, monitor health
7. **Knowledge Search** - Find prompts, functions, docs

---

## 📊 BRAIN STATS

| Metric | Count |
|--------|-------|
| Files Indexed | 29,349 |
| Lines of Code | 8,541,560 |
| Functions | 29,952 |
| Classes | 7,511 |
| Prompts | 98 |
| Knowledge Docs | 1,262 |
| TODOs | 1,718 |
| Imports | 3,303 |

---

## 🚀 QUICK SETUP

### Step 1: Install MCP
```bash
pip install mcp
```

### Step 2: Add to Claude Desktop
Copy to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "gabriel": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/GABRIEL/mcp_servers/gabriel_mcp/server.py"]
    }
  }
}
```

### Step 3: Restart Claude Desktop
Done! GABRIEL tools now available.

---

## 🔧 23 TOOLS

### Codebase Tools (4)
| Tool | Action |
|------|--------|
| `search_code` | Find files/content |
| `read_file` | Read any file |
| `write_file` | Create/edit files |
| `list_files` | Browse directories |

### Voice (1)
| Tool | Action |
|------|--------|
| `speak` | Text-to-speech |

### Memory (2)
| Tool | Action |
|------|--------|
| `remember` | Store info |
| `recall` | Search memories |

### Tasks (3)
| Tool | Action |
|------|--------|
| `add_task` | Create todo |
| `complete_task` | Mark done |
| `list_tasks` | View all |

### System (4)
| Tool | Action |
|------|--------|
| `run_command` | Shell exec |
| `system_info` | System stats |
| `scan_project` | Analyze project |
| `git_status` | Git info |

### 🆕 Deep Knowledge (9)
| Tool | Action |
|------|--------|
| `knowledge_stats` | Brain statistics |
| `search_knowledge` | Search everything |
| `get_prompts` | Get 98 prompts |
| `get_functions` | Find 30K functions |
| `get_knowledge_base` | Search 1200+ docs |
| `get_imports` | List 3300 imports |
| `get_todos` | View 1700 TODOs |
| `explore_category` | Browse by category |
| `reindex_knowledge` | Update brain |

---

## 📦 5 RESOURCES

| URI | Content |
|-----|---------|
| `gabriel://brain` | Full knowledge index |
| `gabriel://memory` | Conversation memory |
| `gabriel://tasks` | Task queue |
| `gabriel://status` | System health |
| `gabriel://logs` | Activity logs |

---

## 🏷️ CATEGORIES

Search files by category with `explore_category`:

- `voice` - 841 files (TTS, RVC, audio)
- `ai_ml` - 375 files (models, training)
- `prompts` - 168 files (system prompts)
- `api` - 218 files (endpoints)
- `database` - 2,502 files (SQL, schemas)
- `cloud` - 183 files (Cloudflare, Docker)
- `network` - 279 files (HTTP, WebSocket)
- `automation` - 1,515 files (scripts)
- `ui` - 710 files (React, frontend)
- `config` - 427 files (settings)
- `docs` - 466 files (documentation)

---

## 📂 KEY FILES

```
/Users/m2ultra/NOIZYLAB/GABRIEL/
├── mcp_servers/
│   └── gabriel_mcp/
│       └── server.py              # MCP Server (23 tools)
├── memcell_data/
│   ├── gabriel_brain.json         # Full knowledge index
│   ├── gabriel_brain_quick.json   # Quick stats
│   ├── prompts_index.json         # All prompts
│   └── functions_index.json       # Top functions
├── tools/
│   └── deep_knowledge_indexer.py  # Brain builder
└── KNOWLEDGE_INDEX.md             # Full docs
```

---

## 🔄 UPDATE BRAIN

```bash
# Reindex all knowledge
python3 ~/NOIZYLAB/GABRIEL/tools/deep_knowledge_indexer.py
```

Or use MCP tool: `reindex_knowledge`

---

## 💡 EXAMPLE QUERIES

Ask Claude:
- "Search for voice synthesis code"
- "Find all React components"
- "Show me prompts about agents"
- "List all TODOs in the codebase"
- "What functions are in GABRIEL?"
- "Explore the ai_ml category"

---

*🧠 GABRIEL: 29K files. 8.5M lines. Infinite knowledge.*

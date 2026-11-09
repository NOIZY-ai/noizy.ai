# GORUNFREE - Quick Reference Card

## Voice Commands (When Connected)

| Say | Does |
|-----|------|
| "Hey Gabriel" | Wake word |
| "Search for [X]" | `search_knowledge` |
| "Remember [X]" | `remember` tool |
| "What do you know about [X]" | `recall` tool |
| "Run [command]" | `run_command` (safe mode) |
| "Status" | `system_info` |
| "Tasks" | `list_tasks` |

---

## MCP Tools Available

### Gabriel (23 tools)
```
search_code, read_file, write_file, list_files
speak
remember, recall
add_task, complete_task, list_tasks
run_command, system_info, scan_project, git_status
knowledge_stats, search_knowledge, get_prompts
get_functions, get_knowledge_base, get_imports
get_todos, explore_category, reindex_knowledge
```

### Cloudflare
```
d1_query, kv_get, kv_put, workers_list
r2_list, pages_deploy
```

### Stripe
```
create_payment_link, list_customers
get_balance, create_invoice
```

### ekkOS (11 layers)
```
search_memory, forge_pattern, forge_directive
record_outcome, capture_event, get_memory_stats
recall_conversation
```

---

## Quick Queries

| Ask Claude | What Happens |
|------------|--------------|
| "Find voice synthesis code" | Searches 29K files |
| "Show me all prompts" | Returns 98 indexed prompts |
| "What functions exist?" | Searches 30K+ functions |
| "List TODOs" | Shows 1700+ TODOs |
| "Explore ai_ml category" | 375 AI/ML files |

---

## Device Status

| Device | MCP | Status |
|--------|-----|--------|
| GOD (M2 Ultra) | Full | Active |
| DaFixer | Full | Ready |
| GABRIEL (WSL) | Full | Ready |
| iPhone 15 | App | Ready |
| iPad 12.9 | App | Ready |

---

## Key Paths

```
/Users/m2ultra/NOIZYLAB/GABRIEL/
├── mcp_servers/
│   ├── gabriel_mcp/server.py      # Main MCP
│   ├── ekkos_bridge/server.js     # ekkOS bridge
│   └── unified_mcp_config.json    # All configs
├── memcell_data/
│   └── gabriel_brain.json         # 8.5M lines indexed
└── install-claude-mac.sh          # Installer
```

---

## Memory Layers (ekkOS)

| # | Layer | Purpose |
|---|-------|---------|
| 1 | Working | Current session |
| 2 | Episodic | Past conversations |
| 3 | Semantic | Embeddings |
| 4 | Patterns | Proven solutions |
| 5 | Procedural | Workflows |
| 6 | Collective | Cross-project |
| 7 | Meta | Pattern effectiveness |
| 8 | Codebase | This-repo-only |
| 9 | Directives | User preferences |
| 10 | Conflict | Auto-resolution |
| 11 | Secrets | Encrypted creds |

---

## Stats

- **Files Indexed:** 29,349
- **Lines of Code:** 8,541,560
- **Functions:** 29,952
- **Classes:** 7,511
- **Prompts:** 98
- **Knowledge Docs:** 1,262
- **Database Tables:** 248+

---

*GORUNFREE ACROSS ALL DEVICES!*

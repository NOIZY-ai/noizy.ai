---
description: NOIZY.ai/NOIZYLAB
auto_execution_mode: 1
---

## Goal
Make Windsurf ready for NOIZYLAB work: correct workspace, rules active, MCP ready, and a repeatable command checklist.

## Steps
1. Open folder: `/Users/m2ultra`
2. Confirm rules are active:
   - Ensure `/Users/m2ultra/.windsurfrules` exists (global behavior)
3. Verify MCP bridge:
   - Extensions installed:
     - `yutengjing.vscode-mcp-bridge`
4. Restart Windsurf (required after rules/workflow changes)
5. Quick sanity checks (run in terminal from the project root):
   - `git status`
   - `python3 --version`
   - `node -v`

---

## 🧠 NOIZYLAB COMMAND CENTER

### MCP Server (Unified)
// turbo
```bash
# Add to Windsurf MCP config, then restart
# Config location: ~/.codeium/windsurf/mcp_config.json
{
  "mcpServers": {
    "noizylab": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/UNIFIED_MCP/noizylab_mcp.py"]
    }
  }
}
```

### Dashboard & Services
// turbo
```bash
cd /Users/m2ultra/NOIZYLAB/UNIFIED_MCP
./noizylab.sh start      # Start dashboard + agent
./noizylab.sh status     # Check status
./noizylab.sh dashboard  # Open web UI (http://localhost:5175)
```

### Local LLM (GLM-4.7 355B)
// turbo
```bash
cd /Users/m2ultra/NOIZYLAB/LOCAL_LLM
./launcher.sh setup-glm   # Build llama.cpp + download 135GB model
./launcher.sh glm         # Interactive chat
./launcher.sh glm-server  # Start API server (port 8080)
```

### OpenManus AI Agent
// turbo
```bash
cd /Users/m2ultra/NOIZYLAB/LOCAL_LLM
./launcher.sh setup-manus  # Clone + install OpenManus
./launcher.sh manus        # Run agent
./launcher.sh manus-flow   # Multi-agent mode
```

### GABRIEL Intelligence
// turbo
```bash
cd /Users/m2ultra/NOIZYLAB/GABRIEL
./launch_gabriel.sh agent   # Start autonomous agent
./launch_gabriel.sh status  # Check status
```

---

## 📁 Key Paths

| Path | Purpose |
|------|---------|
| `/Users/m2ultra/NOIZYLAB/UNIFIED_MCP/` | Unified MCP server (25+ tools) |
| `/Users/m2ultra/NOIZYLAB/GABRIEL/` | GABRIEL intelligence engine |
| `/Users/m2ultra/NOIZYLAB/LOCAL_LLM/GLM-4.7/` | GLM-4.7 355B local LLM |
| `/Users/m2ultra/NOIZYLAB/LOCAL_LLM/OpenManus/` | OpenManus AI agent |
| `/Users/m2ultra/NOIZYLAB/AI_COMMAND_CENTER/` | AI tools database |
| `/Users/m2ultra/NOIZYLAB/POLYGLOT/` | Multi-language polyglots |

---

## 🔧 MCP Tools Available (via noizylab server)

**Codebase**: `scan`, `grep`, `find`
**Files**: `read`, `write`, `list`, `info`
**System**: `run`, `parallel`, `system`, `processes`, `network`
**Git**: `git_status`, `git_log`, `git_diff`
**Memory**: `mem_set`, `mem_get`, `mem_search`, `mem_del`, `mem_list`
**AI Gen**: `gen_video`, `gen_audio`, `gen_speech`, `gen_avatar`
**Local LLM**: `llm_start`, `llm_stop`, `llm_chat`, `llm_status`
**Volumes**: `volumes`, `scan_volume`
**Services**: `start_all`, `stop_all`, `status`, `turbo`
**API Keys**: `key_set`, `key_list`

---

## ⚡ OMEGA MCP (RECOMMENDED - 40+ TOOLS, ZERO LATENCY)

Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "omega": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/OMEGA/omega_mcp.py"]
    }
  }
}
```

### GORUNFREE TURBO
// turbo
```bash
cd /Users/m2ultra/NOIZYLAB/TURBO
./gorunfree.sh turbo    # Full parallel setup (29s)
./gorunfree.sh status   # Check everything
./gorunfree.sh glm      # Start GLM-4.7
./gorunfree.sh manus    # Start OpenManus
```

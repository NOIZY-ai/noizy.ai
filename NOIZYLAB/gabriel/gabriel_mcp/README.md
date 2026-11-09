# 🧠 GABRIEL MCP Server

Model Context Protocol server for GABRIEL AI system.

## Quick Start

```bash
# Install dependencies
pip install mcp

# Run server
python server.py
```

## Configure in Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gabriel": {
      "command": "python",
      "args": ["/Users/m2ultra/NOIZYLAB/GABRIEL/mcp_servers/gabriel_mcp/server.py"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `search_code` | Search codebase |
| `read_file` | Read file contents |
| `write_file` | Write to files |
| `list_files` | List directory |
| `speak` | Voice synthesis |
| `remember` | Store memory |
| `recall` | Search memory |
| `add_task` | Create task |
| `complete_task` | Mark done |
| `list_tasks` | View tasks |
| `run_command` | Execute shell |
| `system_info` | System stats |
| `scan_project` | Project structure |
| `git_status` | Git info |

## Resources

- `gabriel://brain` - Knowledge state
- `gabriel://memory` - Conversation history
- `gabriel://tasks` - Task queue
- `gabriel://status` - System health
- `gabriel://logs` - Activity logs

# 🧠 NOIZYLAB UNIFIED COMMAND CENTER

> **One system to rule them all**

---

## What's Included

| Component | Description | Port |
|-----------|-------------|------|
| **MCP Server** | 25+ tools for Windsurf/Claude | stdio |
| **Dashboard** | Web UI for management | 5175 |
| **Agent** | Autonomous monitoring | background |

---

## Quick Start

```bash
# Make executable
chmod +x /Users/m2ultra/NOIZYLAB/UNIFIED_MCP/noizylab.sh

# Start everything
./noizylab.sh start

# Open dashboard
./noizylab.sh dashboard
```

---

## MCP Setup (Windsurf)

Add to your Windsurf MCP config:

```json
{
  "mcpServers": {
    "noizylab": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/UNIFIED_MCP/noizylab_mcp.py"]
    }
  }
}
```

Then restart Windsurf.

---

## Available MCP Tools (25+)

### Codebase Intelligence
| Tool | Description |
|------|-------------|
| `scan_codebase` | Full scan with stats, languages, complexity |
| `search_files` | Find files by name |
| `grep_content` | Search file contents |

### File Operations
| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write/append to files |
| `list_dir` | List directory |

### System
| Tool | Description |
|------|-------------|
| `run_command` | Execute shell commands |
| `system_info` | CPU, memory, disk info |
| `process_list` | Running processes |

### Git
| Tool | Description |
|------|-------------|
| `git_status` | Repository status |
| `git_log` | Recent commits |

### Memory
| Tool | Description |
|------|-------------|
| `memory_store` | Store key-value data |
| `memory_get` | Retrieve data |
| `memory_search` | Search memory |
| `memory_delete` | Delete data |

### API Keys
| Tool | Description |
|------|-------------|
| `api_key_set` | Set API key |
| `api_key_list` | List key status |

### AI Generation
| Tool | Description |
|------|-------------|
| `generate_video` | Runway, Kling, Pika |
| `generate_audio` | Suno, Udio |
| `generate_speech` | ElevenLabs TTS |
| `generate_avatar` | HeyGen |

### Network & Volumes
| Tool | Description |
|------|-------------|
| `network_scan` | Scan local network |
| `list_volumes` | List mounted volumes |
| `scan_volume` | Scan volume for files |

---

## Commands

```bash
./noizylab.sh start      # Start dashboard + agent
./noizylab.sh stop       # Stop all
./noizylab.sh restart    # Restart all
./noizylab.sh status     # Show status
./noizylab.sh dashboard  # Open web UI
./noizylab.sh install    # Install as system service
./noizylab.sh uninstall  # Remove system service
./noizylab.sh config     # Show MCP config
./noizylab.sh logs       # Tail logs
```

---

## Production Mode

Install as system services (auto-start on login):

```bash
./noizylab.sh install
```

This creates launchd services for:
- Dashboard server
- GABRIEL agent

The MCP server is started by Windsurf automatically.

---

## File Structure

```
UNIFIED_MCP/
├── noizylab_mcp.py      # Main MCP server (25+ tools)
├── noizylab.sh          # Master control script
├── README.md            # This file
├── dashboard/
│   ├── index.html       # Web UI
│   └── server.py        # REST API backend
└── production/
    ├── com.noizylab.dashboard.plist
    ├── com.noizylab.agent.plist
    └── com.noizylab.mcp.plist
```

---

## Dashboard Features

- **System Status**: Real-time monitoring
- **AI Services**: API key management
- **Quick Actions**: One-click generation
- **Codebase Stats**: Language distribution
- **Terminal Output**: Live logs

---

## Supported AI Services

| Service | Category | API Key Env |
|---------|----------|-------------|
| Runway | Video | `RUNWAY_API_KEY` |
| Kling | Video | `KLING_API_KEY` |
| Pika | Video | `PIKA_API_KEY` |
| Suno | Audio | `SUNO_API_KEY` |
| Udio | Audio | `UDIO_API_KEY` |
| ElevenLabs | Voice | `ELEVENLABS_API_KEY` |
| HeyGen | Avatar | `HEYGEN_API_KEY` |
| OpenAI | LLM | `OPENAI_API_KEY` |
| Anthropic | LLM | `ANTHROPIC_API_KEY` |

---

*NOIZYLAB Unified Command Center • December 2024*

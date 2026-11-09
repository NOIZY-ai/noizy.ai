�@# 🟠 ANTHROPIC AI - COMPLETE GUIDE

## Claude Models

### Available Models (Dec 2025)

| Model | ID | Context | Best For |
|-------|-----|---------|----------|
| **Claude 4 Opus** | `claude-4-opus-20250514` | 200K | Most capable |
| **Claude 4 Sonnet** | `claude-sonnet-4-20250514` | 200K | Balanced |
| **Claude 3.7 Sonnet** | `claude-3-7-sonnet-20250219` | 200K | Extended thinking |
| **Claude 3.5 Sonnet** | `claude-3-5-sonnet-20241022` | 200K | Fast + smart |
| **Claude 3.5 Haiku** | `claude-3-5-haiku-20241022` | 200K | Ultra-fast |
| **Claude 3 Opus** | `claude-3-opus-20240229` | 200K | Legacy best |

---

## API Configuration

### OpenManus Config
```toml
[llm]
model = "claude-sonnet-4-20250514"
base_url = "https://api.anthropic.com/v1/"
api_key = "YOUR_ANTHROPIC_API_KEY"
max_tokens = 8192
temperature = 0.7
```

### Direct API
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## Extended Thinking (Claude 3.7+)

### Enable Thinking Mode
```json
{
  "model": "claude-3-7-sonnet-20250219",
  "max_tokens": 16000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  },
  "messages": [{"role": "user", "content": "Solve this complex problem..."}]
}
```

### Streaming Thinking
```python
with client.messages.stream(
    model="claude-3-7-sonnet-20250219",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "..."}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(f"Thinking: {event.delta.thinking}")
            elif event.delta.type == "text_delta":
                print(f"Response: {event.delta.text}")
```

---

## Computer Use (Beta)

### Enable Computer Use
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[
        {
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
            "display_number": 1
        },
        {
            "type": "text_editor_20250124",
            "name": "str_replace_editor"
        },
        {
            "type": "bash_20250124",
            "name": "bash"
        }
    ],
    messages=[{"role": "user", "content": "Open Chrome and search for..."}],
    betas=["computer-use-2025-01-24"]
)
```

### Computer Use Tools
| Tool | Description |
|------|-------------|
| `computer_20250124` | Mouse, keyboard, screenshots |
| `text_editor_20250124` | File editing |
| `bash_20250124` | Shell commands |

---

## MCP (Model Context Protocol)

### Claude Desktop MCP Config
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/m2ultra"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {"GITHUB_TOKEN": "YOUR_TOKEN"}
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-brave-search"],
      "env": {"BRAVE_API_KEY": "YOUR_KEY"}
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-slack"],
      "env": {"SLACK_BOT_TOKEN": "xoxb-..."}
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-google-drive"]
    },
    "noizylab": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/OMEGA/omega_mcp.py"]
    }
  }
}
```

### Available MCP Servers

| Server | Package | Description |
|--------|---------|-------------|
| Filesystem | `@modelcontextprotocol/server-filesystem` | File operations |
| GitHub | `@modelcontextprotocol/server-github` | Repos, issues, PRs |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Database queries |
| SQLite | `@modelcontextprotocol/server-sqlite` | SQLite access |
| Brave Search | `@anthropic/mcp-server-brave-search` | Web search |
| Memory | `@modelcontextprotocol/server-memory` | Persistent memory |
| Puppeteer | `@anthropic/mcp-server-puppeteer` | Browser automation |
| Slack | `@anthropic/mcp-server-slack` | Slack integration |
| Google Drive | `@anthropic/mcp-server-google-drive` | Drive access |
| Fetch | `@modelcontextprotocol/server-fetch` | HTTP requests |
| Git | `@modelcontextprotocol/server-git` | Git operations |
| Sequential Thinking | `@modelcontextprotocol/server-sequential-thinking` | Step-by-step reasoning |

---

## Vision (Image Analysis)

### Send Images
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image
                }
            },
            {"type": "text", "text": "What's in this image?"}
        ]
    }]
)
```

### Supported Formats
- PNG, JPEG, GIF, WebP
- Max 20MB per image
- Up to 100 images per request

---

## Tool Use (Function Calling)

### Define Tools
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

---

## Prompt Caching

### Enable Caching
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a helpful assistant with access to a large codebase...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Explain the main function"}]
)
```

### Cache Benefits
- 90% cost reduction on cached tokens
- Faster response times
- Persists for 5 minutes

---

## Batch API

### Create Batch
```python
batch = client.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello"}]
            }
        },
        # ... more requests
    ]
)
```

### Benefits
- 50% cost reduction
- Up to 100,000 requests per batch
- 24-hour processing window

---

## Pricing (Dec 2025)

| Model | Input (1M) | Output (1M) |
|-------|------------|-------------|
| Claude 4 Opus | $15.00 | $75.00 |
| Claude 4 Sonnet | $3.00 | $15.00 |
| Claude 3.7 Sonnet | $3.00 | $15.00 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3.5 Haiku | $0.80 | $4.00 |

---

## Get API Key

1. Go to: https://console.anthropic.com/
2. Create account or sign in
3. Settings → API Keys → Create Key

---

## Python SDK

```bash
pip install anthropic
```

```python
from anthropic import Anthropic

client = Anthropic(api_key="YOUR_KEY")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)
```

---

*Anthropic AI Guide • NOIZYLAB*
�@*cascade08"(a1b6a0eed5fda92b075b21780c1e15f048a239dd2@file:///Users/m2ultra/NOIZYLAB/AI_COMMAND_CENTER/ANTHROPIC_AI.md:file:///Users/m2ultra/NOIZYLAB
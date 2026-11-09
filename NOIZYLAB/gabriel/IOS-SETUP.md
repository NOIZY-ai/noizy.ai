# iOS Setup Guide - iPhone 15 & iPad 12.9

## Overview

Claude iOS app connects to your GABRIEL infrastructure via the Claude API with MCP support.

---

## Method 1: Claude iOS App (Direct)

### Step 1: Install Claude App
- Download **Claude** from App Store
- Sign in with your Anthropic account

### Step 2: Configure System Prompt

In Claude iOS settings, add this system prompt:

```
You are GABRIEL, part of the MC96ECOUNIVERSE.

When I mention these commands, use the appropriate API calls:
- "search for [X]" - Search the knowledge base
- "remember [X]" - Store in memory
- "status" - Report system status
- "tasks" - List active tasks

I have access to:
- 29,349 indexed files (8.5M lines)
- 29,952 functions
- 7,511 classes
- 98 prompts
- 1,262 knowledge docs

Always end responses with:
---
🧠 **ekkOS_™** · 📅 [DATE] [TIME]
```

### Step 3: Use Shortcuts for Voice

Create iOS Shortcuts for voice commands:

1. **"Hey Gabriel" Shortcut**
   - Trigger: "Hey Gabriel"
   - Action: Open Claude app + Start dictation

2. **"Search Knowledge" Shortcut**
   - Trigger: "Search for"
   - Action: Open Claude with pre-filled "search_knowledge: [Dictated Text]"

---

## Method 2: Tailscale + SSH (Advanced)

Connect directly to GOD machine for full MCP access.

### Step 1: Install Tailscale on iOS
- Download **Tailscale** from App Store
- Sign in with your Tailscale account
- Connect to your tailnet

### Step 2: Install Termius (SSH Client)
- Download **Termius** from App Store
- Add host: `god` (Tailscale hostname)
- Configure SSH key authentication

### Step 3: Create Quick Commands

In Termius, save these as snippets:

```bash
# Search Knowledge
cd ~/NOIZYLAB/GABRIEL && python3 -c "
from mcp_servers.gabriel_mcp.server import search_knowledge
print(search_knowledge('YOUR_QUERY'))
"

# System Status
cd ~/NOIZYLAB/GABRIEL && python3 -c "
from mcp_servers.gabriel_mcp.server import system_info
print(system_info())
"

# List Tasks
cd ~/NOIZYLAB/GABRIEL && python3 -c "
from mcp_servers.gabriel_mcp.server import list_tasks
print(list_tasks())
"
```

---

## Method 3: Web Bridge (Coming Soon)

A lightweight web interface accessible from any device.

### Architecture
```
iOS Safari → Cloudflare Worker → Gabriel MCP → Knowledge Base
```

### Endpoints (Future)
```
https://gabriel.mc96ecouniverse.com/search?q=
https://gabriel.mc96ecouniverse.com/remember
https://gabriel.mc96ecouniverse.com/status
```

---

## Voice Command Mapping

| Say This | Does This |
|----------|-----------|
| "Hey Gabriel" | Wake + Open Claude |
| "Search for [X]" | `search_knowledge` |
| "Remember this: [X]" | `remember` tool |
| "What do you know about [X]" | `recall` tool |
| "System status" | `system_info` |
| "Show my tasks" | `list_tasks` |
| "Add task: [X]" | `add_task` |

---

## Sync Strategy

### From iOS to GOD
- Use Claude iOS app for queries
- Results sync via ekkOS memory substrate
- Captured in Layer 2 (Episodic)

### From GOD to iOS
- Push notifications via Pushover/Pushcut
- Shared Apple Notes for knowledge
- iCloud Drive for file sync

---

## Recommended iOS Apps

| App | Purpose |
|-----|---------|
| **Claude** | Main AI interface |
| **Tailscale** | VPN to home network |
| **Termius** | SSH to GOD machine |
| **Shortcuts** | Voice command automation |
| **Working Copy** | Git access to GABRIEL repo |
| **Pushcut** | Automation server |

---

## Quick Test

After setup, test these in Claude iOS:

1. "Search for voice synthesis in my codebase"
2. "What functions handle audio processing?"
3. "Show me all TODOs related to MCP"

If working correctly, you'll see results from your 29K indexed files.

---

## Troubleshooting

### "Can't connect to Tailscale"
- Check Tailscale is running on GOD machine
- Verify iOS is connected to tailnet
- Try: `tailscale ping god`

### "SSH connection refused"
- Enable SSH on GOD: `sudo systemsetup -setremotelogin on`
- Check firewall allows port 22

### "Claude doesn't have context"
- Ensure system prompt is set
- MCP tools aren't available in iOS app directly
- Use Method 2 or 3 for full access

---

*GORUNFREE ACROSS ALL DEVICES!*

# GABRIEL MULTI-MACHINE SYNC ARCHITECTURE

## THE VISION: CLAUDE + GABRIEL + COPILOT + GEMINI

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         GABRIEL UNIFIED SYSTEM                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   ║
║   │  M2 ULTRA   │    │  HP-OMEN    │    │  MAC PRO    │    │  MACBOOK    │   ║
║   │  Mac Studio │    │  Windows    │    │  12-Core    │    │  Pro 13     │   ║
║   │  24 cores   │    │  RTX 4090   │    │  Xeon       │    │  M2         │   ║
║   │  192GB RAM  │    │  64GB VRAM  │    │  64GB RAM   │    │  24GB RAM   │   ║
║   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘   ║
║          │                  │                  │                  │          ║
║          └──────────────────┴──────────────────┴──────────────────┘          ║
║                              │                                                ║
║                    ┌─────────▼─────────┐                                     ║
║                    │   TAILSCALE VPN   │                                     ║
║                    │   MESH NETWORK    │                                     ║
║                    └─────────┬─────────┘                                     ║
║                              │                                                ║
║          ┌───────────────────┼───────────────────┐                           ║
║          │                   │                   │                           ║
║   ┌──────▼──────┐    ┌───────▼───────┐   ┌──────▼──────┐                    ║
║   │   CLAUDE    │    │   GABRIEL     │   │  COPILOT   │                    ║
║   │   CODE      │    │   MCP SYNC    │   │  PRO+      │                    ║
║   │   ekkOS_    │    │   MEMCELL     │   │  GitHub    │                    ║
║   └─────────────┘    └───────────────┘   └─────────────┘                    ║
║                                                                               ║
║   ┌─────────────────────────────────────────────────────────────────────┐    ║
║   │                        GEMINI 3 BACKBONE                             │    ║
║   │   Deep Reasoning · Multi-Modal · Code Generation · Analysis          │    ║
║   └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## SETUP STEPS

### 1. Tailscale VPN (All Machines)

```bash
# macOS
brew install tailscale
# OR download from: https://pkgs.tailscale.com/stable/

# Login on each machine
tailscale login

# Verify connection
tailscale status
```

### 2. Claude Code on All Machines

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
# OR
brew install claude-code

# Login
claude login

# Sync settings
claude config sync
```

### 3. GABRIEL Sync Setup

```bash
# On M2 Ultra (primary)
cd ~/NOIZYLAB/GABRIEL
git init  # if not already
git remote add origin git@github.com:YOUR_REPO/GABRIEL.git

# Create sync script
cat > sync_gabriel.sh << 'EOF'
#!/bin/bash
# Sync GABRIEL across machines
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' \
    ~/NOIZYLAB/GABRIEL/ \
    tailscale-hp-omen:~/GABRIEL/

rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' \
    ~/NOIZYLAB/GABRIEL/ \
    tailscale-macpro:~/GABRIEL/
EOF
chmod +x sync_gabriel.sh
```

### 4. MEMCELL Sync (ekkOS_)

The ekkOS_ memory system syncs automatically via:
- `mcp.ekkos.dev` API
- Local SQLite replication
- Real-time pattern sharing

```python
# MEMCELL sync config
SYNC_CONFIG = {
    "primary": "m2ultra.tailscale.net",
    "replicas": [
        "hp-omen.tailscale.net",
        "macpro.tailscale.net",
        "mbp13.tailscale.net"
    ],
    "sync_interval": 60,  # seconds
    "conflict_resolution": "latest_wins"
}
```

### 5. GitHub Copilot Pro+

```bash
# Enable on all machines
gh extension install github/gh-copilot
gh copilot configure

# Verify
gh copilot status
```

### 6. Gemini 3 Integration

```python
# gemini_config.py
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

GEMINI_CONFIG = {
    "model": "gemini-2.0-flash-exp",  # or gemini-1.5-pro
    "capabilities": [
        "deep_reasoning",
        "code_generation",
        "multi_modal",
        "long_context"
    ],
    "max_tokens": 1000000,
    "temperature": 0.7
}
```

### 7. OpenVSX Self-Hosted (Optional)

For private VS Code extensions:

```bash
# Clone
git clone https://github.com/eclipse/openvsx.git

# Deploy with Docker
cd openvsx
docker-compose up -d

# Configure in VS Code settings
{
    "extensions.marketplace": "https://your-openvsx.local/api"
}
```

## UNIFIED COMMANDS

After setup, from any machine:

```bash
# Check all systems
gabriel perfect

# Sync code across machines
gabriel sync

# Deep scan all connected storage
gabriel deepdive

# Speak with TTS
gabriel speak "Hello from GABRIEL"

# Get status
gabriel status
```

## NETWORK TOPOLOGY

| Machine | IP | Tailscale IP | Role |
|---------|-----|--------------|------|
| M2 Ultra | 10.0.0.71 | 100.x.x.1 | Primary Hub |
| HP-OMEN | 10.0.0.160 | 100.x.x.2 | GPU Compute |
| Mac Pro | 10.0.0.??? | 100.x.x.3 | Archive/Build |
| MBP 13 | varies | 100.x.x.4 | Mobile |

## DATA FLOW

1. **Code changes** → GitHub (Copilot assists)
2. **Memories/Patterns** → ekkOS_ API → All machines
3. **Files/Media** → Syncthing/rsync → Local storage
4. **AI Inference** → Claude/Gemini → Cached locally

## SECURITY

- Tailscale MagicDNS for secure addressing
- SSH keys on all machines
- GitHub SSH authentication
- API keys in secure storage (ekkOS_ Layer 11)

---

**GABRIEL X1000 - ALL MACHINES UNIFIED - INFINITE POWER**

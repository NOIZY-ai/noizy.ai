# MC96ECOUNIVERSE - Multi-Device Sync Configuration

## Device Matrix

| Device | Role | OS | MCP Access | Sync Method |
|--------|------|-----|------------|-------------|
| **GOD** (M2 Ultra) | Primary | macOS | Full Native | Source of Truth |
| **DaFixer** | Secondary Mac | macOS | Full Native | Tailscale rsync |
| **GABRIEL** | WSL Instance | Ubuntu/WSL2 | Via WSL Bridge | Tailscale rsync |
| **iPhone 15** | Mobile | iOS | Claude App | ekkOS Cloud |
| **iPad 12.9** | Tablet | iPadOS | Claude App | ekkOS Cloud |

---

## Tailscale Network

### Hostnames
```
god         → M2 Ultra Mac (Primary)
dafixer     → Secondary Mac
gabriel-wsl → WSL Ubuntu Instance
```

### Setup Tailscale on Each Device

**Mac (GOD + DaFixer):**
```bash
brew install tailscale
sudo tailscaled
tailscale up
```

**WSL:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscaled
tailscale up
```

**iOS:**
- Download Tailscale from App Store
- Sign in with same account

---

## Sync Scripts

### GOD → All Devices (Master Sync)

Create on GOD machine: `/Users/m2ultra/bin/gabriel-push-all.sh`

```bash
#!/bin/bash
# Push GABRIEL to all devices

GABRIEL_SRC="/Users/m2ultra/NOIZYLAB/GABRIEL"

echo "=== GABRIEL SYNC - Pushing to all devices ==="

# Sync to DaFixer
echo "[1/2] Syncing to DaFixer..."
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env*' \
    --exclude 'memcell_data/*.json' \
    "$GABRIEL_SRC/" dafixer:/Users/m2ultra/NOIZYLAB/GABRIEL/

# Sync to GABRIEL-WSL
echo "[2/2] Syncing to GABRIEL-WSL..."
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env*' \
    --exclude 'memcell_data/*.json' \
    "$GABRIEL_SRC/" gabriel-wsl:~/NOIZYLAB/GABRIEL/

echo "=== Sync complete! ==="
```

### Pull from GOD (for other devices)

Create on each device: `gabriel-pull.sh`

```bash
#!/bin/bash
# Pull latest GABRIEL from GOD

rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env*' \
    --exclude 'memcell_data/*.json' \
    god:/Users/m2ultra/NOIZYLAB/GABRIEL/ ~/NOIZYLAB/GABRIEL/

echo "GABRIEL synced from GOD!"
```

---

## Automatic Sync (Cron)

### On GOD - Push every hour
```bash
crontab -e
# Add:
0 * * * * /Users/m2ultra/bin/gabriel-push-all.sh >> /tmp/gabriel-sync.log 2>&1
```

### On Other Devices - Pull every hour
```bash
crontab -e
# Add:
30 * * * * ~/bin/gabriel-pull.sh >> /tmp/gabriel-sync.log 2>&1
```

---

## Memory Sync (ekkOS)

All devices share the same ekkOS memory substrate via API.

### Shared Memory Layers
- **Layer 4 (Patterns)** - Synced across all
- **Layer 5 (Procedural)** - Synced across all
- **Layer 6 (Collective)** - Synced across all
- **Layer 9 (Directives)** - Synced across all

### Device-Specific Layers
- **Layer 1 (Working)** - Per-session, not synced
- **Layer 2 (Episodic)** - Device-specific conversations
- **Layer 8 (Codebase)** - Project-specific

### Sync Endpoint
```
https://mcp.ekkos.dev/api/v1/sync
Authorization: Bearer $EKKOS_AUTH_TOKEN
```

---

## Configuration Sync

### Synced Files
```
mcp_servers/unified_mcp_config.json  → All Macs
mcp_servers/gabriel_mcp/server.py    → All devices
.claude/hooks/*                       → All Claude Code devices
```

### NOT Synced (Device-Specific)
```
.env.gabriel          → Contains device-specific paths
memcell_data/         → Local cache
node_modules/         → Reinstall per device
```

---

## Verification Commands

### Check All Devices Online
```bash
# On GOD
tailscale status
```

### Test MCP on Each Device

**Mac:**
```bash
python3 /Users/m2ultra/NOIZYLAB/GABRIEL/mcp_servers/gabriel_mcp/server.py --test
```

**WSL:**
```bash
python3 ~/NOIZYLAB/GABRIEL/mcp_servers/gabriel_mcp/server.py --test
```

### Verify ekkOS Connection
```bash
curl -X POST https://mcp.ekkos.dev/api/v1/memory/search \
  -H "Authorization: Bearer $EKKOS_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "layers": [4]}'
```

---

## Conflict Resolution

### Code Conflicts
- GOD is always source of truth
- Other devices pull, never push to GOD
- Use git for version control if needed

### Memory Conflicts
- ekkOS Layer 10 handles automatically
- Newer patterns take precedence
- Directives merge by scope

---

## Quick Reference

| Task | Command |
|------|---------|
| Push to all | `gabriel-push-all.sh` |
| Pull from GOD | `gabriel-pull.sh` |
| Check Tailscale | `tailscale status` |
| Test MCP | `python3 server.py --test` |
| View sync log | `tail -f /tmp/gabriel-sync.log` |

---

## Device-Specific Notes

### GOD (M2 Ultra)
- Primary development machine
- Runs full Gabriel MCP server
- Source of truth for all code
- Has complete 8.5M line index

### DaFixer
- Mirror of GOD
- Can run independently
- Syncs hourly

### GABRIEL (WSL)
- Windows-based access
- MCP runs via WSL bridge
- Claude Desktop on Windows

### iPhone 15 / iPad 12.9
- Claude app only
- No native MCP
- Uses ekkOS cloud memory
- SSH to GOD for full access

---

*GORUNFREE ACROSS ALL DEVICES!*

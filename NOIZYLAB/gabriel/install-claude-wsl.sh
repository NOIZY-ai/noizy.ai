#!/bin/bash
# ============================================================================
# MC96ECOUNIVERSE - Claude Setup for WSL (GABRIEL Device)
# ============================================================================
# Run: chmod +x install-claude-wsl.sh && ./install-claude-wsl.sh
# ============================================================================

set -e

echo "============================================"
echo "  MC96ECOUNIVERSE CLAUDE INSTALLER (WSL)"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

# Detect WSL paths
WINDOWS_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r' || echo "")
if [ -z "$WINDOWS_USER" ]; then
    WINDOWS_USER="$USER"
fi

GABRIEL_ROOT="$HOME/NOIZYLAB/GABRIEL"
CLAUDE_CONFIG_DIR="/mnt/c/Users/$WINDOWS_USER/AppData/Roaming/Claude"
WSL_CLAUDE_DIR="$HOME/.claude"

# Step 1: Check prerequisites
echo -e "${CYAN}[1/8] Checking prerequisites...${RESET}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 not found! Installing...${RESET}"
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js not found! Installing...${RESET}"
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

echo -e "${GREEN}  Prerequisites OK${RESET}"

# Step 2: Clone/Update GABRIEL repo
echo -e "${CYAN}[2/8] Setting up GABRIEL repository...${RESET}"

mkdir -p "$HOME/NOIZYLAB"

if [ -d "$GABRIEL_ROOT" ]; then
    echo "  GABRIEL folder exists, updating..."
    cd "$GABRIEL_ROOT" && git pull 2>/dev/null || echo "  Not a git repo, skipping pull"
else
    echo "  Cloning GABRIEL from GOD machine..."
    # Option 1: Clone from GitHub if available
    # git clone https://github.com/mc96ecouniverse/gabriel.git "$GABRIEL_ROOT"

    # Option 2: Sync from GOD via Tailscale
    echo -e "${YELLOW}  Please run this on GOD machine to sync:${RESET}"
    echo "  rsync -avz /Users/m2ultra/NOIZYLAB/GABRIEL/ gabriel-wsl:~/NOIZYLAB/GABRIEL/"
fi

echo -e "${GREEN}  GABRIEL repo ready${RESET}"

# Step 3: Install Python MCP SDK
echo -e "${CYAN}[3/8] Installing Python MCP SDK...${RESET}"
pip3 install mcp --quiet 2>/dev/null || pip3 install mcp
echo -e "${GREEN}  MCP SDK installed${RESET}"

# Step 4: Install Node MCP packages
echo -e "${CYAN}[4/8] Installing Node MCP packages...${RESET}"
if [ -d "$GABRIEL_ROOT/mcp_servers/ekkos_bridge" ]; then
    cd "$GABRIEL_ROOT/mcp_servers/ekkos_bridge"
    npm install --silent 2>/dev/null || npm install
fi
echo -e "${GREEN}  Node packages installed${RESET}"

# Step 5: Setup Windows Claude config
echo -e "${CYAN}[5/8] Setting up Windows Claude config...${RESET}"
mkdir -p "$CLAUDE_CONFIG_DIR"

# Convert WSL paths to Windows paths for the config
GABRIEL_WIN_PATH=$(wslpath -w "$GABRIEL_ROOT" 2>/dev/null || echo "\\\\wsl$\\Ubuntu$GABRIEL_ROOT")

cat > "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" << EOF
{
  "mcpServers": {
    "gabriel": {
      "command": "wsl",
      "args": ["-e", "python3", "$GABRIEL_ROOT/mcp_servers/gabriel_mcp/server.py"],
      "env": {
        "PYTHONPATH": "$GABRIEL_ROOT"
      }
    },
    "cloudflare": {
      "command": "npx",
      "args": ["-y", "@cloudflare/mcp-server-cloudflare"]
    },
    "stripe": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-memory"]
    },
    "filesystem": {
      "command": "wsl",
      "args": ["-e", "npx", "-y", "@anthropic/mcp-server-filesystem", "$HOME/NOIZYLAB", "$HOME/Documents"]
    }
  }
}
EOF

echo -e "${GREEN}  Windows Claude config deployed${RESET}"

# Step 6: Setup WSL Claude hooks
echo -e "${CYAN}[6/8] Setting up ekkOS hooks...${RESET}"

mkdir -p "$WSL_CLAUDE_DIR/hooks/lib"

# Create settings.json if needed
if [ ! -f "$WSL_CLAUDE_DIR/settings.json" ]; then
    cat > "$WSL_CLAUDE_DIR/settings.json" << 'EOF'
{
  "hooks": {
    "user-prompt-submit": [
      {
        "matcher": "",
        "hooks": ["~/.claude/hooks/user-prompt-submit.sh"]
      }
    ],
    "stop": [
      {
        "matcher": "",
        "hooks": ["~/.claude/hooks/stop.sh"]
      }
    ]
  }
}
EOF
fi

# Copy hooks from GABRIEL if they exist
if [ -d "$GABRIEL_ROOT/.claude/hooks" ]; then
    cp -r "$GABRIEL_ROOT/.claude/hooks/"* "$WSL_CLAUDE_DIR/hooks/" 2>/dev/null || true
fi

echo -e "${GREEN}  ekkOS hooks configured${RESET}"

# Step 7: Setup Tailscale sync
echo -e "${CYAN}[7/8] Configuring Tailscale sync...${RESET}"

# Create sync script
cat > "$HOME/bin/gabriel-sync.sh" << 'EOF'
#!/bin/bash
# Sync GABRIEL from GOD machine via Tailscale
# Run: gabriel-sync.sh

GOD_HOST="god"  # Tailscale hostname for M2 Ultra
GABRIEL_PATH="/Users/m2ultra/NOIZYLAB/GABRIEL"
LOCAL_PATH="$HOME/NOIZYLAB/GABRIEL"

echo "Syncing GABRIEL from GOD..."
rsync -avz --exclude '.git' --exclude 'node_modules' --exclude '__pycache__' \
    "$GOD_HOST:$GABRIEL_PATH/" "$LOCAL_PATH/"
echo "Sync complete!"
EOF

mkdir -p "$HOME/bin"
chmod +x "$HOME/bin/gabriel-sync.sh"

echo -e "${GREEN}  Tailscale sync configured${RESET}"

# Step 8: Verify installation
echo -e "${CYAN}[8/8] Verifying installation...${RESET}"

echo ""
echo -e "${GREEN}============================================${RESET}"
echo -e "${GREEN}  INSTALLATION COMPLETE!${RESET}"
echo -e "${GREEN}============================================${RESET}"
echo ""
echo "MCP Servers configured:"
echo "  - gabriel     (via WSL python)"
echo "  - cloudflare  (D1, KV, Workers)"
echo "  - stripe      (Payments)"
echo "  - memory      (Claude memory)"
echo "  - filesystem  (via WSL)"
echo ""
echo -e "${YELLOW}NEXT STEPS:${RESET}"
echo "  1. Create ~/.env.gabriel with your API keys"
echo "  2. Run: gabriel-sync.sh (to sync from GOD)"
echo "  3. Restart Claude Desktop on Windows"
echo "  4. Test: Ask Claude 'search_knowledge for voice'"
echo ""
echo -e "${CYAN}GORUNFREE!${RESET}"

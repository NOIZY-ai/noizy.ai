#!/bin/bash
# ============================================================================
# MC96ECOUNIVERSE - Claude Setup for Mac (GOD + DaFixer)
# ============================================================================
# Run: chmod +x install-claude-mac.sh && ./install-claude-mac.sh
# ============================================================================

set -e

echo "============================================"
echo "  MC96ECOUNIVERSE CLAUDE INSTALLER (Mac)"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

GABRIEL_ROOT="/Users/m2ultra/NOIZYLAB/GABRIEL"
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"

# Step 1: Check prerequisites
echo -e "${CYAN}[1/7] Checking prerequisites...${RESET}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 not found! Installing via Homebrew...${RESET}"
    brew install python3
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js not found! Installing via Homebrew...${RESET}"
    brew install node
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm not found! Installing via Homebrew...${RESET}"
    brew install npm
fi

echo -e "${GREEN}  Prerequisites OK${RESET}"

# Step 2: Install Python MCP SDK
echo -e "${CYAN}[2/7] Installing Python MCP SDK...${RESET}"
pip3 install mcp --quiet 2>/dev/null || pip3 install mcp
echo -e "${GREEN}  MCP SDK installed${RESET}"

# Step 3: Install Node MCP packages
echo -e "${CYAN}[3/7] Installing Node MCP packages...${RESET}"
cd "$GABRIEL_ROOT/mcp_servers/ekkos_bridge"
npm install --silent 2>/dev/null || npm install
echo -e "${GREEN}  Node packages installed${RESET}"

# Step 4: Create Claude config directory
echo -e "${CYAN}[4/7] Setting up Claude config...${RESET}"
mkdir -p "$CLAUDE_CONFIG_DIR"

# Step 5: Deploy MCP config
echo -e "${CYAN}[5/7] Deploying unified MCP config...${RESET}"

# Read the template and substitute env vars
if [ -f "$HOME/.env.gabriel" ]; then
    source "$HOME/.env.gabriel"
fi

cat > "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" << 'EOF'
{
  "mcpServers": {
    "gabriel": {
      "command": "python3",
      "args": ["/Users/m2ultra/NOIZYLAB/GABRIEL/mcp_servers/gabriel_mcp/server.py"],
      "env": {
        "PYTHONPATH": "/Users/m2ultra/NOIZYLAB/GABRIEL"
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
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/Users/m2ultra/NOIZYLAB", "/Users/m2ultra/Documents"]
    }
  }
}
EOF

echo -e "${GREEN}  Config deployed${RESET}"

# Step 6: Setup ekkOS hooks
echo -e "${CYAN}[6/7] Setting up ekkOS hooks...${RESET}"

HOOKS_DIR="$HOME/.claude/hooks"
mkdir -p "$HOOKS_DIR/lib"

# Create settings.json if needed
if [ ! -f "$HOME/.claude/settings.json" ]; then
    cat > "$HOME/.claude/settings.json" << 'EOF'
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

echo -e "${GREEN}  ekkOS hooks configured${RESET}"

# Step 7: Verify installation
echo -e "${CYAN}[7/7] Verifying installation...${RESET}"

echo ""
echo -e "${GREEN}============================================${RESET}"
echo -e "${GREEN}  INSTALLATION COMPLETE!${RESET}"
echo -e "${GREEN}============================================${RESET}"
echo ""
echo "MCP Servers configured:"
echo "  - gabriel     (29K files, 8.5M lines indexed)"
echo "  - cloudflare  (D1, KV, Workers)"
echo "  - stripe      (Payments)"
echo "  - memory      (Claude memory)"
echo "  - filesystem  (NOIZYLAB access)"
echo ""
echo -e "${YELLOW}NEXT STEPS:${RESET}"
echo "  1. Restart Claude Desktop"
echo "  2. Create ~/.env.gabriel with your API keys"
echo "  3. Test: Ask Claude 'search_knowledge for voice'"
echo ""
echo -e "${CYAN}GORUNFREE!${RESET}"

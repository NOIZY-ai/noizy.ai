#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# GABRIEL MCP v2 — Startup Script
# ═══════════════════════════════════════════════════════════════════
# For M2 Ultra and local development.
#
# Usage:
#   ./start.sh           # Start MCP server (stdio mode)
#   ./start.sh demo      # Run demo session
#   ./start.sh status    # Show configuration
#   ./start.sh test      # Run test suite
#   ./start.sh install   # Install dependencies
# ═══════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GABRIEL_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
NOIZYLAB_ROOT="$(dirname "$GABRIEL_ROOT")"

# Export environment for config resolution
export NOIZYLAB_ROOT="$NOIZYLAB_ROOT"
export GABRIEL_ROOT="$GABRIEL_ROOT"
export GABRIEL_DATA_DIR="${GABRIEL_DATA_DIR:-$GABRIEL_ROOT/memcell_data}"
export GABRIEL_STATE_DIR="${GABRIEL_STATE_DIR:-$SCRIPT_DIR/state/sessions}"
export GABRIEL_CHARACTERS_DIR="${GABRIEL_CHARACTERS_DIR:-$GABRIEL_ROOT/characters}"
export GABRIEL_AUDIO_DIR="${GABRIEL_AUDIO_DIR:-$GABRIEL_ROOT/audio_output}"

# Detect Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "ERROR: Python not found"
    exit 1
fi

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              GABRIEL MCP v2 — Dream Chamber               ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

install_deps() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    $PYTHON -m pip install --upgrade pip
    $PYTHON -m pip install mcp pytest pytest-asyncio

    # Optional: Cocoro / Fish Speech if available
    # pip install cosyvoice fish-speech

    echo -e "${GREEN}Dependencies installed.${NC}"
}

run_tests() {
    echo -e "${YELLOW}Running test suite...${NC}"
    cd "$SCRIPT_DIR"
    $PYTHON -m pytest tests/ -v
}

show_status() {
    echo -e "${YELLOW}Gabriel MCP Configuration:${NC}"
    echo ""
    echo "  NOIZYLAB_ROOT:      $NOIZYLAB_ROOT"
    echo "  GABRIEL_ROOT:       $GABRIEL_ROOT"
    echo "  GABRIEL_DATA_DIR:   $GABRIEL_DATA_DIR"
    echo "  GABRIEL_STATE_DIR:  $GABRIEL_STATE_DIR"
    echo "  CHARACTERS_DIR:     $GABRIEL_CHARACTERS_DIR"
    echo "  AUDIO_OUTPUT_DIR:   $GABRIEL_AUDIO_DIR"
    echo ""
    echo -e "${YELLOW}Characters available:${NC}"
    ls -1 "$GABRIEL_CHARACTERS_DIR"/*.json 2>/dev/null | xargs -I{} basename {} .json || echo "  (none)"
    echo ""
    echo -e "${YELLOW}Python:${NC} $($PYTHON --version)"
    echo ""
}

run_demo() {
    echo -e "${YELLOW}Running demo session...${NC}"
    cd "$SCRIPT_DIR"
    $PYTHON -m gabriel_mcp demo
}

start_server() {
    show_header
    echo -e "${GREEN}Starting Gabriel MCP Server...${NC}"
    echo "  Mode: stdio (MCP protocol)"
    echo ""
    cd "$SCRIPT_DIR"
    $PYTHON -m gabriel_mcp
}

# Main dispatch
case "${1:-server}" in
    install)
        show_header
        install_deps
        ;;
    test)
        show_header
        run_tests
        ;;
    status)
        show_header
        show_status
        ;;
    demo)
        show_header
        run_demo
        ;;
    server|"")
        start_server
        ;;
    *)
        echo "Usage: $0 [install|test|status|demo|server]"
        exit 1
        ;;
esac

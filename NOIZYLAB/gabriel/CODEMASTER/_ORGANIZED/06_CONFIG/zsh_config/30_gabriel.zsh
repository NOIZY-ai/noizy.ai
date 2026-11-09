# ============================================================================
# GABRIEL AI System Configuration
# MC96DIGIUNIVERSE AI LIFELUV INFINITE ENERGY
# ============================================================================
# Loaded automatically by ~/.zshrc modular configuration system

# GABRIEL directories - CONSOLIDATED LOCATION
export GABRIEL_ROOT="$HOME/NOIZYLAB/GABRIEL"
export CODEMASTER="$GABRIEL_ROOT/CODEMASTER"
export AI_BRAIN="$HOME/AI_COMPLETE_BRAIN"
export NOIZYLAB="$HOME/NOIZYLAB"

# Add Gabriel CLI to PATH
export PATH="$GABRIEL_ROOT/bin:$PATH"

# Gabriel CLI aliases
alias gab='gabriel'
alias gabs='gabriel status'
alias gabd='gabriel doctor'
alias gabdc='gabriel dreamchamber'
alias gabscan='gabriel scan'
alias gabserv='gabriel server'

# Quick speak function
speak() {
    if [ -n "$1" ]; then
        say -v Oliver "$*"
    else
        echo "Usage: speak <text>"
    fi
}

# God Brain activation
godbrain() {
    python3 "$GABRIEL_ROOT/brain/god_brain.py"
}

# DreamChamber launcher
dreamchamber() {
    python3 "$GABRIEL_ROOT/core/dreamchamber.py"
}

# Visual Scanner
visualscan() {
    python3 "$GABRIEL_ROOT/core/visual_scanner.py"
}

# MC96 Server
mc96server() {
    python3 "$GABRIEL_ROOT/core/mc96_server_x1000.py"
}

# GORUNFREEX1000 launcher
gorunfree() {
    python3 "$GABRIEL_ROOT/GORUNFREEX1000.py"
}

# Master activation
gabrielactivate() {
    "$GABRIEL_ROOT/MASTER_ACTIVATE.sh" "$@"
}

# AI Brain TypeScript commands
aibuild() {
    cd "$AI_BRAIN" && npm run build
}

aidev() {
    cd "$AI_BRAIN" && npm run dev
}

aitest() {
    cd "$AI_BRAIN" && npm test
}

# Quick status check
gabrielstatus() {
    echo "═══════════════════════════════════════════════════"
    echo "  GABRIEL SYSTEM STATUS"
    echo "═══════════════════════════════════════════════════"
    echo ""
    [ -d "$GABRIEL_ROOT" ] && echo "  ✅ GABRIEL_ROOT: $GABRIEL_ROOT" || echo "  ❌ GABRIEL_ROOT missing"
    [ -d "$AI_BRAIN" ] && echo "  ✅ AI_BRAIN: $AI_BRAIN" || echo "  ❌ AI_BRAIN missing"
    [ -f "$GABRIEL_ROOT/bin/gabriel" ] && echo "  ✅ Gabriel CLI: Available" || echo "  ❌ Gabriel CLI: Missing"
    [ -f "$GABRIEL_ROOT/brain/god_brain.py" ] && echo "  ✅ God Brain: Ready" || echo "  ❌ God Brain: Missing"
    [ -f "$GABRIEL_ROOT/core/dreamchamber.py" ] && echo "  ✅ DreamChamber: Ready" || echo "  ❌ DreamChamber: Missing"
    echo ""
    echo "  Energy Level: ∞ INFINITE"
    echo "  God Mode: ENABLED"
    echo "═══════════════════════════════════════════════════"
}

# Navigate to Gabriel directory
cdgab() {
    cd "$GABRIEL_ROOT"
}

# Navigate to CODEMASTER
cdcm() {
    cd "$CODEMASTER"
}

# Navigate to NOIZYLAB
cdnl() {
    cd "$NOIZYLAB"
}

echo "GABRIEL AI System loaded (NOIZYLAB/GABRIEL). Type 'gabrielstatus' for status."

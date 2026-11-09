#!/bin/bash
# INSTALLATION VERIFICATION - MC96
# Verify all systems are properly installed

echo "╔════════════════════════════════════════════════════╗"
echo "║  INSTALLATION VERIFICATION - MC96                 ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

PASSED=0
FAILED=0

# Check directories
echo "📁 Checking directories..."
DIRS=(
    "$HOME/CODE_MASTER"
    "$HOME/CODE_MASTER/scripts"
    "$HOME/CODE_MASTER/logs"
    "$HOME/CODE_MASTER/backups"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
        PASSED=$((PASSED + 1))
    else
        echo "  ✗ $dir - MISSING"
        FAILED=$((FAILED + 1))
    fi
done

# Check scripts
echo ""
echo "📜 Checking scripts..."
SCRIPTS=(
    "HEALTH_CHECK.sh"
    "AUTO_OPTIMIZE.sh"
    "FIX_GHOST_DRIVE.sh"
    "ENHANCED_GHOST_SCAN.sh"
    "DAILY_MAINTENANCE.sh"
    "AUTO_BACKUP.sh"
    "PERF_MONITOR.sh"
)

for script in "${SCRIPTS[@]}"; do
    SCRIPT_PATH="$HOME/CODE_MASTER/scripts/$script"
    if [ -f "$SCRIPT_PATH" ] && [ -x "$SCRIPT_PATH" ]; then
        echo "  ✓ $script"
        PASSED=$((PASSED + 1))
    else
        echo "  ✗ $script - MISSING or NOT EXECUTABLE"
        FAILED=$((FAILED + 1))
    fi
done

# Check control panel
echo ""
echo "🎛️  Checking control panel..."
if [ -f "$HOME/CODE_MASTER/CONTROL_PANEL.sh" ] && [ -x "$HOME/CODE_MASTER/CONTROL_PANEL.sh" ]; then
    echo "  ✓ CONTROL_PANEL.sh"
    PASSED=$((PASSED + 1))
else
    echo "  ✗ CONTROL_PANEL.sh - MISSING or NOT EXECUTABLE"
    FAILED=$((FAILED + 1))
fi

# Check GHOST drive
echo ""
echo "👻 Checking GHOST drive..."
if [ -L "$HOME/Desktop/GHOST_DRIVE" ]; then
    echo "  ✓ GHOST_DRIVE alias exists"
    PASSED=$((PASSED + 1))
else
    echo "  ✗ GHOST_DRIVE alias missing"
    FAILED=$((FAILED + 1))
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  VERIFICATION SUMMARY                             ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "✅ ALL SYSTEMS VERIFIED!"
    exit 0
else
    echo "⚠️  Some systems need attention"
    exit 1
fi

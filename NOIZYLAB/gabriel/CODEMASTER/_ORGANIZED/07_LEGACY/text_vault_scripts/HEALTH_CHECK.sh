#!/bin/bash
# SYSTEM HEALTH CHECK - MC96
# Comprehensive system health monitoring

echo "╔════════════════════════════════════════════════════╗"
echo "║  SYSTEM HEALTH CHECK - MC96                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check disk space
echo "📊 Disk Space:"
df -h | grep -E "/$|/Volumes" | awk '{print "  " $1 " - " $4 " free (" $5 " used)"}'

# Check memory
echo ""
echo "💾 Memory:"
vm_stat | grep -E "Pages free|Pages active|Pages inactive" | awk '{print "  " $0}'

# Check CPU
echo ""
echo "⚡ CPU:"
sysctl -n machdep.cpu.brand_string

# Check mounted drives
echo ""
echo "💿 Mounted Drives:"
ls -1 /Volumes/ 2>/dev/null | while read vol; do
    if [ -d "/Volumes/$vol" ]; then
        SIZE=$(du -sh "/Volumes/$vol" 2>/dev/null | awk '{print $1}')
        echo "  • $vol - $SIZE"
    fi
done

# Check CODE_MASTER
echo ""
echo "📁 CODE_MASTER Status:"
if [ -d "$HOME/CODE_MASTER" ]; then
    SCRIPT_COUNT=$(find "$HOME/CODE_MASTER/scripts" -type f 2>/dev/null | wc -l | tr -d ' ')
    PYTHON_COUNT=$(find "$HOME/CODE_MASTER/python" -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✓ Scripts: $SCRIPT_COUNT"
    echo "  ✓ Python files: $PYTHON_COUNT"
else
    echo "  ✗ CODE_MASTER not found"
fi

# Check GHOST drive
echo ""
echo "👻 GHOST Drive:"
if [ -L "$HOME/Desktop/GHOST_DRIVE" ]; then
    TARGET=$(readlink "$HOME/Desktop/GHOST_DRIVE")
    echo "  ✓ Alias exists → $TARGET"
    if [ -d "$TARGET" ]; then
        SIZE=$(du -sh "$TARGET" 2>/dev/null | awk '{print $1}')
        echo "  ✓ Mounted - $SIZE"
    else
        echo "  ✗ Not mounted"
    fi
else
    echo "  ✗ Alias not found"
fi

echo ""
echo "✅ Health check complete!"


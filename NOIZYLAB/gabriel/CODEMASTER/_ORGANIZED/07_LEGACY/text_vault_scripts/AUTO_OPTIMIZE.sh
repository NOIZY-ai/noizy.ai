#!/bin/bash
# AUTO-OPTIMIZATION - MC96
# Automatically optimize system performance

echo "╔════════════════════════════════════════════════════╗"
echo "║  AUTO-OPTIMIZATION - MC96                         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Clear caches
echo "🧹 Clearing caches..."
rm -rf ~/Library/Caches/* 2>/dev/null
echo "  ✓ Caches cleared"

# Clean temp files
echo ""
echo "🗑️  Cleaning temp files..."
find /tmp -type f -mtime +7 -delete 2>/dev/null
echo "  ✓ Temp files cleaned"

# Optimize CODE_MASTER
echo ""
echo "📁 Optimizing CODE_MASTER..."
if [ -d "$HOME/CODE_MASTER" ]; then
    # Remove empty directories
    find "$HOME/CODE_MASTER" -type d -empty -delete 2>/dev/null
    echo "  ✓ Empty directories removed"
    
    # Compress old logs
    if [ -d "$HOME/CODE_MASTER/logs" ]; then
        find "$HOME/CODE_MASTER/logs" -name "*.log" -mtime +30 -exec gzip {} \; 2>/dev/null
        echo "  ✓ Old logs compressed"
    fi
fi

# Update permissions
echo ""
echo "🔐 Updating permissions..."
find "$HOME/CODE_MASTER/scripts" -type f -exec chmod +x {} \; 2>/dev/null
echo "  ✓ Script permissions updated"

echo ""
echo "✅ Optimization complete!"


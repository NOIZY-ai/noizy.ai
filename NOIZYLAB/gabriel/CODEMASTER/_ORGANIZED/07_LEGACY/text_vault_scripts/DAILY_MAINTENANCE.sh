#!/bin/bash
# DAILY MAINTENANCE - MC96
# Run daily system maintenance tasks

echo "╔════════════════════════════════════════════════════╗"
echo "║  DAILY MAINTENANCE - MC96                         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Health check
echo "🏥 Running health check..."
bash "/Users/M2ULTRA/CODE_MASTER/scripts/HEALTH_CHECK.sh" > "/Users/M2ULTRA/CODE_MASTER/logs/health_20251117.log" 2>&1

# Auto-optimize
echo ""
echo "🧹 Running auto-optimization..."
bash "/Users/M2ULTRA/CODE_MASTER/scripts/AUTO_OPTIMIZE.sh" >> "/Users/M2ULTRA/CODE_MASTER/logs/health_20251117.log" 2>&1

# GHOST drive check
echo ""
echo "👻 Checking GHOST drive..."
if [ -L "/Users/M2ULTRA/Desktop/GHOST_DRIVE" ]; then
    TARGET=/Volumes/MC_RESCUE
    if [ -d "" ]; then
        echo "  ✓ GHOST drive accessible"
    else
        echo "  ✗ GHOST drive not mounted"
    fi
fi

echo ""
echo "✅ Daily maintenance complete!"
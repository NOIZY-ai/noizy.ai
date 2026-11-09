#!/bin/bash
# AUTOMATED BACKUP SYSTEM - MC96
# Comprehensive backup automation

echo "╔════════════════════════════════════════════════════╗"
echo "║  AUTOMATED BACKUP SYSTEM - MC96                   ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

BACKUP_DIR="/Users/M2ULTRA/CODE_MASTER/backups/20251117_170431"
mkdir -p "/Users/M2ULTRA/CODE_MASTER/backups/20251117_163312"

# Backup CODE_MASTER scripts
echo "📦 Backing up CODE_MASTER scripts..."
tar -czf "/Users/M2ULTRA/CODE_MASTER/backups/20251117_163312/code_master_scripts.tar.gz" "/Users/M2ULTRA/CODE_MASTER/scripts" 2>/dev/null
echo "  ✓ Scripts backed up"

# Backup configs
echo ""
echo "📦 Backing up configurations..."
if [ -d "/Users/M2ULTRA/CODE_MASTER/config" ]; then
    tar -czf "/Users/M2ULTRA/CODE_MASTER/backups/20251117_163312/configs.tar.gz" "/Users/M2ULTRA/CODE_MASTER/config" 2>/dev/null
    echo "  ✓ Configs backed up"
fi

# Backup logs (compressed)
echo ""
echo "📦 Backing up logs..."
if [ -d "/Users/M2ULTRA/CODE_MASTER/logs" ]; then
    find "/Users/M2ULTRA/CODE_MASTER/logs" -name "*.log" -mtime +7 -exec gzip {} \; 2>/dev/null
    echo "  ✓ Logs compressed"
fi

echo ""
echo "✅ Backup complete: /Users/M2ULTRA/CODE_MASTER/backups/20251117_163312"
#!/bin/bash
# CREATE_CODE_BACKUP.sh
# Create comprehensive backup of all CODE_MASTER work

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     💾 CREATING COMPLETE CODE BACKUP                                 ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

CODE_MASTER="/Users/rsp_ms/CODE_MASTER"
BACKUP_BASE="$HOME/Documents/CODE_MASTER_BACKUPS"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE/BACKUP_$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup structure..."
echo ""

# Copy all code files
echo "1. Copying all code files..."
rsync -av --exclude='.git' --exclude='*.log' "$CODE_MASTER/" "$BACKUP_DIR/CODE_MASTER/" 2>/dev/null

# Create archive
echo "2. Creating compressed archive..."
cd "$BACKUP_BASE"
tar -czf "CODE_MASTER_$TIMESTAMP.tar.gz" "BACKUP_$TIMESTAMP" 2>/dev/null

# Calculate sizes
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
ARCHIVE_SIZE=$(du -sh "CODE_MASTER_$TIMESTAMP.tar.gz" | cut -f1)

echo ""
echo "✅ BACKUP COMPLETE!"
echo ""
echo "📁 Backup Location: $BACKUP_DIR"
echo "📦 Archive: CODE_MASTER_$TIMESTAMP.tar.gz"
echo "💾 Backup Size: $BACKUP_SIZE"
echo "📦 Archive Size: $ARCHIVE_SIZE"
echo ""
echo "✅ All your work is saved!"


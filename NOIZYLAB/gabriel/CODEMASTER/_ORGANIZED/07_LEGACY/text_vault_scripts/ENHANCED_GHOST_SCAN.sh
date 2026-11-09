#!/bin/bash
# ENHANCED GHOST DRIVE SCANNER - Advanced Analysis
# Rob Sonic Protocol | GORUNFREE

echo "╔════════════════════════════════════════════════════╗"
echo "║  ENHANCED GHOST DRIVE SCANNER                      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

REPORT_FILE="$HOME/CODE_MASTER/logs/ghost_scan_$(date +%Y%m%d_%H%M%S).txt"
GHOST_PATH=""

# Find GHOST drive
if [ -L "$HOME/Desktop/GHOST_DRIVE" ]; then
    GHOST_PATH=$(readlink "$HOME/Desktop/GHOST_DRIVE")
elif [ -d "/Volumes/MC_RESCUE" ]; then
    GHOST_PATH="/Volumes/MC_RESCUE"
elif [ -d "/Volumes/TM_BackUp" ]; then
    GHOST_PATH="/Volumes/TM_BackUp"
fi

if [ -z "$GHOST_PATH" ] || [ ! -d "$GHOST_PATH" ]; then
    echo "❌ GHOST drive not found or not mounted"
    exit 1
fi

echo "📁 Scanning: $GHOST_PATH"
echo "📄 Report: $REPORT_FILE"
echo ""

# Comprehensive Analysis
echo "=== ENHANCED GHOST DRIVE ANALYSIS ===" > "$REPORT_FILE"
echo "Date: $(date)" >> "$REPORT_FILE"
echo "Path: $GHOST_PATH" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# File Statistics
echo "📊 Analyzing file statistics..."
TOTAL_FILES=$(find "$GHOST_PATH" -type f 2>/dev/null | wc -l | tr -d ' ')
TOTAL_DIRS=$(find "$GHOST_PATH" -type d 2>/dev/null | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh "$GHOST_PATH" 2>/dev/null | awk '{print $1}')

echo "  Total files: $TOTAL_FILES"
echo "  Total directories: $TOTAL_DIRS"
echo "  Total size: $TOTAL_SIZE"

echo "File Statistics:" >> "$REPORT_FILE"
echo "  Total files: $TOTAL_FILES" >> "$REPORT_FILE"
echo "  Total directories: $TOTAL_DIRS" >> "$REPORT_FILE"
echo "  Total size: $TOTAL_SIZE" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# File Types
echo ""
echo "📋 Analyzing file types..."
echo "File Types:" >> "$REPORT_FILE"
find "$GHOST_PATH" -type f 2>/dev/null | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20 | while read count ext; do
    echo "  $ext: $count files"
    echo "  $ext: $count files" >> "$REPORT_FILE"
done

# Largest Files
echo ""
echo "📦 Finding largest files..."
echo "Largest Files:" >> "$REPORT_FILE"
find "$GHOST_PATH" -type f -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' | sort -hr | head -10 | while read size file; do
    echo "  $size - $file"
    echo "  $size - $file" >> "$REPORT_FILE"
done

# Directory Structure
echo ""
echo "📁 Analyzing directory structure..."
echo "Top-Level Directories:" >> "$REPORT_FILE"
find "$GHOST_PATH" -maxdepth 1 -type d 2>/dev/null | while read dir; do
    if [ "$dir" != "$GHOST_PATH" ]; then
        DIR_SIZE=$(du -sh "$dir" 2>/dev/null | awk '{print $1}')
        DIR_FILES=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
        DIR_NAME=$(basename "$dir")
        echo "  $DIR_NAME - $DIR_SIZE ($DIR_FILES files)"
        echo "  $DIR_NAME - $DIR_SIZE ($DIR_FILES files)" >> "$REPORT_FILE"
    fi
done

# Backup Detection
echo ""
echo "💾 Detecting backups..."
BACKUP_ITEMS=$(find "$GHOST_PATH" -type f \( -name "*backup*" -o -name "*BACKUP*" -o -name "*.bak" -o -name "*.backup" \) 2>/dev/null | wc -l | tr -d ' ')
TM_ITEMS=$(find "$GHOST_PATH" -type d -name "*TimeMachine*" -o -name "*Time Machine*" 2>/dev/null | wc -l | tr -d ' ')

echo "  Backup files: $BACKUP_ITEMS"
echo "  Time Machine folders: $TM_ITEMS"

echo "Backup Detection:" >> "$REPORT_FILE"
echo "  Backup files: $BACKUP_ITEMS" >> "$REPORT_FILE"
echo "  Time Machine folders: $TM_ITEMS" >> "$REPORT_FILE"

# Health Check
echo ""
echo "🏥 Health Check..."
if [ -d "$GHOST_PATH" ]; then
    PERMISSIONS=$(ls -ld "$GHOST_PATH" | awk '{print $1}')
    OWNER=$(ls -ld "$GHOST_PATH" | awk '{print $3}')
    echo "  Permissions: $PERMISSIONS"
    echo "  Owner: $OWNER"
    echo "  ✓ Drive is accessible"
    
    echo "Health Status:" >> "$REPORT_FILE"
    echo "  Permissions: $PERMISSIONS" >> "$REPORT_FILE"
    echo "  Owner: $OWNER" >> "$REPORT_FILE"
    echo "  Status: Accessible" >> "$REPORT_FILE"
else
    echo "  ✗ Drive not accessible"
fi

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  SCAN COMPLETE                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📄 Full report: $REPORT_FILE"
echo "✅ Enhanced scan complete!"


#!/bin/bash
# FIX GHOST DRIVE - Find and Mount 2.8TB GHOST Drive
# Rob Sonic Protocol | GORUNFREE

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║  FIXING GHOST DRIVE ISSUES                         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

REPORT_FILE="$HOME/CODE_MASTER/GHOST_DRIVE_FIX_REPORT.txt"
echo "=== GHOST DRIVE FIX REPORT ===" > "$REPORT_FILE"
echo "Date: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# PHASE 1: FIND ALL 2-3TB DRIVES
echo "🔍 PHASE 1: Finding 2.8TB drives..."
echo ""

# List all disks
diskutil list > /tmp/disk_list.txt

# Check for drives around 2.8TB
echo "Checking for 2.8TB drives..." >> "$REPORT_FILE"
diskutil list | grep -E "2\.8|2800|GHOST" >> "$REPORT_FILE" || echo "No 2.8TB drives found by name" >> "$REPORT_FILE"

# PHASE 2: CHECK MOUNTED VOLUMES
echo ""
echo "🔍 PHASE 2: Checking mounted volumes..."
echo ""

echo "=== MOUNTED VOLUMES ===" >> "$REPORT_FILE"
ls -la /Volumes/ >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check for GHOST in volume names
GHOST_VOLUMES=$(ls /Volumes/ 2>/dev/null | grep -i ghost || true)
if [ -n "$GHOST_VOLUMES" ]; then
    echo "✓ Found GHOST volume(s):" 
    echo "$GHOST_VOLUMES" | while read vol; do
        echo "  • /Volumes/$vol"
        echo "GHOST Volume: /Volumes/$vol" >> "$REPORT_FILE"
        
        # Scan contents
        if [ -d "/Volumes/$vol" ]; then
            ITEM_COUNT=$(find "/Volumes/$vol" -type f 2>/dev/null | wc -l | tr -d ' ')
            SIZE_GB=$(du -sh "/Volumes/$vol" 2>/dev/null | awk '{print $1}')
            echo "    Items: $ITEM_COUNT | Size: $SIZE_GB"
            echo "  Items: $ITEM_COUNT | Size: $SIZE_GB" >> "$REPORT_FILE"
        fi
    done
else
    echo "⚠️  No GHOST volumes found in /Volumes/"
    echo "No GHOST volumes found" >> "$REPORT_FILE"
fi

# PHASE 3: CHECK DISK13 PARTITIONS (2x 2TB)
echo ""
echo "🔍 PHASE 3: Checking disk13 partitions..."
echo ""

echo "=== DISK13 PARTITIONS ===" >> "$REPORT_FILE"

# Check disk14 (MC_RESCUE)
if diskutil info disk14 > /dev/null 2>&1; then
    echo "disk14 (MC_RESCUE):"
    echo "disk14 (MC_RESCUE):" >> "$REPORT_FILE"
    
    VOL_NAME=$(diskutil info disk14 | grep "Volume Name" | awk -F': ' '{print $2}' | xargs)
    MOUNT_POINT=$(diskutil info disk14 | grep "Mount Point" | awk -F': ' '{print $2}' | xargs)
    FS_TYPE=$(diskutil info disk14 | grep "File System" | awk -F': ' '{print $2}' | xargs)
    
    echo "  Volume: $VOL_NAME"
    echo "  Mount: $MOUNT_POINT"
    echo "  FS: $FS_TYPE"
    
    echo "  Volume: $VOL_NAME" >> "$REPORT_FILE"
    echo "  Mount: $MOUNT_POINT" >> "$REPORT_FILE"
    echo "  FS: $FS_TYPE" >> "$REPORT_FILE"
    
    if [ -n "$MOUNT_POINT" ] && [ "$MOUNT_POINT" != "Not applicable" ]; then
        if [ -d "$MOUNT_POINT" ]; then
            ITEM_COUNT=$(find "$MOUNT_POINT" -type f 2>/dev/null | wc -l | tr -d ' ')
            SIZE_GB=$(du -sh "$MOUNT_POINT" 2>/dev/null | awk '{print $1}')
            echo "  Items: $ITEM_COUNT | Size: $SIZE_GB"
            echo "  Items: $ITEM_COUNT | Size: $SIZE_GB" >> "$REPORT_FILE"
        fi
    fi
fi

# Check disk15 (TM_BackUp)
if diskutil info disk15 > /dev/null 2>&1; then
    echo ""
    echo "disk15 (TM_BackUp):"
    echo "" >> "$REPORT_FILE"
    echo "disk15 (TM_BackUp):" >> "$REPORT_FILE"
    
    VOL_NAME=$(diskutil info disk15 | grep "Volume Name" | awk -F': ' '{print $2}' | xargs)
    MOUNT_POINT=$(diskutil info disk15 | grep "Mount Point" | awk -F': ' '{print $2}' | xargs)
    FS_TYPE=$(diskutil info disk15 | grep "File System" | awk -F': ' '{print $2}' | xargs)
    
    echo "  Volume: $VOL_NAME"
    echo "  Mount: $MOUNT_POINT"
    echo "  FS: $FS_TYPE"
    
    echo "  Volume: $VOL_NAME" >> "$REPORT_FILE"
    echo "  Mount: $MOUNT_POINT" >> "$REPORT_FILE"
    echo "  FS: $FS_TYPE" >> "$REPORT_FILE"
    
    if [ -n "$MOUNT_POINT" ] && [ "$MOUNT_POINT" != "Not applicable" ]; then
        if [ -d "$MOUNT_POINT" ]; then
            ITEM_COUNT=$(find "$MOUNT_POINT" -type f 2>/dev/null | wc -l | tr -d ' ')
            SIZE_GB=$(du -sh "$MOUNT_POINT" 2>/dev/null | awk '{print $1}')
            echo "  Items: $ITEM_COUNT | Size: $SIZE_GB"
            echo "  Items: $ITEM_COUNT | Size: $SIZE_GB" >> "$REPORT_FILE"
        fi
    fi
fi

# PHASE 4: CHECK OTHER 2TB+ DRIVES
echo ""
echo "🔍 PHASE 4: Checking other 2TB+ drives..."
echo ""

echo "=== OTHER 2TB+ DRIVES ===" >> "$REPORT_FILE"

# Check disk6 (2.1TB)
if diskutil info disk6 > /dev/null 2>&1; then
    VOL_NAME=$(diskutil info disk6s2 2>/dev/null | grep "Volume Name" | awk -F': ' '{print $2}' | xargs || echo "Untitled")
    MOUNT_POINT=$(diskutil info disk6s2 2>/dev/null | grep "Mount Point" | awk -F': ' '{print $2}' | xargs || echo "Not mounted")
    
    if [ "$MOUNT_POINT" != "Not applicable" ] && [ -n "$MOUNT_POINT" ]; then
        echo "disk6: $VOL_NAME - $MOUNT_POINT"
        echo "disk6: $VOL_NAME - $MOUNT_POINT" >> "$REPORT_FILE"
    fi
fi

# Check disk8 (2.1TB)
if diskutil info disk8 > /dev/null 2>&1; then
    VOL_NAME=$(diskutil info disk8s2 2>/dev/null | grep "Volume Name" | awk -F': ' '{print $2}' | xargs || echo "NATO")
    MOUNT_POINT=$(diskutil info disk8s2 2>/dev/null | grep "Mount Point" | awk -F': ' '{print $2}' | xargs || echo "Not mounted")
    
    if [ "$MOUNT_POINT" != "Not applicable" ] && [ -n "$MOUNT_POINT" ]; then
        echo "disk8: $VOL_NAME - $MOUNT_POINT"
        echo "disk8: $VOL_NAME - $MOUNT_POINT" >> "$REPORT_FILE"
    fi
fi

# PHASE 5: DETAILED FILE ANALYSIS
echo ""
echo "🔍 PHASE 5: Detailed file analysis..."
echo ""

if [ -n "$GHOST_PATH" ] && [ -d "$GHOST_PATH" ]; then
    echo "Analyzing GHOST drive contents..." >> "$REPORT_FILE"
    
    # Count files by type
    echo "File types:" >> "$REPORT_FILE"
    find "$GHOST_PATH" -type f 2>/dev/null | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20 >> "$REPORT_FILE"
    
    # Find largest files
    echo "" >> "$REPORT_FILE"
    echo "Largest files:" >> "$REPORT_FILE"
    find "$GHOST_PATH" -type f -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' | sort -hr | head -10 >> "$REPORT_FILE"
    
    # Directory structure
    echo "" >> "$REPORT_FILE"
    echo "Directory structure:" >> "$REPORT_FILE"
    find "$GHOST_PATH" -type d -maxdepth 2 2>/dev/null | head -20 >> "$REPORT_FILE"
    
    echo "  ✓ File analysis complete"
fi

# PHASE 6: BACKUP VERIFICATION
echo ""
echo "🔍 PHASE 6: Verifying backups..."
echo ""

if [ -d "$GHOST_PATH" ]; then
    BACKUP_COUNT=$(find "$GHOST_PATH" -name "*backup*" -o -name "*BACKUP*" 2>/dev/null | wc -l | tr -d ' ')
    TM_COUNT=$(find "$GHOST_PATH" -name "*TimeMachine*" -o -name "*Time Machine*" 2>/dev/null | wc -l | tr -d ' ')
    echo "  Found $BACKUP_COUNT backup-related items"
    echo "  Found $TM_COUNT Time Machine items"
    echo "Backup items: $BACKUP_COUNT" >> "$REPORT_FILE"
    echo "Time Machine items: $TM_COUNT" >> "$REPORT_FILE"
fi

# PHASE 7: CREATE DESKTOP ALIAS IF NEEDED
echo ""
echo "🔍 PHASE 7: Creating Desktop alias if needed..."
echo ""

GHOST_PATH=""
if [ -d "/Volumes/MC_RESCUE" ]; then
    GHOST_PATH="/Volumes/MC_RESCUE"
elif [ -d "/Volumes/TM_BackUp" ]; then
    GHOST_PATH="/Volumes/TM_BackUp"
elif [ -n "$GHOST_VOLUMES" ]; then
    GHOST_PATH="/Volumes/$(echo "$GHOST_VOLUMES" | head -1)"
fi

if [ -n "$GHOST_PATH" ] && [ -d "$GHOST_PATH" ]; then
    echo "✓ Found GHOST drive at: $GHOST_PATH"
    echo "GHOST Drive Location: $GHOST_PATH" >> "$REPORT_FILE"
    
    # Create alias on Desktop if it doesn't exist
    if [ ! -e "$HOME/Desktop/GHOST_DRIVE" ]; then
        ln -s "$GHOST_PATH" "$HOME/Desktop/GHOST_DRIVE"
        echo "✓ Created Desktop alias: ~/Desktop/GHOST_DRIVE"
        echo "Created Desktop alias: ~/Desktop/GHOST_DRIVE -> $GHOST_PATH" >> "$REPORT_FILE"
    else
        echo "✓ Desktop alias already exists"
    fi
else
    echo "⚠️  GHOST drive not found or not mounted"
    echo "GHOST drive not found" >> "$REPORT_FILE"
fi

# SUMMARY
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  FIX COMPLETE                                     ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📄 Report saved to: $REPORT_FILE"
echo ""
echo "✅ GHOST Drive fix complete!"
echo ""


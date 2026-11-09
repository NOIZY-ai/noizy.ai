#!/bin/bash

# LIBRARIAN v1.0 // NOIZY.ai AUDIO ORGANIZER
# AUTOMATED SORTING & NORMALIZATION PROTOCOL

ROOT_DIR="$(pwd)/Audio_Master_2026"
mkdir -p "$ROOT_DIR"

# DETECTED REAL-WORLD VOLUMES (The "Leviathan")
VOL_SAMPLE="/Volumes/SAMPLE_MASTER"
VOL_DESIGN="/Volumes/SOUND_DESIGN"
VOL_12TB="/Volumes/12TB"

# MIGRATION DESTINATION (The "Ark")
# PRIMARY: Google Drive
# FALLBACK: 12TB (If GDrive is read-only)
MIGRATE_DEST="$HOME/Google Drive/Audio_Master_Unified"
if [ ! -w "$HOME/Google Drive" ]; then
    echo "WARNING: Google Drive is Read-Only. Switching to Local 12TB Staging."
    MIGRATE_DEST="$VOL_12TB/Audio_Master_Unified_Staging"
fi
MIGRATE_LOG="$AI_BRAIN/migration_log.txt"

INBOX="$ROOT_DIR/00_INBOX_TO_PROCESS"
AI_BRAIN="$ROOT_DIR/05_AI_BRAIN"
mkdir -p "$INBOX"
mkdir -p "$AI_BRAIN"

LOG_FILE="$AI_BRAIN/librarian_log.txt"
MANIFEST="$AI_BRAIN/manifest.json"

# If volumes exist, add them to scan targets
echo "Mounting Neuro-Link to Drives..." | tee -a "$LOG_FILE"
SCAN_TARGETS=("$ROOT_DIR/00_INBOX_TO_PROCESS")

if [ -d "$VOL_SAMPLE" ]; then SCAN_TARGETS+=("$VOL_SAMPLE"); echo "CONNECTED: SAMPLE_MASTER" | tee -a "$LOG_FILE"; fi
if [ -d "$VOL_DESIGN" ]; then SCAN_TARGETS+=("$VOL_DESIGN"); echo "CONNECTED: SOUND_DESIGN" | tee -a "$LOG_FILE"; fi

echo "Root: $ROOT_DIR" | tee -a "$LOG_FILE"

# Function: Normalize Filenames (Sanitize)
normalize_names() {
    echo "Scanning for irregular filenames..." | tee -a "$LOG_FILE"
    find "$ROOT_DIR" -depth -name "* *" -execdir bash -c 'mv "$1" "${1// /_}"' _ {} \;
    # Convert to lowercase (Optional - keeping case for now to be safe with project links)
}

# Function: Generate AI Manifest
generate_manifest() {
    echo "Generating AI Manifest..." | tee -a "$LOG_FILE"
    echo "{" > "$MANIFEST"
    echo "  \"scan_date\": \"$(date)\"," >> "$MANIFEST"
    echo "  \"assets\": [" >> "$MANIFEST"
    
    first=true
    
    for target in "${SCAN_TARGETS[@]}"; do
        echo "Scanning Sector: $target" | tee -a "$LOG_FILE"
        # Limit depth to avoid infinite scan on 12TB drives for this demo
        find "$target" -maxdepth 3 -type f \( -name "*.wav" -o -name "*.mp3" -o -name "*.aif" -o -name "*.ogg" \) | while read -r file; do
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$MANIFEST"
            fi
            filename=$(basename "$file")
            filepath=$(realpath "$file")
            # size=$(du -h "$file" | cut -f1) # optimize speed
            
            # Simple JSON entry
            echo "    {" >> "$MANIFEST"
            echo "      \"name\": \"$filename\"," >> "$MANIFEST"
            echo "      \"path\": \"$filepath\"," >> "$MANIFEST"
            echo "      \"source\": \"$target\"," >> "$MANIFEST"
            echo "      \"type\": \"audio\"" >> "$MANIFEST"
            echo -n "    }" >> "$MANIFEST"
        done
    done
    
    echo "" >> "$MANIFEST"
    echo "  ]" >> "$MANIFEST"
    echo "}" >> "$MANIFEST"
    echo "Manifest Updated: $MANIFEST" | tee -a "$LOG_FILE"
}

# Function: Sort Inbox (Mock Logic - Safe Mode)
# Only moves if strict extensions match known categories, otherwise warns.
sort_inbox() {
    echo "Checking Inbox..." | tee -a "$LOG_FILE"
    count=$(ls -1 "$INBOX" | wc -l)
    if [ "$count" -eq 0 ]; then
        echo "Inbox is empty. Standing by." | tee -a "$LOG_FILE"
    else
        echo "Found $count items in Inbox. Human Review Recommended before Auto-Sort." | tee -a "$LOG_FILE"
        # In a real scenario, we would move *.wav to a temp folder or try to detect content.
        # For now, we just list them.
        ls -lh "$INBOX" >> "$LOG_FILE"
    fi
}

# Function: Migrate Audio (to Google Drive or 12TB Staging)
migrate_audio() {
    local dry_run="$1"
    echo "Initiating Migration Protocol..." | tee -a "$LOG_FILE"
    echo "Destination: $MIGRATE_DEST" | tee -a "$LOG_FILE"

    if [ "$dry_run" = true ]; then
        echo "DRY RUN: No files will be moved." | tee -a "$LOG_FILE"
        local rsync_opts="-n" # Dry run option for rsync
    else
        echo "LIVE RUN: Files will be moved." | tee -a "$LOG_FILE"
        local rsync_opts=""
    fi

    mkdir -p "$MIGRATE_DEST" # Ensure destination exists

    for target in "${SCAN_TARGETS[@]}"; do
        # Exclude the AI_BRAIN directory from migration if it's within a target
        if [[ "$target" == *"$AI_BRAIN"* ]]; then
            echo "Skipping AI_BRAIN directory from migration: $target" | tee -a "$LOG_FILE"
            continue
        fi

        # Construct destination path, mirroring source structure
        local dest_path="$MIGRATE_DEST/$(basename "$target")"
        mkdir -p "$dest_path"

        if [ "$dry_run" = true ]; then
            echo "[DRY RUN] Migrating $target to $dest_path..." | tee -a "$LOG_FILE"
            # rsync options: archive, verbose, human-readable, progress, partial (for resume), inplace, dry-run
            rsync $rsync_opts -avh --progress --partial --inplace "$target/" "$dest_path/" >> "$MIGRATE_LOG" 2>&1
        else
            echo "[LIVE] Migrating $target to $dest_path..." | tee -a "$LOG_FILE"
            # rsync options: archive, verbose, human-readable, progress, partial (for resume), inplace
            rsync $rsync_opts -avh --progress --partial --inplace "$target/" "$dest_path/" >> "$MIGRATE_LOG" 2>&1
        fi
    done
    echo "Migration Protocol Complete." | tee -a "$LOG_FILE"
}


# Execution
normalize_names   # REPAIR PROTOCOL ACTIVE
sort_inbox        # SORTING ACTIVE
echo "Mode: Scanning & Migration Setup"
generate_manifest

# Uncomment to run migration:
migrate_audio true  # Dry Run
migrate_audio false # LIVE

echo "Librarian Cycle Complete." | tee -a "$LOG_FILE"
date >> "$LOG_FILE"

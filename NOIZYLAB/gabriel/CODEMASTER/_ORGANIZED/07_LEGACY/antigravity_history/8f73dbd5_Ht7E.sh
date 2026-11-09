#!/bin/bash

# LIBRARIAN v1.0 // NOIZY.ai AUDIO ORGANIZER
# AUTOMATED SORTING & NORMALIZATION PROTOCOL

ROOT_DIR="$(pwd)/Audio_Master_2026"
INBOX="$ROOT_DIR/00_INBOX_TO_PROCESS"
LOG_FILE="$ROOT_DIR/05_AI_BRAIN/librarian_log.txt"
MANIFEST="$ROOT_DIR/05_AI_BRAIN/manifest.json"

echo "Initializing Librarian Protocol..." | tee -a "$LOG_FILE"
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
    find "$ROOT_DIR" -type f \( -name "*.wav" -o -name "*.mp3" -o -name "*.aif" -o -name "*.ogg" \) | while read -r file; do
        if [ "$first" = true ]; then
            first=false
        else
            echo "," >> "$MANIFEST"
        fi
        filename=$(basename "$file")
        filepath=$(realpath "$file")
        size=$(du -h "$file" | cut -f1)
        
        # Simple JSON entry
        echo "    {" >> "$MANIFEST"
        echo "      \"name\": \"$filename\"," >> "$MANIFEST"
        echo "      \"path\": \"$filepath\"," >> "$MANIFEST"
        echo "      \"size\": \"$size\"," >> "$MANIFEST"
        echo "      \"type\": \"audio\"" >> "$MANIFEST"
        echo -n "    }" >> "$MANIFEST"
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

# Execution
normalize_names
sort_inbox
generate_manifest

echo "Librarian Cycle Complete." | tee -a "$LOG_FILE"
date >> "$LOG_FILE"

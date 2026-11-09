#!/bin/bash
# GABRIEL File Suite - Nightly Automation Script
# This script runs scheduled scans, classification, and organization

set -e

# Configuration
GABRIEL_HOME="/Users/rsp_ms/GABRIEL/THE_FAMILY/GABRIEL/gabriel_file_suite"
DB_PATH="/Volumes/GABRIEL/gabriel_suite.db"
LOG_FILE="/Volumes/GABRIEL/logs/automation_$(date +%Y%m%d).log"

# Python environment
PYTHON="python3"
if [ -d "$GABRIEL_HOME/venv" ]; then
    source "$GABRIEL_HOME/venv/bin/activate"
fi

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "GABRIEL File Suite - Nightly Automation"
log "=========================================="

# Step 1: Scan volumes
log "Step 1/4: Scanning volumes..."
for volume in /Volumes/GABRIEL /Volumes/NOIZYWIN /Volumes/OMEN; do
    if [ -d "$volume" ]; then
        log "Scanning $volume..."
        $PYTHON "$GABRIEL_HOME/gabriel.py" scan "$volume" --database "$DB_PATH" --workers 8 >> "$LOG_FILE" 2>&1
    else
        log "Warning: Volume $volume not mounted"
    fi
done

# Step 2: Classify files
log "Step 2/4: Classifying new files..."
$PYTHON "$GABRIEL_HOME/gabriel.py" classify "$DB_PATH" --batch 500 >> "$LOG_FILE" 2>&1

# Step 3: Organize files (dry-run by default for safety)
log "Step 3/4: Organizing files (dry-run)..."
$PYTHON "$GABRIEL_HOME/gabriel.py" organize "$DB_PATH" "/Volumes/GABRIEL/Organized" \
    --mode symlink --dry-run --manifest "/Volumes/GABRIEL/manifest_$(date +%Y%m%d).json" >> "$LOG_FILE" 2>&1

# Step 4: Find duplicates
log "Step 4/4: Finding duplicates..."
$PYTHON "$GABRIEL_HOME/gabriel.py" duplicates "$DB_PATH" --action list >> "$LOG_FILE" 2>&1

# Database stats
log "Generating statistics..."
$PYTHON "$GABRIEL_HOME/gabriel.py" stats "$DB_PATH" >> "$LOG_FILE" 2>&1

# Backup database
log "Backing up database..."
BACKUP_DIR="/Volumes/GABRIEL/Backups"
mkdir -p "$BACKUP_DIR"
cp "$DB_PATH" "$BACKUP_DIR/gabriel_suite_$(date +%Y%m%d_%H%M%S).db"

# Cleanup old logs (keep 30 days)
find "/Volumes/GABRIEL/logs" -name "automation_*.log" -mtime +30 -delete

# Cleanup old backups (keep 7 days)
find "$BACKUP_DIR" -name "gabriel_suite_*.db" -mtime +7 -delete

log "=========================================="
log "Automation complete!"
log "=========================================="

# Send summary notification (optional - requires setup)
# osascript -e 'display notification "GABRIEL automation complete" with title "File Suite"'

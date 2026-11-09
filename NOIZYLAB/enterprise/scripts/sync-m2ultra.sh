#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# M2 Ultra Archive Sync
# ═══════════════════════════════════════════════════════════════════
# Syncs code from M2 Ultra to the enterprise archive.
# Run this from the enterprise repo root.
#
# Usage:
#   ./scripts/sync-m2ultra.sh [m2ultra-host] [source-path]
#
# Examples:
#   ./scripts/sync-m2ultra.sh m2ultra.local /Users/m2ultra/NOIZYLAB
#   ./scripts/sync-m2ultra.sh 192.168.1.100 /Users/m2ultra/projects
# ═══════════════════════════════════════════════════════════════════

set -e

M2ULTRA_HOST="${1:-m2ultra.local}"
M2ULTRA_PATH="${2:-/Users/m2ultra/NOIZYLAB}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_DIR="archive/m2ultra"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              M2 Ultra Archive Sync                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "Host:      $M2ULTRA_HOST"
echo "Path:      $M2ULTRA_PATH"
echo "Timestamp: $TIMESTAMP"
echo "Archive:   $ARCHIVE_DIR"
echo ""

# Check if we can reach M2 Ultra
echo -e "${YELLOW}Testing connection...${NC}"
if ! ssh -q -o ConnectTimeout=5 "$M2ULTRA_HOST" exit 2>/dev/null; then
    echo "ERROR: Cannot connect to $M2ULTRA_HOST"
    echo ""
    echo "Options:"
    echo "  1. Check if M2 Ultra is on the network"
    echo "  2. Verify SSH access: ssh $M2ULTRA_HOST"
    echo "  3. Use IP address instead of hostname"
    echo "  4. For local sync, use migrate-to-enterprise.py instead"
    exit 1
fi

echo -e "${GREEN}Connected!${NC}"
echo ""

# Create archive subdirectory for this sync
SYNC_DIR="$ARCHIVE_DIR/sync_$TIMESTAMP"
mkdir -p "$SYNC_DIR"

# Define what to sync
# Adjust these paths based on what exists on your M2 Ultra
SYNC_ITEMS=(
    "gabriel"
    "voice"
    "experiments"
    "scripts"
    "models"
    "audio_output"
)

echo -e "${YELLOW}Syncing from M2 Ultra...${NC}"
for item in "${SYNC_ITEMS[@]}"; do
    SRC="$M2ULTRA_HOST:$M2ULTRA_PATH/$item"
    DST="$SYNC_DIR/$item"

    echo "  Syncing: $item"

    # Use rsync with archive mode, compression, and progress
    rsync -avz --progress \
        --exclude='*.pyc' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='venv' \
        --exclude='.venv' \
        --exclude='*.wav' \
        --exclude='*.mp3' \
        --exclude='*.mp4' \
        "$SRC" "$DST" 2>/dev/null || echo "    (skipped - not found)"
done

# Create sync manifest
cat > "$SYNC_DIR/SYNC_MANIFEST.md" << EOF
# M2 Ultra Sync Manifest

**Timestamp:** $TIMESTAMP
**Host:** $M2ULTRA_HOST
**Source:** $M2ULTRA_PATH

## Synced Items

$(for item in "${SYNC_ITEMS[@]}"; do
    if [ -d "$SYNC_DIR/$item" ]; then
        echo "- [x] $item"
    else
        echo "- [ ] $item (not found)"
    fi
done)

## Notes

Add any relevant notes about this sync here.
EOF

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Sync complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Archive location: $SYNC_DIR"
echo ""
echo "Next steps:"
echo "  1. Review synced files in $SYNC_DIR"
echo "  2. Move relevant code to projects/ using migrate script"
echo "  3. Update archive/MIGRATION_LOG.md"
echo ""

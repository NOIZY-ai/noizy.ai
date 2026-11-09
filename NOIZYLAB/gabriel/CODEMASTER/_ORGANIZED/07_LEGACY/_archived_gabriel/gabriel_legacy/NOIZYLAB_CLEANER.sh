#!/bin/zsh
# ═══════════════════════════════════════════════════════════════════════════
#  🔥 NOIZYLAB SYSTEM CLEANER - ZERO LATENCY EDITION
# ═══════════════════════════════════════════════════════════════════════════
# Cleans: __pycache__, .pyc, logs, temp files, DS_Store, stale data

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

GABRIEL_ROOT="/Users/m2ultra/NOIZYLAB/GABRIEL"
TOTAL_FREED=0

echo ""
echo "${MAGENTA}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo "${MAGENTA}║${NC}  ${BOLD}🔥 NOIZYLAB SYSTEM CLEANER${NC}                                       ${MAGENTA}║${NC}"
echo "${MAGENTA}║${NC}     ${CYAN}Zero Latency • Maximum Performance • Clean State${NC}            ${MAGENTA}║${NC}"
echo "${MAGENTA}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to calculate size
get_size() {
    du -sk "$1" 2>/dev/null | awk '{print $1}'
}

# Function to format size
format_size() {
    local kb=$1
    if [ $kb -gt 1048576 ]; then
        echo "$(echo "scale=1; $kb/1048576" | bc)GB"
    elif [ $kb -gt 1024 ]; then
        echo "$(echo "scale=1; $kb/1024" | bc)MB"
    else
        echo "${kb}KB"
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
echo "${YELLOW}━━━ PHASE 1: ROOT PYCACHE ━━━${NC}"
# ─────────────────────────────────────────────────────────────────────────────
if [ -d "$GABRIEL_ROOT/__pycache__" ]; then
    SIZE=$(get_size "$GABRIEL_ROOT/__pycache__")
    rm -rf "$GABRIEL_ROOT/__pycache__"
    TOTAL_FREED=$((TOTAL_FREED + SIZE))
    echo "${GREEN}✅ Removed root __pycache__ ($(format_size $SIZE))${NC}"
else
    echo "   No root __pycache__ found"
fi

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "${YELLOW}━━━ PHASE 2: LOG FILES ━━━${NC}"
# ─────────────────────────────────────────────────────────────────────────────
for logfile in "$GABRIEL_ROOT"/*.log; do
    if [ -f "$logfile" ]; then
        SIZE=$(get_size "$logfile")
        rm -f "$logfile"
        TOTAL_FREED=$((TOTAL_FREED + SIZE))
        echo "${GREEN}✅ Removed $(basename $logfile) ($(format_size $SIZE))${NC}"
    fi
done

# Clean logs directory
if [ -d "$GABRIEL_ROOT/logs" ]; then
    SIZE=$(get_size "$GABRIEL_ROOT/logs")
    rm -rf "$GABRIEL_ROOT/logs"/*
    TOTAL_FREED=$((TOTAL_FREED + SIZE))
    echo "${GREEN}✅ Cleared logs/ directory ($(format_size $SIZE))${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "${YELLOW}━━━ PHASE 3: STALE JSON DATA ━━━${NC}"
# ─────────────────────────────────────────────────────────────────────────────
# Remove large analysis files that can be regenerated
if [ -f "$GABRIEL_ROOT/code_analysis.json" ]; then
    SIZE=$(get_size "$GABRIEL_ROOT/code_analysis.json")
    rm -f "$GABRIEL_ROOT/code_analysis.json"
    TOTAL_FREED=$((TOTAL_FREED + SIZE))
    echo "${GREEN}✅ Removed code_analysis.json ($(format_size $SIZE))${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "${YELLOW}━━━ PHASE 4: .DS_STORE FILES ━━━${NC}"
# ─────────────────────────────────────────────────────────────────────────────
DS_COUNT=$(find "$GABRIEL_ROOT" -name ".DS_Store" -type f 2>/dev/null | wc -l | tr -d ' ')
find "$GABRIEL_ROOT" -name ".DS_Store" -type f -delete 2>/dev/null
echo "${GREEN}✅ Removed $DS_COUNT .DS_Store files${NC}"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "${YELLOW}━━━ PHASE 5: MODULES PYCACHE ━━━${NC}"
# ─────────────────────────────────────────────────────────────────────────────
if [ -d "$GABRIEL_ROOT/modules" ]; then
    PYCACHE_COUNT=0
    for dir in $(find "$GABRIEL_ROOT/modules" -type d -name "__pycache__" 2>/dev/null); do
        SIZE=$(get_size "$dir")
        rm -rf "$dir"
        TOTAL_FREED=$((TOTAL_FREED + SIZE))
        PYCACHE_COUNT=$((PYCACHE_COUNT + 1))
    done
    echo "${GREEN}✅ Removed $PYCACHE_COUNT __pycache__ dirs from modules/${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "${YELLOW}━━━ PHASE 6: TEMP FILES ━━━${NC}"
# ─────────────────────────────────────────────────────────────────────────────
TEMP_PATTERNS=("*.tmp" "*.temp" "*.bak" "*~" "*.swp" "*.swo")
TEMP_COUNT=0
for pattern in "${TEMP_PATTERNS[@]}"; do
    count=$(find "$GABRIEL_ROOT" -name "$pattern" -type f 2>/dev/null | wc -l | tr -d ' ')
    TEMP_COUNT=$((TEMP_COUNT + count))
    find "$GABRIEL_ROOT" -name "$pattern" -type f -delete 2>/dev/null
done
echo "${GREEN}✅ Removed $TEMP_COUNT temp files${NC}"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "${MAGENTA}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo "${MAGENTA}║${NC}  ${BOLD}🎯 CLEANUP COMPLETE${NC}                                              ${MAGENTA}║${NC}"
echo "${MAGENTA}╠═══════════════════════════════════════════════════════════════════╣${NC}"
echo "${MAGENTA}║${NC}  ${GREEN}Total Space Freed: $(format_size $TOTAL_FREED)${NC}                                     ${MAGENTA}║${NC}"
echo "${MAGENTA}║${NC}  ${CYAN}System Status: CLEAN & OPTIMIZED${NC}                                ${MAGENTA}║${NC}"
echo "${MAGENTA}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

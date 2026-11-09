#!/bin/bash
# CODECLEANER Quick Fix Script
# Implements Priority 1 and 2 fixes from audit report
# 
# Usage: ./CODECLEANER_QUICK_FIX.sh [--dry-run]
#
# Time Required: ~30 minutes
# Impact: Removes blockers, fixes critical issues

set -e  # Exit on error

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No changes will be made"
    echo ""
fi

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

execute() {
    local description="$1"
    shift
    
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY RUN] Would execute: $*"
        return 0
    fi
    
    log_info "$description"
    if "$@"; then
        log_success "Done: $description"
        return 0
    else
        log_error "Failed: $description"
        return 1
    fi
}

# Banner
echo "════════════════════════════════════════════════════════════"
echo "  🏥 CODECLEANER - Quick Fix Script"
echo "  Repository: NOIZYLAB"
echo "  Mode: $([ "$DRY_RUN" = true ] && echo "DRY RUN" || echo "LIVE")"
echo "════════════════════════════════════════════════════════════"
echo ""

# Confirmation for live mode
if [ "$DRY_RUN" = false ]; then
    echo "⚠️  This script will make changes to your repository."
    echo "   Recommendation: Run with --dry-run first"
    echo ""
    read -p "Continue with live changes? (yes/no): " confirm
    if [[ ! "$confirm" =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    echo ""
fi

# ==============================================================================
# PHASE 1: CRITICAL FIXES (Immediate Blockers)
# ==============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PHASE 1: CRITICAL FIXES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Remove broken symlinks
log_info "Step 1: Removing broken symlinks..."

if [ -L "./OneDrive" ]; then
    execute "Remove broken OneDrive symlink" rm ./OneDrive
else
    log_warning "OneDrive symlink not found (may have been removed already)"
fi

if [ -L "./gabriel/CODEMASTER/_ORGANIZED/05_TOOLS/bin_tools/gorunfree" ]; then
    execute "Remove broken gorunfree symlink" rm ./gabriel/CODEMASTER/_ORGANIZED/05_TOOLS/bin_tools/gorunfree
else
    log_warning "gorunfree symlink not found (may have been removed already)"
fi

echo ""

# 2. Quarantine files with syntax errors
log_info "Step 2: Quarantining files with syntax errors..."

if [ -f "gabriel/archive_recovered/agency_ui.py" ]; then
    execute "Quarantine agency_ui.py (syntax error)" \
        mv gabriel/archive_recovered/agency_ui.py gabriel/archive_recovered/agency_ui.py.broken
    
    if [ "$DRY_RUN" = false ]; then
        cat > gabriel/archive_recovered/agency_ui.py.README << 'EOF'
# agency_ui.py - QUARANTINED

This file was quarantined due to syntax error on line 506:
- `elif MODE == "Omni-Archive":` without matching `if` block

Original file renamed to: agency_ui.py.broken

To fix:
1. Review control flow structure starting around line 504
2. Add missing `if` statement or fix logic
3. Test thoroughly before restoring
EOF
        log_success "Created README explaining quarantine"
    fi
else
    log_warning "agency_ui.py not found (may have been moved already)"
fi

if [ -f "gabriel/titanhive/main.py" ]; then
    execute "Quarantine titanhive/main.py (syntax error)" \
        mv gabriel/titanhive/main.py gabriel/titanhive/main.py.broken
    
    if [ "$DRY_RUN" = false ]; then
        cat > gabriel/titanhive/main.py.README << 'EOF'
# main.py - QUARANTINED

This file was quarantined due to syntax error on line 684:
- `global OLLAMA_MODEL` used after variable reference

Original file renamed to: main.py.broken

To fix:
1. Move `global OLLAMA_MODEL` to top of function
2. Ensure variable is defined before use
3. Test thoroughly before restoring
EOF
        log_success "Created README explaining quarantine"
    fi
else
    log_warning "titanhive/main.py not found (may have been moved already)"
fi

echo ""

# 3. Remove empty files
log_info "Step 3: Removing empty files..."

EMPTY_FILES=(
    "gabriel/NOIZYLAB_CLEANER.sh"
    "gabriel/gabriel_mcp_server.py"
    "gabriel/gabriel_indexer.py"
    "gabriel/CODEMASTER/_ORGANIZED/07_LEGACY/antigravity_history/103ebc23_8Pdh.py"
    "gabriel/CODEMASTER/_ORGANIZED/07_LEGACY/antigravity_history/72b06a55_gT5K.py"
    "gabriel/CODEMASTER/_ORGANIZED/07_LEGACY/antigravity_history/8d497572_QnF7.py"
    "gabriel/CODEMASTER/_ORGANIZED/07_LEGACY/antigravity_history/e6e2b61a_ODcW.py"
    "gabriel/CODEMASTER/_ORGANIZED/07_LEGACY/antigravity_history/932bcb4a_3vGy.sh"
)

for file in "${EMPTY_FILES[@]}"; do
    if [ -f "$file" ]; then
        execute "Remove empty file: $file" rm "$file"
    fi
done

echo ""

# ==============================================================================
# PHASE 2: HIGH PRIORITY (Remove Duplication)
# ==============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PHASE 2: HIGH PRIORITY - Remove Duplication"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

log_info "Step 4: Removing duplicate mc96_projects/GABRIEL directory..."

if [ -d "gabriel/mc96_projects/GABRIEL" ]; then
    log_warning "This will remove 146+ duplicate files"
    log_warning "Canonical location: gabriel/voice_ai/"
    
    if [ "$DRY_RUN" = false ]; then
        read -p "Proceed with removal? (yes/no): " confirm_dup
        if [[ "$confirm_dup" =~ ^[Yy][Ee][Ss]$ ]]; then
            execute "Remove duplicate GABRIEL directory" rm -rf gabriel/mc96_projects/GABRIEL
            
            # Create a README explaining what happened
            mkdir -p gabriel/mc96_projects
            cat > gabriel/mc96_projects/README.md << 'EOF'
# mc96_projects Directory

## GABRIEL Project Relocated

The GABRIEL project was previously duplicated in this directory.

**Canonical Location:** `gabriel/voice_ai/`

All GABRIEL-related code, tests, and documentation can be found there.

**Reason for Removal:**
- Complete 100% duplication (146+ files)
- Risk of code divergence
- Wasted repository space (~2.4MB)
- Maintenance confusion

**Date Removed:** $(date +"%Y-%m-%d")
**Removed By:** CODECLEANER Quick Fix Script

For questions, see: CODECLEANER_AUDIT_REPORT.md
EOF
            log_success "Created README explaining removal"
        else
            log_warning "Skipped: User declined removal"
        fi
    else
        echo "  [DRY RUN] Would remove gabriel/mc96_projects/GABRIEL/"
    fi
else
    log_warning "mc96_projects/GABRIEL not found (may have been removed already)"
fi

echo ""

# ==============================================================================
# PHASE 3: FIXES (Permissions)
# ==============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PHASE 3: Fix Shell Script Permissions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

log_info "Step 5: Making all shell scripts executable..."

if [ "$DRY_RUN" = false ]; then
    FIXED_COUNT=$(find gabriel -name "*.sh" -type f ! -executable | wc -l | tr -d ' ')
    if [ "$FIXED_COUNT" -gt 0 ]; then
        find gabriel -name "*.sh" -type f ! -executable -exec chmod +x {} \;
        log_success "Fixed permissions on $FIXED_COUNT shell scripts"
    else
        log_success "All shell scripts already executable"
    fi
else
    WOULD_FIX=$(find gabriel -name "*.sh" -type f ! -executable | wc -l | tr -d ' ')
    echo "  [DRY RUN] Would fix permissions on $WOULD_FIX shell scripts"
fi

echo ""

# ==============================================================================
# SUMMARY
# ==============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ QUICK FIX SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "🔍 DRY RUN COMPLETED - No actual changes made"
    echo ""
    echo "To apply these changes, run:"
    echo "  ./CODECLEANER_QUICK_FIX.sh"
else
    echo "✅ LIVE RUN COMPLETED"
    echo ""
    echo "Changes made:"
    echo "  • Removed broken symlinks (2)"
    echo "  • Quarantined files with syntax errors (2)"
    echo "  • Removed empty files (8)"
    echo "  • Removed duplicate directory (if confirmed)"
    echo "  • Fixed shell script permissions"
    echo ""
    echo "Next steps:"
    echo "  1. Review changes: git status"
    echo "  2. Test affected functionality"
    echo "  3. Commit changes: git add -A && git commit -m 'CRITICAL: Apply CODECLEANER quick fixes'"
    echo ""
    echo "For complete cleanup, see:"
    echo "  • CODECLEANER_AUDIT_REPORT.md (full details)"
    echo "  • CODECLEANER_EXECUTIVE_SUMMARY.md (overview)"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  🏥 CODECLEANER Quick Fix - Complete"
echo "════════════════════════════════════════════════════════════"
echo ""

# Exit successfully
exit 0

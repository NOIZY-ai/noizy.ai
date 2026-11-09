#!/bin/bash
# =============================================================================
# RUN THIS SCRIPT TO COMPLETE THE CODE CONSOLIDATION
# GABRIEL SYSTEM - GLOBAL FISHNET COMPLETE
# =============================================================================
#
# This script copies the consolidated code to CODEMASTER and pushes to GitHub
#
# RUN WITH: bash RUN_ME_TO_COMPLETE_CONSOLIDATION.sh
#
# =============================================================================

set -e

WORKSPACE="/Users/m2ultra/.gemini/antigravity/playground/iridescent-station"
CODEMASTER="/Users/m2ultra/NOIZYLAB/CODEMASTER"
NOIZYLAB="/Users/m2ultra/NOIZYLAB"

echo "========================================================================"
echo "    COMPLETING GLOBAL FISHNET CODE CONSOLIDATION"
echo "========================================================================"
echo ""

# Step 1: Copy consolidated code to CODEMASTER
echo ">>> Step 1: Copying consolidated code to CODEMASTER..."
cp -rv "$WORKSPACE/consolidated_code/"* "$CODEMASTER/"
echo "   Done!"
echo ""

# Step 2: Show what's now in CODEMASTER
echo ">>> Step 2: CODEMASTER now contains:"
ls -la "$CODEMASTER/"
echo ""

# Step 3: Count total files
echo ">>> Step 3: Total code files in CODEMASTER:"
find "$CODEMASTER" -name "*.py" -o -name "*.sh" | wc -l
echo ""

# Step 4: Git status
echo ">>> Step 4: Git status..."
cd "$NOIZYLAB"
git status
echo ""

# Step 5: Stage, commit, push
echo ">>> Step 5: Staging changes..."
git add -A
echo ""

echo ">>> Step 6: Committing..."
git commit -m "$(cat <<'EOF'
Consolidate all unique code to CODEMASTER - Global Fishnet Complete

Added:
- gabriel_unified/core/ - Dreamchamber Gateway, Universe Flow, etc.
- workspaces_tools/ - Turbo Miner, Hyper Miner, Gabriel Ultra, etc.
- gabriel_v1/ - Original GABRIEL core and tools

30 unique code files consolidated from:
- /Users/m2ultra/.gemini/antigravity/playground/iridescent-station/GABRIEL_UNIFIED
- /Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL

GORUNFREE!!! Global Fishnet Scan Complete.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
echo ""

echo ">>> Step 7: Pushing to GitHub (NOIZY-ai/NOIZYLAB)..."
git push origin main
echo ""

echo "========================================================================"
echo "    CONSOLIDATION COMPLETE!"
echo "========================================================================"
echo ""
echo "✅ 30 unique code files added to CODEMASTER"
echo "✅ Pushed to GitHub: github.com/NOIZY-ai/NOIZYLAB"
echo ""
echo "GORUNFREE!!! GLOBAL FISHNET SCAN COMPLETE!!!"

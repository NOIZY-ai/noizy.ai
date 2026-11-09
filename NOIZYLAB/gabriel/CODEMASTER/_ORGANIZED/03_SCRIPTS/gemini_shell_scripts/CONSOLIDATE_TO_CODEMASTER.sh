#!/bin/bash
# =============================================================================
# CONSOLIDATE UNIQUE CODE TO CODEMASTER
# GABRIEL SYSTEM - GLOBAL FISHNET CONSOLIDATION
# =============================================================================

set -e

CODEMASTER="/Users/m2ultra/NOIZYLAB/CODEMASTER"
WORKSPACE="/Users/m2ultra/.gemini/antigravity/playground/iridescent-station"

echo "========================================================================"
echo "    CONSOLIDATING ALL UNIQUE CODE TO CODEMASTER"
echo "    GLOBAL FISHNET CONSOLIDATION COMPLETE"
echo "========================================================================"
echo ""

# Create target directories
echo "Creating target directories..."
mkdir -p "$CODEMASTER/gabriel_unified/core"
mkdir -p "$CODEMASTER/workspaces_tools"
mkdir -p "$CODEMASTER/gabriel_v1"

# Copy GABRIEL_UNIFIED core
echo ""
echo ">>> Copying GABRIEL_UNIFIED core..."
cp -v "$WORKSPACE/GABRIEL_UNIFIED/core/dreamchamber_gateway.py" "$CODEMASTER/gabriel_unified/core/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/core/hypervelocity_universe_bridge.py" "$CODEMASTER/gabriel_unified/core/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/core/mc96_universe_flow.py" "$CODEMASTER/gabriel_unified/core/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/core/performance_monitor.py" "$CODEMASTER/gabriel_unified/core/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/core/system_optimizer.py" "$CODEMASTER/gabriel_unified/core/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/core/visual_scanner.py" "$CODEMASTER/gabriel_unified/core/" 2>/dev/null || echo "   (already exists or not found)"

# Copy GABRIEL_UNIFIED root scripts
echo ""
echo ">>> Copying GABRIEL_UNIFIED scripts..."
cp -v "$WORKSPACE/GABRIEL_UNIFIED/ACTIVATE_EVERYTHING.py" "$CODEMASTER/gabriel_unified/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/GORUNFREE.sh" "$CODEMASTER/gabriel_unified/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/GORUNFREEX1000.sh" "$CODEMASTER/gabriel_unified/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/MASTER_FLOW.sh" "$CODEMASTER/gabriel_unified/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/GABRIEL_UNIFIED/ULTIMATE_VOICE_FLOW.sh" "$CODEMASTER/gabriel_unified/" 2>/dev/null || echo "   (already exists or not found)"

# Copy workspaces tools
echo ""
echo ">>> Copying workspaces tools..."
for f in hyper_miner.py turbo_miner.py turbo_unify.py turbo_dedupe.py gabriel_ultra.py \
         zero_latency_organize.py zero_latency_optimizer.py portal.py nuke_folders.py \
         organize_folders.py organize_txt.py clean_home_root.py verify_integrity.py \
         google_worker.py app.py gabriel_singularity.py gabriel_m2.py; do
    if [ -f "$WORKSPACE/NOIZYLAB_WORKSPACES_LOCAL/$f" ]; then
        cp -v "$WORKSPACE/NOIZYLAB_WORKSPACES_LOCAL/$f" "$CODEMASTER/workspaces_tools/" 2>/dev/null || echo "   (already exists)"
    fi
done

# Copy GABRIEL_V1
echo ""
echo ">>> Copying GABRIEL_V1..."
cp -v "$WORKSPACE/NOIZYLAB_WORKSPACES_LOCAL/GABRIEL_V1/gabriel_tools.py" "$CODEMASTER/gabriel_v1/" 2>/dev/null || echo "   (already exists or not found)"
cp -v "$WORKSPACE/NOIZYLAB_WORKSPACES_LOCAL/GABRIEL_V1/gabriel_core.py" "$CODEMASTER/gabriel_v1/" 2>/dev/null || echo "   (already exists or not found)"

# Also copy from other known locations
echo ""
echo ">>> Checking other known locations..."

# From m2ultra/noizylab
if [ -d "/Users/m2ultra/m2ultra/noizylab" ]; then
    echo "   Found /Users/m2ultra/m2ultra/noizylab"
    mkdir -p "$CODEMASTER/noizylab_m2ultra"
    cp -v /Users/m2ultra/m2ultra/noizylab/*.py "$CODEMASTER/noizylab_m2ultra/" 2>/dev/null || true
    cp -v /Users/m2ultra/m2ultra/noizylab/*.sh "$CODEMASTER/noizylab_m2ultra/" 2>/dev/null || true
fi

# From .gemini/_script_archive
if [ -d "/Users/m2ultra/.gemini/_script_archive" ]; then
    echo "   Found /Users/m2ultra/.gemini/_script_archive"
    mkdir -p "$CODEMASTER/script_archive"
    cp -v /Users/m2ultra/.gemini/_script_archive/*.py "$CODEMASTER/script_archive/" 2>/dev/null || true
    cp -v /Users/m2ultra/.gemini/_script_archive/*.sh "$CODEMASTER/script_archive/" 2>/dev/null || true
fi

echo ""
echo "========================================================================"
echo "    CONSOLIDATION COMPLETE!"
echo "========================================================================"
echo ""

# Show what's in CODEMASTER now
echo "CODEMASTER Contents:"
ls -la "$CODEMASTER/"
echo ""

# Count files
echo "Total code files in CODEMASTER:"
find "$CODEMASTER" -name "*.py" -o -name "*.sh" | wc -l

echo ""
echo "Now run: cd /Users/m2ultra/NOIZYLAB && git add -A && git commit -m 'Consolidate all unique code to CODEMASTER' && git push"

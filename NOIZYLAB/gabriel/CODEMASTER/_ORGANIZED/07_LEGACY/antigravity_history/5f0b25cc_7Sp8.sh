#!/bin/bash
# 🚀 PEAK AI PERFORMANCE AUTOMATION
# Runs the full maintenance suite for the MC96 Intelligence Core.

BASE_DIR="/Users/m2ultra/.gemini/antigravity/scratch"
MEMCELL_DIR="$BASE_DIR/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL"
DOCTRINE_SCRIPT="$BASE_DIR/ingest_doctrine.py"

echo "========================================"
echo "    🚀 PEAK AI PERFORMANCE PROTOCOL     "
echo "========================================"
date
echo ""

# 1. DOCTRINE INGEST
echo "📜 [1/3] INGESTING LATEST DOCTRINE..."
if [ -f "$DOCTRINE_SCRIPT" ]; then
    python3 "$DOCTRINE_SCRIPT"
else
    echo "⚠️ Doctrine script not found!"
fi
echo ""

# 2. MEMCELL V3 DIAGNOSTICS
echo "🧠 [2/3] RUNNING MEMCELL V3 DIAGNOSTICS..."
if [ -f "$MEMCELL_DIR/MemCell_V3.py" ]; then
    python3 "$MEMCELL_DIR/MemCell_V3.py" test
    
    # 2b. Print Stats
    echo ""
    echo "📊 SYSTEM STATS:"
    python3 "$MEMCELL_DIR/MemCell_V3.py" stats
else
    echo "❌ MemCell V3 Core Missing!"
fi
echo ""

# 3. TRUTH SCAN (Safe Mode)
echo "🛡️ [3/3] VERIFYING TRUTH (SCAN)..."
TRUTH_SCRIPT="$BASE_DIR/memcell_truth_scanner.py"
if [ -f "$TRUTH_SCRIPT" ]; then
    python3 "$TRUTH_SCRIPT"
else
    echo "⚠️ Truth Scanner not found."
fi
echo ""

# 4. KNOWLEDGE CONDENSER
echo "🔮 [4/4] GENERATING CONDENSED WISDOM..."
CONDENSER_SCRIPT="$BASE_DIR/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/Knowledge_Condenser.py"
if [ -f "$CONDENSER_SCRIPT" ]; then
    python3 "$CONDENSER_SCRIPT"
else
    echo "⚠️ Condenser script not found!"
fi

echo ""
echo "========================================"
echo "    ✅ SYSTEM OPTIMIZED & READY         "
echo "========================================"

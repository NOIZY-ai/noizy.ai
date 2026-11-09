#!/bin/zsh
# HEAL_THE_BUILD.sh
# "Crystal Smooth" Global Optimization Protocol

echo "✨ INITIATING HEALING SEQUENCE..."

# 1. PERMISSION REPAIR
echo "🔧 Fixing Permissions..."
TARGETS=(
    "$HOME/NOIZYLAB/scripts"
    "$HOME/Documents/GABRIEL"
)

for dir in "${TARGETS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  -> Scanning $dir"
        find "$dir" -name "*.sh" -exec chmod +x {} \;
        find "$dir" -name "*.py" -exec chmod +x {} \;
    fi
done

# 2. PRUNE DEAD CODE
echo "🧹 Pruning Dead Code..."
find "$HOME/NOIZYLAB" -name "*.tmp" -delete
find "$HOME/NOIZYLAB" -name "*.bak" -delete
find "$HOME/NOIZYLAB" -name ".DS_Store" -delete
echo "  -> Debris cleared."

# 3. VERIFY TURBO SUITE
echo "💎 Verifying Turbo Suite..."
SCRIPTS=(
    "turbo_reset.sh"
    "turbo_net_check.py"
    "turbo_vitals.py"
    "turbo_speed.py"
    "turbo_bridge.py"
    "core/MemCell.py"
)

ALL_GOOD=true
for script in "${SCRIPTS[@]}"; do
    if [ ! -f "$HOME/NOIZYLAB/scripts/$script" ]; then
        echo "❌ MISSING: $script"
        ALL_GOOD=false
    else
        echo "✅ FOUND: $script"
    fi
done

if [ "$ALL_GOOD" = true ]; then
    echo "✨ BUILD STATUS: CRYSTAL SMOOTH"
    
    # 4. FINAL PULSE
    MEMCELL="$HOME/NOIZYLAB/scripts/core/MemCell.py"
    if [ -f "$MEMCELL" ]; then
        "$MEMCELL" track "optimization" "HEAL_THE_BUILD" "Success"
    fi
else
    echo "⚠️  BUILD FRACTURED. CHECK LOGS."
    exit 1
fi

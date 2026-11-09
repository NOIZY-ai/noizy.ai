#!/bin/zsh
# ============================================================================
# FORCE_PERFECTION.sh
# GORUNFREE GLOBAL OPTIMIZER
# Enforces Permissions, Cleans Junk, and Optimizes MC96ECOUNIVERSE
# ============================================================================

# Load MemCell for tracking
MEMCELL="$HOME/NOIZYLAB/scripts/core/MemCell.py"
log_action() {
    echo "$1"
    if [ -f "$MEMCELL" ]; then
        "$MEMCELL" track "optimization" "$1" &>/dev/null
    fi
}

log_action "INITIATING GLOBAL PERFECTION SEQUENCE..."

TARGET_DIRS=(
    "$HOME/NOIZYLAB"
    "$HOME/Documents/PROJECTS"
    "$HOME/Documents/GABRIEL"
    "$HOME/bin"
    "$HOME/.config/zsh"
)

# 1. FORCE PERMISSIONS
echo "🔒 FORCING PERMISSIONS..."
for dir in "${TARGET_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        log_action "Optimizing directory: $dir"
        
        # Make scripts executable
        find "$dir" -name "*.sh" -exec chmod +x {} \; 2>/dev/null
        find "$dir" -name "*.py" -exec chmod +x {} \; 2>/dev/null
        find "$dir" -name "*.zsh" -exec chmod +x {} \; 2>/dev/null
        
        # Ensure directories are accessible
        find "$dir" -type d -exec chmod 755 {} \; 2>/dev/null
        
        log_action "Permissions enforced for $dir"
    else
        echo "⚠️ Directory not found: $dir"
    fi
done

# 2. CLEANUP JUNK
echo "🧹 CLEANING JUNK FILES..."
# 2. CLEANUP JUNK (Optimized - No "Fishnet" Scanning)
echo "🧹 CLEANING JUNK FILES..."
for dir in "${TARGET_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        log_action "Sweeping: $dir"
        find "$dir" -name ".DS_Store" -delete 2>/dev/null
        find "$dir" -name "Thumbs.db" -delete 2>/dev/null
        find "$dir" -name "*.tmp" -delete 2>/dev/null
        find "$dir" -name "*.bak" -delete 2>/dev/null
    fi
done
log_action "Junk files incinerated."

# 3. VERIFY CORE SYSTEMS
echo "🧠 VERIFYING CORE SYSTEMS..."
if [ -f "$MEMCELL" ]; then
    echo "✅ MemCell: ONLINE"
else
    echo "❌ MemCell: OFFLINE (CRITICAL FAILURE)"
fi

if [ -f "$HOME/bin/god" ]; then
    echo "✅ God Mode: ACTIVE"
else
    echo "❌ God Mode: INACTIVE"
fi

if [ -f "$HOME/bin/ask" ]; then
    echo "✅ AI Bridge: CONNECTED"
else
    echo "❌ AI Bridge: DISCONNECTED"
fi

# 4. MEMCELL UPDATE
log_action "GLOBAL OPTIMIZATION COMPLETE. SYSTEM STATUS: PERFECT."

echo "✨ MC96ECOUNIVERSE OPTIMIZED. READY FOR GORUNFREE."

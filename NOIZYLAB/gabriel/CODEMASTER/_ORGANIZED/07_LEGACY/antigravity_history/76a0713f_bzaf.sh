#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# MASTER_REPAIR v3.0 - "HYPERDRIVE EDITION"
# THE ULTIMATE AutoRepair System for MC96 Universe
# Commander: Rob
# ═══════════════════════════════════════════════════════════════════════════════

# --- Strict Mode ---
set -euo pipefail

# --- Configuration ---
NOIZYLAB_HOME="${HOME}/NOIZYLAB"
GUARDIAN_HOME="${NOIZYLAB_HOME}/SystemGuardian"
GABRIEL_HOME="${NOIZYLAB_HOME}/PROJECTS/GABRIEL/workers"
LOG_DIR="${GUARDIAN_HOME}/logs"
LOG_FILE="${LOG_DIR}/master_repair_$(date +%Y%m%d_%H%M%S).log"
ISSUES_FOUND=0
ISSUES_FIXED=0

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# --- Banner ---
banner() {
    echo -e "${MAGENTA}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗             ║"
    echo "║  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗            ║"
    echo "║  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝            ║"
    echo "║  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗            ║"
    echo "║  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║            ║"
    echo "║  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝            ║"
    echo "║               REPAIR v3.0 - HYPERDRIVE EDITION                   ║"
    echo "║                    Commander: ROB                                 ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# --- Logging ---
log() { echo -e "[$(date +%H:%M:%S)] $1" | tee -a "$LOG_FILE"; }
info() { log "${CYAN}[INFO]${NC} $1"; }
warn() { log "${YELLOW}[WARN]${NC} $1"; ((ISSUES_FOUND++)); }
fix() { log "${GREEN}[FIX]${NC} $1"; ((ISSUES_FIXED++)); }
error() { log "${RED}[ERROR]${NC} $1"; }
success() { log "${GREEN}[OK]${NC} $1"; }

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: AI DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════
ai_diagnostics() {
    echo -e "\n${WHITE}▓▓▓ AI DIAGNOSTICS ▓▓▓${NC}"
    
    # CPU Analysis
    CPU_LOAD=$(sysctl -n vm.loadavg | awk '{print $2}')
    CPU_CORES=$(sysctl -n hw.ncpu)
    CPU_RATIO=$(echo "$CPU_LOAD $CPU_CORES" | awk '{printf "%.1f", ($1/$2)*100}')
    
    if (( $(echo "$CPU_RATIO > 80" | bc -l) )); then
        warn "CPU Load Critical: ${CPU_RATIO}%"
    elif (( $(echo "$CPU_RATIO > 50" | bc -l) )); then
        info "CPU Load Moderate: ${CPU_RATIO}%"
    else
        success "CPU Load Healthy: ${CPU_RATIO}%"
    fi
    
    # Memory Analysis
    MEM_TOTAL=$(sysctl -n hw.memsize)
    MEM_TOTAL_GB=$((MEM_TOTAL / 1024 / 1024 / 1024))
    MEM_USED_PERCENT=$(ps -A -o %mem | awk '{s+=$1} END {print int(s)}')
    
    if [ "$MEM_USED_PERCENT" -gt 85 ]; then
        warn "Memory Critical: ${MEM_USED_PERCENT}% of ${MEM_TOTAL_GB}GB"
    elif [ "$MEM_USED_PERCENT" -gt 70 ]; then
        info "Memory Moderate: ${MEM_USED_PERCENT}% of ${MEM_TOTAL_GB}GB"
    else
        success "Memory Healthy: ${MEM_USED_PERCENT}% of ${MEM_TOTAL_GB}GB"
    fi
    
    # Disk Analysis
    DISK_PERCENT=$(df -h / | tail -1 | awk '{gsub(/%/,""); print $5}')
    
    if [ "$DISK_PERCENT" -gt 90 ]; then
        warn "Disk Critical: ${DISK_PERCENT}% full"
    elif [ "$DISK_PERCENT" -gt 75 ]; then
        info "Disk Moderate: ${DISK_PERCENT}% full"
    else
        success "Disk Healthy: ${DISK_PERCENT}% full"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: AUTO-FIX ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
autofix_engine() {
    echo -e "\n${WHITE}▓▓▓ AUTO-FIX ENGINE ▓▓▓${NC}"
    
    # Fix 1: Broken symlinks
    info "Scanning for broken symlinks..."
    BROKEN_LINKS=$(find "$NOIZYLAB_HOME" -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BROKEN_LINKS" -gt 0 ]; then
        warn "Found $BROKEN_LINKS broken symlinks"
        find "$NOIZYLAB_HOME" -type l ! -exec test -e {} \; -delete 2>/dev/null || true
        fix "Removed broken symlinks"
    else
        success "No broken symlinks"
    fi
    
    # Fix 2: Empty directories
    info "Cleaning empty directories..."
    EMPTY_DIRS=$(find "$NOIZYLAB_HOME" -type d -empty 2>/dev/null | wc -l | tr -d ' ')
    if [ "$EMPTY_DIRS" -gt 0 ]; then
        find "$NOIZYLAB_HOME" -type d -empty -delete 2>/dev/null || true
        fix "Removed $EMPTY_DIRS empty directories"
    else
        success "No empty directories"
    fi
    
    # Fix 3: Permission issues on scripts
    info "Fixing script permissions..."
    FIXED_PERMS=0
    while IFS= read -r script; do
        if [ ! -x "$script" ]; then
            chmod +x "$script" 2>/dev/null && ((FIXED_PERMS++))
        fi
    done < <(find "$NOIZYLAB_HOME" -name "*.sh" -type f 2>/dev/null)
    
    if [ "$FIXED_PERMS" -gt 0 ]; then
        fix "Fixed permissions on $FIXED_PERMS scripts"
    else
        success "All scripts executable"
    fi
    
    # Fix 4: Python cache cleanup
    info "Cleaning Python caches..."
    PYCACHE_COUNT=$(find "$NOIZYLAB_HOME" -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$PYCACHE_COUNT" -gt 0 ]; then
        find "$NOIZYLAB_HOME" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find "$NOIZYLAB_HOME" -name "*.pyc" -delete 2>/dev/null || true
        fix "Cleaned $PYCACHE_COUNT Python cache directories"
    else
        success "Python caches clean"
    fi
    
    # Fix 5: DS_Store cleanup
    info "Removing .DS_Store files..."
    DS_COUNT=$(find "$NOIZYLAB_HOME" -name ".DS_Store" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$DS_COUNT" -gt 0 ]; then
        find "$NOIZYLAB_HOME" -name ".DS_Store" -delete 2>/dev/null || true
        fix "Removed $DS_COUNT .DS_Store files"
    else
        success "No .DS_Store files"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: STORAGE HEALTH (PARALLEL)
# ═══════════════════════════════════════════════════════════════════════════════
storage_health() {
    echo -e "\n${WHITE}▓▓▓ STORAGE HEALTH SCAN ▓▓▓${NC}"
    
    # Scan all volumes in parallel
    for vol in /Volumes/*; do
        if [ -d "$vol" ] && [ "$vol" != "/Volumes/M2Ultra" ]; then
            (
                VOL_NAME=$(basename "$vol")
                VOL_INFO=$(df -h "$vol" 2>/dev/null | tail -1)
                VOL_PERCENT=$(echo "$VOL_INFO" | awk '{gsub(/%/,""); print $5}')
                VOL_AVAIL=$(echo "$VOL_INFO" | awk '{print $4}')
                
                if [ -n "$VOL_PERCENT" ]; then
                    if [ "$VOL_PERCENT" -gt 95 ]; then
                        echo -e "${RED}🔴 $VOL_NAME: ${VOL_PERCENT}% (${VOL_AVAIL} free) - CRITICAL${NC}"
                    elif [ "$VOL_PERCENT" -gt 85 ]; then
                        echo -e "${YELLOW}⚠️  $VOL_NAME: ${VOL_PERCENT}% (${VOL_AVAIL} free) - WARNING${NC}"
                    else
                        echo -e "${GREEN}✅ $VOL_NAME: ${VOL_PERCENT}% (${VOL_AVAIL} free)${NC}"
                    fi
                fi
            ) &
        fi
    done
    wait
}

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: NETWORK TURBO
# ═══════════════════════════════════════════════════════════════════════════════
network_turbo() {
    echo -e "\n${WHITE}▓▓▓ NETWORK TURBO ▓▓▓${NC}"
    
    # DNS Flush
    info "Flushing DNS cache..."
    sudo dscacheutil -flushcache 2>/dev/null || true
    sudo killall -HUP mDNSResponder 2>/dev/null || true
    success "DNS cache flushed"
    
    # MTU Check
    MTU=$(networksetup -getMTU Ethernet 2>/dev/null | awk '{print $NF}' || echo "1500")
    if [ "$MTU" = "9000" ]; then
        success "Jumbo Frames: ACTIVE (MTU 9000)"
    else
        warn "Jumbo Frames: INACTIVE (MTU $MTU) - Run 'jumbo' to enable"
    fi
    
    # Gateway ping
    GATEWAY="10.0.0.1"
    if ping -c 1 -W 1 "$GATEWAY" > /dev/null 2>&1; then
        LATENCY=$(ping -c 1 "$GATEWAY" 2>/dev/null | grep "time=" | awk -F'time=' '{print $2}' | awk '{print $1}')
        success "Gateway: ${LATENCY}"
    else
        warn "Gateway: UNREACHABLE"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: CODE MAGIC
# ═══════════════════════════════════════════════════════════════════════════════
code_magic() {
    echo -e "\n${WHITE}▓▓▓ CODE MAGIC ▓▓▓${NC}"
    
    # Python validation
    info "Validating Python files..."
    PY_ERRORS=0
    PY_TOTAL=0
    while IFS= read -r pyfile; do
        ((PY_TOTAL++))
        if ! python3 -m py_compile "$pyfile" 2>/dev/null; then
            ((PY_ERRORS++))
            warn "Python syntax error: $(basename "$pyfile")"
        fi
    done < <(find "$NOIZYLAB_HOME" -name "*.py" -type f 2>/dev/null | head -100)
    
    if [ "$PY_ERRORS" -eq 0 ]; then
        success "Python: $PY_TOTAL files validated"
    else
        warn "Python: $PY_ERRORS/$PY_TOTAL files with errors"
    fi
    
    # Shell validation
    info "Validating Shell scripts..."
    SH_ERRORS=0
    SH_TOTAL=0
    while IFS= read -r shfile; do
        ((SH_TOTAL++))
        if ! bash -n "$shfile" 2>/dev/null; then
            ((SH_ERRORS++))
            warn "Shell syntax error: $(basename "$shfile")"
        fi
    done < <(find "$NOIZYLAB_HOME" -name "*.sh" -type f 2>/dev/null | head -100)
    
    if [ "$SH_ERRORS" -eq 0 ]; then
        success "Shell: $SH_TOTAL scripts validated"
    else
        warn "Shell: $SH_ERRORS/$SH_TOTAL scripts with errors"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: GIT TURBO
# ═══════════════════════════════════════════════════════════════════════════════
git_turbo() {
    echo -e "\n${WHITE}▓▓▓ GIT TURBO ▓▓▓${NC}"
    
    if [ -d "$NOIZYLAB_HOME/.git" ]; then
        cd "$NOIZYLAB_HOME"
        
        info "Optimizing git repository..."
        git gc --auto --quiet 2>/dev/null || true
        git prune 2>/dev/null || true
        
        # Check status
        CHANGES=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        if [ "$CHANGES" -gt 0 ]; then
            info "Uncommitted changes: $CHANGES files"
        else
            success "Git: Clean working tree"
        fi
        
        # Check remote
        if git remote -v 2>/dev/null | grep -q "origin"; then
            success "Git: Remote configured"
        else
            warn "Git: No remote configured"
        fi
    else
        warn "Git: Not a repository"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
main() {
    mkdir -p "$LOG_DIR"
    
    banner
    
    START_TIME=$(date +%s)
    
    ai_diagnostics
    autofix_engine
    storage_health
    network_turbo
    code_magic
    git_turbo
    
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    echo -e "\n${MAGENTA}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                    REPAIR COMPLETE                                ║"
    echo "╠═══════════════════════════════════════════════════════════════════╣"
    printf "║  Issues Found: %-5s    Issues Fixed: %-5s    Time: %ds       ║\n" "$ISSUES_FOUND" "$ISSUES_FIXED" "$DURATION"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "Complete. Log: $LOG_FILE"
}

# --- Mode Selection ---
case "${1:-full}" in
    "diag"|"diagnostics") ai_diagnostics ;;
    "fix"|"autofix") autofix_engine ;;
    "storage") storage_health ;;
    "network") network_turbo ;;
    "code"|"magic") code_magic ;;
    "git") git_turbo ;;
    "full"|*) main ;;
esac

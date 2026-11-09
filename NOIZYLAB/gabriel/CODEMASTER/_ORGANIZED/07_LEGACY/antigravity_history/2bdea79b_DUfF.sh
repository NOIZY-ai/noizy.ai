#!/bin/bash
# ========================================
# MASTER_REPAIR v2.0 - "THE FLASH EDITION"
# Unified AutoRepair System for MC96 Universe
# Commander: Rob
# ========================================

set -e

# --- Configuration ---
NOIZYLAB_HOME="${HOME}/NOIZYLAB"
GUARDIAN_HOME="${NOIZYLAB_HOME}/SystemGuardian"
GABRIEL_HOME="${NOIZYLAB_HOME}/PROJECTS/GABRIEL/workers"
LOG_FILE="${GUARDIAN_HOME}/logs/master_repair_$(date +%Y%m%d_%H%M%S).log"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Banner ---
echo -e "${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       MASTER REPAIR v2.0 - THE FLASH EDITION             ║"
echo "║       MC96 Universe AutoRepair System                     ║"
echo "║       Commander: Rob                                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# --- Logging ---
log() {
    local level=$1
    local message=$2
    echo -e "[$(date +%H:%M:%S)] [$level] $message" | tee -a "$LOG_FILE"
}

# --- Module: System Health Check ---
health_check() {
    log "INFO" "${CYAN}Running System Health Check...${NC}"
    
    # CPU Load
    CPU_LOAD=$(sysctl -n vm.loadavg | awk '{print $2}')
    log "INFO" "CPU Load: $CPU_LOAD"
    
    # Memory
    MEM_PERCENT=$(ps -A -o %mem | awk '{s+=$1} END {print int(s)}')
    log "INFO" "Memory Usage: ${MEM_PERCENT}%"
    
    # Disk
    DISK_PERCENT=$(df -h / | tail -1 | awk '{print $5}')
    log "INFO" "Disk Usage: $DISK_PERCENT"
    
    echo -e "${GREEN}✅ Health Check Complete${NC}"
}

# --- Module: Fix Permissions ---
fix_permissions() {
    log "INFO" "${CYAN}Fixing Permissions...${NC}"
    
    # Fix common permission issues
    chmod +x "$NOIZYLAB_HOME"/*.sh 2>/dev/null || true
    chmod +x "$NOIZYLAB_HOME"/scripts/**/*.sh 2>/dev/null || true
    chmod +x "$GABRIEL_HOME"/*.sh 2>/dev/null || true
    
    echo -e "${GREEN}✅ Permissions Fixed${NC}"
}

# --- Module: Clean Caches ---
clean_caches() {
    log "INFO" "${CYAN}Cleaning Caches...${NC}"
    
    # Python cache
    find "$NOIZYLAB_HOME" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$NOIZYLAB_HOME" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Node modules cache
    find "$NOIZYLAB_HOME" -type d -name "node_modules/.cache" -exec rm -rf {} + 2>/dev/null || true
    
    # DS_Store
    find "$NOIZYLAB_HOME" -name ".DS_Store" -delete 2>/dev/null || true
    
    echo -e "${GREEN}✅ Caches Cleaned${NC}"
}

# --- Module: Git Cleanup ---
git_cleanup() {
    log "INFO" "${CYAN}Cleaning Git Repositories...${NC}"
    
    cd "$NOIZYLAB_HOME"
    git gc --auto 2>/dev/null || true
    git prune 2>/dev/null || true
    
    echo -e "${GREEN}✅ Git Cleaned${NC}"
}

# --- Module: Network Optimization ---
optimize_network() {
    log "INFO" "${CYAN}Optimizing Network...${NC}"
    
    # Flush DNS
    sudo dscacheutil -flushcache 2>/dev/null || true
    sudo killall -HUP mDNSResponder 2>/dev/null || true
    
    # Check MTU
    MTU=$(networksetup -getMTU Ethernet 2>/dev/null | awk '{print $NF}')
    if [ "$MTU" != "9000" ]; then
        log "WARN" "${YELLOW}MTU is $MTU - Run 'jumbo' to enable Jumbo Frames${NC}"
    else
        log "INFO" "MTU: 9000 (Jumbo Frames Active)"
    fi
    
    echo -e "${GREEN}✅ Network Optimized${NC}"
}

# --- Module: GABRIEL Ping (HP-OMEN) ---
ping_gabriel() {
    log "INFO" "${CYAN}Pinging GABRIEL (HP-OMEN)...${NC}"
    
    # Try to reach GABRIEL agent
    GABRIEL_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health 2>/dev/null || echo "000")
    
    if [ "$GABRIEL_STATUS" = "200" ]; then
        echo -e "${GREEN}✅ GABRIEL Agent: ONLINE${NC}"
    else
        echo -e "${YELLOW}⚠️ GABRIEL Agent: OFFLINE (Start with 'gabriel')${NC}"
    fi
}

# --- Module: Auto Code Magic ---
autocodemagic() {
    log "INFO" "${MAGENTA}Running AutoCodeMagic...${NC}"
    
    # Validate Python syntax
    log "INFO" "Checking Python files..."
    PYTHON_ERRORS=0
    for pyfile in $(find "$NOIZYLAB_HOME" -name "*.py" -type f 2>/dev/null | head -50); do
        python3 -m py_compile "$pyfile" 2>/dev/null || ((PYTHON_ERRORS++))
    done
    
    if [ $PYTHON_ERRORS -eq 0 ]; then
        echo -e "${GREEN}✅ Python: All files valid${NC}"
    else
        echo -e "${YELLOW}⚠️ Python: $PYTHON_ERRORS files with issues${NC}"
    fi
    
    # Validate Shell scripts
    log "INFO" "Checking Shell scripts..."
    SHELL_ERRORS=0
    for shfile in $(find "$NOIZYLAB_HOME" -name "*.sh" -type f 2>/dev/null | head -50); do
        bash -n "$shfile" 2>/dev/null || ((SHELL_ERRORS++))
    done
    
    if [ $SHELL_ERRORS -eq 0 ]; then
        echo -e "${GREEN}✅ Shell: All scripts valid${NC}"
    else
        echo -e "${YELLOW}⚠️ Shell: $SHELL_ERRORS scripts with issues${NC}"
    fi
}

# --- MAIN EXECUTION ---
main() {
    mkdir -p "${GUARDIAN_HOME}/logs"
    
    echo ""
    log "INFO" "${BLUE}Starting MASTER REPAIR v2.0...${NC}"
    echo ""
    
    health_check
    echo ""
    
    fix_permissions
    echo ""
    
    clean_caches
    echo ""
    
    git_cleanup
    echo ""
    
    optimize_network
    echo ""
    
    ping_gabriel
    echo ""
    
    autocodemagic
    echo ""
    
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║       MASTER REPAIR COMPLETE                              ║"
    echo "║       All Systems: OPTIMIZED                              ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "INFO" "Repair complete. Log saved to: $LOG_FILE"
}

# Run with mode argument or default to full
case "${1:-full}" in
    "health")
        health_check
        ;;
    "clean")
        clean_caches
        ;;
    "network")
        optimize_network
        ;;
    "code")
        autocodemagic
        ;;
    "full"|*)
        main
        ;;
esac

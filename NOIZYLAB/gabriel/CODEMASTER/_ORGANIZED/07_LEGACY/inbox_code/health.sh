#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  MAIL MANAGER PRO — HEALTH CHECK & MONITORING
#  System diagnostics and health monitoring
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIL_MANAGER_HOME="${MAIL_MANAGER_HOME:-$SCRIPT_DIR}"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; BLUE='\033[0;34m'; MAGENTA='\033[0;35m'; RESET='\033[0m'
BOLD='\033[1m'

print_header() {
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}$1${RESET}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${RESET}"
}

check_status() {
    local name="$1"
    local status="$2"
    
    if [[ "$status" == "ok" ]] || [[ "$status" == "healthy" ]] || [[ "$status" == "true" ]]; then
        printf "${GREEN}✓${RESET} %-40s %s\n" "$name" "OK"
    elif [[ "$status" == "warning" ]]; then
        printf "${YELLOW}⚠${RESET} %-40s %s\n" "$name" "Warning"
    else
        printf "${RED}✗${RESET} %-40s %s\n" "$name" "FAILED"
    fi
}

# Main health check
cmd_health_check() {
    print_header "MAIL MANAGER PRO — HEALTH CHECK"
    
    # Installation
    print_header "Installation & Files"
    [[ -f "${MAIL_MANAGER_HOME}/bin/mailmgr" ]] && check_status "Main executable" "ok" || check_status "Main executable" "error"
    [[ -f "${MAIL_MANAGER_HOME}/lib/backup.sh" ]] && check_status "Backup library" "ok" || check_status "Backup library" "error"
    [[ -f "${MAIL_MANAGER_HOME}/config/config.yaml" ]] && check_status "Configuration" "ok" || check_status "Configuration" "error"
    [[ -d "${MAIL_MANAGER_HOME}/backups" ]] && check_status "Backups directory" "ok" || check_status "Backups directory" "error"
    [[ -d "${MAIL_MANAGER_HOME}/logs" ]] && check_status "Logs directory" "ok" || check_status "Logs directory" "error"
    
    # Dependencies
    print_header "System Dependencies"
    command -v bash &>/dev/null && check_status "Bash" "ok" || check_status "Bash" "error"
    command -v tput &>/dev/null && check_status "tput (TUI support)" "ok" || check_status "tput (TUI support)" "warning"
    command -v tar &>/dev/null && check_status "tar (backups)" "ok" || check_status "tar (backups)" "error"
    command -v curl &>/dev/null && check_status "curl (API/OAuth)" "ok" || check_status "curl (API/OAuth)" "warning"
    command -v python3 &>/dev/null && check_status "Python 3 (API/ML)" "ok" || check_status "Python 3 (API/ML)" "warning"
    
    # macOS-specific
    if [[ "$OSTYPE" == darwin* ]]; then
        print_header "macOS Specific"
        command -v osascript &>/dev/null && check_status "osascript (Apple Mail)" "ok" || check_status "osascript (Apple Mail)" "warning"
        command -v launchctl &>/dev/null && check_status "launchctl (scheduler)" "ok" || check_status "launchctl (scheduler)" "warning"
        [[ -d "/Applications/Microsoft Outlook.app" ]] && check_status "Outlook installed" "ok" || check_status "Outlook installed" "warning"
    fi
    
    # Disk space
    print_header "Disk & Storage"
    local total_size=$(du -sh "${MAIL_MANAGER_HOME}" 2>/dev/null | cut -f1)
    local backup_size=$(du -sh "${MAIL_MANAGER_HOME}/backups" 2>/dev/null | cut -f1)
    local log_size=$(du -sh "${MAIL_MANAGER_HOME}/logs" 2>/dev/null | cut -f1)
    
    printf "%-42s %10s\n" "Installation size:" "$total_size"
    printf "%-42s %10s\n" "Backups size:" "$backup_size"
    printf "%-42s %10s\n" "Logs size:" "$log_size"
    
    # Backup status
    print_header "Backup Status"
    local backup_count=$(ls -1 "${MAIL_MANAGER_HOME}/backups"/backup_v*.tar.gz 2>/dev/null | wc -l | xargs)
    local latest_backup=$(ls -1t "${MAIL_MANAGER_HOME}/backups"/backup_v*.tar.gz 2>/dev/null | head -1)
    
    if [[ $backup_count -gt 0 ]]; then
        printf "%-42s %s\n" "Total backups:" "$backup_count"
        
        if [[ -n "$latest_backup" ]]; then
            local latest_date=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$latest_backup" 2>/dev/null || echo "unknown")
            printf "%-42s %s\n" "Latest backup:" "$latest_date"
            check_status "Recent backup (< 7 days)" "ok"
        fi
    else
        printf "%-42s %s\n" "Total backups:" "0"
        check_status "Recent backup (< 7 days)" "warning"
    fi
    
    # Scheduler status
    print_header "Scheduler Status"
    if [[ "$OSTYPE" == darwin* ]]; then
        local plist="${HOME}/Library/LaunchAgents/com.mailmanager.pro.plist"
        if [[ -f "$plist" ]]; then
            if launchctl list 2>/dev/null | grep -q "com.mailmanager.pro"; then
                check_status "launchd agent" "ok"
            else
                check_status "launchd agent" "warning"
            fi
        else
            check_status "launchd agent" "warning"
        fi
    fi
    
    # API status
    print_header "API Server"
    local api_pid_file="${MAIL_MANAGER_HOME}/data/api.pid"
    if [[ -f "$api_pid_file" ]]; then
        local pid=$(cat "$api_pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            check_status "API server (PID: $pid)" "ok"
        else
            check_status "API server" "warning"
        fi
    else
        check_status "API server" "warning"
    fi
    
    # Mail app status
    print_header "Mail Applications"
    if [[ "$OSTYPE" == darwin* ]]; then
        if osascript -e 'tell application "Mail" to get name of first account' &>/dev/null 2>&1; then
            check_status "Apple Mail" "ok"
        else
            check_status "Apple Mail" "warning"
        fi
    fi
    
    # Permissions
    print_header "Permissions"
    if [[ -x "${MAIL_MANAGER_HOME}/bin/mailmgr" ]]; then
        check_status "mailmgr executable" "ok"
    else
        check_status "mailmgr executable" "error"
    fi
    
    # Summary
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${RESET}"
    echo -e "${GREEN}✓ Health check complete${RESET}"
    echo ""
}

# Quiet health check (returns exit code only)
cmd_health_check_quiet() {
    local errors=0
    
    [[ ! -f "${MAIL_MANAGER_HOME}/bin/mailmgr" ]] && ((errors++))
    [[ ! -f "${MAIL_MANAGER_HOME}/lib/backup.sh" ]] && ((errors++))
    [[ ! -f "${MAIL_MANAGER_HOME}/config/config.yaml" ]] && ((errors++))
    command -v bash &>/dev/null || ((errors++))
    command -v tar &>/dev/null || ((errors++))
    
    return $errors
}

# Recommend fixes
cmd_health_fix() {
    echo "Recommended fixes:"
    
    if [[ ! -f "${MAIL_MANAGER_HOME}/bin/mailmgr" ]]; then
        echo ""
        echo "  Missing: Main executable"
        echo "  Fix: Run installation again or check file permissions"
    fi
    
    if ! command -v python3 &>/dev/null; then
        echo ""
        echo "  Missing: Python 3 (optional, needed for API)"
        echo "  Fix: brew install python3"
    fi
    
    if ! command -v tput &>/dev/null; then
        echo ""
        echo "  Missing: tput (optional, needed for TUI)"
        echo "  Fix: Usually pre-installed on macOS/Linux"
    fi
    
    if [[ ! -x "${MAIL_MANAGER_HOME}/bin/mailmgr" ]]; then
        echo ""
        echo "  Not executable: mailmgr script"
        echo "  Fix: chmod +x ${MAIL_MANAGER_HOME}/bin/mailmgr"
    fi
    
    local backup_count=$(ls -1 "${MAIL_MANAGER_HOME}/backups"/backup_v*.tar.gz 2>/dev/null | wc -l | xargs)
    if [[ $backup_count -eq 0 ]]; then
        echo ""
        echo "  Warning: No backups found"
        echo "  Fix: Run 'mailmgr backup create' to create first backup"
    fi
}

# Main dispatch
case "${1:-check}" in
    check)
        cmd_health_check
        ;;
    quiet)
        cmd_health_check_quiet
        ;;
    fix)
        cmd_health_fix
        ;;
    *)
        cmd_health_check
        ;;
esac

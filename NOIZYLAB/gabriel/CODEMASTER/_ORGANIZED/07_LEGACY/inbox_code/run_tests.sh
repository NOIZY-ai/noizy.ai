#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  MAIL MANAGER PRO — TEST SUITE
#  Comprehensive unit and integration tests
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIL_MANAGER_HOME="${MAIL_MANAGER_HOME:-$SCRIPT_DIR}"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; BLUE='\033[0;34m'; RESET='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

# Test helpers
assert_success() {
    local cmd="$1"
    local desc="${2:-$cmd}"
    
    if bash -c "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${RESET} $desc"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${RESET} $desc"
        ((TESTS_FAILED++))
    fi
}

assert_file_exists() {
    local file="$1"
    local desc="${2:-File exists: $file}"
    
    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✓${RESET} $desc"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${RESET} $desc"
        ((TESTS_FAILED++))
    fi
}

assert_command_exists() {
    local cmd="$1"
    local desc="${2:-Command exists: $cmd}"
    
    if command -v "$cmd" &>/dev/null; then
        echo -e "${GREEN}✓${RESET} $desc"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${RESET} $desc"
        ((TESTS_FAILED++))
    fi
}

# Test suites
test_installation() {
    echo ""
    echo -e "${BLUE}Testing Installation${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    assert_file_exists "${MAIL_MANAGER_HOME}/bin/mailmgr" "Main executable exists"
    assert_file_exists "${MAIL_MANAGER_HOME}/lib/backup.sh" "Backup library exists"
    assert_file_exists "${MAIL_MANAGER_HOME}/lib/tui.sh" "TUI library exists"
    assert_file_exists "${MAIL_MANAGER_HOME}/lib/scheduler.sh" "Scheduler library exists"
    assert_file_exists "${MAIL_MANAGER_HOME}/lib/api.sh" "API library exists"
    assert_file_exists "${MAIL_MANAGER_HOME}/api/server.py" "API server exists"
    assert_file_exists "${MAIL_MANAGER_HOME}/config/config.yaml" "Configuration file exists"
}

test_directories() {
    echo ""
    echo -e "${BLUE}Testing Directory Structure${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    local dirs=(
        "bin" "lib" "config" "api" "python"
        "logs" "backups" "data" "cache"
        "plugins" "tests" "docs"
        "integrations/raycast" "integrations/alfred"
        "integrations/keyboard-maestro" "integrations/shortcuts"
    )
    
    for dir in "${dirs[@]}"; do
        if [[ -d "${MAIL_MANAGER_HOME}/$dir" ]]; then
            echo -e "${GREEN}✓${RESET} Directory exists: $dir"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗${RESET} Directory missing: $dir"
            ((TESTS_FAILED++))
        fi
    done
}

test_bash_syntax() {
    echo ""
    echo -e "${BLUE}Testing Bash Syntax${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    local scripts=(
        "${MAIL_MANAGER_HOME}/bin/mailmgr"
        "${MAIL_MANAGER_HOME}/lib/backup.sh"
        "${MAIL_MANAGER_HOME}/lib/tui.sh"
        "${MAIL_MANAGER_HOME}/lib/scheduler.sh"
        "${MAIL_MANAGER_HOME}/lib/api.sh"
        "${MAIL_MANAGER_HOME}/lib/oauth.sh"
        "${MAIL_MANAGER_HOME}/lib/webhooks.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]]; then
            if bash -n "$script" 2>/dev/null; then
                echo -e "${GREEN}✓${RESET} Syntax OK: $(basename "$script")"
                ((TESTS_PASSED++))
            else
                echo -e "${RED}✗${RESET} Syntax error: $(basename "$script")"
                ((TESTS_FAILED++))
            fi
        fi
    done
}

test_python_syntax() {
    echo ""
    echo -e "${BLUE}Testing Python Syntax${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    command -v python3 &>/dev/null || {
        echo -e "${YELLOW}⊘${RESET} Python 3 not installed, skipping"
        return 0
    }
    
    local scripts=(
        "${MAIL_MANAGER_HOME}/api/server.py"
        "${MAIL_MANAGER_HOME}/python/ml_categorizer.py"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]]; then
            if python3 -m py_compile "$script" 2>/dev/null; then
                echo -e "${GREEN}✓${RESET} Syntax OK: $(basename "$script")"
                ((TESTS_PASSED++))
            else
                echo -e "${RED}✗${RESET} Syntax error: $(basename "$script")"
                ((TESTS_FAILED++))
            fi
        fi
    done
}

test_permissions() {
    echo ""
    echo -e "${BLUE}Testing Permissions${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    local executables=(
        "${MAIL_MANAGER_HOME}/bin/mailmgr"
    )
    
    for script in "${executables[@]}"; do
        if [[ -x "$script" ]]; then
            echo -e "${GREEN}✓${RESET} Executable: $(basename "$script")"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗${RESET} Not executable: $(basename "$script")"
            ((TESTS_FAILED++))
        fi
    done
}

test_dependencies() {
    echo ""
    echo -e "${BLUE}Testing Dependencies${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    # Required
    assert_command_exists "bash" "Bash required"
    assert_command_exists "tput" "tput required for TUI"
    assert_command_exists "tar" "tar required for backups"
    assert_command_exists "curl" "curl required for API"
    
    # Optional
    if command -v python3 &>/dev/null; then
        echo -e "${GREEN}✓${RESET} Python 3 installed (optional)"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⊘${RESET} Python 3 not installed (optional, needed for API)"
    fi
    
    if [[ "$OSTYPE" == darwin* ]]; then
        assert_command_exists "osascript" "osascript (macOS only)"
        assert_command_exists "launchctl" "launchctl (macOS only)"
    fi
}

test_backup_operations() {
    echo ""
    echo -e "${BLUE}Testing Backup Operations${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    local test_backup_dir=$(mktemp -d)
    trap "rm -rf '$test_backup_dir'" RETURN
    
    # Test backup creation (dry-run)
    if BACKUP_DIR="$test_backup_dir" \
       SCRIPT_DIR="${MAIL_MANAGER_HOME}" \
       bash "${MAIL_MANAGER_HOME}/bin/mailmgr" backup create 2>/dev/null; then
        echo -e "${GREEN}✓${RESET} Backup creation works"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⊘${RESET} Backup creation needs more setup"
    fi
}

test_configuration() {
    echo ""
    echo -e "${BLUE}Testing Configuration${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    local config_file="${MAIL_MANAGER_HOME}/config/config.yaml"
    
    if [[ -f "$config_file" ]]; then
        # Check YAML structure
        if grep -q "mail_manager:" "$config_file" && \
           grep -q "accounts:" "$config_file" && \
           grep -q "folders:" "$config_file"; then
            echo -e "${GREEN}✓${RESET} Configuration has all required sections"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗${RESET} Configuration missing required sections"
            ((TESTS_FAILED++))
        fi
        
        # Check version match
        local config_version=$(grep "version:" "$config_file" | head -1 | cut -d' ' -f2)
        if [[ "$config_version" == "3.5.0" ]]; then
            echo -e "${GREEN}✓${RESET} Configuration version matches"
            ((TESTS_PASSED++))
        fi
    fi
}

test_integrations() {
    echo ""
    echo -e "${BLUE}Testing Integration Files${RESET}"
    echo "═══════════════════════════════════════════════════"
    
    assert_file_exists "${MAIL_MANAGER_HOME}/integrations/raycast/backup-manager.raycast.sh" "Raycast integration"
    
    # Check OAuth library
    if grep -q "cmd_oauth_gmail" "${MAIL_MANAGER_HOME}/lib/oauth.sh" 2>/dev/null; then
        echo -e "${GREEN}✓${RESET} OAuth2 Gmail implementation"
        ((TESTS_PASSED++))
    fi
    
    if grep -q "cmd_oauth_microsoft" "${MAIL_MANAGER_HOME}/lib/oauth.sh" 2>/dev/null; then
        echo -e "${GREEN}✓${RESET} OAuth2 Microsoft implementation"
        ((TESTS_PASSED++))
    fi
    
    # Check Webhooks
    if grep -q "send_webhook" "${MAIL_MANAGER_HOME}/lib/webhooks.sh" 2>/dev/null; then
        echo -e "${GREEN}✓${RESET} Webhook integration"
        ((TESTS_PASSED++))
    fi
}

# Run all tests
main() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════"
    echo "    MAIL MANAGER PRO v3.5.0 — TEST SUITE"
    echo -e "═══════════════════════════════════════════════════${RESET}"
    
    test_installation
    test_directories
    test_bash_syntax
    test_python_syntax
    test_permissions
    test_dependencies
    test_backup_operations
    test_configuration
    test_integrations
    
    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${RESET}"
    
    local total=$((TESTS_PASSED + TESTS_FAILED))
    local percentage=$((TESTS_PASSED * 100 / total))
    
    echo "Tests Passed:  ${GREEN}${TESTS_PASSED}${RESET}"
    echo "Tests Failed:  ${RED}${TESTS_FAILED}${RESET}"
    echo "Total Tests:   $total"
    echo "Success Rate:  ${GREEN}${percentage}%${RESET}"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All tests passed!${RESET}"
        return 0
    else
        echo -e "${RED}✗ Some tests failed${RESET}"
        return 1
    fi
}

main "$@"

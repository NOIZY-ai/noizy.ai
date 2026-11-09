#!/bin/bash
#
# 🚀 GABRIEL BOOTSTRAP SCRIPT
# ===========================
# Sets up GABRIEL with pinned dependencies and consistent environment.
#
# Usage:
#   ./bootstrap.sh           # Full setup
#   ./bootstrap.sh check     # Check environment only
#   ./bootstrap.sh update    # Update dependencies
#

set -e  # Exit on error

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT="${HOME}/NOIZYLAB/GABRIEL"
PYTHON_VERSION="3.11"
NODE_VERSION="20"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# HELPERS
# =============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# =============================================================================
# ENVIRONMENT CHECKS
# =============================================================================

check_environment() {
    echo ""
    echo "🔍 Checking Environment..."
    echo "=========================="
    
    local issues=0
    
    # macOS version
    if [[ "$(uname)" == "Darwin" ]]; then
        local mac_version=$(sw_vers -productVersion)
        log_success "macOS $mac_version"
    else
        log_warn "Not macOS - some features may not work"
    fi
    
    # Python
    if check_command python3; then
        local py_version=$(python3 --version | cut -d' ' -f2)
        local py_major=$(echo $py_version | cut -d'.' -f1)
        local py_minor=$(echo $py_version | cut -d'.' -f2)
        
        if [[ "$py_major" -eq 3 && "$py_minor" -ge 10 ]]; then
            log_success "Python $py_version"
        else
            log_warn "Python $py_version (recommend 3.10+)"
            ((issues++))
        fi
    else
        log_error "Python 3 not found"
        ((issues++))
    fi
    
    # Node.js
    if check_command node; then
        local node_version=$(node --version | tr -d 'v')
        local node_major=$(echo $node_version | cut -d'.' -f1)
        
        if [[ "$node_major" -ge 18 ]]; then
            log_success "Node.js $node_version"
        else
            log_warn "Node.js $node_version (recommend 18+)"
            ((issues++))
        fi
    else
        log_error "Node.js not found"
        ((issues++))
    fi
    
    # Homebrew
    if check_command brew; then
        log_success "Homebrew installed"
    else
        log_error "Homebrew not found"
        ((issues++))
    fi
    
    # Git
    if check_command git; then
        local git_version=$(git --version | cut -d' ' -f3)
        log_success "Git $git_version"
    else
        log_error "Git not found"
        ((issues++))
    fi
    
    # FFmpeg (for audio)
    if check_command ffmpeg; then
        log_success "FFmpeg installed"
    else
        log_warn "FFmpeg not found (needed for audio)"
    fi
    
    # GABRIEL directories
    if [[ -d "$GABRIEL_ROOT" ]]; then
        log_success "GABRIEL root: $GABRIEL_ROOT"
    else
        log_error "GABRIEL root not found: $GABRIEL_ROOT"
        ((issues++))
    fi
    
    echo ""
    if [[ $issues -eq 0 ]]; then
        log_success "Environment OK!"
        return 0
    else
        log_warn "$issues issues found"
        return 1
    fi
}

# =============================================================================
# DEPENDENCY INSTALLATION
# =============================================================================

install_python_deps() {
    log_info "Installing Python dependencies..."
    
    # Create virtual environment if not exists
    local venv_path="$GABRIEL_ROOT/.venv"
    
    if [[ ! -d "$venv_path" ]]; then
        python3 -m venv "$venv_path"
        log_success "Created virtual environment"
    fi
    
    # Activate venv
    source "$venv_path/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip wheel setuptools
    
    # Install from requirements
    if [[ -f "$GABRIEL_ROOT/requirements.txt" ]]; then
        pip install -r "$GABRIEL_ROOT/requirements.txt"
        log_success "Installed Python requirements"
    else
        # Install essential packages
        pip install \
            anthropic \
            openai \
            google-generativeai \
            groq \
            httpx \
            aiohttp \
            pydantic \
            python-dotenv \
            watchdog \
            rich \
            click \
            mcp
        
        # Save requirements
        pip freeze > "$GABRIEL_ROOT/requirements.txt"
        log_success "Installed and saved Python requirements"
    fi
}

install_node_deps() {
    log_info "Installing Node.js dependencies..."
    
    if [[ -f "$GABRIEL_ROOT/package.json" ]]; then
        cd "$GABRIEL_ROOT"
        npm install
        log_success "Installed Node.js packages"
    else
        log_warn "No package.json found, skipping Node deps"
    fi
}

install_system_deps() {
    log_info "Installing system dependencies..."
    
    if check_command brew; then
        # Install/update essentials
        brew install ffmpeg jq gh 2>/dev/null || true
        
        # Optional: Local LLM support
        if ! check_command ollama; then
            log_info "Installing Ollama for local LLM support..."
            brew install ollama 2>/dev/null || true
        fi
        
        log_success "System dependencies installed"
    else
        log_warn "Homebrew not available, skipping system deps"
    fi
}

# =============================================================================
# DIRECTORY SETUP
# =============================================================================

setup_directories() {
    log_info "Setting up GABRIEL directories..."
    
    local dirs=(
        "$GABRIEL_ROOT/core"
        "$GABRIEL_ROOT/tools"
        "$GABRIEL_ROOT/runs"
        "$GABRIEL_ROOT/logs"
        "$GABRIEL_ROOT/logs/events"
        "$GABRIEL_ROOT/costs"
        "$GABRIEL_ROOT/verification"
        "$GABRIEL_ROOT/memcell_data"
        "$GABRIEL_ROOT/00_Inbox"
        "$GABRIEL_ROOT/00_Inbox/PROCESSED"
        "$GABRIEL_ROOT/00_Inbox/FAILED"
        "$GABRIEL_ROOT/artifacts"
        "$GABRIEL_ROOT/secrets"
        "$GABRIEL_ROOT/tests"
        "$GABRIEL_ROOT/tests/gold"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
    done
    
    log_success "Directories created"
}

# =============================================================================
# VERSION LOCKING
# =============================================================================

lock_versions() {
    log_info "Locking dependency versions..."
    
    # Python
    if [[ -d "$GABRIEL_ROOT/.venv" ]]; then
        source "$GABRIEL_ROOT/.venv/bin/activate"
        pip freeze > "$GABRIEL_ROOT/requirements.lock"
        log_success "Python versions locked: requirements.lock"
    fi
    
    # Node
    if [[ -f "$GABRIEL_ROOT/package.json" ]]; then
        cd "$GABRIEL_ROOT"
        npm shrinkwrap 2>/dev/null || npm ci --package-lock-only
        log_success "Node versions locked: package-lock.json"
    fi
    
    # Record system info
    cat > "$GABRIEL_ROOT/.environment" << EOF
# GABRIEL Environment Lock
# Generated: $(date -Iseconds)

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
NODE_VERSION=$(node --version 2>&1 | tr -d 'v')
NPM_VERSION=$(npm --version 2>&1)
MACOS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "N/A")
ARCH=$(uname -m)
HOSTNAME=$(hostname)
EOF
    
    log_success "Environment info saved: .environment"
}

# =============================================================================
# SHELL SETUP
# =============================================================================

setup_shell() {
    log_info "Setting up shell integration..."
    
    local shell_config=""
    
    if [[ -f "$HOME/.zshrc" ]]; then
        shell_config="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        shell_config="$HOME/.bashrc"
    fi
    
    if [[ -n "$shell_config" ]]; then
        # Check if already configured
        if ! grep -q "GABRIEL_ROOT" "$shell_config"; then
            cat >> "$shell_config" << 'EOF'

# GABRIEL AI System
export GABRIEL_ROOT="$HOME/NOIZYLAB/GABRIEL"
export PATH="$GABRIEL_ROOT/bin:$PATH"

# Gabriel aliases
alias gab='python3 $GABRIEL_ROOT/core/gabriel.py'
alias gwatch='python3 $GABRIEL_ROOT/core/automation.py watch'
alias gstatus='python3 $GABRIEL_ROOT/core/cost_controller.py status'
alias glogs='tail -f $GABRIEL_ROOT/logs/*.log'

# Activate GABRIEL venv
gabriel_activate() {
    source "$GABRIEL_ROOT/.venv/bin/activate"
}
EOF
            log_success "Added GABRIEL to $shell_config"
            log_info "Run 'source $shell_config' to activate"
        else
            log_success "Shell already configured"
        fi
    else
        log_warn "No shell config found"
    fi
}

# =============================================================================
# VALIDATION
# =============================================================================

validate_installation() {
    log_info "Validating installation..."
    
    local errors=0
    
    # Check core modules
    source "$GABRIEL_ROOT/.venv/bin/activate" 2>/dev/null || true
    
    local modules=(
        "core/security.py"
        "core/run_manager.py"
        "core/cost_controller.py"
        "core/observability.py"
        "core/verifier.py"
        "core/automation.py"
    )
    
    for mod in "${modules[@]}"; do
        if [[ -f "$GABRIEL_ROOT/$mod" ]]; then
            python3 -c "import sys; sys.path.insert(0, '$GABRIEL_ROOT'); exec(open('$GABRIEL_ROOT/$mod').read())" 2>/dev/null && \
                log_success "$mod" || \
                { log_error "$mod has syntax errors"; ((errors++)); }
        else
            log_error "$mod not found"
            ((errors++))
        fi
    done
    
    echo ""
    if [[ $errors -eq 0 ]]; then
        log_success "All modules validated!"
        return 0
    else
        log_error "$errors modules have issues"
        return 1
    fi
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    echo ""
    echo "🚀 GABRIEL Bootstrap"
    echo "===================="
    echo ""
    
    local cmd="${1:-full}"
    
    case "$cmd" in
        check)
            check_environment
            ;;
        update)
            install_python_deps
            install_node_deps
            lock_versions
            ;;
        validate)
            validate_installation
            ;;
        full|*)
            check_environment
            setup_directories
            install_system_deps
            install_python_deps
            install_node_deps
            lock_versions
            setup_shell
            validate_installation
            
            echo ""
            echo "=================================="
            log_success "GABRIEL Bootstrap Complete!"
            echo "=================================="
            echo ""
            echo "Next steps:"
            echo "  1. source ~/.zshrc           # Reload shell"
            echo "  2. gabriel_activate          # Activate venv"
            echo "  3. python3 core/security.py setup  # Configure API keys"
            echo "  4. gwatch                    # Start file watcher"
            echo ""
            ;;
    esac
}

main "$@"

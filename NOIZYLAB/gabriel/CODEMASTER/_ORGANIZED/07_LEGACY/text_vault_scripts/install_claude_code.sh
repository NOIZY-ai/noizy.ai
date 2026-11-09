#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════╗
# ║     CLAUDE CODE - COMPLETE SETUP FOR GOD                          ║
# ║                 GORUNFREE EDITION                                 ║
# ╚═══════════════════════════════════════════════════════════════════╝
#
# ONE COMMAND: bash install_claude_code.sh
#
# This installs Claude Code and makes it your PRIMARY coding tool

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║           INSTALLING CLAUDE CODE ON GOD                           ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════
# 1. INSTALL CLAUDE CODE
# ═══════════════════════════════════════════════════════════════════

echo "📦 Installing Claude Code..."

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "⚠️  npm not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install node
fi

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

echo "✅ Claude Code installed"

# ═══════════════════════════════════════════════════════════════════
# 2. CONFIGURE API KEY FROM VAULT
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "🔑 Configuring API key..."

# Create config directory
mkdir -p ~/.config/claude-code

# Check if vault has anthropic key
if command -v python3 &> /dev/null && [ -f ~/api_token_vault.py ]; then
    ANTHROPIC_KEY=$(python3 ~/api_token_vault.py get anthropic --full 2>/dev/null || echo "")
    if [ -n "$ANTHROPIC_KEY" ] && [ "$ANTHROPIC_KEY" != "None" ]; then
        export ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
        echo "✅ API key loaded from vault"
    fi
fi

# If no key yet, prompt
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  No Anthropic API key found in vault"
    echo "   Add it with: vault add anthropic YOUR-KEY"
    echo "   Or set: export ANTHROPIC_API_KEY='your-key'"
fi

# ═══════════════════════════════════════════════════════════════════
# 3. CREATE SHELL INTEGRATION
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "🔧 Creating shell integration..."

cat > ~/claude_code_shortcuts.sh << 'CCSHORTCUTS'
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════╗
# ║     CLAUDE CODE SHORTCUTS - GORUNFREE EDITION                     ║
# ╚═══════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════════
# AUTO-LOAD API KEY FROM VAULT
# ═══════════════════════════════════════════════════════════════════

_load_anthropic_key() {
    if [ -z "$ANTHROPIC_API_KEY" ] && [ -f ~/api_token_vault.py ]; then
        local key=$(python3 ~/api_token_vault.py get anthropic --full 2>/dev/null)
        if [ -n "$key" ] && [ "$key" != "None" ]; then
            export ANTHROPIC_API_KEY="$key"
        fi
    fi
}

# Load key on shell start
_load_anthropic_key

# ═══════════════════════════════════════════════════════════════════
# CORE ALIASES - Voice Friendly
# ═══════════════════════════════════════════════════════════════════

# Main command
alias cc="claude"
alias claude-code="claude"

# Quick actions
alias ccc="claude --continue"          # Continue last conversation
alias ccr="claude --resume"            # Resume with context
alias cch="claude --help"              # Help

# ═══════════════════════════════════════════════════════════════════
# POWER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

# Start Claude Code in current directory
code-here() {
    _load_anthropic_key
    cd "${1:-.}" && claude
}

# Start Claude Code in specific project
code-project() {
    _load_anthropic_key
    local project="$1"
    if [ -d "$project" ]; then
        cd "$project" && claude
    elif [ -d ~/Projects/"$project" ]; then
        cd ~/Projects/"$project" && claude
    elif [ -d ~/code/"$project" ]; then
        cd ~/code/"$project" && claude
    else
        echo "❌ Project not found: $project"
        echo "   Checking: ./$project, ~/Projects/$project, ~/code/$project"
    fi
}

# Quick fix - open Claude Code with a task
fix() {
    _load_anthropic_key
    claude "Fix this: $*"
}

# Build something
build() {
    _load_anthropic_key
    claude "Build: $*"
}

# Explain code
explain() {
    _load_anthropic_key
    if [ -f "$1" ]; then
        claude "Explain this code:" < "$1"
    else
        claude "Explain: $*"
    fi
}

# Review code
review() {
    _load_anthropic_key
    if [ -f "$1" ]; then
        claude "Review this code for issues, improvements:" < "$1"
    else
        echo "Usage: review <filename>"
    fi
}

# Refactor
refactor() {
    _load_anthropic_key
    if [ -f "$1" ]; then
        claude "Refactor this code to be cleaner and more efficient:" < "$1"
    else
        claude "Refactor: $*"
    fi
}

# Debug help
debug() {
    _load_anthropic_key
    claude "Debug this issue: $*"
}

# Create new file with AI
create() {
    _load_anthropic_key
    claude "Create a new file: $*"
}

# Git commit with AI message
aicommit() {
    _load_anthropic_key
    local diff=$(git diff --staged)
    if [ -z "$diff" ]; then
        echo "No staged changes. Stage files first: git add <files>"
        return 1
    fi
    claude "Write a concise git commit message for these changes:" <<< "$diff"
}

# ═══════════════════════════════════════════════════════════════════
# PROJECT SHORTCUTS - Rob's Common Locations
# ═══════════════════════════════════════════════════════════════════

# Fish Music projects
alias cc-fish="cd ~/Projects/fishmusicinc && claude"
alias cc-noizyvox="cd ~/Projects/noizyvox && claude"
alias cc-noizylab="cd ~/Projects/noizylab && claude"

# Quick project navigation
alias cc-aquarium="cd ~/Projects/aquarium && claude"
alias cc-mc96="cd ~/Projects/mc96 && claude"

# ═══════════════════════════════════════════════════════════════════
# WORKFLOW COMMANDS
# ═══════════════════════════════════════════════════════════════════

# Morning startup - load everything
morning-code() {
    _load_anthropic_key
    echo "🌅 Good morning Rob!"
    echo "   API Key: $([ -n "$ANTHROPIC_API_KEY" ] && echo '✅ Loaded' || echo '❌ Missing')"
    echo "   Claude Code: $(command -v claude &>/dev/null && echo '✅ Ready' || echo '❌ Not installed')"
    echo ""
    echo "   Commands: cc, fix, build, review, debug, create"
    echo "   Projects: cc-fish, cc-noizyvox, cc-noizylab"
}

# Status check
cc-status() {
    echo "Claude Code Status:"
    echo "  Installed: $(command -v claude &>/dev/null && claude --version || echo 'No')"
    echo "  API Key: $([ -n "$ANTHROPIC_API_KEY" ] && echo 'Set ✅' || echo 'Not set ❌')"
    echo "  Vault: $([ -f ~/api_token_vault.py ] && echo 'Available ✅' || echo 'Not found')"
}

# Reload API key
cc-reload() {
    unset ANTHROPIC_API_KEY
    _load_anthropic_key
    echo "✅ API key reloaded: $([ -n "$ANTHROPIC_API_KEY" ] && echo 'Found' || echo 'Not found')"
}

# ═══════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════

echo "🤖 Claude Code Ready"
echo "   cc | fix | build | review | debug | create"
CCSHORTCUTS

echo "✅ Shortcuts created: ~/claude_code_shortcuts.sh"

# ═══════════════════════════════════════════════════════════════════
# 4. ADD TO SHELL CONFIG
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "🔧 Adding to shell config..."

ZSHRC="${HOME}/.zshrc"

# Add Claude Code shortcuts
if ! grep -q "claude_code_shortcuts.sh" "$ZSHRC" 2>/dev/null; then
    echo "" >> "$ZSHRC"
    echo "# Claude Code - Primary Coding Tool" >> "$ZSHRC"
    echo "source ~/claude_code_shortcuts.sh" >> "$ZSHRC"
    echo "✅ Added to .zshrc"
else
    echo "⏭️  Already in .zshrc"
fi

# ═══════════════════════════════════════════════════════════════════
# 5. CREATE PROJECT DIRECTORIES
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "📁 Setting up project directories..."

mkdir -p ~/Projects/{fishmusicinc,noizyvox,noizylab,aquarium,mc96}
echo "✅ Project directories ready"

# ═══════════════════════════════════════════════════════════════════
# 6. VERIFY INSTALLATION
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "🔍 Verifying installation..."

if command -v claude &> /dev/null; then
    VERSION=$(claude --version 2>/dev/null || echo "installed")
    echo "✅ Claude Code: $VERSION"
else
    echo "❌ Claude Code not found in PATH"
    echo "   Try: npm install -g @anthropic-ai/claude-code"
fi

# ═══════════════════════════════════════════════════════════════════
# DONE
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║              ✅ CLAUDE CODE SETUP COMPLETE                        ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║                                                                   ║"
echo "║  RELOAD SHELL:                                                    ║"
echo "║    source ~/.zshrc                                                ║"
echo "║                                                                   ║"
echo "║  FIRST TIME:                                                      ║"
echo "║    vault add anthropic YOUR-ANTHROPIC-API-KEY                     ║"
echo "║                                                                   ║"
echo "║  DAILY USE:                                                       ║"
echo "║    cc              → Start Claude Code                            ║"
echo "║    fix 'the bug'   → Quick fix                                    ║"
echo "║    build 'an API'  → Build something                              ║"
echo "║    review file.py  → Code review                                  ║"
echo "║    debug 'error'   → Debug help                                   ║"
echo "║    create 'script' → Create new file                              ║"
echo "║                                                                   ║"
echo "║  PROJECTS:                                                        ║"
echo "║    cc-fish         → Fish Music Inc                               ║"
echo "║    cc-noizyvox     → NOIZYVOX                                     ║"
echo "║    cc-noizylab     → NOIZYLAB                                     ║"
echo "║                                                                   ║"
echo "║  STATUS:                                                          ║"
echo "║    cc-status       → Check everything                             ║"
echo "║    morning-code    → Morning startup                              ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"

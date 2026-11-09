# ============================================================================
# 00_env.zsh - Environment Variables & Paths
# ============================================================================
# SECURITY: API keys moved to ~/.env.secrets (sourced below)
# ============================================================================

# --- PATH CONFIGURATION ---
export PATH="$HOME/bin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"
export PATH="/Users/m2ultra/scripts/mail_manager_pro/bin:$PATH"

# --- LOAD SECRETS (if exists) ---
# API keys are stored separately for security
[[ -f "$HOME/.env.secrets" ]] && source "$HOME/.env.secrets"

# --- NOIZYLAB CORE ---
export NOIZYLAB_HOME="/Users/m2ultra/.claude-worktrees/NOIZYLAB/upbeat-moore"
export RR_ROOT="$HOME/NOIZYLAB_GIT_STAGING/repairrob"
export RR_SRC="$RR_ROOT/src"

# --- GABRIEL CORE ---
export GABRIEL="$HOME/NOIZYLAB/GABRIEL"

# --- DRIVES ---
export DRIVE_RED_DRAGON="/Volumes/RED DRAGON"
export DRIVE_RSP="/Volumes/RSP"
export DRIVE_DATA="/Volumes/RSP/NOISYLABZ"

# --- EDITOR ---
export EDITOR="nano"
export PAGER="cat"

# --- OLLAMA ---
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_MAX_LOADED_MODELS=3
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_HOST="0.0.0.0"

# --- CLAUDE CODE ---
export MAX_THINKING_TOKENS=1024
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096

# --- AI ENVIRONMENT ---
[[ -f "$HOME/.ai-env/bin/activate" ]] && source "$HOME/.ai-env/bin/activate"

# --- MC96 ---
export MC96_QUARANTINE="$HOME/MC96_Quarantine"
export MC96_SCANS="$HOME/MC96_TruthScans"

# --- TAILSCALE ---
# Set your Tailscale sync target here (hostname of target machine)
export TAILSCALE_SYNC_TARGET=""

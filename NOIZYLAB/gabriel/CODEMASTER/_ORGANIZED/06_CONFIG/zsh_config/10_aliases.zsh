# ============================================================================
# 10_aliases.zsh - Shortcuts & Commands
# ============================================================================

# --- GOD MODE COMMANDS ---
alias email='god email'
alias mail='god email'
alias inbox='god email inbox'
alias support='god email support'
alias net='god net'
alias dns='god net dns'
alias noizy='god noizy'
alias fish='god fish'
alias cf='god cf'

# --- DREAMCHAMBER BRIDGE ---
alias pc='dreamchamber'
alias dc='dreamchamber'

# --- NOIZYLAB NAVIGATION ---
alias nl="$HOME/NOIZYLAB/LAUNCH.sh"
alias mc96="$HOME/NOIZYLAB/MC96"
alias nd="cd $NOIZYLAB_HOME"
alias rd="cd $DRIVE_RED_DRAGON"
alias rsp="cd $DRIVE_RSP"
alias data="cd $DRIVE_DATA"

# --- ORGANIZED FOLDERS ---
alias org-py="cd $NOIZYLAB_HOME/_ORGANIZED/BY_TYPE/PYTHON"
alias org-json="cd $NOIZYLAB_HOME/_ORGANIZED/BY_TYPE/JSON"
alias org-func="cd $NOIZYLAB_HOME/_ORGANIZED/BY_FUNCTION"
alias org-scripts="cd $NOIZYLAB_HOME/_ORGANIZED/BY_FUNCTION/SCRIPTS"

# --- GABRIEL & WORKERS ---
alias gabriel='cd $GABRIEL'
alias gab='cd $GABRIEL'
alias g='cd $GABRIEL'
alias gorunfree='$GABRIEL/gorunfree'
alias grf='$GABRIEL/gorunfree'
alias deploy='cd $GABRIEL/workers/noizylab-main && wrangler deploy'
alias deploy-all='for w in $GABRIEL/workers/*/wrangler.toml; do (cd "$(dirname "$w")" && wrangler deploy); done'

# --- GABRIEL API ---
alias worker='curl -s https://noizylab.rsplowman.workers.dev'
alias wstatus='curl -s https://noizylab.rsplowman.workers.dev/status | jq'
alias whealth='curl -s https://noizylab.rsplowman.workers.dev/health | jq'
alias wask='curl -s -X POST https://noizylab.rsplowman.workers.dev/api/ask -H "Content-Type: application/json" -d'

# --- REPAIR ROB (GIT STAGING) ---
alias crr='cd "$RR_ROOT"'
alias rrsetup='$HOME/rr.sh setup'
alias rrall='$HOME/rr.sh all'
alias norr='nano "$HOME/rr.sh"'
alias nodata='nano "$RR_SRC/dataset.py"'
alias noinfer='nano "$RR_SRC/infer.py"'

# --- MAINTENANCE & SYSTEM ---
alias resetos="~/Tools/macos-reset/reset_macos_settings_v3.sh"
alias declutter='$GABRIEL/../scripts/DECLUTTER.sh 2>/dev/null || ~/NOIZYLAB/scripts/DECLUTTER.sh'
alias repair='$GABRIEL/../scripts/MASTER_REPAIR.sh 2>/dev/null || ~/NOIZYLAB/scripts/MASTER_REPAIR.sh'
alias health='$GABRIEL/../scripts/health-check.sh 2>/dev/null || ~/NOIZYLAB/scripts/health-check.sh'
alias diskfree='df -h / | tail -1'
alias memfree='vm_stat | head -5'
alias jumbo='sudo ifconfig en0 mtu 9000'

# --- ENTERPRISE v2.0 SHORTCUTS ---
alias enterprise='~/.local/bin/interactive-enterprise-v2.sh'
alias interactive='~/.local/bin/interactive-session-manager.sh'
alias remote-dashboard="cd ~/.noizylab/web && python3 -m http.server 8888 --bind 127.0.0.1"

# --- GIT SHORTCUTS ---
alias gpush='cd $GABRIEL && git add -A && git commit -m "Update $(date +%Y-%m-%d)" && git push'
alias gpull='cd $GABRIEL && git pull'
alias g-status="cd $NOIZYLAB_HOME && git status --short"
alias g-push="cd $NOIZYLAB_HOME && git push -u origin upbeat-moore"
alias g-pull="cd $NOIZYLAB_HOME && git pull origin upbeat-moore"

# --- SHELL ---
alias mailmgr='/Users/m2ultra/scripts/mail_manager_pro/bin/mailmgr'

# --- AI / LLM SHORTCUTS ---
alias ai='~/bin/ai'
alias code='ollama run codestral'
alias llama70='ollama run llama3.1:70b'
alias qwen72='ollama run qwen2.5:72b'
alias models='ollama list'
alias aiwhisper='source ~/.ai-env/bin/activate && mlx_lm.generate'

# ============================================================================
# MC96 TRUTH SCANNER & DEDUPE
# ============================================================================
alias scan='mc96_truth_scanner.sh'
alias scan-sync='mc96_truth_scanner.sh --sync'
alias dedupe='python3 ~/bin/mc96_dedupe.py'
alias quarantine='mc96_quarantine.sh'
alias qstatus='mc96_quarantine.sh status'

# ============================================================================
# TAILSCALE VPN
# ============================================================================
alias ts='tailscale_setup.sh'
alias ts-status='tailscale_setup.sh status'
alias ts-up='tailscale_setup.sh up'
alias ts-down='tailscale_setup.sh down'
alias ts-send='tailscale_setup.sh send'
alias ts-ssh='tailscale_setup.sh ssh'

# Quick Tailscale commands (direct)
alias tss='tailscale status'
alias tsip='tailscale ip -4'
alias tsnodes='tailscale status | grep -v "^#"'

# ============================================================================
# .zshrc - NoizyLab Modular Configuration Loader
# ============================================================================
# This file automatically loads configuration modules from ~/.config/zsh/

# 1. Load all .zsh files in alphabetical order
if [ -d "$HOME/.config/zsh" ]; then
    for config_file in "$HOME/.config/zsh/"*.zsh; do
        [ -f "$config_file" ] && source "$config_file"
    done
fi

# 2. Key Bindings (Standard macOS)
bindkey -e

# 3. Simple Prompt (Can be enhanced later)
export PS1="%F{cyan}%n@%m%f:%F{yellow}%~%f$ "

# 4. Final Status Check
# echo "✨ NoizyLab Environment Loaded."

# Voice Forge Aliases
alias vf='/Users/m2ultra/voice-forge-local/scripts/voice-forge-god.sh'
alias vf-stop='docker-compose -f /Users/m2ultra/voice-forge-local/docker-compose.yml down'
alias vf-status='/Users/m2ultra/voice-forge-local/scripts/mc96-voice-status.sh'
alias vf-logs='tail -f /Users/m2ultra/voice-forge-local/voice-forge.log'
export GEMINI_API_KEY="AIzaSyApy-oSdDxL71Ht1pCRcnnbjobbmRIGSPI"
export PATH="$PATH:/Users/m2ultra/NOIZYLAB/bin"

# 🚀 GOOGLE & MICROSOFT AI QUICK ACCESS ALIASES
alias gemini="open https://gemini.google.com"
alias notebooklm="open https://notebooklm.google.com"
alias aistudio="open https://aistudio.google.com"
alias copilot="open -a 'Microsoft Edge' https://copilot.microsoft.com"
alias designer="open https://designer.microsoft.com"
alias azure="open https://portal.azure.com"
alias ai-menu="/Users/m2ultra/NOIZYLAB/MC96/ai_quick_access.sh"

# 🎤 MICROSOFT VOICE GENERATOR ALIASES
alias voice-gen="/Users/m2ultra/NOIZYLAB/MC96/voice_generator.py"
alias voice-menu="/Users/m2ultra/NOIZYLAB/MC96/voice_quick_start.sh"
alias speech-studio="open https://speech.microsoft.com/portal"

# 🎤 FREE VOICE TOOLS ALIASES
alias voice-tools="/Users/m2ultra/NOIZYLAB/MC96/voice_tools_quick_access.sh"
alias whisper-transcribe="whisper"
alias voice-all="cat /Users/m2ultra/NOIZYLAB/MC96/ALL_FREE_VOICE_TECH_COMPLETE.md"

# 🎤 VOICE AI ALIASES
alias voice-ai-universal="python3 /Users/m2ultra/NOIZYLAB/MC96/voice_ai_universal.py"
alias voice-ai-setup="/Users/m2ultra/NOIZYLAB/MC96/voice_ai_api_setup.sh"
alias voice-ai-install="/Users/m2ultra/NOIZYLAB/MC96/install_all_voice_ai.sh"

. "$HOME/.local/bin/env"

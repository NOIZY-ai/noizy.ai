#!/bin/bash
# =============================================================================
# 🔐 NOIZYVOX API KEY QUICK COMMANDS
# =============================================================================
# ONE LOCATION • MAXIMUM SECURITY • DIRECT LINKS
#
# Usage: source this file or run: ./api_keys.sh [command]
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DASHBOARD="$SCRIPT_DIR/api_dashboard.py"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_help() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}  🔐 ${GREEN}NOIZYVOX API KEY COMMANDS${NC}                               ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${GREEN}api${NC}              - Open interactive dashboard"
    echo -e "  ${GREEN}api status${NC}       - Show current API key status"
    echo -e "  ${GREEN}api links${NC}        - Show quick links for required keys"
    echo -e "  ${GREEN}api setup${NC}        - Guided setup wizard"
    echo -e "  ${GREEN}api open${NC}         - Open all required key URLs"
    echo -e "  ${GREEN}api add NAME${NC}     - Add a specific API key"
    echo -e "  ${GREEN}api export${NC}       - Export keys to shell format"
    echo ""
    echo -e "  ${YELLOW}Quick Links:${NC}"
    echo -e "  ${BLUE}anthropic${NC}        - https://console.anthropic.com/settings/keys"
    echo -e "  ${BLUE}openai${NC}           - https://platform.openai.com/api-keys"
    echo -e "  ${BLUE}elevenlabs${NC}       - https://elevenlabs.io/app/settings/api-keys"
    echo -e "  ${BLUE}cloudflare${NC}       - https://dash.cloudflare.com/profile/api-tokens"
    echo ""
}

# Quick link functions
anthropic() { open "https://console.anthropic.com/settings/keys"; }
openai_keys() { open "https://platform.openai.com/api-keys"; }
elevenlabs() { open "https://elevenlabs.io/app/settings/api-keys"; }
cloudflare() { open "https://dash.cloudflare.com/profile/api-tokens"; }
huggingface() { open "https://huggingface.co/settings/tokens"; }
replicate() { open "https://replicate.com/account/api-tokens"; }
groq() { open "https://console.groq.com/keys"; }
deepgram() { open "https://console.deepgram.com/"; }
stripe() { open "https://dashboard.stripe.com/apikeys"; }
github_tokens() { open "https://github.com/settings/tokens?type=beta"; }
vercel() { open "https://vercel.com/account/tokens"; }
supabase() { open "https://supabase.com/dashboard/project/_/settings/api"; }

# Main api command
api() {
    case "$1" in
        status)
            python3 "$DASHBOARD" --status
            ;;
        links)
            python3 "$DASHBOARD" --links
            ;;
        setup)
            python3 "$DASHBOARD" --setup
            ;;
        open)
            python3 "$DASHBOARD" --open-all
            ;;
        add)
            if [ -n "$2" ]; then
                python3 "$DASHBOARD" --add "$2"
            else
                echo "Usage: api add KEY_NAME"
            fi
            ;;
        export)
            python3 "$DASHBOARD" --export
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            python3 "$DASHBOARD"
            ;;
    esac
}

# If script is run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "$1" in
        status)   python3 "$DASHBOARD" --status ;;
        links)    python3 "$DASHBOARD" --links ;;
        setup)    python3 "$DASHBOARD" --setup ;;
        open)     python3 "$DASHBOARD" --open-all ;;
        add)      python3 "$DASHBOARD" --add "$2" ;;
        export)   python3 "$DASHBOARD" --export ;;
        help|--help|-h|"") show_help ;;
        anthropic|openai_keys|elevenlabs|cloudflare|huggingface|replicate|groq|deepgram|stripe|github_tokens|vercel|supabase)
            "$1"
            ;;
        *)        python3 "$DASHBOARD" "$@" ;;
    esac
fi

CLOUDFLARE_API_TOKEN=your_token_here

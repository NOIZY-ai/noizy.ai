#!/usr/bin/env bash
# Interactive Terminal UI with keyboard navigation

declare -A TUI_STATE
TUI_STATE[current_screen]="main"
TUI_STATE[selected_item]=0

get_terminal_size() {
    TUI_STATE[rows]=$(tput lines)
    TUI_STATE[cols]=$(tput cols)
}

# Colors for TUI
TUI_BG="\033[48;5;235m"
TUI_FG="\033[38;5;252m"
TUI_HIGHLIGHT="\033[48;5;27m\033[38;5;255m"
TUI_HEADER="\033[48;5;24m\033[38;5;255m\033[1m"

cursor_hide() { printf '\033[?25l'; }
cursor_show() { printf '\033[?25h'; }
move_to() { printf '\033[%d;%dH' "$1" "$2"; }
tui_clear() { printf '\033[2J\033[H'; }

draw_box() {
    local y=$1 x=$2 h=$3 w=$4 title="${5:-}"
    move_to $y $x
    printf "┌"
    for ((i=1; i<w-1; i++)); do printf "─"; done
    printf "┐"
    
    [[ -n "$title" ]] && { move_to $y $((x + 2)); printf " %s " "$title"; }
    
    for ((i=1; i<h-1; i++)); do
        move_to $((y+i)) $x; printf "│"
        move_to $((y+i)) $((x+w-1)); printf "│"
    done
    
    move_to $((y+h-1)) $x
    printf "└"
    for ((i=1; i<w-1; i++)); do printf "─"; done
    printf "┘"
}

draw_header() {
    local title="$1"
    local width=${TUI_STATE[cols]}
    move_to 1 1
    printf "\033[48;5;24m\033[38;5;255m"
    printf "%-${width}s" "📧 MAIL MANAGER PRO v3.5 — $title"
    printf "\033[0m"
}

draw_menu() {
    local -n items=$1
    local selected=$2
    local start_row=$3
    local start_col=$4
    local width=$5
    
    local i
    for ((i=0; i<${#items[@]}; i++)); do
        move_to $((start_row + i)) $start_col
        if [[ $i -eq $selected ]]; then
            printf "\033[48;5;27m\033[38;5;255m ▶ %-$((width-4))s \033[0m" "${items[$i]}"
        else
            printf "   %-$((width-4))s " "${items[$i]}"
        fi
    done
}

MAIN_MENU_ITEMS=(
    "📁 Folders       - Create, list, sync folders"
    "📋 Rules         - Manage mail sorting rules"
    "👤 Accounts      - Configure mail accounts"
    "💾 Backup        - Backup & restore"
    "⏰ Scheduler     - Scheduled tasks"
    "🔌 API Server    - REST API management"
    "🩺 Health Check  - System diagnostics"
    "❌ Exit"
)

screen_main() {
    draw_header "Main Menu"
    local box_width=50
    local box_height=$((${#MAIN_MENU_ITEMS[@]} + 4))
    local box_x=$(( (${TUI_STATE[cols]} - box_width) / 2 ))
    local box_y=5
    
    draw_box $box_y $box_x $box_height $box_width "Main Menu"
    draw_menu MAIN_MENU_ITEMS ${TUI_STATE[selected_item]} $((box_y + 2)) $((box_x + 2)) $((box_width - 4))
    
    move_to $((${TUI_STATE[rows]} - 1)) 2
    printf "↑↓: Navigate | Enter: Select | q: Quit"
}

cmd_tui() {
    command -v tput &>/dev/null || { echo "tput required for TUI"; return 1; }
    
    get_terminal_size
    cursor_hide
    tui_clear
    trap 'cursor_show; tui_clear; exit 0' EXIT INT TERM
    
    local running=true
    while $running; do
        tui_clear
        screen_main
        
        IFS= read -rsn1 key
        if [[ "$key" == $'\x1b' ]]; then
            read -rsn2 -t 0.1 key
            case "$key" in
                '[A') ((TUI_STATE[selected_item]--)); [[ ${TUI_STATE[selected_item]} -lt 0 ]] && TUI_STATE[selected_item]=0 ;;
                '[B') ((TUI_STATE[selected_item]++)); [[ ${TUI_STATE[selected_item]} -ge ${#MAIN_MENU_ITEMS[@]} ]] && TUI_STATE[selected_item]=$((${#MAIN_MENU_ITEMS[@]} - 1)) ;;
            esac
        else
            case "$key" in
                q|Q) running=false ;;
                '') [[ ${TUI_STATE[selected_item]} -eq $((${#MAIN_MENU_ITEMS[@]} - 1)) ]] && running=false ;;
            esac
        fi
    done
    
    cursor_show
    tui_clear
    success "Goodbye!"
}


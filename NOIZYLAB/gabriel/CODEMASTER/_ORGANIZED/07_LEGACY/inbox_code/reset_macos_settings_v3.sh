#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------
# macOS user settings reset (modular v3)
# Run as your normal user (e.g. rsplowman), NOT sudo.
# ----------------------------------------

PREF_DIR="$HOME/Library/Preferences"
BACKUP_ROOT="$HOME/PreferencesResets"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/run_$TIMESTAMP"
DRY_RUN=false

RESET_DOCK=false
RESET_FINDER=false
RESET_INPUT=false
RESET_GLOBAL=false
RESET_SPACES=false
RESET_CONTROLCENTER=false
RESET_DESKTOP=false

# --- Colors (fallback if not TTY) ---
if [ -t 1 ]; then
  BOLD="\033[1m"
  DIM="\033[2m"
  RED="\033[31m"
  GREEN="\033[32m"
  YELLOW="\033[33m"
  RESET="\033[0m"
else
  BOLD=""; DIM=""; RED=""; GREEN=""; YELLOW=""; RESET=""
fi

log()  { echo -e "${BOLD}[*]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!]${RESET} $*"; }
err()  { echo -e "${RED}[x]${RESET} $*" >&2; }

usage() {
  cat <<EOF2
Usage: \$(basename "\$0") [options]

Options:
  --all            Reset Dock, Finder, input, global, spaces, menubar, desktop
  --dock           Reset Dock settings
  --finder         Reset Finder settings
  --input          Reset trackpad/mouse/keyboard related prefs
  --global         Reset global hotkeys & NSGlobalDomain basics
  --spaces         Reset Spaces / Mission Control / Stage Manager layout
  --menubar        Reset Control Center & menu bar items
  --desktop        Reset desktop & screensaver layout prefs
  --dry-run        Show what would be changed, but do nothing
  -h, --help       Show this help

No options = same as --all
EOF2
}

# --- Arg parsing ---
if [ "$#" -eq 0 ]; then
  RESET_DOCK=true
  RESET_FINDER=true
  RESET_INPUT=true
  RESET_GLOBAL=true
  RESET_SPACES=true
  RESET_CONTROLCENTER=true
  RESET_DESKTOP=true
else
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --all)
        RESET_DOCK=true
        RESET_FINDER=true
        RESET_INPUT=true
        RESET_GLOBAL=true
        RESET_SPACES=true
        RESET_CONTROLCENTER=true
        RESET_DESKTOP=true
        ;;
      --dock)        RESET_DOCK=true ;;
      --finder)      RESET_FINDER=true ;;
      --input)       RESET_INPUT=true ;;
      --global)      RESET_GLOBAL=true ;;
      --spaces)      RESET_SPACES=true ;;
      --menubar|--control-center)
                      RESET_CONTROLCENTER=true ;;
      --desktop)     RESET_DESKTOP=true ;;
      --dry-run)     DRY_RUN=true ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        err "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
    shift
  done
fi

# --- Safety checks ---
if [ "$EUID" -eq 0 ]; then
  err "Do NOT run this as root. Run it as your normal user."
  exit 1
fi

log "macOS user settings reset (v3)"
echo "User: $USER"
echo "Home: $HOME"
echo

# --- Helpers ---
ensure_backup_dir() {
  [ -d "$BACKUP_DIR" ] && return 0
  log "Creating backup directory: $BACKUP_DIR"
  $DRY_RUN || mkdir -p "$BACKUP_DIR"
}

backup_plist() {
  local domain="$1"
  local plist

  if [ "$domain" = "NSGlobalDomain" ]; then
    plist="$PREF_DIR/.GlobalPreferences.plist"
  else
    plist="$PREF_DIR/${domain}.plist"
  fi

  if [ -f "$plist" ]; then
    ensure_backup_dir
    log "Backing up $plist"
    if ! $DRY_RUN; then
      mv "$plist" "$BACKUP_DIR"/
    fi
  else
    echo "  (no plist file for $domain)"
  fi
}

clear_domain() {
  local domain="$1"
  backup_plist "$domain"
  log "Clearing defaults for $domain"
  if ! $DRY_RUN; then
    defaults delete "$domain" >/dev/null 2>&1 || true
  fi
}

# --- Groups ---
reset_dock() {
  log "=== Dock ==="
  clear_domain "com.apple.dock"

  if ! $DRY_RUN; then
    defaults write com.apple.dock show-recents -bool true
    defaults write com.apple.dock tilesize -int 48
    killall Dock >/dev/null 2>&1 || true
  fi
}

reset_finder() {
  log "=== Finder ==="
  clear_domain "com.apple.finder"

  if ! $DRY_RUN; then
    defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"  # list view
    killall Finder >/dev/null 2>&1 || true
  fi
}

reset_input() {
  log "=== Input (trackpad/mouse/keyboard layout) ==="
  local domains=(
    "com.apple.AppleMultitouchTrackpad"
    "com.apple.driver.AppleBluetoothMultitouch.trackpad"
    "com.apple.driver.AppleBluetoothMultitouch.mouse"
    "com.apple.mouse"
    "com.apple.trackpad"
    "com.apple.HIToolbox"
  )

  for d in "${domains[@]}"; do
    clear_domain "$d"
  done
}

reset_global() {
  log "=== Global (shortcuts & general prefs) ==="
  clear_domain "com.apple.symbolichotkeys"
  clear_domain "NSGlobalDomain"

  if ! $DRY_RUN; then
    killall SystemUIServer >/dev/null 2>&1 || true
  fi
}

reset_spaces() {
  log "=== Spaces / Mission Control / Stage Manager ==="
  local domains=(
    "com.apple.spaces"
    "com.apple.WindowManager"
  )

  for d in "${domains[@]}"; do
    clear_domain "$d"
  done

  if ! $DRY_RUN; then
    killall Dock >/dev/null 2>&1 || true
  fi
}

reset_controlcenter() {
  log "=== Control Center / Menu Bar ==="
  local domains=(
    "com.apple.controlcenter"
    "com.apple.systemuiserver"
  )

  for d in "${domains[@]}"; do
    clear_domain "$d"
  done

  if ! $DRY_RUN; then
    killall SystemUIServer >/dev/null 2>&1 || true
  fi
}

reset_desktop() {
  log "=== Desktop & Screen Saver layout ==="
  local domains=(
    "com.apple.desktop"
    "com.apple.ScreenSaver.Engine"
    "com.apple.ScreenSaverPhotoChooser"
  )

  for d in "${domains[@]}"; do
    clear_domain "$d"
  done

  if ! $DRY_RUN; then
    killall Dock >/dev/null 2>&1 || true
    killall SystemUIServer >/dev/null 2>&1 || true
  fi
}

# --- Run selected groups ---
$RESET_DOCK           && reset_dock
$RESET_FINDER         && reset_finder
$RESET_INPUT          && reset_input
$RESET_GLOBAL         && reset_global
$RESET_SPACES         && reset_spaces
$RESET_CONTROLCENTER  && reset_controlcenter
$RESET_DESKTOP        && reset_desktop

echo
if $DRY_RUN; then
  warn "Dry run only: no files were moved or changed."
else
  log "Done."
  if [ -d "$BACKUP_DIR" ]; then
    echo -e "${DIM}Backups stored at:${RESET} $BACKUP_DIR"
    echo "You can restore individual .plist files if needed (while apps are closed)."
  else
    warn "No preference files were backed up (nothing existed for these domains)."
  fi
fi

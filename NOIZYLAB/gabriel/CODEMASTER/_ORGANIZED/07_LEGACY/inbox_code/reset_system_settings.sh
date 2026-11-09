#!/bin/zsh
set -euo pipefail

# *** CONFIG ***
# Automatically detect current user instead of hardcoding
TARGET_USER="$(id -un)"
EMAIL_FOR_NOTE="${TARGET_USER}@icloud.com"

echo "=========================================="
echo "  macOS System Settings Reset Script"
echo "=========================================="
echo
echo "User:  $TARGET_USER"
echo "Email: $EMAIL_FOR_NOTE"
echo

# Core domains tied to System Settings & basic UI
DOMAINS=(
  "com.apple.systempreferences"               # legacy System Preferences
  "com.apple.systemsettings"                  # newer System Settings
  "com.apple.dock"
  "com.apple.finder"
  "com.apple.controlcenter"
  "com.apple.Spotlight"
  "com.apple.universalaccess"                 # Accessibility
  "com.apple.Accessibility"
  "com.apple.AppleMultitouchTrackpad"
  "com.apple.AppleMultitouchMouse"
  "com.apple.driver.AppleBluetoothMultitouch.trackpad"
  "com.apple.driver.AppleBluetoothMultitouch.mouse"
  "com.apple.loginitems"
  "com.apple.multitouch.trackpad"
  "com.apple.HIToolbox"
)

# Show what will be reset
echo "The following preference domains will be RESET to defaults:"
echo
for domain in "${DOMAINS[@]}"; do
  PLIST="$HOME/Library/Preferences/${domain}.plist"
  if [[ -f "$PLIST" ]]; then
    echo "  - $domain (exists)"
  else
    echo "  - $domain (not present)"
  fi
done

echo
echo "This will reset:"
echo "  - Dock layout, size, position, autohide"
echo "  - Finder preferences and view settings"
echo "  - Control Center menu bar items"
echo "  - Spotlight search preferences"
echo "  - Accessibility features"
echo "  - Trackpad/Mouse gestures and sensitivity"
echo "  - Keyboard input sources"
echo

# Confirmation prompt - handle both interactive and piped input
if [[ -t 0 ]]; then
  # Interactive mode
  echo -n "Are you sure you want to continue? [y/N]: "
  read -r CONFIRM
else
  # Non-interactive (piped) mode
  read -r CONFIRM
  echo "Are you sure you want to continue? [y/N]: $CONFIRM"
fi

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

# Create backup directory
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$HOME/PreferencesResets/SystemSettingsBackup_$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

echo
echo "Backup directory: $BACKUP_DIR"
echo
echo "Backing up and resetting preference domains..."
echo

RESET_COUNT=0
SKIP_COUNT=0

for domain in "${DOMAINS[@]}"; do
  PLIST="$HOME/Library/Preferences/${domain}.plist"

  if [[ -f "$PLIST" ]]; then
    echo "[$domain]"
    echo "  Backing up..."
    if cp "$PLIST" "$BACKUP_DIR/"; then
      echo "  Deleting defaults..."
      defaults delete "$domain" >/dev/null 2>&1 || true
      echo "  Removing plist..."
      rm -f "$PLIST" 2>/dev/null || true
      echo "  Done."
      RESET_COUNT=$((RESET_COUNT + 1))
    else
      echo "  ERROR: Failed to backup, skipping reset for safety."
      SKIP_COUNT=$((SKIP_COUNT + 1))
    fi
  else
    echo "[$domain] - skipped (no plist file)"
    SKIP_COUNT=$((SKIP_COUNT + 1))
  fi
done

echo
echo "Restarting affected processes..."

killall "System Settings" >/dev/null 2>&1 || true
killall "System Preferences" >/dev/null 2>&1 || true
killall Dock >/dev/null 2>&1 || true
killall Finder >/dev/null 2>&1 || true

echo
echo "=========================================="
echo "  Reset Complete"
echo "=========================================="
echo
echo "Summary:"
echo "  - Domains reset: $RESET_COUNT"
echo "  - Domains skipped: $SKIP_COUNT"
echo "  - Backup location: $BACKUP_DIR"
echo
echo "Next steps:"
echo "  1. Log out and back in (or reboot) to fully apply changes"
echo "  2. To restore, copy files from backup to ~/Library/Preferences/"
echo
echo "Restore command (if needed):"
echo "  cp \"$BACKUP_DIR\"/*.plist ~/Library/Preferences/"
echo

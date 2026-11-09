#!/bin/bash
# GRUNFREEX3000 - Ultimate macOS Migration System
# Usage: sudo ./GRUNFREEX3000.sh OLDUSER NEWUSER [--dry-run]

OLDUSER="$1"
NEWUSER="$2"
DRYRUN="$3"
LOGFILE="/tmp/grunfreex3000.log"
BACKUP="/Users/${OLDUSER}_backup_$(date +%Y%m%d).tar.gz.enc"

echo "=== GRUNFREEX3000 Migration Started ===" | tee "$LOGFILE"

# Validate input
if [ -z "$OLDUSER" ] || [ -z "$NEWUSER" ]; then
    echo "Usage: sudo $0 OLDUSER NEWUSER [--dry-run]"
    exit 1
fi

# Check users exist
id "$OLDUSER" &>/dev/null || { echo "Old user not found!"; exit 1; }
id "$NEWUSER" &>/dev/null || { echo "New user not found!"; exit 1; }

# GUI confirmation
osascript -e 'display dialog "Proceed with GRUNFREEX3000 migration?" buttons {"Cancel", "OK"} default button "OK"' || exit 0

# Encrypted backup
echo "Creating encrypted backup of $OLDUSER..."
if [ "$DRYRUN" != "--dry-run" ]; then
    tar -czf - "/Users/$OLDUSER" | openssl enc -aes-256-cbc -salt -out "$BACKUP"
    echo "Backup stored at $BACKUP" | tee -a "$LOGFILE"
fi

# Migration folders
MIGRATION_DIR="/Users/$NEWUSER/Migration"
mkdir -p "$MIGRATION_DIR"

FOLDERS=("Documents" "Desktop" "Downloads" "Pictures" "Movies" "Music")
for folder in "${FOLDERS[@]}"; do
    SRC="/Users/$OLDUSER/$folder"
    if [ -d "$SRC" ]; then
        echo "Copying $SRC..."
        if [ "$DRYRUN" == "--dry-run" ]; then
            echo "[DRY RUN] Would copy $SRC to $MIGRATION_DIR/"
        else
            rsync -ah --progress "$SRC" "$MIGRATION_DIR/"
        fi
    fi
done

# Safe Library migration
SAFE_LIB=("Application Support" "Fonts" "Safari")
for lib in "${SAFE_LIB[@]}"; do
    SRC="/Users/$OLDUSER/Library/$lib"
    if [ -d "$SRC" ]; then
        echo "Migrating Library/$lib..."
        if [ "$DRYRUN" != "--dry-run" ]; then
            mkdir -p "$MIGRATION_DIR/Library"
            rsync -ah --progress "$SRC" "$MIGRATION_DIR/Library/"
        fi
    fi
done

# Keychain & Mail
if [ "$DRYRUN" != "--dry-run" ]; then
    echo "Migrating Keychain and Mail..."
    cp -R "/Users/$OLDUSER/Library/Keychains" "$MIGRATION_DIR/Library/"
    cp -R "/Users/$OLDUSER/Library/Mail" "$MIGRATION_DIR/Library/"
fi

# Fix permissions
if [ "$DRYRUN" != "--dry-run" ]; then
    chown -R "$NEWUSER":staff "$MIGRATION_DIR"
fi

# Auto-delete old user
read -p "Delete old user $OLDUSER now? (y/n): " DELETE
if [ "$DELETE" == "y" ]; then
    sysadminctl -deleteUser "$OLDUSER" --secure
fi

echo "Migration complete! Files are in $MIGRATION_DIR"
echo "=== GRUNFREEX3000 Finished ==="

#!/bin/bash
# Quick User Migration - X1000 Simple
# Usage: sudo ./migrate_user.sh OLDUSER

OLDUSER="$1"
[ -z "$OLDUSER" ] && { echo "Usage: sudo $0 OLDUSER"; exit 1; }

echo "🚀 Migrating $OLDUSER to $(whoami)..."

# Create migration folder
mkdir -p ~/Migration

# Copy folders
for folder in Documents Desktop Downloads Pictures Movies Music; do
    [ -d "/Users/$OLDUSER/$folder" ] && sudo cp -R "/Users/$OLDUSER/$folder" ~/Migration/
done

# Fix permissions
sudo chown -R $(whoami):staff ~/Migration/

echo "✅ Done! Files in ~/Migration/"

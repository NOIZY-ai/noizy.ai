#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  MAIL MANAGER PRO — ALFRED WORKFLOW GENERATOR
#  Generates Alfred workflow for mail operations
#═══════════════════════════════════════════════════════════════════════════════

INSTALL_DIR="${MAIL_MANAGER_HOME:-${HOME}/scripts/mail_manager_pro}"
WORKFLOW_DIR="${HOME}/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/user.mailmanager.pro"

mkdir -p "$WORKFLOW_DIR"

# Create workflow info.plist
cat > "$WORKFLOW_DIR/info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>bundleid</key>
    <string>user.mailmanager.pro</string>
    <key>name</key>
    <string>Mail Manager Pro</string>
    <key>description</key>
    <string>Mail organization and backup management</string>
    <key>uidata</key>
    <dict>
        <key>0BB91C42-E00B-46C7-9D57-FF8299374666</key>
        <dict>
            <key>xpos</key>
            <integer>50</integer>
            <key>ypos</key>
            <integer>10</integer>
        </dict>
    </dict>
    <key>version</key>
    <string>3.5.0</string>
</dict>
</plist>
PLIST

# Create script filter for backup operations
cat > "$WORKFLOW_DIR/backup-script.sh" << 'SCRIPT'
#!/bin/bash
MAIL_MANAGER_HOME="${HOME}/scripts/mail_manager_pro"
source "${MAIL_MANAGER_HOME}/lib/backup.sh"

query="$1"

case "$query" in
    create)
        cmd_backup_create
        echo '{"items":[{"title":"✓ Backup Created","subtitle":"New backup has been created"}]}'
        ;;
    list)
        echo '{"items":['
        first=true
        cmd_backup_list | while read -r line; do
            if [[ "$first" == true ]]; then
                first=false
            else
                echo ","
            fi
            echo "{\"title\":\"$line\",\"arg\":\"$line\"}"
        done
        echo ']}'
        ;;
    *)
        echo '{"items":['
        echo '{"title":"Create Backup","subtitle":"Create new backup now","arg":"create"},'
        echo '{"title":"List Backups","subtitle":"Show all available backups","arg":"list"},'
        echo '{"title":"Restore Latest","subtitle":"Restore from latest backup","arg":"restore"}'
        echo ']}'
        ;;
esac
SCRIPT

chmod +x "$WORKFLOW_DIR/backup-script.sh"

echo "Alfred workflow created at: $WORKFLOW_DIR"

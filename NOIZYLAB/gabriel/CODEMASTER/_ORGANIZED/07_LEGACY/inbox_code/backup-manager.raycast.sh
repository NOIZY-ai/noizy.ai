#!/usr/bin/env bash
# @raycast.schemaVersion 1
# @raycast.title Mail Manager - Backup Operations
# @raycast.description Create, list, and restore mail backups
# @raycast.mode fullOutput
# @raycast.packageName Mail Manager Pro
#
# @raycast.argument1 { "type": "dropdown", "values": ["create", "list", "restore"], "description": "Operation" }
# @raycast.argument2 { "type": "text", "description": "Backup name (for restore)", "optional": true }

MAIL_MANAGER_HOME="${HOME}/scripts/mail_manager_pro"
source "${MAIL_MANAGER_HOME}/lib/backup.sh"

operation="$1"
backup_name="$2"

case "$operation" in
    create)
        echo "Creating backup..."
        cmd_backup_create
        ;;
    list)
        echo "Available backups:"
        cmd_backup_list
        ;;
    restore)
        if [[ -z "$backup_name" ]]; then
            echo "Error: Backup name required"
            exit 1
        fi
        echo "Restoring: $backup_name"
        cmd_backup_restore "$backup_name"
        ;;
esac


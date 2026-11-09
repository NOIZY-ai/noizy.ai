#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  MAIL MANAGER PRO — EXAMPLE: BACKUP OPERATIONS
#  Comprehensive backup examples
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

MAIL_MANAGER_HOME="${HOME}/scripts/mail_manager_pro"

# Colors
BOLD='\033[1m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo ""
echo -e "${BOLD}${CYAN}MAIL MANAGER PRO — BACKUP EXAMPLES${RESET}"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Example 1: Create a basic backup
echo -e "${BOLD}Example 1: Create a Basic Backup${RESET}"
echo ""
echo "Command: mailmgr backup create"
echo ""
echo "This will:"
echo "  • Backup your mail configuration"
echo "  • Capture current folder structure"
echo "  • Store mail rules"
echo "  • Create SHA256 checksum"
echo "  • Save to ~/scripts/mail_manager_pro/backups/"
echo ""
echo "Run it:"
echo -e "  ${CYAN}mailmgr backup create${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 2: List available backups
echo -e "${BOLD}Example 2: List All Backups${RESET}"
echo ""
echo "Command: mailmgr backup list"
echo ""
echo "This shows:"
echo "  • Backup filename"
echo "  • File size"
echo "  • Creation date/time"
echo "  • Latest backup indicator"
echo ""
echo "Run it:"
echo -e "  ${CYAN}mailmgr backup list${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 3: Restore from latest backup
echo -e "${BOLD}Example 3: Restore from Latest Backup${RESET}"
echo ""
echo "Command: mailmgr backup restore"
echo ""
echo "This will:"
echo "  • Verify backup integrity (SHA256)"
echo "  • Create pre-restore safety backup"
echo "  • Restore configuration"
echo "  • Restore folder structure"
echo "  • Restore mail rules"
echo ""
echo "Run it:"
echo -e "  ${CYAN}mailmgr backup restore${RESET}"
echo ""
echo "With confirmation:"
echo -e "  ${CYAN}mailmgr backup restore --yes${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 4: Restore from specific backup
echo -e "${BOLD}Example 4: Restore from Specific Backup${RESET}"
echo ""
echo "Command: mailmgr backup restore backup_v2_20231215_143022"
echo ""
echo "First, list backups to find the name:"
echo -e "  ${CYAN}mailmgr backup list${RESET}"
echo ""
echo "Then restore specific one:"
echo -e "  ${CYAN}mailmgr backup restore backup_v2_20231215_143022${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 5: Dry-run (preview changes)
echo -e "${BOLD}Example 5: Dry-Run Mode (Preview)${RESET}"
echo ""
echo "Preview backup without making changes:"
echo -e "  ${CYAN}DRY_RUN=1 mailmgr backup create${RESET}"
echo ""
echo "Preview restore without making changes:"
echo -e "  ${CYAN}DRY_RUN=1 mailmgr backup restore${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 6: Prune old backups
echo -e "${BOLD}Example 6: Delete Old Backups${RESET}"
echo ""
echo "Keep only 10 most recent backups:"
echo -e "  ${CYAN}mailmgr backup prune 10${RESET}"
echo ""
echo "Keep only 5 most recent backups:"
echo -e "  ${CYAN}mailmgr backup prune 5${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 7: Custom backup location
echo -e "${BOLD}Example 7: Custom Backup Location${RESET}"
echo ""
echo "Backup to external drive:"
echo -e "  ${CYAN}BACKUP_DIR=/Volumes/backup mailmgr backup create${RESET}"
echo ""
echo "Backup to cloud-synced folder:"
echo -e "  ${CYAN}BACKUP_DIR=~/Dropbox/mailmgr-backups mailmgr backup create${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 8: Automated backups
echo -e "${BOLD}Example 8: Automated Backups (Scheduler)${RESET}"
echo ""
echo "Enable scheduler for automatic backups:"
echo -e "  ${CYAN}mailmgr schedule enable${RESET}"
echo ""
echo "Configure schedule in config.yaml:"
echo "  scheduler:"
echo "    enabled: true"
echo "    tasks:"
echo "      - name: \"backup\""
echo "        schedule: \"0 2 * * 0\"  # Weekly Sunday @ 2 AM"
echo ""
echo "Check scheduler status:"
echo -e "  ${CYAN}mailmgr schedule status${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 9: Cloud backup
echo -e "${BOLD}Example 9: Sync Backups to Cloud${RESET}"
echo ""
echo "Amazon S3:"
echo -e "  ${CYAN}aws s3 sync ~/scripts/mail_manager_pro/backups s3://mybucket/mailmgr${RESET}"
echo ""
echo "Google Drive (with rclone):"
echo -e "  ${CYAN}rclone sync ~/scripts/mail_manager_pro/backups gdrive:mailmgr${RESET}"
echo ""
echo "Dropbox:"
echo -e "  ${CYAN}cp ~/scripts/mail_manager_pro/backups/* ~/Dropbox/mailmgr-backups/${RESET}"
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Example 10: Monitor backups
echo -e "${BOLD}Example 10: Monitor Backups${RESET}"
echo ""
echo "View latest backup:"
echo -e "  ${CYAN}ls -lah ~/scripts/mail_manager_pro/backups/backup_latest.tar.gz${RESET}"
echo ""
echo "Check backup size:"
echo -e "  ${CYAN}du -h ~/scripts/mail_manager_pro/backups/backup_*.tar.gz${RESET}"
echo ""
echo "See backup manifest:"
echo -e "  ${CYAN}cat ~/scripts/mail_manager_pro/backups/backup_latest.manifest.json${RESET}"
echo ""
echo "Verify checksum:"
echo -e "  ${CYAN}shasum -a 256 ~/scripts/mail_manager_pro/backups/backup_v2_*.tar.gz${RESET}"
echo ""

echo ""
echo -e "${GREEN}✓ Examples shown above${RESET}"
echo ""
echo "For more information:"
echo -e "  ${CYAN}mailmgr --help${RESET}"
echo -e "  ${CYAN}cat ~/scripts/mail_manager_pro/docs/COMPLETE_GUIDE.md${RESET}"
echo ""

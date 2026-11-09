#!/bin/bash
################################################################################
#  🕒 GABRIEL Network Backup - Automated Scheduler Setup
#  Helps configure automated weekly backups via cron
################################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/System/NetworkBackups/dgs1210_backup.py"
CRON_LOG="/tmp/gabriel_network_backup.log"

# Banner
show_banner() {
    clear
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║                                                            ║${NC}"
    echo -e "${MAGENTA}║  ${BOLD}🕒 GABRIEL Network Backup - Cron Setup v1.0${NC}${MAGENTA}          ║${NC}"
    echo -e "${MAGENTA}║                                                            ║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Check if script exists
check_backup_script() {
    if [ ! -f "$BACKUP_SCRIPT" ]; then
        echo -e "${RED}❌ Backup script not found: $BACKUP_SCRIPT${NC}"
        exit 1
    fi
    
    if [ ! -x "$BACKUP_SCRIPT" ]; then
        echo -e "${YELLOW}⚠️  Making backup script executable...${NC}"
        chmod +x "$BACKUP_SCRIPT"
    fi
    
    echo -e "${GREEN}✅ Backup script found and executable${NC}"
}

# Show current crontab
show_current_cron() {
    echo -e "\n${CYAN}📋 Current Crontab:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if crontab -l 2>/dev/null | grep -q "dgs1210_backup.py"; then
        crontab -l 2>/dev/null | grep "dgs1210_backup.py"
        echo -e "${GREEN}✅ Backup job already configured${NC}"
    else
        echo -e "${YELLOW}⚠️  No backup job found${NC}"
    fi
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Schedule options
show_schedule_options() {
    echo -e "\n${CYAN}${BOLD}📅 Schedule Options:${NC}\n"
    echo -e "  ${GREEN}1.${NC} ${BOLD}Daily at 3 AM${NC}"
    echo -e "     ${BLUE}0 3 * * *${NC}"
    echo -e ""
    echo -e "  ${GREEN}2.${NC} ${BOLD}Weekly (Monday at 3 AM)${NC} ⭐ Recommended"
    echo -e "     ${BLUE}0 3 * * 1${NC}"
    echo -e ""
    echo -e "  ${GREEN}3.${NC} ${BOLD}Twice Weekly (Monday & Thursday at 3 AM)${NC}"
    echo -e "     ${BLUE}0 3 * * 1,4${NC}"
    echo -e ""
    echo -e "  ${GREEN}4.${NC} ${BOLD}Every 12 hours${NC}"
    echo -e "     ${BLUE}0 */12 * * *${NC}"
    echo -e ""
    echo -e "  ${GREEN}5.${NC} ${BOLD}Custom Schedule${NC}"
    echo -e ""
    echo -e "  ${GREEN}6.${NC} ${BOLD}Remove Scheduled Backup${NC}"
    echo -e ""
    echo -e "  ${RED}7.${NC} ${BOLD}Exit${NC}"
    echo ""
}

# Get cron expression from user
get_cron_expression() {
    local choice=$1
    
    case $choice in
        1)
            echo "0 3 * * *"
            ;;
        2)
            echo "0 3 * * 1"
            ;;
        3)
            echo "0 3 * * 1,4"
            ;;
        4)
            echo "0 */12 * * *"
            ;;
        5)
            echo -e "\n${CYAN}Enter custom cron expression:${NC}"
            echo -e "${YELLOW}Format: minute hour day-of-month month day-of-week${NC}"
            echo -e "${YELLOW}Example: 30 14 * * 5  (Every Friday at 2:30 PM)${NC}"
            read -p "Cron expression: " custom_cron
            echo "$custom_cron"
            ;;
        *)
            echo ""
            ;;
    esac
}

# Add cron job
add_cron_job() {
    local cron_expression=$1
    local python_path=$(which python3)
    
    # Create cron command
    local cron_command="$cron_expression $python_path $BACKUP_SCRIPT >> $CRON_LOG 2>&1"
    
    echo -e "\n${CYAN}➕ Adding cron job...${NC}"
    echo -e "${BLUE}Expression: $cron_expression${NC}"
    echo -e "${BLUE}Script:     $BACKUP_SCRIPT${NC}"
    echo -e "${BLUE}Log:        $CRON_LOG${NC}"
    
    # Backup current crontab
    crontab -l 2>/dev/null > /tmp/crontab_backup.txt
    
    # Remove any existing dgs1210_backup entries
    crontab -l 2>/dev/null | grep -v "dgs1210_backup.py" > /tmp/new_crontab.txt
    
    # Add new entry
    echo "$cron_command" >> /tmp/new_crontab.txt
    
    # Install new crontab
    crontab /tmp/new_crontab.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Cron job added successfully!${NC}"
        echo ""
        echo -e "${CYAN}Scheduled backups will run:${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        explain_cron "$cron_expression"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to add cron job${NC}"
        # Restore backup
        crontab /tmp/crontab_backup.txt 2>/dev/null
        return 1
    fi
}

# Remove cron job
remove_cron_job() {
    echo -e "\n${CYAN}🗑️  Removing backup cron job...${NC}"
    
    if ! crontab -l 2>/dev/null | grep -q "dgs1210_backup.py"; then
        echo -e "${YELLOW}⚠️  No backup job found to remove${NC}"
        return 1
    fi
    
    # Backup current crontab
    crontab -l 2>/dev/null > /tmp/crontab_backup.txt
    
    # Remove dgs1210_backup entries
    crontab -l 2>/dev/null | grep -v "dgs1210_backup.py" > /tmp/new_crontab.txt
    
    # Install new crontab
    crontab /tmp/new_crontab.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Cron job removed successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to remove cron job${NC}"
        crontab /tmp/crontab_backup.txt 2>/dev/null
        return 1
    fi
}

# Explain cron expression in plain English
explain_cron() {
    local cron=$1
    
    case $cron in
        "0 3 * * *")
            echo -e "   ${GREEN}📅 Every day at 3:00 AM${NC}"
            ;;
        "0 3 * * 1")
            echo -e "   ${GREEN}📅 Every Monday at 3:00 AM${NC}"
            ;;
        "0 3 * * 1,4")
            echo -e "   ${GREEN}📅 Every Monday and Thursday at 3:00 AM${NC}"
            ;;
        "0 */12 * * *")
            echo -e "   ${GREEN}📅 Every 12 hours (midnight and noon)${NC}"
            ;;
        *)
            echo -e "   ${GREEN}📅 Custom schedule: $cron${NC}"
            ;;
    esac
}

# Test backup manually
test_backup() {
    echo -e "\n${CYAN}🧪 Testing backup manually...${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    python3 "$BACKUP_SCRIPT"
    
    if [ $? -eq 0 ]; then
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}✅ Test backup completed successfully${NC}"
    else
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}❌ Test backup failed${NC}"
    fi
}

# View logs
view_logs() {
    echo -e "\n${CYAN}📜 Recent Backup Logs:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ -f "$CRON_LOG" ]; then
        tail -30 "$CRON_LOG"
    else
        echo -e "${YELLOW}⚠️  No logs found yet (backup hasn't run)${NC}"
    fi
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Show next run time
show_next_run() {
    echo -e "\n${CYAN}⏰ Next Scheduled Run:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # This requires 'cron' package with 'next' utility (not standard)
    # Fallback to showing current schedule
    if crontab -l 2>/dev/null | grep -q "dgs1210_backup.py"; then
        local cron_line=$(crontab -l 2>/dev/null | grep "dgs1210_backup.py")
        echo -e "${GREEN}Current schedule:${NC}"
        echo -e "   $cron_line"
        echo ""
        echo -e "${YELLOW}💡 Tip: Check system logs for actual run times${NC}"
        echo -e "   ${BLUE}macOS: grep CRON /var/log/system.log | tail${NC}"
        echo -e "   ${BLUE}Linux: grep CRON /var/log/syslog | tail${NC}"
    else
        echo -e "${YELLOW}⚠️  No scheduled backup job found${NC}"
    fi
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Main menu
main_menu() {
    while true; do
        show_banner
        check_backup_script
        show_current_cron
        show_schedule_options
        
        read -p "$(echo -e ${BOLD}Select option [1-7]: ${NC})" choice
        
        case $choice in
            1|2|3|4|5)
                cron_expr=$(get_cron_expression $choice)
                if [ ! -z "$cron_expr" ]; then
                    add_cron_job "$cron_expr"
                    echo ""
                    read -p "Press Enter to continue..."
                fi
                ;;
            6)
                remove_cron_job
                echo ""
                read -p "Press Enter to continue..."
                ;;
            7)
                echo -e "\n${MAGENTA}👋 Done!${NC}\n"
                exit 0
                ;;
            test)
                test_backup
                echo ""
                read -p "Press Enter to continue..."
                ;;
            logs)
                view_logs
                echo ""
                read -p "Press Enter to continue..."
                ;;
            next)
                show_next_run
                echo ""
                read -p "Press Enter to continue..."
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                sleep 1
                ;;
        esac
    done
}

# Run main menu
main_menu

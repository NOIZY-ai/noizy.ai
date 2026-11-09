#!/usr/bin/env bash
# Webhook integrations for Slack, Discord, Teams, custom endpoints

send_webhook() {
    local service="$1"
    local message="$2"
    local url="$3"
    
    case "$service" in
        slack)
            curl -s -X POST "$url" \
                -H "Content-Type: application/json" \
                -d "{\"text\":\"$message\"}" > /dev/null
            ;;
        discord)
            curl -s -X POST "$url" \
                -H "Content-Type: application/json" \
                -d "{\"content\":\"$message\"}" > /dev/null
            ;;
        teams)
            curl -s -X POST "$url" \
                -H "Content-Type: application/json" \
                -d "{\"text\":\"$message\"}" > /dev/null
            ;;
        *)
            curl -s -X POST "$url" \
                -H "Content-Type: application/json" \
                -d "{\"message\":\"$message\"}" > /dev/null
            ;;
    esac
}

webhook_on_backup_complete() {
    local backup_file="$1"
    local size=$(du -h "$backup_file" | cut -f1)
    
    local message="✅ Backup completed: $backup_file ($size)"
    
    [[ -n "${SLACK_WEBHOOK:-}" ]] && send_webhook slack "$message" "$SLACK_WEBHOOK"
    [[ -n "${DISCORD_WEBHOOK:-}" ]] && send_webhook discord "$message" "$DISCORD_WEBHOOK"
    [[ -n "${TEAMS_WEBHOOK:-}" ]] && send_webhook teams "$message" "$TEAMS_WEBHOOK"
}

webhook_on_error() {
    local error_msg="$1"
    
    local message="❌ Error: $error_msg"
    
    [[ -n "${SLACK_WEBHOOK:-}" ]] && send_webhook slack "$message" "$SLACK_WEBHOOK"
    [[ -n "${DISCORD_WEBHOOK:-}" ]] && send_webhook discord "$message" "$DISCORD_WEBHOOK"
}


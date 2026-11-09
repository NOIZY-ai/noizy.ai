#!/usr/bin/env bash
# Scheduler management for macOS (launchd) and Linux (cron)

LAUNCHD_LABEL="com.mailmanager.pro"
LAUNCHD_PLIST="${HOME}/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"

cmd_schedule_status() {
    echo "[*] Scheduler Status"
    
    if [[ "$OSTYPE" == darwin* ]]; then
        echo ""
        echo "launchd Agent:"
        if [[ -f "$LAUNCHD_PLIST" ]]; then
            if launchctl list 2>/dev/null | grep -q "$LAUNCHD_LABEL"; then
                echo "  ✓ Status: Running"
                echo "  📄 Plist: $LAUNCHD_PLIST"
            else
                echo "  ○ Status: Installed but not running"
            fi
        else
            echo "  ✗ Status: Not installed"
        fi
    fi
    
    echo ""
    echo "Scheduled Tasks:"
    echo "  • sync_folders: daily @ 06:00"
    echo "  • process_rules: every 5 minutes"
    echo "  • backup: weekly (Sunday) @ 02:00"
    echo "  • health_check: hourly"
}

cmd_schedule_enable() {
    echo "[*] Enabling scheduler..."
    
    if [[ "$OSTYPE" == darwin* ]]; then
        mkdir -p "$(dirname "$LAUNCHD_PLIST")"
        
        cat > "$LAUNCHD_PLIST" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LAUNCHD_LABEL}</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>${INSTALL_DIR}/bin/mailmgr</string>
        <string>schedule</string>
        <string>run</string>
    </array>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>${INSTALL_DIR}/logs/scheduler.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>MAIL_MANAGER_HOME</key>
        <string>${INSTALL_DIR}</string>
    </dict>
</dict>
</plist>
PLIST
        
        launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true
        launchctl load "$LAUNCHD_PLIST"
        success "Scheduler enabled"
    fi
}

cmd_schedule_disable() {
    echo "[*] Disabling scheduler..."
    
    if [[ "$OSTYPE" == darwin* ]] && [[ -f "$LAUNCHD_PLIST" ]]; then
        launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true
        rm -f "$LAUNCHD_PLIST"
        success "Scheduler disabled"
    fi
}


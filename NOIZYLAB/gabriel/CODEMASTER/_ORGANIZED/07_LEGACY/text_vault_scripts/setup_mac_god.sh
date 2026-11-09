#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🖥️  GOD MAC STUDIO SETUP SCRIPT v1.0
# ═══════════════════════════════════════════════════════════════════════════
#  Purpose: Configure Mac Studio (GOD) with OneDrive, SMB, and Auto-Sync
#  Created: November 11, 2025
#  System: macOS (Mac Studio)
#  Features: OneDrive Installation, SMB Server, Automated Sync, Folder Actions
# ═══════════════════════════════════════════════════════════════════════════

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
MAC_NAME="MacStudio"
ONEDRIVE_FOLDER="$HOME/OneDrive"
SYNC_FOLDER="$HOME/OneDriveSync"
PROJECTS_FOLDER="$HOME/Projects"
LOG_FILE="$HOME/Library/Logs/mac_god_setup.log"

# ═══════════════════════════════════════════════════════════════════════════
#  ASCII ART BANNER
# ═══════════════════════════════════════════════════════════════════════════

print_banner() {
    clear
    echo -e "${CYAN}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🖥️  GOD MAC STUDIO SETUP v1.0                                  ║
║                                                                   ║
║   Configure: OneDrive • SMB • Auto-Sync • Folder Actions         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
#  LOGGING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
    log "SUCCESS: $1"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    log "ERROR: $1"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    log "WARNING: $1"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
    log "INFO: $1"
}

section() {
    echo ""
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║  $1${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
    log "SECTION: $1"
}

# ═══════════════════════════════════════════════════════════════════════════
#  SYSTEM CHECKS
# ═══════════════════════════════════════════════════════════════════════════

check_macos() {
    section "CHECKING SYSTEM REQUIREMENTS"
    
    # Check if macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        error "This script is for macOS only!"
        exit 1
    fi
    success "macOS detected"
    
    # Check macOS version
    OS_VERSION=$(sw_vers -productVersion)
    info "macOS Version: $OS_VERSION"
    
    # Check if Mac Studio (optional - for info)
    MODEL=$(sysctl -n hw.model)
    info "Hardware Model: $MODEL"
}

check_homebrew() {
    info "Checking for Homebrew..."
    
    if ! command -v brew &> /dev/null; then
        warning "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        
        if command -v brew &> /dev/null; then
            success "Homebrew installed successfully"
        else
            error "Homebrew installation failed"
            exit 1
        fi
    else
        success "Homebrew already installed"
        BREW_VERSION=$(brew --version | head -n1)
        info "$BREW_VERSION"
    fi
}

check_sudo() {
    info "Checking sudo access..."
    if sudo -v; then
        success "Sudo access granted"
        # Keep sudo alive
        while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &
    else
        error "Sudo access required"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  ONEDRIVE INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════

install_onedrive() {
    section "INSTALLING ONEDRIVE"
    
    # Check if already installed
    if [ -d "/Applications/OneDrive.app" ]; then
        warning "OneDrive already installed"
        info "Location: /Applications/OneDrive.app"
        
        # Check if running
        if pgrep -x "OneDrive" > /dev/null; then
            success "OneDrive is running"
        else
            warning "OneDrive not running. Launch it from Applications."
        fi
    else
        info "Installing OneDrive via Homebrew..."
        if brew install --cask onedrive; then
            success "OneDrive installed successfully"
            info "Launch OneDrive from Applications to sign in"
        else
            error "OneDrive installation failed"
            return 1
        fi
    fi
    
    # Create OneDriveSync folder
    if [ ! -d "$SYNC_FOLDER" ]; then
        mkdir -p "$SYNC_FOLDER"
        success "Created OneDriveSync folder: $SYNC_FOLDER"
    else
        info "OneDriveSync folder already exists"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  SMB SERVER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

configure_smb() {
    section "CONFIGURING SMB SHARING"
    
    info "Setting NetBIOS name to: $MAC_NAME"
    sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server NetBIOSName -string "$MAC_NAME"
    
    if [ $? -eq 0 ]; then
        success "NetBIOS name set successfully"
    else
        error "Failed to set NetBIOS name"
        return 1
    fi
    
    info "Restarting SMB server..."
    sudo launchctl kickstart -k system/com.apple.smbd
    
    if [ $? -eq 0 ]; then
        success "SMB server restarted"
    else
        warning "SMB server restart may have failed (check manually)"
    fi
    
    # Enable File Sharing
    info "Enabling File Sharing..."
    sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.smbd.plist 2>/dev/null
    
    success "SMB configuration complete"
    info "Network name: $MAC_NAME"
    info "Access via: smb://$MAC_NAME or smb://$(ipconfig getifaddr en0)"
}

# ═══════════════════════════════════════════════════════════════════════════
#  SYNC SCRIPT CREATION
# ═══════════════════════════════════════════════════════════════════════════

create_sync_script() {
    section "CREATING AUTO-SYNC SCRIPT"
    
    SYNC_SCRIPT="$HOME/Library/Scripts/sync_to_onedrive.sh"
    mkdir -p "$HOME/Library/Scripts"
    
    cat > "$SYNC_SCRIPT" << 'SYNCEOF'
#!/bin/bash
# Auto-sync Projects to OneDriveSync

SOURCE="$HOME/Projects"
DEST="$HOME/OneDriveSync"
LOG="$HOME/Library/Logs/onedrive_sync.log"

timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

log() {
    echo "[$(timestamp)] $1" >> "$LOG"
}

# Create destination if needed
mkdir -p "$DEST"

# Sync using rsync (preserves timestamps, only copies changes)
log "Starting sync: $SOURCE -> $DEST"

rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    "$SOURCE/" "$DEST/"

if [ $? -eq 0 ]; then
    log "Sync completed successfully"
else
    log "Sync failed with error code $?"
fi
SYNCEOF
    
    chmod +x "$SYNC_SCRIPT"
    success "Sync script created: $SYNC_SCRIPT"
    
    # Test the sync script
    info "Testing sync script..."
    if [ -d "$PROJECTS_FOLDER" ]; then
        bash "$SYNC_SCRIPT"
        if [ $? -eq 0 ]; then
            success "Sync test successful"
        else
            warning "Sync test failed (check if Projects folder exists)"
        fi
    else
        warning "Projects folder doesn't exist yet: $PROJECTS_FOLDER"
        info "Create it and files will sync automatically"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  LAUNCHD AUTOMATION (Better than Folder Actions)
# ═══════════════════════════════════════════════════════════════════════════

create_launchd_service() {
    section "SETTING UP AUTO-SYNC SERVICE"
    
    PLIST_NAME="com.macstudio.onedrive.sync"
    PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
    
    mkdir -p "$HOME/Library/LaunchAgents"
    
    cat > "$PLIST_PATH" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$HOME/Library/Scripts/sync_to_onedrive.sh</string>
    </array>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/onedrive_sync_error.log</string>
    
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/onedrive_sync_out.log</string>
</dict>
</plist>
PLISTEOF
    
    success "LaunchAgent created: $PLIST_PATH"
    info "Sync interval: Every 5 minutes"
    
    # Load the service
    info "Loading LaunchAgent..."
    launchctl unload "$PLIST_PATH" 2>/dev/null
    launchctl load "$PLIST_PATH"
    
    if [ $? -eq 0 ]; then
        success "Auto-sync service started"
        info "Projects will sync every 5 minutes automatically"
    else
        error "Failed to start service"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  FOLDER ACTIONS (ALTERNATIVE)
# ═══════════════════════════════════════════════════════════════════════════

create_folder_action() {
    section "CREATING FOLDER ACTION (OPTIONAL)"
    
    info "To create Folder Action manually:"
    echo ""
    echo "1. Open Automator"
    echo "2. Choose 'Folder Action'"
    echo "3. Set folder to: $PROJECTS_FOLDER"
    echo "4. Add 'Run Shell Script' action:"
    echo "   bash $HOME/Library/Scripts/sync_to_onedrive.sh"
    echo "5. Save as 'OneDrive Sync'"
    echo ""
    
    warning "Folder Actions require manual setup via Automator"
    info "LaunchAgent (above) is recommended instead"
}

# ═══════════════════════════════════════════════════════════════════════════
#  SYSTEM PREFERENCES & TWEAKS
# ═══════════════════════════════════════════════════════════════════════════

configure_system_preferences() {
    section "CONFIGURING SYSTEM PREFERENCES"
    
    # Set computer name
    info "Setting computer name to: $MAC_NAME"
    sudo scutil --set ComputerName "$MAC_NAME"
    sudo scutil --set HostName "$MAC_NAME"
    sudo scutil --set LocalHostName "$MAC_NAME"
    success "Computer name set"
    
    # Disable sleep for better server operation
    info "Adjusting power settings..."
    sudo pmset -c sleep 0
    sudo pmset -c displaysleep 10
    sudo pmset -c disksleep 0
    success "Power settings optimized for server use"
    
    # Enable Remote Login (SSH) - optional
    read -p "Enable SSH (Remote Login)? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo systemsetup -setremotelogin on
        success "SSH enabled"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  STATUS & VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════

show_status() {
    section "SYSTEM STATUS"
    
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Mac Studio (GOD) Configuration Summary                  ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Computer Name
    echo -e "${GREEN}🖥️  Computer Name:${NC}"
    echo "   Network: $(scutil --get ComputerName)"
    echo "   Local: $(scutil --get LocalHostName)"
    echo ""
    
    # OneDrive
    echo -e "${GREEN}☁️  OneDrive:${NC}"
    if [ -d "/Applications/OneDrive.app" ]; then
        echo "   ✅ Installed: /Applications/OneDrive.app"
        if pgrep -x "OneDrive" > /dev/null; then
            echo "   ✅ Status: Running"
        else
            echo "   ⚠️  Status: Not running (launch manually)"
        fi
    else
        echo "   ❌ Not installed"
    fi
    echo ""
    
    # SMB Sharing
    echo -e "${GREEN}🌐 SMB Sharing:${NC}"
    echo "   NetBIOS Name: $(defaults read /Library/Preferences/SystemConfiguration/com.apple.smb.server NetBIOSName 2>/dev/null || echo 'Not set')"
    echo "   Access: smb://$MAC_NAME"
    IP_ADDRESS=$(ipconfig getifaddr en0 2>/dev/null || echo "Not connected")
    echo "   IP Address: $IP_ADDRESS"
    echo ""
    
    # Sync Status
    echo -e "${GREEN}🔄 Auto-Sync:${NC}"
    echo "   Source: $PROJECTS_FOLDER"
    echo "   Destination: $SYNC_FOLDER"
    echo "   Script: $HOME/Library/Scripts/sync_to_onedrive.sh"
    
    PLIST_NAME="com.macstudio.onedrive.sync"
    if launchctl list | grep -q "$PLIST_NAME"; then
        echo "   ✅ Service: Active (syncs every 5 minutes)"
    else
        echo "   ⚠️  Service: Not loaded"
    fi
    echo ""
    
    # Folders
    echo -e "${GREEN}📁 Folders:${NC}"
    [ -d "$PROJECTS_FOLDER" ] && echo "   ✅ $PROJECTS_FOLDER" || echo "   ⚠️  $PROJECTS_FOLDER (not created yet)"
    [ -d "$SYNC_FOLDER" ] && echo "   ✅ $SYNC_FOLDER" || echo "   ❌ $SYNC_FOLDER"
    [ -d "$ONEDRIVE_FOLDER" ] && echo "   ✅ $ONEDRIVE_FOLDER" || echo "   ⚠️  $ONEDRIVE_FOLDER (sign in to OneDrive)"
    echo ""
    
    # Logs
    echo -e "${GREEN}📋 Logs:${NC}"
    echo "   Setup: $LOG_FILE"
    echo "   Sync: $HOME/Library/Logs/onedrive_sync.log"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  MENU SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

show_menu() {
    print_banner
    echo -e "${CYAN}Select setup options:${NC}"
    echo ""
    echo "  1. Full Setup (All features)"
    echo "  2. Install OneDrive only"
    echo "  3. Configure SMB only"
    echo "  4. Setup Auto-Sync only"
    echo "  5. System Preferences only"
    echo "  6. Show Status"
    echo "  7. Test Sync Now"
    echo "  8. View Logs"
    echo "  9. Exit"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

main() {
    print_banner
    
    # Log start
    log "=========================================="
    log "GOD Mac Setup Script Started"
    log "=========================================="
    
    while true; do
        show_menu
        read -p "Enter choice [1-9]: " choice
        
        case $choice in
            1)
                check_macos
                check_homebrew
                check_sudo
                install_onedrive
                configure_smb
                create_sync_script
                create_launchd_service
                configure_system_preferences
                show_status
                success "Full setup complete!"
                ;;
            2)
                check_macos
                check_homebrew
                install_onedrive
                ;;
            3)
                check_macos
                check_sudo
                configure_smb
                ;;
            4)
                check_macos
                create_sync_script
                create_launchd_service
                ;;
            5)
                check_macos
                check_sudo
                configure_system_preferences
                ;;
            6)
                show_status
                ;;
            7)
                if [ -f "$HOME/Library/Scripts/sync_to_onedrive.sh" ]; then
                    info "Running sync now..."
                    bash "$HOME/Library/Scripts/sync_to_onedrive.sh"
                    success "Sync complete"
                else
                    error "Sync script not found. Run option 4 first."
                fi
                ;;
            8)
                info "Recent sync logs:"
                echo ""
                if [ -f "$HOME/Library/Logs/onedrive_sync.log" ]; then
                    tail -20 "$HOME/Library/Logs/onedrive_sync.log"
                else
                    warning "No sync logs found"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            9)
                echo ""
                success "Setup complete. Goodbye!"
                log "Script exited normally"
                exit 0
                ;;
            *)
                error "Invalid option: $choice"
                sleep 2
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main

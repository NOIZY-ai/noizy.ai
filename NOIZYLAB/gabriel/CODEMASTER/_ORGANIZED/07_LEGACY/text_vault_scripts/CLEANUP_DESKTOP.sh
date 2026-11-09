#!/bin/bash
# CLEANUP_DESKTOP.sh
# Clean up desktop and organize all setup files

clear

echo "🧹 CLEANING UP DESKTOP..."
echo ""

# Create organized folders
SETUP_DIR="$HOME/NOIZYLAB/beats_email_setup"
SCRIPTS_DIR="$SETUP_DIR/scripts"
GUIDES_DIR="$SETUP_DIR/guides"

mkdir -p "$SCRIPTS_DIR"
mkdir -p "$GUIDES_DIR"

# Move all Beats scripts
echo "📦 Moving Beats scripts..."
[ -f "$HOME/Desktop/BEATS_MASTER_SETUP.command" ] && mv "$HOME/Desktop/BEATS_MASTER_SETUP.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/ADVANCED_BEATS_SETUP.command" ] && mv "$HOME/Desktop/ADVANCED_BEATS_SETUP.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/OPTIMIZE_BEATS.command" ] && mv "$HOME/Desktop/OPTIMIZE_BEATS.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/TEST_BEATS_MIC.command" ] && mv "$HOME/Desktop/TEST_BEATS_MIC.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/CALIBRATE_BEATS.command" ] && mv "$HOME/Desktop/CALIBRATE_BEATS.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/AUTO_CALIBRATE_BEATS.command" ] && mv "$HOME/Desktop/AUTO_CALIBRATE_BEATS.command" "$SCRIPTS_DIR/"

# Move all email scripts
echo "📦 Moving email scripts..."
[ -f "$HOME/Desktop/EMAIL_MASTER.command" ] && mv "$HOME/Desktop/EMAIL_MASTER.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/ULTIMATE_VOICE_SETUP.command" ] && mv "$HOME/Desktop/ULTIMATE_VOICE_SETUP.command" "$SCRIPTS_DIR/"

# Move all automation scripts
echo "📦 Moving automation scripts..."
[ -f "$HOME/Desktop/ULTIMATE_MASTER_X10000.command" ] && mv "$HOME/Desktop/ULTIMATE_MASTER_X10000.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/SMART_STATUS_MONITOR.command" ] && mv "$HOME/Desktop/SMART_STATUS_MONITOR.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/AUTO_CONFIGURATOR.command" ] && mv "$HOME/Desktop/AUTO_CONFIGURATOR.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/VOICE_COMMAND_HELPER.command" ] && mv "$HOME/Desktop/VOICE_COMMAND_HELPER.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/INSTANT_ACTIONS.command" ] && mv "$HOME/Desktop/INSTANT_ACTIONS.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/ULTIMATE_LAUNCHER.command" ] && mv "$HOME/Desktop/ULTIMATE_LAUNCHER.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/INTELLIGENT_WIZARD.command" ] && mv "$HOME/Desktop/INTELLIGENT_WIZARD.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/ONE_CLICK_EVERYTHING.command" ] && mv "$HOME/Desktop/ONE_CLICK_EVERYTHING.command" "$SCRIPTS_DIR/"
[ -f "$HOME/Desktop/QUICK_LAUNCH_ALL.command" ] && mv "$HOME/Desktop/QUICK_LAUNCH_ALL.command" "$SCRIPTS_DIR/"

# Move all guides
echo "📦 Moving guides..."
[ -f "$HOME/Desktop/BEATS_OPTIMIZATION.txt" ] && mv "$HOME/Desktop/BEATS_OPTIMIZATION.txt" "$GUIDES_DIR/"
[ -f "$HOME/Desktop/ADVANCED_BEATS_GUIDE.txt" ] && mv "$HOME/Desktop/ADVANCED_BEATS_GUIDE.txt" "$GUIDES_DIR/"
[ -f "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt" ] && mv "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt" "$GUIDES_DIR/"
[ -f "$HOME/Desktop/BEATS_STATUS.txt" ] && mv "$HOME/Desktop/BEATS_STATUS.txt" "$GUIDES_DIR/"
[ -f "$HOME/Desktop/MASTER_SUMMARY.txt" ] && mv "$HOME/Desktop/MASTER_SUMMARY.txt" "$GUIDES_DIR/"

# Create clean launcher on desktop
cat > "$HOME/Desktop/BEATS_EMAIL_SETUP.command" << 'LAUNCHER_EOF'
#!/bin/bash
# BEATS_EMAIL_SETUP - Clean launcher

SETUP_DIR="$HOME/NOIZYLAB/beats_email_setup"

# Open all settings
open "x-apple.systempreferences:com.apple.preference.sound"
open "x-apple.systempreferences:com.apple.preference.universalaccess"

# Open all email pages
open "https://dash.cloudflare.com/login"
open "https://app.improvmx.com/"
open "https://mail.google.com/mail/u/0/#settings/accounts"

# Open quick guide
open "$SETUP_DIR/guides/VOICE_COMMANDS_QUICK.txt" 2>/dev/null

echo "✅ Everything launched!"
say "Beats and email setup launched. All pages are open."
LAUNCHER_EOF

chmod +x "$HOME/Desktop/BEATS_EMAIL_SETUP.command"

# Create quick access folder launcher
cat > "$HOME/Desktop/OPEN_SETUP_FOLDER.command" << 'FOLDER_EOF'
#!/bin/bash
open "$HOME/NOIZYLAB/beats_email_setup"
FOLDER_EOF

chmod +x "$HOME/Desktop/OPEN_SETUP_FOLDER.command"

echo ""
echo "✅ DESKTOP CLEANED UP!"
echo ""
echo "📋 WHAT'S ON DESKTOP NOW:"
echo "   ✅ BEATS_EMAIL_SETUP.command - Launch everything"
echo "   ✅ OPEN_SETUP_FOLDER.command - Open setup folder"
echo ""
echo "📁 ALL FILES MOVED TO:"
echo "   $SETUP_DIR"
echo "   ├── scripts/ (all .command files)"
echo "   └── guides/ (all .txt files)"
echo ""


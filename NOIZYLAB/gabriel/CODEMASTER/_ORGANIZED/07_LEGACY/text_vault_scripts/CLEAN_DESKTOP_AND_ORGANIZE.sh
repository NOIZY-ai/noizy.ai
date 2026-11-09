#!/bin/bash
# CLEAN_DESKTOP_AND_ORGANIZE.sh
# Clean desktop and organize all files

clear

echo "🧹 CLEANING DESKTOP AND ORGANIZING FILES..."
echo ""

SETUP_DIR="$HOME/NOIZYLAB/email_setup"
GUIDES_DIR="$SETUP_DIR/guides"
SCRIPTS_DIR="$SETUP_DIR/scripts"

mkdir -p "$GUIDES_DIR"
mkdir -p "$SCRIPTS_DIR"

# Move all text files
echo "📦 Moving text files..."
cd "$HOME/Desktop"
for file in *.txt; do
    [ -f "$file" ] && mv "$file" "$GUIDES_DIR/" 2>/dev/null
done

# Move all command files
echo "📦 Moving command files..."
for file in *.command; do
    [ -f "$file" ] && mv "$file" "$SCRIPTS_DIR/" 2>/dev/null
done

# Create one simple launcher on desktop
cat > "$HOME/Desktop/EMAIL_SETUP.command" << 'LAUNCHER_EOF'
#!/bin/bash
# Email Setup Launcher

SETUP_DIR="$HOME/NOIZYLAB/email_setup"

# Open all necessary pages
open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/home/domains"
open "https://app.improvmx.com/"
open "https://mail.google.com/mail/u/0/#settings/accounts"

# Open main guides
open "$SETUP_DIR/guides/NOIZYLAB_CA_GUIDE.txt" 2>/dev/null
open "$SETUP_DIR/guides/NUMBERED_GUIDE.txt" 2>/dev/null

echo "✅ All pages and guides opened!"
say "Email setup launcher complete. All pages and guides are open."
LAUNCHER_EOF

chmod +x "$HOME/Desktop/EMAIL_SETUP.command"

# Create folder launcher
cat > "$HOME/Desktop/OPEN_EMAIL_SETUP_FOLDER.command" << 'FOLDER_EOF'
#!/bin/bash
open "$HOME/NOIZYLAB/email_setup"
FOLDER_EOF

chmod +x "$HOME/Desktop/OPEN_EMAIL_SETUP_FOLDER.command"

echo ""
echo "✅ DESKTOP CLEANED!"
echo ""
echo "📋 WHAT'S ON DESKTOP NOW:"
echo "   ✅ EMAIL_SETUP.command - Launch everything"
echo "   ✅ OPEN_EMAIL_SETUP_FOLDER.command - Open setup folder"
echo ""
echo "📁 ALL FILES MOVED TO:"
echo "   $SETUP_DIR/guides/ (all .txt files)"
echo "   $SETUP_DIR/scripts/ (all .command files)"
echo ""

say "Desktop cleaned. All files moved to organized folder. Only two launchers remain on desktop."


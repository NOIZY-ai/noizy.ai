#!/bin/bash
# SET_NO_DESKTOP_RULE.sh
# Set up rule to never save to desktop

clear

echo "📋 Setting up NO DESKTOP rule..."
echo ""

# Create organized folders structure
ORGANIZED_DIR="$HOME/Documents/NOIZYLAB"
mkdir -p "$ORGANIZED_DIR/guides"
mkdir -p "$ORGANIZED_DIR/scripts"
mkdir -p "$ORGANIZED_DIR/email_setup/guides"
mkdir -p "$ORGANIZED_DIR/email_setup/scripts"
mkdir -p "$ORGANIZED_DIR/scripts_collection/executed"
mkdir -p "$ORGANIZED_DIR/scripts_collection/email_setup"
mkdir -p "$ORGANIZED_DIR/scripts_collection/beats_setup"
mkdir -p "$ORGANIZED_DIR/scripts_collection/automation"
mkdir -p "$ORGANIZED_DIR/scripts_collection/utilities"

# Create reminder file
cat > "$ORGANIZED_DIR/NO_DESKTOP_RULE.txt" << 'RULE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📋 NO DESKTOP RULE - ALWAYS FOLLOW                              ║
╚══════════════════════════════════════════════════════════════════════╝

NEVER SAVE ANYTHING TO DESKTOP!

══════════════════════════════════════════════════════════════════════

ORGANIZED LOCATIONS:
────────────────────

Guides/Documentation:
  → $HOME/Documents/NOIZYLAB/guides/
  → $HOME/Documents/NOIZYLAB/email_setup/guides/

Scripts:
  → $HOME/Documents/NOIZYLAB/scripts/
  → $HOME/Documents/NOIZYLAB/email_setup/scripts/

Executed Scripts:
  → $HOME/Documents/NOIZYLAB/scripts_collection/executed/
  → $HOME/Documents/NOIZYLAB/scripts_collection/email_setup/
  → $HOME/Documents/NOIZYLAB/scripts_collection/beats_setup/
  → $HOME/Documents/NOIZYLAB/scripts_collection/automation/
  → $HOME/Documents/NOIZYLAB/scripts_collection/utilities/

══════════════════════════════════════════════════════════════════════

RULES:
──────

✅ ALWAYS save to organized folders
✅ NEVER save to Desktop
✅ Move any files created to proper folders immediately
✅ Use organized structure

══════════════════════════════════════════════════════════════════════
RULE_EOF

echo "✅ NO DESKTOP RULE set up!"
echo ""
echo "📁 ORGANIZED FOLDERS:"
echo "   Guides: $ORGANIZED_DIR/guides/"
echo "   Scripts: $ORGANIZED_DIR/scripts/"
echo "   Email Setup: $ORGANIZED_DIR/email_setup/"
echo "   Script Collection: $ORGANIZED_DIR/scripts_collection/"
echo ""
echo "✅ I will NEVER save to Desktop again!"
echo "   All files will go to organized folders."
echo ""

say "No desktop rule set up. All files will be saved to organized folders in Documents. Nothing will be saved to desktop."


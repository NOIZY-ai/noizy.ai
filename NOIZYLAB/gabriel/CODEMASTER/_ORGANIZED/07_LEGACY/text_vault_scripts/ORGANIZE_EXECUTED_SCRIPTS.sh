#!/bin/bash
# ORGANIZE_EXECUTED_SCRIPTS.sh
# Move executed scripts to proper collection folder

clear

echo "📁 Setting up script organization system..."
echo ""

# Create collection folders
COLLECTION_DIR="$HOME/Documents/NOIZYLAB/scripts_collection"
mkdir -p "$COLLECTION_DIR/executed"
mkdir -p "$COLLECTION_DIR/email_setup"
mkdir -p "$COLLECTION_DIR/beats_setup"
mkdir -p "$COLLECTION_DIR/automation"
mkdir -p "$COLLECTION_DIR/utilities"

echo "✅ Collection folders created: $COLLECTION_DIR"
echo ""

# Create script organizer function
cat > "$HOME/Documents/NOIZYLAB/scripts_collection/ORGANIZE_SCRIPT.sh" << 'ORG_EOF'
#!/bin/bash
# ORGANIZE_SCRIPT.sh - Move executed script to collection

SCRIPT_PATH="$1"
CATEGORY="${2:-executed}"

if [ -z "$SCRIPT_PATH" ]; then
    echo "Usage: ORGANIZE_SCRIPT.sh <script_path> [category]"
    exit 1
fi

COLLECTION_DIR="$HOME/Documents/NOIZYLAB/scripts_collection"
TARGET_DIR="$COLLECTION_DIR/$CATEGORY"

mkdir -p "$TARGET_DIR"

if [ -f "$SCRIPT_PATH" ]; then
    SCRIPT_NAME=$(basename "$SCRIPT_PATH")
    mv "$SCRIPT_PATH" "$TARGET_DIR/$SCRIPT_NAME"
    echo "✅ Moved $SCRIPT_NAME to $TARGET_DIR/"
else
    echo "❌ Script not found: $SCRIPT_PATH"
fi
ORG_EOF

chmod +x "$HOME/Documents/NOIZYLAB/scripts_collection/ORGANIZE_SCRIPT.sh"

# Create auto-organizer wrapper
cat > "$HOME/Documents/NOIZYLAB/scripts_collection/EXECUTE_AND_ORGANIZE.sh" << 'EXEC_ORG_EOF'
#!/bin/bash
# EXECUTE_AND_ORGANIZE.sh - Execute script then move it

SCRIPT_PATH="$1"
CATEGORY="${2:-executed}"

if [ -z "$SCRIPT_PATH" ]; then
    echo "Usage: EXECUTE_AND_ORGANIZE.sh <script_path> [category]"
    exit 1
fi

# Execute the script
echo "🚀 Executing: $SCRIPT_PATH"
bash "$SCRIPT_PATH"

# Move to collection
echo "📁 Organizing script..."
bash "$HOME/Documents/NOIZYLAB/scripts_collection/ORGANIZE_SCRIPT.sh" "$SCRIPT_PATH" "$CATEGORY"

echo "✅ Done!"
EXEC_ORG_EOF

chmod +x "$HOME/Documents/NOIZYLAB/scripts_collection/EXECUTE_AND_ORGANIZE.sh"

echo "✅ Script organization system created!"
echo ""
echo "📁 COLLECTION STRUCTURE:"
echo "   $COLLECTION_DIR/"
echo "   ├── executed/ (general executed scripts)"
echo "   ├── email_setup/ (email setup scripts)"
echo "   ├── beats_setup/ (Beats setup scripts)"
echo "   ├── automation/ (automation scripts)"
echo "   └── utilities/ (utility scripts)"
echo ""
echo "📋 USAGE:"
echo "   bash EXECUTE_AND_ORGANIZE.sh <script> [category]"
echo ""

say "Script organization system created. All executed scripts will be moved to the collection folder automatically."


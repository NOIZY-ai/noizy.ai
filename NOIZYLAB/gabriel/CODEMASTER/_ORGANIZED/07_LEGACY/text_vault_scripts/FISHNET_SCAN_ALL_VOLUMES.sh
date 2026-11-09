#!/bin/bash
# FISHNET SCAN - Find All Lost Code Across All Volumes
# Rob Sonic Protocol | GORUNFREE | MC96

echo "╔════════════════════════════════════════════════════╗"
echo "║  FISHNET SCAN - Finding All Lost Code             ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

REPORT_FILE="$HOME/CODE_MASTER/logs/fishnet_scan_$(date +%Y%m%d_%H%M%S).txt"
RECOVERY_DIR="$HOME/CODE_MASTER/RECOVERED_CODE_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RECOVERY_DIR"
mkdir -p "$HOME/CODE_MASTER/logs"

echo "📄 Report: $REPORT_FILE"
echo "📁 Recovery: $RECOVERY_DIR"
echo ""

echo "=== FISHNET CODE SCAN ===" > "$REPORT_FILE"
echo "Date: $(date)" >> "$REPORT_FILE"
echo "Recovery Directory: $RECOVERY_DIR" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Code file extensions
CODE_EXTENSIONS=(
    ".py" ".js" ".ts" ".jsx" ".tsx"
    ".sh" ".bash" ".zsh" ".fish"
    ".ps1" ".psm1" ".psd1"
    ".java" ".cpp" ".c" ".h" ".hpp"
    ".go" ".rs" ".rb" ".php"
    ".html" ".css" ".scss" ".sass"
    ".json" ".xml" ".yaml" ".yml"
    ".md" ".txt" ".conf" ".config"
    ".sql" ".r" ".m" ".swift"
    ".kt" ".scala" ".clj" ".lua"
)

# PHASE 1: LIST ALL VOLUMES
echo "🔍 PHASE 1: Discovering all volumes..."
echo ""

VOLUMES=()
while IFS= read -r vol; do
    if [ -d "/Volumes/$vol" ] && [ "$vol" != "Macintosh HD" ]; then
        VOLUMES+=("$vol")
        echo "  ✓ Found: /Volumes/$vol"
        echo "Volume: /Volumes/$vol" >> "$REPORT_FILE"
    fi
done < <(ls /Volumes/ 2>/dev/null)

# Also check home directory
VOLUMES+=("HOME")
echo "  ✓ Including: $HOME"
echo ""

echo "=== VOLUMES TO SCAN ===" >> "$REPORT_FILE"
printf '%s\n' "${VOLUMES[@]}" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# PHASE 2: SCAN EACH VOLUME
echo "🔍 PHASE 2: Scanning volumes for code..."
echo ""

TOTAL_FOUND=0

for vol in "${VOLUMES[@]}"; do
    if [ "$vol" = "HOME" ]; then
        SCAN_PATH="$HOME"
        VOL_NAME="HOME"
    else
        SCAN_PATH="/Volumes/$vol"
        VOL_NAME="$vol"
    fi
    
    if [ ! -d "$SCAN_PATH" ]; then
        continue
    fi
    
    echo "📦 Scanning: $VOL_NAME..."
    echo "" >> "$REPORT_FILE"
    echo "=== SCANNING: $VOL_NAME ===" >> "$REPORT_FILE"
    
    # Create recovery subdirectory
    VOL_RECOVERY="$RECOVERY_DIR/$VOL_NAME"
    mkdir -p "$VOL_RECOVERY"
    
    FOUND_COUNT=0
    
    # Scan for code files
    for ext in "${CODE_EXTENSIONS[@]}"; do
        find "$SCAN_PATH" -type f -name "*$ext" \
            -not -path "*/node_modules/*" \
            -not -path "*/.git/*" \
            -not -path "*/Library/*" \
            -not -path "*/Trash/*" \
            -not -path "*/.cache/*" \
            -not -path "*/venv/*" \
            -not -path "*/__pycache__/*" \
            -not -path "*/\.DS_Store" \
            2>/dev/null | while read -r file; do
            
            if [ -f "$file" ] && [ -r "$file" ]; then
                # Get relative path for organization
                REL_PATH=$(echo "$file" | sed "s|^$SCAN_PATH/||")
                DIR_PATH=$(dirname "$REL_PATH")
                
                # Create directory structure in recovery
                if [ "$DIR_PATH" != "." ]; then
                    mkdir -p "$VOL_RECOVERY/$DIR_PATH"
                    DEST="$VOL_RECOVERY/$REL_PATH"
                else
                    DEST="$VOL_RECOVERY/$(basename "$file")"
                fi
                
                # Avoid duplicates
                if [ ! -f "$DEST" ]; then
                    cp "$file" "$DEST" 2>/dev/null
                    if [ $? -eq 0 ]; then
                        FOUND_COUNT=$((FOUND_COUNT + 1))
                        echo "    ✓ $REL_PATH" >> "$REPORT_FILE"
                    fi
                fi
            fi
        done
    done
    
    # Count files in recovery directory
    ACTUAL_COUNT=$(find "$VOL_RECOVERY" -type f 2>/dev/null | wc -l | tr -d ' ')
    TOTAL_FOUND=$((TOTAL_FOUND + ACTUAL_COUNT))
    
    if [ "$ACTUAL_COUNT" -gt 0 ]; then
        echo "  ✓ Found $ACTUAL_COUNT code files"
        echo "Files found: $ACTUAL_COUNT" >> "$REPORT_FILE"
    else
        echo "  ⚠️  No code files found"
    fi
    echo ""
done

# PHASE 3: ORGANIZE RECOVERED CODE
echo "🔍 PHASE 3: Organizing recovered code..."
echo ""

ORGANIZED_DIR="$RECOVERY_DIR/ORGANIZED"
mkdir -p "$ORGANIZED_DIR"/{python,javascript,shell,config,docs,other}

find "$RECOVERY_DIR" -type f -not -path "*/ORGANIZED/*" | while read -r file; do
    ext="${file##*.}"
    filename=$(basename "$file")
    
    case "$ext" in
        py) mv "$file" "$ORGANIZED_DIR/python/" 2>/dev/null || true ;;
        js|jsx|ts|tsx) mv "$file" "$ORGANIZED_DIR/javascript/" 2>/dev/null || true ;;
        sh|bash|zsh|fish) mv "$file" "$ORGANIZED_DIR/shell/" 2>/dev/null || true ;;
        json|yaml|yml|conf|config) mv "$file" "$ORGANIZED_DIR/config/" 2>/dev/null || true ;;
        md|txt) mv "$file" "$ORGANIZED_DIR/docs/" 2>/dev/null || true ;;
        *) mv "$file" "$ORGANIZED_DIR/other/" 2>/dev/null || true ;;
    esac
done

echo "  ✓ Code organized by type"
echo ""

# PHASE 4: CREATE SUMMARY
echo "🔍 PHASE 4: Generating summary..."
echo ""

echo "=== SUMMARY ===" >> "$REPORT_FILE"
echo "Total code files found: $TOTAL_FOUND" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Count by type
echo "Files by type:" >> "$REPORT_FILE"
for dir in python javascript shell config docs other; do
    COUNT=$(find "$ORGANIZED_DIR/$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  $dir: $COUNT" >> "$REPORT_FILE"
done

# PHASE 5: MOVE TO CODE_MASTER
echo "🔍 PHASE 5: Moving to CODE_MASTER..."
echo ""

# Move organized code to CODE_MASTER
if [ -d "$ORGANIZED_DIR/python" ] && [ "$(ls -A $ORGANIZED_DIR/python 2>/dev/null)" ]; then
    cp -r "$ORGANIZED_DIR/python"/* "$HOME/CODE_MASTER/python/" 2>/dev/null || true
    echo "  ✓ Python files moved to CODE_MASTER"
fi

if [ -d "$ORGANIZED_DIR/javascript" ] && [ "$(ls -A $ORGANIZED_DIR/javascript 2>/dev/null)" ]; then
    cp -r "$ORGANIZED_DIR/javascript"/* "$HOME/CODE_MASTER/nodejs/" 2>/dev/null || true
    echo "  ✓ JavaScript files moved to CODE_MASTER"
fi

if [ -d "$ORGANIZED_DIR/shell" ] && [ "$(ls -A $ORGANIZED_DIR/shell 2>/dev/null)" ]; then
    cp -r "$ORGANIZED_DIR/shell"/* "$HOME/CODE_MASTER/scripts/" 2>/dev/null || true
    echo "  ✓ Shell scripts moved to CODE_MASTER"
fi

if [ -d "$ORGANIZED_DIR/config" ] && [ "$(ls -A $ORGANIZED_DIR/config 2>/dev/null)" ]; then
    cp -r "$ORGANIZED_DIR/config"/* "$HOME/CODE_MASTER/config/" 2>/dev/null || true
    echo "  ✓ Config files moved to CODE_MASTER"
fi

echo ""

# SUMMARY
echo "╔════════════════════════════════════════════════════╗"
echo "║  FISHNET SCAN COMPLETE                            ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📊 RESULTS:"
echo "  Total code files found: $TOTAL_FOUND"
echo "  Recovery location: $RECOVERY_DIR"
echo "  Report: $REPORT_FILE"
echo ""
echo "✅ All lost code recovered and organized!"
echo ""


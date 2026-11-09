#!/bin/bash
# RESET LOGITECH OPTIONS - Wake Up & Reset
# Rob Sonic Protocol | GORUNFREE

echo "╔════════════════════════════════════════════════════╗"
echo "║  RESETTING LOGITECH OPTIONS                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# PHASE 1: KILL LOGITECH OPTIONS
echo "🔍 PHASE 1: Stopping Logitech Options..."
pkill -9 "LogiMgr" 2>/dev/null || true
pkill -9 "LogiOptions" 2>/dev/null || true
pkill -9 "LogiOptionsDaemon" 2>/dev/null || true
sleep 2
echo "  ✓ Logitech Options stopped"
echo ""

# PHASE 2: REMOVE CACHES
echo "🔍 PHASE 2: Clearing Logitech caches..."
rm -rf ~/Library/Caches/com.logitech.LogiOptions* 2>/dev/null
rm -rf ~/Library/Caches/Logitech* 2>/dev/null
rm -rf ~/Library/Application\ Support/Logitech/LogiOptions* 2>/dev/null
echo "  ✓ Caches cleared"
echo ""

# PHASE 3: RESET PREFERENCES
echo "🔍 PHASE 3: Resetting preferences..."
rm -rf ~/Library/Preferences/com.logitech.LogiOptions* 2>/dev/null
rm -rf ~/Library/Preferences/Logitech* 2>/dev/null
echo "  ✓ Preferences reset"
echo ""

# PHASE 4: RESTART LOGITECH OPTIONS
echo "🔍 PHASE 4: Restarting Logitech Options..."

# Try to find Logitech Options
LOGITECH_PATHS=(
    "/Applications/LogiOptions.app"
    "/Applications/Logitech Options.app"
    "/Applications/Utilities/LogiOptions.app"
)

FOUND=false
for path in "${LOGITECH_PATHS[@]}"; do
    if [ -d "$path" ]; then
        echo "  ✓ Found: $path"
        open "$path"
        FOUND=true
        break
    fi
done

if [ "$FOUND" = false ]; then
    echo "  ⚠️  Logitech Options not found in standard locations"
    echo "  Searching for Logitech Options..."
    
    # Search for it
    find /Applications -name "*Logitech*" -o -name "*Logi*" 2>/dev/null | head -5 | while read app; do
        if [ -d "$app" ]; then
            echo "  Found: $app"
            open "$app"
            FOUND=true
        fi
    done
fi

if [ "$FOUND" = true ]; then
    echo "  ✓ Logitech Options launched"
else
    echo "  ⚠️  Could not find Logitech Options"
    echo "  Please install or launch manually"
fi

echo ""

# PHASE 5: WAIT AND VERIFY
echo "🔍 PHASE 5: Verifying restart..."
sleep 5

if pgrep -f "LogiOptions" > /dev/null; then
    echo "  ✓ Logitech Options is running"
else
    echo "  ⚠️  Logitech Options may not have started"
    echo "  Try launching manually from Applications"
fi

echo ""

# PHASE 6: RESET BLUETOOTH (if needed)
echo "🔍 PHASE 6: Resetting Bluetooth connection..."
echo "  To reset Bluetooth:"
echo "  1. Open System Settings → Bluetooth"
echo "  2. Remove your Logitech device"
echo "  3. Put device in pairing mode"
echo "  4. Re-pair the device"
echo ""

# SUMMARY
echo "╔════════════════════════════════════════════════════╗"
echo "║  RESET COMPLETE                                   ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "✅ Logitech Options reset complete!"
echo ""
echo "📋 NEXT STEPS:"
echo "  1. Logitech Options should be launching"
echo "  2. Reconfigure your device settings"
echo "  3. If device not working, reset Bluetooth connection"
echo ""


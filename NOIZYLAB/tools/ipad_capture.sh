#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# iPad Audio Capture for Audio Hijack
# Routes iPad audio via AirPlay to M2 Ultra "God" for recording
# ═══════════════════════════════════════════════════════════════════════════════

SESSION_NAME="iPad to God (M2 Ultra)"
OUTPUT_DIR="$HOME/NOIZYLAB/audio/ipad_captures"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

case "$1" in
    start)
        osascript <<EOF
tell application "Audio Hijack"
    activate
    set targetSession to first session whose name is "$SESSION_NAME"
    if not (running of targetSession) then
        start targetSession
        delay 0.5
        display notification "iPad audio capture started" with title "NOIZY Audio" sound name "Glass"
    end if
end tell
EOF
        echo "✓ iPad capture STARTED"
        echo "  Recording to: $OUTPUT_DIR"
        ;;

    stop)
        osascript <<EOF
tell application "Audio Hijack"
    set targetSession to first session whose name is "$SESSION_NAME"
    if (running of targetSession) then
        stop targetSession
        display notification "iPad audio capture stopped" with title "NOIZY Audio" sound name "Blow"
    end if
end tell
EOF
        echo "✓ iPad capture STOPPED"
        # List recent captures
        echo "  Recent captures:"
        ls -lt "$OUTPUT_DIR" 2>/dev/null | head -5
        ;;

    status)
        STATUS=$(osascript -e "tell application \"Audio Hijack\" to return running of (first session whose name is \"$SESSION_NAME\")")
        if [ "$STATUS" = "true" ]; then
            echo "● RECORDING - iPad capture is active"
        else
            echo "○ STOPPED - iPad capture is inactive"
        fi
        ;;

    list)
        echo "Recent iPad captures:"
        echo "─────────────────────"
        ls -lth "$OUTPUT_DIR" 2>/dev/null | head -10
        ;;

    create)
        # Create the Audio Hijack session via AppleScript
        osascript <<EOF
tell application "Audio Hijack"
    activate

    -- Create new session
    set newSession to make new session with properties {name:"$SESSION_NAME"}

    display dialog "Session '$SESSION_NAME' created. Please configure manually:

1. Add 'System Audio' source block
2. Add '10-Band EQ' effect (optional)
3. Add 'Recorder' block:
   • Format: WAV 24-bit 48kHz
   • Folder: $OUTPUT_DIR
4. Add 'Output Device' block

Then connect: Source → EQ → Recorder → Output" buttons {"OK"} default button "OK"
end tell
EOF
        echo "✓ Session template created in Audio Hijack"
        ;;

    *)
        echo "═══════════════════════════════════════════════════════════════"
        echo "  NOIZY iPad Audio Capture"
        echo "  Routes iPad → AirPlay → M2 Ultra God → Recording"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        echo "  Usage: $0 {start|stop|status|list|create}"
        echo ""
        echo "  Commands:"
        echo "    start   - Begin recording iPad audio"
        echo "    stop    - Stop recording"
        echo "    status  - Check if capture is running"
        echo "    list    - Show recent captures"
        echo "    create  - Create Audio Hijack session template"
        echo ""
        echo "  Setup:"
        echo "    1. Enable AirPlay Receiver on Mac"
        echo "    2. Run: $0 create"
        echo "    3. Configure session in Audio Hijack"
        echo "    4. Connect iPad via AirPlay to 'God'"
        echo "    5. Run: $0 start"
        echo ""
        exit 1
        ;;
esac

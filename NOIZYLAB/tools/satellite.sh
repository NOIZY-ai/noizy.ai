#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  NOIZY SATELLITE COMMAND CENTER
#  iPad & iPhone → M2 Ultra "God" via Rogue Amoeba Satellite
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Satellite provides pro-quality audio routing from iOS to Mac:
#  • Lower latency than AirPlay
#  • Full quality audio (up to 48kHz/24-bit)
#  • App-specific audio capture
#  • Multiple iOS devices simultaneously
#
# ═══════════════════════════════════════════════════════════════════════════════

OUTPUT_DIR="$HOME/NOIZYLAB/audio/satellite_captures"
IPAD_SESSION="NOIZY iPad Satellite"
IPHONE_SESSION="NOIZY iPhone Satellite"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Ensure directories exist
mkdir -p "$OUTPUT_DIR/ipad"
mkdir -p "$OUTPUT_DIR/iphone"
mkdir -p "$OUTPUT_DIR/mixed"

print_header() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║         NOIZY SATELLITE COMMAND CENTER                          ║"
    echo "║         iPad & iPhone → M2 Ultra 'God'                          ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_satellite_devices() {
    echo -e "${BLUE}Scanning for Satellite devices...${NC}"
    osascript <<'EOF'
tell application "Audio Hijack"
    set deviceList to {}
    set allSources to available sources
    repeat with src in allSources
        if name of src contains "Satellite" then
            set end of deviceList to name of src
        end if
    end repeat
    return deviceList
end tell
EOF
}

create_ipad_session() {
    echo -e "${YELLOW}Creating iPad Satellite session in Audio Hijack...${NC}"
    osascript <<EOF
tell application "Audio Hijack"
    activate

    -- Check if session exists
    set sessionExists to false
    repeat with s in sessions
        if name of s is "$IPAD_SESSION" then
            set sessionExists to true
            exit repeat
        end if
    end repeat

    if not sessionExists then
        set newSession to make new session with properties {name:"$IPAD_SESSION"}
        display notification "Created iPad Satellite session" with title "NOIZY Audio"
    end if

    display dialog "iPad Satellite Session Ready!

Configure in Audio Hijack:
━━━━━━━━━━━━━━━━━━━━━━━━━
1. Source: 'Satellite' (select iPad when connected)
2. Add: 10-Band EQ (voice enhancement)
3. Add: Recorder
   • WAV 24-bit 48kHz
   • Folder: $OUTPUT_DIR/ipad/
4. Add: Output Device (monitor)

On iPad:
━━━━━━━━
1. Install 'Satellite' from App Store
2. Open Satellite
3. Select audio source (Mic, App, etc.)
4. Tap your Mac name to connect" buttons {"OK"} default button "OK"
end tell
EOF
    echo -e "${GREEN}✓ iPad session created${NC}"
}

create_iphone_session() {
    echo -e "${YELLOW}Creating iPhone Satellite session in Audio Hijack...${NC}"
    osascript <<EOF
tell application "Audio Hijack"
    activate

    -- Check if session exists
    set sessionExists to false
    repeat with s in sessions
        if name of s is "$IPHONE_SESSION" then
            set sessionExists to true
            exit repeat
        end if
    end repeat

    if not sessionExists then
        set newSession to make new session with properties {name:"$IPHONE_SESSION"}
        display notification "Created iPhone Satellite session" with title "NOIZY Audio"
    end if

    display dialog "iPhone Satellite Session Ready!

Configure in Audio Hijack:
━━━━━━━━━━━━━━━━━━━━━━━━━
1. Source: 'Satellite' (select iPhone when connected)
2. Add: 10-Band EQ (voice enhancement)
3. Add: Recorder
   • WAV 24-bit 48kHz
   • Folder: $OUTPUT_DIR/iphone/
4. Add: Output Device (monitor)

On iPhone:
━━━━━━━━━━
1. Install 'Satellite' from App Store
2. Open Satellite
3. Select audio source (Mic, App, etc.)
4. Tap your Mac name to connect" buttons {"OK"} default button "OK"
end tell
EOF
    echo -e "${GREEN}✓ iPhone session created${NC}"
}

start_ipad() {
    echo -e "${GREEN}Starting iPad Satellite capture...${NC}"
    osascript <<EOF
tell application "Audio Hijack"
    set targetSession to first session whose name is "$IPAD_SESSION"
    if not (running of targetSession) then
        start targetSession
        display notification "iPad Satellite capture started" with title "NOIZY Audio" sound name "Glass"
    end if
end tell
EOF
    echo -e "${GREEN}✓ iPad capture ACTIVE${NC}"
    echo -e "  Recording to: ${CYAN}$OUTPUT_DIR/ipad/${NC}"
}

start_iphone() {
    echo -e "${GREEN}Starting iPhone Satellite capture...${NC}"
    osascript <<EOF
tell application "Audio Hijack"
    set targetSession to first session whose name is "$IPHONE_SESSION"
    if not (running of targetSession) then
        start targetSession
        display notification "iPhone Satellite capture started" with title "NOIZY Audio" sound name "Glass"
    end if
end tell
EOF
    echo -e "${GREEN}✓ iPhone capture ACTIVE${NC}"
    echo -e "  Recording to: ${CYAN}$OUTPUT_DIR/iphone/${NC}"
}

start_both() {
    echo -e "${GREEN}Starting BOTH Satellite captures...${NC}"
    osascript <<EOF
tell application "Audio Hijack"
    -- Start iPad
    try
        set ipadSession to first session whose name is "$IPAD_SESSION"
        if not (running of ipadSession) then
            start ipadSession
        end if
    end try

    -- Start iPhone
    try
        set iphoneSession to first session whose name is "$IPHONE_SESSION"
        if not (running of iphoneSession) then
            start iphoneSession
        end if
    end try

    display notification "Both Satellite captures started" with title "NOIZY Audio" sound name "Glass"
end tell
EOF
    echo -e "${GREEN}✓ iPad + iPhone captures ACTIVE${NC}"
}

stop_all() {
    echo -e "${YELLOW}Stopping all Satellite captures...${NC}"
    osascript <<EOF
tell application "Audio Hijack"
    try
        stop (first session whose name is "$IPAD_SESSION")
    end try
    try
        stop (first session whose name is "$IPHONE_SESSION")
    end try
    display notification "Satellite captures stopped" with title "NOIZY Audio" sound name "Blow"
end tell
EOF
    echo -e "${GREEN}✓ All captures STOPPED${NC}"
}

status() {
    echo -e "${BLUE}Checking Satellite status...${NC}"
    echo ""

    IPAD_STATUS=$(osascript -e "tell application \"Audio Hijack\" to return running of (first session whose name is \"$IPAD_SESSION\")" 2>/dev/null || echo "not found")
    IPHONE_STATUS=$(osascript -e "tell application \"Audio Hijack\" to return running of (first session whose name is \"$IPHONE_SESSION\")" 2>/dev/null || echo "not found")

    if [ "$IPAD_STATUS" = "true" ]; then
        echo -e "  iPad:   ${GREEN}● RECORDING${NC}"
    elif [ "$IPAD_STATUS" = "false" ]; then
        echo -e "  iPad:   ${YELLOW}○ Ready${NC}"
    else
        echo -e "  iPad:   ${RED}✗ Session not found${NC}"
    fi

    if [ "$IPHONE_STATUS" = "true" ]; then
        echo -e "  iPhone: ${GREEN}● RECORDING${NC}"
    elif [ "$IPHONE_STATUS" = "false" ]; then
        echo -e "  iPhone: ${YELLOW}○ Ready${NC}"
    else
        echo -e "  iPhone: ${RED}✗ Session not found${NC}"
    fi

    echo ""
    echo -e "${BLUE}Connected Satellite devices:${NC}"
    check_satellite_devices
}

list_captures() {
    echo -e "${BLUE}Recent Satellite Captures:${NC}"
    echo ""
    echo -e "${CYAN}iPad Captures:${NC}"
    ls -lth "$OUTPUT_DIR/ipad" 2>/dev/null | head -5 || echo "  (none)"
    echo ""
    echo -e "${CYAN}iPhone Captures:${NC}"
    ls -lth "$OUTPUT_DIR/iphone" 2>/dev/null | head -5 || echo "  (none)"
    echo ""
    echo -e "${CYAN}Mixed Captures:${NC}"
    ls -lth "$OUTPUT_DIR/mixed" 2>/dev/null | head -5 || echo "  (none)"
}

show_help() {
    print_header
    echo "Usage: $0 <command>"
    echo ""
    echo -e "${CYAN}Setup Commands:${NC}"
    echo "  setup-ipad      Create iPad Satellite session"
    echo "  setup-iphone    Create iPhone Satellite session"
    echo "  setup-both      Create both sessions"
    echo ""
    echo -e "${CYAN}Recording Commands:${NC}"
    echo "  ipad            Start iPad capture"
    echo "  iphone          Start iPhone capture"
    echo "  both            Start both captures"
    echo "  stop            Stop all captures"
    echo ""
    echo -e "${CYAN}Info Commands:${NC}"
    echo "  status          Show capture status"
    echo "  devices         List connected Satellite devices"
    echo "  list            Show recent captures"
    echo ""
    echo -e "${CYAN}iOS Setup:${NC}"
    echo "  1. Install 'Satellite' from App Store on iPad/iPhone"
    echo "  2. Open Satellite app"
    echo "  3. Select audio source (Microphone, specific app, etc.)"
    echo "  4. Tap your Mac's name to connect"
    echo "  5. Run: $0 setup-ipad (or setup-iphone)"
    echo "  6. Configure session in Audio Hijack"
    echo "  7. Run: $0 ipad (or iphone, or both)"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

case "$1" in
    setup-ipad)
        create_ipad_session
        ;;
    setup-iphone)
        create_iphone_session
        ;;
    setup-both)
        create_ipad_session
        create_iphone_session
        ;;
    ipad)
        start_ipad
        ;;
    iphone)
        start_iphone
        ;;
    both)
        start_both
        ;;
    stop)
        stop_all
        ;;
    status)
        print_header
        status
        ;;
    devices)
        print_header
        check_satellite_devices
        ;;
    list)
        print_header
        list_captures
        ;;
    *)
        show_help
        ;;
esac

#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  NOIZY STUDIO COMMAND CENTER
#  Master Control for the Complete Audio Production Pipeline
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Hardware:
#  • M2 Ultra Mac Studio "God" (192GB) - Master Hub
#  • MacBook Pro (16GB) - Mobile/Windsurf/Cascade
#  • iPad Pro 12.9" (2nd Gen) - Portable Voice
#  • iPhone 15 Pro Max - Field Capture
#  • Neumann Microphone - Primary Voice
#
#  Software:
#  • Logic Pro X - DAW
#  • Audio Hijack - Routing
#  • Satellite - iOS Audio
#  • Windsurf + Cascade - AI Integration
#
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

NOIZY_HOME="$HOME/NOIZYLAB"
AUDIO_DIR="$NOIZY_HOME/audio"
STUDIO_DIR="$NOIZY_HOME/studio"

# Session names
SESSION_IPAD="NOIZY iPad Satellite"
SESSION_IPHONE="NOIZY iPhone Satellite"
SESSION_DUAL="NOIZY Dual Satellite"
SESSION_NEUMANN="NOIZY Neumann Master"
SESSION_MACBOOK="NOIZY MacBook Relay"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║     ███╗   ██╗ ██████╗ ██╗███████╗██╗   ██╗    ███████╗████████╗██╗   ██╗ ║
    ║     ████╗  ██║██╔═══██╗██║╚══███╔╝╚██╗ ██╔╝    ██╔════╝╚══██╔══╝██║   ██║ ║
    ║     ██╔██╗ ██║██║   ██║██║  ███╔╝  ╚████╔╝     ███████╗   ██║   ██║   ██║ ║
    ║     ██║╚██╗██║██║   ██║██║ ███╔╝    ╚██╔╝      ╚════██║   ██║   ██║   ██║ ║
    ║     ██║ ╚████║╚██████╔╝██║███████╗   ██║       ███████║   ██║   ╚██████╔╝ ║
    ║     ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝       ╚══════╝   ╚═╝    ╚═════╝  ║
    ║                                                                           ║
    ║     M2 Ultra "God" │ iPad Pro 12.9 │ iPhone 15 Pro Max │ Neumann │ Logic  ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

print_section() {
    echo -e "\n${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}  $1${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

ensure_directories() {
    mkdir -p "$AUDIO_DIR/satellite_captures/ipad"
    mkdir -p "$AUDIO_DIR/satellite_captures/iphone"
    mkdir -p "$AUDIO_DIR/satellite_captures/mixed"
    mkdir -p "$AUDIO_DIR/neumann"
    mkdir -p "$AUDIO_DIR/logic_exports"
    mkdir -p "$AUDIO_DIR/transcripts"
    mkdir -p "$AUDIO_DIR/talespin"
    mkdir -p "$AUDIO_DIR/masters"
}

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIO HIJACK CONTROL
# ═══════════════════════════════════════════════════════════════════════════════

create_all_sessions() {
    print_section "CREATING AUDIO HIJACK SESSIONS"

    osascript << 'EOF'
tell application "Audio Hijack"
    activate

    -- Create sessions if they don't exist
    set sessionNames to {"NOIZY iPad Satellite", "NOIZY iPhone Satellite", "NOIZY Dual Satellite", "NOIZY Neumann Master", "NOIZY MacBook Relay"}

    repeat with sessionName in sessionNames
        set sessionExists to false
        repeat with s in sessions
            if name of s is sessionName then
                set sessionExists to true
                exit repeat
            end if
        end repeat

        if not sessionExists then
            make new session with properties {name:sessionName}
        end if
    end repeat

    display notification "All NOIZY sessions ready" with title "NOIZY Studio"
end tell
EOF

    echo -e "${GREEN}✓ Sessions created:${NC}"
    echo "  • $SESSION_IPAD"
    echo "  • $SESSION_IPHONE"
    echo "  • $SESSION_DUAL"
    echo "  • $SESSION_NEUMANN"
    echo "  • $SESSION_MACBOOK"
}

start_session() {
    local session_name="$1"
    osascript -e "tell application \"Audio Hijack\" to start (first session whose name is \"$session_name\")" 2>/dev/null || true
}

stop_session() {
    local session_name="$1"
    osascript -e "tell application \"Audio Hijack\" to stop (first session whose name is \"$session_name\")" 2>/dev/null || true
}

session_status() {
    local session_name="$1"
    osascript -e "tell application \"Audio Hijack\" to return running of (first session whose name is \"$session_name\")" 2>/dev/null || echo "not found"
}

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIC PRO X CONTROL
# ═══════════════════════════════════════════════════════════════════════════════

open_logic() {
    print_section "OPENING LOGIC PRO X"
    osascript -e 'tell application "Logic Pro X" to activate'
    echo -e "${GREEN}✓ Logic Pro X activated${NC}"
}

create_logic_session() {
    print_section "CREATING NEW LOGIC SESSION"

    local session_name="${1:-NOIZY_Session_$(date +%Y%m%d_%H%M%S)}"

    osascript << EOF
tell application "Logic Pro X"
    activate
    delay 1

    -- Create new project (user will configure via Logic's interface)
    display dialog "Create new Logic session: $session_name

Recommended settings:
━━━━━━━━━━━━━━━━━━━━━
• Sample Rate: 96 kHz
• Bit Depth: 24-bit
• I/O Buffer: 128 samples

Tracks to create:
━━━━━━━━━━━━━━━━
1. Neumann Vox (Input 1)
2. iPad Satellite (Loopback)
3. iPhone Satellite (Loopback)

Save location:
$HOME/NOIZYLAB/audio/logic_exports/" buttons {"OK"} default button "OK"
end tell
EOF

    echo -e "${GREEN}✓ Logic session dialog shown${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SATELLITE CONTROL
# ═══════════════════════════════════════════════════════════════════════════════

start_satellite_ipad() {
    echo -e "${CYAN}Starting iPad Satellite capture...${NC}"
    start_session "$SESSION_IPAD"
    echo -e "${GREEN}✓ iPad Satellite ACTIVE${NC}"
}

start_satellite_iphone() {
    echo -e "${CYAN}Starting iPhone Satellite capture...${NC}"
    start_session "$SESSION_IPHONE"
    echo -e "${GREEN}✓ iPhone Satellite ACTIVE${NC}"
}

start_satellite_both() {
    echo -e "${CYAN}Starting BOTH Satellite captures...${NC}"
    start_session "$SESSION_IPAD"
    start_session "$SESSION_IPHONE"
    echo -e "${GREEN}✓ Both Satellite captures ACTIVE${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# NEUMANN CONTROL
# ═══════════════════════════════════════════════════════════════════════════════

start_neumann() {
    echo -e "${CYAN}Starting Neumann capture session...${NC}"
    start_session "$SESSION_NEUMANN"
    echo -e "${GREEN}✓ Neumann capture ACTIVE${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# FULL SYSTEM CONTROL
# ═══════════════════════════════════════════════════════════════════════════════

start_all() {
    print_section "STARTING ALL CAPTURE SESSIONS"

    echo -e "${YELLOW}Starting Neumann...${NC}"
    start_session "$SESSION_NEUMANN"

    echo -e "${YELLOW}Starting iPad Satellite...${NC}"
    start_session "$SESSION_IPAD"

    echo -e "${YELLOW}Starting iPhone Satellite...${NC}"
    start_session "$SESSION_IPHONE"

    echo -e "${YELLOW}Starting MacBook Relay...${NC}"
    start_session "$SESSION_MACBOOK"

    osascript -e 'display notification "All capture sessions started" with title "NOIZY Studio" sound name "Glass"'

    echo -e "\n${GREEN}${BOLD}✓ ALL SYSTEMS ACTIVE${NC}"
    echo ""
    echo -e "  ${CYAN}Recording to:${NC}"
    echo "  • Neumann    → $AUDIO_DIR/neumann/"
    echo "  • iPad       → $AUDIO_DIR/satellite_captures/ipad/"
    echo "  • iPhone     → $AUDIO_DIR/satellite_captures/iphone/"
}

stop_all() {
    print_section "STOPPING ALL CAPTURE SESSIONS"

    stop_session "$SESSION_NEUMANN"
    stop_session "$SESSION_IPAD"
    stop_session "$SESSION_IPHONE"
    stop_session "$SESSION_DUAL"
    stop_session "$SESSION_MACBOOK"

    osascript -e 'display notification "All capture sessions stopped" with title "NOIZY Studio" sound name "Blow"'

    echo -e "${GREEN}✓ All sessions STOPPED${NC}"
}

show_status() {
    print_banner
    print_section "SYSTEM STATUS"

    echo -e "\n${BOLD}Audio Hijack Sessions:${NC}"

    # Check each session
    for session in "$SESSION_NEUMANN" "$SESSION_IPAD" "$SESSION_IPHONE" "$SESSION_MACBOOK"; do
        status=$(session_status "$session")
        if [ "$status" = "true" ]; then
            echo -e "  ${GREEN}● RECORDING${NC}  $session"
        elif [ "$status" = "false" ]; then
            echo -e "  ${YELLOW}○ Ready${NC}      $session"
        else
            echo -e "  ${RED}✗ Not Found${NC}  $session"
        fi
    done

    echo -e "\n${BOLD}Connected Satellite Devices:${NC}"
    osascript << 'EOF' 2>/dev/null || echo "  (Unable to query devices)"
tell application "Audio Hijack"
    set deviceList to {}
    try
        set allSources to available sources
        repeat with src in allSources
            if name of src contains "Satellite" or name of src contains "iPad" or name of src contains "iPhone" then
                log "  • " & name of src
            end if
        end repeat
    end try
end tell
EOF

    echo -e "\n${BOLD}Recent Recordings:${NC}"
    echo -e "  ${CYAN}Neumann:${NC}"
    ls -lt "$AUDIO_DIR/neumann" 2>/dev/null | head -3 | tail -2 || echo "    (none)"
    echo -e "  ${CYAN}iPad:${NC}"
    ls -lt "$AUDIO_DIR/satellite_captures/ipad" 2>/dev/null | head -3 | tail -2 || echo "    (none)"
    echo -e "  ${CYAN}iPhone:${NC}"
    ls -lt "$AUDIO_DIR/satellite_captures/iphone" 2>/dev/null | head -3 | tail -2 || echo "    (none)"

    echo -e "\n${BOLD}Logic Pro X:${NC}"
    if pgrep -x "Logic Pro X" > /dev/null 2>&1; then
        echo -e "  ${GREEN}● Running${NC}"
    else
        echo -e "  ${YELLOW}○ Not running${NC}"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# TRANSCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════

transcribe_audio() {
    local audio_file="$1"

    if [ -z "$audio_file" ]; then
        echo -e "${RED}Error: No audio file specified${NC}"
        echo "Usage: $0 transcribe <audio_file>"
        return 1
    fi

    if [ ! -f "$audio_file" ]; then
        echo -e "${RED}Error: File not found: $audio_file${NC}"
        return 1
    fi

    print_section "TRANSCRIBING AUDIO"
    echo "File: $audio_file"

    local output_file="$AUDIO_DIR/transcripts/$(basename "${audio_file%.*}").txt"

    # Check for Whisper
    if command -v whisper &> /dev/null; then
        echo -e "${CYAN}Using Whisper for transcription...${NC}"
        whisper "$audio_file" --model large-v3 --output_dir "$AUDIO_DIR/transcripts" --output_format txt
        echo -e "${GREEN}✓ Transcription complete: $output_file${NC}"
    elif command -v mlx_whisper &> /dev/null; then
        echo -e "${CYAN}Using MLX Whisper for transcription...${NC}"
        mlx_whisper "$audio_file" --model large-v3 > "$output_file"
        echo -e "${GREEN}✓ Transcription complete: $output_file${NC}"
    else
        echo -e "${YELLOW}Whisper not found. Install with:${NC}"
        echo "  pip install openai-whisper"
        echo "  # or for Apple Silicon:"
        echo "  pip install mlx-whisper"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# AI INTEGRATION SETUP
# ═══════════════════════════════════════════════════════════════════════════════

setup_ai_audio() {
    print_section "SETTING UP AI AUDIO INTEGRATION"

    echo -e "${CYAN}Creating Loopback virtual devices for Windsurf/Cascade...${NC}"

    osascript << 'EOF'
tell application "Loopback"
    activate

    display dialog "Create these virtual audio devices in Loopback:

1. 'NOIZY to Windsurf'
   • Pass-through device for voice commands

2. 'NOIZY to Cascade'
   • Pass-through device for AI collaboration

3. 'iPad Satellite Loopback'
   • Capture iPad audio for Logic Pro X

4. 'iPhone Satellite Loopback'
   • Capture iPhone audio for Logic Pro X

These allow audio from any source to feed into your AI tools." buttons {"OK"} default button "OK"
end tell
EOF

    echo -e "${GREEN}✓ Loopback configuration guide shown${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

full_setup() {
    print_banner
    print_section "NOIZY STUDIO FULL SETUP"

    echo -e "${CYAN}Step 1: Creating directories...${NC}"
    ensure_directories
    echo -e "${GREEN}✓ Directories created${NC}"

    echo -e "\n${CYAN}Step 2: Creating Audio Hijack sessions...${NC}"
    create_all_sessions

    echo -e "\n${CYAN}Step 3: Opening configuration guide...${NC}"

    osascript << 'EOF'
display dialog "NOIZY STUDIO SETUP GUIDE
═══════════════════════════════════════════════════

STEP 1: Configure Audio Hijack Sessions
────────────────────────────────────────
Open each session and set up:

• NOIZY Neumann Master
  [Audio Device Input: Your interface] → [Recorder] → [Output]
  Output: ~/NOIZYLAB/audio/neumann/

• NOIZY iPad Satellite
  [Satellite: iPad Pro 12.9] → [EQ] → [Recorder] → [Output]
  Output: ~/NOIZYLAB/audio/satellite_captures/ipad/

• NOIZY iPhone Satellite
  [Satellite: iPhone 15 Pro Max] → [EQ] → [Recorder] → [Output]
  Output: ~/NOIZYLAB/audio/satellite_captures/iphone/

STEP 2: Configure iOS Devices
────────────────────────────────────────
On iPad Pro 12.9 & iPhone 15 Pro Max:
1. Install 'Satellite' from App Store
2. Open Satellite
3. Select audio source (Mic or App)
4. Connect to 'God' (Mac Studio)

STEP 3: Configure Logic Pro X
────────────────────────────────────────
1. Create Loopback devices for Satellite audio
2. Set up audio tracks with inputs from Loopback
3. Apply NOIZY voice processing chain

STEP 4: Test All Connections
────────────────────────────────────────
Run: ./noizy_studio.sh start
Speak into each mic/device
Check levels in Audio Hijack
Verify recordings in output folders" buttons {"Got It!"} default button "Got It!"
EOF

    echo -e "\n${GREEN}${BOLD}✓ SETUP COMPLETE${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Configure sessions in Audio Hijack"
    echo "  2. Install Satellite on iOS devices"
    echo "  3. Run: ./noizy_studio.sh start"
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

show_help() {
    print_banner

    echo -e "${BOLD}Usage:${NC} $0 <command>"
    echo ""
    echo -e "${CYAN}Setup Commands:${NC}"
    echo "  setup              Full studio setup"
    echo "  create-sessions    Create Audio Hijack sessions"
    echo "  setup-ai           Configure AI audio integration"
    echo ""
    echo -e "${CYAN}Recording Commands:${NC}"
    echo "  start              Start ALL capture sessions"
    echo "  stop               Stop ALL capture sessions"
    echo "  neumann            Start Neumann capture only"
    echo "  ipad               Start iPad Satellite only"
    echo "  iphone             Start iPhone Satellite only"
    echo "  satellite          Start both iOS devices"
    echo ""
    echo -e "${CYAN}Logic Pro X:${NC}"
    echo "  logic              Open Logic Pro X"
    echo "  logic-new [name]   Create new Logic session"
    echo ""
    echo -e "${CYAN}Utilities:${NC}"
    echo "  status             Show full system status"
    echo "  transcribe <file>  Transcribe audio with Whisper"
    echo "  list               List recent recordings"
    echo ""
    echo -e "${CYAN}Hardware:${NC}"
    echo "  • M2 Ultra Mac Studio 'God' (192GB)"
    echo "  • MacBook Pro (16GB)"
    echo "  • iPad Pro 12.9\" (2nd Gen)"
    echo "  • iPhone 15 Pro Max"
    echo "  • Neumann Microphone"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

case "$1" in
    setup)
        full_setup
        ;;
    create-sessions)
        create_all_sessions
        ;;
    setup-ai)
        setup_ai_audio
        ;;
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    neumann)
        start_neumann
        ;;
    ipad)
        start_satellite_ipad
        ;;
    iphone)
        start_satellite_iphone
        ;;
    satellite)
        start_satellite_both
        ;;
    logic)
        open_logic
        ;;
    logic-new)
        create_logic_session "$2"
        ;;
    status)
        show_status
        ;;
    transcribe)
        transcribe_audio "$2"
        ;;
    list)
        print_banner
        print_section "RECENT RECORDINGS"
        echo -e "\n${CYAN}Neumann:${NC}"
        ls -lth "$AUDIO_DIR/neumann" 2>/dev/null | head -6 || echo "  (none)"
        echo -e "\n${CYAN}iPad Satellite:${NC}"
        ls -lth "$AUDIO_DIR/satellite_captures/ipad" 2>/dev/null | head -6 || echo "  (none)"
        echo -e "\n${CYAN}iPhone Satellite:${NC}"
        ls -lth "$AUDIO_DIR/satellite_captures/iphone" 2>/dev/null | head -6 || echo "  (none)"
        echo -e "\n${CYAN}Masters:${NC}"
        ls -lth "$AUDIO_DIR/masters" 2>/dev/null | head -6 || echo "  (none)"
        ;;
    *)
        show_help
        ;;
esac

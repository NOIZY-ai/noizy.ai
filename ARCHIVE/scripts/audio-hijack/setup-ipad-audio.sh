#!/bin/bash
# ============================================================================
# NOIZY.AI — iPad → M2 Ultra Audio Hijack Setup
# ============================================================================
# This script automates the setup of Audio Hijack sessions for routing
# audio from your iPad to the M2 Ultra Mac ("God Machine").
#
# Two modes:
#   1. USB (wired)  — iPad connected via USB-C/Lightning cable
#   2. AirPlay (wireless) — iPad streams over local network
#
# Prerequisites:
#   - Audio Hijack 4 (Rogue Amoeba) installed on M2 Ultra
#   - Loopback (Rogue Amoeba) recommended for virtual audio routing
#   - iPad and M2 Ultra on same network (for AirPlay mode)
#   - For USB: iPad connected via cable, trusted on Mac
#
# Usage:
#   ./setup-ipad-audio.sh          # Interactive mode
#   ./setup-ipad-audio.sh usb      # USB mode directly
#   ./setup-ipad-audio.sh airplay  # AirPlay mode directly
#
# Author: Robert Stephen Plowman / NOIZY.AI
# ============================================================================

set -euo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${MAGENTA}"
echo "  ┌─────────────────────────────────────────┐"
echo "  │  NOIZY.AI — iPad → M2 Ultra Audio Setup  │"
echo "  │  Audio Hijack Configuration Script        │"
echo "  └─────────────────────────────────────────┘"
echo -e "${NC}"

# ── Check for Audio Hijack ──────────────────────────────────────────────────
check_audio_hijack() {
  if [ -d "/Applications/Audio Hijack.app" ]; then
    echo -e "${GREEN}✓ Audio Hijack found${NC}"
  else
    echo -e "${YELLOW}⚠ Audio Hijack not found at /Applications/Audio Hijack.app${NC}"
    echo "  Install from: https://rogueamoeba.com/audiohijack/"
    echo "  Continuing with script generation anyway..."
  fi
}

# ── Check for Loopback ──────────────────────────────────────────────────────
check_loopback() {
  if [ -d "/Applications/Loopback.app" ]; then
    echo -e "${GREEN}✓ Loopback found${NC}"
  else
    echo -e "${YELLOW}⚠ Loopback not found (recommended for virtual audio routing)${NC}"
    echo "  Install from: https://rogueamoeba.com/loopback/"
  fi
}

# ── Check for connected iPad (USB) ──────────────────────────────────────────
check_ipad_usb() {
  if command -v system_profiler &>/dev/null; then
    if system_profiler SPUSBDataType 2>/dev/null | grep -qi "iPad"; then
      echo -e "${GREEN}✓ iPad detected via USB${NC}"
      return 0
    else
      echo -e "${YELLOW}⚠ No iPad detected via USB — connect your iPad and trust this Mac${NC}"
      return 1
    fi
  fi
  return 1
}

# ── Generate AppleScript for USB mode ────────────────────────────────────────
generate_usb_applescript() {
  cat > "${SCRIPT_DIR}/ipad-usb-session.applescript" << 'APPLESCRIPT'
-- ============================================================================
-- NOIZY.AI — iPad USB Audio Capture via Audio Hijack
-- ============================================================================
-- This script creates an Audio Hijack session that captures audio from
-- an iPad connected via USB cable to the M2 Ultra.
--
-- The iPad appears as an audio input device when connected via USB.
-- Audio Hijack captures this input and routes it to your desired output.
-- ============================================================================

tell application "Audio Hijack"
    activate
    delay 1

    -- Create a new session for iPad USB audio capture
    set iPadSession to make new session with properties {name:"NOIZY — iPad USB Input"}

    tell iPadSession
        -- BLOCK 1: Input Source — iPad USB Audio
        -- When your iPad is connected via USB and trusted, it appears as
        -- an audio input device. The device name is typically "iPad" or
        -- "Robert's iPad" — adjust the name below to match yours.
        set inputBlock to make new source block at end of source blocks
        tell inputBlock
            -- Set to "Input Device" type and select iPad
            -- You may need to adjust the device name
            set input device to "iPad"
        end tell

        -- BLOCK 2: Volume control for level adjustment
        set volumeBlock to make new effect block at end of effect blocks
        -- Volume block lets you ride the gain from iPad input

        -- BLOCK 3: Recorder — capture to disk for TALESPIN/NOIZY.AI assets
        set recorderBlock to make new recorder block at end of recorder blocks
        tell recorderBlock
            set output format to "Apple Lossless"
            set output directory to (POSIX path of (path to home folder)) & "Music/NOIZY-AI/iPad-Captures/"
            set output name format to "iPad-Capture_%Y-%m-%d_%H-%M-%S"
        end tell

        -- BLOCK 4: Output Device — route to Mac speakers or Loopback
        set outputBlock to make new output device block at end of output device blocks
        tell outputBlock
            -- "Built-in Output" for Mac speakers
            -- Change to your Loopback device name for DAW routing
            set output device to "Built-in Output"
        end tell
    end tell

    -- Start the session
    tell iPadSession
        start hijacking
    end tell

    display notification "iPad USB audio capture is LIVE" with title "NOIZY.AI Audio" subtitle "Routing iPad → M2 Ultra"
end tell
APPLESCRIPT

  echo -e "${GREEN}✓ Generated: ipad-usb-session.applescript${NC}"
}

# ── Generate AppleScript for AirPlay mode ────────────────────────────────────
generate_airplay_applescript() {
  cat > "${SCRIPT_DIR}/ipad-airplay-session.applescript" << 'APPLESCRIPT'
-- ============================================================================
-- NOIZY.AI — iPad AirPlay Audio Capture via Audio Hijack
-- ============================================================================
-- This script creates an Audio Hijack session that captures AirPlay audio
-- from an iPad streaming to the M2 Ultra over the local network.
--
-- Requirements:
--   1. Mac must have AirPlay Receiver enabled:
--      System Settings → General → AirDrop & Handoff → AirPlay Receiver ON
--   2. iPad and Mac on the same WiFi network
--   3. From iPad: swipe to Control Center → Screen Mirroring or AirPlay
--      → select your M2 Ultra Mac
-- ============================================================================

tell application "Audio Hijack"
    activate
    delay 1

    -- Create a new session for AirPlay audio capture
    set airplaySession to make new session with properties {name:"NOIZY — iPad AirPlay Input"}

    tell airplaySession
        -- BLOCK 1: System Audio Capture
        -- When iPad AirPlays to Mac, the audio plays through the system.
        -- We capture system audio to grab the iPad's stream.
        set inputBlock to make new source block at end of source blocks
        tell inputBlock
            -- Use "System Audio" source type to capture AirPlay stream
            set source type to system audio
        end tell

        -- BLOCK 2: 10-Band EQ for shaping the incoming iPad audio
        set eqBlock to make new effect block at end of effect blocks
        -- EQ lets you shape the iPad audio for NOIZY.AI production needs

        -- BLOCK 3: Recorder — capture to disk
        set recorderBlock to make new recorder block at end of recorder blocks
        tell recorderBlock
            set output format to "Apple Lossless"
            set output directory to (POSIX path of (path to home folder)) & "Music/NOIZY-AI/AirPlay-Captures/"
            set output name format to "AirPlay-Capture_%Y-%m-%d_%H-%M-%S"
        end tell

        -- BLOCK 4: Output Device
        set outputBlock to make new output device block at end of output device blocks
        tell outputBlock
            set output device to "Built-in Output"
        end tell
    end tell

    -- Start the session
    tell airplaySession
        start hijacking
    end tell

    display notification "AirPlay audio capture is LIVE" with title "NOIZY.AI Audio" subtitle "Routing iPad AirPlay → M2 Ultra"
end tell
APPLESCRIPT

  echo -e "${GREEN}✓ Generated: ipad-airplay-session.applescript${NC}"
}

# ── Generate the master control AppleScript ──────────────────────────────────
generate_master_control() {
  cat > "${SCRIPT_DIR}/noizy-audio-control.applescript" << 'APPLESCRIPT'
-- ============================================================================
-- NOIZY.AI — Master Audio Control Panel
-- ============================================================================
-- Quick-launch dialog to manage iPad → M2 Ultra audio routing.
-- Run this from Script Editor, Automator, or assign to a keyboard shortcut.
-- ============================================================================

set actionChoice to button returned of (display dialog ¬
    "NOIZY.AI — Audio Control" & return & return & ¬
    "iPad → M2 Ultra Audio Routing" buttons ¬
    {"USB Capture", "AirPlay Capture", "Stop All"} ¬
    default button "USB Capture" ¬
    with title "NOIZY.AI Audio Hub" ¬
    with icon note)

tell application "Audio Hijack"
    activate

    if actionChoice is "Stop All" then
        -- Stop all running sessions
        repeat with s in every session
            if hijacking of s then
                tell s to stop hijacking
            end if
        end repeat
        display notification "All audio capture stopped" with title "NOIZY.AI Audio"
        return
    end if

    -- Find or create the appropriate session
    set sessionName to "NOIZY — "
    if actionChoice is "USB Capture" then
        set sessionName to sessionName & "iPad USB Input"
    else
        set sessionName to sessionName & "iPad AirPlay Input"
    end if

    set targetSession to missing value
    repeat with s in every session
        if name of s is sessionName then
            set targetSession to s
            exit repeat
        end if
    end repeat

    if targetSession is not missing value then
        tell targetSession
            if hijacking then
                stop hijacking
                display notification sessionName & " stopped" with title "NOIZY.AI Audio"
            else
                start hijacking
                display notification sessionName & " is LIVE" with title "NOIZY.AI Audio"
            end if
        end tell
    else
        display dialog "Session '" & sessionName & "' not found." & return & return & ¬
            "Run the setup scripts first to create the sessions." buttons {"OK"} ¬
            default button "OK" with icon caution
    end if
end tell
APPLESCRIPT

  echo -e "${GREEN}✓ Generated: noizy-audio-control.applescript${NC}"
}

# ── Generate Loopback routing helper ─────────────────────────────────────────
generate_loopback_guide() {
  cat > "${SCRIPT_DIR}/loopback-routing.applescript" << 'APPLESCRIPT'
-- ============================================================================
-- NOIZY.AI — Loopback Virtual Device Setup
-- ============================================================================
-- Creates a Loopback virtual audio device called "NOIZY iPad Bridge"
-- that routes iPad audio into any DAW (Logic Pro, Ableton, etc.)
--
-- Chain: iPad → Audio Hijack → NOIZY iPad Bridge → Your DAW
-- ============================================================================

tell application "Loopback"
    activate
    delay 1

    -- Create virtual device for iPad audio routing
    set noizyDevice to make new virtual device with properties ¬
        {name:"NOIZY iPad Bridge"}

    -- This device acts as a bridge:
    --   Audio Hijack outputs TO this device
    --   Your DAW reads FROM this device as an input
    --
    -- In Audio Hijack: set Output Device to "NOIZY iPad Bridge"
    -- In your DAW: set Audio Input to "NOIZY iPad Bridge"

    display notification "Virtual device 'NOIZY iPad Bridge' created" ¬
        with title "NOIZY.AI Audio" ¬
        subtitle "Use as input in your DAW"
end tell
APPLESCRIPT

  echo -e "${GREEN}✓ Generated: loopback-routing.applescript${NC}"
}

# ── Create capture directories ───────────────────────────────────────────────
create_capture_dirs() {
  local base="${HOME}/Music/NOIZY-AI"
  mkdir -p "${base}/iPad-Captures"
  mkdir -p "${base}/AirPlay-Captures"
  mkdir -p "${base}/TALESPIN"
  echo -e "${GREEN}✓ Created capture directories:${NC}"
  echo "    ~/Music/NOIZY-AI/iPad-Captures/"
  echo "    ~/Music/NOIZY-AI/AirPlay-Captures/"
  echo "    ~/Music/NOIZY-AI/TALESPIN/"
}

# ── Generate quick-run shell scripts ─────────────────────────────────────────
generate_runners() {
  cat > "${SCRIPT_DIR}/start-usb-capture.sh" << 'SH'
#!/bin/bash
# Quick-start iPad USB audio capture
echo "🎤 Starting iPad USB audio capture..."
osascript "$(dirname "$0")/ipad-usb-session.applescript"
echo "✓ iPad USB capture is live"
SH

  cat > "${SCRIPT_DIR}/start-airplay-capture.sh" << 'SH'
#!/bin/bash
# Quick-start iPad AirPlay audio capture
echo "📡 Starting iPad AirPlay audio capture..."
osascript "$(dirname "$0")/ipad-airplay-session.applescript"
echo "✓ iPad AirPlay capture is live"
SH

  cat > "${SCRIPT_DIR}/audio-control.sh" << 'SH'
#!/bin/bash
# Launch the NOIZY.AI audio control panel
osascript "$(dirname "$0")/noizy-audio-control.applescript"
SH

  chmod +x "${SCRIPT_DIR}/start-usb-capture.sh"
  chmod +x "${SCRIPT_DIR}/start-airplay-capture.sh"
  chmod +x "${SCRIPT_DIR}/audio-control.sh"

  echo -e "${GREEN}✓ Generated runner scripts (chmod +x applied)${NC}"
}

# ── Main ─────────────────────────────────────────────────────────────────────
main() {
  local mode="${1:-}"

  echo -e "${CYAN}Checking environment...${NC}"
  check_audio_hijack
  check_loopback
  echo ""

  if [ -z "$mode" ]; then
    echo -e "${CYAN}Select audio routing mode:${NC}"
    echo "  1) USB    — iPad connected via cable (lowest latency)"
    echo "  2) AirPlay — iPad streaming wirelessly"
    echo "  3) Both   — Generate all scripts"
    echo ""
    read -rp "Choice [1/2/3]: " choice
    case "$choice" in
      1) mode="usb" ;;
      2) mode="airplay" ;;
      *) mode="both" ;;
    esac
  fi

  echo ""
  echo -e "${CYAN}Generating scripts...${NC}"

  case "$mode" in
    usb)
      generate_usb_applescript
      ;;
    airplay)
      generate_airplay_applescript
      ;;
    *)
      generate_usb_applescript
      generate_airplay_applescript
      ;;
  esac

  generate_master_control
  generate_loopback_guide
  generate_runners
  create_capture_dirs

  echo ""
  echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}Setup complete!${NC}"
  echo ""
  echo -e "${CYAN}Generated files:${NC}"
  echo "  AppleScripts:"
  echo "    • ipad-usb-session.applescript     — USB capture session"
  echo "    • ipad-airplay-session.applescript  — AirPlay capture session"
  echo "    • noizy-audio-control.applescript   — Master control panel"
  echo "    • loopback-routing.applescript      — Virtual device setup"
  echo ""
  echo "  Shell runners:"
  echo "    • start-usb-capture.sh             — Quick USB start"
  echo "    • start-airplay-capture.sh         — Quick AirPlay start"
  echo "    • audio-control.sh                 — Launch control panel"
  echo ""
  echo -e "${CYAN}Quick start on your M2 Ultra:${NC}"
  echo "  USB mode:     ./start-usb-capture.sh"
  echo "  AirPlay mode: ./start-airplay-capture.sh"
  echo "  Control:      ./audio-control.sh"
  echo ""
  echo -e "${CYAN}For DAW routing (Logic/Ableton):${NC}"
  echo "  1. Run loopback-routing.applescript to create virtual device"
  echo "  2. In Audio Hijack: set output → 'NOIZY iPad Bridge'"
  echo "  3. In your DAW: set input → 'NOIZY iPad Bridge'"
  echo ""
  echo -e "${CYAN}Capture directories:${NC}"
  echo "  ~/Music/NOIZY-AI/iPad-Captures/"
  echo "  ~/Music/NOIZY-AI/AirPlay-Captures/"
  echo "  ~/Music/NOIZY-AI/TALESPIN/"
  echo ""
  echo -e "${YELLOW}NOTE: Run these scripts ON YOUR M2 ULTRA MAC, not in this cloud env.${NC}"
  echo -e "${YELLOW}Copy this folder to your Mac:${NC}"
  echo -e "${YELLOW}  scp -r scripts/audio-hijack/ your-mac:~/NOIZY-AI/scripts/${NC}"
  echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

main "$@"

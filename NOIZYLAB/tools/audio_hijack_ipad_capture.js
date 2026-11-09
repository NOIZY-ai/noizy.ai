/*
 * Audio Hijack Script: iPad to M2 Ultra ("God") Audio Routing
 * ============================================================
 *
 * PURPOSE: Capture audio from iPad via AirPlay and route to recording/processing
 *
 * SETUP REQUIREMENTS:
 * 1. Enable AirPlay Receiver on Mac: System Settings > General > AirDrop & Handoff > AirPlay Receiver
 * 2. iPad and Mac on same network
 * 3. Audio Hijack 4.x installed
 *
 * SESSION CONFIGURATION (in Audio Hijack GUI):
 *
 * Source: "System Audio" or "Application" (select AirPlay audio source)
 *    |
 *    v
 * [10-Band EQ] --> [Denoiser] --> [Recorder] --> [Output Device]
 *                                     |
 *                                     v
 *                              [Save to NOIZYLAB]
 */

// ═══════════════════════════════════════════════════════════════════════════════
// Audio Hijack Session Configuration Export
// Import this JSON into Audio Hijack via File > Import Session
// ═══════════════════════════════════════════════════════════════════════════════

const AudioHijackSession = {
  "name": "iPad to God (M2 Ultra)",
  "version": 4,
  "blocks": [
    {
      "type": "source",
      "source_type": "system_audio",
      "name": "iPad AirPlay Input",
      "notes": "Captures AirPlay audio from iPad",
      "position": { "x": 50, "y": 100 }
    },
    {
      "type": "effect",
      "effect_type": "10band_eq",
      "name": "Voice Enhancement EQ",
      "settings": {
        "32hz": 0,
        "64hz": -2,
        "125hz": 0,
        "250hz": 2,
        "500hz": 3,
        "1khz": 4,
        "2khz": 5,
        "4khz": 4,
        "8khz": 2,
        "16khz": 0
      },
      "notes": "Optimized for voice clarity",
      "position": { "x": 200, "y": 100 }
    },
    {
      "type": "effect",
      "effect_type": "denoiser",
      "name": "Noise Reduction",
      "settings": {
        "reduction_amount": 15,
        "sensitivity": "medium"
      },
      "position": { "x": 350, "y": 100 }
    },
    {
      "type": "recorder",
      "recorder_type": "file",
      "name": "NOIZY Recorder",
      "settings": {
        "format": "wav",
        "sample_rate": 48000,
        "bit_depth": 24,
        "channels": "stereo",
        "output_folder": "~/NOIZYLAB/audio/ipad_captures",
        "filename_template": "ipad_%date%_%time%",
        "auto_split": false
      },
      "position": { "x": 500, "y": 100 }
    },
    {
      "type": "output",
      "output_type": "device",
      "name": "Monitor Output",
      "settings": {
        "device": "default",
        "volume": 0.8
      },
      "position": { "x": 650, "y": 100 }
    }
  ],
  "connections": [
    { "from": "iPad AirPlay Input", "to": "Voice Enhancement EQ" },
    { "from": "Voice Enhancement EQ", "to": "Noise Reduction" },
    { "from": "Noise Reduction", "to": "NOIZY Recorder" },
    { "from": "Noise Reduction", "to": "Monitor Output" }
  ],
  "metadata": {
    "created": "2026-03-23",
    "author": "NOIZYLAB",
    "purpose": "Capture iPad voice performances for NOIZY.AI"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// AppleScript to Auto-Start Session When iPad Connects
// Save as: ~/Library/Scripts/Audio Hijack Scripts/ipad_auto_capture.scpt
// ═══════════════════════════════════════════════════════════════════════════════

const AppleScriptAutoStart = `
-- Audio Hijack Auto-Start for iPad AirPlay
-- Trigger: Run via Shortcuts or EventScripts when AirPlay connects

tell application "Audio Hijack"
    -- Find the iPad capture session
    set targetSession to first session whose name is "iPad to God (M2 Ultra)"

    -- Start the session if not already running
    if not (running of targetSession) then
        start targetSession

        -- Notification
        display notification "iPad audio capture started" with title "Audio Hijack" sound name "Glass"
    end if
end tell
`;

// ═══════════════════════════════════════════════════════════════════════════════
// Shell Script for Quick Toggle
// Save as: ~/NOIZYLAB/tools/ipad_capture.sh
// ═══════════════════════════════════════════════════════════════════════════════

const ShellScript = `#!/bin/bash
# iPad Audio Capture Toggle for Audio Hijack
# Usage: ./ipad_capture.sh [start|stop|status]

SESSION_NAME="iPad to God (M2 Ultra)"

case "$1" in
    start)
        osascript -e "tell application \\"Audio Hijack\\" to start (first session whose name is \\"$SESSION_NAME\\")"
        echo "✓ iPad capture started"
        ;;
    stop)
        osascript -e "tell application \\"Audio Hijack\\" to stop (first session whose name is \\"$SESSION_NAME\\")"
        echo "✓ iPad capture stopped"
        ;;
    status)
        osascript -e "tell application \\"Audio Hijack\\" to return running of (first session whose name is \\"$SESSION_NAME\\")"
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac
`;

// ═══════════════════════════════════════════════════════════════════════════════
// Alternative: Loopback Virtual Device Setup
// For more control, create a virtual audio device
// ═══════════════════════════════════════════════════════════════════════════════

const LoopbackConfig = {
  "device_name": "iPad to NOIZY",
  "channels": 2,
  "sample_rate": 48000,
  "sources": [
    {
      "type": "airplay",
      "name": "iPad AirPlay",
      "notes": "Will appear when iPad connects via AirPlay"
    }
  ],
  "monitors": [
    {
      "device": "Built-in Output",
      "volume": 0.8
    }
  ]
};

// ═══════════════════════════════════════════════════════════════════════════════
// Instructions
// ═══════════════════════════════════════════════════════════════════════════════

console.log(`
╔══════════════════════════════════════════════════════════════════════════════╗
║  IPAD TO M2 ULTRA AUDIO ROUTING - SETUP GUIDE                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  STEP 1: Enable AirPlay Receiver on Mac                                     ║
║  ─────────────────────────────────────────                                   ║
║  System Settings > General > AirDrop & Handoff > AirPlay Receiver = ON      ║
║                                                                              ║
║  STEP 2: Create Audio Hijack Session                                        ║
║  ─────────────────────────────────────                                       ║
║  1. Open Audio Hijack                                                        ║
║  2. Create new session: "iPad to God (M2 Ultra)"                            ║
║  3. Add blocks:                                                              ║
║     [System Audio] → [10-Band EQ] → [Recorder] → [Output Device]            ║
║                                                                              ║
║  STEP 3: Configure Recorder                                                  ║
║  ─────────────────────────────                                               ║
║  • Format: WAV (24-bit, 48kHz)                                              ║
║  • Output: ~/NOIZYLAB/audio/ipad_captures/                                  ║
║  • Filename: ipad_%date%_%time%                                             ║
║                                                                              ║
║  STEP 4: Connect iPad                                                        ║
║  ─────────────────────                                                       ║
║  1. On iPad: Swipe down for Control Center                                  ║
║  2. Tap AirPlay icon (or Screen Mirroring)                                  ║
║  3. Select "God" (your M2 Ultra)                                            ║
║  4. Start Audio Hijack session                                              ║
║                                                                              ║
║  QUICK COMMANDS:                                                             ║
║  ───────────────                                                             ║
║  ./ipad_capture.sh start   - Begin recording                                ║
║  ./ipad_capture.sh stop    - Stop recording                                 ║
║  ./ipad_capture.sh status  - Check if running                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
`);

// Export configurations
module.exports = {
  AudioHijackSession,
  AppleScriptAutoStart,
  ShellScript,
  LoopbackConfig
};

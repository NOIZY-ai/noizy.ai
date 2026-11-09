/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * NOIZY SATELLITE SESSION CONFIGURATIONS
 * iPad & iPhone → M2 Ultra "God" via Rogue Amoeba Satellite + Audio Hijack
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Satellite provides professional iOS audio routing:
 * • App-specific audio capture (capture from any app)
 * • Device microphone capture
 * • Multiple sources simultaneously
 * • Network audio streaming to Mac
 *
 * These configurations can be imported into Audio Hijack.
 */

// ═══════════════════════════════════════════════════════════════════════════════
// IPAD SATELLITE SESSION
// Optimized for voice recording on iPad Pro
// ═══════════════════════════════════════════════════════════════════════════════

const iPadSatelliteSession = {
  name: "NOIZY iPad Satellite",
  version: 4,
  description: "Capture iPad audio via Satellite - Voice optimized",

  blocks: [
    {
      id: "source_satellite_ipad",
      type: "source",
      source_type: "satellite",
      name: "iPad Satellite",
      notes: "Receives audio from iPad via Satellite app",
      settings: {
        device_name: "iPad",  // Will match any iPad
        channels: 2,
        sample_rate: 48000
      },
      position: { x: 50, y: 100 }
    },
    {
      id: "input_gain",
      type: "effect",
      effect_type: "gain",
      name: "Input Gain",
      settings: {
        gain_db: 0,
        normalize: false
      },
      position: { x: 180, y: 100 }
    },
    {
      id: "noise_gate",
      type: "effect",
      effect_type: "noise_gate",
      name: "Noise Gate",
      notes: "Remove background noise between phrases",
      settings: {
        threshold_db: -40,
        attack_ms: 5,
        release_ms: 100,
        hold_ms: 50
      },
      position: { x: 310, y: 100 }
    },
    {
      id: "voice_eq",
      type: "effect",
      effect_type: "10band_eq",
      name: "Voice Enhancement EQ",
      notes: "Optimized for NOIZY voice clarity",
      settings: {
        // Frequencies: 32, 64, 125, 250, 500, 1k, 2k, 4k, 8k, 16k
        bands: [
          { frequency: 32, gain: -6 },     // Cut rumble
          { frequency: 64, gain: -3 },     // Reduce mud
          { frequency: 125, gain: 0 },     // Body
          { frequency: 250, gain: 2 },     // Warmth
          { frequency: 500, gain: 1 },     // Fullness
          { frequency: 1000, gain: 3 },    // Presence
          { frequency: 2000, gain: 4 },    // Clarity
          { frequency: 4000, gain: 5 },    // Articulation
          { frequency: 8000, gain: 3 },    // Air
          { frequency: 16000, gain: 0 }    // Ultra-high (natural)
        ]
      },
      position: { x: 440, y: 100 }
    },
    {
      id: "compressor",
      type: "effect",
      effect_type: "compressor",
      name: "Voice Compressor",
      notes: "Even out dynamics for consistent levels",
      settings: {
        threshold_db: -18,
        ratio: 3,
        attack_ms: 10,
        release_ms: 100,
        makeup_gain_db: 3,
        knee_db: 6
      },
      position: { x: 570, y: 100 }
    },
    {
      id: "limiter",
      type: "effect",
      effect_type: "limiter",
      name: "Safety Limiter",
      notes: "Prevent clipping",
      settings: {
        ceiling_db: -1,
        release_ms: 50
      },
      position: { x: 700, y: 100 }
    },
    {
      id: "recorder_wav",
      type: "recorder",
      recorder_type: "file",
      name: "WAV Recorder",
      settings: {
        format: "wav",
        sample_rate: 48000,
        bit_depth: 24,
        channels: "stereo",
        output_folder: "~/NOIZYLAB/audio/satellite_captures/ipad",
        filename_template: "ipad_satellite_%date%_%time%",
        auto_split: false,
        add_markers: true
      },
      position: { x: 830, y: 60 }
    },
    {
      id: "recorder_mp3",
      type: "recorder",
      recorder_type: "file",
      name: "MP3 Backup",
      notes: "Compressed backup for quick sharing",
      settings: {
        format: "mp3",
        bitrate: 320,
        output_folder: "~/NOIZYLAB/audio/satellite_captures/ipad/mp3",
        filename_template: "ipad_%date%_%time%"
      },
      position: { x: 830, y: 140 }
    },
    {
      id: "output_monitor",
      type: "output",
      output_type: "device",
      name: "Monitor Output",
      settings: {
        device: "default",
        volume: 0.7
      },
      position: { x: 960, y: 100 }
    }
  ],

  connections: [
    { from: "source_satellite_ipad", to: "input_gain" },
    { from: "input_gain", to: "noise_gate" },
    { from: "noise_gate", to: "voice_eq" },
    { from: "voice_eq", to: "compressor" },
    { from: "compressor", to: "limiter" },
    { from: "limiter", to: "recorder_wav" },
    { from: "limiter", to: "recorder_mp3" },
    { from: "limiter", to: "output_monitor" }
  ]
};


// ═══════════════════════════════════════════════════════════════════════════════
// IPHONE SATELLITE SESSION
// Optimized for mobile voice capture
// ═══════════════════════════════════════════════════════════════════════════════

const iPhoneSatelliteSession = {
  name: "NOIZY iPhone Satellite",
  version: 4,
  description: "Capture iPhone audio via Satellite - Mobile voice optimized",

  blocks: [
    {
      id: "source_satellite_iphone",
      type: "source",
      source_type: "satellite",
      name: "iPhone Satellite",
      notes: "Receives audio from iPhone via Satellite app",
      settings: {
        device_name: "iPhone",
        channels: 2,
        sample_rate: 48000
      },
      position: { x: 50, y: 100 }
    },
    {
      id: "input_gain",
      type: "effect",
      effect_type: "gain",
      name: "Input Gain",
      settings: {
        gain_db: 3,  // iPhone mics often need slight boost
        normalize: false
      },
      position: { x: 180, y: 100 }
    },
    {
      id: "noise_gate",
      type: "effect",
      effect_type: "noise_gate",
      name: "Noise Gate",
      settings: {
        threshold_db: -35,  // Slightly higher for mobile environments
        attack_ms: 5,
        release_ms: 100,
        hold_ms: 50
      },
      position: { x: 310, y: 100 }
    },
    {
      id: "voice_eq",
      type: "effect",
      effect_type: "10band_eq",
      name: "Mobile Voice EQ",
      notes: "Compensates for iPhone mic characteristics",
      settings: {
        bands: [
          { frequency: 32, gain: -8 },     // Cut handling noise
          { frequency: 64, gain: -4 },     // Reduce proximity effect
          { frequency: 125, gain: -1 },    // Tame boominess
          { frequency: 250, gain: 2 },     // Add warmth
          { frequency: 500, gain: 1 },     // Body
          { frequency: 1000, gain: 2 },    // Presence
          { frequency: 2000, gain: 4 },    // Clarity (iPhone can be thin)
          { frequency: 4000, gain: 5 },    // Articulation
          { frequency: 8000, gain: 4 },    // Air
          { frequency: 16000, gain: 2 }    // Sparkle
        ]
      },
      position: { x: 440, y: 100 }
    },
    {
      id: "denoiser",
      type: "effect",
      effect_type: "denoiser",
      name: "AI Denoiser",
      notes: "Remove background noise from mobile recording",
      settings: {
        reduction_amount: 20,
        sensitivity: "high"
      },
      position: { x: 570, y: 100 }
    },
    {
      id: "compressor",
      type: "effect",
      effect_type: "compressor",
      name: "Voice Compressor",
      settings: {
        threshold_db: -20,
        ratio: 4,  // Stronger ratio for mobile
        attack_ms: 8,
        release_ms: 80,
        makeup_gain_db: 4,
        knee_db: 8
      },
      position: { x: 700, y: 100 }
    },
    {
      id: "limiter",
      type: "effect",
      effect_type: "limiter",
      name: "Safety Limiter",
      settings: {
        ceiling_db: -1,
        release_ms: 50
      },
      position: { x: 830, y: 100 }
    },
    {
      id: "recorder_wav",
      type: "recorder",
      recorder_type: "file",
      name: "WAV Recorder",
      settings: {
        format: "wav",
        sample_rate: 48000,
        bit_depth: 24,
        channels: "stereo",
        output_folder: "~/NOIZYLAB/audio/satellite_captures/iphone",
        filename_template: "iphone_satellite_%date%_%time%"
      },
      position: { x: 960, y: 60 }
    },
    {
      id: "output_monitor",
      type: "output",
      output_type: "device",
      name: "Monitor Output",
      settings: {
        device: "default",
        volume: 0.7
      },
      position: { x: 960, y: 140 }
    }
  ],

  connections: [
    { from: "source_satellite_iphone", to: "input_gain" },
    { from: "input_gain", to: "noise_gate" },
    { from: "noise_gate", to: "voice_eq" },
    { from: "voice_eq", to: "denoiser" },
    { from: "denoiser", to: "compressor" },
    { from: "compressor", to: "limiter" },
    { from: "limiter", to: "recorder_wav" },
    { from: "limiter", to: "output_monitor" }
  ]
};


// ═══════════════════════════════════════════════════════════════════════════════
// DUAL DEVICE SESSION
// Capture from both devices simultaneously with mixing
// ═══════════════════════════════════════════════════════════════════════════════

const dualDeviceSession = {
  name: "NOIZY Dual Satellite",
  version: 4,
  description: "Capture iPad + iPhone simultaneously with individual and mixed outputs",

  blocks: [
    // iPad chain
    {
      id: "source_ipad",
      type: "source",
      source_type: "satellite",
      name: "iPad",
      settings: { device_name: "iPad" },
      position: { x: 50, y: 50 }
    },
    {
      id: "ipad_eq",
      type: "effect",
      effect_type: "10band_eq",
      name: "iPad EQ",
      position: { x: 180, y: 50 }
    },
    {
      id: "ipad_recorder",
      type: "recorder",
      recorder_type: "file",
      name: "iPad WAV",
      settings: {
        format: "wav",
        output_folder: "~/NOIZYLAB/audio/satellite_captures/ipad",
        filename_template: "ipad_%date%_%time%"
      },
      position: { x: 310, y: 50 }
    },

    // iPhone chain
    {
      id: "source_iphone",
      type: "source",
      source_type: "satellite",
      name: "iPhone",
      settings: { device_name: "iPhone" },
      position: { x: 50, y: 150 }
    },
    {
      id: "iphone_eq",
      type: "effect",
      effect_type: "10band_eq",
      name: "iPhone EQ",
      position: { x: 180, y: 150 }
    },
    {
      id: "iphone_recorder",
      type: "recorder",
      recorder_type: "file",
      name: "iPhone WAV",
      settings: {
        format: "wav",
        output_folder: "~/NOIZYLAB/audio/satellite_captures/iphone",
        filename_template: "iphone_%date%_%time%"
      },
      position: { x: 310, y: 150 }
    },

    // Mixer for combined output
    {
      id: "mixer",
      type: "effect",
      effect_type: "mixer",
      name: "Device Mixer",
      settings: {
        input_1_volume: 0.5,
        input_2_volume: 0.5,
        pan_1: -0.3,  // iPad slightly left
        pan_2: 0.3    // iPhone slightly right
      },
      position: { x: 440, y: 100 }
    },
    {
      id: "mixed_recorder",
      type: "recorder",
      recorder_type: "file",
      name: "Mixed WAV",
      settings: {
        format: "wav",
        output_folder: "~/NOIZYLAB/audio/satellite_captures/mixed",
        filename_template: "dual_satellite_%date%_%time%"
      },
      position: { x: 570, y: 100 }
    },
    {
      id: "output",
      type: "output",
      output_type: "device",
      name: "Monitor",
      position: { x: 700, y: 100 }
    }
  ],

  connections: [
    // iPad chain
    { from: "source_ipad", to: "ipad_eq" },
    { from: "ipad_eq", to: "ipad_recorder" },
    { from: "ipad_eq", to: "mixer", port: 1 },

    // iPhone chain
    { from: "source_iphone", to: "iphone_eq" },
    { from: "iphone_eq", to: "iphone_recorder" },
    { from: "iphone_eq", to: "mixer", port: 2 },

    // Mixed output
    { from: "mixer", to: "mixed_recorder" },
    { from: "mixer", to: "output" }
  ]
};


// ═══════════════════════════════════════════════════════════════════════════════
// APPLESCRIPT FOR SESSION CREATION
// ═══════════════════════════════════════════════════════════════════════════════

const createSessionsAppleScript = `
-- NOIZY Satellite Sessions Creator
-- Run this to set up all sessions in Audio Hijack

tell application "Audio Hijack"
    activate

    display dialog "NOIZY Satellite Setup

This will create 3 Audio Hijack sessions:

1. NOIZY iPad Satellite
   iPad → Voice Processing → Recording

2. NOIZY iPhone Satellite
   iPhone → Voice Processing → Recording

3. NOIZY Dual Satellite
   Both devices → Individual + Mixed recording

Proceed?" buttons {"Cancel", "Create Sessions"} default button "Create Sessions"

    if button returned of result is "Create Sessions" then
        -- Create iPad session
        make new session with properties {name:"NOIZY iPad Satellite"}

        -- Create iPhone session
        make new session with properties {name:"NOIZY iPhone Satellite"}

        -- Create Dual session
        make new session with properties {name:"NOIZY Dual Satellite"}

        display notification "Created 3 Satellite sessions" with title "NOIZY Audio"

        display dialog "Sessions Created!

Next Steps:
━━━━━━━━━━━
1. Open each session in Audio Hijack
2. Configure the signal chain:
   [Satellite Source] → [EQ] → [Compressor] → [Recorder] → [Output]

3. Set recorder output folders:
   • iPad: ~/NOIZYLAB/audio/satellite_captures/ipad/
   • iPhone: ~/NOIZYLAB/audio/satellite_captures/iphone/
   • Mixed: ~/NOIZYLAB/audio/satellite_captures/mixed/

4. On iOS devices:
   • Install 'Satellite' from App Store
   • Open Satellite
   • Select audio source
   • Connect to this Mac

Ready to capture!" buttons {"OK"} default button "OK"
    end if
end tell
`;


// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

console.log(`
╔══════════════════════════════════════════════════════════════════════════════╗
║  NOIZY SATELLITE SESSIONS                                                    ║
║  Professional iOS Audio Capture                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Sessions Defined:                                                           ║
║  • NOIZY iPad Satellite    - Full voice processing chain                    ║
║  • NOIZY iPhone Satellite  - Mobile-optimized processing                    ║
║  • NOIZY Dual Satellite    - Both devices with mixing                       ║
║                                                                              ║
║  Quick Setup:                                                                ║
║  1. Run: ./satellite.sh setup-both                                          ║
║  2. Configure sessions in Audio Hijack                                      ║
║  3. Install Satellite on iPad/iPhone                                        ║
║  4. Connect devices to Mac                                                  ║
║  5. Run: ./satellite.sh both                                                ║
║                                                                              ║
║  Output Folders:                                                             ║
║  ~/NOIZYLAB/audio/satellite_captures/ipad/                                  ║
║  ~/NOIZYLAB/audio/satellite_captures/iphone/                                ║
║  ~/NOIZYLAB/audio/satellite_captures/mixed/                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
`);

module.exports = {
  iPadSatelliteSession,
  iPhoneSatelliteSession,
  dualDeviceSession,
  createSessionsAppleScript
};

/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *  NOIZY SESSION EVENTS — Audio Hijack Event Scripts
 *  Automated responses to recording events
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *  These scripts respond to Audio Hijack events:
 *  • sessionWillStart — Session is about to start
 *  • sessionDidStop — Session just stopped
 *  • sessionDidIdle — Session has been idle
 *  • fileDidEnd — Recording file completed
 *  • timerWillStart / timerDidStop — Timer events
 *
 *  Add these to your session's Script block with "Run on Event" enabled
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// Configuration
const NOIZY_BASE = "~/NOIZYLAB/audio";
const WHISPER_ENABLED = true;  // Auto-transcribe on file completion
const NOTIFY_ON_COMPLETE = true;

/**
 * Handle session start event
 */
function onSessionWillStart() {
    const session = __event__.session;
    const sessionName = session.name;

    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    __console__.log("  SESSION STARTING: " + sessionName);
    __console__.log("  Time: " + new Date().toLocaleString());
    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    // Configure recorder with timestamp
    const recorder = session.blockWithName("Recorder");
    if (recorder) {
        // Set filename with date/time
        const now = new Date();
        const timestamp = now.toISOString().replace(/[:.]/g, "-").slice(0, 19);
        const deviceType = getDeviceType(sessionName);

        recorder.fileName = deviceType + "_" + timestamp;

        __console__.log("  Recorder configured: " + recorder.fileName);
    }

    // Notification
    __app__.runShellCommand("osascript -e 'display notification \"" +
        sessionName + " started recording\" with title \"NOIZY Studio\" sound name \"Glass\"'");
}

/**
 * Handle session stop event
 */
function onSessionDidStop() {
    const session = __event__.session;
    const sessionName = session.name;
    const runTime = session.runTime;

    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    __console__.log("  SESSION STOPPED: " + sessionName);
    __console__.log("  Duration: " + formatDuration(runTime));
    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    // List recordings from this session
    const recordings = session.recordings;
    if (recordings.length > 0) {
        __console__.log("\n  Recordings:");
        for (const rec of recordings.slice(-3)) {
            __console__.log("    • " + rec.fileName + " (" + rec.displayTime + ")");
        }
    }

    // Notification
    __app__.runShellCommand("osascript -e 'display notification \"" +
        sessionName + " stopped (" + formatDuration(runTime) + ")\" with title \"NOIZY Studio\" sound name \"Blow\"'");
}

/**
 * Handle file completion event
 * This is where the magic happens — process completed recordings
 */
function onFileDidEnd() {
    const file = __event__.file;
    const session = __event__.session;

    __console__.log("═══════════════════════════════════════════════════════");
    __console__.log("  RECORDING COMPLETE");
    __console__.log("═══════════════════════════════════════════════════════");
    __console__.log("  File: " + file.fileName);
    __console__.log("  Path: " + file.filePath);
    __console__.log("  Duration: " + file.displayTime);
    __console__.log("  Size: " + formatFileSize(file.fileSize));
    __console__.log("  Session: " + session.name);
    __console__.log("═══════════════════════════════════════════════════════");

    // Update tags with NOIZY metadata
    const deviceType = getDeviceType(session.name);
    file.updateTags({
        "artist": "NOIZY Studio",
        "album": deviceType + " Recordings",
        "comment": "Recorded via " + session.name + " | NOIZYLAB",
        "genre": "Voice Recording"
    });
    __console__.log("  ✓ Tags updated");

    // Auto-transcribe if enabled
    if (WHISPER_ENABLED) {
        transcribeRecording(file);
    }

    // Notification with option to reveal
    if (NOTIFY_ON_COMPLETE) {
        __app__.runShellCommand("osascript -e 'display notification \"" +
            file.fileName + " (" + file.displayTime + ")\" with title \"Recording Complete\" sound name \"Hero\"'");
    }
}

/**
 * Transcribe recording using Whisper
 */
function transcribeRecording(file) {
    __console__.log("\n  Starting transcription...");

    const filePath = __app__.shellEscapeArgument(file.filePath);
    const outputDir = NOIZY_BASE + "/transcripts";

    // Check for Whisper and transcribe in background
    const command = "if command -v whisper &> /dev/null; then " +
        "nohup whisper " + filePath + " --model base --output_dir " +
        __app__.shellEscapeArgument(outputDir) +
        " --output_format txt > /dev/null 2>&1 & " +
        "echo 'Transcription started'; " +
        "else echo 'Whisper not installed'; fi";

    const result = __app__.runShellCommand(command);
    __console__.log("  Transcription: " + result[1]);
}

/**
 * Handle idle event — session running but no audio
 */
function onSessionDidIdle() {
    const session = __event__.session;

    __console__.log("⚠ Session idle: " + session.name);
    __console__.log("  No audio detected. Check connections.");

    // Could auto-stop after extended idle:
    // session.stop();
}

/**
 * Get device type from session name
 */
function getDeviceType(sessionName) {
    if (sessionName.includes("iPad")) return "ipad";
    if (sessionName.includes("iPhone")) return "iphone";
    if (sessionName.includes("Neumann")) return "neumann";
    if (sessionName.includes("MacBook")) return "macbook";
    return "unknown";
}

/**
 * Format duration in seconds to human readable
 */
function formatDuration(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hrs > 0) {
        return hrs + "h " + mins + "m " + secs + "s";
    } else if (mins > 0) {
        return mins + "m " + secs + "s";
    } else {
        return secs + "s";
    }
}

/**
 * Format file size to human readable
 */
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + " GB";
}

// ═══════════════════════════════════════════════════════════════════════════════
// EVENT ROUTER — Automatically called by Audio Hijack
// ═══════════════════════════════════════════════════════════════════════════════

// Check event type and route to appropriate handler
if (typeof __event__ !== 'undefined') {
    const eventType = __event__.eventType;

    switch (eventType) {
        case "sessionWillStart":
            onSessionWillStart();
            break;
        case "sessionDidStop":
            onSessionDidStop();
            break;
        case "fileDidEnd":
            onFileDidEnd();
            break;
        case "sessionDidIdle":
            onSessionDidIdle();
            break;
        case "timerWillStart":
            __console__.log("Timer starting: " + __event__.session.name);
            break;
        case "timerDidStop":
            __console__.log("Timer stopped: " + __event__.session.name);
            break;
        default:
            __console__.log("Unhandled event: " + eventType);
    }
} else {
    // Script run manually, show help
    __console__.log("═══════════════════════════════════════════════════════");
    __console__.log("  NOIZY SESSION EVENTS");
    __console__.log("═══════════════════════════════════════════════════════");
    __console__.log("");
    __console__.log("  This script handles Audio Hijack events:");
    __console__.log("    • sessionWillStart — Configure recorder");
    __console__.log("    • sessionDidStop — Log duration");
    __console__.log("    • fileDidEnd — Tag & transcribe recording");
    __console__.log("    • sessionDidIdle — Warn about no audio");
    __console__.log("");
    __console__.log("  Setup:");
    __console__.log("    1. Add Script block to session");
    __console__.log("    2. Paste this script");
    __console__.log("    3. Enable 'Run on Event'");
    __console__.log("");
    __console__.log("═══════════════════════════════════════════════════════");
}

/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *  NOIZY SHORTCUTS — Quick Commands for Audio Hijack
 *  One-liners for common operations
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *  Create Script Shortcuts in Audio Hijack pointing to these functions:
 *  - Each function is self-contained
 *  - Can be triggered via keyboard shortcuts
 *  - Works with Shortcuts.app integration
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// MASTER SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * START ALL — Launch every NOIZY session
 * Shortcut: Cmd+Shift+R
 */
function NOIZY_START_ALL() {
    const sessions = [
        "NOIZY iPad Satellite",
        "NOIZY iPhone Satellite",
        "NOIZY Neumann Master"
    ];

    let count = 0;
    for (const name of sessions) {
        const s = __app__.sessionWithName(name);
        if (s && !s.running) {
            s.start();
            count++;
        }
    }

    __console__.dialog("NOIZY: " + count + " sessions started");
}

/**
 * STOP ALL — Shutdown everything
 * Shortcut: Cmd+Shift+S
 */
function NOIZY_STOP_ALL() {
    __app__.stopAllSessions();
    __console__.dialog("NOIZY: All sessions stopped");
}

/**
 * QUICK STATUS — Show what's running
 * Shortcut: Cmd+Shift+?
 */
function NOIZY_STATUS() {
    const running = __app__.runningSessions;
    let msg = running.length + " sessions running:\n";

    for (const s of running) {
        const mins = Math.floor(s.runTime / 60);
        const secs = Math.floor(s.runTime % 60);
        msg += "• " + s.name + " [" + mins + ":" + (secs < 10 ? "0" : "") + secs + "]\n";
    }

    __console__.dialog(msg);
}

// ═══════════════════════════════════════════════════════════════════════════════
// DEVICE SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * IPAD START — Quick start iPad capture
 */
function NOIZY_IPAD_START() {
    const s = __app__.sessionWithName("NOIZY iPad Satellite");
    if (s) {
        s.start();
        __console__.log("✓ iPad Satellite started");
    }
}

/**
 * IPAD STOP
 */
function NOIZY_IPAD_STOP() {
    const s = __app__.sessionWithName("NOIZY iPad Satellite");
    if (s) s.stop();
}

/**
 * IPHONE START — Quick start iPhone capture
 */
function NOIZY_IPHONE_START() {
    const s = __app__.sessionWithName("NOIZY iPhone Satellite");
    if (s) {
        s.start();
        __console__.log("✓ iPhone Satellite started");
    }
}

/**
 * IPHONE STOP
 */
function NOIZY_IPHONE_STOP() {
    const s = __app__.sessionWithName("NOIZY iPhone Satellite");
    if (s) s.stop();
}

/**
 * NEUMANN START — Start Neumann master capture
 */
function NOIZY_NEUMANN_START() {
    const s = __app__.sessionWithName("NOIZY Neumann Master");
    if (s) {
        s.start();
        __console__.log("✓ Neumann capture started");
    }
}

/**
 * NEUMANN STOP
 */
function NOIZY_NEUMANN_STOP() {
    const s = __app__.sessionWithName("NOIZY Neumann Master");
    if (s) s.stop();
}

/**
 * SATELLITE BOTH — Start iPad + iPhone together
 */
function NOIZY_SATELLITE_START() {
    NOIZY_IPAD_START();
    NOIZY_IPHONE_START();
    __console__.dialog("Satellite: iPad + iPhone active");
}

/**
 * SATELLITE STOP
 */
function NOIZY_SATELLITE_STOP() {
    NOIZY_IPAD_STOP();
    NOIZY_IPHONE_STOP();
}

// ═══════════════════════════════════════════════════════════════════════════════
// RECORDING SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * LIST RECENT — Show last 5 recordings
 */
function NOIZY_LIST_RECENT() {
    const recs = __app__.recordings.slice(-5);
    let msg = "Recent Recordings:\n";

    for (const r of recs) {
        msg += "• " + r.displayName + " (" + r.displayTime + ")\n";
    }

    __console__.dialog(msg);
}

/**
 * REVEAL LAST — Show last recording in Finder
 */
function NOIZY_REVEAL_LAST() {
    const recs = __app__.recordings;
    if (recs.length > 0) {
        const last = recs[recs.length - 1];
        last.revealInFinder();
        __console__.log("Revealed: " + last.fileName);
    }
}

/**
 * PLAY LAST — Start playing the last recording
 */
function NOIZY_PLAY_LAST() {
    const recs = __app__.recordings;
    if (recs.length > 0) {
        const last = recs[recs.length - 1];
        last.startPlaying();
    }
}

/**
 * OPEN LAST IN LOGIC — Send last recording to Logic Pro X
 */
function NOIZY_TO_LOGIC() {
    const recs = __app__.recordings;
    if (recs.length > 0) {
        const last = recs[recs.length - 1];
        last.openInApp("/Applications/Logic Pro X.app");
        __console__.log("Opened in Logic: " + last.fileName);
    }
}

/**
 * TRANSCRIBE LAST — Whisper transcription of last recording
 */
function NOIZY_TRANSCRIBE_LAST() {
    const recs = __app__.recordings;
    if (recs.length === 0) {
        __console__.dialog("No recordings to transcribe");
        return;
    }

    const last = recs[recs.length - 1];
    const filePath = __app__.shellEscapeArgument(last.filePath);
    const outDir = __app__.shellEscapeArgument("~/NOIZYLAB/audio/transcripts");

    __console__.log("Transcribing: " + last.fileName);

    const cmd = "nohup whisper " + filePath +
                " --model base --output_dir " + outDir +
                " --output_format txt > /dev/null 2>&1 &";

    __app__.runShellCommand(cmd);
    __console__.dialog("Transcription started:\n" + last.fileName);
}

// ═══════════════════════════════════════════════════════════════════════════════
// AI INTEGRATION SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * TO WINDSURF — Route audio to Windsurf
 */
function NOIZY_TO_WINDSURF() {
    const s = __app__.sessionWithName("NOIZY to Windsurf");
    if (s) {
        s.running ? s.stop() : s.start();
        __console__.log("Windsurf audio: " + (s.running ? "ON" : "OFF"));
    }
}

/**
 * TO CASCADE — Route audio to Cascade
 */
function NOIZY_TO_CASCADE() {
    const s = __app__.sessionWithName("NOIZY to Cascade");
    if (s) {
        s.running ? s.stop() : s.start();
        __console__.log("Cascade audio: " + (s.running ? "ON" : "OFF"));
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// UTILITY SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * SHOW SESSIONS WINDOW
 */
function NOIZY_SHOW_SESSIONS() {
    __app__.showSessionsWindow();
}

/**
 * BRING TO FRONT
 */
function NOIZY_FOCUS() {
    __app__.bringToFront();
}

/**
 * CLEAR LOG
 */
function NOIZY_CLEAR_LOG() {
    __console__.clear();
    __console__.log("═══════════════════════════════════════════════════════");
    __console__.log("  NOIZY STUDIO — Log cleared");
    __console__.log("═══════════════════════════════════════════════════════");
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMBO SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * FULL STUDIO — Start everything for a full session
 */
function NOIZY_FULL_STUDIO() {
    __console__.clear();
    __console__.log("═══════════════════════════════════════════════════════");
    __console__.log("  NOIZY FULL STUDIO SESSION");
    __console__.log("═══════════════════════════════════════════════════════\n");

    // Start all capture sessions
    NOIZY_START_ALL();

    // Open Logic Pro X
    __app__.runShellCommand("open -a 'Logic Pro X'");

    __console__.log("\n  ✓ Full studio session ready");
    __console__.log("  • All capture sessions active");
    __console__.log("  • Logic Pro X opening");
    __console__.log("\n═══════════════════════════════════════════════════════");
}

/**
 * QUICK VOICE — Just Neumann, quick recording
 */
function NOIZY_QUICK_VOICE() {
    // Stop everything else
    __app__.stopAllSessions();

    // Start just Neumann
    NOIZY_NEUMANN_START();

    __console__.dialog("Quick Voice: Neumann only");
}

/**
 * MOBILE SESSION — iPad + iPhone for field work
 */
function NOIZY_MOBILE_SESSION() {
    // Stop desktop sources
    NOIZY_NEUMANN_STOP();

    // Start Satellite
    NOIZY_SATELLITE_START();

    __console__.dialog("Mobile Session: Satellite devices active");
}

// ═══════════════════════════════════════════════════════════════════════════════
// HELP
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * HELP — Show all available shortcuts
 */
function NOIZY_HELP() {
    const help = `
═══════════════════════════════════════════════════════
  NOIZY SHORTCUTS — Quick Commands
═══════════════════════════════════════════════════════

MASTER:
  NOIZY_START_ALL()       Start all sessions
  NOIZY_STOP_ALL()        Stop all sessions
  NOIZY_STATUS()          Show status

DEVICES:
  NOIZY_IPAD_START/STOP()
  NOIZY_IPHONE_START/STOP()
  NOIZY_NEUMANN_START/STOP()
  NOIZY_SATELLITE_START/STOP()  (both iOS)

RECORDINGS:
  NOIZY_LIST_RECENT()     Last 5 recordings
  NOIZY_REVEAL_LAST()     Show in Finder
  NOIZY_PLAY_LAST()       Play last recording
  NOIZY_TO_LOGIC()        Open in Logic Pro X
  NOIZY_TRANSCRIBE_LAST() Whisper transcription

AI INTEGRATION:
  NOIZY_TO_WINDSURF()     Toggle Windsurf feed
  NOIZY_TO_CASCADE()      Toggle Cascade feed

COMBOS:
  NOIZY_FULL_STUDIO()     Start everything
  NOIZY_QUICK_VOICE()     Neumann only
  NOIZY_MOBILE_SESSION()  Satellite only

═══════════════════════════════════════════════════════
`;

    __console__.log(help);
}

// Default action when script runs
NOIZY_STATUS();

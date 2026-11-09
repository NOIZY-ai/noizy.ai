/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *  NOIZY MASTER CONTROL — Audio Hijack JavaScript
 *  Controls all NOIZY sessions from a single script
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *  Run this script from Audio Hijack's Script block or "Run Now" feature
 *
 *  Hardware controlled:
 *  • iPad Pro 12.9" (2nd Gen) via Satellite
 *  • iPhone 15 Pro Max via Satellite
 *  • Neumann Microphone via audio interface
 *  • MacBook Pro relay
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// Session names
const SESSIONS = {
    IPAD: "NOIZY iPad Satellite",
    IPHONE: "NOIZY iPhone Satellite",
    NEUMANN: "NOIZY Neumann Master",
    MACBOOK: "NOIZY MacBook Relay",
    DUAL: "NOIZY Dual Satellite"
};

// Output directories
const OUTPUT_BASE = "~/NOIZYLAB/audio";
const OUTPUTS = {
    IPAD: OUTPUT_BASE + "/satellite_captures/ipad",
    IPHONE: OUTPUT_BASE + "/satellite_captures/iphone",
    NEUMANN: OUTPUT_BASE + "/neumann",
    MIXED: OUTPUT_BASE + "/satellite_captures/mixed"
};

/**
 * Get session by name, with error handling
 */
function getSession(name) {
    const session = __app__.sessionWithName(name);
    if (!session) {
        __console__.error("Session not found: " + name);
        return null;
    }
    return session;
}

/**
 * Start all NOIZY recording sessions
 */
function startAllSessions() {
    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    __console__.log("  NOIZY STUDIO — Starting all sessions");
    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    let started = 0;

    for (const [key, name] of Object.entries(SESSIONS)) {
        const session = getSession(name);
        if (session && !session.running) {
            session.start();
            __console__.log("  ✓ Started: " + name);
            started++;
        } else if (session && session.running) {
            __console__.log("  ○ Already running: " + name);
        }
    }

    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    __console__.log("  " + started + " sessions started");
    __console__.dialog("NOIZY Studio: " + started + " sessions started");
}

/**
 * Stop all NOIZY recording sessions
 */
function stopAllSessions() {
    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    __console__.log("  NOIZY STUDIO — Stopping all sessions");
    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    let stopped = 0;

    for (const [key, name] of Object.entries(SESSIONS)) {
        const session = getSession(name);
        if (session && session.running) {
            session.stop();
            __console__.log("  ✓ Stopped: " + name);
            stopped++;
        }
    }

    __console__.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    __console__.log("  " + stopped + " sessions stopped");
    __console__.dialog("NOIZY Studio: " + stopped + " sessions stopped");
}

/**
 * Get status of all sessions
 */
function getStatus() {
    __console__.log("\n═══════════════════════════════════════════════════════");
    __console__.log("  NOIZY STUDIO STATUS");
    __console__.log("═══════════════════════════════════════════════════════\n");

    let running = 0;
    let total = 0;

    for (const [key, name] of Object.entries(SESSIONS)) {
        const session = getSession(name);
        total++;

        if (session) {
            const status = session.running ? "● RECORDING" : "○ Ready";
            const time = session.running ? " (" + formatTime(session.runTime) + ")" : "";
            __console__.log("  " + status + "  " + name + time);

            if (session.running) running++;
        } else {
            __console__.log("  ✗ NOT FOUND  " + name);
        }
    }

    __console__.log("\n═══════════════════════════════════════════════════════");
    __console__.log("  " + running + "/" + total + " sessions active");
    __console__.log("═══════════════════════════════════════════════════════\n");

    // List recent recordings
    __console__.log("  Recent Recordings:");
    const recordings = __app__.recordings;
    const recent = recordings.slice(-5);
    for (const rec of recent) {
        __console__.log("    • " + rec.displayName + " (" + rec.displayTime + ")");
    }

    return { running: running, total: total };
}

/**
 * Format seconds to MM:SS
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins + ":" + (secs < 10 ? "0" : "") + secs;
}

/**
 * Start specific device session
 */
function startDevice(device) {
    const sessionName = SESSIONS[device.toUpperCase()];
    if (!sessionName) {
        __console__.error("Unknown device: " + device);
        return;
    }

    const session = getSession(sessionName);
    if (session) {
        if (!session.running) {
            session.start();
            __console__.log("✓ Started: " + sessionName);
            __console__.dialog(device + " capture started");
        } else {
            __console__.log("Already running: " + sessionName);
        }
    }
}

/**
 * Stop specific device session
 */
function stopDevice(device) {
    const sessionName = SESSIONS[device.toUpperCase()];
    if (!sessionName) {
        __console__.error("Unknown device: " + device);
        return;
    }

    const session = getSession(sessionName);
    if (session && session.running) {
        session.stop();
        __console__.log("✓ Stopped: " + sessionName);
        __console__.dialog(device + " capture stopped");
    }
}

/**
 * Start iPad + iPhone together (Satellite capture)
 */
function startSatellite() {
    __console__.log("Starting Satellite captures...");
    startDevice("ipad");
    startDevice("iphone");
    __console__.dialog("iPad + iPhone Satellite captures started");
}

/**
 * Configure recorder block output paths
 */
function configureRecorders() {
    __console__.log("Configuring recorder output paths...\n");

    for (const [key, sessionName] of Object.entries(SESSIONS)) {
        const session = getSession(sessionName);
        if (!session) continue;

        // Find recorder block in session
        const recorder = session.blockWithName("Recorder");
        if (recorder) {
            const outputPath = OUTPUTS[key] || OUTPUT_BASE + "/misc";
            recorder.folderPath = outputPath;
            __console__.log("  " + sessionName + " → " + outputPath);
        }
    }

    __console__.dialog("Recorder paths configured");
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN — Run when script is executed
// ═══════════════════════════════════════════════════════════════════════════════

// Show status by default
getStatus();

// Export functions for use as shortcuts
// To use: Create Script Shortcuts in Audio Hijack pointing to these functions

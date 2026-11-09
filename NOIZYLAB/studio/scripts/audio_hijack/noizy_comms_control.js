/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *     ███╗   ██╗ ██████╗ ██╗███████╗██╗   ██╗     ██████╗ ██████╗ ███╗   ███╗███╗   ███╗███████╗
 *     ████╗  ██║██╔═══██╗██║╚══███╔╝╚██╗ ██╔╝    ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔════╝
 *     ██╔██╗ ██║██║   ██║██║  ███╔╝  ╚████╔╝     ██║     ██║   ██║██╔████╔██║██╔████╔██║███████╗
 *     ██║╚██╗██║██║   ██║██║ ███╔╝    ╚██╔╝      ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║╚════██║
 *     ██║ ╚████║╚██████╔╝██║███████╗   ██║       ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║███████║
 *     ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝
 *
 *     BIG CONTROL FOR ALL COMMS
 *     M2 Ultra "God" (192GB) │ MacBook Pro │ iPad Pro 12.9 │ iPhone 15 Pro Max │ Neumann
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *     This is your COMMAND CENTER. Total control over all audio communications.
 *
 *     FEATURES:
 *     • Multi-device simultaneous capture
 *     • Live routing between devices
 *     • Auto-organization of recordings
 *     • Whisper transcription pipeline
 *     • Windsurf/Cascade audio feed
 *     • Logic Pro X integration
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const CONFIG = {
    // Base paths
    NOIZY_HOME: "~/NOIZYLAB",
    AUDIO_BASE: "~/NOIZYLAB/audio",

    // Output directories
    PATHS: {
        IPAD: "~/NOIZYLAB/audio/satellite_captures/ipad",
        IPHONE: "~/NOIZYLAB/audio/satellite_captures/iphone",
        NEUMANN: "~/NOIZYLAB/audio/neumann",
        MACBOOK: "~/NOIZYLAB/audio/macbook",
        MIXED: "~/NOIZYLAB/audio/satellite_captures/mixed",
        MASTERS: "~/NOIZYLAB/audio/masters",
        TRANSCRIPTS: "~/NOIZYLAB/audio/transcripts",
        TALESPIN: "~/NOIZYLAB/audio/talespin"
    },

    // Session names
    SESSIONS: {
        IPAD: "NOIZY iPad Satellite",
        IPHONE: "NOIZY iPhone Satellite",
        NEUMANN: "NOIZY Neumann Master",
        MACBOOK: "NOIZY MacBook Relay",
        DUAL: "NOIZY Dual Satellite",
        WINDSURF: "NOIZY to Windsurf",
        CASCADE: "NOIZY to Cascade",
        ALL_DEVICES: "NOIZY All Devices"
    },

    // Device info
    DEVICES: {
        GOD: {
            name: "M2 Ultra Mac Studio",
            nickname: "God",
            ram: "192GB",
            role: "Master Hub"
        },
        MACBOOK: {
            name: "MacBook Pro",
            ram: "16GB",
            role: "Mobile / Windsurf / Cascade"
        },
        IPAD: {
            name: "iPad Pro 12.9\"",
            generation: "2nd Gen",
            role: "Portable Voice Capture"
        },
        IPHONE: {
            name: "iPhone 15 Pro Max",
            role: "Field Capture"
        },
        NEUMANN: {
            name: "Neumann Microphone",
            connection: "XLR → Interface → God",
            role: "Primary Voice"
        }
    },

    // Recording settings
    RECORDING: {
        SAMPLE_RATE: 48000,
        BIT_DEPTH: 24,
        FORMAT: "WAV",
        FILENAME_TEMPLATE: "%device%_%date%_%time%"
    },

    // Automation
    AUTO_TRANSCRIBE: true,
    AUTO_ORGANIZE: true,
    NOTIFY_ON_COMPLETE: true
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMMS CONTROL CLASS
// ═══════════════════════════════════════════════════════════════════════════════

const CommsControl = {

    // ───────────────────────────────────────────────────────────────────────────
    // MASTER CONTROLS
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * LAUNCH ALL — Start every capture session
     */
    launchAll: function() {
        this.banner("LAUNCHING ALL COMMS");

        const sessions = __app__.sessions;
        let launched = 0;

        for (const sessionName of Object.values(CONFIG.SESSIONS)) {
            const session = __app__.sessionWithName(sessionName);
            if (session && !session.running) {
                session.start();
                __console__.log("  ✓ " + sessionName);
                launched++;
            } else if (session && session.running) {
                __console__.log("  ○ " + sessionName + " (already running)");
            }
        }

        this.notify("All Comms Launched", launched + " sessions started");
        __console__.log("\n  " + launched + " sessions launched");

        return launched;
    },

    /**
     * SHUTDOWN ALL — Stop everything
     */
    shutdownAll: function() {
        this.banner("SHUTTING DOWN ALL COMMS");

        __app__.stopAllSessions();

        this.notify("Comms Shutdown", "All sessions stopped");
        __console__.log("  ✓ All sessions stopped");
    },

    /**
     * PANIC STOP — Emergency stop all
     */
    panicStop: function() {
        __console__.log("\n  ⚠️  PANIC STOP ACTIVATED  ⚠️\n");
        __app__.stopAllSessions();
        this.notify("PANIC STOP", "All recording halted immediately");
    },

    // ───────────────────────────────────────────────────────────────────────────
    // DEVICE CONTROLS
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Control iPad capture
     */
    ipad: {
        start: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.IPAD);
            if (session) {
                session.start();
                CommsControl.configureRecorder(session, "ipad", CONFIG.PATHS.IPAD);
                CommsControl.notify("iPad", "Satellite capture started");
            }
        },
        stop: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.IPAD);
            if (session) session.stop();
        },
        status: function() {
            return CommsControl.getSessionStatus(CONFIG.SESSIONS.IPAD);
        }
    },

    /**
     * Control iPhone capture
     */
    iphone: {
        start: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.IPHONE);
            if (session) {
                session.start();
                CommsControl.configureRecorder(session, "iphone", CONFIG.PATHS.IPHONE);
                CommsControl.notify("iPhone", "Satellite capture started");
            }
        },
        stop: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.IPHONE);
            if (session) session.stop();
        },
        status: function() {
            return CommsControl.getSessionStatus(CONFIG.SESSIONS.IPHONE);
        }
    },

    /**
     * Control Neumann capture
     */
    neumann: {
        start: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.NEUMANN);
            if (session) {
                session.start();
                CommsControl.configureRecorder(session, "neumann", CONFIG.PATHS.NEUMANN);
                CommsControl.notify("Neumann", "Master capture started");
            }
        },
        stop: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.NEUMANN);
            if (session) session.stop();
        },
        status: function() {
            return CommsControl.getSessionStatus(CONFIG.SESSIONS.NEUMANN);
        }
    },

    /**
     * Control MacBook relay
     */
    macbook: {
        start: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.MACBOOK);
            if (session) {
                session.start();
                CommsControl.notify("MacBook", "Relay started");
            }
        },
        stop: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.MACBOOK);
            if (session) session.stop();
        }
    },

    /**
     * Start both iOS devices (Satellite)
     */
    satellite: {
        startBoth: function() {
            CommsControl.ipad.start();
            CommsControl.iphone.start();
            CommsControl.notify("Satellite", "iPad + iPhone capture active");
        },
        stopBoth: function() {
            CommsControl.ipad.stop();
            CommsControl.iphone.stop();
        }
    },

    // ───────────────────────────────────────────────────────────────────────────
    // AI INTEGRATION
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Route audio to Windsurf
     */
    toWindsurf: {
        start: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.WINDSURF);
            if (session) {
                session.start();
                CommsControl.notify("Windsurf", "Audio feed active");
                __console__.log("  Audio routing to Windsurf enabled");
            }
        },
        stop: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.WINDSURF);
            if (session) session.stop();
        }
    },

    /**
     * Route audio to Cascade
     */
    toCascade: {
        start: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.CASCADE);
            if (session) {
                session.start();
                CommsControl.notify("Cascade", "Audio feed active");
                __console__.log("  Audio routing to Cascade enabled");
            }
        },
        stop: function() {
            const session = __app__.sessionWithName(CONFIG.SESSIONS.CASCADE);
            if (session) session.stop();
        }
    },

    // ───────────────────────────────────────────────────────────────────────────
    // RECORDING MANAGEMENT
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Configure a recorder block
     */
    configureRecorder: function(session, deviceType, outputPath) {
        const recorder = session.blockWithName("Recorder");
        if (!recorder) return;

        // Set output folder
        recorder.folderPath = outputPath;

        // Set filename with timestamp
        const now = new Date();
        const timestamp = now.toISOString().slice(0, 19).replace(/[:.]/g, "-");
        recorder.fileName = deviceType + "_" + timestamp;

        // Set tags
        recorder.updateTags({
            artist: "NOIZY Studio",
            album: deviceType.toUpperCase() + " Recordings",
            comment: "Captured via NOIZY Comms Control",
            genre: "Voice Recording",
            year: now.getFullYear()
        });

        __console__.log("  Recorder configured: " + deviceType + " → " + outputPath);
    },

    /**
     * Get all recent recordings
     */
    listRecordings: function(limit) {
        limit = limit || 10;
        const recordings = __app__.recordings;
        const recent = recordings.slice(-limit).reverse();

        this.banner("RECENT RECORDINGS");

        for (const rec of recent) {
            __console__.log("  • " + rec.displayName);
            __console__.log("    " + rec.displayTime + " | " + this.formatSize(rec.fileSize));
            __console__.log("    " + rec.filePath);
            __console__.log("");
        }

        return recent;
    },

    /**
     * Organize recordings into folders
     */
    organizeRecordings: function() {
        this.banner("ORGANIZING RECORDINGS");

        const recordings = __app__.recordings;
        let moved = 0;

        for (const rec of recordings) {
            const fileName = rec.fileName.toLowerCase();
            let targetPath = CONFIG.PATHS.MASTERS;

            if (fileName.includes("ipad")) {
                targetPath = CONFIG.PATHS.IPAD;
            } else if (fileName.includes("iphone")) {
                targetPath = CONFIG.PATHS.IPHONE;
            } else if (fileName.includes("neumann")) {
                targetPath = CONFIG.PATHS.NEUMANN;
            } else if (fileName.includes("talespin")) {
                targetPath = CONFIG.PATHS.TALESPIN;
            }

            // Move if not already in correct location
            if (!rec.filePath.includes(targetPath.replace("~", ""))) {
                rec.moveFile(targetPath);
                __console__.log("  Moved: " + rec.fileName + " → " + targetPath);
                moved++;
            }
        }

        __console__.log("\n  " + moved + " files organized");
        return moved;
    },

    // ───────────────────────────────────────────────────────────────────────────
    // TRANSCRIPTION
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Transcribe a recording
     */
    transcribe: function(file) {
        const filePath = __app__.shellEscapeArgument(file.filePath);
        const outputDir = __app__.shellEscapeArgument(CONFIG.PATHS.TRANSCRIPTS);

        __console__.log("  Transcribing: " + file.fileName);

        // Use Whisper (run async to not block)
        const cmd = "nohup whisper " + filePath +
                   " --model large-v3 --output_dir " + outputDir +
                   " --output_format txt > /dev/null 2>&1 &";

        __app__.runShellCommand(cmd);
        __console__.log("  Transcription started (background)");

        this.notify("Transcription", "Processing: " + file.fileName);
    },

    /**
     * Batch transcribe recent recordings
     */
    transcribeRecent: function(count) {
        count = count || 3;
        const recordings = __app__.recordings.slice(-count);

        this.banner("BATCH TRANSCRIPTION");
        __console__.log("  Processing " + recordings.length + " recordings...\n");

        for (const rec of recordings) {
            this.transcribe(rec);
        }
    },

    // ───────────────────────────────────────────────────────────────────────────
    // STATUS & MONITORING
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Full system status
     */
    status: function() {
        __console__.clear();
        this.megaBanner();

        // Running sessions
        __console__.log("  ACTIVE SESSIONS:");
        __console__.log("  ─────────────────────────────────────────────────────");

        const running = __app__.runningSessions;
        if (running.length === 0) {
            __console__.log("    (no sessions running)");
        } else {
            for (const session of running) {
                const time = this.formatTime(session.runTime);
                __console__.log("    ● " + session.name + " [" + time + "]");
            }
        }

        // All sessions status
        __console__.log("\n  ALL SESSIONS:");
        __console__.log("  ─────────────────────────────────────────────────────");

        for (const [key, name] of Object.entries(CONFIG.SESSIONS)) {
            const session = __app__.sessionWithName(name);
            if (session) {
                const status = session.running ? "● RECORDING" : "○ Ready";
                const time = session.running ? " [" + this.formatTime(session.runTime) + "]" : "";
                __console__.log("    " + status + "  " + name + time);
            } else {
                __console__.log("    ✗ NOT FOUND  " + name);
            }
        }

        // Recent recordings
        __console__.log("\n  RECENT RECORDINGS:");
        __console__.log("  ─────────────────────────────────────────────────────");

        const recent = __app__.recordings.slice(-5);
        for (const rec of recent) {
            __console__.log("    • " + rec.displayName + " (" + rec.displayTime + ")");
        }

        // Device status
        __console__.log("\n  HARDWARE:");
        __console__.log("  ─────────────────────────────────────────────────────");
        __console__.log("    God (M2 Ultra 192GB)  │  Master Hub");
        __console__.log("    MacBook Pro 16GB      │  Windsurf + Cascade");
        __console__.log("    iPad Pro 12.9\" 2ndGen │  Satellite");
        __console__.log("    iPhone 15 Pro Max     │  Satellite");
        __console__.log("    Neumann Microphone    │  XLR → Interface");

        __console__.log("\n  ═══════════════════════════════════════════════════════\n");

        return {
            running: running.length,
            total: Object.keys(CONFIG.SESSIONS).length,
            recordings: __app__.recordings.length
        };
    },

    /**
     * Get single session status
     */
    getSessionStatus: function(sessionName) {
        const session = __app__.sessionWithName(sessionName);
        if (!session) return { exists: false };

        return {
            exists: true,
            name: session.name,
            running: session.running,
            runTime: session.runTime,
            recordings: session.recordings.length
        };
    },

    // ───────────────────────────────────────────────────────────────────────────
    // LOGIC PRO X INTEGRATION
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Open Logic Pro X
     */
    openLogic: function() {
        __app__.runShellCommand("open -a 'Logic Pro X'");
        this.notify("Logic Pro X", "Opening...");
    },

    /**
     * Send recording to Logic
     */
    sendToLogic: function(file) {
        file.openInApp("/Applications/Logic Pro X.app");
        this.notify("Logic Pro X", "Opened: " + file.fileName);
    },

    // ───────────────────────────────────────────────────────────────────────────
    // UTILITIES
    // ───────────────────────────────────────────────────────────────────────────

    /**
     * Show notification
     */
    notify: function(title, message) {
        const escapedTitle = __app__.shellEscapeArgument(title);
        const escapedMsg = __app__.shellEscapeArgument(message);

        __app__.runShellCommand(
            "osascript -e 'display notification " + escapedMsg +
            " with title \"NOIZY: " + escapedTitle + "\" sound name \"Glass\"'"
        );
    },

    /**
     * Format time duration
     */
    formatTime: function(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return mins + ":" + (secs < 10 ? "0" : "") + secs;
    },

    /**
     * Format file size
     */
    formatSize: function(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
        if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + " MB";
        return (bytes / 1073741824).toFixed(2) + " GB";
    },

    /**
     * Print section banner
     */
    banner: function(text) {
        __console__.log("\n  ═══════════════════════════════════════════════════════");
        __console__.log("    " + text);
        __console__.log("  ═══════════════════════════════════════════════════════\n");
    },

    /**
     * Print mega banner
     */
    megaBanner: function() {
        __console__.log("");
        __console__.log("  ╔═══════════════════════════════════════════════════════════╗");
        __console__.log("  ║                                                           ║");
        __console__.log("  ║   ███╗   ██╗ ██████╗ ██╗███████╗██╗   ██╗                 ║");
        __console__.log("  ║   ████╗  ██║██╔═══██╗██║╚══███╔╝╚██╗ ██╔╝                 ║");
        __console__.log("  ║   ██╔██╗ ██║██║   ██║██║  ███╔╝  ╚████╔╝                  ║");
        __console__.log("  ║   ██║╚██╗██║██║   ██║██║ ███╔╝    ╚██╔╝                   ║");
        __console__.log("  ║   ██║ ╚████║╚██████╔╝██║███████╗   ██║                    ║");
        __console__.log("  ║   ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝                    ║");
        __console__.log("  ║                                                           ║");
        __console__.log("  ║   COMMS CONTROL — BIG CONTROL FOR ALL COMMUNICATIONS     ║");
        __console__.log("  ║                                                           ║");
        __console__.log("  ╚═══════════════════════════════════════════════════════════╝");
        __console__.log("");
    },

    /**
     * Show help
     */
    help: function() {
        this.megaBanner();

        __console__.log("  COMMANDS:");
        __console__.log("  ─────────────────────────────────────────────────────────");
        __console__.log("");
        __console__.log("  MASTER:");
        __console__.log("    CommsControl.launchAll()      Start all sessions");
        __console__.log("    CommsControl.shutdownAll()    Stop all sessions");
        __console__.log("    CommsControl.panicStop()      Emergency stop");
        __console__.log("    CommsControl.status()         Full system status");
        __console__.log("");
        __console__.log("  DEVICES:");
        __console__.log("    CommsControl.ipad.start()     Start iPad capture");
        __console__.log("    CommsControl.iphone.start()   Start iPhone capture");
        __console__.log("    CommsControl.neumann.start()  Start Neumann capture");
        __console__.log("    CommsControl.satellite.startBoth()  Start iOS devices");
        __console__.log("");
        __console__.log("  AI INTEGRATION:");
        __console__.log("    CommsControl.toWindsurf.start()  Route to Windsurf");
        __console__.log("    CommsControl.toCascade.start()   Route to Cascade");
        __console__.log("");
        __console__.log("  RECORDINGS:");
        __console__.log("    CommsControl.listRecordings(10)  List recent");
        __console__.log("    CommsControl.organizeRecordings()  Auto-organize");
        __console__.log("    CommsControl.transcribeRecent(3)  Transcribe batch");
        __console__.log("");
        __console__.log("  ═══════════════════════════════════════════════════════\n");
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// AUTO-EXECUTE ON LOAD
// ═══════════════════════════════════════════════════════════════════════════════

// Check if this is an event or manual run
if (typeof __event__ !== 'undefined') {
    // Event-driven execution
    const eventType = __event__.eventType;

    switch (eventType) {
        case "runNow":
            CommsControl.status();
            break;
        case "sessionWillStart":
            __console__.log("Session starting: " + __event__.session.name);
            break;
        case "sessionDidStop":
            __console__.log("Session stopped: " + __event__.session.name);
            break;
        case "fileDidEnd":
            const file = __event__.file;
            __console__.log("Recording complete: " + file.fileName);
            if (CONFIG.AUTO_TRANSCRIBE) {
                CommsControl.transcribe(file);
            }
            break;
    }
} else {
    // Manual execution — show status
    CommsControl.status();
}

// Make CommsControl globally available
this.CommsControl = CommsControl;
this.CC = CommsControl;  // Short alias

/**
 * 👑 GABRIEL CORE (CLIENT SIDE)
 * The Frontend Intelligence Bridge for MC96ECOUNIVERSE.
 * 
 * "I translate the binary will of the Server into the fluid reality of the Browser."
 */

class GabrielCore {
    constructor() {
        this.status = "OFFLINE";
        this.vibe = 50;
        this.serverUrl = ""; // Relative path usually
        this.pingInterval = null;
        
        console.log("%c 👑 GABRIEL CORE INITIALIZED ", "background: #000; color: #00ffcc; font-size: 14px; padding: 5px; border: 1px solid #00ffcc;");
    }

    async connect() {
        try {
            const res = await fetch('/api/stats');
            if (res.ok) {
                this.status = "ONLINE";
                console.log("⚡ GABRIEL: Connected to Nexus Server.");
                this.startHeartbeat();
                return true;
            }
        } catch (e) {
            console.error("❌ GABRIEL: Connection Failed.", e);
            this.status = "DISCONNECTED";
            return false;
        }
    }

    startHeartbeat() {
        this.pingInterval = setInterval(async () => {
            // Pulse check logic could go here
        }, 5000);
    }

    /**
     * OMNI-SEARCH
     * Finds sounds, files, or concepts.
     */
    async search(query) {
        if (!query) return [];
        console.log(`👁️ GABRIEL: Searching for '${query}'...`);
        
        try {
            const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            console.log(`   found ${data.length} results.`);
            return data;
        } catch (e) {
            console.error("Search Error:", e);
            return [];
        }
    }

    /**
     * TRIGGER BACKEND ACTION
     */
    async command(cmd) {
        console.log(`⚡ GABRIEL: COMMAND > ${cmd}`);
        fetch(`/api/action?cmd=${cmd}`);
    }

    /**
     * LOG EVENT TO MEMCELL (via Server)
     * (Placeholder for future API expansion)
     */
    logExposure(filename) {
        // Tell the server we listened to this
        // fetch('/api/log_event', ...)
    }
}

// Global Singleton
window.Gabriel = new GabrielCore();

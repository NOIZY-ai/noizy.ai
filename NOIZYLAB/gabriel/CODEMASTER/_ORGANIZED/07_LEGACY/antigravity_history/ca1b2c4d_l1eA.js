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
        
        this.avatarElement = document.getElementById('gabriel-avatar');
        console.log("%c 👑 GABRIEL CORE INITIALIZED ", "background: #000; color: #00ffcc; font-size: 14px; padding: 5px; border: 1px solid #00ffcc;");
    }

    setVisualState(state) {
        if (!this.avatarElement) return;
        this.avatarElement.classList.remove('speaking', 'thinking');
        if (state === 'speaking') this.avatarElement.classList.add('speaking');
        if (state === 'thinking') this.avatarElement.classList.add('thinking');
    }

    setPersona(name) {
        if (!this.avatarElement) return;
        const personas = ['titan', 'solar', 'void', 'nature'];
        this.avatarElement.classList.remove(...personas);
        if (personas.includes(name.toLowerCase())) {
            this.avatarElement.classList.add(name.toLowerCase());
            console.log(`🎭 GABRIEL: Persona Switched to [${name.toUpperCase()}]`);
        } else {
            this.avatarElement.classList.add('titan'); // Default
        }
    }

    async connect() {
        try {
            const res = await fetch('/api/stats');
            if (res.ok) {
                this.status = "ONLINE";
                console.log("⚡ GABRIEL: Connected to Nexus Server.");
                this.setVisualState('idle');
                this.setPersona('titan'); // Default start
                this.startHeartbeat();
                this.startVisualizer(); // Start the render loop
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

    startVisualizer() {
        const update = () => {
            if (window.AudioEngine && window.AudioEngine.isPlaying && this.avatarElement) {
                // Get FFT data
                const data = window.AudioEngine.getVisualData(); 
                if (data) {
                    // Average the bass frequencies (roughly first 20 bins)
                    let sum = 0;
                    for(let i=0; i<20; i++) sum += data[i];
                    const avg = sum / 20;
                    
                    // Scale factor: 1.0 to 1.5 roughly
                    const scale = 1.0 + (avg / 255) * 0.5;
                    
                    // Apply, preserving rotation if thinking
                    const isThinking = this.avatarElement.classList.contains('thinking');
                    // We can't easily mix CSS animation transform with JS transform without one overriding.
                    // Simple fix: Only apply audio pulse if NOT thinking or speaking (which use their own animations).
                    if (!this.avatarElement.classList.contains('thinking') && !this.avatarElement.classList.contains('speaking')) {
                         this.avatarElement.style.transform = `scale(${scale})`;
                         this.avatarElement.style.animation = 'none'; // Pause idle animation while music controls it
                    } else {
                         this.avatarElement.style.transform = ''; // Clear JS override
                         this.avatarElement.style.animation = ''; // Let CSS take over
                    }
                }
            } else if (this.avatarElement) {
                 // Reset if stopped
                 if (this.avatarElement.style.transform) {
                     this.avatarElement.style.transform = '';
                     this.avatarElement.style.animation = ''; // Resume idle
                 }
            }
            requestAnimationFrame(update);
        };
        update();
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
        this.setVisualState('thinking');
        console.log(`⚡ GABRIEL: COMMAND > ${cmd}`);
        await fetch(`/api/action?cmd=${cmd}`);
        setTimeout(() => this.setVisualState('idle'), 1000);
    }
    
    /**
     * SPEAK (Voice Output)
     */
    async speak(text, persona="titan") {
        console.log(`🗣️ GABRIEL SPEAKING: "${text}"`);
        this.setVisualState('thinking');
        
        // 1. Request Audio Generation from Server/Voice Bridge
        // Assuming /api/gabriel/command can handle 'speak' or we have a specialized endpoint.
        // Let's use the 'speak' command via CLI wrapper or direct if exposed.
        // Actually, we should probably hit the voice worker directly if possible, or use the server proxy.
        // Let's use the server's /api/generate/audio if configured for TTS, or just trigger the system command.
        
        // Option A: Trigger backend command (Server plays it) -> This is "God Mode" (System speaks)
        // fetch(`/api/gabriel/command?cmd=speak&args=${encodeURIComponent(text)}`);
        
        // Option B: Browser plays it (Avatar speaks) -> Requires getting audio blob back.
        // For now, let's trigger the system voice to unify with the new Voice Bridge.
        
        // Update Persona Visual if provided
        if(persona) this.setPersona(persona);

        await fetch(`/api/gabriel/command?cmd=speak&args="${encodeURIComponent(text)}" --persona ${persona}`);
        
        // Simulate Speaking Visuals (since we don't have accurate end-of-audio event yet without complex piping)
        this.setVisualState('speaking');
        const duration = Math.min(text.length * 100, 5000); // Rough estimate
        setTimeout(() => this.setVisualState('idle'), duration);
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

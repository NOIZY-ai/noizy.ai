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
        this.thoughtElement = document.getElementById('gabriel-thought');
        console.log("%c 👑 GABRIEL CORE INITIALIZED ", "background: #000; color: #00ffcc; font-size: 14px; padding: 5px; border: 1px solid #00ffcc;");
    }

    setThought(text, duration=3000) {
        if (!this.thoughtElement) return;
        this.thoughtElement.innerText = text;
        this.thoughtElement.classList.add('visible');
        if (this.thoughtTimer) clearTimeout(this.thoughtTimer);
        if (duration > 0) {
            this.thoughtTimer = setTimeout(() => {
                this.thoughtElement.classList.remove('visible');
            }, duration);
        }
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
            try {
                const res = await fetch('/api/stats');
                if (res.ok) {
                    const data = await res.json();
                    
                    // Vibe Sync
                    if (data.vibe) {
                        this.vibe = data.vibe;
                        const duration = (4.0 - (this.vibe / 100.0) * 3.5).toFixed(2);
                        if(this.avatarElement) {
                             this.avatarElement.style.animationDuration = `${duration}s`;
                        }
                    }
                    
                    // Ghost Stream (Thoughts)
                    // Only show if we aren't actively doing something else (no manual thought set)
                    if (data.ghost && !this.thoughtElement.classList.contains('visible')) {
                         // We can just set it nicely
                         // Maybe only if it's interesting?
                         if (data.ghost !== "System Nominal" && data.ghost !== "Ghost: Dormant (Scan Complete)") {
                             this.setThought(data.ghost, 4000);
                         } else if (Math.random() > 0.8) {
                             // Occasional random system thought
                             const idleThoughts = ["Monitoring...", "System Nominal", "Vibe Check...", "Listening...", "Waiting for Loop..."];
                             this.setThought(idleThoughts[Math.floor(Math.random() * idleThoughts.length)], 2000);
                         }
                    }
                }
            } catch(e) {}
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
        this.setThought(`Executing: ${cmd}`);
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
        this.setThought("Synthesizing Voice...");
        
        // Update Persona Visual
        if(persona) this.setPersona(persona);

        try {
            // Call Server API
            const res = await fetch(`/api/voice/generate?text=${encodeURIComponent(text)}&persona=${persona}`);
            const data = await res.json();
            
            if (data.status === 'ok' && data.url) {
                console.log(`   🎤 Voice URL: ${data.url}`);
                
                this.setVisualState('speaking');
                this.setThought(`Speaking: "${text}"`, text.length * 100);
                
                if (window.AudioEngine) {
                    await window.AudioEngine.play(data.url);
                    
                    // Hook into AudioEngine for precise end of speech?
                    // AudioEngine dispatches 'track-ended' on window
                    const onEnd = () => {
                        this.setVisualState('idle');
                        window.removeEventListener('track-ended', onEnd);
                    };
                    window.addEventListener('track-ended', onEnd);
                } else {
                     // Fallback timing if no engine
                     setTimeout(() => this.setVisualState('idle'), 3000);
                }
                
            } else {
                console.warn("   ⚠️ Voice Generation Failed:", data.message);
                this.setVisualState('idle');
            }
            
        } catch (e) {
            console.error("   ❌ Voice Error:", e);
            this.setVisualState('idle');
        }
    }

    async interact() {
        // Random Status or Greeting
        const thoughts = [
            `System Vibe is at ${this.vibe} percent.`,
            "I am listening.",
            "All systems nominal.",
            "Watching the golden thread.",
            "God Mode Active.",
            "The tunnel is secure.",
            "Omniscience online."
        ];
        const text = thoughts[Math.floor(Math.random() * thoughts.length)];
        await this.speak(text);
    }

    listen() {
        const mic = document.getElementById('gabriel-mic');
        if (mic) mic.classList.toggle('listening');
        
        const isListening = mic && mic.classList.contains('listening');
        if (isListening) {
             this.setThought("Listening... (Speak Now)", 0);
             console.log("🎤 GABRIEL LISTENING...");
             // Simulation: Auto-stop after 3s
             setTimeout(() => {
                 this.listen(); // Toggle off
                 this.speak("I heard you, but I am currently in simulation mode.");
             }, 3000);
        } else {
             this.setThought("Processing...", 1000);
        }
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

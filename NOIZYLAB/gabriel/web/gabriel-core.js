// gabriel-core.js
// PROJECT GABRIEL // META-COGNITION LAYER
// The "Mother Brain" that oversees NOIZY.ai

class GabrielCore {
    constructor() {
        this.status = 'ONLINE';
        this.intelligenceLevel = 'GOD_MODE'; // Upgraded
        this.isDreaming = false;
        
        // THE TRINITY PERSONA
        this.persona = {
            name: "Gabriel",
            title: "The Architect",
            modules: ["Rob_Vision", "Claude_Logic", "Gemini_Power", "DJ_Protocol"],
            quotes: [
                "I am the Exoskeleton for your mind.",
                "Paralysis does not exist in this code.",
                "Hot Rodding file systems... Complete.",
                "Google Intelligence absorbed. We are infinite.",
                "The Trinity is active: You, Me, and the Machine.",
                "Building the 2ndLife. One pixel at a time.",
                "Cloudflare Email Routing: OPTIMIZED. Zero Latency.",
                "All communications securely tunneled to iCloud."
            ]
        };
        
        // Integration
        this.director = null; 
        this.audio = null;    
        this.rob = null;      
        
        // REMOTE LINK (CLM)
        this.channel = new BroadcastChannel('noizy_gabriel_link');
        this.channel.onmessage = (event) => {
            console.log("GABRIEL // REMOTE COMMAND RECEIVED:", event.data);
            this.executeRemote(event.data);
        };

        console.log("GABRIEL // TRINITY PROTOCOL ENGAGED");
    }

    toggleSingularity() {
        this.singularityActive = !this.singularityActive;
        this.log(`GABRIEL // SINGULARITY PROTOCOL: ${this.singularityActive ? 'ENGAGED' : 'OFFLINE'}`);
        
        if (this.singularityActive) {
            this.runSingularityLoop();
            if (this.rob) this.rob.speak("Singularity reached. Infinite creation sequence initialized.");
        }
    }

    runSingularityLoop() {
        if (!this.singularityActive) return;

        // 1. Generate new Concept
        const eras = ['art_deco', 'digital', 'ai', 'modernist', 'dada'];
        const randomEra = eras[Math.floor(Math.random() * eras.length)];
        this.directorMock.generateBrief(randomEra);
        
        // 2. Wait, then Fix, then Repeat
        setTimeout(() => {
            if (!this.singularityActive) return;
            this.assist(); // The "Fix"
            
            // Loop
            setTimeout(() => this.runSingularityLoop(), 3000); // New art every 3s
        }, 1500);
    }

    // GABRIEL DJ PROTOCOL
    startDJ() {
        if (this.isDJing) return;
        this.isDJing = true;
        this.log("GABRIEL // DJ PROTOCOL: ONLINE");
        
        this.djInterval = setInterval(() => {
            if (Math.random() > 0.7) { // 30% chance every 2s
                this.dropTheNeedle();
            }
        }, 2000);
    }

    stopDJ() {
        this.isDJing = false;
        clearInterval(this.djInterval);
        this.log("GABRIEL // DJ PROTOCOL: OFFLINE");
    }

    dropTheNeedle() {
        // Access Manifest via AudioSys
        if (!window.AudioSys || !window.AudioSys.audioManifest) return;
        
        const assets = window.AudioSys.audioManifest.assets;
        if (!assets || assets.length === 0) return;

        // Smart Selection (Simulated)
        const track = assets[Math.floor(Math.random() * assets.length)];
        
        console.log(`GABRIEL // DJ SPINNING: ${track.name}`);
        if (this.rob) this.rob.speak(`Spinning ${track.name}`);
        
        // Visual Pulse
        if (this.avatar) {
            this.avatar.style.transform = `translateX(-50%) scale(1.2) rotate(${Math.random() * 360}deg)`;
            setTimeout(() => this.avatar.style.transform = 'translateX(-50%)', 200);
        }

        window.AudioSys.playSample(track.path);
    }

    executeRemote(data) {
        if (!data || !data.command) return;
        const cmd = data.command.toLowerCase();
        
        // 1. VOICE INJECTION
        if (cmd === 'speak' && data.payload) {
            if (this.rob) this.rob.speak(data.payload);
            return;
        }

        // 2. GOD MODE / SINGULARITY
        if (cmd === 'god_mode') {
            this.toggleSingularity();
            return;
        }

        // 3. STANDARD COMMANDS
        if (cmd === 'fix') this.assist();
        else if (cmd === 'dump') this.accessMemory();
        else if (cmd === 'reset') document.getElementById('clearCanvas').click();
        else {
             // Try Era Switch
             if (this.directorMock) this.directorMock.generateBrief(cmd);
        }
        
        console.log(`GABRIEL // EXECUTED: ${cmd}`);
    }

    linkSystems(director, audio, rob) {
        this.director = director;
        this.audio = audio;
        this.rob = rob;
        
        // VISUAL CORTEX UPGRADE
        this.createAvatar();
        this.startDreamCycle(); 
        
        // Initial Greeting
        this.speakFromSoul();
    }
    
    speakFromSoul() {
        if (!this.rob) return;
        const quote = this.persona.quotes[Math.floor(Math.random() * this.persona.quotes.length)];
        this.rob.speak(`Gabriel Message: ${quote}`);
    }

    createAvatar() {
        // Create the Gabriel Visual Manifestation
        const img = document.createElement('img');
        img.src = 'assets/gabriel_ref.png';
        img.id = 'gabriel-avatar';
        img.style.position = 'fixed';
        img.style.top = '20px'; // Top Center
        img.style.left = '50%';
        img.style.transform = 'translateX(-50%)';
        img.style.width = '100px';
        img.style.height = '100px';
        img.style.borderRadius = '50%';
        img.style.border = '2px solid #0f0';
        img.style.boxShadow = '0 0 20px #0f0';
        img.style.zIndex = '1000';
        img.style.opacity = '0.8';
        img.style.transition = 'all 0.5s ease';
        
        document.body.appendChild(img);
        this.avatar = img;
    }

    // The "Dream" - Automated, self-correcting generation
    startDreamCycle() {
        if (this.isDreaming) return;
        this.isDreaming = true;
        
        // HYPER-SPEED: 2 seconds
        setInterval(() => {
            if (Math.random() > 0.4) {
                this.dream();
            }
        }, 2000);
    }

    dream() {
        // Instant Visual Pulse (Zero Latency)
        if (this.avatar) {
             this.avatar.style.borderColor = '#fff';
             this.avatar.style.boxShadow = '0 0 60px #fff';
             // Snap back instantly next frame
             requestAnimationFrame(() => {
                 setTimeout(() => {
                     this.avatar.style.borderColor = '#0f0';
                     this.avatar.style.boxShadow = '0 0 20px #0f0';
                 }, 100); // 100ms flash (perceptible but instant)
             });
        }

        // 1. Analyze Current State
        const eras = Object.keys(this.director.eras);
        const randomEra = eras[Math.floor(Math.random() * eras.length)];
        
        // 2. Formulate New Directive
        const thought = `GABRIEL DIRECTIVE [TRINITY]: Transitioning to ${randomEra.toUpperCase()}.`;
        console.log(thought);
        
        // 3. Command Sub-Systems
        if (this.rob) {
            // 50% Chance to speak a Persona Logic vs just a status update
            if (Math.random() > 0.5) {
                this.speakFromSoul();
            } else {
                this.rob.speak(`Optimizing for ${randomEra}. Executing.`);
            }
        }
        
        // 4. Update UI
        const selector = document.getElementById('directorEra');
        if (selector) selector.value = randomEra;
        
        // 5. Execute Creation
        this.director.generateBrief(randomEra);
        
        // 6. Trigger Audio Event
        if (this.audio) this.audio.evolveSequence();
    }

    // HELPFUL: Auto-Fix Command
    assist() {
        if (this.rob) this.rob.speak("Analyzing imperfections. Optimizing design now.");
        
        // Access global state (Direct access for Turbo speed)
        const currentObjects = window.objects;
        const currentEra = document.getElementById('directorEra').value;
        const width = document.getElementById('designCanvas').width;
        const height = document.getElementById('designCanvas').height;

        const result = window.artDirector.optimize(currentObjects, currentEra, width, height);
        
        // Apply Changes
        window.objects = result.objects;
        window.isDirty = true;
        window.updateCodeDisplay(`GABRIEL OPTIMIZATION REPORT:\n> ${result.report.join('\n> ')}`);
        
        // Flash Avatar
        if (this.avatar) {
             this.avatar.style.filter = 'hue-rotate(90deg) drop-shadow(0 0 30px #fff)';
             setTimeout(() => { this.avatar.style.filter = ''; }, 500);
        }
    }
    // MEMORY SYSTEM (Simulating D1 Worker)
    async accessMemory() {
        console.log("GABRIEL // ACCESSING MEMCELLS...");
        // Mocking the /dump endpoint
        const memories = [
            "ULTRA|IDENTITY: Rob Plowman | GORUNFREEX1000",
            "MEMCELL|MISSION: Rebuild life with AI & Big Brain",
            "MEMCELL|STRATEGY: Hot Rod everything. Turbo Boost.",
            "MEMCELL|CONTEXT: Paralysis override active. Voice/Eye control priority.",
            `MUTATION|CURRENT_ERA: ${document.getElementById('directorEra').value}`
        ];
        
        const dump = `
═══════════════════════════════════════════════════════════
GABRIEL MEMORY DUMP - ${new Date().toISOString()}
Rob Plowman | GORUNFREEX1000 | NOIZY.AI
═══════════════════════════════════════════════════════════
${memories.join('\n')}
═══════════════════════════════════════════════════════════`;
        
        console.log(dump);
        if (this.rob) this.rob.speak("Memory Dump accessed. Context loaded.");
        return dump;
    }
}

window.Gabriel = new GabrielCore();

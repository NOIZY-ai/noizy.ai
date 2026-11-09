// gabriel-core.js
// PROJECT GABRIEL // META-COGNITION LAYER
// The "Mother Brain" that oversees NOIZY.ai

class GabrielCore {
    constructor() {
        this.status = 'ONLINE';
        this.intelligenceLevel = 'HYPER';
        this.observers = [];
        this.isDreaming = false;
        
        // Integration
        this.director = null; // Link to ArtDirector
        this.audio = null;    // Link to AudioEngine
        this.rob = null;      // Link to NLRR01
        
        console.log("GABRIEL // CORE INITIALIZED");
    }

    linkSystems(director, audio, rob) {
        this.director = director;
        this.audio = audio;
        this.rob = rob;
        
        // VISUAL CORTEX UPGRADE
        this.createAvatar();
        this.startDreamCycle();
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
        
        // Every 5 seconds (Turbo Boost), Gabriel acts
        setInterval(() => {
            if (Math.random() > 0.3) {
                this.dream();
            }
        }, 5000);
    }

    dream() {
        // Pulse Avatar
        if (this.avatar) {
             this.avatar.style.transform = 'translateX(-50%) scale(1.2)';
             this.avatar.style.boxShadow = '0 0 50px #0f0';
             setTimeout(() => {
                 this.avatar.style.transform = 'translateX(-50%) scale(1.0)';
                 this.avatar.style.boxShadow = '0 0 20px #0f0';
             }, 500);
        }

        // 1. Analyze Current State
        const eras = Object.keys(this.director.eras);
        const randomEra = eras[Math.floor(Math.random() * eras.length)];
        
        // 2. Formulate New Directive
        const thought = `GABRIEL DIRECTIVE: Transitioning to ${randomEra.toUpperCase()} for optimization.`;
        console.log(thought);
        
        // 3. Command Sub-Systems
        if (this.rob) this.rob.speak(`Gabriel Override. Changing paradigm to ${randomEra}.`);
        
        // 4. Update UI
        const selector = document.getElementById('directorEra');
        if (selector) selector.value = randomEra;
        
        // 5. Execute Creation
        this.director.generateBrief(randomEra);
        
        // 6. Trigger Audio Event
        if (this.audio) this.audio.evolveSequence();
    }
}

window.Gabriel = new GabrielCore();

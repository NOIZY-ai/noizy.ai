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
        this.startDreamCycle();
    }

    // The "Dream" - Automated, self-correcting generation
    startDreamCycle() {
        if (this.isDreaming) return;
        this.isDreaming = true;
        
        // Every 8 seconds, Gabriel decides to change the world
        setInterval(() => {
            if (Math.random() > 0.3) {
                this.dream();
            }
        }, 8000);
    }

    dream() {
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

// repair-rob.js
// NLRR01 - "Repair-Rob"
// The AI Host of NOIZY.ai

class RepairRob {
    constructor() {
        this.active = false;
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'rob-avatar';
        this.ctx = this.canvas.getContext('2d');
        this.voice = null;
        this.speaking = false;
        
        // Config
        this.canvas.width = 200;
        this.canvas.height = 200;
        this.canvas.style.position = 'fixed';
        this.canvas.style.bottom = '20px';
        this.canvas.style.right = '20px';
        this.canvas.style.index = '9999';
        this.canvas.style.pointerEvents = 'none'; // Click through
        this.canvas.style.filter = 'drop-shadow(0 0 10px #00ffcc)';
        
        document.body.appendChild(this.canvas);
        
        // Animation State
        this.time = 0;
        this.pulse = 0;
        
        this.mode = 'CREATIVE'; // Modes: CREATIVE, SERVICE, OMNISCIENT
        
        // THE OMNIBUS: ALL Apple & Windows Knowledge (Past -> Future)
        this.omnibus = {
            apple: [
                "Apple I (1976) - MOS 6502", "Macintosh 128K (1984) - Hello", 
                "System 7 (1991)", "macOS X Cheetah (2001)", 
                "M2 Ultra (2023)", "Vision Pro (2024)",
                "macOS Nebula (2028) - Neural Core", "Apple Quantum (2035)"
            ],
            windows: [
                "Windows 1.0 (1985)", "Windows 95 (1995) - Chicago",
                "Windows XP (2001) - Bliss", "Windows 11 (2021) - Sun Valley",
                "Windows 12 (2024) - AI Core", 
                "Windows Infinite (2030) - Cloud OS", "Microsoft Singularity (2045)"
            ],
            code: [
                "Assembly", "C", "Objective-C", "Swift", "C#", ".NET", 
                "Rust", "Quantum-Script", "Universal Binary v9"
            ]
        };
        
        this.initVoice();
        this.startLoop();
    }
    
    // OMNISCIENT SERVICE MODES
    setServiceMode(mode) {
        this.mode = mode;
        if (mode === 'SERVICE') {
            this.speak("Mode switched. Remote Service Protocol initiated. Accessing Global Root.");
            this.eyeColor = '#FF0000'; // Tech Support Red
        } else if (mode === 'OMNISCIENT') {
            this.speak("I see everything. Apple. Windows. The Beginning. The End.");
            this.eyeColor = '#FFFFFF'; // Pure Light
        } else {
             this.speak("Returning to Creative Director mode.");
             this.eyeColor = '#00FF41'; // Matrix Green
        }
    }

    queryOmnibus(topic) {
        this.speak("Accessing Deep Storage...");
        
        let data = [];
        if (topic.includes('apple') || topic.includes('mac')) data = this.omnibus.apple;
        if (topic.includes('win') || topic.includes('pc')) data = this.omnibus.windows;
        
        if (data.length > 0) {
            const fact = data[Math.floor(Math.random() * data.length)];
            // Simulated Future Prediction
            if (fact.includes('20') && parseInt(fact.split('(')[1]) > 2025) {
                 this.speak(`FUTURE SIGHT ACTIVATED. Timeline: ${fact}. Warning: Protocol Unstable.`);
            } else {
                 this.speak(`Retrieving Data: ${fact}. optimized code found.`);
            }
            return fact;
        } else {
            this.speak("Query unclear. Please specify Apple or Windows vector.");
        }
    }
    
    initVoice() {
        // Wait for voices to load
        window.speechSynthesis.onvoiceschanged = () => {
            const voices = window.speechSynthesis.getVoices();
            // Try to find a "Robotic" or deep voice
            this.voice = voices.find(v => v.name.includes('Google US English')) || 
                         voices.find(v => v.name.includes('Samantha')) || 
                         voices[0];
            console.log("NLRR01 Voice initialized:", this.voice.name);
        };
    }

    speak(text) {
        if (!this.voice) return;
        
        // Cancel previous
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = this.voice;
        utterance.pitch = 0.8; // Lower pitch for Rob
        utterance.rate = 1.1; // Slightly faster
        utterance.volume = 1.0;
        
        utterance.onstart = () => { this.speaking = true; };
        utterance.onend = () => { this.speaking = false; };
        
        window.speechSynthesis.speak(utterance);
    }
    
    startLoop() {
        const loop = () => {
            if (this.ctx) this.draw();
            requestAnimationFrame(loop);
        };
        loop();
    }

    draw() {
        this.time += 0.05;
        this.pulse = Math.sin(this.time) * 10;
        const w = this.canvas.width;
        const h = this.canvas.height;
        const ctx = this.ctx;

        ctx.clearRect(0, 0, w, h);
        
        // Glitch Shake
        const ox = this.speaking ? (Math.random() - 0.5) * 5 : 0;
        const oy = this.speaking ? (Math.random() - 0.5) * 5 : 0;
        
        ctx.save();
        ctx.translate(w/2 + ox, h/2 + oy);
        
        // "Eye" (HAL-9000 style / Iron Man)
        const scale = this.speaking ? (1 + Math.random() * 0.2) : (this.eyeScale || 1);
        
        ctx.fillStyle = '#000'; // Original core color
        ctx.beginPath();
        ctx.arc(0, 0, 60 * scale, 0, Math.PI*2); // Apply scale to core
        ctx.fill();
        
        ctx.strokeStyle = this.color; // Use new color property
        ctx.lineWidth = 3;
        ctx.stroke();

        // Inner Iris (Glow)
        ctx.fillStyle = this.speaking ? '#ff00ff' : this.color; // Reactive color
        const irisSize = this.speaking ? 20 + Math.random()*20 : 20 + this.pulse * 0.5;
        ctx.beginPath();
        ctx.arc(0, 0, irisSize * scale, 0, Math.PI*2); // Apply scale to iris
        ctx.fill();
        
        // Scanner Ring
        ctx.strokeStyle = this.color; // Use new color property
        ctx.lineWidth = 2; // Adjusted line width
        ctx.beginPath();
        ctx.arc(0, 0, 70 + (Math.sin(Date.now() / 200) * 5), 0, Math.PI * 2); // New scanner ring animation
        ctx.stroke();

        if (this.speaking) {
             // Waveform visualization simulation
             ctx.strokeStyle = this.color;
             ctx.lineWidth = 1;
             ctx.beginPath();
             ctx.moveTo(-50, 80);
             for(let i=0; i<100; i+=10) {
                 ctx.lineTo(-50 + i, 80 + (Math.random()*20 - 10));
             }
             ctx.stroke();
        }
        
        // 4. Data Streams (Original)
        ctx.fillStyle = 'rgba(0, 255, 204, 0.5)';
        ctx.font = '10px monospace';
        ctx.fillText(`NLRR01 // ${Math.floor(this.time * 100)}`, -50, 90);

        ctx.restore();
    }
}

// Global accessor
window.Rob = null;
window.initRob = () => {
    window.Rob = new RepairRob();
    window.Rob.speak("Hello Rob. Antigravity Systems connected. Zero Latency Mode confirmed.");
};

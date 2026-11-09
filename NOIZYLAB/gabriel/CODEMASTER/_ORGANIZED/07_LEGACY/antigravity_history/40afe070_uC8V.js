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
        
        this.initVoice();
        this.startLoop();
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
        
        // 1. Core (The Eye)
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(0, 0, 60, 0, Math.PI*2);
        ctx.fill();
        
        ctx.strokeStyle = '#00ffcc';
        ctx.lineWidth = 3;
        ctx.stroke();

        // 2. Iris (Reactive)
        ctx.fillStyle = this.speaking ? '#ff00ff' : '#00ffcc';
        const irisSize = this.speaking ? 20 + Math.random()*20 : 20 + this.pulse * 0.5;
        ctx.beginPath();
        ctx.arc(0, 0, irisSize, 0, Math.PI*2);
        ctx.fill();

        // 3. Scanner Ring
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(0, 0, 70 + this.pulse, this.time, this.time + 1.5);
        ctx.stroke();
        
        // 4. Data Streams
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
    window.Rob.speak("System Online. I am Repair Rob. Welcome to Noisy A.I.");
};

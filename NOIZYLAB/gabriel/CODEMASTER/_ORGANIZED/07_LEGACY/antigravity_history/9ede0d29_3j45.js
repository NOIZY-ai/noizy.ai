// audio-engine.js
// NOIZY.ai "Audio Arsenal"
// 0% Latency Audio Generation

class AudioEngine {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = 0.3; // Prevent ear blasting
        this.masterGain.connect(this.ctx.destination);
    }

    playTone(freq, type = 'sine', duration = 0.1) {
        if (this.ctx.state === 'suspended') this.ctx.resume();

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        
        gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + duration);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start();
        osc.stop(this.ctx.currentTime + duration);
    }

    // "FishMusic" Generative Sequencer
    playSequence(bpm = 120) {
        if (this.ctx.state === 'suspended') this.ctx.resume();
        
        const noteDuration = 60 / bpm / 2; // 8th notes
        const scale = [220, 261.63, 293.66, 329.63, 392.00, 440, 523.25]; // A Minor Pentatonic
        let step = 0;

        if (this.sequencer) clearInterval(this.sequencer);

        this.sequencer = setInterval(() => {
            // Generative Logic: 50% chance to play a note per step
            if (Math.random() > 0.5) {
                const freq = scale[Math.floor(Math.random() * scale.length)];
                
                // Oscillator 1 (Bass/Lead)
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                
                osc.type = Math.random() > 0.5 ? 'square' : 'sawtooth';
                osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
                
                // Envelope
                gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                
                osc.connect(gain);
                gain.connect(this.masterGain);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.2);
            }
            
            // Rhythm (Hi-hat click) every 4 steps
            if (step % 4 === 0) {
                 const osc = this.ctx.createOscillator();
                 const gain = this.ctx.createGain();
                 osc.type = 'triangle';
                 osc.frequency.setValueAtTime(1000 + Math.random()*2000, this.ctx.currentTime);
                 gain.gain.setValueAtTime(0.05, this.ctx.currentTime);
                 gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);
                 osc.connect(gain);
                 gain.connect(this.masterGain);
                 osc.start();
                 osc.stop(this.ctx.currentTime + 0.05);
            }

            step++;
        }, noteDuration * 1000);
    }

    evolveSequence() {
        // Change BPM or Scale dynamically (Mock evolution)
        this.playSequence(120 + Math.random() * 40);
    }
}

window.AudioSys = new AudioEngine();

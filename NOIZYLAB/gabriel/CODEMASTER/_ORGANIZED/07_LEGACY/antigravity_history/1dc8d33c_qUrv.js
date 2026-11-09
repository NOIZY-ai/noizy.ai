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

    // "Flow" Sound - Generative ambient texture
    playFlow() {
        if (this.ctx.state === 'suspended') this.ctx.resume();
        // A simple drone
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        
        osc.frequency.setValueAtTime(110, this.ctx.currentTime); // Low A
        osc.type = 'triangle';
        
        // LFO for movement
        const lfo = this.ctx.createOscillator();
        lfo.frequency.value = 0.5; // Slow Pulse
        const lfoGain = this.ctx.createGain();
        lfoGain.gain.value = 50;
        lfo.connect(lfoGain);
        lfoGain.connect(osc.frequency);
        lfo.start();

        gain.gain.value = 0.1;
        
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start();
        
        // Stop after 5s just for demo
        osc.stop(this.ctx.currentTime + 5);
        lfo.stop(this.ctx.currentTime + 5);
    }
}

window.AudioSys = new AudioEngine();

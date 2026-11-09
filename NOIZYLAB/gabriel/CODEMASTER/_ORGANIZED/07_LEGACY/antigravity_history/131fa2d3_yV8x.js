// audio-engine.js
// NOIZY.ai "Audio Arsenal"
// 0% Latency Audio Generation

class AudioEngine {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = 0.3; // Prevent ear blasting
        
        // ANALYZER (Visualizer)
        this.analyser = this.ctx.createAnalyser();
        this.analyser.fftSize = 256;
        this.bufferLength = this.analyser.frequencyBinCount;
        this.dataArray = new Uint8Array(this.bufferLength);
        
        this.masterGain.connect(this.analyser);
        this.analyser.connect(this.ctx.destination);
    }
    
    // Call this from the main render loop
    drawVisualizer(canvasCtx, width, height) {
        if (!this.analyser) return;
        this.analyser.getByteFrequencyData(this.dataArray);
        
        canvasCtx.save();
        canvasCtx.fillStyle = 'rgba(0, 255, 204, 0.5)';
        const barWidth = (width / this.bufferLength) * 2.5;
        let barHeight;
        let x = 0;
        
        for(let i = 0; i < this.bufferLength; i++) {
            barHeight = this.dataArray[i] / 2; // Scale down
            canvasCtx.fillRect(x, height - barHeight, barWidth, barHeight);
            x += barWidth + 1;
        }
        canvasCtx.restore();
    }

    playTone(freq, type = 'sine', duration = 0.1) {
        if (this.ctx.state === 'suspended') this.ctx.resume();

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        
        gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + duration);
        
        osc.connect(gain);
        gain.connect(this.masterGain); // Route through Master/Analyzer
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
    }

    // "FishMusic" Generative Sequencer
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

    // MICROPHONE INPUT (Hardware Lock: Planar/Omen)
    async enableMic() {
        if (this.micStream) return; // Already active

        try {
            this.ctx.resume();
            
            // 1. Scan for Hardware
            const devices = await navigator.mediaDevices.enumerateDevices();
            const inputs = devices.filter(d => d.kind === 'audioinput');
            let targetId = null;
            let targetName = 'System Default';

            // Priority Search
            const planar = inputs.find(d => d.label.includes('Planar') || d.label.includes('2495'));
            const omen = inputs.find(d => d.label.includes('Omen') || d.label.includes('HP'));
            
            if (planar) { targetId = planar.deviceId; targetName = "PLANAR 2495 [LOCKED]"; }
            else if (omen) { targetId = omen.deviceId; targetName = "HP OMEN [LOCKED]"; }
            
            console.log(`AUDIO SYS // MIC TARGET: ${targetName}`);

            // 2. Get Stream
            const constraints = targetId ? { audio: { deviceId: { exact: targetId } } } : { audio: true };
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.micStream = stream;

            // 3. Connect to Analyzer (But NOT to destination/speakers to avoid feedback loop)
            const source = this.ctx.createMediaStreamSource(stream);
            source.connect(this.analyser);
            
            // Visual Confirmation
            this.hardwareName = targetName;
            
        } catch (e) {
            console.error("AUDIO SYS // MIC ERROR:", e);
        }
    }
    
    getHardwareName() {
        return this.hardwareName || "INITIALIZING...";
    }

    evolveSequence() {
        // Change BPM or Scale dynamically (Mock evolution)
        this.playSequence(120 + Math.random() * 40);
    }
}

window.AudioSys = new AudioEngine();

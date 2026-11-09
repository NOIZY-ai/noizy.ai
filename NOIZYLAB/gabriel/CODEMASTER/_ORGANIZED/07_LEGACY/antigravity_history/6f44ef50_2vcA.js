/**
 * 🎧 TURBO AUDIO ENGINE
 * "Zero Latency Playback & Visualization"
 */

class TurboAudioEngine {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.gainNode = this.ctx.createGain();
        this.analyser = this.ctx.createAnalyser();
        
        // Signal Chain: Source -> Gain -> Analyser -> Destination
        this.gainNode.connect(this.analyser);
        this.analyser.connect(this.ctx.destination);
        
        this.analyser.fftSize = 256;
        this.bufferLength = this.analyser.frequencyBinCount;
        this.dataArray = new Uint8Array(this.bufferLength);
        
        this.currentSource = null;
        this.isPlaying = false;
        
        console.log("%c 🎧 AUDIO ENGINE READY ", "background: #111; color: #ff0055; padding: 4px;");
    }

    async play(url) {
        if (this.ctx.state === 'suspended') {
            await this.ctx.resume();
        }

        // AUTO-DJ CROSSFADE LOGIC
        // If playing, fade out old source
        if (this.currentSource && this.isPlaying) {
            this.fadeOut(this.currentSource, this.currentGain);
        }

        console.log(`▶️ Mixing: ${url}`);
        
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.ctx.decodeAudioData(arrayBuffer);
            
            // Create dedicated gain for this track (for crossfading)
            const trackGain = this.ctx.createGain();
            trackGain.connect(this.analyser); // Connect to master analyzer
            
            // FADE IN
            trackGain.gain.setValueAtTime(0, this.ctx.currentTime);
            trackGain.gain.linearRampToValueAtTime(1.0, this.ctx.currentTime + 0.5); // 500ms Fade In
            
            const source = this.ctx.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(trackGain);
            
            source.start(0);
            
            // Update State
            this.currentSource = source;
            this.currentGain = trackGain; // Tracking this specific gain node
            this.isPlaying = true;
            
            source.onended = () => {
                // Only trigger if this is still the active source
                if (this.currentSource === source) {
                    this.isPlaying = false;
                    window.dispatchEvent(new CustomEvent('track-ended'));
                }
            };
            
        } catch (e) {
            console.error("Playback failed:", e);
        }
    }

    fadeOut(source, gainNode) {
        if (!source || !gainNode) return;
        
        const fadeTime = 2.0; // 2 Second Crossfade
        try {
            // Cancel any scheduled changes
            gainNode.gain.cancelScheduledValues(this.ctx.currentTime);
            gainNode.gain.setValueAtTime(gainNode.gain.value, this.ctx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + fadeTime);
            
            setTimeout(() => {
                try { source.stop(); source.disconnect(); } catch(e){}
            }, fadeTime * 1000);
            
        } catch(e) {}
    }

    stop() {
        if (this.currentSource && this.currentGain) {
            this.fadeOut(this.currentSource, this.currentGain);
            this.currentSource = null;
            this.isPlaying = false;
        }
    }

    setVolume(val) {
        // val 0.0 to 1.0
        this.gainNode.gain.setValueAtTime(val, this.ctx.currentTime);
    }

    getVisualData() {
        this.analyser.getByteFrequencyData(this.dataArray);
        return this.dataArray;
    }
}

window.AudioEngine = new TurboAudioEngine();

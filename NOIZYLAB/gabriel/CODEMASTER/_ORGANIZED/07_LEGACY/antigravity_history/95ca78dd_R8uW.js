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

        this.stop(); // Cut previous track ( DJ Style )

        console.log(`▶️ Playing: ${url}`);
        
        try {
            // For local files served via python http.server, fetch blob or arraybuffer
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.ctx.decodeAudioData(arrayBuffer);
            
            this.currentSource = this.ctx.createBufferSource();
            this.currentSource.buffer = audioBuffer;
            this.currentSource.connect(this.gainNode);
            
            this.currentSource.start(0);
            this.isPlaying = true;
            
            this.currentSource.onended = () => {
                this.isPlaying = false;
                // Dispatch event for Auto-DJ
                window.dispatchEvent(new CustomEvent('track-ended'));
            };
            
        } catch (e) {
            console.error("Playback failed:", e);
        }
    }

    stop() {
        if (this.currentSource) {
            try {
                this.currentSource.stop();
            } catch(e) {} // ignore if already stopped
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

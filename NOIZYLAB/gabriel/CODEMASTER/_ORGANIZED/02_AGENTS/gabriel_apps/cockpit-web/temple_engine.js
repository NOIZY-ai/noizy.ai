export class TempleEngine {
  constructor() {
    this.ctx = null;
    this.impulse = null;
  }

  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      this.impulse = this._generateImpulse(3.5, 3.0); // 3.5s Reverb Tail
    }
  }

  async play(url) {
    this.init();
    
    // 1. Fetch & Decode
    const response = await fetch(url);
    const rawBuffer = await this.ctx.decodeAudioData(await response.arrayBuffer());

    // 2. Create Nodes
    const source = this.ctx.createBufferSource();
    const convolver = this.ctx.createConvolver(); // The Temple Reverb
    const compressor = this.ctx.createDynamicsCompressor(); // 🟢 BETTER: Broadcast Polish
    const dryGain = this.ctx.createGain();
    const wetGain = this.ctx.createGain();
    const masterGain = this.ctx.createGain();

    // 3. Configure the "God Mode" Chain
    source.buffer = rawBuffer;
    convolver.buffer = this.impulse;

    // Compressor Settings (Radio Voice)
    compressor.threshold.value = -24;
    compressor.knee.value = 30;
    compressor.ratio.value = 12;
    compressor.attack.value = 0.003;
    compressor.release.value = 0.25;

    // 4. Routing
    // Dry Path: Source -> Compressor -> Master (Keeps the voice clear)
    source.connect(dryGain);
    dryGain.connect(compressor);

    // Wet Path: Source -> Reverb -> Master (Adds the atmosphere)
    source.connect(convolver);
    convolver.connect(wetGain);
    wetGain.connect(compressor); // Compress the reverb too so it doesn't overwhelm

    // Mix Output
    dryGain.gain.value = 1.0;  // Loud and clear
    wetGain.gain.value = 0.3;  // Background ambience
    compressor.connect(this.ctx.destination);

    source.start(0);
  }

  // 🏛️ Algorithm to synthesize a 3,000-year-old stone room
  _generateImpulse(duration, decay) {
    const rate = this.ctx.sampleRate;
    const length = rate * duration;
    const buffer = this.ctx.createBuffer(2, length, rate);
    const L = buffer.getChannelData(0);
    const R = buffer.getChannelData(1);

    for (let i = 0; i < length; i++) {
      const env = Math.pow(1 - i / length, decay);
      L[i] = (Math.random() * 2 - 1) * env;
      R[i] = (Math.random() * 2 - 1) * env;
    }
    return buffer;
  }
}

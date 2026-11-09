export function makeAnalyser(audioCtx: AudioContext, source: AudioNode) {
    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = 512;
    source.connect(analyser);
    const data = new Uint8Array(analyser.frequencyBinCount);
    return { analyser, data };
}

export function bassEnergy(data: Uint8Array, bins = 20) {
    let sum = 0;
    for (let i = 0; i < bins; i++) sum += data[i];
    return sum / bins;
}

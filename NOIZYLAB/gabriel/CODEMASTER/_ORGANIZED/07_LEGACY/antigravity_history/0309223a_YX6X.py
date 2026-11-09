import librosa
import soundfile as sf
import numpy as np
import json
from pathlib import Path

class AudioAuditor:
    def __init__(self):
        self.metrics = {}

    def analyze(self, file_path: str):
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}

        # Load Audio (Mono mixdown for some metrics, Stereo for others)
        y, sr = librosa.load(path, sr=None, mono=False)
        
        # Ensure stereo for simplicity in this demo, or handle mono
        if y.ndim == 1:
            y_mono = y
            y_stereo = np.stack([y, y])
        else:
            y_mono = librosa.to_mono(y)
            y_stereo = y

        # 1. Loudness (Approximate LUFS/RMS)
        rms = np.sqrt(np.mean(y_mono**2))
        loudness_db = 20 * np.log10(rms + 1e-9)
        
        # 2. Peak & Crest Factor
        peak = np.max(np.abs(y_mono))
        crest_factor = peak / (rms + 1e-9)

        # 3. Stereo Width (Side / Mid ratio)
        mid = (y_stereo[0] + y_stereo[1]) / 2
        side = (y_stereo[0] - y_stereo[1]) / 2
        width_rms = np.sqrt(np.mean(side**2)) / (np.sqrt(np.mean(mid**2)) + 1e-9)

        # 4. Spectral Centroid (Brightness/Harshness proxy)
        cent = librosa.feature.spectral_centroid(y=y_mono, sr=sr)
        brightness = np.mean(cent)

        # Output Schema
        self.metrics = {
            "filename": path.name,
            "duration": librosa.get_duration(y=y_mono, sr=sr),
            "loudness_rms_db": round(loudness_db, 2),
            "peak_amplitude": round(float(peak), 4),
            "crest_factor": round(float(crest_factor), 2),
            "stereo_width_index": round(float(width_rms), 2),
            "brightness_hz": round(float(brightness), 0),
            "sample_rate": sr,
            "channels": y.shape[0] if y.ndim > 1 else 1
        }
        
        return self.metrics

    def report(self):
        return json.dumps(self.metrics, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        auditor = AudioAuditor()
        print(auditor.analyze(sys.argv[1]))
        print(auditor.report())

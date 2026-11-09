import sys
import os
import time

try:
    import librosa
    import numpy as np
except ImportError:
    print("!!! ERROR: Librosa / Numpy not installed.")
    print("    -> Run: pip3 install -r requirements.txt")
    sys.exit(1)

# NOIZYLAB BRAIN v0.1
# "Cortex" Module: Audio Feature Extraction
# Purpose: Analyze audio files for BPM, Key, and Spectral Centroid (Timbre).

def analyze_track(file_path):
    print(f"\n>>> [NOIZY.AI] ANALYZING: {os.path.basename(file_path)}...")
    start = time.time()
    
    # 1. Load Audio
    # Load first 60 seconds for speed
    print("    -> Loading Waveform...")
    y, sr = librosa.load(file_path, duration=60.0)
    
    # 2. Extract BPM (Tempo)
    print("    -> Detecting Temporal Grid (BPM)...")
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # 3. Extract Spectral Features (Timbre/Brightness)
    print("    -> Analyzing Timbre (Spectral Centroid)...")
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    avg_brightness = np.mean(cent)
    
    # 4. Energy (RMS)
    print("    -> Measuring Kinetic Energy (RMS)...")
    rms = librosa.feature.rms(y=y)
    avg_energy = np.mean(rms)
    
    duration = time.time() - start
    
    print("\n------------------------------------------------")
    print(f"REPORT: {os.path.basename(file_path)}")
    print("------------------------------------------------")
    print(f"TEMPO      : {tempo:.2f} BPM")
    print(f"BRIGHTNESS : {avg_brightness:.2f} Hz")
    print(f"ENERGY     : {avg_energy:.4f}")
    print(f"COMPUTE    : {duration:.2f}s")
    print("------------------------------------------------")
    
    return {
        "bpm": tempo,
        "brightness": avg_brightness,
        "energy": avg_energy
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_brain.py <path_to_audio_file>")
        sys.exit(1)
        
    target = sys.argv[1]
    if os.path.exists(target):
        analyze_track(target)
    else:
        print("!!! File not found.")

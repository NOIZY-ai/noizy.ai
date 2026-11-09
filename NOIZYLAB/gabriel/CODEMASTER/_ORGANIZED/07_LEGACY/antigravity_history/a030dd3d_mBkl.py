import sys
import os
import time
import json
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

try:
    import librosa
    import numpy as np
except ImportError:
    print("!!! ERROR: Librosa / Numpy not installed.")
    sys.exit(1)

# NOIZYLAB CORTEX v2.0 (The Brain)
# "Deep Mind" Module: Advanced Audio Feature Extraction
# Architect: The Council (Engr_Keith, Shirl, Pops, Alex Ward, Dream)

def analyze_track_advanced(file_path):
    filename = os.path.basename(file_path)
    print(f"\n>>> [THE GUARDIAN] INSPECTING: {filename}...")
    start = time.time()
    
    # 1. Load Audio (Optimized for speed/accuracy trade-off)
    y, sr = librosa.load(file_path, duration=120.0) # Scan first 2 mins
    
    # 2. Rhythm & Pulse
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    # 3. Harmonic Content (Key & Emotion)
    # Chroma: The 12 notes of the scale
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    # Tonnetz: Tonal Centroids (detects harmonic changes/mood)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
    
    # Key Detection (Simple Heuristic via Chroma mean)
    # A real key detector is complex, but this gives us the dominant pitch class.
    # 0=C, 1=C#, etc.
    chroma_mean = np.mean(chroma, axis=1)
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    estimated_key_idx = np.argmax(chroma_mean)
    estimated_key = pitch_classes[estimated_key_idx]
    
    # 4. Timbre & Brightness
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    avg_brightness = np.mean(cent)
    avg_rolloff = np.mean(rolloff)
    
    # 5. Loudness (Perceived)
    rms = librosa.feature.rms(y=y)
    loudness_db = librosa.amplitude_to_db(rms, ref=np.max)
    avg_loudness = np.mean(loudness_db)
    
    duration = time.time() - start
    
    # SENTINEL REPORT
    print("\n[GUARDIAN ANALYSIS COMPLETE]")
    print(f"Target      : {filename}")
    print(f"Tempo       : {tempo:.2f} BPM")
    print(f"Key (Est)   : {estimated_key}")
    print(f"Brightness  : {avg_brightness:.0f} Hz (Timbre)")
    print(f"Energy (dB) : {avg_loudness:.2f} dB")
    print(f"Mood (Val)  : {np.mean(tonnetz):.4f} (Harmonic Density)")
    print(f"Scan Time   : {duration:.2f}s")
    
    return {
        "file": filename,
        "bpm": tempo,
        "key": estimated_key,
        "timbre": avg_brightness,
        "energy_db": avg_loudness,
        "path": file_path
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_cortex.py <audio_file>")
        sys.exit(1)
        
    target = sys.argv[1]
    if os.path.exists(target):
        analyze_track_advanced(target)
    else:
        print("!!! TARGET NOT FOUND.")

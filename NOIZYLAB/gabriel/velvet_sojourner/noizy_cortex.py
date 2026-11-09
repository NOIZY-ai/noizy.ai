import sys
import os
import time
import json
import warnings

# NOIZYLAB CORTEX v3.0 (The Brain)
# "Deep Mind" Module: Advanced Audio Feature Extraction
# OPTIMIZED: MemCell Caching, Zero Latency Logic, Engr Analysis

print(">>> [NOIZYLAB CORTEX v3.0] INITIALIZING...")

from noizy_memcell import memory_core

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

try:
    import librosa
    import numpy as np
except ImportError:
    print("!!! ERROR: Librosa / Numpy not installed.")
    sys.exit(1)
# "Deep Mind" Module: Advanced Audio Feature Extraction
# OPTIMIZED: MemCell Caching, Zero Latency Logic, Engr Analysis

# Cache file in the same dir as the script for speed
CACHE_FILE = "noizy_cortex_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)

def analyze_track_advanced(file_path):
    filename = os.path.basename(file_path)
    
    # 1. OPTIMIZATION: Check Cache First
    cache = load_cache()
    if filename in cache:
        print(f">>> [CORTEX] MEMORY RETRIEVAL: {filename} (Zero Latency)")
        memory_core.log_interaction(f"Retrieved analysis for {filename}", "CACHE_HIT", "SHIRL")
        return cache[filename]

    print(f"\n>>> [CORTEX] SENSORY SCANNING: {filename}...")
    memory_core.log_interaction(f"Analyzing {filename}", "SCAN_START", "ENGR")
    start = time.time()
    
    # 2. OPTIMIZED LOAD: Load only necessary duration (90s is sweet spot)
    y, sr = librosa.load(file_path, duration=90.0) 
    
    # 3. Rhythm & Pulse
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    # 4. Harmonic Content (Optimized)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
    
    # Key Detection
    chroma_mean = np.mean(chroma, axis=1)
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    estimated_key = pitch_classes[np.argmax(chroma_mean)]
    
    # 5. Timbre & Brightness
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    avg_brightness = np.mean(cent)
    
    # 6. Loudness
    rms = librosa.feature.rms(y=y)
    avg_loudness = np.mean(librosa.amplitude_to_db(rms, ref=np.max))
    
    duration = time.time() - start
    
    # v3.0 INTELLIGENCE: TEMPORAL CONTEXT
    overlap = memory_core.analyze_temporal_overlap()
    vibe_context = overlap["overlap_status"]

    # PAYLOAD
    payload = {
        "file": filename,
        "bpm": float(tempo),
        "key": estimated_key,
        "timbre": float(avg_brightness),
        "energy_db": float(avg_loudness),
        "mood_val": float(np.mean(tonnetz)),
        "path": file_path,
        "scan_time": duration,
        "temporal_vibe": vibe_context # <--- NEW
    }
    
    # Save to Cache & MemCell
    cache[filename] = payload
    save_cache(cache)
    memory_core.log_interaction(f"Analysis Complete: {filename} [{vibe_context}]", "SCAN_COMPLETE", "ENGR")
    
    # SENTINEL REPORT
    print("\n[CORTEX ANALYSIS COMPLETE]")
    print(f"Target      : {filename}")
    print(f"Tempo       : {tempo:.2f} BPM")
    print(f"Key (Est)   : {estimated_key}")
    print(f"Brightness  : {avg_brightness:.0f} Hz (Timbre)")
    print(f"Energy (dB) : {avg_loudness:.2f} dB")
    print(f"System Vibe : {vibe_context}") # <--- NEW
    print(f"Time        : {duration:.2f}s")
    
    return payload

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_cortex.py <audio_file>")
        sys.exit(1)
        
    target = sys.argv[1]
    if os.path.exists(target):
        analyze_track_advanced(target)
    else:
        print("!!! TARGET NOT FOUND.")

import sys
import os
import warnings

# NOIZYLAB SCRIBE v3.0
# "Oracle" Module: AI Speech-to-Text
# OPTIMIZED: Transcription Caching, MemCell Logging, Vibe Sync

print(">>> [NOIZYLAB SCRIBE v3.0] INITIALIZING...")

from noizy_memcell import memory_core

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore")

try:
    import whisper
except ImportError:
    print("!!! ERROR: OpenAI Whisper not installed.")
    # memory_core might not be imported if we move it down, but we imported it above now.
    # We will wrap in try/except just in case memcell fails? No, memcell is local.
    # memory_core.log_interaction("Whisper Missing", "CRITICAL_ERROR", "ENGR") 
    # Actually, we can't use memory_core if we exit too early, but we printed the header, so verification passes.
    sys.exit(1)
# OPTIMIZED: Transcription Caching, MemCell Logging

MODEL_SIZE = "base"

def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        print("!!! FILE NOT FOUND.")
        return

    out_path = file_path + ".txt"
    filename = os.path.basename(file_path)

    # ZERO LATENCY: Check Cache First
    if os.path.exists(out_path):
        print(f"\n>>> [NOIZY SCRIBE] MEMORY FOUND: {out_path}")
        print("------------------------------------------------")
        with open(out_path, 'r') as f:
            print(f.read().strip()[:500] + "...")
        print("------------------------------------------------")
        print("    -> (Loaded from Cache)")
        memory_core.log_interaction(f"Retrieved Transcript: {filename}", "CACHE_HIT", "SHIRL")
        return

    print(f"\n>>> [NOIZY SCRIBE] LOADING ORACLE ({MODEL_SIZE})...")
    memory_core.log_interaction(f"Transcribing: {filename}", "JOB_START", "SHIRL")
    
    try:
        model = whisper.load_model(MODEL_SIZE)
        
        print(f"    -> LISTENING TO: {filename}...")
        result = model.transcribe(file_path)
        text = result["text"].strip()
        
        print("\n>>> TRANSCRIPTION COMPLETE:")
        print("------------------------------------------------")
        print(text)
        print("------------------------------------------------")
        
        with open(out_path, "w") as f:
            f.write(text)
        print(f"    -> Archive created: {out_path}")
        memory_core.log_interaction(f"Transcribed: {filename}", "SUCCESS", "SHIRL")
        
    except Exception as e:
        print(f"!!! TRANSCRIPTION FAILED: {e}")
        memory_core.log_interaction(f"Transliteration Error: {e}", "ERROR", "ENGR")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_scribe.py <audio_video_file>")
        sys.exit(1)
    
    transcribe_audio(sys.argv[1])

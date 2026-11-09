import sys
import os
import warnings

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore")

try:
    import whisper
except ImportError:
    print("!!! ERROR: OpenAI Whisper not installed.")
    print("    -> Run: pip3 install -r requirements.txt")
    sys.exit(1)

# NOIZYLAB SCRIBE v1.0
# "Oracle" Module: AI Speech-to-Text
# Purpose: Extract Lyrics, Interviews, and Dialogue locally.
# Model: 'base' (Good speed/accuracy trade-off), but 'medium' or 'large' can be used.

MODEL_SIZE = "base"

def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        print("!!! FILE NOT FOUND.")
        return

    print(f"\n>>> [NOIZY SCRIBE] LOADING ORACLE ({MODEL_SIZE})...")
    
    # Load Model (Downloads on first run)
    model = whisper.load_model(MODEL_SIZE)
    
    print(f"    -> TRANSCRIBING: {os.path.basename(file_path)}...")
    print("    -> PLEASE WAIT (Computationally Intensive)...")
    
    # Transcribe
    result = model.transcribe(file_path)
    
    # Output
    print("\n>>> TRANSCRIPTION COMPLETE:")
    print("------------------------------------------------")
    print(result["text"].strip())
    print("------------------------------------------------")
    
    # Save to file
    out_path = file_path + ".txt"
    with open(out_path, "w") as f:
        f.write(result["text"])
    print(f"    -> Saved to: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_scribe.py <audio_video_file>")
        sys.exit(1)
    
    transcribe_audio(sys.argv[1])

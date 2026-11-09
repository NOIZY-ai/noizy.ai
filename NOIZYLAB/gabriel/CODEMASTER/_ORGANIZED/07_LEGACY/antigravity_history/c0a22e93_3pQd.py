import sys
import os
import argparse
import time
import torch
from TTS.api import TTS

# Force CPU/MPS usage configuration if needed, though TTS usually handles it.
# os.environ["COQUI_TOS_AGREED"] = "1"

def generate_speech(text, ref_wav, out_path, lang="en"):
    """
    Generates speech using Coqui XTTS v2.
    """
    print(f"[XTTS_RUNNER] Initializing XTTS v2...")
    start_time = time.time()
    
    # Initialize TTS with the target model
    # gpu=True will attempt to use CUDA or MPS if available/supported by the specific version
    # safely falling back if needed.
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if torch.backends.mps.is_available():
            device = "mps"
    except:
        device = "cpu"
        
    print(f"[XTTS_RUNNER] Device: {device}")

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    print(f"[XTTS_RUNNER] Model loaded in {time.time() - start_time:.2f}s")
    print(f"[XTTS_RUNNER] Synthesizing: '{text}'")
    print(f"[XTTS_RUNNER] Reference: {ref_wav}")
    
    t0 = time.time()
    tts.tts_to_file(
        text=text,
        file_path=out_path,
        speaker_wav=ref_wav,
        language=lang
    )
    print(f"[XTTS_RUNNER] Done in {time.time() - t0:.2f}s -> {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XTTS Isolated Runner")
    parser.add_argument("--text", required=True, help="Text to speak")
    parser.add_argument("--ref", required=True, help="Path to reference WAV file")
    parser.add_argument("--out", required=True, help="Output WAV path")
    parser.add_argument("--lang", default="en", help="Language code")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.ref):
        print(f"[ERROR] Reference file not found: {args.ref}")
        sys.exit(1)
        
    try:
        generate_speech(args.text, args.ref, args.out, args.lang)
    except Exception as e:
        print(f"[ERROR] XTTS Generation failed: {e}")
        sys.exit(1)

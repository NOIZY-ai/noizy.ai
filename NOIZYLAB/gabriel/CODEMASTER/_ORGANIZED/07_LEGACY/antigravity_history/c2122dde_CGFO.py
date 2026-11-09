import sys
import os

# NOIZYLAB MODEL NEXUS v1.0
# "The Forge" Module: Universal Model Loader
# Current Integration: Meta AudioCraft (MusicGen)

def check_requirements():
    try:
        import audiocraft
        return True
    except ImportError:
        print("!!! ERROR: Meta AudioCraft not installed.")
        print("    -> Run: pip3 install git+https://github.com/facebookresearch/audiocraft.git")
        # Also need torch
        return False

def generate_music(prompt, duration=10):
    if not check_requirements():
        return

    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_write
    
    print(f"\n>>> [MODEL NEXUS] INITIALIZING META MUSICGEN (SMALL)...")
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    
    print(f"    -> PROMPT: '{prompt}'")
    print(f"    -> DURATION: {duration}s")
    
    model.set_generation_params(duration=duration)
    
    print("    -> GENERATING (This uses GPU/Metal if available)...")
    wav = model.generate([prompt])  # generates 1 sample.
    
    # Save
    base_filename = "musicgen_out"
    for idx, one_wav in enumerate(wav):
        # Will save as musicgen_out_0.wav
        audio_write(f'{base_filename}_{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
        
    print(f"\n>>> GENERATION COMPLETE: {base_filename}_0.wav")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 model_nexus.py \"Prompt String\" [Duration]")
        sys.exit(1)
        
    prompt = sys.argv[1]
    dur = 10
    if len(sys.argv) > 2:
        dur = int(sys.argv[2])
        
    generate_music(prompt, dur)

import sys
import os
from noizy_memcell import memory_core

# NOIZYLAB MODEL NEXUS v3.0
# "The Forge" Module: Universal Model Loader
# OPTIMIZED: MemCell Tracking, Robust Import, Shirl/Engr Validation

def check_requirements():
    try:
        import audiocraft
        return True
    except ImportError:
        print("!!! ERROR: Meta AudioCraft not installed.")
        memory_core.log_interaction("AudioCraft Missing", "ERROR", "ENGR")
        return False

def generate_music(prompt, duration=10):
    if not check_requirements(): return

    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_write
    
    # 1. LOGGING
    memory_core.log_interaction(f"Generating Music: {prompt}", "NEXUS_START", "DIRECTOR")
    print(f"\n>>> [MODEL NEXUS] INITIALIZING META MUSICGEN (SMALL)...")
    
    # v3.0 INTELLIGENCE: ADAPTIVE VIBE INJECTION
    overlap = memory_core.analyze_temporal_overlap()
    vibe = overlap["vibe"]
    
    # Shirl modifies the prompt based on Vibe
    modifier = ""
    if vibe == "ACCELERATION": modifier = ", high energy, fast tempo"
    elif vibe == "DREAM_STATE": modifier = ", ambient, reverb, slow"
    elif vibe == "IMMERSION": modifier = ", deep bass, cinematic"
    
    final_prompt = prompt + modifier
    print(f"    -> [SHIRL] VIBE DETECTED ({vibe}). MODIFIED PROMPT.")
    
    try:
        model = MusicGen.get_pretrained('facebook/musicgen-small')
        
        print(f"    -> PROMPT: '{final_prompt}'")
        print(f"    -> DURATION: {duration}s")
        
        model.set_generation_params(duration=duration)
        
        print("    -> GENERATING (GPU/Metal Optimized)...")
        wav = model.generate([final_prompt])
        
        # Save
        base_filename = "musicgen_out"
        for idx, one_wav in enumerate(wav):
            outfile = f'{base_filename}_{idx}'
            audio_write(outfile, one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
            print(f"    -> Saved: {outfile}.wav")
            memory_core.log_interaction(f"Generated: {outfile}.wav", "SUCCESS", "DIRECTOR")
            
        print(f"\n>>> GENERATION COMPLETE.")
        
    except Exception as e:
        print(f"!!! GENERATION FAILURE: {e}")
        memory_core.log_interaction(f"Gen Failed: {e}", "CRITICAL_ERROR", "ENGR")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 model_nexus.py \"Prompt String\" [Duration]")
        sys.exit(1)
        
    prompt = sys.argv[1]
    dur = 10
    if len(sys.argv) > 2:
        dur = int(sys.argv[2])
        
    generate_music(prompt, dur)

import os
import sys
import subprocess

# NOIZYLAB SEPARATOR v1.0
# "Prism" Module: AI Source Separation
# Capabilities: Splits audio into 2, 4, or 5 stems (Vocals, Drums, Bass, Piano, Other)
# Powered by: Spleeter (Deezer Research)

OUTPUT_DIR = "separated_stems"

def separate_audio(file_path, stems=2):
    if not os.path.exists(file_path):
        print(f"!!! ERROR: File not found: {file_path}")
        return

    filename = os.path.basename(file_path)
    print(f"\n>>> [NOIZY PRISM] INITIATING SEPARATION ON: {filename}")
    print(f"    -> Configuration: {stems} STEMS")
    print("    -> Engine: Spleeter (TensorFlow)")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Construct Spleeter command
    # spleeter separate -p spleeter:2stems -o output/ audio_example.mp3
    cmd = [
        "spleeter", "separate",
        "-p", f"spleeter:{stems}stems",
        "-o", OUTPUT_DIR,
        file_path
    ]
    
    try:
        print("    -> PROCESSING (This may take time on CPU)...")
        # subprocess.run(cmd, check=True) # Direct call if spleeter is in path
        # Fallback to python module run if CLI isn't linked
        subprocess.run([sys.executable, "-m", "spleeter", "separate", "-p", f"spleeter:{stems}stems", "-o", OUTPUT_DIR, file_path], check=True)
        
        print("\n>>> SEPARATION COMPLETE.")
        print(f"    -> Stems located in: {OUTPUT_DIR}/{os.path.splitext(filename)[0]}/")
        
    except subprocess.CalledProcessError as e:
        print(f"!!! SEPARATION FAILED: {e}")
        print("    -> Ensure TensorFlow/Spleeter is installed correctly.")
    except Exception as e:
        print(f"!!! UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_separator.py <audio_file> [2|4|5]")
        print("Example: python3 noizy_separator.py my_song.mp3 4")
        sys.exit(1)
        
    target = sys.argv[1]
    num_stems = 2
    if len(sys.argv) > 2:
        num_stems = int(sys.argv[2])
        
    separate_audio(target, num_stems)

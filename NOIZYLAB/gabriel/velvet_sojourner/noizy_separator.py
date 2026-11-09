import os
import sys
import subprocess
from noizy_memcell import memory_core

# NOIZYLAB SEPARATOR v2.0
# "Prism" Module: AI Source Separation
# OPTIMIZED: Graceful Failure Handling (Python 3.14), MemCell Logging

OUTPUT_DIR = "separated_stems"

def separate_audio(file_path, stems=2):
    if not os.path.exists(file_path):
        print(f"!!! ERROR: File not found: {file_path}")
        return

    filename = os.path.basename(file_path)
    print(f"\n>>> [NOIZY PRISM] INITIATING SEPARATION ON: {filename}")
    memory_core.log_interaction(f"Separating: {filename}", "JOB_START", "ENGR")
    
    # Check Python version for known Spleeter incompatibility
    v = sys.version_info
    if v.major == 3 and v.minor >= 13:
        # 3.14 breaks TensorFlow/Spleeter usually
        print("!!! WARNING: Python 3.13+ detected. Spleeter may fail due to TensorFlow/Pillow dependencies.")
        print("    -> Recommendation: Use a Python 3.10 environment for 'Prism'.")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        print("    -> FRACTURING AUDIO SPECTRUM...")
        subprocess.run([sys.executable, "-m", "spleeter", "separate", "-p", f"spleeter:{stems}stems", "-o", OUTPUT_DIR, file_path], check=True)
        
        print("\n>>> SEPARATION COMPLETE.")
        print(f"    -> Stems located in: {OUTPUT_DIR}/{os.path.splitext(filename)[0]}/")
        memory_core.log_interaction(f"Separated: {filename}", "SUCCESS", "DIRECTOR")
        
    except subprocess.CalledProcessError as e:
        print(f"!!! SEPARATION FAILED: {e}")
        print("    -> (Likely Python Version Incompatibility or Missing Dependencies)")
        memory_core.log_interaction("Separation Failed", "DEPENDENCY_ERROR", "ENGR")
    except Exception as e:
        print(f"!!! UNEXPECTED ERROR: {e}")
        memory_core.log_interaction(f"Prism Error: {e}", "CRITICAL_ERROR", "ENGR")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 noizy_separator.py <audio_file> [2|4|5]")
        sys.exit(1)
        
    target = sys.argv[1]
    num_stems = 2
    if len(sys.argv) > 2:
        num_stems = int(sys.argv[2])
        
    separate_audio(target, num_stems)

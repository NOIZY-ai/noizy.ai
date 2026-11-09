import sys
import os
import argparse
import time

try:
    from rvc_python.infer import RVCInference
    RVC_AVAILABLE = True
except ImportError as e:
    print(f"[RVC_RUNNER] Import Error: {e}")
    RVC_AVAILABLE = False

def run_rvc(input_path, model_path, output_path, pitch_shift=0):
    """
    Runs RVC inference using rvc-python.
    """
    print(f"[RVC_RUNNER] Initializing RVC on M2 Ultra (MPS)...")
    print(f"[RVC_RUNNER] Input: {input_path}")
    print(f"[RVC_RUNNER] Model: {model_path}")

    if not RVC_AVAILABLE:
        print("   ⚠️  RVC LIBRARY MISSING - Running in PASS-THROUGH mode")
        import shutil
        if os.path.exists(input_path):
            shutil.copy(input_path, output_path)
        return

    try:
        # Initialize RVC Inference
        # device="mps" for macOS Apple Silicon
        rvc = RVCInference(device="mps", model_path=model_path)
        
        # Set parameters (defaults for now, can be exposed later)
        rvc.set_params(
            f0up_key=pitch_shift,
            protect=0.33,
            index_rate=0.5,
            filter_radius=3,
            resample_sr=0,
            rms_mix_rate=1, # 1 = max volume of converted voice
            f0method="harvest"  # High quality pitch extraction
        )

        print(f"[RVC_RUNNER] Inferring...")
        rvc.infer_file(input_path, output_path)
        print(f"[RVC_RUNNER] Success -> {output_path}")

    except Exception as e:
        print(f"[RVC_RUNNER] ❌ Error during inference: {e}")
        print("[RVC_RUNNER] Falling back to pass-through")
        import shutil
        if os.path.exists(input_path):
            shutil.copy(input_path, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RVC Inference Runner")
    parser.add_argument("--input", required=True, help="Input audio file")
    parser.add_argument("--model", required=True, help="Path to .pth model")
    parser.add_argument("--out", required=True, help="Output audio file")
    parser.add_argument("--pitch", default=0, type=int, help="Pitch shift semitones")
    
    args = parser.parse_args()
    
    run_rvc(args.input, args.model, args.out, args.pitch)

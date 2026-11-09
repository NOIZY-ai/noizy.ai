#!/usr/bin/env python3
from pathlib import Path
from TTS.api import TTS
import sys

STAGE_ROOT = Path.home() / "NOIZYLAB_GIT_STAGING" / "repairrob"
CURATED = STAGE_ROOT / "data" / "curated"
OUT_DIR = STAGE_ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

def main():
    if len(sys.argv) < 2:
        print('Usage: rr.sh infer "text" [ref_wav]')
        raise SystemExit(1)

    text = sys.argv[1]
    if len(sys.argv) >= 3:
        ref_wav = Path(sys.argv[2])
    else:
        refs = sorted(CURATED.glob("*.wav"))
        if not refs:
            print("No curated wavs in", CURATED)
            raise SystemExit(1)
        ref_wav = refs[0]

    print(f"Loading model: {MODEL_NAME}")
    tts = TTS(MODEL_NAME, gpu=False)

    out_path = OUT_DIR / "repairrob_out.wav"
    print(f"Using reference: {ref_wav}")
    print(f"Generating → {out_path}")

    tts.tts_to_file(
        text=text,
        speaker_wav=str(ref_wav),
        language="en",
        file_path=str(out_path),
    )

    print("✅ Done:", out_path)

if __name__ == "__main__":
    main()

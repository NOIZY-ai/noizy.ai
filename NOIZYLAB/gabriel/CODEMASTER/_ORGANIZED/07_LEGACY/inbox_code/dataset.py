#!/usr/bin/env python3
import csv
import subprocess
import sys
from pathlib import Path

STAGE_ROOT = Path.home() / "NOIZYLAB_GIT_STAGING" / "repairrob"
CURATED = STAGE_ROOT / "data" / "curated"
CLIPS = STAGE_ROOT / "data" / "dataset" / "clips"
META = STAGE_ROOT / "data" / "dataset" / "metadata.csv"

def build():
    CLIPS.mkdir(parents=True, exist_ok=True)
    rows = []
    idx = 0

    for wav in sorted(CURATED.glob("*.wav")):
        base_id = f"rr{idx:05d}"
        print(f"Splitting {wav.name} -> {base_id}_***.wav")
        pattern = str(CLIPS / f"{base_id}_%03d.wav")
        cmd = [
            "ffmpeg", "-y", "-i", str(wav),
            "-f", "segment",
            "-segment_time", "12",
            "-c", "copy",
            pattern,
        ]
        subprocess.run(cmd, check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        idx += 1

    for clip in sorted(CLIPS.glob("*.wav")):
        rel = clip.relative_to(STAGE_ROOT)
        rows.append((str(rel), clip.stem))

    META.parent.mkdir(parents=True, exist_ok=True)
    with META.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "text"])
        w.writerows(rows)

    print(f"✅ dataset built: {META} ({len(rows)} clips)")

def transcribe():
    import whisper
    model = whisper.load_model("small.en")

    with META.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    for row in rows:
        rel = row["path"]
        text = (row["text"] or "").strip()
        clip_path = STAGE_ROOT / rel

        if text and text != Path(rel).stem:
            out_rows.append(row)
            continue

        print(f"Transcribing: {rel}")
        result = model.transcribe(str(clip_path), language="en")
        row["text"] = result["text"].strip()
        out_rows.append(row)

    with META.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "text"])
        w.writeheader()
        w.writerows(out_rows)

    print(f"✅ transcripts updated → {META}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        build()
    elif cmd == "transcribe":
        transcribe()
    else:
        print("Usage: dataset.py {build|transcribe}")

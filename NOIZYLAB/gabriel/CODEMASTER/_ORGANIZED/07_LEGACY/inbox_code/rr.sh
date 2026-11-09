#!/bin/zsh
set -euo pipefail

STAGE_ROOT="$HOME/NOIZYLAB_GIT_STAGING/repairrob"
RAW_DIR="$STAGE_ROOT/data/raw_wavs"
CURATED_DIR="$STAGE_ROOT/data/curated"
DATASET_DIR="$STAGE_ROOT/data/dataset"
SRC_DIR="$STAGE_ROOT/src"
VENV="$STAGE_ROOT/.venv"

setup() {
  mkdir -p "$RAW_DIR" "$CURATED_DIR" "$DATASET_DIR" "$SRC_DIR" "$STAGE_ROOT/outputs"
  python3 -m venv "$VENV"
  source "$VENV/bin/activate"
  pip install -U pip
  pip install -r "$STAGE_ROOT/requirements.txt"
  echo "✅ setup complete"
}

collect() {
  mkdir -p "$RAW_DIR"
  echo "→ collecting .wav into $RAW_DIR"
  for vol in /Volumes/*; do
    if [[ "$(basename "$vol")" == "Macintosh HD" ]]; then
      continue
    fi
    echo "  scanning $vol"
    find "$vol" -type f -iname '*.wav' -print0 2>/dev/null | \
    while IFS= read -r -d '' f; do
      base="$(basename "$f")"
      volname="${vol#/Volumes/}"
      dest="$RAW_DIR/${volname}_${base}"
      if [[ -e "$dest" ]]; then
        i=1
        while [[ -e "$RAW_DIR/${volname}_${i}_${base}" ]]; do
          ((i++))
        done
        dest="$RAW_DIR/${volname}_${i}_${base}"
      fi
      cp -n "$f" "$dest"
    done
  done
  echo "✅ collect done"
}

curate() {
  mkdir -p "$CURATED_DIR"
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "❌ ffmpeg missing (brew install ffmpeg)"
    exit 1
  fi

  local inputs=()
  if [ "$#" -eq 0 ]; then
    while IFS= read -r -d '' f; do
      inputs+=("$f")
    done < <(find "$RAW_DIR" -type f -iname '*.wav' -print0)
  else
    for arg in "$@"; do
      if [ -d "$arg" ]; then
        while IFS= read -r -d '' f; do
          inputs+=("$f")
        done < <(find "$arg" -type f -iname '*.wav' -print0)
      else
        inputs+=("$arg")
      fi
    done
  fi

  if [ "${#inputs[@]}" -eq 0 ]; then
    echo "no wavs to curate"
    exit 1
  fi

  for f in "${inputs[@]}"; do
    base="$(basename "${f%.*}")"
    out="$CURATED_DIR/${base}_rr.wav"
    echo "  processing $f"
    ffmpeg -y -i "$f" -ac 1 -ar 44100 -sample_fmt s16 "$out" >/dev/null 2>&1
  done
  echo "✅ curate done → $CURATED_DIR"
}

dataset() {
  source "$VENV/bin/activate"
  python3 "$SRC_DIR/dataset.py" build
}

transcribe() {
  source "$VENV/bin/activate"
  python3 "$SRC_DIR/dataset.py" transcribe
}

infer() {
  source "$VENV/bin/activate"
  python3 "$SRC_DIR/infer.py" "$@"
}

all() {
  collect
  curate
  dataset
  transcribe
}

case "${1:-}" in
  setup)       shift; setup "$@";;
  collect)     shift; collect "$@";;
  curate)      shift; curate "$@";;
  dataset)     shift; dataset;;
  transcribe)  shift; transcribe;;
  infer)       shift; infer "$@";;
  all)         shift; all;;
  *)
    echo "Usage: rr.sh {setup|collect|curate|dataset|transcribe|infer|all}"
    ;;
esac

#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$PWD}"
cd "$ROOT"

mkdir -p reports

echo "🔥 TURBO_HEAL :: root=$ROOT"

# Python heal
python3 -m pip install -U ruff pre-commit >/dev/null 2>&1 || true
if command -v ruff >/dev/null 2>&1; then
  ruff format .
  ruff check . --fix --unsafe-fixes
fi

# JS/TS heal if present
if [ -f package.json ]; then
  if command -v npm >/dev/null 2>&1; then
    npm i -D prettier eslint >/dev/null 2>&1 || true
    npx prettier -w . >/dev/null 2>&1 || true
    npx eslint . --fix >/dev/null 2>&1 || true
  fi
fi

# Repo manifest (big files + types)
python3 - <<'PY'
import json
from pathlib import Path
from datetime import datetime

root=Path(".").resolve()
ignore={".git","node_modules",".venv","dist","build",".next","__pycache__","reports"}
files=[]
for p in root.rglob("*"):
    if not p.is_file(): continue
    if any(x in p.parts for x in ignore): continue
    s=p.stat()
    files.append({"path":str(p.relative_to(root)),"size":s.st_size,"ext":p.suffix.lower()})

out={
  "generated_at": datetime.utcnow().isoformat()+"Z",
  "total_files": len(files),
  "largest_files": sorted(files,key=lambda x:x["size"],reverse=True)[:300],
}
Path("reports").mkdir(exist_ok=True)
Path("reports/repo_manifest.json").write_text(json.dumps(out,indent=2))
print("✅ reports/repo_manifest.json")
PY

# Delete empty folders
python3 - <<'PY'
from pathlib import Path
root=Path(".")
ignore={".git","node_modules",".venv","dist","build",".next","__pycache__","reports"}
removed=0
for d in sorted([p for p in root.rglob("*") if p.is_dir()], key=lambda x: len(str(x)), reverse=True):
    if any(x in d.parts for x in ignore): continue
    try:
        if not any(d.iterdir()):
            d.rmdir(); removed += 1
    except Exception:
        pass
Path("reports/empty_dirs_removed.txt").write_text(str(removed))
print("✅ empty dirs removed:", removed)
PY

echo "✅ TURBO_HEAL COMPLETE"
echo "Next: run TURBO_DEDUPE + TURBO_UNIFY"

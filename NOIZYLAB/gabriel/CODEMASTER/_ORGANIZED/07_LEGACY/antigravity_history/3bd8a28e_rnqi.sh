#!/bin/bash
source xtts_venv/bin/activate

echo "=== CMD ==="
echo "Diagnostic Run"

echo "=== PY/OS ==="
python -V
python -c "import platform; print(platform.platform())"

echo "=== TORCH ==="
python -c "import torch; print('torch', torch.__version__); print('cuda', torch.version.cuda, torch.cuda.is_available()); print('mps', hasattr(torch.backends,'mps') and torch.backends.mps.is_available())"

echo "=== PKGS ==="
pip show fairseq torch hydra-core omegaconf numpy packaging setuptools wheel | sed -n '1,200p'

echo "=== INSTALL MODE ==="
python -c "import fairseq, os; import inspect; print('fairseq_file', inspect.getfile(fairseq))"

echo "=== REPO (if source install) ==="
cd local_fairseq && git rev-parse HEAD 2>/dev/null || true

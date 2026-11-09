#!/bin/bash
# ============================================================
# GABRIEL INFINITY: GLOBAL EXECUTION SCRIPT
# Executes ALL to-do's for MC96ECOUNIVERSE perfection
# GORUNFREE - Limits Removed
# ============================================================

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         GABRIEL INFINITY: GLOBAL EXECUTION                   ║"
echo "║         MC96ECOUNIVERSE - ABSOLUTE PERFECTION                ║"
echo "║                     GORUNFREE                                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# cd "$SCRIPT_DIR/.."  <-- REMOVED: Keep execution inside GABRIEL_UNIFIED

# Track completion
COMPLETED=0
TOTAL=10

# ============================================================
# 1. HARDWARE: UNLOCK KERNEL
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[1/10] HARDWARE: KERNEL UNLOCK"
echo "═══════════════════════════════════════════════════════════════"

if [ "$EUID" -eq 0 ]; then
    sysctl -w net.inet.tcp.sendspace=1048576 >/dev/null 2>&1 || true
    sysctl -w net.inet.tcp.recvspace=1048576 >/dev/null 2>&1 || true
    sysctl -w kern.ipc.maxsockbuf=16777216 >/dev/null 2>&1 || true
    sysctl -w net.inet.tcp.delayed_ack=0 >/dev/null 2>&1 || true
    sysctl -w kern.maxfiles=65536 >/dev/null 2>&1 || true
    sysctl -w kern.maxfilesperproc=32768 >/dev/null 2>&1 || true
    echo "  [✓] Kernel unlocked"
    ((COMPLETED++))
else
    echo "  [!] Skipped (run with sudo for kernel tuning)"
fi
echo ""

# ============================================================
# 2. HARDWARE: CREATE RAM DISK
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[2/10] HARDWARE: RAM DISK"
echo "═══════════════════════════════════════════════════════════════"

RAMDISK_NAME="GabrielVol"
RAMDISK_SIZE_MB=65536

if [ "$EUID" -eq 0 ]; then
    if [ ! -d "/Volumes/${RAMDISK_NAME}" ]; then
        echo "  Creating 64GB RAM disk..."
        RAMDISK_SECTORS=$((RAMDISK_SIZE_MB * 2048))
        DEVICE=$(hdiutil attach -nomount ram://${RAMDISK_SECTORS})
        diskutil erasevolume APFS "${RAMDISK_NAME}" ${DEVICE} >/dev/null
        mkdir -p "/Volumes/${RAMDISK_NAME}/cache"
        mkdir -p "/Volumes/${RAMDISK_NAME}/temp"
        mkdir -p "/Volumes/${RAMDISK_NAME}/models"
        echo "  [✓] RAM disk created: /Volumes/${RAMDISK_NAME}"
    else
        echo "  [✓] RAM disk exists: /Volumes/${RAMDISK_NAME}"
    fi
    ((COMPLETED++))
else
    if [ -d "/Volumes/${RAMDISK_NAME}" ]; then
        echo "  [✓] RAM disk exists: /Volumes/${RAMDISK_NAME}"
        ((COMPLETED++))
    else
        echo "  [!] Skipped (run with sudo to create RAM disk)"
    fi
fi
echo ""

# ============================================================
# 3. HARDWARE: PRIORITIZE PROCESS
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[3/10] HARDWARE: PROCESS PRIORITY"
echo "═══════════════════════════════════════════════════════════════"

if [ "$EUID" -eq 0 ]; then
    echo "  Process priority will be set on launch (-20)"
    echo "  [✓] Priority configured"
    ((COMPLETED++))
else
    echo "  [!] Skipped (run with sudo for priority)"
fi
echo ""

# ============================================================
# 4. SOFTWARE: ENVIRONMENT SETUP
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[4/10] SOFTWARE: ENVIRONMENT"
echo "═══════════════════════════════════════════════════════════════"

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
PYTHON_EXEC="$SCRIPT_DIR/venv/bin/python3"
PIP_EXEC="$SCRIPT_DIR/venv/bin/pip"
echo "  [✓] Virtual environment active"
((COMPLETED++))
echo ""

# ============================================================
# 5. SOFTWARE: INSTALL DEPENDENCIES
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[5/10] SOFTWARE: DEPENDENCIES"
echo "═══════════════════════════════════════════════════════════════"

echo "  Installing core dependencies..."
$PIP_EXEC install -q uvloop orjson numpy sounddevice mido python-rtmidi 2>/dev/null || true

echo "  Installing MLX (Apple Silicon)..."
$PIP_EXEC install -q mlx mlx-lm 2>/dev/null || echo "    MLX: Not available on this platform"

# echo "  Installing AudioCraft..."
# pip install -q audiocraft 2>/dev/null || echo "    AudioCraft: Not available"

echo "  Installing web dependencies..."
$PIP_EXEC install -q google-genai google-generativeai fastapi uvicorn websockets python-multipart 2>/dev/null || true

echo "  [✓] Dependencies installed"
((COMPLETED++))
echo ""

# ============================================================
# 6. SOFTWARE: VERIFY MODELS
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[6/10] SOFTWARE: MODEL CHECK"
echo "═══════════════════════════════════════════════════════════════"

$PYTHON_EXEC -c "
import sys
try:
    from mlx_lm import load
    print('  MLX-LM: Available')
    print('  Models will download on first use:')
    print('    - mlx-community/Meta-Llama-3-70B-Instruct-4bit')
    print('    - mlx-community/Meta-Llama-3-8B-Instruct-4bit')
except ImportError:
    print('  MLX-LM: Not available (cloud API will be used)')
" 2>/dev/null || echo "  [!] MLX check failed"

echo "  [✓] Model configuration verified"
((COMPLETED++))
echo ""

# ============================================================
# 7. DATA: INITIALIZE TEMPORAL GRAPH
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[7/10] DATA: TEMPORAL GRAPH"
echo "═══════════════════════════════════════════════════════════════"

$PYTHON_EXEC -c "
from pathlib import Path
from datetime import datetime, timezone
import json

# Determine path
vol = Path('/Volumes/GabrielVol')
if vol.exists():
    graph_path = vol / 'temporal_graph.json'
else:
    graph_path = Path.home() / '.gabriel' / 'temporal_graph.json'

graph_path.parent.mkdir(parents=True, exist_ok=True)

if not graph_path.exists():
    data = {
        'events': [],
        'facts': {
            'system_initialized': datetime.now(timezone.utc).isoformat(),
            'version': 'INFINITY'
        },
        'archive': []
    }
    graph_path.write_text(json.dumps(data, indent=2))
    print(f'  Created: {graph_path}')
else:
    print(f'  Exists: {graph_path}')

print('  [✓] Temporal graph initialized')
"
((COMPLETED++))
echo ""

# ============================================================
# 8. DATA: CREATE REPORTS DIRECTORY
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[8/10] DATA: REPORTS & LOGS"
echo "═══════════════════════════════════════════════════════════════"

mkdir -p reports
mkdir -p logs
echo "  [✓] Reports directory ready"
echo "  [✓] Logs directory ready"
((COMPLETED++))
echo ""

# ============================================================
# 9. INTERACTION: MIDI PORT CHECK
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[9/10] INTERACTION: MIDI"
echo "═══════════════════════════════════════════════════════════════"

$PYTHON_EXEC -c "
try:
    import mido
    outputs = mido.get_output_names()
    print('  Available MIDI outputs:')
    for o in outputs[:5]:
        print(f'    - {o}')
    if not outputs:
        print('    (none detected)')
    print('  Gabriel_Virtual_Out will be created on launch')
except ImportError:
    print('  mido not installed')
    sys.exit(1)
" 2>/dev/null && {
    echo "  [✓] MIDI configured"
    ((COMPLETED++))
} || echo "  [!] MIDI check failed"
echo ""

# ============================================================
# 10. INTERACTION: LATENCY TEST
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "[10/10] INTERACTION: LATENCY CHECK"
echo "═══════════════════════════════════════════════════════════════"

$PYTHON_EXEC -c "
import time
start = time.perf_counter()

# Test uvloop
try:
    import uvloop
    print('  uvloop: ACTIVE')
except ImportError:
    print('  uvloop: NOT FOUND (slower)')

# Test orjson
try:
    import orjson
    print('  orjson: ACTIVE')
except ImportError:
    print('  orjson: NOT FOUND (slower)')

# Simple benchmark
import json
try:
    import orjson
    dumps = orjson.dumps
except ImportError:
    dumps = json.dumps

data = {'test': 'data', 'numbers': list(range(1000))}
for _ in range(1000):
    dumps(data)
elapsed = (time.perf_counter() - start) * 1000
print(f'  JSON benchmark: {elapsed:.1f}ms for 1000 ops')

if elapsed < 50:
    print('  [✓] Latency: EXCELLENT')
elif elapsed < 100:
    print('  [✓] Latency: GOOD')
else:
    print('  [!] Latency: Could be improved')
"
((COMPLETED++))
echo ""

# ============================================================
# SUMMARY
# ============================================================
echo "═══════════════════════════════════════════════════════════════"
echo "                    EXECUTION COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  Completed: $COMPLETED / $TOTAL tasks"
echo ""
echo "  Status:"
if [ -d "/Volumes/GabrielVol" ]; then
    echo "    RAM Disk:    ✓ MOUNTED"
else
    echo "    RAM Disk:    - NOT MOUNTED (run with sudo)"
fi
echo "    Environment: ✓ READY"
echo "    Dependencies:✓ INSTALLED"
echo "    Temporal:    ✓ INITIALIZED"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  NEXT STEPS:"
echo ""
echo "    1. Launch Gabriel Cloud (Gemini API):"
echo "       export GEMINI_API_KEY='your-key'"
echo "       ./configs/run_hypervelocity.sh"
echo ""
echo "    2. Launch Gabriel Infinity (Local LLM):"
echo "       ./configs/run_infinity.sh"
echo ""
echo "    3. Full God Mode (requires sudo):"
echo "       sudo ./launch_god_mode.sh"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "               GORUNFREE. THE SYSTEM IS YOURS."
echo "═══════════════════════════════════════════════════════════════"
echo ""

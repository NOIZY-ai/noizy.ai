#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Configuration & Path Resolution
=================================================
Environment-aware. No hardcoded paths. Works on M2 Ultra locally
and in any deployed environment.
"""

import os
from pathlib import Path


def _resolve_root() -> Path:
    """Resolve NOIZYLAB root from environment or filesystem traversal."""
    # 1. Explicit env var wins
    env_root = os.environ.get("NOIZYLAB_ROOT")
    if env_root:
        return Path(env_root)

    # 2. Walk up from this file to find repo root (contains .git)
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / ".git").exists():
            return current
        current = current.parent

    # 3. Fallback: common locations
    for candidate in [
        Path.home() / "NOIZYLAB",
        Path("/Users/m2ultra/NOIZYLAB"),
        Path("/home/user/NOIZYLAB"),
    ]:
        if candidate.exists():
            return candidate

    # 4. Last resort: cwd
    return Path.cwd()


# ── Root Paths ──────────────────────────────────────────────────────
NOIZYLAB_ROOT = _resolve_root()
GABRIEL_ROOT = NOIZYLAB_ROOT / "gabriel"
MCP_ROOT = GABRIEL_ROOT / "mcp_servers" / "gabriel_mcp"

# ── Data & State ────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("GABRIEL_DATA_DIR", GABRIEL_ROOT / "memcell_data"))
STATE_DIR = Path(os.environ.get("GABRIEL_STATE_DIR", MCP_ROOT / "state" / "sessions"))
LOGS_DIR = Path(os.environ.get("GABRIEL_LOGS_DIR", GABRIEL_ROOT / "logs"))

# ── Brain Files ─────────────────────────────────────────────────────
BRAIN_FILE = DATA_DIR / "gabriel_brain.json"
BRAIN_QUICK_FILE = DATA_DIR / "gabriel_brain_quick.json"
MEMORY_FILE = DATA_DIR / "memory.json"
TASKS_FILE = DATA_DIR / "tasks.json"

# ── Character Definitions ───────────────────────────────────────────
CHARACTERS_DIR = Path(os.environ.get("GABRIEL_CHARACTERS_DIR", GABRIEL_ROOT / "characters"))

# ── Audio Pipeline ──────────────────────────────────────────────────
AUDIO_OUTPUT_DIR = Path(os.environ.get("GABRIEL_AUDIO_DIR", GABRIEL_ROOT / "audio_output"))

# ── Server Config ───────────────────────────────────────────────────
SERVER_NAME = "gabriel-mcp"
SERVER_VERSION = "2.0.0"

# ── Ensure critical directories exist ───────────────────────────────
def ensure_dirs():
    """Create required directories if they don't exist."""
    for d in [DATA_DIR, STATE_DIR, LOGS_DIR, CHARACTERS_DIR, AUDIO_OUTPUT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

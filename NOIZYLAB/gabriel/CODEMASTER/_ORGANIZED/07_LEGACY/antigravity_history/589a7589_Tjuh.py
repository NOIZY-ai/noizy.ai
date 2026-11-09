import os
import sys
import time
from pathlib import Path

# ==============================================================================
# ⚡ TURBO CONFIGURATION (GOD MODE)
# ==============================================================================

# ------------------------------------------------------------------------------
# 🎨 VISUAL SYSTEM (AESTHETICS)
# ------------------------------------------------------------------------------
CYAN    = '\033[96m'
GREEN   = '\033[92m'
YELLOW  = '\033[93m'
RED     = '\033[91m'
MAGENTA = '\033[95m'
BLUE    = '\033[94m'
WHITE   = '\033[97m'
RESET   = '\033[0m'
BOLD    = '\033[1m'
DIM     = '\033[2m'

# ------------------------------------------------------------------------------
# 📂 PATHS & LOCATIONS
# ------------------------------------------------------------------------------
# The root folder of the Scripts
SCRIPTS_DIR = Path(__file__).parent.absolute()

# Important Directories
STAGING_AREA = Path("/Volumes/6TB/Audio_Universe")
REMOTE_DRIVE_NAME = "FISHMUSIC_MASTERS"
REMOTE_PATH = "MC96UNIVERSE"

# Search Paths (For Hunters/Scanners)
DEFAULT_SEARCH_DIRS = [
    Path.expanduser(Path("~/Downloads")),
    Path.expanduser(Path("~/Desktop")),
    Path.expanduser(Path("~/Documents"))
]

# Assets
ASSETS_DIR = Path.expanduser(Path("~/Universal/Library/Assets"))
LOG_DIR = Path("logs")
DATABASE_DIR = SCRIPTS_DIR.parent / "Database"
UNIVERSE_DB_PATH = DATABASE_DIR / "universe.db"
VI_DB_PATH = DATABASE_DIR / "vi_db.json"
ORACLE_INDEX_PATH = DATABASE_DIR / "oracle_index.json"

# ------------------------------------------------------------------------------
# ⚙️  SYSTEM CONSTANTS
# ------------------------------------------------------------------------------
APP_NAME = "AUDIO UNITOR"
VERSION  = "2.0 (TURBO)"
AUTHOR   = "M2ULTRA"
PROTOCOL = "GORUNFREE"

# ------------------------------------------------------------------------------
# 🧠 SHARED FUNCTIONS
# ------------------------------------------------------------------------------
def print_header(title, subtitle=None):
    print(f"\n{BOLD}{CYAN}================================================================{RESET}")
    print(f"{BOLD}{CYAN}   {title.upper()}{RESET}")
    if subtitle:
        print(f"{DIM}   {subtitle}{RESET}")
    print(f"{BOLD}{CYAN}================================================================{RESET}\n")

def print_step(name, status="START"):
    if status == "START":
        print(f"{BOLD}{MAGENTA}CORE > ⛩️  STEP: {name}{RESET}")
    elif status == "SUCCESS":
        print(f"{GREEN}CORE > ✅ {name} COMPLETE.{RESET}")
    elif status == "FAIL":
        print(f"{RED}CORE > ❌ {name} FAILED.{RESET}")

def system_log(msg, level="INFO"):
    timestamp = time.strftime('%H:%M:%S')
    color = WHITE
    if level == "WARN": color = YELLOW
    if level == "ERROR": color = RED
    if level == "SUCCESS": color = GREEN
    
    print(f"{DIM}[{timestamp}]{RESET} {color}{msg}{RESET}")

def ensure_dirs(paths):
    for p in paths:
        if isinstance(p, str): p = Path(p)
        if not p.exists():
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                pass

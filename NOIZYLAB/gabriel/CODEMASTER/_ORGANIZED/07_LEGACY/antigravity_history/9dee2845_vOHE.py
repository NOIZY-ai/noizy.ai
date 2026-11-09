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
# 🌐 NETWORK TOPOLOGY (GOD MODE)
# ------------------------------------------------------------------------------
GIT_REMOTE_URL = "https://github.com/NOIZYLAB-io/Code_Universe.git"

NETWORK_NODES = {
    "127.0.0.1":   {"role": "COMMAND_CENTER", "device": "M2 Ultra Mac Studio", "name": "M2_OMEGA (LOCALHOST)"},
    "10.90.90.20": {"role": "PROCESSING_ENGINE", "device": "HP-OMEN 25L", "name": "GABRIEL"},
    "10.90.90.30": {"role": "ARCHIVES", "device": "Old Mac Pro 12-Core", "name": "THE_VAULT"},
    "10.90.90.50": {"role": "VISUAL_CORTEX", "device": "Meta Quest 2", "name": "GABRIEL_VR"},
    "10.90.90.40": {"role": "MOBILE_OPS", "device": "MacBook Pro", "name": "PLANAR 2485"},
    "DGS1210-10":  {"role": "SWITCH", "device": "D-Link Managed Switch", "name": "NET_CORE"}
}

# ------------------------------------------------------------------------------
# 🚀 MISSION CONTROL
# ------------------------------------------------------------------------------
PORTAL_INTERFACE = "iPad 12.9"
TACTICAL_CONTROL = "Touchscreen via DGS1210-10"

# ------------------------------------------------------------------------------
# ⚙️  SYSTEM CONSTANTS
# ------------------------------------------------------------------------------
APP_NAME = "AUDIO UNITOR"
VERSION  = "2.0 (TURBO)"
AUTHOR   = "M2ULTRA"
PROTOCOL = "GORUNFREE"
ORGANIZATION = "FISHMUSIC INC"
DOMAIN = "fishmusicinc.com"

# ------------------------------------------------------------------------------
# 🔑 API KEYS & SECRETS
# ------------------------------------------------------------------------------
# Centralized retrieval with environment variable fallback
RUNWAY_API_KEY    = os.getenv("RUNWAY_API_KEY")
LUMA_API_KEY      = os.getenv("LUMA_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
ELEVEN_API_KEY    = os.getenv("ELEVEN_API_KEY")
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

API_KEYS = {
    "Runway": RUNWAY_API_KEY,
    "Luma": LUMA_API_KEY,
    "Stability": STABILITY_API_KEY,
    "ElevenLabs": ELEVEN_API_KEY,
    "Gemini": GEMINI_API_KEY,
    "Discord": os.getenv("DISCORD_TOKEN")
}

# ------------------------------------------------------------------------------
# 👥 THE DIGITAL TEAM (PERSONAS)
# ------------------------------------------------------------------------------
TEAM_ROSTER = {
    "GABRIEL": "The Omniscient System Leader (God Mode)",
    "SHIRL": "Executive Creative Assistant (Vibe Guardian)",
    "ENGR_KEITH": "Chief Technical Architect (System Integrity)",
    "ORACLE": "The Prediction Engine",
    "THE_CARRIER": "Discord Communication Relay"
}

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

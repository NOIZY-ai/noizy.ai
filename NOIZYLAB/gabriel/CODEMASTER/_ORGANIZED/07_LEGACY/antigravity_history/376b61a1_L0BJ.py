# ==============================================================================
# 🦅 GABRIEL ALLEGIANCE (SYSTEM LEADER)
# ==============================================================================
# This script operates under the command of GABRIEL.
# PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE
# ==============================================================================

import sys
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

import os
import shutil
import subprocess

# SUPER-SONIC FREEBIES (THE ESSENTIALS)
FREEBIES = [
    {"name": "Raycast", "cask": "raycast", "desc": "Super-charged Spotlight replacement.", "check": "Raycast.app"},
    {"name": "Cloudflare WARP", "cask": "cloudflare-warp", "desc": "Fastest DNS & Secure Tunnel.", "check": "Cloudflare WARP.app"},
    {"name": "Rectangle", "cask": "rectangle", "desc": "Instant Window Management.", "check": "Rectangle.app"},
    {"name": "IINA", "cask": "iina", "desc": "Modern Video Player.", "check": "IINA.app"},
    {"name": "OnyX", "cask": "onyx", "desc": "Deep System Maintenance.", "check": "OnyX.app"},
    {"name": "Keka", "cask": "keka", "desc": "High-speed Archiver.", "check": "Keka.app"},
    {"name": "AltTab", "cask": "alt-tab", "desc": "Windows-style Alt-Tab switcher.", "check": "AltTab.app"},
    {"name": "Hidden Bar", "cask": "hiddenbar", "desc": "Clean up menu bar clutter.", "check": "Hidden Bar.app"}
]

# GOD MODE EXTENSIONS (VS CODE)
EXTENSIONS = [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "esbenp.prettier-vscode",
    "eamodio.gitlens",
    "usernamehw.errorlens",
    "tamasfe.even-better-toml",
    "mechatroner.rainbow-csv"
]

def check_app_installed(app_name):
    """Check if app exists in /Applications."""
    return Path(f"/Applications/{app_name}").exists() or \
           Path(f"{Path.home()}/Applications/{app_name}").exists()

def get_installed_extensions():
    """Get list of VS Code extensions."""
    if not shutil.which("code"): return []
    try:
        res = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True)
        return [l.strip().lower() for l in res.stdout.splitlines()]
    except: return []

def list_freebies():
    cfg.print_header("SUPER-SONIC FREEBIES", "ACTIVE INSTALLATION SCAN")
    
    missing_casks = []
    
    print(f"{cfg.BOLD}CORE > Checking App Essentials:{cfg.RESET}")
    for tool in FREEBIES:
        installed = check_app_installed(tool['check'])
        status = f"{cfg.GREEN}INSTALLED{cfg.RESET}" if installed else f"{cfg.RED}MISSING{cfg.RESET}"
        print(f"   • {tool['name']:<20} [{status}] {cfg.DIM}- {tool['desc']}{cfg.RESET}")
        
        if not installed:
            missing_casks.append(tool['cask'])
            
    print(f"\n{cfg.BOLD}CORE > Checking VS Code Extensions:{cfg.RESET}")
    current_exts = get_installed_extensions()
    missing_exts = []
    
    if not current_exts:
        print(f"   {cfg.YELLOW}(VS Code 'code' CLI not found or inactive){cfg.RESET}")
    else:
        for ext in EXTENSIONS:
            is_in = ext.lower() in current_exts
            status = f"{cfg.GREEN}ACTIVE{cfg.RESET}" if is_in else f"{cfg.RED}MISSING{cfg.RESET}"
            print(f"   • {ext:<30} [{status}]")
            if not is_in: missing_exts.append(ext)

    # ACTION PLAN
    if missing_casks or missing_exts:
        print(f"\n{cfg.BOLD}{cfg.MAGENTA}⚡ OPTIMIZATION PLAN (COPY & RUN):{cfg.RESET}")
        
        if missing_casks:
            casks_str = " ".join(missing_casks)
            print(f"   {cfg.CYAN}brew install --cask {casks_str}{cfg.RESET}")
            
        if missing_exts:
            for ext in missing_exts:
                print(f"   {cfg.CYAN}code --install-extension {ext}{cfg.RESET}")
    else:
        print(f"\n{cfg.GREEN}✨ SYSTEM IS PERFECTLY OPTIMIZED. ALL TOOLS PRESENT.{cfg.RESET}")


if __name__ == "__main__":
    list_freebies()

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

# SUPER-SONIC FREEBIES (THE ESSENTIALS)
FREEBIES = [
    {
        "name": "Raycast",
        "desc": "Super-charged Spotlight replacement. Zero Latency.",
        "url": "https://www.raycast.com/"
    },
    {
        "name": "Cloudflare WARP",
        "desc": "Fastest DNS (1.1.1.1) & Secure Tunnel.",
        "url": "https://1.1.1.1/"
    },
    {
        "name": "Rectangle",
        "desc": "Instant Window Management (Snap to grid).",
        "url": "https://rectangleapp.com/"
    },
    {
        "name": "IINA",
        "desc": "Modern Video Player (The VLC Killer).",
        "url": "https://iina.io/"
    },
    {
        "name": "OnyX",
        "desc": "Deep System Maintenance & Cache Cleaning.",
        "url": "https://titanium-software.fr/en/onyx.html"
    },
    {
        "name": "Keka",
        "desc": "The Ultimate Archiver (Zip/Rar/7z).",
        "url": "https://keka.io/"
    }
]

def list_freebies():
    cfg.print_header("SUPER-SONIC FREEBIES", "3RD PARTY ENGINES")
    
    print(f"{cfg.BOLD}CORE > The following acceleration units are recommended:{cfg.RESET}\n")
    
    for i, tool in enumerate(FREEBIES):
        print(f"   {i+1}. {cfg.CYAN}{tool['name']}{cfg.RESET}")
        print(f"      {cfg.DIM}{tool['desc']}{cfg.RESET}")
        print(f"      🔗 {tool['url']}\n")
        
    print(f"{cfg.GREEN}CORE > Install these to achieve Maximum Velocity.{cfg.RESET}")

if __name__ == "__main__":
    list_freebies()

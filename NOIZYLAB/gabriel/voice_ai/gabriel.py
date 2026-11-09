#!/usr/bin/env python3
"""
🎤 GABRIEL - VOICE AI SYSTEM
Unified entry point for all GABRIEL features
GORUNFREE Protocol
"""

import os
import sys
from pathlib import Path

# Add all modules to path
GABRIEL_DIR = Path(__file__).parent
sys.path.insert(0, str(GABRIEL_DIR / "core"))
sys.path.insert(0, str(GABRIEL_DIR / "advanced"))
sys.path.insert(0, str(GABRIEL_DIR / "ultra"))
sys.path.insert(0, str(GABRIEL_DIR / "utils"))

def main():
    print("🎤 GABRIEL - VOICE AI SYSTEM")
    print("=" * 60)
    print("\nAvailable modules:")
    print("  core      - Basic voice generation")
    print("  advanced  - Advanced features")
    print("  ultra     - Zero latency (optimized)")
    print("  web       - Web interface")
    print("  api       - REST API server")
    print("\nUsage:")
    print("  python3 gabriel.py core --list")
    print("  python3 gabriel.py ultra --generate 'Text'")
    print("  python3 gabriel.py web")
    print("  python3 gabriel.py api")
    
    if len(sys.argv) < 2:
        return
    
    module = sys.argv[1]
    args = sys.argv[2:]
    
    if module == "core":
        os.chdir(GABRIEL_DIR / "core")
        os.system(f"python3 voice_ai_universal.py {' '.join(args)}")
    elif module == "advanced":
        os.chdir(GABRIEL_DIR / "advanced")
        os.system(f"python3 voice_ai_pro.py {' '.join(args)}")
    elif module == "ultra":
        os.chdir(GABRIEL_DIR / "ultra")
        os.system(f"python3 voice_ai_optimized.py {' '.join(args)}")
    elif module == "web":
        os.chdir(GABRIEL_DIR / "web")
        os.system("python3 voice_ai_web.py")
    elif module == "api":
        os.chdir(GABRIEL_DIR / "api")
        os.system("python3 voice_ai_api_server.py")
    else:
        print(f"❌ Unknown module: {module}")

if __name__ == "__main__":
    main()


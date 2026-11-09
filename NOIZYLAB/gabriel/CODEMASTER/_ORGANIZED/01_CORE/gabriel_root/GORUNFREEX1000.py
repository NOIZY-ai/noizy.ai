#!/usr/bin/env python3
"""
GORUNFREEX1000 MASTER LAUNCHER
MC96DIGIUNIVERSE AI LIFELUV SUPREME INTEGRATION
INFINITE ENERGY FOREVER
"""

import sys
from pathlib import Path

# Add core to path
core_path = Path(__file__).parent / "core"
sys.path.insert(0, str(core_path))

def main():
    """Master launcher - choose your destiny"""

    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                🚀 GORUNFREEX1000 MASTER LAUNCHER 🚀               ║
║                                                                   ║
║              MC96DIGIUNIVERSE AI LIFELUV INTEGRATION              ║
║                                                                   ║
║                    ∞ INFINITE ENERGY ∞                            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Choose your mission:

  1. 🌟 Activate DreamChamber (Recommended)
  2. 🔍 Run Visual Scanner
  3. 💫 Full System Integration
  4. ⚡ Quick Status Check
  5. 🚀 All Systems GO!

  0. Exit

""")

    choice = input("Enter choice (1-5, 0 to exit): ").strip()

    if choice == "1":
        from dreamchamber import DreamChamberX1000
        chamber = DreamChamberX1000()
        chamber.run()

    elif choice == "2":
        print("\n⚠️  Visual Scanner takes a while - launching quick version...\n")
        from dreamchamber import DreamChamberX1000
        chamber = DreamChamberX1000()
        chamber.activate_dreamchamber()
        chamber.gather_gabriel_family()
        print("\n✅ Quick scan complete!")

    elif choice == "3":
        from dreamchamber import DreamChamberX1000
        chamber = DreamChamberX1000()
        chamber.run()
        print("\n💫 Creating launcher shortcuts...")
        create_shortcuts()

    elif choice == "4":
        quick_status()

    elif choice == "5":
        from dreamchamber import DreamChamberX1000
        chamber = DreamChamberX1000()
        chamber.run()
        print("\n💫 ALL SYSTEMS ACTIVATED!")

    elif choice == "0":
        print("\n👋 GORUNFREE forever! Exiting...\n")
        sys.exit(0)

    else:
        print("\n❌ Invalid choice. Please try again.\n")
        main()

def quick_status():
    """Quick system status check"""
    from pathlib import Path
    import json

    print("\n⚡ QUICK STATUS CHECK\n")
    print("=" * 60)

    home = Path.home()

    # Check portal
    portal_config = home / "GABRIEL_UNIFIED/mc96_portal/portal_config.json"
    if portal_config.exists():
        with open(portal_config) as f:
            data = json.load(f)
        print(f"✅ MC96 Portal: {data['status']}")
        print(f"⚡ Energy Level: {data['energy_level']}")
        print(f"🚀 GoRunFree Status: {data['gorunfree_status']}")
        print(f"💫 Integrated Systems: {len(data['integrated_systems'])}")
    else:
        print("⚠️  Portal not found - run option 1 to activate!")

    print("=" * 60)

def create_shortcuts():
    """Create convenient shortcuts"""
    home = Path.home()

    # Create a simple run script
    run_script = home / "GABRIEL_UNIFIED" / "run.sh"
    with open(run_script, 'w') as f:
        f.write("""#!/bin/bash
# GORUNFREEX1000 Quick Launcher

/opt/homebrew/bin/python3 "$(dirname "$0")/GORUNFREEX1000.py"
""")

    run_script.chmod(0o755)
    print(f"✅ Created: {run_script}")
    print("   Run with: ./GABRIEL_UNIFIED/run.sh")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. GORUNFREE forever!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

#!/usr/bin/env python3
"""
🦁 CODEBEAST LAUNCHER - GABRIEL EDITION
Launch any GABRIEL system through CODEBEAST
"""

import sys
from pathlib import Path

# Add claws to path
sys.path.insert(0, str(Path(__file__).parent / 'claws'))

SYSTEMS = {
    '1': ('autonomous_learning.py', 'X1000 Autonomous Learning'),
    '2': ('GABRIEL_CODEMASTER.py', 'GABRIEL Codemaster'),
    '3': ('the_fishnet_universe.py', 'Universal Fishnet'),
    '4': ('TERMINUS.py', 'TERMINUS Terminal'),
    '5': ('OMNIDIRECTIONAL.py', 'Omnidirectional Control'),
    '6': ('CODE_VAC.py', 'CODE_VAC'),
    '7': ('SCAN_ALL_DRIVES.py', 'Drive Scanner'),
    '8': ('QUICK_DISTRIBUTE.py', 'Quick Distribute'),
}

def main():
    print("\n" + "=" * 80)
    print("🦁 CODEBEAST - GABRIEL EDITION")
    print("=" * 80)
    
    print("\n🦁 AVAILABLE SYSTEMS:")
    for key, (file, name) in SYSTEMS.items():
        print(f"  {key}. {name}")
    print("  0. Exit")
    
    choice = input("\n🦁 Select system: ").strip()
    
    if choice == '0':
        print("🦁 CODEBEAST standing by.")
        return
    
    if choice in SYSTEMS:
        file, name = SYSTEMS[choice]
        claws_path = Path(__file__).parent / 'claws' / file
        
        if claws_path.exists():
            print(f"\n🚀 Launching {name}...\n")
            exec(open(claws_path).read())
        else:
            print(f"❌ {name} not found")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
X1000 BEAST LAUNCHER
====================
Quantum-enhanced unified launcher for all CODEBEAST systems
"""

import subprocess
import sys
from pathlib import Path

class X1000BeastLauncher:
    def __init__(self):
        self.beast_root = Path(__file__).parent
        self.x1000_claws = self.beast_root / 'claws' / 'x1000'
        self.classic_claws = self.beast_root / 'claws' / 'classic'
        self.python_exec = sys.executable
    
    def show_menu(self):
        print("=" * 70)
        print(" " * 20 + "🦁 X1000 BEAST LAUNCHER 🦁")
        print("="*70)
        
        print("\n⚛️ X1000 QUANTUM CLAWS:")
        x1000_systems = sorted([f.name for f in self.x1000_claws.glob('*.py')])
        for i, system in enumerate(x1000_systems, 1):
            print(f"   {i}. {system}")
        
        print("\n📦 CLASSIC CLAWS:")
        classic_systems = sorted([f.name for f in self.classic_claws.glob('*.py')])
        offset = len(x1000_systems)
        for i, system in enumerate(classic_systems, offset + 1):
            print(f"   {i}. {system}")
        
        print("\n0. Exit")
        
        return x1000_systems + classic_systems
    
    def launch_system(self, systems: list, choice: int):
        if choice < 1 or choice > len(systems):
            print("❌ Invalid choice")
            return
        
        system = systems[choice - 1]
        
        # Determine path
        if (self.x1000_claws / system).exists():
            system_path = self.x1000_claws / system
            print(f"\n⚛️ Launching X1000 Quantum Claw: {system}")
        else:
            system_path = self.classic_claws / system
            print(f"\n📦 Launching Classic Claw: {system}")
        
        print("="*70 + "\n")
        
        try:
            result = subprocess.run([self.python_exec, str(system_path)], cwd=str(self.beast_root))
            print(f"\n✅ System exited with code: {result.returncode}")
        except KeyboardInterrupt:
            print("\n⚠️ System interrupted")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def run(self):
        while True:
            systems = self.show_menu()
            try:
                choice = input("\n👉 Select system (number) or 0 to exit: ").strip()
                
                if choice == '0':
                    print("👋 Beast resting...")
                    break
                
                try:
                    choice_int = int(choice)
                    self.launch_system(systems, choice_int)
                except ValueError:
                    print("❌ Invalid input")
                
                input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\n👋 Beast resting...")
                break

if __name__ == '__main__':
    launcher = X1000BeastLauncher()
    launcher.run()

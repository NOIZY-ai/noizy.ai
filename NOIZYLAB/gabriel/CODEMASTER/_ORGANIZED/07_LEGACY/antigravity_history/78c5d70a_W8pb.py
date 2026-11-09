#!/usr/bin/env python3
"""
👑 GABRIEL SYSTEM CORE
The Central Nervous System of the NOIZYLAB GABRIEL Instance.
Integrates: God Mode Brain, X1000 Learning, Fishnet Surveillance.
Protocol: GOD MODE
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Import Subsystems
from gabriel_brain import GabrielBrain
# Note: autonomous_learning and the_fishnet are scripts, we'll run them as subprocesses or import if refactored.
# For now, we will run them as subprocesses to maintain their isolation and state.

class GabrielSystemCore:
    """
    👑 GABRIEL - The Unified System Orchestrator
    """
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.brain_path = self.workspace / "CB_01_COMPLETE_MUSIC_PRODUCTION_KNOWLEDGE_GOD_MODE.md"
        self.brain = GabrielBrain(self.brain_path) if self.brain_path.exists() else None
        
        self.status = {
            'core': '✅ ONLINE',
            'brain': '✅ ACTIVE' if self.brain else '❌ DETACHED',
            'x1000': '❓ READY',
            'fishnet': '❓ READY',
            'terminal': '❓ CHECKING...'
        }
        
    def show_banner(self):
        print("\n" + "🌌" * 40)
        print("   👑 GABRIEL SYSTEM CORE v7.0 (GOD MODE)")
        print("   Unified Intelligence & Orchestration")
        print("🌌" * 40 + "\n")

    def diagnose_system(self):
        """Quick system heart-beat check."""
        print("🔍 RUNNING SYSTEM DIAGNOSTICS...")
        
        # Check Brain
        if self.brain_path.exists():
            print(f"  🧠 Brain Connection: STABLE ({len(self.brain.entries)} nodes loaded)")
        else:
            print("  🧠 Brain Connection: FAILED (Knowledge Base missing)")
            
        # Check Subsystems
        if (self.workspace / "autonomous_learning.py").exists():
            print("  🎓 X1000 Module: DETECTED")
            self.status['x1000'] = '✅ LOADED'
        else:
            print("  🎓 X1000 Module: MISSING")
            self.status['x1000'] = '❌ ERROR'
            
        if (self.workspace / "the_fishnet.py").exists():
            print("  🎣 Fishnet Module: DETECTED")
            self.status['fishnet'] = '✅ LOADED'
        else:
            print("  🎣 Fishnet Module: MISSING")
            self.status['fishnet'] = '❌ ERROR'
            
        print("\n✅ DIAGNOSTIC COMPLETE.\n")

    def run_brain_interface(self):
        """Interactive interface for God Mode Brain."""
        while True:
            print("\n🧠 GABRIEL BRAIN INTERFACE")
            print("="*40)
            print("1. 🔍 Search Knowledge Base")
            print("2. 🧪 Get Production Recipe")
            print("3. 🎲 Random God Mode Insight")
            print("0. 🔙 Back to Main Menu")
            
            choice = input("\n🧠 QUERY > ").strip()
            
            if choice == '1':
                q = input("  Search Term: ")
                self.brain.search(q)
            elif choice == '2':
                q = input("  Era/Genre (e.g. 1993): ")
                self.brain.get_recipe(q)
            elif choice == '3':
                self.brain.random_insight()
            elif choice == '0':
                break
            else:
                input("Invalid option.")

    def launch_x1000(self):
        """Launch X1000 Learning System."""
        script_path = self.workspace / "autonomous_learning.py"
        if script_path.exists():
            print("\n🚀 INITIALIZING X1000 LEARNING MATRIX...")
            try:
                subprocess.run([sys.executable, str(script_path)])
            except KeyboardInterrupt:
                print("\n⏸️  X1000 SUSPENDED.")
        else:
            print("❌ X1000 Module Not Found.")

    def launch_fishnet(self):
        """Launch Fishnet Surveillance."""
        script_path = self.workspace / "the_fishnet.py"
        if script_path.exists():
            print("\n🎣 DEPLOYING FISHNET...")
            try:
                subprocess.run([sys.executable, str(script_path)])
            except KeyboardInterrupt:
                print("\n⏸️  FISHNET RETRACTED.")
        else:
            print("❌ Fishnet Module Not Found.")

    def main_loop(self):
        self.show_banner()
        self.diagnose_system()
        
        while True:
            print("👑 COMMAND DECK")
            print("="*40)
            print("1. 🧠 Access God Mode Brain")
            print("2. 🎓 Launch X1000 Autonomous Learning")
            print("3. 🎣 Run Fishnet Code Scan")
            print("4. 🔍 System Diagnostics")
            print("0. 🛑 SHUTDOWN SYSTEM")
            
            choice = input("\n👑 COMMAND > ").strip()
            
            if choice == '1':
                if self.brain:
                    self.run_brain_interface()
                else:
                    print("❌ Brain not connected.")
            elif choice == '2':
                self.launch_x1000()
            elif choice == '3':
                self.launch_fishnet()
            elif choice == '4':
                self.diagnose_system()
            elif choice == '0':
                print("\n🌌 GABRIEL SYSTEM GOING DARK. GORUNFREE.")
                break
            else:
                print("❌ Invalid Command.")
                
            print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    core = GabrielSystemCore()
    core.main_loop()

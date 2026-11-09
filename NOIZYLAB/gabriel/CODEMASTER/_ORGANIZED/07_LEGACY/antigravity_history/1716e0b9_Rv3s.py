#!/usr/bin/env python3
"""
👑 GABRIEL SYSTEM GUARDIAN
The Central Nervous System & Active Monitor of the NOIZYLAB Instance.
Protocol: GOD MODE | Aesthetics: PREMIUM
Integrates: Brain (Knowledge), Fishnet (Vision), X1000 (Learning)
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Optional

# Import Subsystems
from gabriel_brain import GabrielBrain

# === AESTHETICS ENGINE ===
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def print_banner():
        print(f"{Colors.BLUE}")
        print("🌌" * 50)
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("   👑  G A B R I E L   S Y S T E M   G U A R D I A N")
        print("       v8.0 | OMNISCIENT CORE | GOD MODE ACTIVE")
        print(f"{Colors.ENDC}{Colors.BLUE}")
        print("🌌" * 50)
        print(f"{Colors.ENDC}")

    @staticmethod
    def status(component, status, detail=""):
        symbol = "✅" if "ONLINE" in status or "ACTIVE" in status or "LOADED" in status else "❌"
        if "CHECKING" in status: symbol = "⏳"
        col = Colors.GREEN if symbol == "✅" else Colors.FAIL
        if symbol == "⏳": col = Colors.WARNING
        print(f"   {symbol} {Colors.BOLD}{component:<15}{Colors.ENDC} : {col}{status:<10}{Colors.ENDC} {Colors.CYAN}{detail}{Colors.ENDC}")

class SystemGuardian:
    """
    👑 GABRIEL GUARDIAN - The Orchestrator
    """
    
    def __init__(self):
        self.workspace = Path.cwd()
        
        # Locate Brain
        self.brain_path = Path("CB_01_COMPLETE_MUSIC_PRODUCTION_KNOWLEDGE_GOD_MODE.md")
        # Fallback search if moved
        if not self.brain_path.exists():
             possible_paths = [
                 Path("PROJECTS_MASTER/MUSIC_INTELLIGENCE") / self.brain_path.name,
                 Path("../MUSIC_INTELLIGENCE") / self.brain_path.name
             ]
             for p in possible_paths:
                 if p.exists():
                     self.brain_path = p
                     break

        self.brain = GabrielBrain(self.brain_path) if self.brain_path.exists() else None
        
        self.status = {
            'Guardian': '✅ ONLINE',
            'Brain': '✅ ACTIVE' if self.brain else '❌ DETACHED',
            'X1000': '❓ SCANNING',
            'Fishnet': '❓ SCANNING'
        }
        
    def boot_sequence(self):
        os.system('clear')
        Colors.print_banner()
        print(f"\n{Colors.CYAN}📋 INITIALIZING GUARDIAN PROTOCOLS...{Colors.ENDC}\n")
        time.sleep(0.5)
        
        # Brain Check
        if self.brain:
            Colors.status("Global Brain", "ACTIVE", f"({len(self.brain.entries)} Core Nodes)")
        else:
            Colors.status("Global Brain", "OFFLINE", "Knowledge Base Unreachable")
            
        time.sleep(0.3)
        
        # Subsystem Check
        x1000_path = self.find_component("autonomous_learning.py")
        if x1000_path:
            Colors.status("X1000 Matrix", "LOADED", "Autonomous Learning Ready")
            self.status['X1000'] = '✅ LOADED'
        else:
            Colors.status("X1000 Matrix", "MISSING", "Module Not Found")
            
        time.sleep(0.3)
        
        fishnet_path = self.find_component("the_fishnet.py")
        if fishnet_path:
            Colors.status("The Fishnet", "LOADED", "Surveillance System Ready")
            self.status['Fishnet'] = '✅ LOADED'
        else:
            Colors.status("The Fishnet", "MISSING", "Module Not Found")

        print(f"\n{Colors.GREEN}✨ SYSTEM READY. WAITING FOR COMMAND.{Colors.ENDC}\n")

    def find_component(self, filename):
        """Smart find for components in local or master structure."""
        if (self.workspace / filename).exists(): return self.workspace / filename
        # Check Master Structure locations
        if (self.workspace / "GABRIEL_CORE" / filename).exists(): return self.workspace / "GABRIEL_CORE" / filename
        # Check current dir if script is running inside GABRIEL_CORE
        if (Path(".") / filename).exists(): return Path(".") / filename
        return None

    def run_brain_interface(self):
        """Interactive interface for God Mode Brain."""
        while True:
            print(f"\n{Colors.HEADER}🧠 GABRIEL BRAIN INTERFACE{Colors.ENDC}")
            print(f"{Colors.BLUE}="*40 + f"{Colors.ENDC}")
            print(f"{Colors.CYAN}1. 🔍 Search Knowledge Base")
            print(f"2. 🧪 Get Production Recipe")
            print(f"3. 🎲 Random God Mode Insight")
            print(f"4. 🧠 Ask the Guardian (AI Help)")
            print(f"0. 🔙 Back to Command Deck{Colors.ENDC}")
            
            choice = input(f"\n{Colors.HEADER}🧠 QUERY > {Colors.ENDC}").strip()
            
            if choice == '1':
                q = input(f"  {Colors.CYAN}Search Term: {Colors.ENDC}")
                self.brain.search(q)
            elif choice == '2':
                q = input(f"  {Colors.CYAN}Era/Genre (e.g. 1993): {Colors.ENDC}")
                self.brain.get_recipe(q)
            elif choice == '3':
                self.brain.random_insight()
            elif choice == '4':
                print(f"{Colors.WARNING}⚠️  Guardian AI Connection: STANDBY (NLP Module Active){Colors.ENDC}")
            elif choice == '0':
                break
            else:
                pass

    def launch_x1000(self):
        script_path = self.find_component("autonomous_learning.py")
        if script_path:
            print(f"\n{Colors.HEADER}🚀 INITIALIZING X1000 LEARNING MATRIX...{Colors.ENDC}")
            try:
                subprocess.run([sys.executable, str(script_path)])
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}⏸️  X1000 SUSPENDED.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ X1000 Module Not Found.{Colors.ENDC}")

    def run_fishnet_scan(self):
        script_path = self.find_component("the_fishnet.py")
        if script_path:
            print(f"\n{Colors.HEADER}🎣 DEPLOYING FISHNET SURVEILLANCE...{Colors.ENDC}")
            try:
                # Pass a flag to fishnet if supported, or just run it
                subprocess.run([sys.executable, str(script_path)])
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}⏸️  FISHNET RETRACTED.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ Fishnet Module Not Found.{Colors.ENDC}")

    def main_loop(self):
        self.boot_sequence()
        
        while True:
            print(f"{Colors.HEADER}👑 GUARDIAN COMMAND DECK{Colors.ENDC}")
            print(f"{Colors.BLUE}="*40 + f"{Colors.ENDC}")
            print(f"{Colors.BOLD}1. 🧠 Access God Mode Brain{Colors.ENDC}")
            print(f"{Colors.BOLD}2. 🎓 Launch X1000 (Autonomous Learning){Colors.ENDC}")
            print(f"{Colors.BOLD}3. 🎣 Run Fishnet (System Scan){Colors.ENDC}")
            print(f"{Colors.BOLD}4. 🔄 System Reboot (Diagnostics){Colors.ENDC}")
            print(f"{Colors.FAIL}0. 🛑 SHUTDOWN SYSTEM{Colors.ENDC}")
            
            choice = input(f"\n{Colors.HEADER}👑 COMMAND > {Colors.ENDC}").strip()
            
            if choice == '1':
                if self.brain:
                    self.run_brain_interface()
                else:
                    print(f"{Colors.FAIL}❌ Brain not connected.{Colors.ENDC}")
            elif choice == '2':
                self.launch_x1000()
            elif choice == '3':
                self.run_fishnet_scan()
            elif choice == '4':
                self.boot_sequence()
            elif choice == '0':
                print(f"\n{Colors.BLUE}🌌 GABRIEL GUARDIAN GOING DARK. GORUNFREE.{Colors.ENDC}")
                break
            else:
                print(f"{Colors.FAIL}❌ Invalid Command.{Colors.ENDC}")
                
            print("\n" + f"{Colors.BLUE}-"*40 + f"{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        core = SystemGuardian()
        core.main_loop()
    except KeyboardInterrupt:
        print(f"\n{Colors.BLUE}🌌 SYSTEM HALTED.{Colors.ENDC}")

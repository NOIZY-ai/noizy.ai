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
# Import Subsystems
from gabriel_brain import GabrielBrain
from gabriel_voice import GabrielVoice
from gabriel_player import GabrielPlayer

# Add MemCell to path
try:
    sys.path.append(str(Path(__file__).parent / "MEMCELL"))
    from MEMCELL_CORE import MemCellCore
except ImportError:
    MemCellCore = None

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
        print("       v9.0 | OMNISCIENT CORE | GOD MODE ACTIVE")
        print("       ZERO LATENCY | MAX EFFECTIVENESS | 100% PERFECT")
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
        self.memory = MemCellCore() if MemCellCore else None
        self.voice = GabrielVoice(voice="Samantha", rate=180)
        self.voice.greet()
        self.player = GabrielPlayer()
        
        # WARP Drive Check
        # Check if cloudflared is running in background (rudimentary check)
        try:
            res = subprocess.run(["pgrep", "cloudflared"], capture_output=True)
            warp_status = "✅ ONLINE" if res.returncode == 0 else "❌ OFFLINE"
            self.status = {'Portal Uplink': warp_status} # Initialize self.status here
        except:
             self.status = {'Portal Uplink': "❓ UNKNOWN"} # Initialize self.status here

        self.status = {
            'Guardian': '✅ ONLINE',
            'Brain': '✅ ACTIVE' if self.brain else '❌ DETACHED',
            'MemCell': '✅ CONNECTED' if self.memory else '❌ DETACHED',
            'Portal Uplink': self.status.get('Portal Uplink', '❌ OFFLINE'),
            'X1000': '❓ SCANNING',
            'Fishnet': '❓ SCANNING'
        }
        
    def boot_sequence(self):
        os.system('clear')
        Colors.print_banner()
        print(f"\n{Colors.CYAN}📋 INITIALIZING GUARDIAN PROTOCOLS...{Colors.ENDC}\n")
        time.sleep(0.3)
        
        # Brain Check
        if self.brain:
            Colors.status("Global Brain", "ACTIVE", f"({len(self.brain.entries)} Core Nodes)")
        else:
            Colors.status("Global Brain", "OFFLINE", "Knowledge Base Unreachable")
            
        time.sleep(0.1)
        
        # MemCell Check
        if self.memory:
            Colors.status("MemCell Core", "CONNECTED", f"({len(self.memory.db)} Memories Available)")
        else:
            Colors.status("MemCell Core", "OFFLINE", "Memory Core Unreachable")

        time.sleep(0.1)
        
        # WARP Drive Check
        Colors.status("Portal Uplink", self.status['Portal Uplink'], "Cloudflare Tunnel Status")
        time.sleep(0.1)
        
        # Subsystem Check
        x1000_path = self.find_component("autonomous_learning.py")
        if x1000_path:
            Colors.status("X1000 Matrix", "LOADED", "Autonomous Learning Ready")
            self.status['X1000'] = '✅ LOADED'
        else:
            Colors.status("X1000 Matrix", "MISSING", "Module Not Found")
            
        time.sleep(0.1)
        
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

    def launch_warp_drive(self):
        """Engages the Cloudflare WARP Drive."""
        script_path = self.find_component("warp_drive.py")
        if script_path:
             print(f"\n{Colors.HEADER}🚀 ENGAGING WARP DRIVE...{Colors.ENDC}")
             try:
                 # Running strictly via python3 to ensure new window/process control
                 subprocess.run([sys.executable, str(script_path)])
             except KeyboardInterrupt:
                 print(f"\n{Colors.WARNING}⏸️  WARP DRIVE DISENGAGED.{Colors.ENDC}")
        else:
             print(f"{Colors.FAIL}❌ WARP Drive Module Not Found.{Colors.ENDC}")

    def run_brain_interface(self):
        """Interactive interface for God Mode Brain."""
        while True:
            print(f"\n{Colors.HEADER}🧠 GABRIEL BRAIN INTERFACE{Colors.ENDC}")
            print(f"{Colors.BLUE}="*40 + f"{Colors.ENDC}")
            print(f"{Colors.CYAN}1. 🔍 Search Knowledge Base")
            print(f"2. 🧪 Get Production Recipe")
            print(f"3. 🎲 Random God Mode Insight")
            print(f"0. 🔙 Back to Command Deck{Colors.ENDC}")
            
            choice = self.voice.ask("Awaiting your command, Commander.")
            
            if choice == '1':
                q = self.voice.ask("What knowledge do you seek?")
                self.brain.search(q)
            elif choice == '2':
                q = self.voice.ask("Which era or genre shall I analyze?")
                self.brain.get_recipe(q)
            elif choice == '3':
                self.brain.random_insight()
            elif choice == '0':
                break
            else:
                pass
    
    def run_memcell_interface(self):
        """Interactive interface for MemCell."""
        if not self.memory:
            print(f"{Colors.FAIL}❌ MemCell Not Connected.{Colors.ENDC}")
            return

        while True:
            print(f"\n{Colors.HEADER}🧠 MEMCELL GUARDIAN INTERFACE{Colors.ENDC}")
            print(f"{Colors.BLUE}="*40 + f"{Colors.ENDC}")
            print(f"{Colors.CYAN}1. 📜 Review Recent Memories")
            print(f"2. 🔍 Search Memory Bank")
            print(f"3. ➕ Inject New Thought")
            print(f"0. 🔙 Back to Command Deck{Colors.ENDC}")
            
            choice = self.voice.ask("Accessing Memory Core. State your directive.")
            
            if choice == '1':
                print("\n📜 RECENT MEMORIES:")
                for m in self.memory.get_recent(5):
                    print(self.memory.format_memory_for_display(m))
            elif choice == '2':
                q = self.voice.ask("What memory trace are we tracking?")
                res = self.memory.search_memories(q)
                for m in res:
                    print(self.memory.format_memory_for_display(m))
            elif choice == '3':
                c = input(f"  {Colors.CYAN}Content: {Colors.ENDC}")
                t = input(f"  {Colors.CYAN}Topic (Optional): {Colors.ENDC}")
                self.memory.add_memory(c, topic=t if t else "GuardianLog", author="GUARDIAN")
                print("✅ Memory Injected.")
            elif choice == '0':
                break

    def run_matrix_interface(self):
        """Interactive interface for MemCell Expertise & Project Matrix."""
        if not self.memory:
            print(f"{Colors.FAIL}❌ MemCell Not Connected.{Colors.ENDC}")
            return

        while True:
            print(f"\n{Colors.HEADER}🧬 MEMCELL MATRIX INTERFACE{Colors.ENDC}")
            print(f"{Colors.BLUE}="*40 + f"{Colors.ENDC}")
            print(f"{Colors.CYAN}1. 🔍 Find Expert (Who is good at...?)")
            print(f"2. 👥 View Project Roster (Who is on...?)")
            print(f"3. ➕ Register Expertise")
            print(f"4. 📊 Update Project Status")
            print(f"0. 🔙 Back to Command Deck{Colors.ENDC}")
            
            choice = input(f"\n{Colors.HEADER}🧬 MATRIX > {Colors.ENDC}").strip()
            
            if choice == '1':
                skill = input(f"  {Colors.CYAN}Skill: {Colors.ENDC}")
                experts = self.memory.find_expert(skill)
                if experts:
                    print(f"\n  🧬 EXPERTS IN '{skill.upper()}': {Colors.GREEN}{', '.join(experts)}{Colors.ENDC}")
                else:
                    print(f"  ❌ No experts found for {skill}")
            elif choice == '2':
                proj = input(f"  {Colors.CYAN}Project Name: {Colors.ENDC}")
                team = self.memory.get_project_roster(proj)
                if team:
                    print(f"\n  👥 TEAM FOR '{proj.upper()}': {Colors.GREEN}{', '.join(team)}{Colors.ENDC}")
                else:
                    print(f"  ❌ No team found (or project inactive).")
            elif choice == '3':
                auth = input(f"  {Colors.CYAN}Author (e.g., SHIRL): {Colors.ENDC}")
                skill = input(f"  {Colors.CYAN}Skill: {Colors.ENDC}")
                self.memory.register_expertise(auth, skill)
            elif choice == '4':
                name = input(f"  {Colors.CYAN}Project Name: {Colors.ENDC}")
                status = input(f"  {Colors.CYAN}Status: {Colors.ENDC}")
                team_raw = input(f"  {Colors.CYAN}Assigned Team (comma-seperated): {Colors.ENDC}")
                team = [t.strip() for t in team_raw.split(',') if t.strip()]
                self.memory.track_project(name, status, assigned_to=team)
            elif choice == '0':
                break

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
            print(f"{Colors.BOLD}2. 🧬 Access MemCell Memory Bank{Colors.ENDC}")
            print(f"{Colors.BOLD}3. 👥 Team & Skills Matrix{Colors.ENDC}")
            print(f"{Colors.BOLD}4. 🚀 Engage WARP Drive (Portal Uplink){Colors.ENDC}")
            print(f"{Colors.BOLD}5. 🎓 Launch X1000 (Autonomous Learning){Colors.ENDC}")
            print(f"{Colors.BOLD}6. 🎣 Run Fishnet (System Scan){Colors.ENDC}")
            print(f"{Colors.BOLD}7. 🔄 System Reboot (Diagnostics){Colors.ENDC}")
            print(f"{Colors.BOLD}8. 🗣️  Voice Settings / Test{Colors.ENDC}")
            print(f"{Colors.BOLD}9. 🎧 Gabriel Player / DJ Mode{Colors.ENDC}")
            print(f"{Colors.FAIL}0. 🛑 SHUTDOWN SYSTEM{Colors.ENDC}")
            
            choice = self.voice.ask("System Guardian Active. What is your will?")
            
            if choice == '1':
                if self.brain:
                    self.run_brain_interface()
                else:
                    print(f"{Colors.FAIL}❌ Brain not connected.{Colors.ENDC}")
            elif choice == '2':
                 self.run_memcell_interface()
            elif choice == '3':
                 self.run_matrix_interface()
            elif choice == '4':
                self.launch_warp_drive()
            elif choice == '5':
                self.launch_x1000()
            elif choice == '6':
                self.run_fishnet_scan()
            elif choice == '7':
                self.boot_sequence()
            elif choice == '8':
                 self.voice.speak("Voice systems fully operational. I am ready to serve.", block=True)
            elif choice == '9':
                 self.player.dj_random()
                 self.voice.speak("Dropping the beat. Audio systems engaged.", block=False)
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

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

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Optional

# === SYSTEM PATH HEALING ===
# Ensure all packages are visible
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR)) # Root
sys.path.append(str(BASE_DIR / "packages" / "memcell")) # GraphRAG
sys.path.append(str(BASE_DIR / "packages" / "telemetry")) # Dashboard
sys.path.append(str(BASE_DIR / "MEMCELL")) # Legacy MemCell

# Import Subsystems
from gabriel_brain import GabrielBrain
# Subsystem Imports
try:
    from gabriel_voice import GabrielVoice
    from gabriel_vision import GabrielVision
    from gabriel_spirit import GabrielSpirit
    from gabriel_sonic import GabrielSonic
    from packages.media.google_veo import GoogleVeoClient
    from packages.media.elevenlabs import ElevenLabsClient
    from packages.telemetry.neural_link import get_neural_link
except ImportError as e:
    print(f"⚠️ COMPONENT LOAD ERROR: {e}")
    GabrielVoice = None
    GabrielVision = None
    GabrielSpirit = None
    GabrielSonic = None
    GoogleVeoClient = None
    ElevenLabsClient = None
    get_neural_link = None

from gabriel_player import GabrielPlayer
from gabriel_dashboard import GabrielDashboard
from gabriel_preacher import GabrielPreacher
from memcell_sweeper import main as run_sweeper
from memcell_truth_scanner import main as run_truth_scan
from mc96_librarian import MC96Librarian
# Add MemCell to path (Robust)
try:
    # Try looking in local packages first
    pkg_path = str(Path(__file__).parent / "packages" / "memcell")
    if pkg_path not in sys.path: sys.path.append(pkg_path)
    
    # Try looking in MEMCELL folder (Legacy but containing CORE)
    legacy_path = str(Path(__file__).parent / "MEMCELL")
    if legacy_path not in sys.path: sys.path.append(legacy_path)

    from MEMCELL_CORE import MemCellCore
except ImportError as e:
    print(f"DEBUG: MemCell Import Error: {e}") 
    MemCellCore = None

# Telemetry & Neural Link
try:
    telemetry_path = str(Path(__file__).parent / "packages" / "telemetry")
    if telemetry_path not in sys.path: sys.path.append(telemetry_path)
    
    from neural_link import get_neural_link
except ImportError as e:
    print(f"DEBUG: NeuralLink Import Error: {e}")
    get_neural_link = None

from autonomous_learning import AutonomousLearning
from the_fishnet import TheFishnet


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

    # Aliases for compatibility
    OKGREEN = GREEN
    OKCYAN = CYAN
    OKBLUE = BLUE

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
        symbol = "✅" if any(x in status for x in ["ONLINE", "ACTIVE", "LOADED", "CONNECTED"]) else "❌"
        if "CHECKING" in status: symbol = "⏳"
        col = Colors.GREEN if symbol == "✅" else Colors.FAIL
        if symbol == "⏳": col = Colors.WARNING
        print(f"   {symbol} {Colors.BOLD}{component:<15}{Colors.ENDC} : {col}{status:<10}{Colors.ENDC} {Colors.CYAN}{detail}{Colors.ENDC}")

class SystemGuardian:
    """
    👑 GABRIEL GUARDIAN - The Orchestrator
    """

    COLOR_SCHEMES = {
        'GOD_MODE': {'header': Colors.HEADER, 'prompt': Colors.BLUE, 'voice': 'Samantha'},
        'ASSISTANT': {'header': Colors.OKGREEN, 'prompt': Colors.OKCYAN, 'voice': 'Daniel'},
        'HAL': {'header': Colors.FAIL, 'prompt': Colors.FAIL, 'voice': 'Fred'}
    }

    def __init__(self):
        self.workspace = Path.cwd()
        self.current_persona = 'GOD_MODE'
        
        # Load Master Prompt
        self.system_prompt = "You are GABRIEL. God Mode Active."
        prompt_path = Path(__file__).parent / "packages" / "prompts" / "MASTER_PROMPT_CONTRACT.md"
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                self.system_prompt = f.read()
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
        self.vision = GabrielVision()
        self.spirit = GabrielSpirit()
        self.sonic = GabrielSonic()
        self.dashboard = GabrielDashboard()
        self.preacher = GabrielPreacher()
        # Initialize Librarian to enforce structure on boot
        MC96Librarian()
        
        # Neural Link
        self.link = None
        if get_neural_link:
            try:
                self.link = get_neural_link()
                self.link.start()
                self.link.broadcast("system_boot", {"status": "online"})
            except Exception as e:
                print(f"DEBUG: Neural Link Init Failed: {e}")

        self.voice.speak("System Guardian initialized. Components loaded: Memory, Logic, Voice, Vision, Spirit, Dashboard, Preacher.")

        # Subsystems (Lazy Load or Init)
        self.x1000 = AutonomousLearning()
        self.x1000.start() # Trigger background warmup
        self.fishnet = TheFishnet(root_path=self.workspace.parent) # Scan up one level by default
        self.fishnet.start() # Background Scan

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
        print(f"\n{Colors.CYAN}📋 INITIALIZING GUARDIAN PROTOCOLS... (ZERO LATENCY MODE){Colors.ENDC}\n")
        
        # Parallel Checks (simulated by non-blocking prints)
        
        # Brain Check
        if self.brain:
            Colors.status("Global Brain", "ACTIVE", f"({len(self.brain.entries)} Nodes)")
        else:
            Colors.status("Global Brain", "OFFLINE", "Unreachable")

        # MemCell Check (GraphRAG enabled)
        if self.memory:
            # Quick check on graph nodes if available
            graph_status = ""
            if self.memory.graph:
                 graph_status = f"+ {len(self.memory.graph.graph.nodes())} Graph Nodes"
            Colors.status("MemCell Core", "CONNECTED", f"({len(self.memory.db)} Memories {graph_status})")
        else:
            Colors.status("MemCell Core", "OFFLINE", "Unreachable")

        # WARP Drive Check
        Colors.status("Portal Uplink", self.status['Portal Uplink'], "Cloudflare Tunnel")

        # Subsystem Check
        x1000_path = self.find_component("autonomous_learning.py")
        if x1000_path:
            Colors.status("X1000 Matrix", "LOADED", "Ready")
            self.status['X1000'] = '✅ LOADED'
        else:
            Colors.status("X1000 Matrix", "MISSING", "Not Found")

        fishnet_path = self.find_component("the_fishnet.py")
        if fishnet_path:
            Colors.status("The Fishnet", "LOADED", "Ready")
            self.status['Fishnet'] = '✅ LOADED'
        else:
            Colors.status("The Fishnet", "MISSING", "Not Found")

        print(f"\n{Colors.GREEN}✨ SYSTEM READY.{Colors.ENDC}\n")

    def find_component(self, filename):
        """Smart find for components in local or master structure."""
        if (self.workspace / filename).exists(): return self.workspace / filename
        # Check Master Structure locations
        if (self.workspace / "GABRIEL_CORE" / filename).exists(): return self.workspace / "GABRIEL_CORE" / filename
        # Check current dir if script is running inside GABRIEL_CORE
        if (Path(".") / filename).exists(): return Path(".") / filename
        return None

    def check_action_queue(self):
        """Checks for pending actions in the queue"""
        queue_path = self.find_component("MEMCELL/ACTION_QUEUE.md")
        if not queue_path or not queue_path.exists(): return

        try:
            with open(queue_path, 'r') as f:
                lines = f.readlines()

            # Count unchecked boxes
            pending = sum(1 for line in lines if "- [ ]" in line)

            if pending > 0:
                print(f"{Colors.WARNING}   ⚡ PENDING ACTIONS: {pending} items require attention.{Colors.ENDC}")
                self.voice.speak(f"You have {pending} pending actions in the queue.", block=False)
            else:
                print(f"{Colors.OKGREEN}   ⚡ ACTION QUEUE:    Clear.{Colors.ENDC}")
        except Exception:
            pass

    def check_warp_drive(self):
        """ Checks status of Cloudflare WARP connection """
        # Look for status file or process
        warp_status = False
        try:
            # Check for cloudflared process
            result = subprocess.run(["pgrep", "cloudflared"], capture_output=True)
            if result.returncode == 0:
                warp_status = True
        except Exception:
            pass

        if warp_status:
            print(f"{Colors.OKGREEN}   ⚡ PORTAL UPLINK:   ONLINE (Secure Tunnel Active){Colors.ENDC}")
            self.voice.speak("Portal Uplink Online.", block=False)
            self.status['Portal Uplink'] = '✅ ONLINE'
        else:
            print(f"{Colors.FAIL}   ⚡ PORTAL UPLINK:   OFFLINE (Connection Severed){Colors.ENDC}")
            self.voice.speak("Portal Uplink Offline.", block=False)
            self.status['Portal Uplink'] = '❌ OFFLINE'

    def log_interaction(self, speaker, content):
        """Active Listening: Save coversation to MemCell"""
        if self.memory:
            try:
                self.memory.add_memory(
                    content=content,
                    topic="Conversation",
                    author=speaker,
                    subject="User Interaction",
                    group="SHIRL_ARCHIVE", # Shirl captures the atomic memcells
                    tags=["VOICE_LOG", self.current_persona]
                )
                
                # Neural Link Pulse
                if self.link:
                    self.link.broadcast("voice_active", {"speaker": speaker, "content": content})
                    
            except Exception as e:
                print(f"{Colors.WARNING}Memory Error: {e}{Colors.ENDC}")

    def switch_persona(self):
        """Cycles through personalities"""
        personas = list(self.COLOR_SCHEMES.keys())
        current_idx = personas.index(self.current_persona)
        next_idx = (current_idx + 1) % len(personas)
        self.current_persona = personas[next_idx]

        scheme = self.COLOR_SCHEMES[self.current_persona]
        self.voice = GabrielVoice(voice=scheme['voice']) # Re-init voice

        msg = f"Persona switched to {self.current_persona}."
        print(f"\n🎭 {msg}")
        self.voice.speak(msg, block=True)

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
            self.log_interaction("USER", f"Brain Interface Choice: {choice}")

            if choice == '1':
                q = self.voice.ask("What knowledge do you seek?")
                self.log_interaction("USER", f"Brain Search Query: {q}")
                self.brain.search(q)
            elif choice == '2':
                q = self.voice.ask("Which era or genre shall I analyze?")
                self.log_interaction("USER", f"Brain Recipe Query: {q}")
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
            self.log_interaction("USER", f"MemCell Interface Choice: {choice}")

            if choice == '1':
                print("\n📜 RECENT MEMORIES:")
                for m in self.memory.get_recent(5):
                    print(self.memory.format_memory_for_display(m))
            elif choice == '2':
                q = self.voice.ask("What memory trace are we tracking?")
                self.log_interaction("USER", f"MemCell Search Query: {q}")
                res = self.memory.search_memories(q)
                for m in res:
                    print(self.memory.format_memory_for_display(m))
            elif choice == '3':
                c = input(f"  {Colors.CYAN}Content: {Colors.ENDC}")
                t = input(f"  {Colors.CYAN}Topic (Optional): {Colors.ENDC}")
                self.memory.add_memory(c, topic=t if t else "GuardianLog", author="GUARDIAN")
                self.log_interaction("GABRIEL", f"Injected Memory: {c} (Topic: {t})")
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
            self.log_interaction("USER", f"Matrix Interface Choice: {choice}")

            if choice == '1':
                skill = input(f"  {Colors.CYAN}Skill: {Colors.ENDC}")
                self.log_interaction("USER", f"Matrix Find Expert Skill: {skill}")
                experts = self.memory.find_expert(skill)
                if experts:
                    print(f"\n  🧬 EXPERTS IN '{skill.upper()}': {Colors.GREEN}{', '.join(experts)}{Colors.ENDC}")
                else:
                    print(f"  ❌ No experts found for {skill}")
            elif choice == '2':
                proj = input(f"  {Colors.CYAN}Project Name: {Colors.ENDC}")
                self.log_interaction("USER", f"Matrix Project Roster Query: {proj}")
                team = self.memory.get_project_roster(proj)
                if team:
                    print(f"\n  👥 TEAM FOR '{proj.upper()}': {Colors.GREEN}{', '.join(team)}{Colors.ENDC}")
                else:
                    print(f"  ❌ No team found (or project inactive).")
            elif choice == '3':
                auth = input(f"  {Colors.CYAN}Author (e.g., SHIRL): {Colors.ENDC}")
                skill = input(f"  {Colors.CYAN}Skill: {Colors.ENDC}")
                self.memory.register_expertise(auth, skill)
                self.log_interaction("GABRIEL", f"Registered expertise for {auth}: {skill}")
            elif choice == '4':
                name = input(f"  {Colors.CYAN}Project Name: {Colors.ENDC}")
                status = input(f"  {Colors.CYAN}Status: {Colors.ENDC}")
                team_raw = input(f"  {Colors.CYAN}Assigned Team (comma-seperated): {Colors.ENDC}")
                team = [t.strip() for t in team_raw.split(',') if t.strip()]
                self.memory.track_project(name, status, assigned_to=team)
                self.log_interaction("GABRIEL", f"Updated project {name} status to {status}")
            elif choice == '0':
                break

    def launch_x1000(self):
        print(f"\n{Colors.HEADER}🚀 ENGAGING X1000 LEARNING MATRIX...{Colors.ENDC}")
        self.voice.speak("Engaging Learning Matrix.", block=True)
        self.log_interaction("GABRIEL", "Engaging X1000 Learning Matrix.")

        # Display X1000 Stats
        stats = self.x1000.stats
        report = f"Knowledge Graph contains {len(self.x1000.knowledge_graph)} nodes. {stats['skills_mastered']} skills mastered."
        print(f"{Colors.CYAN}📊 {report}{Colors.ENDC}")
        self.voice.speak(report)
        self.log_interaction("GABRIEL", report)

        self.voice.speak("Autonomous optimization is active.", block=False)

    def run_fishnet_scan(self):
        print(f"\n{Colors.HEADER}🎣 DEPLOYING FISHNET SURVEILLANCE...{Colors.ENDC}")
        self.voice.speak("Deploying Fishnet surveillance.", block=True)
        self.log_interaction("GABRIEL", "Deploying Fishnet surveillance.")

        # Visuals
        self.vision.animate(duration=3)

        # Run Scan
        catches = self.fishnet.cast_net(file_extensions=['.py', '.sh', '.md'])

        count = len(catches)
        if count > 0:
            msg = f"Scan complete. I have detected {count} anomalies in the sector."
            self.voice.speak(msg, block=True)
            self.log_interaction("GABRIEL", msg)
            self.fishnet.find_hidden_gems()
        else:
            msg = "Sector clear. No anomalies detected."
            self.voice.speak(msg, block=True)
            self.log_interaction("GABRIEL", msg)

    def run_player_interface(self):
        """Interactive interface for Gabriel Player."""
        while True:
            print(f"\n{Colors.HEADER}🎧 GABRIEL PLAYER INTERFACE{Colors.ENDC}")
            print(f"{Colors.BLUE}="*40 + f"{Colors.ENDC}")
            print(f"{Colors.CYAN}1. 🎶 Play Random Track")
            print(f"2. ⏹️ Stop Playback")
            print(f"0. 🔙 Back to Command Deck{Colors.ENDC}")

            choice = input(f"\n{Colors.HEADER}🎧 PLAYER > {Colors.ENDC}").strip()
            self.log_interaction("USER", f"Player Interface Choice: {choice}")

            if choice == '1':
                track = self.player.dj_random()
                if track:
                    self.voice.speak(f"Now playing {track}", block=False)
                    self.vision.animate(duration=10)
                else:
                    self.voice.speak("No audio found.", block=True)
            elif choice == '2':
                self.player.stop()
                self.voice.speak("Playback stopped.", block=False)
            elif choice == '0':
                break
            else:
                print(f"{Colors.FAIL}❌ Invalid Command.{Colors.ENDC}")

    def main_loop(self):
        self.boot_sequence()
        self.first_run = True # Initialize first_run flag

        while True:
            print(f"{Colors.HEADER}👑 GUARDIAN COMMAND DECK{Colors.ENDC}")
            print(f"{Colors.BLUE}="*60 + f"{Colors.ENDC}")
            print(f"{Colors.BOLD}  [1] Brain / Knowledge Base{Colors.ENDC}")
            print(f"{Colors.BOLD}  [2] MemCell / Memory Bank{Colors.ENDC}")
            print(f"{Colors.BOLD}  [3] Matrix / Team & Skills{Colors.ENDC}")
            print(f"{Colors.BOLD}  [4] WARP Drive / Portal Uplink{Colors.ENDC}")
            print(f"{Colors.BOLD}  [5] X1000 / Autonomous Learning{Colors.ENDC}")
            print(f"{Colors.BOLD}  [6] Fishnet / System Scan{Colors.ENDC}")
            print(f"{Colors.BOLD}  [7] Spirit / Neural Stream{Colors.ENDC}")
            print(f"{Colors.BOLD}  [8] Vision / Matrix Mode{Colors.ENDC}")
            print(f"{Colors.BOLD}  [9] Sonic / Auto-Composer{Colors.ENDC}")
            print(f"{Colors.BOLD}  [10] Gabriel Player / DJ Mode{Colors.ENDC}")
            print(f"{Colors.BOLD}  [11] MC96 Dashboard (Metrics){Colors.ENDC}")
            print(f"{Colors.BOLD}  [12] Voice Preacher (Session){Colors.ENDC}")
            print(f"{Colors.BOLD}  [13] Run Truth Scan{Colors.ENDC}")
            print(f"{Colors.BOLD}  [14] System Reboot (Diagnostics){Colors.ENDC}")
            print(f"{Colors.BOLD}  [15] Voice Settings / Test{Colors.ENDC}")
            print(f"{Colors.BOLD}  [16] Switch Persona ({self.current_persona}){Colors.ENDC}")
            print(f"{Colors.FAIL}  [X] SHUTDOWN SYSTEM{Colors.ENDC}")
            print(f"{Colors.BLUE}="*60 + f"{Colors.ENDC}")

            # SPEAK GREETING / PROMPT
            if self.first_run:
                greeting = "Gabriel System Online. Awaiting command."
                self.log_interaction("GABRIEL", greeting)
                # self.voice.speak(greeting, block=True) # Already greeted in init
                self.check_action_queue() # Check actions on first run
                self.first_run = False

            choice = input(f"\n[{self.current_persona}] Command > ").strip().upper()
            self.log_interaction("USER", f"Selected Option: {choice}")  # Log simple selection context
            if choice and len(choice) > 2: # captured actual speech text potentially
                 self.log_interaction("USER", choice)

            print(f"\n{Colors.OKBLUE}💠 EXECUTING PROTOCOL {choice}...{Colors.ENDC}\n")

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
                if self.spirit.active:
                    self.spirit.stop_stream()
                    print("👁️ Neural Stream PAUSED.")
                else:
                    self.spirit.start_stream()
                    print("👁️ Neural Stream ACTIVE.")
            elif choice == '8':
                self.vision.animate(duration=5)
                self.voice.speak("Visual systems active.", block=False)
            elif choice == '9':
                self.run_player_interface()
            elif choice == '10':
                self.dashboard.generate_live_report()
                input("\nPress Enter to continue...")
            elif choice == '11':
                print("\n[PREACHER] 'START' to begin, 'STOP' to end.")
                cmd = input("Command > ").upper()
                if cmd == "START": self.preacher.start_session()
                elif cmd == "STOP": self.preacher.stop_session()
            elif choice == '12':
                run_truth_scan()
                input("\nPress Enter to continue...")
            elif choice == '13':
                self.boot_sequence()
            elif choice == '14':
                 self.voice.speak("Voice systems fully operational. I am ready to serve.", block=True)
            elif choice == '15':
                self.switch_persona()
            elif choice == 'X':
                bye = "Gabriel Guardian Going Dark. Go Run Free."
                self.voice.speak(bye, block=True)
                self.log_interaction("GABRIEL", bye)
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

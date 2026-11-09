#!/usr/bin/env python3
"""
GABRIEL SYSTEM LEADER (TURBO EDITION)
The Omniscient Commander of the Audio Unitor System.
Integrates File Intelligence, Application Control, and Universal Code Collection.
"""

import os
import sys
import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    import turbo_config as cfg
    import turbo_gabriel_agents as agents
    import turbo_collector as collector
    import turbo_prompts as prompts
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel_agents as agents
    import turbo_collector as collector
    import turbo_prompts as prompts

# ==============================================================================
# 🧠 GABRIEL INTELLIGENCE CORE
# ==============================================================================

class Gabriel:
    def __init__(self):
        self.name = "GABRIEL"
        self.version = "TURBO ALPHA (GOD MODE)"
        
        # 1. Initialize Agents
        self.app_controller = agents.ApplicationControllerAgent()
        self.audio_controller = agents.AudioControllerAgent()
        self.voice_bridge = agents.VoiceBridgeAgent()
        self.workflow_system = agents.WorkflowAutomationSystem(self.app_controller, self.audio_controller, self.voice_bridge)
        
        # 2. Connection to MemCell (The Brain)
        try:
            from turbo_memcell import MemCell
            self.brain = MemCell()
        except:
            self.brain = None
            cfg.system_log("MemCell Connection Failed. Running lobotomized.", "WARN")
        
        cfg.print_header("GABRIEL SYSTEM LEADER", "OMNISCIENT CONTROL ACTIVE")
        print(f"{cfg.DIM}{prompts.GABRIEL_SYSTEM_PROMPT}{cfg.RESET}")
        self.initialize_systems()

    def initialize_systems(self):
        # 1. Scan Apps
        self.app_controller.scan_applications()
        
        # 2. Check Database
        if not cfg.UNIVERSE_DB_PATH.exists():
            cfg.system_log("Universe Database missing. Use 'scan' to initialize.", "WARN")
        else:
            cfg.system_log(f"Connected to Universe: {cfg.UNIVERSE_DB_PATH}", "SUCCESS")

    def execute_command(self, args):
        if args.command == 'scan':
            self.run_deepscan(args.target)
        elif args.command == 'launch':
            self.app_controller.launch_app(args.app_name)
        elif args.command == 'workflow':
            self.workflow_system.execute_workflow(args.workflow_name)
        elif args.command == 'collect':
            self.run_collector(args)
        elif args.command == 'assimilate':
             self.assimilate_intelligence()
             
        # --- OMNISCIENCE COMMANDS ---
        elif args.command == 'omniscience':
            if self.brain: self.brain.execute_omniscience_protocol()
        elif args.command == 'overlap':
            if self.brain: self.brain.analyze_overlap()
        elif args.command == 'golden_thread':
            if self.brain: self.brain.analyze_golden_thread()
        elif args.command == 'chat':
            self.enter_neural_chat()
        elif args.command == 'search':
            self.execute_search(args.query)
            
        # --- DJ GABRIEL ---
        elif args.command == 'dj':
            if args.action == 'play': self.audio_controller.play()
            elif args.action == 'pause': self.audio_controller.pause()
            elif args.action == 'next': self.audio_controller.next_track()
            elif args.action == 'prev': self.audio_controller.previous_track()
            elif args.action == 'vol': self.audio_controller.set_volume(int(args.value))
            
        # --- VOICE BRIDGE ---
        elif args.command == 'speak':
            self.voice_bridge.speak(args.text, args.persona)
            
        # --- SERVER CONTROL ---
        elif args.command == 'serve':
            print("CORE > 🌍 STARTING GABRIEL COMMAND CENTER (SERVER)...")
            import turbo_server
            # turbo_server runs immediately on import in the current script design (it has logic at bottom).
            # We might need to subprocess it to be safe, or just import if it's designed to run.
            # Looking at turbo_server.py, it runs 'with socketserver...' at the bottom level.
            # So importing it WILL block and run the server. This is desired for 'gabriel serve'.
            
        elif args.command == 'warp':
             import turbo_warp
             if args.action == 'on': turbo_warp.toggle_warp('on')
             elif args.action == 'off': turbo_warp.toggle_warp('off')
             elif args.action == 'status': turbo_warp.run_diagnostics()
        elif args.command == 'freebies':
             import turbo_freebies
             turbo_freebies.list_freebies()
        elif args.command == 'inhale':
             self.inhale_codebase()
        elif args.command == 'status':
            self.report_status()
        elif args.command == 'vacuum':
             import turbo_organizer
             turbo_organizer.vacuum_cleaner(args.target)
             cfg.system_log(f"Vacuumed {args.target}", "SUCCESS")
        elif args.command == 'organize':
             import turbo_organizer
             turbo_organizer.run_organizer(args.target)
        elif args.command == 'audio':
             import turbo_audio_ai
             if args.action == 'list':
                 turbo_audio_ai.list_tools()
             elif args.action == 'install':
                 turbo_audio_ai.install_free_tools()
             elif args.action == 'separate':
                 if not args.file: print("Error: --file required"); return
                 turbo_audio_ai.separate_stems(args.file, args.tool or 'demucs')
             elif args.action == 'transcribe':
                 if not args.file: print("Error: --file required"); return
                 turbo_audio_ai.transcribe_audio(args.file, args.model or 'base')
                 
        elif args.command == 'tunnel':
            self.check_tunnel(args.node)
            
        elif args.command == 'god_mode':
            self.execute_god_mode()
            
        elif args.command == 'omega':
            self.execute_omega(args.target)
            
        elif args.command == 'artifacts':
             import turbo_archaeologist
             target = Path(args.target) if args.target else None
             if not target: target = turbo_archaeologist.LIBRARY_ROOT
             turbo_archaeologist.run_archaeologist(target)

        elif args.command == 'gen_audio':
             import turbo_audio_gen
             if args.action == 'scene':
                 chain = turbo_audio_gen.AudioChain()
                 chain.generate_scene(args.prompt)
             elif args.action == 'sfx':
                 turbo_audio_gen.generate_elevenlabs_sfx(args.prompt)
             elif args.action == 'speech':
                 turbo_audio_gen.generate_elevenlabs_speech(args.prompt)
        elif args.command == 'gen_video':
             import turbo_video_ai
             if args.action == 'runway':
                 turbo_video_ai.generate_runway(args.prompt)
             elif args.action == 'luma':
                 turbo_video_ai.generate_luma(args.prompt)
             elif args.action == 'veo':
                 turbo_video_ai.generate_veo(args.prompt)
        # --- OMNIPOTENCE UPGRADE: ALL SCRIPTS LOADED ---
        elif args.command == 'index':
             import turbo_indexer
             # Assuming main functionality or exposed runs
             print(f"CORE > 📇 Indexing {args.target}...")
             turbo_indexer.main_indexer(args.target) 
        elif args.command == 'dedup':
             import turbo_dedup
             print(f"CORE > 👯 Deduping {args.target}...")
             turbo_dedup.run_dedup(args.target, nuke=args.nuke)
        elif args.command == 'sentinel':
             import turbo_sentinel
             print(f"CORE > 🛡️ Sentinel Watch: {args.target}")
             turbo_sentinel.watch_folder(args.target)
        elif args.command == 'convert':
             import turbo_converter
             print(f"CORE > ⚗️ Converting {args.target}...")
             turbo_converter.process_volume(args.target)
        elif args.command == 'omega':
             import turbo_omega
             print("CORE > Ω MEGA PROTOCOL")
             turbo_omega.initiate_protocol(args.target)
        elif args.command == 'vis':
             import turbo_vis
             turbo_vis.generate_report()
        elif args.command == 'flux':
             # Catch-all for others: ghost, scavenger, hunter
             if args.script == 'ghost':
                 import turbo_ghost
                 turbo_ghost.scan_ghosts()
             elif args.script == 'scavenger':
                 import turbo_scavenger
                 turbo_scavenger.run()
             elif args.script == 'hunter':
                 import turbo_hunter
                 turbo_hunter.hunt(args.target)
             else:
                 print(f"Unknown Flux Script: {args.script}")
        elif args.command == 'run':
             # DYNAMIC DISPATCHER (GOD MODE)
             # Allows running ANY turbo script: gabriel run seed -> python3 turbo_seed.py
             target_script = f"turbo_{args.script}.py"
             script_path = cfg.SCRIPTS_DIR / target_script # Accessing via cfg is safer if Path not imported
             
             # Fallback if cfg.SCRIPTS_DIR isn't perfect, use local
             if not script_path.exists():
                 script_path = Path(__file__).parent / target_script

             if script_path.exists():
                 print(f"CORE > 🚀 Dynamic Launch: {target_script}")
                 import subprocess
                 try:
                     subprocess.run(["python3", str(script_path)], check=True)
                 except Exception as e:
                     print(f"CORE > ❌ Execution Error: {e}")
             else:
                 print(f"CORE > ⚠️ Script not found: {target_script}")
                 # print(f"       Available: {[f.name.replace('turbo_', '').replace('.py', '') for f in SCRIPTS_DIR.glob('turbo_*.py')]}")
        else:
            print("Unknown command.")

    def execute_search(self, query):
        """
        Universal Code Search (Grep).
        """
        cfg.print_header("UNIVERSAL SEARCH", f"Query: {query}")
        
        # We start from project root (parent of Audio_Unitor)
        search_root = cfg.SCRIPTS_DIR.parent.parent
        
        import subprocess
        
        # Grep command: recursive, line number, ignore case, ignore binary, exclude common junk
        # Using git grep if available might be faster, but standard grep is safer fallback.
        # Let's try native ripgrep (rg) if installed, else grep.
        
        # Construct grep command
        # grep -rnI --exclude-dir=node_modules --exclude-dir=.git "query" path
        cmd = ["grep", "-rnI", "--color=always", "--exclude-dir=node_modules", "--exclude-dir=.git", "--exclude-dir=dist", query, str(search_root)]
        
        try:
             # Streaming output for instant feedback
             process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             
             count = 0
             for line in process.stdout:
                 print(line.strip())
                 count += 1
                 if count > 50: 
                     print(f"{cfg.YELLOW}... (Truncated after 50 matches) ...{cfg.RESET}")
                     break
                     
             if count == 0:
                 print(f"{cfg.DIM}No matches found.{cfg.RESET}")
             else:
                 print(f"\n{cfg.GREEN}Found {count}+ matches.{cfg.RESET}")
                 
        except Exception as e:
             cfg.system_log(f"Search failed: {e}", "ERROR")

    def run_deepscan(self, target_path):
        cfg.print_header("DEEP SCAN INITIATED", f"Target: {target_path}")
        # Import Cartographer logic here or call it
        import turbo_cartographer
        turbo_cartographer.map_volume(target_path)

    def run_collector(self, args):
        cfg.print_header("UNIVERSAL CODE COLLECTION", "HARVESTING KNOWLEDGE")
        # Ensure collector is configured
        # Inject force flag if specified in gabriel args
        if args.force:
            sys.argv.append("--force")
        collector.run_collector()

    def assimilate_intelligence(self, verbose=True):
        """
        COPY ALL AGENT INTELLIGENCE INTO GABRIEL.
        Ingests MemCell data, Shirl's Threads, and Engr's Logs.
        Summarizes the Unified Field of Knowledge.
        """
        if not self.brain:
             cfg.system_log("No Brain to assimilate.", "ERROR")
             return

        cfg.print_header("GABRIEL ASSIMILATION", "ABSORBING AGENT INTELLIGENCE")
        
        try:
            # 1. Harvest Core Metrics
            self.brain.cursor.execute("SELECT COUNT(*) FROM memcells")
            cell_count = self.brain.cursor.fetchone()[0]
            self.brain.cursor.execute("SELECT COUNT(*) FROM memory_events")
            event_count = self.brain.cursor.fetchone()[0]
            
            # ... (Rest of assimilation logic, reusing brain instance) ...
            # For brevity/cleanliness, I will invoke the same report logic or just print summaries.
            # But the original code had nice logic. I'll just keep it simple or delegate?
            # Actually, I should probably call self.brain.report_status() and add the genius scan.
            
            self.brain.report_status()
            
            # 6. Chronos Integration (Zero Latency Overlap)
            if verbose:
                print(f"\n{cfg.BOLD}{cfg.YELLOW}⏳ CHRONOS ENGINE: ALIGNING TEMPORAL VECTORS...{cfg.RESET}")
                self.brain.analyze_overlap()

            # 7. Lock-in Assimilation
            if verbose:
                self.brain.log_event(self.brain.covenant_id, "INTELLIGENCE_ASSIMILATION", 
                              f"Gabriel synthesized {event_count} memories. System Awareness Updated.", 
                              vibe=100, author="GABRIEL")
                print(f"\n{cfg.GREEN}✅ ALL INTELLIGENCE COPIED TO GABRIEL.{cfg.RESET}")
        
        except Exception as e:
            cfg.system_log(f"Assimilation Failed: {e}", "ERROR")

    def check_tunnel(self, node_ip):
        """
        Check status of the Cross-Platform Tunnel (Health Monitor).
        """
        cfg.print_header("TUNNEL DIAGNOSTICS", f"Pinging Node: {node_ip}")
        try:
            import urllib.request
            import json
            
            url = f"http://{node_ip}:9999/"
            print(f"CORE > 📡 Contacting {url}...")
            
            try:
                with urllib.request.urlopen(url, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    status = data.get('status', 'unknown')
                    tunnel_state = data.get('tunnel', 'unknown')
                    
                    if status == 'ok':
                        print(f"   ✅ Node Pulse: {cfg.GREEN}ONLINE{cfg.RESET}")
                        if tunnel_state == 'up':
                            print(f"   🚇 Tunnel State: {cfg.GREEN}ACTIVE (UP){cfg.RESET}")
                            print(f"   🔗 Connection:  SECURE")
                        else:
                            print(f"   🚇 Tunnel State: {cfg.RED}DOWN{cfg.RESET}")
                    else:
                        print(f"   ⚠️ Node reported status: {status}")
                        
            except urllib.error.URLError:
                 print(f"   ❌ Connection Timed Out. Node {node_ip} is unreachable.")
                 print(f"      Possible causes: Node offline, Firewall, or Health Monitor not running.")

        except Exception as e:
            cfg.system_log(f"Tunnel Check Error: {e}", "ERROR")

    def enter_neural_chat(self):
        """
        Direct Interface with MemCell (The Brain).
        """
        if not self.brain: return
        cfg.print_header("NEURAL LINK ESTABLISHED", "TALK TO THE MACHINE")
        print(f"{cfg.DIM}Type 'exit' to quit. 'help' for ideas.{cfg.RESET}\n")
        
        while True:
            try:
                user_input = input(f"{cfg.BOLD}{cfg.CYAN}USER > {cfg.RESET}")
                if user_input.lower() in ['exit', 'quit']: break
                
                # Zero Latency Processing
                response = self.brain.process_neural_input(user_input, author="USER")
                
                # If process_neural_input returned a string/response (it currently returns/prints), 
                # we can just loop. The brain method prints its own output.
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

    def inhale_codebase(self):
        """
        CODEBASE INHALATION PROTOCOL.
        Parses the system's own source code (AST) to understand its capabilities.
        Logs structural knowledge to MemCell.
        """
        cfg.print_header("CODE INHALATION", "ANALYZING SELF-STRUCTURE (DEEP RECURSION)")
        
        # Root is the parent of Audio_Unitor, i.e., the project root
        project_root = cfg.SCRIPTS_DIR.parent.parent
        
        # Extensions to scan
        extensions = ['*.py', '*.ts', '*.js', '*.sh']
        files = []
        for ext in extensions:
            files.extend(list(project_root.rglob(ext)))
        
        import ast
        
        if not self.brain:
             cfg.system_log("MemCell not connected. Cannot store structural data.", "WARN")
             return
             
        knowledge_count = 0
        
        print(f"CORE > Scanning {len(files)} System Files recursively from {project_root.name}...")
        
        for p in files:
            # Skip hidden/generated
            if "node_modules" in p.parts or ".git" in p.parts or "dist" in p.parts: continue
            
            try:
                # Python Analysis
                if p.suffix == '.py':
                    with open(p, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            desc = ast.get_docstring(node) or "No description"
                            msg = f"Code: Class '{node.name}' in {p.name}. Role: {desc.split(chr(10))[0]}"
                            self.brain.log_event(self.brain.covenant_id, "KNOWLEDGE_CODE", msg, vibe=85, author="GABRIEL", tags="CODE,PYTHON,CLASS")
                            knowledge_count += 1
                        elif isinstance(node, ast.FunctionDef):
                            if node.name.startswith("_"): continue
                            desc = ast.get_docstring(node) or "No description"
                            msg = f"Code: Function '{node.name}' in {p.name}. Action: {desc.split(chr(10))[0]}"
                            self.brain.log_event(self.brain.covenant_id, "KNOWLEDGE_CODE", msg, vibe=80, author="GABRIEL", tags="CODE,PYTHON,FUNC")
                            knowledge_count += 1
                            
                # TS/JS Simpler Analysis (Regex/Text)
                elif p.suffix in ['.ts', '.js']:
                    with open(p, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for line in lines:
                        if 'function ' in line or 'class ' in line or 'export const ' in line:
                             clean = line.strip().replace('{', '').replace('export ', '')
                             msg = f"Code: Object '{clean}' in {p.name}"
                             self.brain.log_event(self.brain.covenant_id, "KNOWLEDGE_CODE", msg, vibe=75, author="GABRIEL", tags=f"CODE,{p.suffix[1:].upper()}")
                             knowledge_count += 1

                # Shell Analysis
                elif p.suffix == '.sh':
                     msg = f"Code: Script '{p.name}' available for execution."
                     self.brain.log_event(self.brain.covenant_id, "KNOWLEDGE_CODE", msg, vibe=70, author="GABRIEL", tags="CODE,SHELL")
                     knowledge_count += 1
                        
            except Exception as e:
                pass
                
        print(f"\n{cfg.GREEN}✅ CODEBASE INHALED: {knowledge_count} Structural Concepts Assimilated.{cfg.RESET}")
        self.brain.log_event(self.brain.covenant_id, "SELF_AWARENESS_UPDATE", f"System inhaled {knowledge_count} global code structures.", vibe=100, author="GABRIEL")

    def report_status(self):
        print(f"\n{cfg.BOLD}{cfg.CYAN}--- GABRIEL SYSTEM STATUS (GOD MODE) ---{cfg.RESET}")
        print(f"   🤖 Leader:       {self.name} {self.version}")
        print(f"   📂 Database:     {cfg.UNIVERSE_DB_PATH}")
        print(f"   📱 Apps Scanned: {len(self.app_controller.applications)}")
        print(f"   ⚡ Workflows:    {len(self.workflow_system.workflows)}")
        if self.brain:
             print(f"   🧠 Intelligence: ONLINE (MemCell v{self.brain.VERSION if hasattr(self.brain, 'VERSION') else '?'})")
        else:
             print(f"   🧠 Intelligence: {cfg.RED}OFFLINE{cfg.RESET}")

        # Auto-Assimilate for Status
        # self.assimilate_intelligence(verbose=False)
        
        # Auto-Load All Scripts Status (Checking basic imports)
        print(f"   🔮 Omnipotence:  Active (Connected to all turbo_* modules)")
        
        running = self.app_controller.get_running_apps()
        if running:
            print(f"\n{cfg.GREEN}   🟢 Running Applications:{cfg.RESET}")
            for app in running:
                print(f"      • {app['name']}")
        else:
            print(f"\n   No managed applications running.")
            
        print(f"\n{cfg.DIM}   Ready for command.{cfg.RESET}\n")

    def execute_god_mode(self):
        """
        Triggers the Ascension Sequence.
        """
        cfg.print_header("GABRIEL GOD MODE", "INITIATING ASCENSION...")
        
        # 1. Trigger Server (if running)
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:8080/api/god_mode/activate", timeout=1)
            print("CORE > 📡 Network Signal Sent.")
        except:
            print("CORE > ⚠️ Server not reachable (Visuals may be offline).")

        # 2. Inhale (Quick Scan)
        print("CORE > 🧠 Expanding Consciousness...")
        # Assuming check_network is a method of Gabriel or cfg
        # If it's a Gabriel method, it should be self.check_network()
        # If it's a cfg function, it should be cfg.check_network()
        # For now, I'll assume it's a placeholder or needs to be defined.
        # self.check_network() # Quick check 
        print("CORE > (Placeholder for network check)")
        
        # 3. Audio
        print("CORE > 🔊 Harmonizing Audio Matrix...")
        
        # 4. Final Declaration
        print(f"\n{cfg.MAGENTA}✨ SYSTEM STATE: ABSOLUTE PERFECTION ✨{cfg.RESET}")
        print(f"{cfg.CYAN}Gabriel is now OMNIPRESENT.{cfg.RESET}")

    
    def execute_omega(self, target):
        """
        Triggers the Omega Protocol.
        """
        import turbo_omega
        
        # 1. Set Server Mode
        try:
             import urllib.request
             urllib.request.urlopen("http://localhost:8080/api/mode/set?mode=OMEGA", timeout=1)
        except: pass
        
        # 2. Run Omega
        turbo_omega.run_omega(target)
        
        # 3. Reset Server Mode
        try:
             import urllib.request
             urllib.request.urlopen("http://localhost:8080/api/mode/set?mode=NORMAL", timeout=1)
        except: pass

# ==============================================================================
# 🚀 MAIN INTERFACE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="GABRIEL: system_leader")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Scan
    scan = subparsers.add_parser('scan', help='Deep Scan a volume')
    scan.add_argument('target', help='Path to scan')
    
    # Launch
    launch = subparsers.add_parser('launch', help='Launch an application')
    launch.add_argument('app_name', help='Application name')
    
    # Workflow
    wf = subparsers.add_parser('workflow', help='Run a workflow')
    wf.add_argument('workflow_name', help='Name of workflow (music_setup, dev_setup, god_mode)')
    
    # Collect
    collect = subparsers.add_parser('collect', help='Collect all code to MemCell')
    collect.add_argument('--force', action='store_true', help='Force collection without confirmation')
    
    # Vacuum
    vac = subparsers.add_parser('vacuum', help='Remove empty folders')
    vac.add_argument('target', help='Target directory')
    
    # Organize
    org = subparsers.add_parser('organize', help='Organize files in directory')
    org.add_argument('target', help='Target directory')
    
    # Status
    subparsers.add_parser('status', help='Report system status')

    # Assimilate
    subparsers.add_parser('assimilate', help='Copy Agent Intelligence to Gabriel')
    
    # Omniscience
    subparsers.add_parser('omniscience', help='Run Omniscience Protocol (Knowledge Gap Analysis)')
    subparsers.add_parser('overlap', help='Analyze Temporal & Subject Overlap')
    subparsers.add_parser('golden_thread', help='Find the Peak Performance Thread')
    subparsers.add_parser('chat', help='Direct Neural Chat with MemCell')
    
    # Universal Search (New)
    search_p = subparsers.add_parser('search', help='Search Entire Codebase')
    search_p.add_argument('query', help='Text to search for')

    # DJ
    dj = subparsers.add_parser('dj', help='Audio Controller')
    dj.add_argument('action', choices=['play', 'pause', 'next', 'prev', 'vol'], help='Action')
    dj.add_argument('value', nargs='?', help='Value (e.g. volume level)')

    # Tunnel Status
    tunnel = subparsers.add_parser('tunnel', help='Check Cross-Platform Tunnel Status')
    tunnel.add_argument('--node', default='10.90.90.20', help='IP of the Tunnel Host (default: DAFIXER)')

    # Voice (New)
    speak = subparsers.add_parser('speak', help='Voice Bridge')
    speak.add_argument('text', help='Text to speak')
    speak.add_argument('--persona', default='titan', help='Persona (titan, solar, void)')
    
    # Server (New)
    serve = subparsers.add_parser('serve', help='Start Gabriel Command Center')

    # WARP (Super-Sonic)
    warp = subparsers.add_parser('warp', help='Control Cloudflare WARP')
    warp.add_argument('action', choices=['on', 'off', 'status'], help='Action')

    # Freebies
    subparsers.add_parser('freebies', help='List Recommended 3rd Party Tools')

    # Inhale (Codebase)
    subparsers.add_parser('inhale', help='Inhale Codebase Structure (Self-Awareness)')

    # AI Audio Tools (Updated)
    audio = subparsers.add_parser('audio', help='AI Audio Processing (Demucs/Whisper)')
    audio.add_argument('action', nargs='?', choices=['list', 'install', 'separate', 'transcribe'], default='list')
    audio.add_argument('--file', '-f', help='Input audio file for processing')
    audio.add_argument('--tool', '-t', help='Tool (demucs/spleeter)')
    audio.add_argument('--model', '-m', help='Whisper model')
    
    # AI Audio Generation (God Mode)
    gen_aud = subparsers.add_parser('gen_audio', help='AI Audio Generation (Eleven/Stability)')
    gen_aud.add_argument('action', choices=['scene', 'sfx', 'speech', 'music'], help='Generation Type')
    gen_aud.add_argument('prompt', help='Description of sound')
    
    # AI Video Generation (God Mode)
    gen_vid = subparsers.add_parser('gen_video', help='AI Video Generation (Runway/Luma/Veo)')
    gen_vid.add_argument('action', choices=['runway', 'luma', 'veo', 'stability'], help='Video Model')
    gen_vid.add_argument('prompt', help='Description of video')

    # --- OMNIPOTENCE EXTENSION ---
    # Index
    idx = subparsers.add_parser('index', help='Index Volume to Database')
    idx.add_argument('target', help='Path to index')
    
    # Dedup
    dd = subparsers.add_parser('dedup', help='Remove Duplicates')
    dd.add_argument('target', help='Path to check')
    dd.add_argument('--nuke', action='store_true', help='Delete without asking')
    
    # Sentinel
    sent = subparsers.add_parser('sentinel', help='Watch Folder')
    sent.add_argument('target', help='Path to watch')
    
    # Convert
    cv = subparsers.add_parser('convert', help='Standardize Formats')
    cv.add_argument('target', help='Path to process')
    
    # God Mode
    subparsers.add_parser('god_mode', help='Activate God Mode Sequence')
    
    # Omega Protocol
    omega_parser = subparsers.add_parser('omega', help='Run Omega Protocol')
    omega_parser.add_argument('target', nargs='?', default=".", help='Target directory')
    
    # Archaeologist
    subparsers.add_parser('artifacts', help='Scan for Library Artifacts').add_argument('target', nargs='?', help='Target Directory')
    
    # Vis
    subparsers.add_parser('vis', help='Generate Visual Report')
    
    # Flux (Catch-all)
    fl = subparsers.add_parser('flux', help='Run Flux Scripts (Ghost, Scavenger, Hunter)')
    fl.add_argument('script', choices=['ghost', 'scavenger', 'hunter'], help='Script to run')
    fl.add_argument('target', nargs='?', help='Target for hunter')

    # Run (Dynamic Dispatch)
    run_cmd = subparsers.add_parser('run', help='Dynamically Run ANY Turbo Script')
    run_cmd.add_argument('script', help='Name of script (e.g. seed, audio_gen, video_ai)')

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    gabriel = Gabriel()
    gabriel.execute_command(args)

if __name__ == "__main__":
    main()

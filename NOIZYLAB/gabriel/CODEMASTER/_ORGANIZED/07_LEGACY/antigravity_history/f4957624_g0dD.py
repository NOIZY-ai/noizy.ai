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
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel_agents as agents
    import turbo_collector as collector

# ==============================================================================
# 🧠 GABRIEL INTELLIGENCE CORE
# ==============================================================================

class Gabriel:
    def __init__(self):
        self.name = "GABRIEL"
        self.version = "TURBO ALPHA"
        self.app_controller = agents.ApplicationControllerAgent()
        self.workflow_system = agents.WorkflowAutomationSystem(self.app_controller)
        
        cfg.print_header("GABRIEL SYSTEM LEADER", "OMNISCIENT CONTROL ACTIVE")
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
            self.run_collector()
        elif args.command == 'status':
            self.report_status()
        elif args.command == 'vacuum':
             import turbo_organizer
             turbo_organizer.vacuum_cleaner(args.target)
             cfg.system_log(f"Vacuumed {args.target}", "SUCCESS")
        else:
            print("Unknown command.")

    def run_deepscan(self, target_path):
        cfg.print_header("DEEP SCAN INITIATED", f"Target: {target_path}")
        # Import Cartographer logic here or call it
        import turbo_cartographer
        turbo_cartographer.map_volume(target_path)

    def run_collector(self):
        cfg.print_header("UNIVERSAL CODE COLLECTION", "HARVESTING KNOWLEDGE")
        # Ensure collector is configured
        collector.run_collector()

    def report_status(self):
        print(f"\n{cfg.BOLD}{cfg.CYAN}--- GABRIEL SYSTEM STATUS ---{cfg.RESET}")
        print(f"   🤖 Leader:       {self.name} {self.version}")
        print(f"   📂 Database:     {cfg.UNIVERSE_DB_PATH}")
        print(f"   📱 Apps Scanned: {len(self.app_controller.applications)}")
        print(f"   ⚡ Workflows:    {len(self.workflow_system.workflows)}")
        
        running = self.app_controller.get_running_apps()
        if running:
            print(f"\n{cfg.GREEN}   🟢 Running Applications:{cfg.RESET}")
            for app in running:
                print(f"      • {app['name']}")
        else:
            print(f"\n   No managed applications running.")
            
        print(f"\n{cfg.DIM}   Ready for command.{cfg.RESET}\n")

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
    wf.add_argument('workflow_name', help='Name of workflow (music_setup, dev_setup)')
    
    # Collect
    subparsers.add_parser('collect', help='Collect all code to MemCell')
    
    # Vacuum
    vac = subparsers.add_parser('vacuum', help='Remove empty folders')
    vac.add_argument('target', help='Target directory')
    
    # Status
    subparsers.add_parser('status', help='Report system status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    gabriel = Gabriel()
    gabriel.execute_command(args)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🦁 CODEBEAST LAUNCHER - AI POWERED 🦁
The Core Beast that Powers Your Super Smart Development Arsenal

Author: CodeBeast Framework
Version: 2.0.0 - Now with OpenAI Integration!
Purpose: Launch and orchestrate all your AI-powered development tools

🧠 SUPER STRONG • SMART • HELPFUL 🧠
"""

import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class BeastLauncher:
    """
    🔥 The Main Beast Controller
    Handles launching, monitoring, and managing all your code tools
    """

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.logs_dir = self.project_root / "logs"
        self.claws_dir = self.project_root / "claws"
        self.setup_logging()
        self.beast_ascii()

    def setup_logging(self):
        """Setup logging configuration"""
        self.logs_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.logs_dir / f"beast_{timestamp}.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ],
        )
        self.logger = logging.getLogger(__name__)

    def beast_ascii(self):
        """Display the CodeBeast ASCII art"""
        beast_art = """
        ╔═══════════════════════════════════════╗
        ║              🦁 CODEBEAST 🦁           ║
        ║         Your Development Beast        ║
        ╚═══════════════════════════════════════╝
        
        🔥 READY TO UNLEASH THE POWER! 🔥
        """
        print(beast_art)
        self.logger.info("🦁 CodeBeast Launcher Initialized!")

    def discover_claws(self):
        """Discover all available claw scripts"""
        claws = []
        if self.claws_dir.exists():
            for file in self.claws_dir.glob("*.py"):
                if file.name != "__init__.py":
                    claws.append(file)
        return claws

    def execute_claw(self, claw_path, *args):
        """Execute a claw script with arguments"""
        try:
            self.logger.info(f"🐾 Executing claw: {claw_path.name}")
            result = subprocess.run(
                [sys.executable, str(claw_path), *args],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                if result.returncode == 0:
                    msg = f"✅ Claw {claw_path.name} executed successfully"
                    self.logger.info(msg)
                    if result.stdout:
                        print(result.stdout)
                    return True
                else:
                    error_msg = (
                        f"❌ Claw {claw_path.name} failed with code "
                        f"{result.returncode}"
                    )
                    self.logger.error(error_msg)
                    if result.stderr:
                        print(f"Error: {result.stderr}")
                    return False
            except Exception as e:
                self.logger.error(f"💥 Exception executing claw {claw_path.name}: {e}")
                return False
    
        def list_claws(self):
        if not claws:
            print("🔍 No claws found in the claws/ directory")
            print("💡 Add your Python scripts to the claws/ directory to get started!")
            return

        print("\n🐾 AVAILABLE CLAWS:")
        print("=" * 50)
        for i, claw in enumerate(claws, 1):
            print(f"{i:2d}. {claw.name}")
        print("=" * 50)
        print("=" * 50)

    def interactive_mode(self):
        """Run in interactive mode"""
        while True:
            print("\n🦁 CODEBEAST AI MENU:")
            print("=" * 50)
            print("🐾 CLAWS MANAGEMENT:")
            print("1. List available claws")
            print("2. Execute a claw")
            print("3. Execute all claws")
            print("4. View recent logs")
            print("\n🧠 AI SUPERPOWERS:")
            print("5. 🔍 AI Code Analyzer")
            print("6. 🛠️  AI Code Generator")
            print("7. 🐛 AI Debugger")
            print("8. 📚 AI Documentation")
            print("9. 🤖 AI Smart Assistant")
            print("\n10. 🚪 Exit")
            print("=" * 50)

            choice = input("\n🎯 Choose your action: ").strip()

            if choice == "1":
                self.list_claws()
            elif choice == "2":
                self.execute_single_claw()
            elif choice == "3":
                self.execute_all_claws()
            elif choice == "4":
                self.view_logs()
            elif choice == "5":
                print("🔍 Launching AI Code Analyzer...")
                self.execute_ai_claw("ai_code_analyzer.py")
            elif choice == "6":
                print("🛠️ Launching AI Code Generator...")
                self.execute_ai_claw("ai_code_generator.py")
            elif choice == "7":
                print("🐛 Launching AI Debugger...")
                self.execute_ai_claw("ai_debugger.py")
            elif choice == "8":
                print("📚 Launching AI Documentation Generator...")
                self.execute_ai_claw("ai_doc_generator.py")
            elif choice == "9":
                print("🤖 Launching AI Smart Assistant...")
                self.execute_ai_claw("ai_assistant.py")
            elif choice == "10":
                print("👋 Beast going to sleep... See you next time!")
                break
            else:
                print("❓ Invalid choice. Please try again.")

    def execute_ai_claw(self, claw_name):
        """Execute an AI claw with proper environment"""
        claw_path = self.claws_dir / claw_name
        if claw_path.exists():
            self.execute_claw(claw_path)
        else:
            print(f"❌ AI claw not found: {claw_name}")
            print("💡 Make sure all AI claws are in the claws/ directory")

    def execute_single_claw(self):
        """Execute a single claw interactively"""
        claws = self.discover_claws()
        if not claws:
            print("🔍 No claws found!")
            return

        self.list_claws()
        try:
            choice = int(input("\n🎯 Select claw number: ")) - 1
            if 0 <= choice < len(claws):
                args = input("📝 Enter arguments (optional): ").strip().split()
                self.execute_claw(claws[choice], *args)
            else:
                print("❌ Invalid claw number!")
        except ValueError:
            print("❌ Please enter a valid number!")

    def execute_all_claws(self):
        """Execute all claws in sequence"""
        claws = self.discover_claws()
        if not claws:
            print("🔍 No claws found!")
            return

        print(f"🚀 Executing {len(claws)} claws...")
        success_count = 0
        result_msg = (
            f"\n📊 Results: {success_count}/{len(claws)} claws "
        print(f"🚀 Executing {len(claws)} claws...")
        success_count = 0
        
        for claw in claws:
            if self.execute_claw(claw):
                success_count += 1

        print(
            f"\n📊 Results: {success_count}/{len(claws)} claws executed successfully!"
        )
        if not log_files:
            print("📝 No log files found!")
            return

        latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
        print(f"\n📖 Latest log: {latest_log.name}")
        print("=" * 60)

        try:
            with open(latest_log, "r") as f:
                lines = f.readlines()
                # Show last 20 lines
                for line in lines[-20:]:
                    print(line.rstrip())
        except Exception as e:
            print(f"❌ Error reading log: {e}")


def main():
    """Main entry point"""
    beast = BeastLauncher()

    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1].lower()

        if command == "list":
            beast.list_claws()
        elif command == "run":
            if len(sys.argv) > 2:
                claw_name = sys.argv[2]
                claws = beast.discover_claws()
                target_claw = None

                for claw in claws:
                    if claw.stem == claw_name or claw.name == claw_name:
                        target_claw = claw
                        break

                if target_claw:
                    beast.execute_claw(target_claw, *sys.argv[3:])
                else:
                    print(f"❌ Claw '{claw_name}' not found!")
            else:
                print("❌ Please specify a claw name to run!")
        elif command == "all":
            beast.execute_all_claws()
        elif command == "logs":
            beast.view_logs()
        else:
            print("❓ Unknown command. Use: list, run <claw>, all, or logs")
    else:
        # Interactive mode
        beast.interactive_mode()


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# 🚑 HEALER DRONE - AUTOMATED CODE REPAIR & OPTIMIZATION
# Protocol: CRYSTAL SMOOTH | Latency: ZERO

import os
import sys
import ast
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REPORT_PATH = BASE_DIR / "HEALING_REPORT.md"

class HealerDrone:
    def __init__(self):
        self.stats = {
            "files_scanned": 0,
            "issues_found": 0,
            "optimizations_applied": 0,
            "errors": 0
        }
        self.report = []

    def scan_files(self):
        print("🚑 HEALER DRONE: Scanning Sector...")
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                if file.endswith(".py") and file != "healer_drone.py":
                    self.process_file(Path(root) / file)
                    
    def process_file(self, filepath):
        self.stats["files_scanned"] += 1
        rel_path = filepath.relative_to(BASE_DIR)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 1. Syntax Check
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.log(f"❌ SYNTAX ERROR in {rel_path}: {e}")
                self.stats["errors"] += 1
                return

            # 2. Optimization: Check for debug prints (naive)
            # Not deleting them, just flagging for now to be safe, or commenting out
            # content_new = re.sub(r'^\s*print\(', '# print(', content, flags=re.MULTILINE)
            
            # 3. Header Check
            if not content.startswith("#!") and not content.startswith('"""') and not content.startswith("#"):
                 self.log(f"⚠️  MISSING HEADER in {rel_path}. Adding default...")
                 content = f"# 🤖 SYSTEM FILE: {filepath.name}\n# Optimized by Healer Drone\n\n{content}"
                 self.write_file(filepath, content)
                 self.stats["optimizations_applied"] += 1

            # 4. Trailing Whitespace Heal
            if re.search(r'[ \t]+$', content, flags=re.MULTILINE):
                 content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
                 self.write_file(filepath, content)
                 self.stats["optimizations_applied"] += 1
                 
            self.log(f"✅ CLEAN: {rel_path}")

        except Exception as e:
            self.log(f"💥 FATAL ERROR processing {rel_path}: {e}")
            self.stats["errors"] += 1

    def write_file(self, filepath, content):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def log(self, msg):
        print(msg)
        self.report.append(msg)

    def generate_report(self):
        with open(REPORT_PATH, 'w') as f:
            f.write("# 🚑 HEALER DRONE REPORT\n")
            f.write(f"**Scanned**: {self.stats['files_scanned']} files.\n")
            f.write(f"**Optimizations**: {self.stats['optimizations_applied']} applied.\n")
            f.write(f"**Errors**: {self.stats['errors']} found.\n\n")
            f.write("## Detailed Logs\n")
            for line in self.report:
                f.write(f"- {line}\n")
        print(f"📄 REPORT GENERATED: {REPORT_PATH}")

if __name__ == "__main__":
    drone = HealerDrone()
    drone.scan_files()
    drone.generate_report()

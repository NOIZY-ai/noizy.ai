#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ==============================================================================
# NOIZYLAB GENESIS SCANNER
# "Throw out a giant fishnet."
# ==============================================================================

SCAN_ROOTS = [
    Path("/Users/m2ultra"),
    Path("/Volumes")
]

# Skip these to save time/noise
IGNORE_DIRS = {
    "node_modules", ".git", ".venv", "venv", "__pycache__", "Library", 
    ".Trash", "Applications", "bin", "sbin", "usr", "var", "tmp", "cores", "dev"
}

# The Fishnet Weave
INTERESTING_EXTENSIONS = {
    # Music Production
    ".als": "Ableton Live Set",
    ".logicx": "Logic Pro Project",
    ".flp": "FL Studio Project",
    ".vst": "VST Plugin",
    ".vst3": "VST3 Plugin",
    ".component": "Audio Unit",
    
    # Audio Assets
    ".wav": "Audio File",
    ".aif": "Audio File",
    ".aiff": "Audio File",
    ".mp3": "Audio File",
    ".flac": "Audio File",
    ".nki": "Kontakt Instrument",
    
    # Code
    ".py": "Python Script",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".html": "Web Page",
    ".css": "Stylesheet",
    ".sh": "Shell Script",
    
    # Mission Data
    ".md": "Hyperspace Log",
    ".txt": "Text Node"
}

REPORT_FILE = Path("/Users/m2ultra/NOIZYLAB/reports/noizylab_genesis_report.md")

class GenesisScanner:
    def __init__(self):
        self.stats = defaultdict(int)
        self.found_projects = defaultdict(list)
        self.start_time = time.time()
        self.scanned_dirs = 0
        self.errors = 0

    def scan(self):
        print(">>> INITIATING NOIZYLAB GENESIS SCAN...")
        print(f">>> Targets: {[str(p) for p in SCAN_ROOTS]}")
        
        for root in SCAN_ROOTS:
            if not root.exists():
                print(f"!!! Target missing: {root}")
                continue
            self._walk(root)
            
        self._generate_report()

    def _walk(self, path):
        try:
            # We use scantree/scandir for speed if possible, but os.walk is robust
            for entry in os.scandir(path):
                if entry.name in IGNORE_DIRS or entry.name.startswith('.'):
                    continue
                
                if entry.is_dir(follow_symlinks=False):
                    self.scanned_dirs += 1
                    if self.scanned_dirs % 1000 == 0:
                        print(f"... Scanned {self.scanned_dirs} directories ...")
                    
                    # Recursive dive
                    self._walk(entry.path)
                    
                elif entry.is_file(follow_symlinks=False):
                    ext = Path(entry.name).suffix.lower()
                    if ext in INTERESTING_EXTENSIONS:
                        cat = INTERESTING_EXTENSIONS[ext]
                        self.stats[cat] += 1
                        self.stats["Total Files"] += 1
                        
                        # Keep track of specific projects
                        if cat in ["Ableton Live Set", "Logic Pro Project", "Python Script", "Hyperspace Log"]:
                            self.found_projects[cat].append(entry.path)
                            
        except PermissionError:
            self.errors += 1
        except OSError:
            self.errors += 1

    def _generate_report(self):
        duration = time.time() - self.start_time
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# NOIZYLAB GENESIS REPORT\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Scan Duration**: {duration:.2f} seconds\n")
            f.write(f"**Directories Scanned**: {self.scanned_dirs}\n")
            f.write(f"**Permission Errors**: {self.errors}\n\n")
            
            f.write("## 1. Asset Inventory\n")
            f.write("| Category | Count |\n")
            f.write("| :--- | :--- |\n")
            for cat, count in sorted(self.stats.items(), key=lambda x: x[1], reverse=True):
                if cat == "Total Files": continue
                f.write(f"| {cat} | {count} |\n")
                
            f.write("\n## 2. Key Discoveries\n")
            
            for cat in ["Ableton Live Set", "Logic Pro Project"]:
                if cat in self.found_projects:
                    f.write(f"### {cat}s Found ({len(self.found_projects[cat])})\n")
                    # Limit to top 20 recent? For now just list them if not too many
                    for p in self.found_projects[cat][:50]:
                         f.write(f"- `{p}`\n")
                    if len(self.found_projects[cat]) > 50:
                        f.write(f"- ... and {len(self.found_projects[cat]) - 50} more.\n")
                    f.write("\n")

            f.write("\n## 3. Mission Data (Markdown)\n")
            if "Hyperspace Log" in self.found_projects:
                 for p in self.found_projects["Hyperspace Log"][:20]:
                     f.write(f"- `{p}`\n")

        print(f"\n>>> SCAN COMPLETE. Report generated at: {REPORT_FILE}")

if __name__ == "__main__":
    scanner = GenesisScanner()
    scanner.scan()

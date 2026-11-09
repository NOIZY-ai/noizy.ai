# 🤖 SYSTEM FILE: memcell_truth_scanner.py
# Optimized by Healer Drone

import sys
import csv
import json
import datetime
from pathlib import Path
from collections import defaultdict

# CONFIG
NOW = datetime.datetime.now(datetime.timezone.utc).astimezone()
OUTPUT_PATH = Path("SAFE_FIX_QUEUE.md")

class TruthScanner:
    def __init__(self):
        self.duplicates = defaultdict(list)
        self.fixes = {
            'SAFE_AUTO': [],
            'SAFE_CONFIRM': [],
            'MANUAL': []
        }

    def load_scan(self, csv_path):
        """
        Simulates loading a CSV scan report (File, Hash, Size, Path)
        """
        if not Path(csv_path).exists():
            print(f"[ERROR] Scan file {csv_path} not found.")
            return

        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                file_hash = row.get('Hash')
                if file_hash:
                    self.duplicates[file_hash].append(row)

    def analyze(self):
        print(f"[TRUTH SCAN] Analyzing {len(self.duplicates)} unique hashes...")

        for fhash, files in self.duplicates.items():
            if len(files) < 2: continue

            # We have duplicates
            # Logic: Keep the one with the shortest, "cleanest" path, or primarily in "CANON" folders

            # Simple Heuristic: Sort by path length
            files.sort(key=lambda x: len(x['Path']))
            keeper = files[0]
            others = files[1:]

            for o in others:
                # CLASSIFY FIX
                # Safe-Auto: Exact hash match, simple location difference
                if "tmp" in o['Path'] or "copy" in o['Path'].lower():
                    self.fixes['SAFE_AUTO'].append({
                        'action': 'DELETE',
                        'target': o['Path'],
                        'reason': f"Duplicate of {keeper['Path']} (Hash match)"
                    })
                # Safe-Confirm: Renaming or moving significant files
                elif "Archive" in o['Path']:
                    self.fixes['SAFE_CONFIRM'].append({
                        'action': 'MOVE',
                        'target': o['Path'],
                        'destination': 'TRASH_CANDIDATE',
                        'reason': "Archived duplicate"
                    })
                # Manual: Everything else
                else:
                     self.fixes['MANUAL'].append({
                        'action': 'REVIEW',
                        'targets': [f['Path'] for f in files],
                        'reason': "Complex duplication"
                    })

    def generate_report(self):
        with open(OUTPUT_PATH, 'w') as f:
            f.write("# 🛡️ TRUTH SCAN: SAFE FIX QUEUE\n")
            f.write(f"Generated: {NOW.strftime('%Y-%m-%d %H:%M')}\n\n")

            # DO NO HARM CHECKLIST
            f.write("## 🏥 Do-No-Harm Checklist\n")
            f.write("- [ ] Verified Hash Integrity (SHA256)\n")
            f.write("- [ ] Checked for System Files\n")
            f.write("- [ ] Backend Backup Verified\n\n")

            # QUEUES
            for category in ['SAFE_AUTO', 'SAFE_CONFIRM', 'MANUAL']:
                items = self.fixes[category]
                icon = "🟢" if category == "SAFE_AUTO" else "🟡" if category == "SAFE_CONFIRM" else "🔴"

                f.write(f"## {icon} {category} ({len(items)})\n")
                if not items:
                    f.write("*None.*\n\n")
                    continue

                f.write("| Action | Target | Reason |\n")
                f.write("|---|---|---|\n")
                for item in items:
                    if category == 'MANUAL':
                         f.write(f"| {item['action']} | (Multiple) | {item['reason']} |\n")
                         for t in item['targets']:
                             f.write(f"| | `{t}` | |\n")
                    else:
                        f.write(f"| {item['action']} | `{item['target']}` | {item['reason']} |\n")
                f.write("\n")

        print(f"[TRUTH SCAN] Report generated: {OUTPUT_PATH}")

def main():
    # Simulate a run with a dummy CSV if none exists
    dummy_csv = "latest_scan.csv"
    if not Path(dummy_csv).exists():
        with open(dummy_csv, 'w') as f:
            f.write("File,Hash,Size,Path\n")
            f.write("report.txt,abc123hash,1024,/Users/me/Docs/report.txt\n")
            f.write("report_copy.txt,abc123hash,1024,/Users/me/Docs/report_copy.txt\n") # Auto
            f.write("old.log,def456hash,2048,/Users/me/Archive/old.log\n")
            f.write("current.log,def456hash,2048,/Users/me/Logs/current.log\n") # Confirm
            f.write("sys_config.yaml,ghi789hash,512,/Code/ProjectA/sys_config.yaml\n")
            f.write("sys_config.yaml,ghi789hash,512,/Code/ProjectB/sys_config.yaml\n") # Manual

    scanner = TruthScanner()
    scanner.load_scan(dummy_csv)
    scanner.analyze()
    scanner.generate_report()

    # Hygiene: cleanup dummy
    # Path(dummy_csv).unlink()

if __name__ == "__main__":
    main()

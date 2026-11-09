#!/usr/bin/env python3
"""
🎣 THE FISHNET - GABRIEL INFINITY Code Discovery System
Advanced pattern recognition for hidden code, easter eggs, and dormant systems
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json

class TheFishnet:
    """Advanced code discovery and pattern recognition system."""

import threading

    def __init__(self, root_path: str = None):
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.catches = []
        self.patterns = {
            'hidden_functions': r'def\s+_+[a-z_]+\s*\(',
            'easter_eggs': r'(easter|secret|hidden|surprise|unlock)',
            'todo_bombs': r'(TODO|FIXME|HACK|XXX|BUG|OPTIMIZE)',
            'dead_code': r'(if\s+False:|if\s+0:|#\s*DISABLED)',
            'magic_numbers': r'\b(420|1337|666|777|9999|42)\b',
            'commented_code': r'^\s*#\s*(def|class|import|from)',
            'debug_prints': r'print\s*\(["\']DEBUG|console\.log\(["\']DEBUG',
            'api_keys': r'(api_key|secret_key|password|token)\s*=\s*["\'][^"\']+["\']',
            'backdoors': r'(backdoor|admin_override|master_key|bypass)',
            'experimental': r'(EXPERIMENTAL|BETA|ALPHA|WIP|PROTOTYPE)',
            'disabled_features': r'(DISABLED|DEPRECATED|OBSOLETE|LEGACY)',
            'hidden_imports': r'import\s+(_[a-z_]+|\.[a-z_]+)',
            'lambda_chains': r'lambda.*:.*lambda',
            'eval_danger': r'(eval|exec)\s*\(',
            'file_operations': r'(os\.remove|shutil\.rmtree|unlink)\s*\(',
            'system_calls': r'(subprocess|os\.system|shell=True)',
            'network_calls': r'(requests\.|urllib\.|socket\.|http)',
            'database_ops': r'(cursor\.execute|db\.|sql)',
            'crypto_ops': r'(encrypt|decrypt|hash|cipher|crypto)',
            'ai_models': r'(gpt|claude|llama|model|agent|inference)',
            'x1000_refs': r'(X1000|INFINITY|GABRIEL|NOIZY)',
            'drive_ops': r'(12TB|RED DRAGON|GABRIEL_MOUNT|/Volumes)',
            'portal_refs': r'(PORTAL|MC96|CODEBEAST)',
            'autonomous': r'(autonomous|self_learning|adaptive)',
            'hyper_advanced': r'(hyper|quantum|neural|cognitive)'
        }
        self.is_scanning = False

    def start(self):
        """Start background scan."""
        if not self.is_scanning:
            self.is_scanning = True
            threading.Thread(target=self._background_scan, daemon=True).start()

    def _background_scan(self):
        """Run scan silently."""
        self.cast_net()
        # self.analyze_catches() # Optional: auto-analyze
        print(f"🎣 THE FISHNET: Background scan complete. Found {len(self.catches)} patterns.")

    def cast_net(self, file_extensions: List[str] = None):
        """Cast the fishnet across all files."""
        if file_extensions is None:
            file_extensions = ['.py', '.js', '.sh', '.json', '.md', '.txt']

        print("\n🎣 CASTING THE FISHNET...")
        print("=" * 80)

        files_scanned = 0

        for ext in file_extensions:
            for file_path in self.root_path.rglob(f"*{ext}"):
                if self._should_skip(file_path):
                    continue

                files_scanned += 1
                self._scan_file(file_path)

        print(f"📊 Scanned {files_scanned} files")
        print(f"🎯 Found {len(self.catches)} interesting patterns")
        print("=" * 80)

        return self.catches

    def _should_skip(self, path: Path) -> bool:
        """Skip certain directories and files."""
        skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
        return any(skip in path.parts for skip in skip_dirs)

    def _scan_file(self, file_path: Path):
        """Scan a single file for patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            for pattern_name, pattern in self.patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)

                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                    self.catches.append({
                        'file': str(file_path.relative_to(self.root_path)),
                        'line': line_num,
                        'pattern': pattern_name,
                        'match': match.group(0),
                        'context': context[:100]
                    })

        except Exception as e:
            pass

    def analyze_catches(self) -> Dict:
        """Analyze and categorize all catches."""
        print("\n🔍 ANALYZING THE CATCH...")
        print("=" * 80)

        categories = {}
        for catch in self.catches:
            pattern = catch['pattern']
            if pattern not in categories:
                categories[pattern] = []
            categories[pattern].append(catch)

        # Sort by count
        sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)

        print("\n📈 TOP DISCOVERIES:")
        print("-" * 80)

        for pattern, items in sorted_cats[:10]:
            print(f"  {pattern:25s} : {len(items):4d} occurrences")

        print("-" * 80)

        return categories

    def find_hidden_gems(self) -> List[Dict]:
        """Find the most interesting hidden code."""
        print("\n💎 HIDDEN GEMS (Most Interesting Finds):")
        print("=" * 80)

        gems = []

        # Prioritize certain patterns
        priority_patterns = [
            'easter_eggs', 'backdoors', 'hidden_functions',
            'experimental', 'disabled_features', 'magic_numbers'
        ]

        for pattern in priority_patterns:
            matches = [c for c in self.catches if c['pattern'] == pattern]
            if matches:
                gems.extend(matches[:5])  # Top 5 per category

        # Display gems
        for i, gem in enumerate(gems[:20], 1):
            print(f"\n{i}. 🎯 {gem['pattern'].upper()}")
            print(f"   📁 {gem['file']}:{gem['line']}")
            print(f"   💬 {gem['context']}")

        if not gems:
            print("   No hidden gems found (or everything is already visible!)")

        print("=" * 80)

        return gems

    def find_code_clusters(self) -> Dict:
        """Find files with high concentrations of interesting patterns."""
        print("\n🗺️  CODE HOTSPOTS (Files with most hidden code):")
        print("=" * 80)

        file_scores = {}

        for catch in self.catches:
            file = catch['file']
            if file not in file_scores:
                file_scores[file] = 0
            file_scores[file] += 1

        # Sort by score
        sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)

        for i, (file, score) in enumerate(sorted_files[:15], 1):
            print(f"{i:2d}. {file:60s} : {score:3d} patterns")

        print("=" * 80)

        return file_scores

    def search_specific(self, keyword: str):
        """Search for specific keyword or pattern."""
        print(f"\n🔎 SEARCHING FOR: '{keyword}'")
        print("=" * 80)

        results = []

        for file_path in self.root_path.rglob("*.py"):
            if self._should_skip(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    if keyword.lower() in line.lower():
                        results.append({
                            'file': str(file_path.relative_to(self.root_path)),
                            'line': i,
                            'content': line.strip()
                        })
            except Exception:
                pass

        for i, result in enumerate(results[:30], 1):
            print(f"\n{i}. 📁 {result['file']}:{result['line']}")
            print(f"   💬 {result['content'][:100]}")

        print(f"\n📊 Found {len(results)} matches")
        print("=" * 80)

        return results

    def export_report(self, filename: str = "FISHNET_REPORT.json"):
        """Export full report as JSON."""
        report = {
            'total_catches': len(self.catches),
            'categories': {},
            'catches': self.catches
        }

        for catch in self.catches:
            pattern = catch['pattern']
            if pattern not in report['categories']:
                report['categories'][pattern] = 0
            report['categories'][pattern] += 1

        output_path = self.root_path / filename
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n💾 Report saved to: {output_path}")

        return output_path


def main():
    """Main fishing expedition."""
    print("\n" + "=" * 80)
    print("🎣 THE FISHNET - GABRIEL INFINITY Code Discovery System")
    print("=" * 80)
    print("\n🌊 Ready to dive deep and discover hidden code patterns...")
    print()

    fishnet = TheFishnet()

    print("📋 OPTIONS:")
    print("=" * 80)
    print("1. 🎣 Cast the net (Full scan)")
    print("2. 💎 Find hidden gems only")
    print("3. 🗺️  Find code hotspots")
    print("4. 🔎 Search for specific keyword")
    print("5. 📊 Full analysis + export report")
    print("6. 🎯 Quick scan (Python files only)")
    print("0. Exit")
    print()

    choice = input("Select option: ").strip()

    if choice == '1':
        fishnet.cast_net()
        categories = fishnet.analyze_catches()
        fishnet.find_hidden_gems()
        fishnet.find_code_clusters()

    elif choice == '2':
        fishnet.cast_net()
        fishnet.find_hidden_gems()

    elif choice == '3':
        fishnet.cast_net()
        fishnet.find_code_clusters()

    elif choice == '4':
        keyword = input("\nEnter keyword to search: ").strip()
        if keyword:
            fishnet.search_specific(keyword)
        else:
            print("❌ No keyword provided")

    elif choice == '5':
        fishnet.cast_net()
        categories = fishnet.analyze_catches()
        fishnet.find_hidden_gems()
        fishnet.find_code_clusters()
        fishnet.export_report()

    elif choice == '6':
        fishnet.cast_net(['.py'])
        categories = fishnet.analyze_catches()
        fishnet.find_hidden_gems()

    elif choice == '0':
        print("\n👋 Happy fishing!")

    else:
        print("\n❌ Invalid option")

    print("\n🎣 FISHNET mission complete!")


if __name__ == "__main__":
    main()

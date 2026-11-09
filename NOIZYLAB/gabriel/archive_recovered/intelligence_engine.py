#!/usr/bin/env python3
"""
REAL-TIME INTELLIGENCE ENGINE
Scans codebase, detects changes, provides real insights
"""
import os
import json
import time
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import threading

class IntelligenceEngine:
    def __init__(self, watch_path):
        self.watch_path = Path(watch_path)
        self.file_hashes = {}
        self.stats = {
            'last_scan': None,
            'total_files': 0,
            'total_lines': 0,
            'total_bytes': 0,
            'languages': defaultdict(lambda: {'files': 0, 'lines': 0, 'bytes': 0}),
            'recent_changes': [],
            'hot_files': [],
            'complexity_score': 0
        }
        self.lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.sh': 'Shell',
            '.go': 'Go',
            '.html': 'HTML',
            '.css': 'CSS',
            '.md': 'Markdown',
            '.json': 'JSON',
        }

    def compute_hash(self, filepath):
        """Compute file hash for change detection"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def analyze_file(self, filepath):
        """Deep analysis of a single file"""
        try:
            stat = os.stat(filepath)
            ext = Path(filepath).suffix.lower()

            analysis = {
                'path': str(filepath),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'ext': ext,
                'lines': 0,
                'complexity': 0
            }

            # Count lines and analyze complexity for code files
            if ext in self.lang_map:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.readlines()
                    analysis['lines'] = len(content)

                    # Simple complexity metrics
                    for line in content:
                        line = line.strip()
                        if 'if ' in line or 'for ' in line or 'while ' in line:
                            analysis['complexity'] += 1
                        if 'def ' in line or 'function ' in line or 'class ' in line:
                            analysis['complexity'] += 2

            return analysis
        except Exception as e:
            return None

    def scan_codebase(self):
        """Full codebase scan with intelligence"""
        print(f"🔍 Scanning {self.watch_path}...")
        start_time = time.time()

        new_stats = {
            'last_scan': datetime.now().isoformat(),
            'total_files': 0,
            'total_lines': 0,
            'total_bytes': 0,
            'languages': defaultdict(lambda: {'files': 0, 'lines': 0, 'bytes': 0}),
            'recent_changes': [],
            'hot_files': [],
            'complexity_score': 0,
            'file_types': defaultdict(int)
        }

        file_analyses = []

        for root, dirs, files in os.walk(self.watch_path):
            # Skip noise
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]

            for file in files:
                if file.startswith('.'):
                    continue

                filepath = Path(root) / file
                ext = filepath.suffix.lower()

                # Analyze file
                analysis = self.analyze_file(filepath)
                if not analysis:
                    continue

                file_analyses.append(analysis)
                new_stats['total_files'] += 1
                new_stats['total_bytes'] += analysis['size']
                new_stats['total_lines'] += analysis['lines']
                new_stats['complexity_score'] += analysis['complexity']
                new_stats['file_types'][ext] += 1

                # Language stats
                if ext in self.lang_map:
                    lang = self.lang_map[ext]
                    new_stats['languages'][lang]['files'] += 1
                    new_stats['languages'][lang]['lines'] += analysis['lines']
                    new_stats['languages'][lang]['bytes'] += analysis['size']

                # Detect changes
                current_hash = self.compute_hash(filepath)
                if str(filepath) in self.file_hashes:
                    if self.file_hashes[str(filepath)] != current_hash:
                        new_stats['recent_changes'].append({
                            'file': str(filepath.relative_to(self.watch_path)),
                            'time': datetime.now().isoformat(),
                            'size': analysis['size'],
                            'lines': analysis['lines']
                        })

                self.file_hashes[str(filepath)] = current_hash

        # Find hot files (most complex)
        file_analyses.sort(key=lambda x: x['complexity'], reverse=True)
        new_stats['hot_files'] = [
            {
                'file': str(Path(f['path']).relative_to(self.watch_path)),
                'complexity': f['complexity'],
                'lines': f['lines'],
                'size': f['size']
            }
            for f in file_analyses[:20]
        ]

        # Limit recent changes
        new_stats['recent_changes'] = new_stats['recent_changes'][-50:]

        scan_time = time.time() - start_time
        new_stats['scan_time'] = round(scan_time, 2)

        self.stats = new_stats

        print(f"✅ Scan complete in {scan_time:.2f}s")
        print(f"   Files: {new_stats['total_files']:,}")
        print(f"   Lines: {new_stats['total_lines']:,}")
        print(f"   Complexity: {new_stats['complexity_score']:,}")

        return new_stats

    def get_insights(self):
        """Generate actionable insights"""
        insights = []

        # Complexity insights
        if self.stats['complexity_score'] > 10000:
            insights.append({
                'type': 'warning',
                'message': f"High complexity detected: {self.stats['complexity_score']:,} decision points",
                'suggestion': 'Consider refactoring hot files'
            })

        # Language diversity
        lang_count = len(self.stats['languages'])
        if lang_count > 5:
            insights.append({
                'type': 'info',
                'message': f"Multi-language codebase: {lang_count} languages detected",
                'suggestion': 'Strong polyglot capability'
            })

        # Large files
        large_files = [f for f in self.stats['hot_files'] if f['lines'] > 1000]
        if large_files:
            insights.append({
                'type': 'warning',
                'message': f"{len(large_files)} files over 1000 lines",
                'suggestion': 'Consider splitting large files'
            })

        # Recent activity
        if self.stats['recent_changes']:
            insights.append({
                'type': 'info',
                'message': f"{len(self.stats['recent_changes'])} files changed recently",
                'suggestion': 'Active development detected'
            })

        return insights

    def save_report(self, output_file='intelligence_report.json'):
        """Save full intelligence report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'stats': dict(self.stats),
            'insights': self.get_insights()
        }

        # Convert defaultdicts
        report['stats']['languages'] = dict(report['stats']['languages'])
        report['stats']['file_types'] = dict(report['stats']['file_types'])

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        return output_file

def watch_mode(engine, interval=60):
    """Continuous monitoring mode"""
    print(f"\n👁️  WATCH MODE ACTIVE - Scanning every {interval}s")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            engine.scan_codebase()
            report_file = engine.save_report()

            print(f"\n📊 Report: {report_file}")

            insights = engine.get_insights()
            if insights:
                print("\n💡 INSIGHTS:")
                for insight in insights:
                    icon = "⚠️ " if insight['type'] == 'warning' else "ℹ️ "
                    print(f"   {icon}{insight['message']}")
                    print(f"      → {insight['suggestion']}")

            print(f"\n⏳ Next scan in {interval}s...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n✅ Watch mode stopped")

if __name__ == '__main__':
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else '/Users/m2ultra/NOIZYLAB/GABRIEL'
    mode = sys.argv[2] if len(sys.argv) > 2 else 'scan'

    engine = IntelligenceEngine(target)

    if mode == 'watch':
        watch_mode(engine, interval=30)
    else:
        engine.scan_codebase()
        report = engine.save_report()

        print("\n" + "="*70)
        print("  INTELLIGENCE REPORT")
        print("="*70)

        insights = engine.get_insights()
        if insights:
            print("\n💡 INSIGHTS:")
            for insight in insights:
                icon = "⚠️ " if insight['type'] == 'warning' else "ℹ️ "
                print(f"   {icon}{insight['message']}")
                print(f"      → {insight['suggestion']}")

        print(f"\n📄 Full report: {report}")
        print("="*70 + "\n")

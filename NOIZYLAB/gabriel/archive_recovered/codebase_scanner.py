#!/usr/bin/env python3
"""
REAL CODEBASE SCANNER - Actually useful tool
Scans your project and gives REAL metrics
"""
import os
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def scan_directory(root_path):
    """Scan directory and return REAL stats"""
    stats = {
        'total_files': 0,
        'total_lines': 0,
        'total_size_bytes': 0,
        'languages': defaultdict(lambda: {'files': 0, 'lines': 0, 'bytes': 0}),
        'largest_files': [],
        'file_types': defaultdict(int),
        'errors': []
    }

    # Language extensions
    lang_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.sh': 'Shell',
        '.go': 'Go',
        '.html': 'HTML',
        '.css': 'CSS',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.txt': 'Text',
        '.yaml': 'YAML',
        '.yml': 'YAML'
    }

    for root, dirs, files in os.walk(root_path):
        # Skip common ignore dirs
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__', '.venv']]

        for file in files:
            if file.startswith('.'):
                continue

            filepath = os.path.join(root, file)
            ext = Path(file).suffix.lower()

            try:
                size = os.path.getsize(filepath)
                stats['total_files'] += 1
                stats['total_size_bytes'] += size
                stats['file_types'][ext] += 1

                # Count lines for text files
                if ext in lang_map:
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            stats['total_lines'] += lines

                            lang = lang_map[ext]
                            stats['languages'][lang]['files'] += 1
                            stats['languages'][lang]['lines'] += lines
                            stats['languages'][lang]['bytes'] += size
                    except Exception as e:
                        stats['errors'].append(f"Error reading {filepath}: {e}")

                # Track largest files
                stats['largest_files'].append({
                    'path': filepath.replace(root_path, ''),
                    'size': size,
                    'ext': ext
                })

            except Exception as e:
                stats['errors'].append(f"Error accessing {filepath}: {e}")

    # Sort largest files
    stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
    stats['largest_files'] = stats['largest_files'][:10]

    return stats

def format_bytes(bytes):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def print_report(stats):
    """Print formatted report"""
    print("\n" + "="*70)
    print("  REAL CODEBASE HEALTH REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

    # Overall stats
    print("📊 OVERALL STATISTICS:")
    print(f"   Total Files:  {stats['total_files']:,}")
    print(f"   Total Lines:  {stats['total_lines']:,}")
    print(f"   Total Size:   {format_bytes(stats['total_size_bytes'])}")
    print()

    # Language breakdown
    print("💻 LANGUAGES:")
    for lang, data in sorted(stats['languages'].items(), key=lambda x: x[1]['lines'], reverse=True):
        print(f"   {lang:12} {data['files']:4} files  {data['lines']:8,} lines  {format_bytes(data['bytes'])}")
    print()

    # File types
    print("📁 FILE TYPES:")
    for ext, count in sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:15]:
        ext_display = ext if ext else '(no ext)'
        print(f"   {ext_display:12} {count:4} files")
    print()

    # Largest files
    print("🔍 LARGEST FILES:")
    for f in stats['largest_files']:
        print(f"   {format_bytes(f['size']):>10}  {f['path']}")
    print()

    # Errors
    if stats['errors']:
        print(f"⚠️  ERRORS ({len(stats['errors'])}):")
        for err in stats['errors'][:5]:
            print(f"   {err}")
        if len(stats['errors']) > 5:
            print(f"   ... and {len(stats['errors']) - 5} more")
        print()

    print("="*70)
    print("✅ SCAN COMPLETE - ALL DATA IS REAL")
    print("="*70 + "\n")

def save_json_report(stats, output_file):
    """Save report as JSON"""
    # Convert defaultdict to dict for JSON
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_files': stats['total_files'],
        'total_lines': stats['total_lines'],
        'total_size_bytes': stats['total_size_bytes'],
        'total_size_human': format_bytes(stats['total_size_bytes']),
        'languages': dict(stats['languages']),
        'file_types': dict(stats['file_types']),
        'largest_files': stats['largest_files'],
        'errors': stats['errors']
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"📄 JSON report saved: {output_file}")

if __name__ == '__main__':
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    target = os.path.abspath(target)

    print(f"\n🔍 Scanning: {target}\n")

    stats = scan_directory(target)
    print_report(stats)

    # Save JSON
    json_file = 'codebase_report.json'
    save_json_report(stats, json_file)

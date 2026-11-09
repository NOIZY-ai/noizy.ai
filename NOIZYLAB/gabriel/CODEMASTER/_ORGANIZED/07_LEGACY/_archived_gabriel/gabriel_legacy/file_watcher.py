#!/usr/bin/env python3
"""
GABRIEL File Watcher - Real-time file system monitoring
Watches for changes and triggers actions (rescan, notify)
"""
import os
import sys
import time
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

class FileWatcher:
    """Watch for file changes in real-time"""

    def __init__(self, watch_paths: list, server_url: str = "http://localhost:5174"):
        self.watch_paths = [Path(p) for p in watch_paths]
        self.server_url = server_url
        self.file_hashes = {}
        self.change_log = []
        self.skip_dirs = {'node_modules', 'venv', '.venv', '__pycache__', '.git', 'dist', 'build', '.next'}
        self.watch_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.json', '.yaml', '.yml'}

        # Stats
        self.stats = {
            'files_watched': 0,
            'changes_detected': 0,
            'last_scan': None,
            'start_time': datetime.now().isoformat()
        }

    def hash_file(self, filepath: Path) -> str:
        """Get hash of file content"""
        try:
            content = filepath.read_bytes()
            return hashlib.md5(content).hexdigest()
        except:
            return None

    def scan_files(self) -> dict:
        """Scan all watched paths and build file hash map"""
        new_hashes = {}

        for watch_path in self.watch_paths:
            if not watch_path.exists():
                continue

            for root, dirs, files in os.walk(watch_path):
                # Skip unwanted directories
                dirs[:] = [d for d in dirs if d not in self.skip_dirs and not d.startswith('.')]

                for file in files:
                    filepath = Path(root) / file
                    if filepath.suffix in self.watch_extensions:
                        file_hash = self.hash_file(filepath)
                        if file_hash:
                            new_hashes[str(filepath)] = file_hash

        self.stats['files_watched'] = len(new_hashes)
        self.stats['last_scan'] = datetime.now().isoformat()

        return new_hashes

    def detect_changes(self, new_hashes: dict) -> dict:
        """Compare hashes to detect changes"""
        changes = {
            'added': [],
            'modified': [],
            'deleted': []
        }

        old_files = set(self.file_hashes.keys())
        new_files = set(new_hashes.keys())

        # Detect added files
        for filepath in new_files - old_files:
            changes['added'].append(filepath)

        # Detect deleted files
        for filepath in old_files - new_files:
            changes['deleted'].append(filepath)

        # Detect modified files
        for filepath in old_files & new_files:
            if self.file_hashes[filepath] != new_hashes[filepath]:
                changes['modified'].append(filepath)

        return changes

    def on_change(self, changes: dict):
        """Handle detected changes"""
        total_changes = len(changes['added']) + len(changes['modified']) + len(changes['deleted'])

        if total_changes == 0:
            return

        self.stats['changes_detected'] += total_changes

        # Log changes
        change_entry = {
            'timestamp': datetime.now().isoformat(),
            'added': len(changes['added']),
            'modified': len(changes['modified']),
            'deleted': len(changes['deleted']),
            'details': changes
        }
        self.change_log.append(change_entry)

        # Keep only last 100 changes
        if len(self.change_log) > 100:
            self.change_log = self.change_log[-100:]

        # Print changes
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] Changes detected:")

        for filepath in changes['added'][:5]:
            print(f"  + {Path(filepath).name}")
        for filepath in changes['modified'][:5]:
            print(f"  * {Path(filepath).name}")
        for filepath in changes['deleted'][:5]:
            print(f"  - {Path(filepath).name}")

        if total_changes > 15:
            print(f"  ... and {total_changes - 15} more")

        # Notify server
        self.notify_server(changes)

    def notify_server(self, changes: dict):
        """Notify server about changes"""
        try:
            resp = requests.post(
                f"{self.server_url}/api/watcher/changes",
                json={
                    'changes': changes,
                    'timestamp': datetime.now().isoformat(),
                    'stats': self.stats
                },
                timeout=5
            )
        except:
            pass  # Server might not have this endpoint yet

    def watch(self, interval: float = 2.0):
        """Start watching for changes"""
        print("\n" + "=" * 60)
        print("  GABRIEL FILE WATCHER - Real-Time Monitoring")
        print("=" * 60)
        print(f"\nWatching: {', '.join(str(p) for p in self.watch_paths)}")
        print(f"Extensions: {', '.join(self.watch_extensions)}")
        print(f"Interval: {interval}s")
        print("\nPress Ctrl+C to stop\n")

        # Initial scan
        print("Performing initial scan...")
        self.file_hashes = self.scan_files()
        print(f"Found {self.stats['files_watched']} files to watch\n")

        try:
            while True:
                time.sleep(interval)

                # Scan for changes
                new_hashes = self.scan_files()
                changes = self.detect_changes(new_hashes)

                # Process changes
                self.on_change(changes)

                # Update hashes
                self.file_hashes = new_hashes

        except KeyboardInterrupt:
            print("\n\nWatcher stopped")
            self.print_summary()

    def print_summary(self):
        """Print summary of watched activity"""
        print("\n" + "=" * 60)
        print("  WATCH SESSION SUMMARY")
        print("=" * 60)
        print(f"  Files watched:      {self.stats['files_watched']}")
        print(f"  Changes detected:   {self.stats['changes_detected']}")
        print(f"  Session start:      {self.stats['start_time']}")
        print(f"  Session end:        {datetime.now().isoformat()}")
        print("=" * 60 + "\n")


def main():
    # Default watch path
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = ['/Users/m2ultra/NOIZYLAB/GABRIEL']

    watcher = FileWatcher(paths)
    watcher.watch(interval=2.0)


if __name__ == '__main__':
    main()

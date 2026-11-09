#!/usr/bin/env python3
"""
GABRIEL MEGA SCANNER - JUMBO FRAMES EDITION
Scans ALL mounted drives at MAXIMUM SPEED
Zero Latency - Parallel Execution - Full Coverage
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import threading

# JUMBO FRAME CONFIG - MAX PARALLELISM
MAX_WORKERS = os.cpu_count() * 2 or 8
SCAN_TIMEOUT = 300  # 5 min max per volume

# Paths
GABRIEL_ROOT = Path.home() / "NOIZYLAB" / "GABRIEL"
SCANS_DIR = GABRIEL_ROOT / "scans"
SCANS_DIR.mkdir(parents=True, exist_ok=True)


class VolumeScanner:
    """Ultra-fast volume scanner with parallel execution"""

    def __init__(self):
        self.results = {}
        self.lock = threading.Lock()
        self.start_time = time.perf_counter()

    def get_mounted_volumes(self) -> list:
        """Get all mounted volumes - FAST"""
        volumes = []

        # Get from /Volumes
        volumes_path = Path("/Volumes")
        if volumes_path.exists():
            for v in volumes_path.iterdir():
                if v.is_dir() and not v.is_symlink():
                    volumes.append(v)

        # Add home directory
        volumes.append(Path.home())

        return volumes

    def get_volume_info(self, path: Path) -> dict:
        """Get volume info using df - FAST"""
        try:
            result = subprocess.run(
                ["df", "-h", str(path)],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    return {
                        "filesystem": parts[0] if len(parts) > 0 else "unknown",
                        "size": parts[1] if len(parts) > 1 else "0",
                        "used": parts[2] if len(parts) > 2 else "0",
                        "available": parts[3] if len(parts) > 3 else "0",
                        "use_percent": parts[4] if len(parts) > 4 else "0%",
                    }
        except:
            pass
        return {"error": "Could not get volume info"}

    def quick_scan_volume(self, volume: Path) -> dict:
        """Quick scan a volume - counts files by type"""
        stats = {
            "path": str(volume),
            "name": volume.name,
            "accessible": False,
            "info": {},
            "file_counts": defaultdict(int),
            "total_files": 0,
            "total_dirs": 0,
            "code_files": 0,
            "media_files": 0,
            "doc_files": 0,
            "scan_time_ms": 0,
            "error": None
        }

        scan_start = time.perf_counter()

        try:
            # Check accessibility
            if not volume.exists():
                stats["error"] = "Volume not accessible"
                return stats

            stats["accessible"] = True
            stats["info"] = self.get_volume_info(volume)

            # Code extensions
            code_ext = {'.py', '.js', '.ts', '.sh', '.swift', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.rb', '.php'}
            media_ext = {'.mp3', '.wav', '.flac', '.aiff', '.mp4', '.mov', '.avi', '.mkv', '.jpg', '.jpeg', '.png', '.gif', '.psd', '.ai'}
            doc_ext = {'.md', '.txt', '.pdf', '.doc', '.docx', '.json', '.yaml', '.yml', '.xml', '.html', '.css'}

            # Fast walk with limits
            file_limit = 100000  # Stop after 100k files per volume
            count = 0

            for root, dirs, files in os.walk(volume, followlinks=False):
                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', '.git', 'venv', 'Library', 'System'}]

                stats["total_dirs"] += len(dirs)

                for f in files:
                    count += 1
                    if count > file_limit:
                        stats["error"] = f"Scan limited to {file_limit} files"
                        break

                    stats["total_files"] += 1
                    ext = Path(f).suffix.lower()
                    stats["file_counts"][ext] += 1

                    if ext in code_ext:
                        stats["code_files"] += 1
                    elif ext in media_ext:
                        stats["media_files"] += 1
                    elif ext in doc_ext:
                        stats["doc_files"] += 1

                if count > file_limit:
                    break

        except PermissionError:
            stats["error"] = "Permission denied"
        except Exception as e:
            stats["error"] = str(e)[:200]

        stats["scan_time_ms"] = int((time.perf_counter() - scan_start) * 1000)
        stats["file_counts"] = dict(stats["file_counts"])

        return stats

    def scan_all_parallel(self) -> dict:
        """Scan all volumes in PARALLEL - JUMBO FRAMES"""
        volumes = self.get_mounted_volumes()

        print(f"\n⚡ GABRIEL MEGA SCANNER - JUMBO FRAMES EDITION")
        print(f"═" * 70)
        print(f"📀 Found {len(volumes)} volumes to scan")
        print(f"🔥 Using {MAX_WORKERS} parallel workers")
        print(f"═" * 70)

        results = {
            "timestamp": datetime.now().isoformat(),
            "total_volumes": len(volumes),
            "volumes": {},
            "summary": {
                "total_files": 0,
                "total_dirs": 0,
                "total_code": 0,
                "total_media": 0,
                "total_docs": 0,
            },
            "scan_time_ms": 0
        }

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self.quick_scan_volume, v): v for v in volumes}

            for future in as_completed(futures):
                volume = futures[future]
                try:
                    data = future.result(timeout=SCAN_TIMEOUT)
                    results["volumes"][str(volume)] = data

                    # Update summary
                    results["summary"]["total_files"] += data.get("total_files", 0)
                    results["summary"]["total_dirs"] += data.get("total_dirs", 0)
                    results["summary"]["total_code"] += data.get("code_files", 0)
                    results["summary"]["total_media"] += data.get("media_files", 0)
                    results["summary"]["total_docs"] += data.get("doc_files", 0)

                    # Print progress
                    status = "✅" if data.get("accessible") else "❌"
                    print(f"  {status} {volume.name}: {data.get('total_files', 0):,} files ({data.get('scan_time_ms', 0)}ms)")

                except Exception as e:
                    print(f"  ❌ {volume.name}: ERROR - {e}")
                    results["volumes"][str(volume)] = {"error": str(e)}

        results["scan_time_ms"] = int((time.perf_counter() - self.start_time) * 1000)

        return results

    def print_summary(self, results: dict):
        """Print beautiful summary"""
        GREEN = '\033[92m'
        CYAN = '\033[96m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'

        summary = results.get("summary", {})

        print(f"\n{CYAN}{'═' * 70}{RESET}")
        print(f"{CYAN}  SCAN COMPLETE - JUMBO FRAMES DELIVERED{RESET}")
        print(f"{CYAN}{'═' * 70}{RESET}\n")

        print(f"  {GREEN}📁 Total Files:{RESET}    {summary.get('total_files', 0):>15,}")
        print(f"  {GREEN}📂 Total Dirs:{RESET}     {summary.get('total_dirs', 0):>15,}")
        print(f"  {YELLOW}💻 Code Files:{RESET}     {summary.get('total_code', 0):>15,}")
        print(f"  {YELLOW}🎵 Media Files:{RESET}    {summary.get('total_media', 0):>15,}")
        print(f"  {YELLOW}📄 Doc Files:{RESET}      {summary.get('total_docs', 0):>15,}")

        print(f"\n  {GREEN}⚡ Total Scan Time:{RESET} {results.get('scan_time_ms', 0):,}ms")
        print(f"  {GREEN}📀 Volumes Scanned:{RESET} {results.get('total_volumes', 0)}")

        print(f"\n{CYAN}{'═' * 70}{RESET}")

        # Top extensions
        all_extensions = defaultdict(int)
        for vol_data in results.get("volumes", {}).values():
            if isinstance(vol_data, dict):
                for ext, count in vol_data.get("file_counts", {}).items():
                    all_extensions[ext] += count

        if all_extensions:
            print(f"\n  {YELLOW}TOP FILE TYPES:{RESET}")
            sorted_ext = sorted(all_extensions.items(), key=lambda x: x[1], reverse=True)[:15]
            for ext, count in sorted_ext:
                ext_display = ext if ext else "(no extension)"
                print(f"    {ext_display:<15} {count:>12,}")

        print(f"\n{CYAN}{'═' * 70}{RESET}\n")

    def save_results(self, results: dict):
        """Save scan results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = SCANS_DIR / f"volume_scan_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"💾 Results saved to: {output_file}")

        # Also save latest
        latest_file = SCANS_DIR / "latest_scan.json"
        with open(latest_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        return output_file


class CodebaseScanner:
    """Scan codebase for specific patterns - FAST"""

    def __init__(self):
        self.results = {}

    def find_all_code(self, root: Path, extensions: list = None) -> list:
        """Find all code files recursively"""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.sh', '.swift', '.go']

        code_files = []
        for ext in extensions:
            code_files.extend(root.rglob(f"*{ext}"))

        return [f for f in code_files if '.git' not in str(f) and 'node_modules' not in str(f)]

    def scan_for_patterns(self, files: list, patterns: list) -> dict:
        """Scan files for patterns in parallel"""
        results = defaultdict(list)

        def scan_file(filepath: Path) -> tuple:
            matches = []
            try:
                content = filepath.read_text(errors='ignore')
                for pattern in patterns:
                    if pattern.lower() in content.lower():
                        matches.append(pattern)
            except:
                pass
            return (filepath, matches)

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(scan_file, f) for f in files[:10000]]  # Limit
            for future in as_completed(futures):
                filepath, matches = future.result()
                for m in matches:
                    results[m].append(str(filepath))

        return dict(results)


def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="GABRIEL MEGA SCANNER")
    parser.add_argument("--quick", action="store_true", help="Quick scan only")
    parser.add_argument("--code", action="store_true", help="Scan for code patterns")
    parser.add_argument("--pattern", type=str, help="Search for specific pattern")
    args = parser.parse_args()

    scanner = VolumeScanner()
    results = scanner.scan_all_parallel()
    scanner.print_summary(results)
    scanner.save_results(results)

    if args.pattern:
        print(f"\n🔍 Searching for pattern: {args.pattern}")
        code_scanner = CodebaseScanner()
        code_files = code_scanner.find_all_code(Path.home() / "NOIZYLAB")
        pattern_results = code_scanner.scan_for_patterns(code_files, [args.pattern])
        print(f"Found in {len(pattern_results.get(args.pattern, []))} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())

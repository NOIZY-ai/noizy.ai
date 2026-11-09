#!/usr/bin/env python3
"""
GABRIEL UNIFIED VISUAL SCANNER X1000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Advanced visual analysis and system monitoring
GORUNFREE!! UPGRADE & IMPROVE!!
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class VisualScanner:
    """Advanced visual scanning and system analysis"""

    def __init__(self):
        self.name = "GABRIEL Visual Scanner X1000"
        self.version = "1.0.0-GORUNFREE"
        self.scan_start = datetime.now()
        self.results = {
            'system': {},
            'files': {},
            'processes': {},
            'network': {},
            'metrics': {}
        }

    def print_banner(self):
        """Display enhanced banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗         ║
║ ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║         ║
║ ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║         ║
║ ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║         ║
║ ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗    ║
║  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝    ║
║                                                          ║
║          UNIFIED VISUAL SCANNER X1000                    ║
║          GORUNFREE!! UPGRADE & IMPROVE!!                 ║
║                                                          ║
║  Version: {self.version:^42} ║
║  Time: {self.scan_start.strftime('%Y-%m-%d %H:%M:%S'):^45} ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
        print(banner)

    def scan_system_info(self) -> Dict[str, Any]:
        """Scan comprehensive system information"""
        print("\n🔍 SCANNING SYSTEM INFORMATION...")

        try:
            # Get macOS version
            sw_vers = subprocess.run(['sw_vers'], capture_output=True, text=True)

            # Get hardware info
            system_profiler = subprocess.run(
                ['system_profiler', 'SPHardwareDataType'],
                capture_output=True, text=True
            )

            # Get disk usage
            df_output = subprocess.run(['df', '-h'], capture_output=True, text=True)

            # Get memory info
            vm_stat = subprocess.run(['vm_stat'], capture_output=True, text=True)

            self.results['system'] = {
                'os_info': sw_vers.stdout,
                'hardware': system_profiler.stdout,
                'disk_usage': df_output.stdout,
                'memory': vm_stat.stdout,
                'hostname': os.uname().nodename,
                'user': os.getenv('USER', 'unknown')
            }

            print("   ✅ System info collected")
            return self.results['system']

        except Exception as e:
            print(f"   ⚠️  Error scanning system: {e}")
            return {}

    def scan_file_structure(self, path: str = ".") -> Dict[str, Any]:
        """Scan and analyze file structure"""
        print(f"\n📁 SCANNING FILE STRUCTURE: {path}")

        try:
            file_stats = {
                'total_files': 0,
                'total_dirs': 0,
                'total_size': 0,
                'by_extension': {},
                'largest_files': []
            }

            for root, dirs, files in os.walk(path):
                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

                file_stats['total_dirs'] += len(dirs)

                for file in files:
                    if file.startswith('.'):
                        continue

                    file_stats['total_files'] += 1
                    filepath = Path(root) / file

                    try:
                        size = filepath.stat().st_size
                        file_stats['total_size'] += size

                        # Track by extension
                        ext = filepath.suffix or 'no_extension'
                        if ext not in file_stats['by_extension']:
                            file_stats['by_extension'][ext] = {'count': 0, 'size': 0}
                        file_stats['by_extension'][ext]['count'] += 1
                        file_stats['by_extension'][ext]['size'] += size

                        # Track largest files
                        file_stats['largest_files'].append({
                            'path': str(filepath),
                            'size': size
                        })

                    except Exception as e:
                        continue

            # Sort and limit largest files
            file_stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
            file_stats['largest_files'] = file_stats['largest_files'][:20]

            self.results['files'] = file_stats

            print(f"   ✅ Found {file_stats['total_files']} files in {file_stats['total_dirs']} directories")
            print(f"   📊 Total size: {self.format_bytes(file_stats['total_size'])}")

            return file_stats

        except Exception as e:
            print(f"   ⚠️  Error scanning files: {e}")
            return {}

    def scan_running_processes(self) -> List[Dict[str, Any]]:
        """Scan running processes"""
        print("\n⚙️  SCANNING RUNNING PROCESSES...")

        try:
            ps_output = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )

            processes = []
            for line in ps_output.stdout.split('\n')[1:]:  # Skip header
                if line.strip():
                    parts = line.split(None, 10)
                    if len(parts) >= 11:
                        processes.append({
                            'user': parts[0],
                            'pid': parts[1],
                            'cpu': parts[2],
                            'mem': parts[3],
                            'command': parts[10]
                        })

            # Sort by CPU usage
            processes.sort(key=lambda x: float(x['cpu']), reverse=True)

            self.results['processes'] = processes[:30]  # Top 30

            print(f"   ✅ Analyzed {len(processes)} processes")
            print(f"   🔥 Top CPU: {processes[0]['command'][:50]}..." if processes else "   No processes")

            return processes

        except Exception as e:
            print(f"   ⚠️  Error scanning processes: {e}")
            return []

    def scan_network_status(self) -> Dict[str, Any]:
        """Scan network configuration and status"""
        print("\n🌐 SCANNING NETWORK STATUS...")

        try:
            # Get network interfaces
            ifconfig = subprocess.run(['ifconfig'], capture_output=True, text=True)

            # Get active connections
            netstat = subprocess.run(
                ['netstat', '-an'],
                capture_output=True,
                text=True
            )

            self.results['network'] = {
                'interfaces': ifconfig.stdout,
                'connections': netstat.stdout[:5000]  # Limit output
            }

            print("   ✅ Network status collected")

            return self.results['network']

        except Exception as e:
            print(f"   ⚠️  Error scanning network: {e}")
            return {}

    def calculate_metrics(self):
        """Calculate performance metrics"""
        print("\n📊 CALCULATING METRICS...")

        scan_duration = (datetime.now() - self.scan_start).total_seconds()

        self.results['metrics'] = {
            'scan_duration': scan_duration,
            'scan_timestamp': self.scan_start.isoformat(),
            'completion_time': datetime.now().isoformat(),
            'total_data_points': sum([
                len(str(self.results['system'])),
                len(str(self.results['files'])),
                len(str(self.results['processes'])),
                len(str(self.results['network']))
            ])
        }

        print(f"   ✅ Scan completed in {scan_duration:.2f} seconds")

    def generate_report(self) -> str:
        """Generate comprehensive visual report"""
        print("\n📝 GENERATING REPORT...")

        report = f"""
╔══════════════════════════════════════════════════════════╗
║              GABRIEL VISUAL SCAN REPORT                  ║
╚══════════════════════════════════════════════════════════╝

⏱️  SCAN METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Started:  {self.results['metrics']['scan_timestamp']}
Finished: {self.results['metrics']['completion_time']}
Duration: {self.results['metrics']['scan_duration']:.2f} seconds

📁 FILE STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Files:       {self.results['files'].get('total_files', 0):,}
Total Directories: {self.results['files'].get('total_dirs', 0):,}
Total Size:        {self.format_bytes(self.results['files'].get('total_size', 0))}

📊 TOP FILE TYPES:
"""

        # Add file type breakdown
        if 'by_extension' in self.results['files']:
            sorted_exts = sorted(
                self.results['files']['by_extension'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:10]

            for ext, stats in sorted_exts:
                report += f"   {ext:20s} {stats['count']:6,} files  {self.format_bytes(stats['size']):>12s}\n"

        report += f"""
⚙️  PROCESS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Active Processes: {len(self.results.get('processes', []))}

🔥 TOP CPU CONSUMERS:
"""

        # Add top processes
        for proc in self.results.get('processes', [])[:5]:
            report += f"   {proc['cpu']:>6s}%  {proc['mem']:>6s}%  {proc['command'][:60]}\n"

        report += f"""
💾 SYSTEM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hostname: {self.results['system'].get('hostname', 'unknown')}
User:     {self.results['system'].get('user', 'unknown')}

╔══════════════════════════════════════════════════════════╗
║              SCAN COMPLETE - GORUNFREE!!                 ║
╚══════════════════════════════════════════════════════════╝
"""

        return report

    def save_results(self, output_dir: str = "GABRIEL_UNIFIED/reports"):
        """Save scan results to JSON"""
        print(f"\n💾 SAVING RESULTS...")

        try:
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/visual_scan_{timestamp}.json"

            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)

            print(f"   ✅ Results saved to: {filename}")
            return filename

        except Exception as e:
            print(f"   ⚠️  Error saving results: {e}")
            return None

    def format_bytes(self, bytes_val: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"

    def run_full_scan(self) -> Dict[str, Any]:
        """Execute complete visual scan"""
        self.print_banner()

        # Run all scans
        self.scan_system_info()
        self.scan_file_structure()
        self.scan_running_processes()
        self.scan_network_status()
        self.calculate_metrics()

        # Generate and display report
        report = self.generate_report()
        print(report)

        # Save results
        self.save_results()

        return self.results


def main():
    """Main execution"""
    scanner = VisualScanner()

    try:
        results = scanner.run_full_scan()

        print("\n🚀 GABRIEL VISUAL SCANNER - COMPLETE!")
        print("   GORUNFREE!! UPGRADE & IMPROVE!!\n")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        return 1

    except Exception as e:
        print(f"\n\n❌ Error during scan: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

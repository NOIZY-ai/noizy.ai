#!/usr/bin/env python3
"""
GABRIEL UNIFIED PERFORMANCE MONITOR X3000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Real-time system performance monitoring and alerts
GORUNFREE!! UPGRADE & IMPROVE!!
"""

import os
import sys
import time
import psutil
import subprocess
from datetime import datetime
from typing import Dict, List, Any


class PerformanceMonitor:
    """Real-time performance monitoring system"""

    def __init__(self, interval: int = 1, duration: int = 60):
        self.name = "GABRIEL Performance Monitor X3000"
        self.version = "3.0.0-GORUNFREE"
        self.interval = interval
        self.duration = duration
        self.samples = []

    def print_banner(self):
        """Display monitor banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    📊 GABRIEL PERFORMANCE MONITOR X3000 📊               ║
║                                                          ║
║    Real-Time System Performance Tracking                ║
║    GORUNFREE!! UPGRADE & IMPROVE!!                       ║
║                                                          ║
║    Version: {self.version:^43}║
║    Interval: {self.interval}s | Duration: {self.duration}s                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
        print(banner)

    def get_cpu_usage(self) -> Dict[str, Any]:
        """Get CPU usage statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
            cpu_freq = psutil.cpu_freq()

            return {
                'total': psutil.cpu_percent(),
                'per_cpu': cpu_percent,
                'count': psutil.cpu_count(),
                'frequency': {
                    'current': cpu_freq.current if cpu_freq else 0,
                    'min': cpu_freq.min if cpu_freq else 0,
                    'max': cpu_freq.max if cpu_freq else 0
                }
            }
        except:
            return {'total': 0, 'per_cpu': [], 'count': 0}

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                'total': mem.total,
                'available': mem.available,
                'used': mem.used,
                'percent': mem.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_percent': swap.percent
            }
        except:
            return {}

    def get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage statistics"""
        try:
            disk = psutil.disk_usage('/')
            io = psutil.disk_io_counters()

            return {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'read_bytes': io.read_bytes if io else 0,
                'write_bytes': io.write_bytes if io else 0
            }
        except:
            return {}

    def get_network_usage(self) -> Dict[str, Any]:
        """Get network usage statistics"""
        try:
            net = psutil.net_io_counters()

            return {
                'bytes_sent': net.bytes_sent,
                'bytes_recv': net.bytes_recv,
                'packets_sent': net.packets_sent,
                'packets_recv': net.packets_recv
            }
        except:
            return {}

    def get_process_info(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Get top processes by resource usage"""
        try:
            processes = []

            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'cpu': pinfo['cpu_percent'] or 0,
                        'memory': pinfo['memory_percent'] or 0
                    })
                except:
                    continue

            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu'], reverse=True)
            return processes[:top_n]

        except:
            return []

    def format_bytes(self, bytes_val: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"

    def draw_bar(self, percent: float, width: int = 40) -> str:
        """Draw a progress bar"""
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)

        # Color based on percentage
        if percent < 50:
            color = '\033[92m'  # Green
        elif percent < 80:
            color = '\033[93m'  # Yellow
        else:
            color = '\033[91m'  # Red

        return f"{color}{bar}\033[0m {percent:5.1f}%"

    def display_realtime(self):
        """Display real-time performance metrics"""
        try:
            # Clear screen
            os.system('clear')

            # Get current stats
            cpu = self.get_cpu_usage()
            mem = self.get_memory_usage()
            disk = self.get_disk_usage()
            net = self.get_network_usage()
            top_procs = self.get_process_info(5)

            print(f"\n{'='*70}")
            print(f"  GABRIEL PERFORMANCE MONITOR - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*70}\n")

            # CPU
            print(f"💻 CPU Usage:")
            print(f"   {self.draw_bar(cpu['total'])}")
            if cpu['per_cpu']:
                cores_display = ', '.join([f"{c:.1f}%" for c in cpu['per_cpu'][:4]])
                print(f"   Cores: {cores_display}...")

            # Memory
            print(f"\n🧠 Memory Usage:")
            print(f"   {self.draw_bar(mem.get('percent', 0))}")
            print(f"   Used: {self.format_bytes(mem.get('used', 0))} / {self.format_bytes(mem.get('total', 0))}")

            # Disk
            print(f"\n💾 Disk Usage:")
            print(f"   {self.draw_bar(disk.get('percent', 0))}")
            print(f"   Free: {self.format_bytes(disk.get('free', 0))}")

            # Network
            print(f"\n🌐 Network:")
            print(f"   ⬆️  Sent: {self.format_bytes(net.get('bytes_sent', 0))}")
            print(f"   ⬇️  Recv: {self.format_bytes(net.get('bytes_recv', 0))}")

            # Top Processes
            print(f"\n🔥 Top Processes:")
            for i, proc in enumerate(top_procs, 1):
                print(f"   {i}. {proc['name'][:30]:30s} CPU: {proc['cpu']:6.1f}% MEM: {proc['memory']:5.1f}%")

            print(f"\n{'='*70}")
            print(f"  Press Ctrl+C to stop monitoring")
            print(f"{'='*70}")

        except Exception as e:
            print(f"Error displaying stats: {e}")

    def run_monitoring(self):
        """Run continuous monitoring"""
        self.print_banner()

        print(f"\n🚀 Starting performance monitoring...")
        print(f"   Interval: {self.interval}s")
        print(f"   Duration: {self.duration}s")
        print(f"\n   Press Ctrl+C to stop early\n")

        time.sleep(2)

        start_time = time.time()
        try:
            while True:
                # Check if duration exceeded
                if time.time() - start_time > self.duration:
                    break

                # Display current stats
                self.display_realtime()

                # Collect sample
                sample = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu': self.get_cpu_usage(),
                    'memory': self.get_memory_usage(),
                    'disk': self.get_disk_usage(),
                    'network': self.get_network_usage()
                }
                self.samples.append(sample)

                # Wait for next interval
                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\n\n⚠️  Monitoring stopped by user")

        # Summary
        self.display_summary()

    def display_summary(self):
        """Display monitoring summary"""
        if not self.samples:
            return

        print("\n\n" + "="*70)
        print("  MONITORING SUMMARY")
        print("="*70 + "\n")

        # Calculate averages
        avg_cpu = sum(s['cpu']['total'] for s in self.samples) / len(self.samples)
        avg_mem = sum(s['memory'].get('percent', 0) for s in self.samples) / len(self.samples)

        print(f"📊 Samples Collected: {len(self.samples)}")
        print(f"📊 Average CPU: {avg_cpu:.1f}%")
        print(f"📊 Average Memory: {avg_mem:.1f}%")

        print("\n✅ Monitoring complete - GORUNFREE!!\n")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='GABRIEL Performance Monitor')
    parser.add_argument('-i', '--interval', type=int, default=1, help='Sampling interval in seconds')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Monitoring duration in seconds')

    args = parser.parse_args()

    monitor = PerformanceMonitor(interval=args.interval, duration=args.duration)

    try:
        monitor.run_monitoring()
        return 0

    except Exception as e:
        print(f"\n\n❌ Error during monitoring: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

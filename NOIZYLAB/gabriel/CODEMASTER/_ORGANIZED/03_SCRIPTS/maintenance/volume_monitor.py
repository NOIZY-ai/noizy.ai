#!/usr/bin/env python3
"""
VOLUME MONITOR - Real-time disk space monitoring
Alerts when volumes reach critical levels
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

class VolumeMonitor:
    CRITICAL_THRESHOLD = 95
    WARNING_THRESHOLD = 85
    
    def __init__(self):
        self.volumes = {}
        
    def scan_volumes(self):
        """Scan all mounted volumes"""
        result = subprocess.run(["df", "-h"], capture_output=True, text=True)
        
        for line in result.stdout.split('\n')[1:]:
            parts = line.split()
            if len(parts) >= 6 and ('/Volumes/' in line or '/System/Volumes/Data' in line):
                mount = parts[-1]
                name = mount.replace('/Volumes/', '').replace('/System/Volumes/Data', 'Main Drive')
                
                try:
                    pct = int(parts[4].replace('%', ''))
                    size = parts[1]
                    used = parts[2]
                    avail = parts[3]
                    
                    self.volumes[name] = {
                        'mount': mount,
                        'size': size,
                        'used': used,
                        'available': avail,
                        'percent': pct,
                        'status': self._get_status(pct)
                    }
                except:
                    pass
    
    def _get_status(self, pct):
        if pct >= self.CRITICAL_THRESHOLD:
            return '🔴 CRITICAL'
        elif pct >= self.WARNING_THRESHOLD:
            return '🟡 WARNING'
        elif pct >= 70:
            return '🟢 OK'
        else:
            return '✅ GOOD'
    
    def report(self):
        """Generate status report"""
        self.scan_volumes()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    VOLUME MONITOR                            ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🕐 Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Sort by percent used (highest first)
        sorted_vols = sorted(self.volumes.items(), key=lambda x: x[1]['percent'], reverse=True)
        
        print(f"{'Volume':<25} {'Used':<10} {'Avail':<10} {'%':>5}  Status")
        print("─" * 70)
        
        for name, info in sorted_vols:
            print(f"{name:<25} {info['used']:<10} {info['available']:<10} {info['percent']:>4}%  {info['status']}")
        
        # Alerts
        critical = [n for n, v in self.volumes.items() if v['percent'] >= self.CRITICAL_THRESHOLD]
        if critical:
            print(f"\n⚠️  CRITICAL ALERTS: {', '.join(critical)}")
            print("   Consider moving data to volumes with more space!")
            
        # Recommendations
        good_targets = [n for n, v in self.volumes.items() if v['percent'] < 50]
        if good_targets and critical:
            print(f"\n💡 Recommended targets for data migration: {', '.join(good_targets)}")
    
    def to_json(self):
        """Export as JSON"""
        self.scan_volumes()
        return json.dumps({
            'timestamp': datetime.now().isoformat(),
            'volumes': self.volumes
        }, indent=2)

if __name__ == "__main__":
    monitor = VolumeMonitor()
    monitor.report()

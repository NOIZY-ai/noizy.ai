#!/usr/bin/env python3
"""
VOLUME MONITOR UPGRADED - Cutting-edge real-time disk space monitoring
Async/await, type hints, caching, network optimization
"""

import subprocess
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, TypedDict
from functools import lru_cache

class VolumeInfo(TypedDict):
    mount: str
    size: str
    used: str
    available: str
    percent: int
    status: str
    device: Optional[str]
    is_network: bool

class VolumeMonitorUpgraded:
    """Upgraded volume monitor with async, caching, and optimization"""
    
    CRITICAL_THRESHOLD = 95
    WARNING_THRESHOLD = 85
    CACHE_DURATION = timedelta(seconds=30)
    
    def __init__(self):
        self.volumes: Dict[str, VolumeInfo] = {}
        self._cache_time: Optional[datetime] = None
        self._cache_data: Optional[Dict] = None
    
    async def scan_volumes_async(self) -> Dict[str, VolumeInfo]:
        """Async volume scanning with caching"""
        # Check cache
        if self._cache_data and self._cache_time:
            if datetime.now() - self._cache_time < self.CACHE_DURATION:
                return self._cache_data
        
        # Run df command in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                ["df", "-h"],
                capture_output=True,
                text=True,
                timeout=15
            )
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"df command failed: {result.stderr}")
        
        volumes: Dict[str, VolumeInfo] = {}
        
        for line in result.stdout.split('\n')[1:]:
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) < 6:
                continue
            
            mount = ' '.join(parts[5:])
            if '/Volumes/' not in mount and '/System/Volumes/Data' not in mount:
                continue
            
            try:
                device = parts[0]
                is_network = device.startswith('//') or 'smb://' in mount.lower()
                
                usage_str = parts[4].replace('%', '')
                pct = int(usage_str)
                
                name = mount.replace('/Volumes/', '').replace('/System/Volumes/Data', 'Main Drive')
                
                volumes[name] = VolumeInfo(
                    mount=mount,
                    size=parts[1],
                    used=parts[2],
                    available=parts[3],
                    percent=pct,
                    status=self._get_status(pct),
                    device=device,
                    is_network=is_network
                )
            except (ValueError, IndexError) as e:
                # Log but continue processing other volumes
                print(f"Warning: Failed to parse volume line: {line[:50]}... Error: {e}")
                continue
        
        # Update cache
        self._cache_data = volumes
        self._cache_time = datetime.now()
        self.volumes = volumes
        
        return volumes
    
    def scan_volumes(self) -> Dict[str, VolumeInfo]:
        """Synchronous wrapper for async scan"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.scan_volumes_async())
    
    def _get_status(self, pct: int) -> str:
        """Get status string for usage percentage"""
        if pct >= self.CRITICAL_THRESHOLD:
            return '🔴 CRITICAL'
        elif pct >= self.WARNING_THRESHOLD:
            return '🟡 WARNING'
        elif pct >= 70:
            return '🟢 OK'
        else:
            return '✅ GOOD'
    
    async def get_critical_volumes_async(self) -> List[str]:
        """Get list of critical capacity volumes (async)"""
        await self.scan_volumes_async()
        return [
            name for name, info in self.volumes.items()
            if info['percent'] >= self.CRITICAL_THRESHOLD
        ]
    
    def get_critical_volumes(self) -> List[str]:
        """Get list of critical capacity volumes (sync wrapper)"""
        if not self.volumes:
            self.scan_volumes()
        return [
            name for name, info in self.volumes.items()
            if info['percent'] >= self.CRITICAL_THRESHOLD
        ]
    
    async def get_network_volumes_async(self) -> Dict[str, VolumeInfo]:
        """Get network/SMB volumes (async)"""
        await self.scan_volumes_async()
        return {
            name: info for name, info in self.volumes.items()
            if info.get('is_network', False)
        }
    
    def get_network_volumes(self) -> Dict[str, VolumeInfo]:
        """Get network/SMB volumes (sync wrapper)"""
        if not self.volumes:
            self.scan_volumes()
        return {
            name: info for name, info in self.volumes.items()
            if info.get('is_network', False)
        }
    
    def report(self) -> None:
        """Generate formatted status report"""
        self.scan_volumes()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║            VOLUME MONITOR UPGRADED                            ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🕐 Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Sort by percent used (highest first)
        sorted_vols = sorted(
            self.volumes.items(),
            key=lambda x: x[1]['percent'],
            reverse=True
        )
        
        print(f"{'Volume':<25} {'Used':<10} {'Avail':<10} {'%':>5}  Status")
        print("─" * 70)
        
        for name, info in sorted_vols:
            network_indicator = "🌐" if info.get('is_network') else " "
            print(f"{network_indicator}{name:<24} {info['used']:<10} {info['available']:<10} {info['percent']:>4}%  {info['status']}")
        
        # Critical alerts
        critical = self.get_critical_volumes()
        if critical:
            print(f"\n⚠️  CRITICAL ALERTS: {', '.join(critical)}")
            print("   Consider moving data to volumes with more space!")
        
        # Network volumes summary
        network_vols = self.get_network_volumes()
        if network_vols:
            print(f"\n🌐 NETWORK VOLUMES: {len(network_vols)} volumes detected")
            for name, info in network_vols.items():
                print(f"   • {name}: {info['percent']}% used ({info['available']} available)")
        
        # Recommendations
        good_targets = [
            n for n, v in self.volumes.items()
            if v['percent'] < 50 and not v.get('is_network', False)
        ]
        if good_targets and critical:
            print(f"\n💡 Recommended targets for data migration: {', '.join(good_targets)}")
    
    def to_json(self) -> str:
        """Export as JSON"""
        self.scan_volumes()
        return json.dumps({
            'timestamp': datetime.now().isoformat(),
            'volumes': self.volumes,
            'critical': self.get_critical_volumes(),
            'network_count': len(self.get_network_volumes())
        }, indent=2)

if __name__ == "__main__":
    monitor = VolumeMonitorUpgraded()
    monitor.report()


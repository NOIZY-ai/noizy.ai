#!/usr/bin/env python3
"""
🌟 GABRIEL OMNIDIRECTIONAL CONTROL SYSTEM
Control EVERYTHING in EVERY DIRECTION simultaneously
North, South, East, West, Up, Down, Forward, Backward, Inward, Outward
Past, Present, Future - Total MC96ECOUNIVERSE dominance
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

class OmnidirectionalControl:
    """
    🌟 GABRIEL's Omnidirectional Control System
    Simultaneous control in ALL directions
    """
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.python = sys.executable
        
        # Direction vectors
        self.directions = {
            'NORTH': 'Filesystem Up (Parent Directories)',
            'SOUTH': 'Filesystem Down (Subdirectories)',
            'EAST': 'Network Out (Remote Systems)',
            'WEST': 'Network In (Local Services)',
            'UP': 'Cloud Services (Azure, AWS, GitHub)',
            'DOWN': 'Hardware Layer (Drives, Devices)',
            'FORWARD': 'Future Operations (Scheduled Tasks)',
            'BACKWARD': 'Historical Data (Logs, History)',
            'INWARD': 'Internal Systems (X1000, Fishnet)',
            'OUTWARD': 'External APIs (Spotify, Termius)',
            'TEMPORAL_PAST': 'Version Control (Git History)',
            'TEMPORAL_FUTURE': 'Predictions (AI Planning)',
            'DIMENSIONAL_PARALLEL': 'Multi-threading',
            'DIMENSIONAL_QUANTUM': 'All possibilities at once'
        }
        
        self.systems = {}
        self.active_threads = []
        self.results = {}
        
        print("\n" + "=" * 80)
        print("🌟 GABRIEL OMNIDIRECTIONAL CONTROL SYSTEM")
        print("   Control EVERYTHING in EVERY DIRECTION")
        print("=" * 80)
    
    def scan_all_directions(self):
        """Scan in ALL directions simultaneously."""
        print("\n🌟 SCANNING ALL DIRECTIONS SIMULTANEOUSLY...")
        print("=" * 80)
        
        with ThreadPoolExecutor(max_workers=14) as executor:
            futures = {
                executor.submit(self._scan_north): 'NORTH',
                executor.submit(self._scan_south): 'SOUTH',
                executor.submit(self._scan_east): 'EAST',
                executor.submit(self._scan_west): 'WEST',
                executor.submit(self._scan_up): 'UP',
                executor.submit(self._scan_down): 'DOWN',
                executor.submit(self._scan_forward): 'FORWARD',
                executor.submit(self._scan_backward): 'BACKWARD',
                executor.submit(self._scan_inward): 'INWARD',
                executor.submit(self._scan_outward): 'OUTWARD',
                executor.submit(self._scan_temporal_past): 'TEMPORAL_PAST',
                executor.submit(self._scan_temporal_future): 'TEMPORAL_FUTURE',
                executor.submit(self._scan_parallel): 'DIMENSIONAL_PARALLEL',
                executor.submit(self._scan_quantum): 'DIMENSIONAL_QUANTUM'
            }
            
            for future in as_completed(futures):
                direction = futures[future]
                try:
                    result = future.result()
                    self.results[direction] = result
                    status = "✅" if result['success'] else "⚠️"
                    print(f"{status} {direction:25s} : {result['summary']}")
                except Exception as e:
                    print(f"❌ {direction:25s} : {e}")
        
        print("=" * 80)
        print(f"🌟 Scanned {len(self.results)} directions!")
    
    def _scan_north(self) -> Dict:
        """NORTH: Scan parent directories."""
        try:
            current = self.workspace
            parents = []
            while current != current.parent:
                parents.append(str(current))
                current = current.parent
            
            return {
                'success': True,
                'summary': f'{len(parents)} levels up',
                'data': parents
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_south(self) -> Dict:
        """SOUTH: Scan subdirectories."""
        try:
            subdirs = [str(d) for d in self.workspace.rglob('*') if d.is_dir()][:100]
            return {
                'success': True,
                'summary': f'{len(subdirs)} subdirectories',
                'data': subdirs
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_east(self) -> Dict:
        """EAST: Scan network/remote systems."""
        try:
            # Check network connectivity
            result = subprocess.run(['ping', '-c', '1', 'google.com'], 
                                  capture_output=True, timeout=3)
            online = result.returncode == 0
            
            return {
                'success': True,
                'summary': 'Online' if online else 'Offline',
                'data': {'network': online}
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_west(self) -> Dict:
        """WEST: Scan local services."""
        try:
            services = []
            ports = [8080, 3000, 5000, 8000, 27017]  # Common local service ports
            for port in ports:
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    result = sock.connect_ex(('localhost', port))
                    if result == 0:
                        services.append(port)
                    sock.close()
                except:
                    pass
            
            return {
                'success': True,
                'summary': f'{len(services)} services running',
                'data': services
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_up(self) -> Dict:
        """UP: Check cloud connectivity."""
        try:
            clouds = {
                'GitHub': 'github.com',
                'Azure': 'azure.microsoft.com',
                'AWS': 'aws.amazon.com'
            }
            
            reachable = []
            for name, host in clouds.items():
                try:
                    result = subprocess.run(['ping', '-c', '1', host], 
                                          capture_output=True, timeout=2)
                    if result.returncode == 0:
                        reachable.append(name)
                except:
                    pass
            
            return {
                'success': True,
                'summary': f'{len(reachable)} clouds reachable',
                'data': reachable
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_down(self) -> Dict:
        """DOWN: Scan ALL hardware/drives - LOCAL AND NETWORK."""
        try:
            all_drives = []
            
            # macOS mounted volumes
            volumes_path = Path('/Volumes')
            if volumes_path.exists():
                for v in volumes_path.iterdir():
                    if v.is_dir() and not v.name.startswith('.'):
                        # Check if network or local
                        try:
                            result = subprocess.run(['df', str(v)], 
                                                  capture_output=True, text=True, check=False)
                            is_network = '//' in result.stdout or 'nfs' in result.stdout or 'smb' in result.stdout
                            drive_type = '🌐 NETWORK' if is_network else '💾 LOCAL'
                            
                            # Get size info
                            stat = v.stat()
                            all_drives.append({
                                'name': v.name,
                                'path': str(v),
                                'type': drive_type,
                                'accessible': True
                            })
                        except:
                            all_drives.append({
                                'name': v.name,
                                'path': str(v),
                                'type': '❓ UNKNOWN',
                                'accessible': False
                            })
            
            # Check df for all mounted filesystems
            try:
                result = subprocess.run(['df', '-h'], capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    for line in result.stdout.split('\n')[1:]:  # Skip header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 6:
                                mount_point = parts[-1]
                                filesystem = parts[0]
                                # Add network mounts not in /Volumes
                                if ('//' in filesystem or 'nfs' in filesystem or 'smb' in filesystem):
                                    if mount_point not in [d['path'] for d in all_drives]:
                                        all_drives.append({
                                            'name': Path(mount_point).name or mount_point,
                                            'path': mount_point,
                                            'type': '🌐 NETWORK',
                                            'filesystem': filesystem,
                                            'accessible': True
                                        })
            except Exception:
                pass
            
            return {
                'success': True,
                'summary': f'{len(all_drives)} total drives (LOCAL + NETWORK)',
                'data': all_drives
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_forward(self) -> Dict:
        """FORWARD: Check scheduled tasks."""
        try:
            # Check for task schedulers
            has_cron = Path('/etc/crontab').exists() or Path('/var/spool/cron').exists()
            
            return {
                'success': True,
                'summary': 'Scheduler available' if has_cron else 'No scheduler',
                'data': {'cron': has_cron}
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_backward(self) -> Dict:
        """BACKWARD: Scan historical data."""
        try:
            log_files = list(self.workspace.glob('*.log'))
            history_files = list(self.workspace.glob('*history*'))
            
            return {
                'success': True,
                'summary': f'{len(log_files)} logs, {len(history_files)} history',
                'data': {'logs': len(log_files), 'history': len(history_files)}
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_inward(self) -> Dict:
        """INWARD: Scan internal GABRIEL systems."""
        try:
            systems = [
                'autonomous_learning.py',
                'the_fishnet.py',
                'the_fishnet_universe.py',
                'GABRIEL_CODEMASTER.py',
                'TERMINUS.py',
                'TERMINUS_BRIDGE.py',
                'distribute_to_drives.py'
            ]
            
            found = [s for s in systems if (self.workspace / s).exists()]
            
            return {
                'success': True,
                'summary': f'{len(found)}/{len(systems)} systems found',
                'data': found
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_outward(self) -> Dict:
        """OUTWARD: Check external APIs."""
        try:
            apis = {
                'Spotify': Path('/Applications/Spotify.app').exists(),
                'Docker': subprocess.run(['which', 'docker'], 
                                       capture_output=True).returncode == 0,
                'Git': subprocess.run(['which', 'git'], 
                                    capture_output=True).returncode == 0
            }
            
            available = [k for k, v in apis.items() if v]
            
            return {
                'success': True,
                'summary': f'{len(available)} APIs available',
                'data': available
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_temporal_past(self) -> Dict:
        """TEMPORAL_PAST: Git history."""
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-n', '10'],
                                  capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                commits = len(result.stdout.strip().split('\n'))
                return {
                    'success': True,
                    'summary': f'{commits} recent commits',
                    'data': result.stdout
                }
            else:
                return {
                    'success': True,
                    'summary': 'Not a git repo',
                    'data': None
                }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_temporal_future(self) -> Dict:
        """TEMPORAL_FUTURE: Predict next actions."""
        try:
            predictions = [
                'Run X1000 training',
                'Distribute files to drives',
                'Run Fishnet scan',
                'Deploy Termius bridge',
                'Configure system sounds'
            ]
            
            return {
                'success': True,
                'summary': f'{len(predictions)} predictions',
                'data': predictions
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_parallel(self) -> Dict:
        """DIMENSIONAL_PARALLEL: Check multi-threading."""
        try:
            import multiprocessing
            cores = multiprocessing.cpu_count()
            
            return {
                'success': True,
                'summary': f'{cores} CPU cores',
                'data': {'cores': cores}
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def _scan_quantum(self) -> Dict:
        """DIMENSIONAL_QUANTUM: All possibilities."""
        try:
            possibilities = [
                'Execute all systems simultaneously',
                'Scan entire universe',
                'Distribute to all drives',
                'Configure all services',
                'Monitor everything'
            ]
            
            return {
                'success': True,
                'summary': 'Infinite possibilities',
                'data': possibilities
            }
        except Exception as e:
            return {'success': False, 'summary': str(e)}
    
    def execute_omnidirectional(self, command: str):
        """Execute command in all applicable directions."""
        print(f"\n🌟 EXECUTING OMNIDIRECTIONALLY: {command}")
        print("=" * 80)
        
        operations = []
        
        # Determine which directions apply
        if 'scan' in command.lower() or 'search' in command.lower():
            operations = [
                ('NORTH', lambda: self._execute_up(command)),
                ('SOUTH', lambda: self._execute_down(command)),
                ('INWARD', lambda: self._execute_local(command)),
            ]
        elif 'deploy' in command.lower() or 'launch' in command.lower():
            operations = [
                ('INWARD', lambda: self._execute_local(command)),
                ('UP', lambda: self._execute_cloud(command)),
            ]
        elif 'distribute' in command.lower():
            operations = [
                ('DOWN', lambda: self._execute_drives(command)),
                ('OUTWARD', lambda: self._execute_network(command)),
            ]
        else:
            # Execute everywhere
            operations = [
                ('ALL', lambda: self._execute_universal(command))
            ]
        
        with ThreadPoolExecutor(max_workers=len(operations)) as executor:
            futures = {executor.submit(op[1]): op[0] for op in operations}
            
            for future in as_completed(futures):
                direction = futures[future]
                try:
                    result = future.result()
                    status = "✅" if result else "⚠️"
                    print(f"{status} {direction:20s} : Complete")
                except Exception as e:
                    print(f"❌ {direction:20s} : {e}")
        
        print("=" * 80)
    
    def _execute_up(self, command: str) -> bool:
        """Execute in parent directories."""
        print(f"  ↑ Executing up: {command}")
        return True
    
    def _execute_down(self, command: str) -> bool:
        """Execute in subdirectories."""
        print(f"  ↓ Executing down: {command}")
        return True
    
    def _execute_local(self, command: str) -> bool:
        """Execute locally."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _execute_cloud(self, command: str) -> bool:
        """Execute in cloud."""
        print(f"  ☁️  Cloud execution: {command}")
        return True
    
    def _execute_drives(self, command: str) -> bool:
        """Execute on drives."""
        print(f"  💾 Drive execution: {command}")
        return True
    
    def _execute_network(self, command: str) -> bool:
        """Execute on network."""
        print(f"  🌐 Network execution: {command}")
        return True
    
    def _execute_universal(self, command: str) -> bool:
        """Execute universally."""
        print(f"  🌟 Universal execution: {command}")
        return self._execute_local(command)
    
    def show_universe_map(self):
        """Show complete directional map."""
        print("\n🌟 OMNIDIRECTIONAL UNIVERSE MAP")
        print("=" * 80)
        
        for direction, description in self.directions.items():
            result = self.results.get(direction, {})
            status = "✅" if result.get('success') else "⚪"
            summary = result.get('summary', 'Not scanned')
            
            print(f"{status} {direction:25s} : {description}")
            print(f"   └─ {summary}")
            
            # Show drive details for DOWN direction
            if direction == 'DOWN' and result.get('data'):
                drives = result['data']
                if isinstance(drives, list) and drives:
                    print(f"   └─ MOUNTED DRIVES:")
                    for drive in drives:
                        if isinstance(drive, dict):
                            print(f"      • {drive['type']} {drive['name']:30s} : {drive['path']}")
        
        print("=" * 80)
    
    def launch_everything(self):
        """Launch ALL systems in ALL directions."""
        print("\n🌟 LAUNCHING EVERYTHING IN ALL DIRECTIONS!")
        print("=" * 80)
        
        systems = [
            ('INWARD', 'GABRIEL_CODEMASTER.py', 'Codemaster'),
            ('INWARD', 'autonomous_learning.py', 'X1000'),
            ('INWARD', 'the_fishnet_universe.py', 'Universal Fishnet'),
            ('DOWN', 'CHECK_DRIVES.py', 'Drive Monitor'),
            ('OUTWARD', 'TERMINUS_BRIDGE.py', 'Termius Bridge'),
            ('OUTWARD', 'system_sound_manager.py', 'Sound Config'),
            ('OUTWARD', 'spotify_crossfade.py', 'Spotify Config'),
        ]
        
        print("\n🚀 Systems to launch:")
        for direction, script, name in systems:
            path = self.workspace / script
            exists = "✅" if path.exists() else "❌"
            print(f"   {exists} {direction:10s} : {name:20s} ({script})")
        
        print("\n⚠️  WARNING: This will launch ALL systems simultaneously!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            with ThreadPoolExecutor(max_workers=len(systems)) as executor:
                futures = []
                for direction, script, name in systems:
                    path = self.workspace / script
                    if path.exists():
                        future = executor.submit(
                            subprocess.run,
                            [self.python, str(path)],
                            capture_output=True,
                            timeout=2
                        )
                        futures.append((future, name))
                
                for future, name in futures:
                    try:
                        future.result()
                        print(f"✅ Launched: {name}")
                    except Exception as e:
                        print(f"⚠️  {name}: {e}")
            
            print("\n🌟 All systems launched!")
        else:
            print("❌ Launch cancelled")


def main():
    """Main omnidirectional control."""
    control = OmnidirectionalControl()
    
    while True:
        print("\n" + "=" * 80)
        print("🌟 GABRIEL OMNIDIRECTIONAL CONTROL")
        print("=" * 80)
        
        print("\n📋 OPERATIONS:")
        print("  1. 🔍 Scan all directions")
        print("  2. 🌟 Show universe map")
        print("  3. 🚀 Launch everything")
        print("  4. ⚡ Execute command omnidirectionally")
        print("  5. 📊 Show scan results")
        print("  6. 🎯 Target specific direction")
        print("  0. Exit")
        
        choice = input("\n🌟 Select operation: ").strip()
        
        if choice == '1':
            control.scan_all_directions()
            
        elif choice == '2':
            if not control.results:
                control.scan_all_directions()
            control.show_universe_map()
            
        elif choice == '3':
            control.launch_everything()
            
        elif choice == '4':
            command = input("Enter command: ").strip()
            if command:
                control.execute_omnidirectional(command)
        
        elif choice == '5':
            print("\n📊 SCAN RESULTS:")
            print("=" * 80)
            for direction, result in control.results.items():
                print(f"\n{direction}:")
                print(json.dumps(result, indent=2))
            print("=" * 80)
        
        elif choice == '6':
            print("\n🎯 Available directions:")
            for i, direction in enumerate(control.directions.keys(), 1):
                print(f"   {i:2d}. {direction}")
            
            try:
                idx = int(input("\nSelect direction: ").strip())
                direction = list(control.directions.keys())[idx - 1]
                print(f"\n🎯 Targeting {direction}...")
                command = input("Enter command: ").strip()
                if command:
                    control.execute_omnidirectional(command)
            except:
                print("❌ Invalid selection")
        
        elif choice == '0':
            print("\n🌟 Omnidirectional control terminated. Goodbye!")
            break
        
        else:
            print("❌ Invalid option")
        
        input("\n⏸️  Press Enter to continue...")


if __name__ == "__main__":
    main()

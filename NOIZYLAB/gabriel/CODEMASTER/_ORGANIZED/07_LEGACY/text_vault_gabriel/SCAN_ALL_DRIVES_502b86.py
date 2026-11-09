#!/usr/bin/env python3
"""
💾 PERMANENT DRIVE SCANNER - GABRIEL
Scans EVERY SINGLE mounted drive (local AND network)
PERMANENT RULE: Always scan ALL drives, no exceptions!
"""

import subprocess
import os
from pathlib import Path
from typing import List, Dict
import json

class UniversalDriveScanner:
    """
    💾 Scans ALL mounted drives - LOCAL AND NETWORK
    PERMANENT RULE: NO DRIVE LEFT BEHIND!
    """
    
    def __init__(self):
        self.drives = []
        self.workspace = Path.cwd()
        
        print("\n" + "=" * 80)
        print("💾 UNIVERSAL DRIVE SCANNER - PERMANENT RULE ACTIVATED")
        print("   Scanning EVERY SINGLE mounted drive (LOCAL + NETWORK)")
        print("=" * 80)
    
    def scan_all_drives(self) -> List[Dict]:
        """Scan ALL mounted drives - PERMANENT RULE."""
        print("\n🔍 SCANNING ALL DRIVES (LOCAL + NETWORK)...")
        print("-" * 80)
        
        all_drives = []
        
        # Method 1: macOS /Volumes directory
        self._scan_volumes_directory(all_drives)
        
        # Method 2: df command (all mounted filesystems)
        self._scan_df_output(all_drives)
        
        # Method 3: mount command
        self._scan_mount_output(all_drives)
        
        # Remove duplicates based on mount point
        unique_drives = {}
        for drive in all_drives:
            mount_point = drive['path']
            if mount_point not in unique_drives:
                unique_drives[mount_point] = drive
        
        self.drives = list(unique_drives.values())
        
        print("-" * 80)
        print(f"✅ Found {len(self.drives)} total mounted drives")
        print("=" * 80)
        
        return self.drives
    
    def _scan_volumes_directory(self, all_drives: List[Dict]):
        """Scan /Volumes directory."""
        print("\n📂 Scanning /Volumes directory...")
        
        volumes_path = Path('/Volumes')
        if not volumes_path.exists():
            print("⚠️  /Volumes not found")
            return
        
        try:
            for volume in volumes_path.iterdir():
                if not volume.is_dir() or volume.name.startswith('.'):
                    continue
                
                try:
                    # Get drive info from df
                    result = subprocess.run(['df', '-h', str(volume)],
                                          capture_output=True, text=True, check=False)
                    
                    drive_info = {
                        'name': volume.name,
                        'path': str(volume),
                        'accessible': volume.exists(),
                        'source': 'volumes'
                    }
                    
                    if result.returncode == 0 and len(result.stdout.split('\n')) > 1:
                        line = result.stdout.split('\n')[1]
                        parts = line.split()
                        
                        if parts:
                            filesystem = parts[0]
                            
                            # Determine type
                            if any(x in filesystem.lower() for x in ['smb', 'afp', 'nfs', '//']):
                                drive_info['type'] = '🌐 NETWORK'
                            elif 'disk' in filesystem.lower():
                                drive_info['type'] = '💾 LOCAL'
                            else:
                                drive_info['type'] = '❓ UNKNOWN'
                            
                            if len(parts) >= 6:
                                drive_info['size'] = parts[1]
                                drive_info['used'] = parts[2]
                                drive_info['available'] = parts[3]
                                drive_info['capacity'] = parts[4]
                            
                            drive_info['filesystem'] = filesystem
                    else:
                        drive_info['type'] = '❓ UNKNOWN'
                    
                    all_drives.append(drive_info)
                    print(f"   ✅ {drive_info.get('type', '❓')} {volume.name}")
                    
                except Exception as e:
                    print(f"   ⚠️  Error scanning {volume.name}: {e}")
        
        except Exception as e:
            print(f"❌ Error accessing /Volumes: {e}")
    
    def _scan_df_output(self, all_drives: List[Dict]):
        """Scan df output for all mounted filesystems."""
        print("\n📊 Scanning df output...")
        
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                print("⚠️  df command failed")
                return
            
            lines = result.stdout.split('\n')[1:]  # Skip header
            
            for line in lines:
                if not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) < 6:
                    continue
                
                filesystem = parts[0]
                mount_point = parts[-1]
                
                # Skip system mounts
                if mount_point in ['/', '/System', '/private', '/dev', '/home']:
                    continue
                
                # Check if it's a network mount
                is_network = any(x in filesystem.lower() for x in ['smb', 'afp', 'nfs', 'cifs', '//'])
                is_network = is_network or any(x in line.lower() for x in ['smb', 'afp', 'nfs', 'cifs'])
                
                drive_info = {
                    'name': Path(mount_point).name or mount_point,
                    'path': mount_point,
                    'filesystem': filesystem,
                    'type': '🌐 NETWORK' if is_network else '💾 LOCAL',
                    'size': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'capacity': parts[4],
                    'accessible': True,
                    'source': 'df'
                }
                
                # Check if not already added
                if not any(d['path'] == mount_point for d in all_drives):
                    all_drives.append(drive_info)
                    print(f"   ✅ {drive_info['type']} {drive_info['name']} @ {mount_point}")
        
        except Exception as e:
            print(f"❌ Error parsing df: {e}")
    
    def _scan_mount_output(self, all_drives: List[Dict]):
        """Scan mount command output."""
        print("\n🔧 Scanning mount output...")
        
        try:
            result = subprocess.run(['mount'], capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                print("⚠️  mount command failed")
                return
            
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue
                
                # Parse mount output: device on mountpoint (type)
                if ' on ' not in line:
                    continue
                
                parts = line.split(' on ')
                if len(parts) < 2:
                    continue
                
                device = parts[0]
                rest = parts[1]
                
                # Extract mount point and type
                if '(' in rest:
                    mount_point = rest.split('(')[0].strip()
                    mount_type = rest.split('(')[1].split(')')[0] if ')' in rest else ''
                else:
                    mount_point = rest.strip()
                    mount_type = ''
                
                # Check if network
                is_network = any(x in mount_type.lower() for x in ['smb', 'afp', 'nfs', 'cifs'])
                is_network = is_network or any(x in device.lower() for x in ['smb', 'afp', 'nfs', '//'])
                
                # Skip system mounts
                if mount_point in ['/', '/System', '/private', '/dev', '/home']:
                    continue
                
                drive_info = {
                    'name': Path(mount_point).name or mount_point,
                    'path': mount_point,
                    'device': device,
                    'mount_type': mount_type,
                    'type': '🌐 NETWORK' if is_network else '💾 LOCAL',
                    'accessible': Path(mount_point).exists(),
                    'source': 'mount'
                }
                
                # Check if not already added
                if not any(d['path'] == mount_point for d in all_drives):
                    all_drives.append(drive_info)
                    print(f"   ✅ {drive_info['type']} {drive_info['name']} @ {mount_point}")
        
        except Exception as e:
            print(f"❌ Error parsing mount: {e}")
    
    def show_all_drives(self):
        """Display all found drives."""
        print("\n" + "=" * 80)
        print("💾 ALL MOUNTED DRIVES (LOCAL + NETWORK)")
        print("=" * 80)
        
        if not self.drives:
            print("❌ No drives found. Run scan_all_drives() first.")
            return
        
        # Group by type
        local_drives = [d for d in self.drives if 'LOCAL' in d.get('type', '')]
        network_drives = [d for d in self.drives if 'NETWORK' in d.get('type', '')]
        unknown_drives = [d for d in self.drives if 'UNKNOWN' in d.get('type', '')]
        
        print(f"\n💾 LOCAL DRIVES ({len(local_drives)}):")
        print("-" * 80)
        for drive in local_drives:
            self._print_drive_details(drive)
        
        print(f"\n🌐 NETWORK DRIVES ({len(network_drives)}):")
        print("-" * 80)
        for drive in network_drives:
            self._print_drive_details(drive)
        
        if unknown_drives:
            print(f"\n❓ UNKNOWN DRIVES ({len(unknown_drives)}):")
            print("-" * 80)
            for drive in unknown_drives:
                self._print_drive_details(drive)
        
        print("\n" + "=" * 80)
        print(f"📊 TOTAL: {len(self.drives)} drives")
        print(f"   • {len(local_drives)} local")
        print(f"   • {len(network_drives)} network")
        if unknown_drives:
            print(f"   • {len(unknown_drives)} unknown")
        print("=" * 80)
    
    def _print_drive_details(self, drive: Dict):
        """Print detailed drive information."""
        status = "✅" if drive.get('accessible') else "❌"
        print(f"\n{status} {drive['name']}")
        print(f"   Path:       {drive['path']}")
        
        if 'filesystem' in drive:
            print(f"   Filesystem: {drive['filesystem']}")
        if 'device' in drive:
            print(f"   Device:     {drive['device']}")
        if 'mount_type' in drive:
            print(f"   Mount Type: {drive['mount_type']}")
        
        if 'size' in drive:
            print(f"   Size:       {drive['size']}")
            print(f"   Used:       {drive['used']}")
            print(f"   Available:  {drive['available']}")
            print(f"   Capacity:   {drive['capacity']}")
    
    def export_drives(self, filename: str = "ALL_DRIVES.json"):
        """Export drive list to JSON."""
        output_path = self.workspace / filename
        
        with open(output_path, 'w') as f:
            json.dump(self.drives, f, indent=2)
        
        print(f"\n💾 Exported drive list to: {output_path}")
        return output_path
    
    def get_drive_by_name(self, name: str) -> Dict:
        """Get drive info by name."""
        for drive in self.drives:
            if drive['name'].lower() == name.lower():
                return drive
        return None
    
    def get_network_drives(self) -> List[Dict]:
        """Get only network drives."""
        return [d for d in self.drives if 'NETWORK' in d.get('type', '')]
    
    def get_local_drives(self) -> List[Dict]:
        """Get only local drives."""
        return [d for d in self.drives if 'LOCAL' in d.get('type', '')]


def main():
    """Main drive scanning."""
    scanner = UniversalDriveScanner()
    
    while True:
        print("\n" + "=" * 80)
        print("💾 UNIVERSAL DRIVE SCANNER - PERMANENT RULE")
        print("=" * 80)
        
        print("\n📋 OPTIONS:")
        print("  1. 🔍 Scan ALL drives (LOCAL + NETWORK)")
        print("  2. 📊 Show all drives")
        print("  3. 💾 Show local drives only")
        print("  4. 🌐 Show network drives only")
        print("  5. 💾 Export drive list to JSON")
        print("  6. 🔎 Find specific drive")
        print("  7. 📈 Show statistics")
        print("  0. Exit")
        
        choice = input("\n💾 Select option: ").strip()
        
        if choice == '1':
            scanner.scan_all_drives()
            scanner.show_all_drives()
            
        elif choice == '2':
            if not scanner.drives:
                scanner.scan_all_drives()
            scanner.show_all_drives()
            
        elif choice == '3':
            if not scanner.drives:
                scanner.scan_all_drives()
            local = scanner.get_local_drives()
            print(f"\n💾 LOCAL DRIVES ({len(local)}):")
            for drive in local:
                print(f"   • {drive['name']:30s} : {drive['path']}")
            
        elif choice == '4':
            if not scanner.drives:
                scanner.scan_all_drives()
            network = scanner.get_network_drives()
            print(f"\n🌐 NETWORK DRIVES ({len(network)}):")
            for drive in network:
                print(f"   • {drive['name']:30s} : {drive['path']}")
            
        elif choice == '5':
            if not scanner.drives:
                scanner.scan_all_drives()
            scanner.export_drives()
            
        elif choice == '6':
            if not scanner.drives:
                scanner.scan_all_drives()
            name = input("Enter drive name: ").strip()
            drive = scanner.get_drive_by_name(name)
            if drive:
                scanner._print_drive_details(drive)
            else:
                print(f"❌ Drive '{name}' not found")
        
        elif choice == '7':
            if not scanner.drives:
                scanner.scan_all_drives()
            
            local = scanner.get_local_drives()
            network = scanner.get_network_drives()
            
            print("\n📈 DRIVE STATISTICS:")
            print("=" * 80)
            print(f"Total Drives:    {len(scanner.drives)}")
            print(f"Local Drives:    {len(local)}")
            print(f"Network Drives:  {len(network)}")
            print(f"Accessible:      {sum(1 for d in scanner.drives if d.get('accessible'))}")
            print("=" * 80)
            
        elif choice == '0':
            print("\n👋 Drive scanner terminated. Goodbye!")
            break
        
        else:
            print("❌ Invalid option")
        
        input("\n⏸️  Press Enter to continue...")


if __name__ == "__main__":
    main()

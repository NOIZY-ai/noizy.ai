#!/usr/bin/env python3
"""
🌌 THE FISHNET - MC96ECOUNIVERSE EDITION
Scan for hidden code across ALL connected devices, drives, and networks
"""

import re
from pathlib import Path
from typing import List, Dict
import json
import subprocess

class UniversalFishnet:
    """Scan entire MC96ECOUNIVERSE for hidden code and patterns."""
    
    def __init__(self):
        self.root_path = Path.cwd()
        self.catches = []
        self.devices = []
        self.patterns = {
            'hidden_functions': r'def\s+_+[a-z_]+\s*\(',
            'easter_eggs': r'(easter|secret|hidden|surprise|unlock|treasure)',
            'todo_bombs': r'(TODO|FIXME|HACK|XXX|BUG|OPTIMIZE|IMPORTANT)',
            'dead_code': r'(if\s+False:|if\s+0:|#\s*DISABLED|#\s*COMMENTED)',
            'magic_numbers': r'\b(420|1337|666|777|9999|42|69|8008135)\b',
            'commented_code': r'^\s*#\s*(def|class|import|from|for|while|if)',
            'debug_prints': r'print\s*\(["\']?(DEBUG|TEST|XXX)',
            'api_keys': r'(api_key|secret_key|password|token|auth)\s*=\s*["\'][^"\']{8,}["\']',
            'backdoors': r'(backdoor|admin_override|master_key|bypass|sudo_mode)',
            'experimental': r'(EXPERIMENTAL|BETA|ALPHA|WIP|PROTOTYPE|UNSTABLE)',
            'disabled_features': r'(DISABLED|DEPRECATED|OBSOLETE|LEGACY|ABANDONED)',
            'hidden_imports': r'import\s+(_[a-z_]+|\.[a-z_]+)',
            'lambda_chains': r'lambda.*:.*lambda',
            'eval_danger': r'(eval|exec|compile)\s*\(',
            'file_operations': r'(os\.remove|shutil\.rmtree|unlink|delete)\s*\(',
            'system_calls': r'(subprocess|os\.system|shell=True|popen)',
            'network_calls': r'(requests\.|urllib\.|socket\.|http\.|ftp)',
            'database_ops': r'(cursor\.execute|db\.|sql|query|SELECT|INSERT)',
            'crypto_ops': r'(encrypt|decrypt|hash|cipher|crypto|aes|rsa)',
            'ai_models': r'(gpt|claude|llama|openai|anthropic|model|agent|inference)',
            'x1000_refs': r'(X1000|INFINITY|GABRIEL|NOIZY|HYPER)',
            'drive_ops': r'(12TB|RED DRAGON|GABRIEL_MOUNT|/Volumes|mount|unmount)',
            'portal_refs': r'(PORTAL|MC96|CODEBEAST|UNIVERSE)',
            'autonomous': r'(autonomous|self_learning|adaptive|cognitive|neural)',
            'hyper_advanced': r'(hyper|quantum|neural|cognitive|singularity)',
            'fishnet_refs': r'(fishnet|NoizyFish|catch|scan|discover)',
            'audio_ops': r'(spotify|audio|music|sound|wav|mp3|aiff)',
            'class_definitions': r'class\s+[A-Z][a-zA-Z0-9_]*',
            'async_ops': r'(async|await|asyncio|thread|parallel)',
            'generator_funcs': r'def\s+\w+.*yield',
            'decorators': r'@\w+',
            'comprehensions': r'\[.*for.*in.*\]',
            'context_managers': r'with\s+\w+.*as\s+\w+:',
            'error_handling': r'(try:|except|raise|assert)',
            'logging': r'(logging\.|logger\.|log\.)',
            'config_files': r'(config|settings|\.env|\.ini|\.yaml|\.json)',
            'version_control': r'(git|commit|branch|merge|pull|push)',
            'docker_k8s': r'(docker|kubernetes|container|pod|deploy)',
            'cloud_services': r'(aws|azure|gcp|s3|lambda|cloud)',
            'timestamps': r'(datetime|timestamp|now\(\)|time\.)',
            'regex_patterns': r'r["\'].*[\[\\^$.*+?{}()].*["\']',
            'url_patterns': r'https?://[^\s\'"]+',
            'email_patterns': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'ip_addresses': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'mac_addresses': r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b'
        }
    
    def discover_universe(self):
        """Discover all connected devices in MC96ECOUNIVERSE."""
        print("\n🌌 DISCOVERING MC96ECOUNIVERSE...")
        print("=" * 80)
        
        devices = []
        
        # 1. Local workspace
        devices.append({
            'name': 'GABRIEL_WORKSPACE',
            'path': self.root_path,
            'type': 'local',
            'status': '✅ ONLINE'
        })
        
        # 2. Mounted volumes
        volumes_path = Path('/Volumes')
        if volumes_path.exists():
            for volume in volumes_path.iterdir():
                if volume.is_dir() and not volume.name.startswith('.'):
                    devices.append({
                        'name': volume.name,
                        'path': volume,
                        'type': 'volume',
                        'status': '✅ MOUNTED'
                    })
        
        # 3. Home directory
        home_path = Path.home()
        devices.append({
            'name': 'HOME_DIRECTORY',
            'path': home_path,
            'type': 'local',
            'status': '✅ ONLINE'
        })
        
        # 4. Desktop
        desktop_path = home_path / 'Desktop'
        if desktop_path.exists():
            devices.append({
                'name': 'DESKTOP',
                'path': desktop_path,
                'type': 'local',
                'status': '✅ ONLINE'
            })
        
        # 5. Documents
        docs_path = home_path / 'Documents'
        if docs_path.exists():
            devices.append({
                'name': 'DOCUMENTS',
                'path': docs_path,
                'type': 'local',
                'status': '✅ ONLINE'
            })
        
        # 6. Check for network drives
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                for line in result.stdout.split('\n')[1:]:
                    if '//' in line or 'smb' in line.lower():
                        parts = line.split()
                        if parts:
                            devices.append({
                                'name': f'NETWORK_{len(devices)}',
                                'path': Path(parts[-1]) if parts else None,
                                'type': 'network',
                                'status': '✅ CONNECTED'
                            })
        except Exception:
            pass
        
        self.devices = devices
        
        print(f"\n📡 DISCOVERED {len(devices)} DEVICES:")
        print("-" * 80)
        for i, device in enumerate(devices, 1):
            print(f"{i:2d}. {device['status']} {device['name']:30s} ({device['type']})")
            print(f"     📁 {device['path']}")
        print("=" * 80)
        
        return devices
    
    def cast_universal_net(self, selected_devices: List[int] = None):
        """Cast fishnet across selected devices."""
        if not self.devices:
            self.discover_universe()
        
        devices_to_scan = self.devices
        if selected_devices:
            devices_to_scan = [self.devices[i-1] for i in selected_devices if 0 < i <= len(self.devices)]
        
        print(f"\n🎣 CASTING NET ACROSS {len(devices_to_scan)} DEVICES...")
        print("=" * 80)
        
        total_files = 0
        
        for device in devices_to_scan:
            print(f"\n🔍 Scanning: {device['name']}")
            try:
                files = self._scan_device(device)
                total_files += files
                print(f"   ✅ Scanned {files} files")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n📊 TOTAL: Scanned {total_files} files across {len(devices_to_scan)} devices")
        print(f"🎯 Found {len(self.catches)} interesting patterns")
        print("=" * 80)
        
        return self.catches
    
    def _scan_device(self, device: Dict) -> int:
        """Scan a single device."""
        path = device['path']
        if not path or not path.exists():
            return 0
        
        files_scanned = 0
        extensions = ['.py', '.js', '.sh', '.bash', '.zsh', '.json', '.yaml', '.yml', 
                     '.txt', '.md', '.rst', '.ini', '.cfg', '.conf']
        
        # Limit depth to avoid infinite recursion
        max_depth = 5
        
        for ext in extensions:
            try:
                for file_path in path.rglob(f"*{ext}"):
                    if self._should_skip(file_path, path):
                        continue
                    
                    # Check depth
                    try:
                        relative = file_path.relative_to(path)
                        if len(relative.parts) > max_depth:
                            continue
                    except ValueError:
                        continue
                    
                    files_scanned += 1
                    self._scan_file(file_path, device['name'])
                    
                    # Limit files per device to prevent overload
                    if files_scanned > 1000:
                        break
                
                if files_scanned > 1000:
                    break
            except Exception:
                continue
        
        return files_scanned
    
    def _should_skip(self, path: Path, root: Path) -> bool:
        """Skip certain directories and files."""
        skip_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'Library', 'Applications', 'System', '.Trash', 'Cache',
            '.cache', 'temp', 'tmp', 'build', 'dist'
        }
        
        try:
            relative = path.relative_to(root)
            return any(skip in relative.parts for skip in skip_dirs)
        except ValueError:
            return True
    
    def _scan_file(self, file_path: Path, device_name: str):
        """Scan a single file for patterns."""
        try:
            # Skip large files
            if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                return
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for pattern_name, pattern in self.patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                    
                    self.catches.append({
                        'device': device_name,
                        'file': str(file_path),
                        'line': line_num,
                        'pattern': pattern_name,
                        'match': match.group(0),
                        'context': context[:150]
                    })
        
        except Exception:
            pass
    
    def analyze_universe(self) -> Dict:
        """Analyze catches across entire universe."""
        print("\n🌌 ANALYZING MC96ECOUNIVERSE DATA...")
        print("=" * 80)
        
        # By pattern
        by_pattern = {}
        for catch in self.catches:
            pattern = catch['pattern']
            if pattern not in by_pattern:
                by_pattern[pattern] = []
            by_pattern[pattern].append(catch)
        
        # By device
        by_device = {}
        for catch in self.catches:
            device = catch['device']
            if device not in by_device:
                by_device[device] = []
            by_device[device].append(catch)
        
        print("\n📈 TOP PATTERNS (Universe-wide):")
        print("-" * 80)
        sorted_patterns = sorted(by_pattern.items(), key=lambda x: len(x[1]), reverse=True)
        for pattern, items in sorted_patterns[:15]:
            print(f"  {pattern:30s} : {len(items):5d} occurrences")
        
        print("\n📡 PATTERNS BY DEVICE:")
        print("-" * 80)
        sorted_devices = sorted(by_device.items(), key=lambda x: len(x[1]), reverse=True)
        for device, items in sorted_devices:
            print(f"  {device:30s} : {len(items):5d} patterns")
        
        print("=" * 80)
        
        return {
            'by_pattern': by_pattern,
            'by_device': by_device
        }
    
    def find_universe_gems(self) -> List[Dict]:
        """Find most interesting patterns across universe."""
        print("\n💎 UNIVERSE GEMS (Cross-device discoveries):")
        print("=" * 80)
        
        gems = []
        
        priority_patterns = [
            'easter_eggs', 'backdoors', 'hidden_functions', 'experimental',
            'magic_numbers', 'x1000_refs', 'portal_refs', 'fishnet_refs',
            'ai_models', 'crypto_ops'
        ]
        
        for pattern in priority_patterns:
            matches = [c for c in self.catches if c['pattern'] == pattern]
            if matches:
                # Get unique devices
                devices = set(m['device'] for m in matches)
                if len(devices) > 1:
                    gems.extend(matches[:3])  # Cross-device gems
                else:
                    gems.extend(matches[:2])  # Single device gems
        
        for i, gem in enumerate(gems[:30], 1):
            print(f"\n{i:2d}. 🎯 {gem['pattern'].upper()} @ {gem['device']}")
            print(f"     📁 {gem['file']}:{gem['line']}")
            print(f"     💬 {gem['context']}")
        
        print("=" * 80)
        
        return gems
    
    def export_universe_map(self, filename: str = "MC96ECOUNIVERSE_MAP.json"):
        """Export complete universe map."""
        universe_map = {
            'total_devices': len(self.devices),
            'total_catches': len(self.catches),
            'devices': [
                {
                    'name': d['name'],
                    'type': d['type'],
                    'status': d['status'],
                    'path': str(d['path']),
                    'pattern_count': len([c for c in self.catches if c['device'] == d['name']])
                }
                for d in self.devices
            ],
            'patterns': {},
            'catches': self.catches[:10000]  # Limit to first 10k
        }
        
        for catch in self.catches:
            pattern = catch['pattern']
            if pattern not in universe_map['patterns']:
                universe_map['patterns'][pattern] = 0
            universe_map['patterns'][pattern] += 1
        
        output_path = self.root_path / filename
        with open(output_path, 'w') as f:
            json.dump(universe_map, f, indent=2)
        
        print(f"\n💾 Universe map saved to: {output_path}")
        print(f"📊 {len(self.catches)} catches across {len(self.devices)} devices")
        
        return output_path


def main():
    """Main universe scan."""
    print("\n" + "=" * 80)
    print("🌌 THE FISHNET - MC96ECOUNIVERSE EDITION")
    print("   Scan for hidden code across ALL connected devices")
    print("=" * 80)
    
    fishnet = UniversalFishnet()
    
    print("\n📋 MISSION OPTIONS:")
    print("=" * 80)
    print("1. 🌌 Discover universe (scan all devices)")
    print("2. 🎣 Cast universal net (full scan)")
    print("3. 🎯 Select specific devices to scan")
    print("4. 💎 Find universe gems")
    print("5. 📊 Complete analysis + export map")
    print("6. 🔍 Quick scan (local workspace only)")
    print("0. Exit")
    print()
    
    choice = input("Select mission: ").strip()
    
    if choice == '1':
        fishnet.discover_universe()
        
    elif choice == '2':
        fishnet.discover_universe()
        fishnet.cast_universal_net()
        fishnet.analyze_universe()
        fishnet.find_universe_gems()
        
    elif choice == '3':
        fishnet.discover_universe()
        print("\nEnter device numbers to scan (comma-separated, e.g., 1,2,5): ")
        selection = input().strip()
        try:
            selected = [int(x.strip()) for x in selection.split(',')]
            fishnet.cast_universal_net(selected)
            fishnet.analyze_universe()
            fishnet.find_universe_gems()
        except ValueError:
            print("❌ Invalid selection")
    
    elif choice == '4':
        fishnet.discover_universe()
        fishnet.cast_universal_net()
        fishnet.find_universe_gems()
        
    elif choice == '5':
        fishnet.discover_universe()
        fishnet.cast_universal_net()
        fishnet.analyze_universe()
        fishnet.find_universe_gems()
        fishnet.export_universe_map()
        
    elif choice == '6':
        fishnet.devices = [{
            'name': 'GABRIEL_WORKSPACE',
            'path': fishnet.root_path,
            'type': 'local',
            'status': '✅ ONLINE'
        }]
        fishnet.cast_universal_net([1])
        fishnet.analyze_universe()
    
    elif choice == '0':
        print("\n🌌 Universe scan complete!")
    
    else:
        print("\n❌ Invalid option")
    
    print("\n🎣 THE FISHNET mission complete!")


if __name__ == "__main__":
    main()

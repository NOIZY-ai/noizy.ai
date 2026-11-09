#!/usr/bin/env python3
"""
👑 GABRIEL - THE CODEMASTER
Supreme orchestrator of all systems, tools, and autonomous operations
Integrates: X1000, Fishnet, Drive Distribution, System Config, Terminal Management
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import re

class GabrielCodemaster:
    """
    👑 GABRIEL - The ultimate system orchestrator
    Controls all subsystems and automates the MC96ECOUNIVERSE
    """
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.systems = {}
        self.status = {
            'terminal': '❓ Unknown',
            'python': '❓ Unknown',
            'drives': '❓ Unknown',
            'fishnet': '❓ Ready',
            'x1000': '❓ Ready',
            'spotify': '❓ Unknown',
            'sounds': '❓ Unknown'
        }
        
        print("\n" + "=" * 80)
        print("👑 GABRIEL - THE CODEMASTER")
        print("   Supreme System Orchestrator")
        print("=" * 80)
    
    def diagnose_all(self):
        """Complete system diagnostic."""
        print("\n🔍 RUNNING COMPLETE SYSTEM DIAGNOSTIC...")
        print("=" * 80)
        
        self._check_terminal()
        self._check_python()
        self._check_drives()
        self._check_spotify()
        self._check_sounds()
        self._check_subsystems()
        
        print("\n📊 SYSTEM STATUS REPORT:")
        print("-" * 80)
        for system, status in self.status.items():
            print(f"  {system.upper():20s} : {status}")
        print("=" * 80)
    
    def _check_terminal(self):
        """Diagnose terminal configuration."""
        print("\n🖥️  TERMINAL DIAGNOSTIC:")
        print("-" * 80)
        
        # Check shell
        try:
            shell = os.environ.get('SHELL', 'unknown')
            print(f"  Current shell: {shell}")
            
            if Path(shell).exists():
                print(f"  ✅ Shell exists: {shell}")
                self.status['terminal'] = '✅ OK'
            else:
                print(f"  ❌ Shell not found: {shell}")
                self.status['terminal'] = '❌ ERROR'
                
                # Check common shell locations
                common_shells = [
                    '/bin/zsh',
                    '/bin/bash',
                    '/usr/bin/zsh',
                    '/usr/bin/bash',
                    '/usr/local/bin/zsh',
                    '/opt/homebrew/bin/zsh'
                ]
                
                print("\n  🔧 Available shells:")
                for shell_path in common_shells:
                    if Path(shell_path).exists():
                        print(f"     ✅ {shell_path}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.status['terminal'] = '❌ ERROR'
    
    def fix_terminal(self):
        """Fix terminal shell configuration."""
        print("\n🔧 FIXING TERMINAL CONFIGURATION...")
        print("=" * 80)
        
        shell = os.environ.get('SHELL', '/bin/zsh')
        
        if not Path(shell).exists():
            print("  ⚠️  Current shell not found, searching for alternatives...")
            
            # Find working shell
            common_shells = [
                '/bin/zsh',
                '/bin/bash',
                '/usr/bin/zsh',
                '/usr/bin/bash'
            ]
            
            working_shell = None
            for shell_path in common_shells:
                if Path(shell_path).exists():
                    working_shell = shell_path
                    print(f"  ✅ Found working shell: {shell_path}")
                    break
            
            if working_shell:
                print(f"\n  💡 To fix permanently, run:")
                print(f"     chsh -s {working_shell}")
                print(f"\n  Or update VS Code settings:")
                print(f"     \"terminal.integrated.shell.osx\": \"{working_shell}\"")
                
                # Create fix script
                fix_script = self.workspace / "FIX_TERMINAL.sh"
                with open(fix_script, 'w') as f:
                    f.write(f"""#!/bin/bash
# GABRIEL TERMINAL FIX SCRIPT

echo "🔧 Fixing terminal configuration..."

# Change default shell
echo "Changing default shell to {working_shell}..."
chsh -s {working_shell}

echo "✅ Shell changed! Restart your terminal."
echo ""
echo "For VS Code, add this to settings.json:"
echo '{{"terminal.integrated.shell.osx": "{working_shell}"}}'
""")
                
                os.chmod(fix_script, 0o755)
                print(f"\n  📝 Created fix script: {fix_script}")
                print(f"     Run: ./FIX_TERMINAL.sh")
            else:
                print("  ❌ No working shell found!")
        else:
            print("  ✅ Shell configuration is correct!")
    
    def _check_python(self):
        """Check Python environment."""
        print("\n🐍 PYTHON DIAGNOSTIC:")
        print("-" * 80)
        
        try:
            version = sys.version.split()[0]
            executable = sys.executable
            print(f"  Python version: {version}")
            print(f"  Python path: {executable}")
            
            if Path(executable).exists():
                print("  ✅ Python is accessible")
                self.status['python'] = '✅ OK'
            else:
                print("  ❌ Python path invalid")
                self.status['python'] = '❌ ERROR'
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.status['python'] = '❌ ERROR'
    
    def _check_drives(self):
        """Check connected drives."""
        print("\n💾 DRIVE DIAGNOSTIC:")
        print("-" * 80)
        
        volumes = Path('/Volumes')
        if volumes.exists():
            drives = [d.name for d in volumes.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            target_drives = ['12TB 1', '12TB', 'RED DRAGON']
            found_drives = [d for d in target_drives if d in drives]
            
            print(f"  Found {len(drives)} mounted volumes")
            for drive in found_drives:
                print(f"  ✅ {drive}")
            
            if len(found_drives) >= 2:
                self.status['drives'] = '✅ OK'
            elif len(found_drives) >= 1:
                self.status['drives'] = '⚠️  PARTIAL'
            else:
                self.status['drives'] = '❌ NONE'
        else:
            print("  ❌ Cannot access /Volumes")
            self.status['drives'] = '❌ ERROR'
    
    def _check_spotify(self):
        """Check Spotify."""
        print("\n🎵 SPOTIFY DIAGNOSTIC:")
        print("-" * 80)
        
        spotify_app = Path("/Applications/Spotify.app")
        if spotify_app.exists():
            print("  ✅ Spotify installed")
            
            # Check if running
            try:
                result = subprocess.run(['pgrep', '-x', 'Spotify'], 
                                      capture_output=True, check=False)
                if result.returncode == 0:
                    print("  ✅ Spotify is running")
                    self.status['spotify'] = '✅ RUNNING'
                else:
                    print("  ⚪ Spotify not running")
                    self.status['spotify'] = '⚪ INSTALLED'
            except Exception:
                self.status['spotify'] = '⚪ INSTALLED'
        else:
            print("  ❌ Spotify not installed")
            self.status['spotify'] = '❌ NOT FOUND'
    
    def _check_sounds(self):
        """Check system sound configuration."""
        print("\n🔊 SYSTEM SOUNDS DIAGNOSTIC:")
        print("-" * 80)
        
        try:
            result = subprocess.run([
                'defaults', 'read', 'NSGlobalDomain', 'com.apple.sound.beep.sound'
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                sound = Path(result.stdout.strip()).stem
                print(f"  Current alert sound: {sound}")
                
                if sound in ['Tink', 'Morse', 'Pop', 'Purr']:
                    print("  ✅ Soft sound configured")
                    self.status['sounds'] = '✅ QUIET'
                else:
                    print("  ⚠️  Default/loud sound")
                    self.status['sounds'] = '⚠️  DEFAULT'
            else:
                print("  ⚪ Default sound")
                self.status['sounds'] = '⚪ DEFAULT'
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.status['sounds'] = '❌ ERROR'
    
    def _check_subsystems(self):
        """Check all GABRIEL subsystems."""
        print("\n🔧 SUBSYSTEM CHECK:")
        print("-" * 80)
        
        subsystems = {
            'autonomous_learning.py': 'X1000 Autonomous Learning',
            'the_fishnet.py': 'Fishnet Code Scanner',
            'the_fishnet_universe.py': 'Universal Fishnet',
            'distribute_to_drives.py': 'Drive Distribution',
            'QUICK_DISTRIBUTE.py': 'Quick Distribution',
            'CHECK_DRIVES.py': 'Drive Monitor',
            'system_sound_manager.py': 'Sound Manager',
            'spotify_crossfade.py': 'Spotify Manager',
            'organize_12tb.py': '12TB Organizer'
        }
        
        for filename, name in subsystems.items():
            filepath = self.workspace / filename
            if filepath.exists():
                print(f"  ✅ {name:30s} @ {filename}")
                self.systems[name] = filepath
            else:
                print(f"  ⚪ {name:30s} (not found)")
    
    def launch_subsystem(self, name: str):
        """Launch a subsystem."""
        if name in self.systems:
            filepath = self.systems[name]
            print(f"\n🚀 Launching {name}...")
            print(f"   File: {filepath}")
            
            try:
                subprocess.run([sys.executable, str(filepath)])
            except KeyboardInterrupt:
                print("\n⏸️  Subsystem stopped")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print(f"❌ Subsystem '{name}' not found")
    
    def run_fishnet(self, scope: str = 'local'):
        """Run fishnet scan."""
        print(f"\n🎣 Running Fishnet ({scope})...")
        
        if scope == 'universe':
            script = self.workspace / 'the_fishnet_universe.py'
        else:
            script = self.workspace / 'the_fishnet.py'
        
        if script.exists():
            try:
                subprocess.run([sys.executable, str(script)])
            except KeyboardInterrupt:
                print("\n⏸️  Fishnet stopped")
        else:
            print(f"❌ Fishnet script not found: {script}")
    
    def distribute_drives(self, mode: str = 'check'):
        """Manage drive distribution."""
        print(f"\n💾 Drive Distribution ({mode})...")
        
        if mode == 'check':
            script = self.workspace / 'CHECK_DRIVES.py'
        elif mode == 'quick':
            script = self.workspace / 'QUICK_DISTRIBUTE.py'
        else:
            script = self.workspace / 'distribute_to_drives.py'
        
        if script.exists():
            try:
                subprocess.run([sys.executable, str(script)])
            except KeyboardInterrupt:
                print("\n⏸️  Distribution stopped")
        else:
            print(f"❌ Distribution script not found: {script}")
    
    def configure_sounds(self):
        """Configure system sounds."""
        print("\n🔊 Configuring system sounds...")
        
        script = self.workspace / 'system_sound_manager.py'
        if script.exists():
            try:
                subprocess.run([sys.executable, str(script)])
            except KeyboardInterrupt:
                print("\n⏸️  Configuration cancelled")
        else:
            print(f"❌ Sound manager not found")
    
    def configure_spotify(self):
        """Configure Spotify."""
        print("\n🎵 Configuring Spotify...")
        
        script = self.workspace / 'spotify_crossfade.py'
        if script.exists():
            try:
                subprocess.run([sys.executable, str(script)])
            except KeyboardInterrupt:
                print("\n⏸️  Configuration cancelled")
        else:
            print(f"❌ Spotify manager not found")
    
    def launch_x1000(self):
        """Launch X1000 Autonomous Learning."""
        print("\n🚀 Launching X1000 Autonomous Learning System...")
        
        script = self.workspace / 'autonomous_learning.py'
        if script.exists():
            try:
                subprocess.run([sys.executable, str(script)])
            except KeyboardInterrupt:
                print("\n⏸️  X1000 stopped")
        else:
            print(f"❌ X1000 not found")
    
    def show_dashboard(self):
        """Show GABRIEL command dashboard."""
        print("\n" + "=" * 80)
        print("👑 GABRIEL CODEMASTER - COMMAND CENTER")
        print("=" * 80)
        
        print("\n🔍 DIAGNOSTICS:")
        print("  1. Full system diagnostic")
        print("  2. Fix terminal configuration")
        
        print("\n🎣 FISHNET OPERATIONS:")
        print("  3. Run Fishnet (local scan)")
        print("  4. Run Fishnet Universe (all devices)")
        
        print("\n💾 DRIVE OPERATIONS:")
        print("  5. Check drives")
        print("  6. Quick distribute")
        print("  7. Full distribution")
        
        print("\n🎵 SYSTEM CONFIGURATION:")
        print("  8. Configure system sounds")
        print("  9. Configure Spotify crossfade")
        
        print("\n🚀 AUTONOMOUS SYSTEMS:")
        print(" 10. Launch X1000 Autonomous Learning")
        
        print("\n📊 UTILITIES:")
        print(" 11. Show all subsystems")
        print(" 12. System status")
        
        print("\n  0. Exit")
        print("=" * 80)
    
    def command_loop(self):
        """Main command loop."""
        while True:
            self.show_dashboard()
            
            try:
                choice = input("\n👑 GABRIEL Command: ").strip()
                
                if choice == '1':
                    self.diagnose_all()
                elif choice == '2':
                    self.fix_terminal()
                elif choice == '3':
                    self.run_fishnet('local')
                elif choice == '4':
                    self.run_fishnet('universe')
                elif choice == '5':
                    self.distribute_drives('check')
                elif choice == '6':
                    self.distribute_drives('quick')
                elif choice == '7':
                    self.distribute_drives('full')
                elif choice == '8':
                    self.configure_sounds()
                elif choice == '9':
                    self.configure_spotify()
                elif choice == '10':
                    self.launch_x1000()
                elif choice == '11':
                    self._check_subsystems()
                elif choice == '12':
                    for system, status in self.status.items():
                        print(f"  {system.upper():20s} : {status}")
                elif choice == '0':
                    print("\n👑 GABRIEL signing off. All systems standing by.")
                    break
                else:
                    print("❌ Invalid command")
                
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👑 GABRIEL signing off. All systems standing by.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\n⏸️  Press Enter to continue...")


def main():
    """Launch GABRIEL Codemaster."""
    gabriel = GabrielCodemaster()
    
    # Quick diagnostic on startup
    print("\n🔍 Running startup diagnostic...")
    gabriel.diagnose_all()
    
    input("\n⏸️  Press Enter to open Command Center...")
    
    # Enter command loop
    gabriel.command_loop()


if __name__ == "__main__":
    main()

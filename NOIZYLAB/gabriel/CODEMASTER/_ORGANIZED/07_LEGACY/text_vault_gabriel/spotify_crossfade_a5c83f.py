#!/usr/bin/env python3
"""
🎵 GABRIEL INFINITY - Spotify Crossfade Manager
Enable smooth crossfading between songs
"""

import subprocess
import json
import os
from pathlib import Path

class SpotifyCrossfadeManager:
    """Manage Spotify crossfade settings."""
    
    def __init__(self):
        self.prefs_path = Path.home() / "Library/Application Support/Spotify/prefs"
    
    def set_crossfade(self, duration: int = 5):
        """
        Set Spotify crossfade duration.
        
        Args:
            duration: Crossfade duration in seconds (0-12)
        """
        if not 0 <= duration <= 12:
            print("❌ Duration must be between 0 and 12 seconds")
            return False
        
        print(f"\n🎵 Setting Spotify crossfade to {duration} seconds...")
        
        # Check if Spotify is installed
        spotify_path = Path("/Applications/Spotify.app")
        if not spotify_path.exists():
            print("❌ Spotify not found in /Applications/")
            return False
        
        # Check if Spotify is running
        is_running = self._is_spotify_running()
        
        if is_running:
            print("⚠️  Spotify is currently running")
            print("   Crossfade can be set in: Spotify > Settings > Playback > Crossfade")
            print("\n   Or close Spotify and run this again to set it automatically.")
            self._open_spotify_settings()
            return False
        
        # Modify prefs file
        if self.prefs_path.exists():
            try:
                with open(self.prefs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update or add crossfade setting
                if 'audio.crossfade_v2' in content:
                    # Replace existing setting
                    import re
                    content = re.sub(
                        r'audio\.crossfade_v2=\d+',
                        f'audio.crossfade_v2={duration}',
                        content
                    )
                else:
                    # Add new setting
                    content += f'\naudio.crossfade_v2={duration}'
                
                with open(self.prefs_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Crossfade set to {duration} seconds")
                print("   Restart Spotify to apply changes")
                return True
                
            except Exception as e:
                print(f"❌ Error modifying prefs: {e}")
                return False
        else:
            print("⚠️  Spotify preferences file not found")
            print("   Open Spotify once to create preferences, then run again")
            return False
    
    def _is_spotify_running(self):
        """Check if Spotify is currently running."""
        try:
            result = subprocess.run(
                ['pgrep', '-x', 'Spotify'],
                capture_output=True,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _open_spotify_settings(self):
        """Open Spotify settings via AppleScript."""
        try:
            # Just open Spotify preferences
            subprocess.run([
                'open', '-a', 'Spotify',
                '--args', '--show-settings'
            ], check=False)
            print("\n💡 Opening Spotify settings...")
            print("   Navigate to: Playback > Crossfade songs")
        except Exception:
            pass
    
    def get_current_crossfade(self):
        """Get current crossfade setting."""
        if not self.prefs_path.exists():
            return None
        
        try:
            with open(self.prefs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            match = re.search(r'audio\.crossfade_v2=(\d+)', content)
            if match:
                return int(match.group(1))
            return 0
        except Exception:
            return None
    
    def show_status(self):
        """Show current Spotify crossfade status."""
        print("\n📊 SPOTIFY CROSSFADE STATUS:")
        print("=" * 60)
        
        # Check if Spotify installed
        if not Path("/Applications/Spotify.app").exists():
            print("❌ Spotify not installed")
            return
        
        print("✅ Spotify installed")
        
        # Check if running
        if self._is_spotify_running():
            print("✅ Spotify is running")
        else:
            print("⚪ Spotify is not running")
        
        # Get crossfade setting
        crossfade = self.get_current_crossfade()
        if crossfade is not None:
            if crossfade > 0:
                print(f"✅ Crossfade: {crossfade} seconds")
            else:
                print("⚪ Crossfade: Disabled (0 seconds)")
        else:
            print("⚪ Crossfade: Not configured")
        
        print("=" * 60)


def main():
    """Main menu."""
    manager = SpotifyCrossfadeManager()
    
    print("\n" + "=" * 60)
    print("🎵 GABRIEL INFINITY - SPOTIFY CROSSFADE MANAGER")
    print("=" * 60)
    
    manager.show_status()
    
    print("\n📋 OPTIONS:")
    print("=" * 60)
    print("1. 🎵 Enable Crossfade (5 seconds) - RECOMMENDED")
    print("2. 🎵 Enable Crossfade (3 seconds) - Subtle")
    print("3. 🎵 Enable Crossfade (8 seconds) - Smooth")
    print("4. 🎵 Enable Crossfade (12 seconds) - Maximum")
    print("5. 🎵 Custom duration")
    print("6. 🔇 Disable Crossfade")
    print("7. 📊 Show current status")
    print("8. ⚙️  Open Spotify settings manually")
    print("0. Exit")
    print()
    
    choice = input("Select option: ").strip()
    
    if choice == '1':
        manager.set_crossfade(5)
    elif choice == '2':
        manager.set_crossfade(3)
    elif choice == '3':
        manager.set_crossfade(8)
    elif choice == '4':
        manager.set_crossfade(12)
    elif choice == '5':
        try:
            duration = int(input("Enter duration (0-12 seconds): "))
            manager.set_crossfade(duration)
        except ValueError:
            print("❌ Invalid duration")
    elif choice == '6':
        manager.set_crossfade(0)
    elif choice == '7':
        manager.show_status()
    elif choice == '8':
        manager._open_spotify_settings()
    elif choice == '0':
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid option")


if __name__ == "__main__":
    main()

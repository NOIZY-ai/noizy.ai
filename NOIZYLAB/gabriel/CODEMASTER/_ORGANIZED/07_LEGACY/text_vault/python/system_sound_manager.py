#!/usr/bin/env python3
"""
🔊 GABRIEL INFINITY - System Sound Manager
Change system sounds from negative beeps to pleasant clicks
"""

import subprocess
import os
from pathlib import Path

class SystemSoundManager:
    """Manage macOS system sounds."""
    
    def __init__(self):
        self.sounds_dir = Path("/System/Library/Sounds")
        self.available_sounds = self._get_available_sounds()
    
    def _get_available_sounds(self):
        """Get list of available system sounds."""
        sounds = {
            'Tink': 'High-pitched click (recommended)',
            'Morse': 'Soft single beep',
            'Pop': 'Bubble pop sound',
            'Purr': 'Gentle vibration',
            'Ping': 'Soft ping',
            'Frog': 'Subtle ribbit',
            'Submarine': 'Sonar beep',
            'Blow': 'Soft whoosh',
            'Bottle': 'Cork pop'
        }
        return sounds
    
    def set_alert_sound(self, sound_name: str):
        """Set the system alert sound."""
        sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
        
        if not Path(sound_path).exists():
            print(f"❌ Sound '{sound_name}' not found")
            return False
        
        try:
            subprocess.run([
                'defaults', 'write', 'NSGlobalDomain',
                'com.apple.sound.beep.sound', '-string', sound_path
            ], check=True)
            print(f"✅ Alert sound changed to: {sound_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to set sound")
            return False
    
    def set_volume(self, volume: float):
        """Set alert volume (0.0 to 1.0)."""
        try:
            subprocess.run([
                'defaults', 'write', 'NSGlobalDomain',
                'com.apple.sound.beep.volume', '-float', str(volume)
            ], check=True)
            print(f"✅ Alert volume set to: {volume * 100:.0f}%")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to set volume")
            return False
    
    def disable_ui_sounds(self):
        """Disable UI feedback sounds."""
        try:
            subprocess.run([
                'defaults', 'write', 'NSGlobalDomain',
                'com.apple.sound.uiaudio.enabled', '-int', '0'
            ], check=True)
            print("✅ UI feedback sounds disabled")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to disable UI sounds")
            return False
    
    def enable_ui_sounds(self):
        """Enable UI feedback sounds."""
        try:
            subprocess.run([
                'defaults', 'write', 'NSGlobalDomain',
                'com.apple.sound.uiaudio.enabled', '-int', '1'
            ], check=True)
            print("✅ UI feedback sounds enabled")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to enable UI sounds")
            return False
    
    def apply_quiet_profile(self):
        """Apply quiet/minimal sound profile."""
        print("\n🔇 Applying QUIET profile...")
        self.set_alert_sound('Tink')
        self.set_volume(0.1)
        self.disable_ui_sounds()
        self.restart_ui()
        print("\n✅ Quiet profile applied!")
    
    def apply_silent_profile(self):
        """Apply completely silent profile."""
        print("\n🔇 Applying SILENT profile...")
        self.set_alert_sound('Tink')
        self.set_volume(0.0)
        self.disable_ui_sounds()
        self.restart_ui()
        print("\n✅ Silent profile applied!")
    
    def apply_default_profile(self):
        """Restore default sounds."""
        print("\n🔊 Restoring DEFAULT profile...")
        try:
            subprocess.run(['defaults', 'delete', 'NSGlobalDomain', 
                          'com.apple.sound.beep.volume'], check=False)
            subprocess.run(['defaults', 'delete', 'NSGlobalDomain', 
                          'com.apple.sound.uiaudio.enabled'], check=False)
            subprocess.run(['defaults', 'delete', 'NSGlobalDomain', 
                          'com.apple.sound.beep.sound'], check=False)
            self.restart_ui()
            print("\n✅ Default profile restored!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def restart_ui(self):
        """Restart SystemUIServer to apply changes."""
        try:
            subprocess.run(['killall', 'SystemUIServer'], 
                         stderr=subprocess.DEVNULL, check=False)
            print("🔄 UI restarted to apply changes")
        except Exception:
            pass
    
    def show_current_settings(self):
        """Display current sound settings."""
        print("\n📊 CURRENT SOUND SETTINGS:")
        print("=" * 50)
        
        # Get alert sound
        try:
            result = subprocess.run([
                'defaults', 'read', 'NSGlobalDomain',
                'com.apple.sound.beep.sound'
            ], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                sound = Path(result.stdout.strip()).stem
                print(f"Alert Sound: {sound}")
            else:
                print("Alert Sound: Default (Funk)")
        except Exception:
            print("Alert Sound: Unknown")
        
        # Get volume
        try:
            result = subprocess.run([
                'defaults', 'read', 'NSGlobalDomain',
                'com.apple.sound.beep.volume'
            ], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                volume = float(result.stdout.strip())
                print(f"Alert Volume: {volume * 100:.0f}%")
            else:
                print("Alert Volume: Default (100%)")
        except Exception:
            print("Alert Volume: Unknown")
        
        # Get UI sounds
        try:
            result = subprocess.run([
                'defaults', 'read', 'NSGlobalDomain',
                'com.apple.sound.uiaudio.enabled'
            ], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                enabled = result.stdout.strip() == '1'
                print(f"UI Sounds: {'Enabled' if enabled else 'Disabled'}")
            else:
                print("UI Sounds: Default (Enabled)")
        except Exception:
            print("UI Sounds: Unknown")
        
        print("=" * 50)


def main():
    """Main menu."""
    manager = SystemSoundManager()
    
    print("\n" + "=" * 60)
    print("🔊 GABRIEL INFINITY - SYSTEM SOUND MANAGER")
    print("=" * 60)
    
    manager.show_current_settings()
    
    print("\n📋 QUICK PROFILES:")
    print("=" * 60)
    print("1. 🔇 QUIET      - Soft click, low volume (RECOMMENDED)")
    print("2. 🔇 SILENT     - No sounds at all")
    print("3. 🔊 DEFAULT    - Restore original macOS sounds")
    print()
    print("📋 CUSTOM OPTIONS:")
    print("=" * 60)
    print("4. Choose specific sound")
    print("5. Set custom volume")
    print("6. Toggle UI sounds")
    print("7. Show current settings")
    print("0. Exit")
    print()
    
    choice = input("Select option: ").strip()
    
    if choice == '1':
        manager.apply_quiet_profile()
        print("\n💡 Your Enter key will now make a soft click sound!")
        
    elif choice == '2':
        manager.apply_silent_profile()
        print("\n💡 All system sounds disabled!")
        
    elif choice == '3':
        confirm = input("\nRestore default sounds? (y/n): ").lower()
        if confirm == 'y':
            manager.apply_default_profile()
    
    elif choice == '4':
        print("\n🎵 AVAILABLE SOUNDS:")
        print("=" * 60)
        for i, (name, desc) in enumerate(manager.available_sounds.items(), 1):
            print(f"{i}. {name:15s} - {desc}")
        print()
        
        try:
            sound_choice = int(input("Select sound number: "))
            sound_name = list(manager.available_sounds.keys())[sound_choice - 1]
            manager.set_alert_sound(sound_name)
            manager.restart_ui()
            print(f"\n✅ Sound changed! Press any invalid key to test.")
        except (ValueError, IndexError):
            print("❌ Invalid selection")
    
    elif choice == '5':
        try:
            volume = float(input("Enter volume (0.0 to 1.0): "))
            if 0 <= volume <= 1:
                manager.set_volume(volume)
                manager.restart_ui()
            else:
                print("❌ Volume must be between 0.0 and 1.0")
        except ValueError:
            print("❌ Invalid volume")
    
    elif choice == '6':
        toggle = input("Enable UI sounds? (y/n): ").lower()
        if toggle == 'y':
            manager.enable_ui_sounds()
        else:
            manager.disable_ui_sounds()
        manager.restart_ui()
    
    elif choice == '7':
        manager.show_current_settings()
    
    elif choice == '0':
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid option")


if __name__ == "__main__":
    main()

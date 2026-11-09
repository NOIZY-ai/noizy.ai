#!/usr/bin/env python3
"""
🚀 X1000 GRUNFREEX3000 EXECUTOR 🚀
===================================
Execute GRUNFREEX3000 migration with X1000 power
"""

import subprocess
import sys
from pathlib import Path

class X1000MigrationExecutor:
    """Execute GRUNFREEX3000 migrations"""
    
    def __init__(self):
        self.gabriel = Path("/Users/rsp_ms/GABRIEL")
        self.original_script = self.gabriel / "GRUNFREEX3000.sh"
        self.x1000_script = self.gabriel / "X1000_GRUNFREEX3000.sh"
        
    def make_executable(self, script_path):
        """Make script executable"""
        try:
            script_path.chmod(0o755)
            print(f"✅ Made executable: {script_path.name}")
            return True
        except Exception as e:
            print(f"❌ Failed to chmod: {e}")
            return False
    
    def show_commands(self):
        """Show execution commands"""
        
        print("🚀" * 40)
        print(" " * 15 + "X1000 GRUNFREEX3000 EXECUTOR")
        print("🚀" * 40)
        
        print("\n📋 STEP 1: MAKE SCRIPTS EXECUTABLE")
        print("=" * 80)
        print(f"chmod +x {self.original_script}")
        print(f"chmod +x {self.x1000_script}")
        
        print("\n📋 STEP 2: DRY RUN (TEST - SAFE!)")
        print("=" * 80)
        print("# Original version:")
        print(f"sudo {self.original_script} OLDUSERNAME NEWUSERNAME --dry-run")
        print("\n# X1000 Enhanced version:")
        print(f"sudo {self.x1000_script} OLDUSERNAME NEWUSERNAME --dry-run")
        
        print("\n📋 STEP 3: FULL MIGRATION (AFTER DRY RUN SUCCESS)")
        print("=" * 80)
        print("# Original version:")
        print(f"sudo {self.original_script} OLDUSERNAME NEWUSERNAME")
        print("\n# X1000 Enhanced version (RECOMMENDED):")
        print(f"sudo {self.x1000_script} OLDUSERNAME NEWUSERNAME")
        
        print("\n💡 REAL EXAMPLE:")
        print("=" * 80)
        print("# If migrating from 'rob' to 'rsp_ms':")
        print(f"\n1. Test first:")
        print(f"   sudo {self.x1000_script} rob rsp_ms --dry-run")
        print(f"\n2. Review output, then run full migration:")
        print(f"   sudo {self.x1000_script} rob rsp_ms")
        
        print("\n⚠️  IMPORTANT NOTES:")
        print("=" * 80)
        print("• Must run as root (sudo)")
        print("• Both users must already exist")
        print("• ALWAYS do dry-run first!")
        print("• Keep backup password safe")
        print("• Don't delete old user until verified")
        print("• Check migration report JSON")
        
        print("\n🎯 READY TO EXECUTE:")
        print("=" * 80)
        
    def auto_chmod(self):
        """Automatically make scripts executable"""
        print("\n🔧 Making scripts executable...")
        
        if self.original_script.exists():
            self.make_executable(self.original_script)
        else:
            print(f"⚠️  Original script not found: {self.original_script}")
        
        if self.x1000_script.exists():
            self.make_executable(self.x1000_script)
        else:
            print(f"⚠️  X1000 script not found: {self.x1000_script}")
        
        print("✅ Scripts ready to execute!")
    
    def interactive_menu(self):
        """Interactive execution menu"""
        
        print("\n" + "🚀" * 40)
        print(" " * 15 + "X1000 MIGRATION MENU")
        print("🚀" * 40)
        
        print("\n1. 🔧 Make scripts executable (chmod +x)")
        print("2. 🧪 Run dry-run test (X1000)")
        print("3. 🚀 Run full migration (X1000)")
        print("4. 📋 Show all commands")
        print("5. ❌ Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            self.auto_chmod()
            
        elif choice == "2":
            old_user = input("\nOld username: ").strip()
            new_user = input("New username: ").strip()
            
            if old_user and new_user:
                print(f"\n🧪 Running dry-run: {old_user} → {new_user}")
                print(f"\nCommand: sudo {self.x1000_script} {old_user} {new_user} --dry-run")
                print("\n⚠️  Copy and paste this command in terminal:")
                print(f"sudo {self.x1000_script} {old_user} {new_user} --dry-run")
            else:
                print("❌ Invalid usernames")
                
        elif choice == "3":
            old_user = input("\nOld username: ").strip()
            new_user = input("New username: ").strip()
            
            if old_user and new_user:
                print(f"\n⚠️  FULL MIGRATION: {old_user} → {new_user}")
                confirm = input("Type 'YES' to confirm: ").strip()
                
                if confirm == "YES":
                    print(f"\n🚀 Running migration...")
                    print(f"\n⚠️  Copy and paste this command in terminal:")
                    print(f"sudo {self.x1000_script} {old_user} {new_user}")
                else:
                    print("❌ Cancelled")
            else:
                print("❌ Invalid usernames")
                
        elif choice == "4":
            self.show_commands()
            
        elif choice == "5":
            print("👋 Goodbye!")
            return
            
        else:
            print("❌ Invalid choice")

def main():
    executor = X1000MigrationExecutor()
    
    print("🚀" * 40)
    print(" " * 10 + "X1000 GRUNFREEX3000 EXECUTOR")
    print("🚀" * 40)
    
    # Auto chmod
    executor.auto_chmod()
    
    # Show commands
    executor.show_commands()
    
    # Interactive menu
    print("\n" + "=" * 80)
    response = input("Show interactive menu? (y/n): ").strip().lower()
    if response == 'y':
        executor.interactive_menu()
    
    print("\n✨ X1000 MIGRATION READY! ✨")

if __name__ == '__main__':
    main()

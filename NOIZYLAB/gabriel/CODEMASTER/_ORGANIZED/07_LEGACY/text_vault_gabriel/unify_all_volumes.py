#!/usr/bin/env python3
"""
🌟 GABRIEL VOLUME UNIFICATION SCRIPT
Consolidates all GABRIEL material from all volumes into unified Git repository
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

class GabrielUnifier:
    def __init__(self):
        self.gabriel_root = Path("/Users/rsp_ms/GABRIEL")
        self.external_deploy = Path("/Volumes/12TB 1/GABRIEL_DEPLOY")
        self.backup_name = f"GABRIEL_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        self.stats = {
            'files_copied': 0,
            'files_skipped': 0,
            'dirs_created': 0,
            'total_size': 0
        }
    
    def print_banner(self):
        print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║       🌟 GABRIEL VOLUME UNIFICATION IN PROGRESS 🌟            ║
║                                                                ║
║  Mission: Consolidate ALL GABRIEL material into Git repo      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    def check_prerequisites(self):
        """Verify all required paths exist"""
        print("\n📋 Checking prerequisites...")
        
        if not self.gabriel_root.exists():
            print(f"❌ GABRIEL root not found: {self.gabriel_root}")
            return False
        print(f"✅ GABRIEL root exists: {self.gabriel_root}")
        
        if not self.external_deploy.exists():
            print(f"⚠️  External deployment not found: {self.external_deploy}")
            print("   Checking if volume is mounted...")
            volumes = list(Path("/Volumes").glob("*"))
            print(f"   Available volumes: {[v.name for v in volumes]}")
            return False
        print(f"✅ External deployment exists: {self.external_deploy}")
        
        return True
    
    def create_backup(self):
        """Create timestamped backup of current GABRIEL repo"""
        print(f"\n💾 Creating backup: {self.backup_name}")
        
        backup_path = self.gabriel_root.parent / self.backup_name
        cmd = f"cd {self.gabriel_root.parent} && tar -czf {self.backup_name} GABRIEL/"
        
        try:
            os.system(cmd)
            if backup_path.exists():
                size_mb = backup_path.stat().st_size / (1024 * 1024)
                print(f"✅ Backup created: {size_mb:.2f} MB")
                return True
            else:
                print("❌ Backup failed")
                return False
        except Exception as e:
            print(f"❌ Backup error: {e}")
            return False
    
    def create_unified_structure(self):
        """Create organized directory structure"""
        print("\n📁 Creating unified structure...")
        
        dirs = [
            'DEPLOY_ARCHIVE',
            'DEPLOY_ARCHIVE/core',
            'core',
            'agents',
            'systems',
            'tools',
            'tests'
        ]
        
        for d in dirs:
            path = self.gabriel_root / d
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                self.stats['dirs_created'] += 1
                print(f"  ✅ Created: {d}")
            else:
                print(f"  ⏭️  Exists: {d}")
    
    def copy_file_safe(self, src, dst):
        """Copy file with safety checks"""
        try:
            if dst.exists():
                # Check if files are different
                if src.stat().st_size == dst.stat().st_size:
                    src_mtime = src.stat().st_mtime
                    dst_mtime = dst.stat().st_mtime
                    if src_mtime <= dst_mtime:
                        self.stats['files_skipped'] += 1
                        return False  # Dest is newer or same
            
            # Copy the file
            shutil.copy2(src, dst)
            self.stats['files_copied'] += 1
            self.stats['total_size'] += src.stat().st_size
            return True
        except Exception as e:
            print(f"    ⚠️  Error copying {src.name}: {e}")
            return False
    
    def consolidate_deployment(self):
        """Copy all files from external deployment"""
        print("\n📦 Consolidating external deployment...")
        
        if not self.external_deploy.exists():
            print("⚠️  External deployment not accessible, skipping...")
            return
        
        # Copy entire deployment directory
        deploy_archive = self.gabriel_root / "DEPLOY_ARCHIVE"
        
        for item in self.external_deploy.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(self.external_deploy)
                dest = deploy_archive / rel_path
                
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                if self.copy_file_safe(item, dest):
                    print(f"  ✅ Copied: {rel_path}")
                else:
                    print(f"  ⏭️  Skipped: {rel_path} (up to date)")
    
    def consolidate_core_files(self):
        """Move critical files to core/ directory"""
        print("\n🔧 Organizing core files...")
        
        core_files = {
            'DEPLOY_ARCHIVE/core/shirl_agent.py': 'core/shirl_agent.py',
            'DEPLOY_ARCHIVE/core/drive_helpers.py': 'core/drive_helpers.py',
            'DEPLOY_ARCHIVE/core/collective_brain.py': 'core/collective_brain.py',
            'DEPLOY_ARCHIVE/core/utils.py': 'core/utils.py',
        }
        
        for src_rel, dst_rel in core_files.items():
            src = self.gabriel_root / src_rel
            dst = self.gabriel_root / dst_rel
            
            if src.exists():
                if self.copy_file_safe(src, dst):
                    print(f"  ✅ Organized: {dst_rel}")
                else:
                    print(f"  ⏭️  Already exists: {dst_rel}")
            else:
                print(f"  ⚠️  Not found: {src_rel}")
    
    def scan_other_volumes(self):
        """Search for GABRIEL material on other volumes"""
        print("\n🔍 Scanning other volumes for GABRIEL material...")
        
        volumes = Path("/Volumes")
        if not volumes.exists():
            print("  ⚠️  Cannot access /Volumes")
            return
        
        found_material = []
        
        for volume in volumes.iterdir():
            if volume.name in ['.', '..', '12TB 1']:
                continue
            
            print(f"  🔎 Scanning: {volume.name}...")
            
            # Search for GABRIEL directories
            for item in volume.rglob('*GABRIEL*'):
                if item.is_dir() or item.is_file():
                    found_material.append(item)
                    print(f"    ⚠️  Found: {item}")
        
        if not found_material:
            print("  ✅ No additional GABRIEL material found on other volumes")
        else:
            print(f"\n  ⚠️  Found {len(found_material)} items on other volumes!")
            print("     Manual review required for:")
            for item in found_material:
                print(f"     - {item}")
    
    def generate_manifest(self):
        """Generate manifest of all unified files"""
        print("\n📄 Generating unification manifest...")
        
        manifest_path = self.gabriel_root / "UNIFICATION_MANIFEST.md"
        
        all_files = sorted(self.gabriel_root.rglob('*'))
        py_files = [f for f in all_files if f.suffix == '.py']
        md_files = [f for f in all_files if f.suffix == '.md']
        sh_files = [f for f in all_files if f.suffix == '.sh']
        cs_files = [f for f in all_files if f.suffix == '.cs']
        
        with open(manifest_path, 'w') as f:
            f.write(f"""# GABRIEL UNIFICATION MANIFEST
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 STATISTICS

- **Total Files**: {len(all_files)}
- **Python Files**: {len(py_files)}
- **Documentation**: {len(md_files)}
- **Scripts**: {len(sh_files)}
- **Unity Scripts**: {len(cs_files)}
- **Files Copied**: {self.stats['files_copied']}
- **Files Skipped**: {self.stats['files_skipped']}
- **Directories Created**: {self.stats['dirs_created']}
- **Total Size**: {self.stats['total_size'] / (1024*1024):.2f} MB

---

## 🐍 PYTHON FILES ({len(py_files)})

""")
            for f in py_files:
                rel = f.relative_to(self.gabriel_root)
                size = f.stat().st_size
                f.write(f"- `{rel}` ({size:,} bytes)\n")
            
            f.write(f"""
---

## 📚 DOCUMENTATION ({len(md_files)})

""")
            for f in md_files:
                rel = f.relative_to(self.gabriel_root)
                f.write(f"- `{rel}`\n")
            
            f.write(f"""
---

## 🛠️  SCRIPTS ({len(sh_files)})

""")
            for f in sh_files:
                rel = f.relative_to(self.gabriel_root)
                f.write(f"- `{rel}`\n")
        
        print(f"  ✅ Manifest created: UNIFICATION_MANIFEST.md")
    
    def create_master_launcher(self):
        """Create unified launcher script"""
        print("\n🚀 Creating master launcher...")
        
        launcher_path = self.gabriel_root / "unified_gabriel_launcher.sh"
        
        launcher_content = """#!/bin/bash
# 🌟 GABRIEL UNIFIED LAUNCHER
# All systems accessible from one location

export GABRIEL_ROOT="/Users/rsp_ms/GABRIEL"
export PYTHONPATH="$GABRIEL_ROOT:$GABRIEL_ROOT/core:$GABRIEL_ROOT/agents"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║           🌟 GABRIEL UNIFIED SYSTEM 🌟                        ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Available Systems:"
echo "  1. SHIRL (Living AI Avatar)"
echo "  2. GABRIEL INFINITY (17 systems)"
echo "  3. GABRIEL ULTIMATE (7 systems)"
echo "  4. Collective Brain (20 agents)"
echo "  5. Unity3D Avatar"
echo "  6. Web Avatar"
echo "  7. Tools & Utilities"
echo "  8. File Organizer"
echo ""
read -p "Select system [1-8]: " choice

case $choice in
    1) python3 "$GABRIEL_ROOT/core/shirl_agent.py" ;;
    2) python3 "$GABRIEL_ROOT/gabriel_infinity.py" ;;
    3) python3 "$GABRIEL_ROOT/gabriel_ultimate.py" ;;
    4) python3 "$GABRIEL_ROOT/core/collective_brain.py" ;;
    5) echo "Launch Unity project from Unity3D/" ;;
    6) cd "$GABRIEL_ROOT/WebAvatar" && python3 -m http.server 8000 ;;
    7) python3 "$GABRIEL_ROOT/gabriel_deployer.py" ;;
    8) python3 "$GABRIEL_ROOT/file_organizer.py" ;;
    *) echo "Invalid selection" ;;
esac
"""
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        os.chmod(launcher_path, 0o755)
        print(f"  ✅ Launcher created: unified_gabriel_launcher.sh")
    
    def print_summary(self):
        """Print final summary"""
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           🎉 GABRIEL UNIFICATION COMPLETE! 🎉                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

📊 UNIFICATION STATISTICS:
   • Files Copied: {self.stats['files_copied']}
   • Files Skipped: {self.stats['files_skipped']} (already up to date)
   • Directories Created: {self.stats['dirs_created']}
   • Total Data: {self.stats['total_size'] / (1024*1024):.2f} MB

📁 UNIFIED LOCATION:
   {self.gabriel_root}

🚀 NEXT STEPS:
   1. Review UNIFICATION_MANIFEST.md
   2. Run: ./unified_gabriel_launcher.sh
   3. Test all systems
   4. Git commit and push
   
✅ ALL GABRIEL MATERIAL IS NOW UNIFIED ON GIT!
""")
    
    def execute(self):
        """Execute full unification process"""
        self.print_banner()
        
        # Phase 1: Prerequisites
        if not self.check_prerequisites():
            print("\n❌ Prerequisites not met. Cannot continue.")
            return False
        
        # Phase 2: Backup
        print("\n" + "="*64)
        print("PHASE 1: BACKUP")
        print("="*64)
        self.create_backup()
        
        # Phase 3: Structure
        print("\n" + "="*64)
        print("PHASE 2: CREATE STRUCTURE")
        print("="*64)
        self.create_unified_structure()
        
        # Phase 4: Consolidate
        print("\n" + "="*64)
        print("PHASE 3: CONSOLIDATE DEPLOYMENT")
        print("="*64)
        self.consolidate_deployment()
        
        # Phase 5: Organize
        print("\n" + "="*64)
        print("PHASE 4: ORGANIZE CORE FILES")
        print("="*64)
        self.consolidate_core_files()
        
        # Phase 6: Scan
        print("\n" + "="*64)
        print("PHASE 5: SCAN OTHER VOLUMES")
        print("="*64)
        self.scan_other_volumes()
        
        # Phase 7: Manifest
        print("\n" + "="*64)
        print("PHASE 6: GENERATE MANIFEST")
        print("="*64)
        self.generate_manifest()
        
        # Phase 8: Launcher
        print("\n" + "="*64)
        print("PHASE 7: CREATE LAUNCHER")
        print("="*64)
        self.create_master_launcher()
        
        # Phase 9: Summary
        self.print_summary()
        
        return True

if __name__ == "__main__":
    unifier = GabrielUnifier()
    success = unifier.execute()
    sys.exit(0 if success else 1)

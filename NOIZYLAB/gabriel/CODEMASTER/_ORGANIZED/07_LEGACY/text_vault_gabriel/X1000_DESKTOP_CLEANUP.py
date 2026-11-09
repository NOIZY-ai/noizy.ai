#!/usr/bin/env python3
"""
🚀 X1000 DESKTOP CLEANUP MASTER 🚀
===================================
Smart desktop organization with AI categorization
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class X1000DesktopCleaner:
    """AI-powered desktop cleanup system"""
    
    def __init__(self):
        self.desktop = Path("/Users/rsp_ms/Desktop")
        self.gabriel = Path("/Users/rsp_ms/GABRIEL")
        
        # Create organized folders
        self.categories = {
            "📁 Projects": [".xcodeproj", ".code-workspace", ".git"],
            "📄 Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".pages"],
            "🖼️ Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
            "🎵 Audio": [".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"],
            "🎬 Videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
            "📦 Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".dmg"],
            "💻 Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sh"],
            "📊 Data": [".json", ".csv", ".xml", ".yaml", ".yml", ".sql"],
            "🎨 Design": [".psd", ".ai", ".sketch", ".fig", ".blend"],
            "📱 Apps": [".app", ".pkg", ".dmg"],
        }
        
        self.stats = defaultdict(int)
        self.moved_files = []
        
    def analyze_desktop(self):
        """Analyze desktop contents"""
        print("🔍 ANALYZING DESKTOP...")
        print("=" * 80)
        print(f"📁 Desktop: {self.desktop}\n")
        
        if not self.desktop.exists():
            print("❌ Desktop not found!")
            return []
        
        items = []
        for item in self.desktop.iterdir():
            if item.name.startswith('.'):
                continue  # Skip hidden files
            
            info = {
                "path": item,
                "name": item.name,
                "is_dir": item.is_dir(),
                "size": 0,
                "modified": datetime.fromtimestamp(item.stat().st_mtime)
            }
            
            if item.is_file():
                info["size"] = item.stat().st_size
                info["ext"] = item.suffix.lower()
            
            items.append(info)
        
        # Sort by type and size
        dirs = [i for i in items if i["is_dir"]]
        files = [i for i in items if not i["is_dir"]]
        
        print(f"📊 Found:")
        print(f"   📁 Folders: {len(dirs)}")
        print(f"   📄 Files: {len(files)}")
        
        if files:
            total_size = sum(f["size"] for f in files)
            print(f"   💾 Total size: {total_size / 1024 / 1024:.2f} MB")
        
        return items
    
    def categorize_file(self, file_info):
        """Categorize file by extension"""
        ext = file_info.get("ext", "")
        
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        
        # Check for project folders
        if file_info["is_dir"]:
            # Check if it's a project
            path = file_info["path"]
            if any((path / marker).exists() for marker in [".git", "package.json", "requirements.txt"]):
                return "📁 Projects"
            return "📁 Folders"
        
        return "📋 Other"
    
    def create_organized_structure(self):
        """Create Desktop/Organized folder structure"""
        organized = self.desktop / "Organized"
        organized.mkdir(exist_ok=True)
        
        # Create category folders
        category_paths = {}
        for category in list(self.categories.keys()) + ["📁 Folders", "📋 Other"]:
            # Clean category name for folder
            folder_name = category.split(" ", 1)[1] if " " in category else category
            category_path = organized / folder_name
            category_path.mkdir(exist_ok=True)
            category_paths[category] = category_path
        
        return organized, category_paths
    
    def cleanup_desktop(self, dry_run=True):
        """Organize desktop files"""
        print("\n🚀 X1000 DESKTOP CLEANUP")
        print("=" * 80)
        print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'LIVE CLEANUP'}")
        print("=" * 80)
        
        # Analyze
        items = self.analyze_desktop()
        
        if not items:
            print("\n✅ Desktop is already clean!")
            return
        
        # Create structure
        organized, category_paths = self.create_organized_structure()
        
        # Categorize and organize
        print("\n📋 ORGANIZATION PLAN:")
        print("-" * 80)
        
        categorized = defaultdict(list)
        
        for item in items:
            # Skip the Organized folder itself
            if item["name"] == "Organized":
                continue
            
            # Skip certain important folders
            if item["name"] in ["GABRIEL", "CODEBEAST", "MissionControl96"]:
                print(f"   ⚠️  SKIP: {item['name']} (protected)")
                continue
            
            category = self.categorize_file(item)
            categorized[category].append(item)
        
        # Show plan
        for category, items_list in sorted(categorized.items()):
            print(f"\n{category} ({len(items_list)} items):")
            for item in items_list[:5]:  # Show first 5
                size_str = f"{item['size'] / 1024:.1f} KB" if not item['is_dir'] else "folder"
                print(f"   • {item['name']:50} {size_str:>15}")
            
            if len(items_list) > 5:
                print(f"   ... and {len(items_list) - 5} more")
        
        # Execute move
        if not dry_run:
            print("\n" + "=" * 80)
            print("🔄 EXECUTING CLEANUP...")
            print("=" * 80)
            
            for category, items_list in categorized.items():
                dest_folder = category_paths[category]
                
                for item in items_list:
                    try:
                        dest = dest_folder / item["name"]
                        
                        # Handle duplicates
                        if dest.exists():
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            name_parts = item["name"].rsplit(".", 1)
                            if len(name_parts) == 2:
                                new_name = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
                            else:
                                new_name = f"{item['name']}_{timestamp}"
                            dest = dest_folder / new_name
                        
                        shutil.move(str(item["path"]), str(dest))
                        print(f"✅ Moved: {item['name']} → {category}")
                        self.moved_files.append((item["name"], category))
                        self.stats[category] += 1
                        
                    except Exception as e:
                        print(f"❌ Error moving {item['name']}: {e}")
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 CLEANUP SUMMARY")
        print("=" * 80)
        
        if dry_run:
            total = sum(len(items) for items in categorized.values())
            print(f"\n📋 Would organize {total} items into {len(categorized)} categories")
            print(f"📁 Destination: {organized}")
            print("\n💡 To execute cleanup, run with: dry_run=False")
        else:
            print(f"\n✅ Organized {len(self.moved_files)} items")
            print(f"📁 Location: {organized}")
            
            for category, count in sorted(self.stats.items()):
                print(f"   {category}: {count} items")
        
        print("\n" + "=" * 80)
        
        return categorized
    
    def show_menu(self):
        """Interactive menu"""
        print("\n" + "🚀" * 40)
        print(" " * 20 + "X1000 DESKTOP CLEANUP")
        print("🚀" * 40)
        
        print("\n1. 🔍 Preview Cleanup (Dry Run)")
        print("2. 🧹 Execute Full Cleanup")
        print("3. 📊 Analyze Desktop Only")
        print("4. ❌ Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            print("\n🔍 PREVIEW MODE")
            self.cleanup_desktop(dry_run=True)
        elif choice == "2":
            print("\n⚠️  EXECUTING LIVE CLEANUP...")
            confirm = input("Type 'YES' to confirm: ").strip()
            if confirm == "YES":
                self.cleanup_desktop(dry_run=False)
                print("\n✨ Desktop cleaned!")
            else:
                print("❌ Cancelled")
        elif choice == "3":
            self.analyze_desktop()
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

def main():
    cleaner = X1000DesktopCleaner()
    cleaner.show_menu()

if __name__ == '__main__':
    main()

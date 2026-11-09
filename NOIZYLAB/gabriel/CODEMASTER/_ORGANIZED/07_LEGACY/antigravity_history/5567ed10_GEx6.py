import os
import shutil
import glob
from datetime import datetime

# --- CONFIGURATION ---
TARGET_DIRS = [
    "/Users/m2ultra/Documents",
    "/Users/m2ultra/Downloads",
    "/Users/m2ultra/Desktop",
    "/Users/m2ultra/NOIZYLAB"
]

# Destination for organized text files
TEXT_VAULT = "/Users/m2ultra/Documents/NOIZYLAB_TEXT_VAULT"

def organize_txt_files():
    print(f"📄 SCANNING TEXT FILES...")
    
    if not os.path.exists(TEXT_VAULT):
        os.makedirs(TEXT_VAULT)
        print(f"Created Vault: {TEXT_VAULT}")

    moved_count = 0
    
    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
            
        print(f"  🔍 Scanning: {target}")
        
        # Walk recursively to find ALL .txt files
        for root, dirs, files in os.walk(target):
            # Skip the vault itself to avoid loops
            if TEXT_VAULT in root:
                continue
                
            for file in files:
                if file.lower().endswith(".txt"):
                    source_path = os.path.join(root, file)
                    
                    # Create timestamped subfolder or category? 
                    # Let's keep it simple: Organized by Source Folder Name
                    source_folder_name = os.path.basename(root)
                    dest_folder = os.path.join(TEXT_VAULT, source_folder_name)
                    
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                        
                    dest_path = os.path.join(dest_folder, file)
                    
                    # Handle duplicates
                    if os.path.exists(dest_path):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest_path = os.path.join(dest_folder, f"{os.path.splitext(file)[0]}_{timestamp}.txt")

                    try:
                        shutil.move(source_path, dest_path)
                        # print(f"    Moved: {file}") # Be quiet unless error
                        moved_count += 1
                    except Exception as e:
                        print(f"    ❌ Failed: {file} - {e}")

    print(f"\n✨ COMPLETE. Moved {moved_count} text files to {TEXT_VAULT}")

if __name__ == "__main__":
    organize_txt_files()

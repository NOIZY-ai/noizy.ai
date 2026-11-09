import os
import shutil
import time

SOURCE_DIR = "/Volumes/4TB Blue Fish"
DEST_DIR = "/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/mined_code/4TB_Blue_Fish"
EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.scss', '.json', 
    '.sh', '.bash', '.zsh', '.c', '.cpp', '.h', '.hpp', '.go', '.rs', 
    '.java', '.kt', '.swift', '.php', '.rb', '.pl', '.md', '.xml', 
    '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.sql'
}

def turbo_copy():
    print(f"Starting TURBO scan in {SOURCE_DIR}...")
    count = 0
    start_time = time.time()
    
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for root, dirs, files in os.walk(SOURCE_DIR):
        # Skip hidden directories to speed up
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS:
                src_path = os.path.join(root, file)
                # Preserve directory structure
                rel_path = os.path.relpath(src_path, SOURCE_DIR)
                dest_path = os.path.join(DEST_DIR, rel_path)
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
                count += 1
                if count % 100 == 0:
                    print(f"Copied {count} files...")

    duration = time.time() - start_time
    print(f"TURBO COMPLETE. Copied {count} files in {duration:.2f} seconds.")

if __name__ == "__main__":
    turbo_copy()

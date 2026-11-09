import os
import json
from datetime import datetime

ROOT_DIR = "/Volumes/6TB/Sample_Libraries"
OUTPUT_DB = "/Users/m2ultra/.gemini/MC96_PROJECT_RECONSTRUCTION.json"
OUTPUT_MD = "/Users/m2ultra/.gemini/MC96_PROJECT_MAP.md"

project_extensions = {
    '.logic': 'Logic Pro',
    '.logicx': 'Logic Pro X',
    '.ptx': 'Pro Tools',
    '.pts': 'Pro Tools',
    '.als': 'Ableton Live',
    '.cpr': 'Cubase',
    '.rpp': 'Reaper',
    '.flp': 'FL Studio',
    '.npr': 'Nuendo'
}

projects = {}
assets_by_project = {}

print(f"🏗️ REBUILDING PROJECT DATA FROM: {ROOT_DIR}")

for root, dirs, files in os.walk(ROOT_DIR):
    # Determine "Project" name from the top-level directory after Root
    rel_path = os.path.relpath(root, ROOT_DIR)
    parts = rel_path.split(os.sep)
    project_name = parts[0] if parts[0] != '.' else "Root"
    
    if project_name not in assets_by_project:
        assets_by_project[project_name] = {"size": 0, "files": 0, "high_quality": 0, "projects_found": []}
    
    for file in files:
        path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        size = os.path.getsize(path)
        
        assets_by_project[project_name]["size"] += size
        assets_by_project[project_name]["files"] += 1
        
        # Check for Project Files
        if ext in project_extensions:
            projects[path] = project_extensions[ext]
            assets_by_project[project_name]["projects_found"].append(file)
            
        # Check for HQ Audio (Heuristic from previous scan would be better, but quick check here)
        if ext in ['.wav', '.aif', '.aiff']:
             assets_by_project[project_name]["high_quality"] += 1

# Generate Report
md_report = f"# 🏗️ MC96 PROJECT RECONSTRUCTION MAP\n**Source:** `{ROOT_DIR}`\n\n"

if projects:
    md_report += "## 🎛️ DAW PROJECTS DISCOVERED\n"
    for p, daw in projects.items():
        md_report += f"- **{daw}**: `{p}`\n"
else:
    md_report += "## 🎛️ DAW PROJECTS\n*No DAW project files (.logic, .ptx, etc.) found in this library volume.*\n"

md_report += "\n## 📂 ASSET GROUPS (RECONSTRUCTED PROJECTS)\n"
for proj, data in sorted(assets_by_project.items()):
    size_gb = data['size'] / (1024**3)
    md_report += f"### 📁 {proj}\n"
    md_report += f"- **Size:** {size_gb:.2f} GB\n"
    md_report += f"- **Files:** {data['files']:,}\n"
    md_report += f"- **Audio Assets:** {data['high_quality']:,}\n"
    if data['projects_found']:
        md_report += f"- **Project Files:** {', '.join(data['projects_found'])}\n"
    md_report += "\n"

with open(OUTPUT_MD, "w") as f:
    f.write(md_report)

with open(OUTPUT_DB, "w") as f:
    json.dump(assets_by_project, f, indent=2)

print(f"✅ RECONSTRUCTION COMPLETE")
print(f"📄 Map: {OUTPUT_MD}")

import json
import os
from collections import defaultdict

MEMCELL_DB = "/Users/m2ultra/.gemini/antigravity/brain/7ce086fd-9c9f-435a-9136-8deed85eaf0f/MEMCELL_LOG.jsonl"
OUTPUT_FILE = "/Users/m2ultra/.gemini/antigravity/brain/7ce086fd-9c9f-435a-9136-8deed85eaf0f/BRAIN_MAP.md"

def generate_brain_map():
    if not os.path.exists(MEMCELL_DB):
        print("No MemCell data found yet.")
        return

    subjects = defaultdict(list)
    overlap_graph = defaultdict(set)

    with open(MEMCELL_DB, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                subj = data.get('subject', 'Unknown')
                ovlp = data.get('overlap', 'None')
                subjects[subj].append(data)
                if ovlp != "None":
                    overlap_graph[subj].add(ovlp)
            except:
                continue

    with open(OUTPUT_FILE, 'w') as f:
        f.write("# GORUNFREE BRAIN MAP 🧠\n\n")
        f.write("> **Visualizing System Intelligence & Overlap**\n\n")
        
        f.write("## 🔗 Knowledge Graph (Overlap)\n")
        for subj, overlaps in overlap_graph.items():
            f.write(f"- **{subj}** connects to:\n")
            for ov in overlaps:
                f.write(f"  - 🔗 `{ov}`\n")
        f.write("\n")

        f.write("## 📚 Subject Matter Index\n")
        for subj, entries in subjects.items():
            f.write(f"### {subj}\n")
            for entry in entries:
                f.write(f"- `[{entry['timestamp']}]` ({entry['persona']}): {entry['overlap']}\n")
    
    print(f"Brain Map generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_brain_map()

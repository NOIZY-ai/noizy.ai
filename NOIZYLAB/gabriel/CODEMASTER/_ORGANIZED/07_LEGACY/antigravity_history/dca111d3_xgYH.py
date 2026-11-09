import json
import os

DB_PATH = "memcell_db.json"
BACKUP_PATH = "memcell_db_legacy_backup.json"

# Keyword mapping for "Intuitive Intelligence"
TOPIC_MAP = {
    "network": "Infrastructure",
    "mtu": "Infrastructure",
    "jumbo": "Infrastructure",
    "memcell": "AI Core",
    "memory": "AI Core",
    "brain": "AI Core",
    "voice": "Tactile System",
    "tactile": "Tactile System",
    "music": "Creative",
    "sound": "Creative",
    "prompt": "AI Config",
    "god mode": "God Mode",
    "zero latency": "God Mode"
}

SUBJECT_MAP = {
    "Infrastructure": "Hardware Optimization",
    "AI Core": "Memory Systems",
    "Tactile System": "Human Interface",
    "Creative": "Music Production",
    "AI Config": "System Alignment",
    "God Mode": "Performance Apex"
}

def optimize_db():
    print("⚡ STARTING RETROACTIVE INTELLIGENCE UPGRADE...")
    
    if not os.path.exists(DB_PATH):
        print("❌ No DB found.")
        return

    # Backup
    os.system(f"cp {DB_PATH} {BACKUP_PATH}")
    
    with open(DB_PATH, 'r') as f:
        db = json.load(f)
    
    upgraded_count = 0
    
    for mem in db:
        # Only upgrade if it looks like legacy/generic data
        current_subject = mem.get("subject", "")
        current_overlap = mem.get("overlap", [])
        content = mem.get("content", "").lower()
        topic = mem.get("topic", "General")
        
        is_legacy = current_subject == "Legacy Data" or current_subject == "General" or not current_overlap
        
        if is_legacy:
            # 1. Infer Topic/Category
            inferred_topic = "General"
            for key, val in TOPIC_MAP.items():
                if key in content:
                    inferred_topic = val
                    break
            
            # 2. Infer Subject
            inferred_subject = SUBJECT_MAP.get(inferred_topic, "General Knowledge")
            
            # 3. Infer Overlap
            inferred_overlap = []
            if inferred_topic != "General":
                inferred_overlap.append(inferred_topic)
            if "python" in content: inferred_overlap.append("Code")
            if "docs" in content: inferred_overlap.append("Documentation")
            
            # Apply Upgrades
            if current_subject == "Legacy Data" or current_subject == "General":
                mem["subject"] = inferred_subject
                mem["topic"] = inferred_topic if mem["topic"] == "General" else mem["topic"]
                upgraded_count += 1
                
            if not current_overlap and inferred_overlap:
                mem["overlap"] = inferred_overlap
                upgraded_count += 1 # Count activity, though logic might double count simple updates
                
            mem["author"] = mem.get("author", "SYSTEM_ARCHIVE")

    # Save
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)
        
    print(f"✅ UPGRADE COMPLETE. Optimized {upgraded_count} fields across memory database.")
    print("🧠 INTUITIVE INTELLIGENCE: MAXIMIZED.")

if __name__ == "__main__":
    optimize_db()

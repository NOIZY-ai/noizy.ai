#!/usr/bin/env python3
"""
TURBO_UNIFY: Create unified GABRIEL structure
Generates a move manifest for organizing all Gabriel code
"""

import json
from pathlib import Path
from datetime import datetime, timezone

# Configuration
ROOT = Path(".").resolve()
REPORTS = ROOT / "reports"
TARGET_BASE = Path("/Volumes/GABRIEL/MC96/GABRIEL_CORE/GABRIEL_UNIFIED")

# Module mappings
MODULE_PATTERNS = {
    "core": ["gabriel_core", "gabriel_m2", "gabriel_ultra", "gabriel_singularity", "app.py"],
    "cortex": ["genius", "brain", "think", "reason", "cognit"],
    "memcell": ["memory", "memcell", "memo", "store", "database"],
    "audio": ["audio", "voice", "tts", "speech", "sound", "music"],
    "swarm": ["swarm", "agent", "multi", "collab"],
    "network": ["network", "net_control", "socket", "websocket", "bridge"],
    "avatar": ["avatar", "face", "3d", "holograph", "interface.html", "ultra_v12"],
    "tools": ["tool", "heal", "dedupe", "doctor", "optimize", "indexer", "archaeo"],
    "configs": ["config", "setting", "env", ".sh", "run.sh", "requirements"],
    "docs": ["readme", "doc", "spec", "manifest", "report"],
    "tests": ["test", "spec.py", "_test.py"],
}

# Ignore patterns
IGNORE = {".git", "node_modules", ".venv", "venv", "dist", "build", ".next", "__pycache__", "reports", "_quarantine"}

def classify_file(filepath: str) -> str:
    """Determine which module a file belongs to"""
    lower = filepath.lower()
    
    for module, patterns in MODULE_PATTERNS.items():
        for pattern in patterns:
            if pattern in lower:
                return module
    
    # Default based on extension
    ext = Path(filepath).suffix.lower()
    if ext in [".py"]:
        return "core"
    elif ext in [".html", ".css"]:
        return "avatar"
    elif ext in [".js"]:
        return "avatar"
    elif ext in [".json", ".yaml", ".yml"]:
        return "configs"
    elif ext in [".md", ".txt"]:
        return "docs"
    elif ext in [".sh"]:
        return "configs"
    
    return "tools"  # Default bucket

def resolve_collision(target: Path, seen_targets: set) -> Path:
    """Resolve target path collision by adding _v2, _v3 suffix"""
    if str(target) not in seen_targets:
        return target
    
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    
    version = 2
    while True:
        new_target = parent / f"{stem}_v{version}{suffix}"
        if str(new_target) not in seen_targets:
            return new_target
        version += 1

def main():
    # Load manifest
    manifest_path = REPORTS / "repo_manifest.json"
    if not manifest_path.exists():
        print("❌ Run TURBO_HEAL first to generate repo_manifest.json")
        return
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    moves = []
    seen_targets = set()
    
    # Process only project files (not venv)
    for file_info in manifest["largest_files"]:
        filepath = file_info["path"]
        
        # Skip virtual environments and large binaries
        if any(x in filepath for x in IGNORE):
            continue
        if file_info.get("ext", "") in [".so", ".dylib", ".woff2", ".npz", ".dat"]:
            continue
        
        # Only process Python, HTML, JS, CSS, JSON, YAML, MD, SH files
        ext = file_info.get("ext", "").lower()
        if ext not in [".py", ".html", ".js", ".css", ".json", ".yaml", ".yml", ".md", ".txt", ".sh"]:
            continue
        
        # Classify and create target path
        module = classify_file(filepath)
        filename = Path(filepath).name
        target = TARGET_BASE / module / filename
        
        # Resolve collisions
        target = resolve_collision(target, seen_targets)
        seen_targets.add(str(target))
        
        moves.append({
            "from": str(ROOT / filepath),
            "to": str(target),
            "action": "copy",  # Use copy to be safe
            "module": module
        })
    
    # Also scan current directory for Gabriel files
    gabriel_patterns = ["gabriel", "turbo", "memcell", "cortex"]
    for p in ROOT.glob("*"):
        if not p.is_file():
            continue
        if any(x in p.name.lower() for x in gabriel_patterns):
            if p.suffix.lower() in [".py", ".html", ".sh"]:
                module = classify_file(str(p))
                target = TARGET_BASE / module / p.name
                target = resolve_collision(target, seen_targets)
                seen_targets.add(str(target))
                
                if str(p) not in [m["from"] for m in moves]:
                    moves.append({
                        "from": str(p),
                        "to": str(target),
                        "action": "copy",
                        "module": module
                    })
    
    # Scan GABRIEL_V1
    gabriel_v1 = ROOT / "GABRIEL_V1"
    if gabriel_v1.exists():
        for p in gabriel_v1.rglob("*"):
            if not p.is_file():
                continue
            if any(x in str(p) for x in IGNORE):
                continue
            if p.suffix.lower() in [".py", ".html", ".sh", ".txt"]:
                module = classify_file(str(p))
                target = TARGET_BASE / module / p.name
                target = resolve_collision(target, seen_targets)
                seen_targets.add(str(target))
                
                if str(p) not in [m["from"] for m in moves]:
                    moves.append({
                        "from": str(p),
                        "to": str(target),
                        "action": "copy",
                        "module": module
                    })
    
    # Generate output
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target_base": str(TARGET_BASE),
        "modules": list(MODULE_PATTERNS.keys()),
        "total_moves": len(moves),
        "moves": moves
    }
    
    # Save manifest
    output_path = REPORTS / "unify_manifest.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ {output_path}")
    print(f"✅ Total files to unify: {len(moves)}")
    
    # Print summary by module
    module_counts = {}
    for m in moves:
        mod = m["module"]
        module_counts[mod] = module_counts.get(mod, 0) + 1
    
    print("\n📊 Module Distribution:")
    for mod, count in sorted(module_counts.items(), key=lambda x: -x[1]):
        print(f"   {mod}: {count}")

if __name__ == "__main__":
    main()

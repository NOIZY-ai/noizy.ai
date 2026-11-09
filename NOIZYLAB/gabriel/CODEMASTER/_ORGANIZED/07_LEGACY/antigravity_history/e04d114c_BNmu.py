"""
SONIC-TEMPLATOR
Automated Audio Project Scaffolding & Manifest Generation
Part of the GABRIEL INFINITY System
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AudioProject:
    name: str
    genre: str
    bpm: int
    key: str
    created_at: str
    uuid: str
    
    def to_dict(self):
        return {
            "name": self.name,
            "genre": self.genre,
            "bpm": self.bpm,
            "key": self.key,
            "created_at": self.created_at,
            "uuid": self.uuid,
            "status": "Inception"
        }

class SonicTemplator:
    def __init__(self, root_path: str = "./data/audio_projects"):
        self.root = Path(root_path)
        self.root.mkdir(parents=True, exist_ok=True)
        
    def scaffold(self, name: str, genre: str = "Electronic", bpm: int = 128, key: str = "Cmin") -> str:
        """Create a full project structure"""
        
        # Sanitize name
        safe_name = "".join([c if c.isalnum() or c in "-_ " else "" for c in name]).strip().replace(" ", "_")
        timestamp = int(time.time())
        project_id = f"{safe_name}_{timestamp}"
        
        project_path = self.root / project_id
        
        # Structure
        subdirs = [
            "01_ProjectFiles",
            "02_Stems/Audio",
            "02_Stems/MIDI",
            "03_References",
            "04_Exports/WAV",
            "04_Exports/MP3",
            "05_Assets/Samples",
            "05_Assets/Artwork",
            "99_Docs"
        ]
        
        try:
            for d in subdirs:
                (project_path / d).mkdir(parents=True, exist_ok=True)
                
            # Create Manifest
            project = AudioProject(
                name=name,
                genre=genre,
                bpm=bpm,
                key=key,
                created_at=datetime.now().isoformat(),
                uuid=project_id
            )
            
            manifest_path = project_path / "99_Docs" / "project_manifest.json"
            manifest_path.write_text(json.dumps(project.to_dict(), indent=2))
            
            # Create README with AI Context
            readme_content = f"""# {name.upper()}
            
## Project Metadata
- **Genre**: {genre}
- **BPM**: {bpm}
- **Key**: {key}
- **Created**: {project.created_at}

## Sonic Objective
[Describe the sonic texture and emotional goal of this track here]

## Todo
- [ ] Sketch core motif
- [ ] Design rhythm section
- [ ] Arrange structure
"""
            (project_path / "README.md").write_text(readme_content)
            
            return f"SUCCESS: Project '{name}' created at {project_path}"
            
        except Exception as e:
            return f"ERROR: Failed to scaffold project. {e}"

    def list_projects(self) -> List[str]:
        if not self.root.exists():
            return []
        return [d.name for d in self.root.iterdir() if d.is_dir()]

# Simple text-based test
if __name__ == "__main__":
    sonic = SonicTemplator()
    print(sonic.scaffold("Test_Track_Alpha", "Techno", 135))

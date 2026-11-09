#!/usr/bin/env python3
"""
🦁 CODEBEAST INTEGRATION - GABRIEL
Move CODEBEAST into GABRIEL and fill it with ALL systems
"""

import shutil
import sys
from pathlib import Path
import json

class CodeBeastIntegrator:
    """Integrate CODEBEAST with GABRIEL ecosystem."""
    
    def __init__(self):
        self.gabriel_workspace = Path("/Users/rsp_ms/GABRIEL")
        self.codebeast_source = Path("/Users/rsp_ms/Desktop/CODEBEAST")
        self.codebeast_dest = self.gabriel_workspace / "CODEBEAST"
        
        print("\n" + "=" * 80)
        print("🦁 CODEBEAST INTEGRATION")
        print("=" * 80)
    
    def integrate(self):
        """Move CODEBEAST into GABRIEL and populate."""
        print("\n🦁 INTEGRATING CODEBEAST INTO GABRIEL...")
        
        # Copy CODEBEAST structure
        if self.codebeast_source.exists():
            print(f"\n📦 Copying CODEBEAST structure...")
            if self.codebeast_dest.exists():
                print("⚠️  CODEBEAST already exists in GABRIEL, updating...")
            else:
                shutil.copytree(self.codebeast_source, self.codebeast_dest, dirs_exist_ok=True)
                print(f"✅ CODEBEAST copied to: {self.codebeast_dest}")
        
        # Fill with GABRIEL systems
        self.populate_beast()
    
    def populate_beast(self):
        """Populate CODEBEAST with all GABRIEL systems."""
        print("\n🦁 POPULATING CODEBEAST WITH GABRIEL SYSTEMS...")
        
        gabriel_systems = [
            'autonomous_learning.py',
            'GABRIEL_CODEMASTER.py',
            'the_fishnet.py',
            'the_fishnet_universe.py',
            'TERMINUS.py',
            'TERMINUS_BRIDGE.py',
            'OMNIDIRECTIONAL.py',
            'CODE_VAC.py',
            'SCAN_ALL_DRIVES.py',
            'distribute_to_drives.py',
            'QUICK_DISTRIBUTE.py',
            'CHECK_DRIVES.py',
            'system_sound_manager.py',
            'spotify_crossfade.py',
            'organize_12tb.py'
        ]
        
        claws_dir = self.codebeast_dest / 'claws'
        claws_dir.mkdir(parents=True, exist_ok=True)
        
        for system in gabriel_systems:
            src = self.gabriel_workspace / system
            if src.exists():
                dst = claws_dir / system
                shutil.copy2(src, dst)
                print(f"✅ Added: {system}")
        
        print("\n🦁 CODEBEAST is now FULL of GABRIEL power!")


if __name__ == "__main__":
    integrator = CodeBeastIntegrator()
    integrator.integrate()

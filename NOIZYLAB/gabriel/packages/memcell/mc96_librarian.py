# 🤖 SYSTEM FILE: mc96_librarian.py
# Optimized by Healer Drone

import os
import datetime
import hashlib
import re
from pathlib import Path

# CONFIG
ROOT_DIR = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/MC96_Data")
REQUIRED_FOLDERS = [
    "TruthScans",
    "Gold",
    "Quarantine",
    "Archive",
    "WorkPacks",
    "NoizyTeam/Sessions"
]

class MC96Librarian:
    def __init__(self):
        self.root = ROOT_DIR
        self.enforce_structure()

    def enforce_structure(self):
        """
        Ensures the canonical folder structure exists.
        """
        if not self.root.exists():
            print(f"[LIBRARIAN] Creating Root: {self.root}")
            self.root.mkdir(parents=True, exist_ok=True)

        for folder in REQUIRED_FOLDERS:
            path = self.root / folder
            if not path.exists():
                print(f"[LIBRARIAN] Creating Canon Folder: {folder}")
                path.mkdir(parents=True, exist_ok=True)

    def validate_filename(self, filename):
        """
        Validates strict naming convention:
        {DOMAIN}_{SUBJECT}_{YYYYMMDD}_{HHMMSS}_{HASH8}.{ext}
        """
        pattern = r"^[A-Z0-9]+_[A-Z0-9]+_\d{8}_\d{6}_[A-F0-9]{8}\.[a-z0-9]+$"
        return bool(re.match(pattern, filename))

    def generate_canonical_name(self, domain, subject, ext, content_bytes=None):
        """
        Generates a compliant filename.
        """
        now = datetime.datetime.now()
        ts_date = now.strftime("%Y%m%d")
        ts_time = now.strftime("%H%M%S")

        if content_bytes:
            h = hashlib.sha256(content_bytes).hexdigest()[:8].upper()
        else:
            # Fallback random/time hash if no content
            h = hashlib.sha256(f"{domain}{subject}{now}".encode()).hexdigest()[:8].upper()

        return f"{domain.upper()}_{subject.upper()}_{ts_date}_{ts_time}_{h}.{ext}"

def main():
    print("📚 MC96 LIBRARIAN: Enforcing File Doctrine...")
    lib = MC96Librarian()

    # Test Naming
    test_name = lib.generate_canonical_name("MC96", "TEST", "txt", b"test content")
    print(f"   Canonical Name Example: {test_name}")
    print(f"   Validation check: {lib.validate_filename(test_name)}")

    print("✅ Structure Verified.")

if __name__ == "__main__":
    main()

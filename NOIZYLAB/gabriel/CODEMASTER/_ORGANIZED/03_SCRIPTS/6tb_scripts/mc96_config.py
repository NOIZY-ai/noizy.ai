"""
MC96 CONFIGURATION
Central source of truth for all MC96 Gabriel AI scripts and systems.
"""

import os

# Base Paths
MC96_ROOT = "/Volumes/6TB/Sample_Libraries"
MEMCELL_DIR = os.path.join(MC96_ROOT, "memcell_data")
MEMCELL_DB = os.path.join(MEMCELL_DIR, "memcell.json")
OVERLAP_LOG = os.path.join(MEMCELL_DIR, "temporal_overlap.json")
PROMPT_CACHE = os.path.join(MEMCELL_DIR, "optimized_prompts.json")
WEB_ROOT = os.path.join(MC96_ROOT, "mission_control_portal")
SERVER_PORT = 5173
REPORT_FILE = os.path.join(MC96_ROOT, "GLOBAL_TODO_REPORT.md")

# Volume Management
VOLUMES = [
    "/Volumes/12TB",
    "/Volumes/6TB",
    "/Volumes/4TB Big Fish",
    "/Volumes/4TB Blue Fish",
    "/Volumes/4TB FISH SG",
    "/Volumes/4TB Lacie",
    "/Volumes/4TBSG",
    "/Volumes/4TB_02",
    "/Volumes/4TB_Utility",
    "/Volumes/EW",
    "/Volumes/FISH",
    "/Volumes/MAG 4TB",
    "/Volumes/RED DRAGON",
    "/Volumes/RSP",
    "/Volumes/SAMPLE_MASTER",
    "/Volumes/SIDNEY",
    "/Volumes/SOUND_DESIGN"
]

# Standard Folder Structure (Hard Rules)
STANDARD_FOLDERS = [
    "Audio_Loops", "Best_Service", "Earth_Moments", 
    "IK_Multimedia", "Native_Instruments", "REX2_Loops",
    "Sample_Magic", "Steven_Slate", "Toontrack", "XLN_Audio"
]

# Directories to check for empty folders (Hard Rule #25)
CLEAN_TARGETS = [
    MC96_ROOT,
    os.path.join(MC96_ROOT, "Native_Instruments"),
    os.path.join(MC96_ROOT, "Sample_Magic"),
    os.path.join(MC96_ROOT, "Earth_Moments")
]

# Critical Files Verification
CRITICAL_FILES = [
    os.path.join(MC96_ROOT, "MC96ECOUNIVERSE_MASTER_MANIFEST.md"),
    os.path.join(MC96_ROOT, "memcell_core.py"),
    os.path.join(WEB_ROOT, "index.html"),
    os.path.join(WEB_ROOT, "styles.css"),
    os.path.join(WEB_ROOT, "app.js"),
    os.path.join(WEB_ROOT, "rmt.html")
]

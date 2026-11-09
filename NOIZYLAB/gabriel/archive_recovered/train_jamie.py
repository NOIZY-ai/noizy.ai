import os
import sys
from TTS.api import TTS

# Configuration
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
OUTPUT_PATH = "/Users/m2ultra/NOIZYLAB/GABRIEL/models/jamie_xtts"
DATASET_PATH = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_samples"

# Ensure output directory exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("⚡ GABRIEL CUSTOM EMULATION TRAINING")
print(f"Target: Jamie Premium Clone")
print(f"Engine: Coqui XTTS v2")
print("-" * 30)

# 1. Provide instructions for fine-tuning (XTTS usually requires specific recipe execution)
# Since direct API fine-tuning can be complex, we will use the ready-to-use fine-tuning recipe wrapper if available,
# or provide the exact CLI command the user needs to run.

print("For XTTS v2, we use the specific fine-tuning command.")
print("The dataset needs to be formatted with a metadata.csv first.")

# Create metadata.csv from filenames (assuming filename format jamie_001.wav|text)
# We need to know the text for each file.
# Since we generated them from a known list in 'record_jamie_dataset.py', we should regenerate that mapping.

print("⚠️  MISSING METADATA: We need to map audio files back to text.")
print("Please run the 'dataset_formatter.py' script first.")


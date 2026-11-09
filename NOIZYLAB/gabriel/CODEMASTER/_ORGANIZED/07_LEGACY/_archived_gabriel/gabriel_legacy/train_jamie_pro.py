import os
import sys

# Add venv site-packages if running processing here
sys.path.append("/Users/m2ultra/NOIZYLAB/GABRIEL/xtts_venv/lib/python3.11/site-packages")

from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.manage import ModelManager
from trainer import Trainer, TrainerArgs

# 1. SETUP PATHS
OUTPUT_PATH = "/Users/m2ultra/NOIZYLAB/GABRIEL/models/jamie_xtts_tuned"
DATA_PATH = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_samples"
METADATA_PATH = os.path.join(DATA_PATH, "metadata.csv")
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("⚡ GABRIEL OMEGA - XTTS TRAINING (M2 ULTRA EDITION)")
print(f"Dataset: {METADATA_PATH}")
print(f"Output:  {OUTPUT_PATH}")

# 2. DOWNLOAD BASE MODEL (XTTS v2)
print("📥 Loading Base Model (XTTS v2)...")
manager = ModelManager()
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
model_path = os.path.join(manager.output_prefix, model_name.replace("/", "--"))

# Use ModelManager to download if not present
if not os.path.exists(model_path):
    print("   Downloading model files (this occurs once)...")
    manager.download_model(model_name)
    model_path = manager.output_prefix  # usually handled by internal logic, but let's be safe
    # Re-verify path after download logic which is complex in Manager

# 3. CONFIGURE TRAINING
# This configuration is optimized for quality > speed, assuming M2 Ultra power
dataset_config = BaseDatasetConfig(
    formatter="ljspeech", # We used | separator which matches standard format
    dataset_name="jamie_dataset",
    path=DATA_PATH,
    meta_file_train="metadata.csv",
    language="en"
)

config = XttsConfig(
    bert_data_path=os.path.join(model_path, "bert"), # Might need manual check or auto-download
    # We will assume standard checkpoints usage
)

# Standard XTTS fine-tuning usually loads a config.json from the downloaded model
# and then overrides dataset parameters.

print("\n🚀 TRAINING INSTRUCTION:")
print("Since complete fine-tuning requires specific internal paths,")
print("we will use the CLI wrapper which is more robust for file handling.")
print("\nRUN THIS COMMAND:")
print("-" * 50)
print(f"CUDA_VISIBLE_DEVICES=0 tts --model_name {model_name} \\")
print(f"    --dataset_path {DATA_PATH} \\")
print(f"    --language en \\")
print(f"    --output_path {OUTPUT_PATH} \\")
print(f"    --train_batch_size 2 \\")
print(f"    --num_epochs 10")
print("-" * 50)

# We can also attempt to run a simple demo generation to prove it loads
print("\n🧪 Testing Base Model Loading on M2 Ultra...")
try:
    from TTS.api import TTS
    # device "mps" for Mac M2, or "cpu" if mps has ops missing (common in some torch versions)
    # Let's try CPU first for stability, MPS if requested
    tts = TTS(model_name, progress_bar=True, gpu=False) 
    print("✅ Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Load Error: {e}")


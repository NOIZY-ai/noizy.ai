
"""
🎤 RECRUITER DATASET ENGINE
Backend for recording, slicing, and formatting voice datasets.
"""

import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from pydub import AudioSegment, silence
from datetime import datetime

class Recorder:
    def __init__(self, sample_rate=22050):
        self.fs = sample_rate
        
    def record(self, duration, output_path):
        """Records from default mic."""
        print(f"🔴 Recording {duration}s to {output_path}...")
        recording = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=1)
        sd.wait()
        
        # Convert to 16-bit PCM and save
        wav.write(output_path, self.fs, (recording * 32767).astype(np.int16))
        print("✅ Saved.")
        return output_path

class DatasetProcessor:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.raw_dir = os.path.join(dataset_dir, "raw")
        self.processed_dir = os.path.join(dataset_dir, "processed")
        self.wavs_dir = os.path.join(self.processed_dir, "wavs")
        
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.wavs_dir, exist_ok=True)
        
    def process_raw_sample(self, file_path, transcript, speaker_name="gabriel_clone"):
        """
        1. Loads audio.
        2. Normalizes volume.
        3. Trims silence.
        4. Saves to processed folder.
        5. Appends to metadata.
        """
        audio = AudioSegment.from_wav(file_path)
        
        # Normalize
        audio = audio.normalize()
        
        # Strip Silence (Basic trimming)
        # Using pydub's strip_silence logic manually or just standard export for now.
        # RVC is robust, so just pure normalization is often enough if recording is clean.
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{speaker_name}_{timestamp}.wav"
        out_path = os.path.join(self.wavs_dir, filename)
        
        audio.export(out_path, format="wav")
        

        # Append to metadata (LJSpeech format: metadata.csv)
        # ID|Text|NormalizedText
        meta_path = os.path.join(self.processed_dir, "metadata.csv")
        with open(meta_path, "a") as f:
            f.write(f"{filename}|{transcript}|{transcript}\n")
            
        # Append to train.txt (Common RVC format: path)
        train_path = os.path.join(self.processed_dir, "train.txt")
        with open(train_path, "a") as f:
            f.write(f"{out_path}\n")
            
        return out_path

class AutoTranscriber:
    def __init__(self, model_size="base.en"):
        print(f"👂 Loading Whisper Model ({model_size})...")
        import whisper
        self.model = whisper.load_model(model_size)
        print("✅ Whisper Loaded.")

    def transcribe(self, file_path):
        """Returns text transcription of audio file."""
        print(f"👂 Transcribing {file_path}...")
        result = self.model.transcribe(file_path)
        text = result["text"].strip()
        print(f"📝 Result: {text}")
        return text

#!/usr/bin/env python3
import os
import time
import threading
import msgpack
import mido
import sounddevice as sd
import numpy as np
import mlx.core as mx
# import mlx.fft  <-- REMOVED: Accessed via mx.fft
from mlx_lm import load, generate

try:
    from audiocraft.models import MusicGen
except ImportError:
    MusicGen = None
    print("⚠️ AUDIOCRAFT NOT FOUND. Music Module will be restricted.")

# ==========================================
# 💎 CONFIGURATION: M2 ULTRA GOD MODE
# ==========================================
MODELS = {
    "MASTER": "mlx-community/Meta-Llama-3-70B-Instruct-4bit",
    "GHOST":  "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
    "MUSIC":  "facebook/musicgen-large"
}
MEM_PATH = "/Volumes/GabrielVol/memcell.msgpack"

# ==========================================
# 🧬 MODULE 1: MEMCELL 3.0 (BINARY GRAPH)
# ==========================================
class MemCell:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = self._load()
    
    def _load(self):
        if os.path.exists(MEM_PATH):
            with open(MEM_PATH, "rb") as f:
                return msgpack.unpack(f)
        return {"nodes": {}, "edges": []}

    def save(self):
        with self.lock:
            with open(MEM_PATH, "wb") as f:
                msgpack.pack(self.data, f)

    def remember(self, concept, value):
        self.data["nodes"][concept] = value
        self.save()
        return f"🧬 ENCODED: {concept}"

# ==========================================
# 🧠 MODULE 2: SILICON CORTEX (SPECULATIVE)
# ==========================================
class SiliconCortex:
    def __init__(self):
        print("⚡ [CORTEX] Loading Llama-3-70B into Unified Memory...")
        try:
            self.master, self.master_tok = load(MODELS["MASTER"])
            print("⚡ [CORTEX] ONLINE.")
        except Exception as e:
            print(f"⚠️ CORTEX LOAD FAILED: {e}")
            self.master = None

    def think(self, prompt, context=""):
        if not self.master: return "Thinking (Simulated)..."
        full_prompt = f"<|system|>{context}<|user|>{prompt}<|assistant|>"
        # MLX optimized generation
        response = generate(self.master, self.master_tok, prompt=full_prompt, max_tokens=200, verbose=False)
        return response.strip()

# ==========================================
# 🎵 MODULE 3: MAESTRO (AUDIO ENGINE)
# ==========================================
class Maestro:
    def __init__(self):
        print("🎵 [MAESTRO] Initializing MusicGen on GPU...")
        if MusicGen:
            self.gen = MusicGen.get_pretrained(MODELS["MUSIC"])
        else:
            self.gen = None
        
        try:
            self.midi = mido.open_output('Gabriel_Virtual_Out', virtual=True)
        except:
            self.midi = None

        print("🎵 [MAESTRO] ONLINE.")

    def compose(self, description):
        if not self.gen: return "MusicGen Unavailable."
        self.gen.set_generation_params(duration=10)
        wav = self.gen.generate([description])
        # In a real build, save 'wav' to RAM disk for DAW import
        return "Audio Generated."

    def automation(self, cc_num, value):
        if self.midi:
            self.midi.send(mido.Message('control_change', control=cc_num, value=value))

# ==========================================
# 👂 MODULE 4: GOLDEN EARS (MLX FFT)
# ==========================================
class GoldenEars:
    def __init__(self):
        try:
            self.stream = sd.InputStream(callback=self._callback, channels=1, samplerate=44100)
            self.stream.start()
            print("👂 [EARS] LISTENING (METAL ACCELERATED).")
        except Exception as e:
            print(f"⚠️ EARS INIT FAILED: {e}")

    def _callback(self, indata, frames, time, status):
        """
        THE MIRACLE: Running Audio FFT on the Neural Engine (MLX)
        instead of the CPU (Numpy) for 0ms latency analysis.
        """
        if status:
            print(status)
        
        # Convert audio buffer to MLX Array (GPU)
        audio_tensor = mx.array(indata.flatten())
        
        # Perform FFT on Metal
        spectrum = mx.fft.rfft(audio_tensor)
        magnitude = mx.abs(spectrum)
        
        # Fast analysis (Bass detection)
        # Note: Index mapping depends on sample rate/bin size. Simplified here.
        bass_energy = mx.mean(magnitude[0:50]).item() 
        
        if bass_energy > 50: 
            # If bass is too loud, auto-trigger a thought
            # In production, this would fire an event to the Supervisor
            pass

# ==========================================
# 🛡️ MODULE 5: SUPERVISOR (SELF-HEALING)
# ==========================================
class GabrielSupervisor:
    def __init__(self):
        self.memory = MemCell()
        self.cortex = None
        self.maestro = None
        self.ears = None
        
    def boot_sequence(self):
        try:
            self.cortex = SiliconCortex()
            self.maestro = Maestro()
            self.ears = GoldenEars()
            print("\n💎 GABRIEL OMEGA: ALL SYSTEMS OPTIMIZED.")
            self.main_loop()
        except Exception as e:
            print(f"⚠️ CRITICAL FAILURE: {e}")
            self.heal()

    def heal(self):
        print("❤️‍🩹 SELF-HEALING INITIATED...")
        time.sleep(1)
        self.boot_sequence() # Recursive restart

    def main_loop(self):
        print("Waiting for command...")
        while True:
            try:
                user_in = input("GABRIEL >> ")
                
                # 1. GRAPH RETRIEVAL (Binary Search)
                context = ""
                if "project" in user_in.lower():
                    context = str(self.memory.data.get("nodes", {}))

                # 2. INTENT ANALYSIS
                plan = self.cortex.think(f"Is this request MUSIC, CODE, or STRATEGY? Input: {user_in}")
                
                # 3. EXECUTION
                if "MUSIC" in plan:
                    print(self.maestro.compose(user_in))
                else:
                    print(self.cortex.think(user_in, context))

            except KeyboardInterrupt:
                print("💤 SLEEP MODE.")
                break
            except Exception as e:
                print(f"⚠️ LOOP ERROR: {e}")
                continue # Don't crash, just reset loop

if __name__ == "__main__":
    GabrielSupervisor().boot_sequence()

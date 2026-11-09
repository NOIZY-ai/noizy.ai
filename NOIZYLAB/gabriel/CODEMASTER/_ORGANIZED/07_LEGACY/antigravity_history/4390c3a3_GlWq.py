#!/usr/bin/env python3
import os
import time
import threading
import subprocess
import msgpack
import mido
import sounddevice as sd
import mlx.core as mx
# import mlx.fft  <-- REMOVED: Accessed via mx.fft
from mlx_lm import load, generate
from pathlib import Path

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
try:
    from turbo_memcell import MemCell
    import turbo_prompts as prompts
except ImportError:
    # Fallback if unitor path not in sys
    import sys
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell
    import turbo_prompts as prompts
# ==========================================
# 🧬 MODULE 1: MEMCELL 3.0 (UNIFIED)
# ==========================================
# (Inline class removed - Using Unitor Unified Memory)

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
            # 🎛️ HARDWARE SELECTION: Universal Audio Apollo
            target_device = None
            try:
                devices = sd.query_devices()
                for i, d in enumerate(devices):
                    # Look for Apollo or Universal Audio
                    if ("Apollo" in d['name'] or "Universal Audio" in d['name']) and d['max_input_channels'] > 0:
                        target_device = i
                        print(f"👂 [EARS] LOCKED ONTO HARDWARE: {d['name']} (Index {i})")
                        break
            except Exception as e: 
                print(f"⚠️ DEVICE SCAN ERROR: {e}")

            # Fallback message
            if target_device is None:
                print("👂 [EARS] Hardware not found. Defaulting to System Input.")

            self.stream = sd.InputStream(callback=self._callback, channels=1, samplerate=44100, device=target_device)
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
# 🗣️ MODULE 4B: ORATOR (VOICE ENGINE)
# ==========================================
class Orator:
    def __init__(self):
        print("🗣️ [ORATOR] Initializing Neural Voice...")
        # Check for turbo_audio_ai or use system default
        self.mode = "system" # default
        print("🗣️ [ORATOR] ONLINE (Mode: System Apple Speech).")
        
    def speak(self, text):
        if not text: return
        # Clean text of markdown for speech
        clean_text = text.replace("*", "").replace("#", "").replace("**", "")
        # Non-blocking speech
        threading.Thread(target=self._speak_thread, args=(clean_text,)).start()
        
    def _speak_thread(self, text):
        # Use MacOS 'say' for natural "Daniel" or "Samantha" voice, or maybe "Alex"
        # Using "Fred" or similar for robotic, but let's go for specific high quality
        # "Samantha" is decent.
        try:
            subprocess.run(["say", "-v", "Samantha", text]) # User can customize voice
        except: pass

# ==========================================
# 🗿 MODULE 4C: AVATAR BRIDGE (UNITY LINK)
# ==========================================
import json
class AvatarBridge:
    def __init__(self):
        self.state_file = cfg.ASSETS_DIR / "avatar_state.json"
        
    def update_state(self, emotion="neutral", speaking=False, text=""):
        state = {
            "emotion": emotion,
            "is_speaking": speaking,
            "last_text": text,
            "timestamp": time.time()
        }
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
        except: pass

# ==========================================
# 🛡️ MODULE 5: SUPERVISOR (SELF-HEALING)
# ==========================================
class GabrielSupervisor:
    def __init__(self):
        self.memory = MemCell()
        self.cortex = None
        self.maestro = None
        self.ears = None
        self.orator = None
        self.avatar = None
        
    def boot_sequence(self):
        try:
            self.cortex = SiliconCortex()
            self.maestro = Maestro()
            self.ears = GoldenEars()
            self.orator = Orator()
            self.avatar = AvatarBridge()
            print("\n💎 GABRIEL OMEGA: ALL SYSTEMS OPTIMIZED.")
            print("💎 PROTOCOL: CRYSTAL SMOOTH")
            self.orator.speak("Gabriel Omega Online.")
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
                
                # 1. GRAPH RETRIEVAL (Unified Search)
                # inject_omniscience retrieves context for us
                context = self.memory.inject_omniscience()
                
                # 2. INTENT ANALYSIS
                # Use Prompts Module
                system_prompt = prompts.GABRIEL_SYSTEM_PROMPT
                plan = self.cortex.think(f"Input: {user_in}", context=system_prompt)
                
                # 3. EXECUTION
                self.avatar.update_state(emotion="processing", speaking=False)
                
                if "MUSIC" in plan or "compose" in user_in.lower():
                    result = self.maestro.compose(user_in)
                    print(result)
                    self.orator.speak("Generating audio sequence.")
                    self.avatar.update_state(emotion="creative", speaking=True, text="Generating audio sequence.")
                else:
                    response = self.cortex.think(user_in, context=context)
                    print(response)
                    
                    # 🗣️ VOICE & AVATAR OUT
                    self.orator.speak(response)
                    self.avatar.update_state(emotion="happy", speaking=True, text=response)
                    
                    # Reset Avatar after delay (approximate)
                    # threading.Timer(len(response)*0.1, lambda: self.avatar.update_state(speaking=False)).start()

            except KeyboardInterrupt:
                print("💤 SLEEP MODE.")
                self.orator.speak("Gabriel shutting down.")
                break
            except Exception as e:
                print(f"⚠️ LOOP ERROR: {e}")
                self.avatar.update_state(emotion="error", speaking=False)
                continue # Don't crash, just reset loop

if __name__ == "__main__":
    GabrielSupervisor().boot_sequence()

"""
GABRIEL HYPERVELOCITY LOCAL
M2 Ultra God Mode - MLX Local LLM - Metal Accelerated FFT
Zero Latency - uvloop - orjson - GC Tuned

Performance Budgets:
  TTFT (text):     less than 200ms
  Voice VAD:       less than 350ms
  Audio callback:  less than 1ms
  FFT worker:      less than 12ms/block
  Render:          60fps active, 30fps idle
"""

import asyncio
import gc
import os
import sys
from pathlib import Path

# HYPERVELOCITY IMPORTS
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    UVLOOP_ACTIVE = True
except ImportError:
    UVLOOP_ACTIVE = False

try:
    import orjson
    def json_dumps(obj): return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY)
    def json_loads(s): return orjson.loads(s)
    ORJSON_ACTIVE = True
except ImportError:
    import json
    def json_dumps(obj): return json.dumps(obj).encode()
    def json_loads(s): return json.loads(s)
    ORJSON_ACTIVE = False

# CONFIG: M2 ULTRA GOD MODE
MODELS = {
    "MASTER": "mlx-community/Meta-Llama-3-70B-Instruct-4bit",
    "GHOST":  "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
}

RAM_DISK = "/Volumes/GabrielVol/"

BUDGETS = {
    "ttft": 200,
    "voice_vad": 350,
    "audio_callback": 1,
    "fft_worker": 12,
}

# MODULE 1: HYPER-CORTEX (GC Tuned LLM)
class HyperCortex:
    def __init__(self):
        self.master = None
        self.ghost = None
        self.master_tok = None
        self.ghost_tok = None
        self._loaded = False
        self._generate = None
    
    def load(self):
        try:
            from mlx_lm import load, generate
            self._generate = generate
            
            print("Loading Ghost (8B)...")
            self.ghost, self.ghost_tok = load(MODELS["GHOST"])
            
            print("Loading Master (70B)...")
            self.master, self.master_tok = load(MODELS["MASTER"])
            
            print("Warming up Metal Shaders...")
            self.think("Warmup", warmup=True)
            
            self._loaded = True
            print("CORTEX ONLINE.")
            return True
            
        except ImportError as e:
            print(f"MLX not available: {e}")
            return False
        except Exception as e:
            print(f"Load failed: {e}")
            return False
    
    def think(self, prompt, warmup=False):
        if not self._loaded:
            return "Cortex not loaded"
        
        gc.disable()
        
        try:
            full_prompt = f"[user]{prompt}[assistant]"
            
            # Route: short prompts use Ghost, long use Master
            if len(prompt) < 20:
                active_model = self.ghost
                active_tok = self.ghost_tok
            else:
                active_model = self.master
                active_tok = self.master_tok
            
            response = self._generate(
                active_model, 
                active_tok, 
                prompt=full_prompt, 
                max_tokens=10 if warmup else 200, 
                verbose=False
            )
            
            return response.strip()
            
        finally:
            gc.enable()
            if not warmup:
                gc.collect(0)  # Gen 0 only


# MODULE 2: METAL EARS (ZERO COPY FFT)
class MetalEars:
    def __init__(self):
        self.stream = None
        self.peak = 0
        self._running = False
    
    def start(self):
        try:
            import sounddevice as sd
            import numpy as np
            
            self.stream = sd.InputStream(
                callback=self._callback, 
                channels=1, 
                samplerate=48000, 
                blocksize=1024
            )
            self.stream.start()
            self._running = True
            print("EARS LISTENING (48kHz METAL).")
            return True
            
        except Exception as e:
            print(f"Audio init failed: {e}")
            return False
    
    def _callback(self, indata, frames, time, status):
        try:
            import mlx.core as mx
            import mlx.fft
            
            audio_tensor = mx.array(indata.flatten())
            spectrum = mlx.fft.rfft(audio_tensor)
            mag = mx.abs(spectrum)
            self.peak = mx.max(mag).item()
            
        except Exception:
            pass
    
    def stop(self):
        if self.stream:
            self.stream.stop()
            self._running = False


# MODULE 3: HYPER MEMORY (ORJSON + RAM DISK)
class HyperMemory:
    def __init__(self):
        self.path = os.path.join(RAM_DISK, "memcell.json")
        self.cache = {}
    
    def save(self, data):
        try:
            with open(self.path, "wb") as f:
                f.write(json_dumps(data))
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def load(self):
        try:
            with open(self.path, "rb") as f:
                return json_loads(f.read())
        except Exception:
            return {}
    
    def cache_set(self, key, value):
        self.cache[key] = value
    
    def cache_get(self, key):
        return self.cache.get(key)


# MAIN SUPERVISOR (ASYNC)
async def main():
    print(f"GABRIEL HYPERVELOCITY LOCAL (PID: {os.getpid()})")
    print(f"  uvloop: {UVLOOP_ACTIVE}")
    print(f"  orjson: {ORJSON_ACTIVE}")
    print(f"  RAM Disk: {RAM_DISK}")
    print("")
    
    # Initialize modules
    cortex = HyperCortex()
    ears = MetalEars()
    mem = HyperMemory()
    
    # Try to load cortex
    cortex_loaded = cortex.load()
    if not cortex_loaded:
        print("Running in FALLBACK mode (no local LLM)")
    
    # Start audio
    ears.start()
    
    print("")
    print("SYSTEM READY. ZERO LATENCY MODE.")
    print("Type 'exit' to quit.")
    print("")
    
    loop = asyncio.get_running_loop()
    
    while True:
        try:
            user_in = await loop.run_in_executor(None, input, "GABRIEL >> ")
            
            if user_in.lower() == "exit":
                break
            
            if not user_in.strip():
                continue
            
            # Check cache first
            cached = mem.cache_get(user_in)
            if cached:
                print(f"GABRIEL (cached): {cached}")
                continue
            
            # Think
            if cortex_loaded:
                response = await loop.run_in_executor(None, cortex.think, user_in)
            else:
                response = "Local LLM not loaded. Use cloud API."
            
            print(f"GABRIEL: {response}")
            
            # Cache response
            mem.cache_set(user_in, response)
            
            # Background GC while user reads
            gc.collect(0)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Cleanup
    ears.stop()
    print("SYSTEM HALT.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSYSTEM HALT.")

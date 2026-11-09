"""
GABRIEL INFINITY KERNEL
The Temporal Operating System for M2 Ultra
GORUNFREE - Limits Removed

Modules:
  1. MemCellTemporal - 4D Timeline with conflict detection
  2. HyperCortex - 70B/8B brain with GC freeze
  3. Maestro - Async music composition
  4. MetalEars - Metal FFT audio analysis
"""

import asyncio
import os
import time
import gc
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

# HYPERVELOCITY RUNTIME
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    UVLOOP = True
except ImportError:
    UVLOOP = False

try:
    import orjson
    def dumps(obj): return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY)
    def loads(s): return orjson.loads(s)
except ImportError:
    import json
    def dumps(obj): return json.dumps(obj).encode()
    def loads(s): return json.loads(s)


# CONFIG: M2 ULTRA INFINITY
MODELS = {
    "MASTER": "mlx-community/Meta-Llama-3-70B-Instruct-4bit",
    "GHOST":  "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
    "MUSIC":  "facebook/musicgen-large"
}

VOL_PATH = Path("/Volumes/GabrielVol/")
DECAY_DAYS = 30


# ============================================================================
# MODULE 1: MEMCELL TEMPORAL (4D Timeline)
# ============================================================================

@dataclass
class TemporalEvent:
    id: str
    title: str
    start: datetime
    end: datetime
    created_at: float
    tags: List[str] = field(default_factory=list)
    priority: int = 5
    recurrence: Optional[str] = None
    
    def overlaps(self, other) -> bool:
        return self.start < other.end and self.end > other.start
    
    def to_dict(self) -> dict:
        return {
            "id": self.id, "title": self.title,
            "start": self.start.isoformat(), "end": self.end.isoformat(),
            "created_at": self.created_at, "tags": self.tags,
            "priority": self.priority, "recurrence": self.recurrence
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"], title=data["title"],
            start=datetime.fromisoformat(data["start"]),
            end=datetime.fromisoformat(data["end"]),
            created_at=data["created_at"],
            tags=data.get("tags", []),
            priority=data.get("priority", 5),
            recurrence=data.get("recurrence")
        )


class MemCellTemporal:
    def __init__(self, path: Path = None):
        self.path = path or VOL_PATH / "temporal_graph.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.events: List[TemporalEvent] = []
        self.facts: Dict[str, Any] = {}
        self.archive: List[TemporalEvent] = []
        self._load()
    
    def _load(self):
        if self.path.exists():
            try:
                data = loads(self.path.read_bytes())
                self.events = [TemporalEvent.from_dict(e) for e in data.get("events", [])]
                self.facts = data.get("facts", {})
            except Exception:
                pass
    
    def save(self):
        data = {
            "events": [e.to_dict() for e in self.events],
            "facts": self.facts,
            "archive": [e.to_dict() for e in self.archive],
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self.path.write_bytes(dumps(data))
    
    def ingest_event(self, title: str, start: datetime, duration_mins: int = 60,
                     tags: List[str] = None, priority: int = 5) -> tuple:
        end = start + timedelta(minutes=duration_mins)
        event_id = hashlib.md5(f"{title}{start.isoformat()}".encode()).hexdigest()[:8]
        
        new_event = TemporalEvent(
            id=event_id, title=title, start=start, end=end,
            created_at=time.time(), tags=tags or [], priority=priority
        )
        
        conflicts = [e.title for e in self.events if new_event.overlaps(e)]
        
        if conflicts:
            return (False, f"TIME CONFLICT with: {', '.join(conflicts)}", conflicts)
        
        self.events.append(new_event)
        self.events.sort(key=lambda e: e.start)
        self.save()
        return (True, f"SCHEDULED: {title} ({start.strftime('%Y-%m-%d %H:%M')})", [])
    
    def get_upcoming(self, hours: int = 24) -> List[TemporalEvent]:
        now = datetime.now()
        end = now + timedelta(hours=hours)
        return [e for e in self.events if e.start >= now and e.start <= end]
    
    def get_context(self, n: int = 5) -> str:
        upcoming = self.get_upcoming(48)[:n]
        lines = ["TEMPORAL CONTEXT:"]
        for e in upcoming:
            lines.append(f"  - {e.title}: {e.start.strftime('%Y-%m-%d %H:%M')}")
        return "\n".join(lines) if len(lines) > 1 else "No upcoming events."
    
    def decay_old_events(self):
        cutoff = datetime.now() - timedelta(days=DECAY_DAYS)
        to_archive = [e for e in self.events if e.end < cutoff]
        self.archive.extend(to_archive)
        self.events = [e for e in self.events if e.end >= cutoff]
        self.save()
        return len(to_archive)


# ============================================================================
# MODULE 2: HYPER-CORTEX (Zero Latency Brain)
# ============================================================================

class HyperCortex:
    def __init__(self):
        self.master = None
        self.ghost = None
        self._generate = None
        self._loaded = False
    
    def load(self) -> bool:
        try:
            from mlx_lm import load, stream_generate
            self._generate = stream_generate  # Use stream_generate
            
            print("Loading Ghost (8B)...")
            self.ghost, self.ghost_tok = load(MODELS["GHOST"])
            
            print("Loading Master (70B)...")
            self.master, self.master_tok = load(MODELS["MASTER"])
            
            self._loaded = True
            print("CORTEX ONLINE.")
            return True
        except Exception as e:
            print(f"Cortex load error: {e}")
            return False
    
    async def think_stream(self, prompt: str, context: str = ""):
        """Async generator for streaming thoughts"""
        if not self._loaded:
            yield "Cortex not loaded. Using fallback."
            return
        
        gc.disable()
        try:
            full_prompt = f"[system]IDENTITY:GABRIEL. CONTEXT:{context}. DIRECTIVE:Concise.Execute.[/system][user]{prompt}[/user][assistant]"
            
            model = self.ghost if len(prompt) < 50 else self.master
            tok = self.ghost_tok if len(prompt) < 50 else self.master_tok
            
            # Offload generation to thread to not block event loop
            # We iterate over the synchronous generator
            loop = asyncio.get_running_loop()
            
            def run_gen():
                return self._generate(model, tok, prompt=full_prompt, max_tokens=200)

            # In a real async setup with MLX, we might iterate directly if it doesn't block GIL too hard
            # or use run_in_executor for the whole generator, but generators are tricky with executors.
            # Best pattern for MLX stream in async loop:
            for response in self._generate(model, tok, prompt=full_prompt, max_tokens=200):
                yield response.text
                await asyncio.sleep(0) # Yield back to loop
                
        finally:
            gc.enable()
            gc.collect(0)


# ============================================================================
# MODULE 3: MAESTRO (Async Music)
# ============================================================================

class Maestro:
    def __init__(self):
        self.gen = None
        self.midi = None
    
    def load(self) -> bool:
        try:
            from audiocraft.models import MusicGen
            import mido
            
            print("Loading MusicGen...")
            self.gen = MusicGen.get_pretrained(MODELS["MUSIC"])
            try:
                self.midi = mido.open_output('Gabriel_Virtual_Out', virtual=True)
            except:
                self.midi = None # Fallback if virtual ports fail
            print("MAESTRO ONLINE.")
            return True
        except Exception as e:
            print(f"Maestro load error: {e}")
            return False
    
    def compose(self, text: str, duration: int = 10):
        if not self.gen:
            return "MusicGen not loaded."
        self.gen.set_generation_params(duration=duration)
        wav = self.gen.generate([text])
        return f"Audio rendered: {text[:30]}..."


# ============================================================================
# MODULE 4: METAL EARS (FFT Analysis)
# ============================================================================

class MetalEars:
    def __init__(self):
        self.stream = None
        self.peak = 0
        self._running = False
    
    def start(self) -> bool:
        try:
            import sounddevice as sd
            self.stream = sd.InputStream(
                callback=self._callback, channels=1, samplerate=48000, blocksize=2048
            )
            self.stream.start()
            self._running = True
            print("EARS ONLINE (48kHz Metal FFT).")
            return True
        except Exception as e:
            print(f"Ears error: {e}")
            return False
    
    def _callback(self, indata, frames, time_info, status):
        try:
            import mlx.core as mx
            import mlx.fft
            tensor = mx.array(indata.flatten())
            spectrum = mlx.fft.rfft(tensor)
            self.peak = mx.mean(mx.abs(spectrum)).item()
        except Exception:
            pass
    
    def stop(self):
        if self.stream:
            self.stream.stop()
            self._running = False


# ============================================================================
# THE INFINITY LOOP
# ============================================================================

async def main():
    print("")
    print("=" * 60)
    print("  GABRIEL INFINITY - TEMPORAL OPERATING SYSTEM")
    print("  GORUNFREE | M2 ULTRA | ZERO LATENCY")
    print("=" * 60)
    print("")
    
    # Initialize Modules
    mem = MemCellTemporal()
    brain = HyperCortex()
    music = Maestro()
    ears = MetalEars()
    
    # Load what's available
    brain.load()
    music.load()
    ears.start()
    
    print("")
    print("SYSTEM READY. Type 'exit' to quit.")
    print("")
    
    loop = asyncio.get_running_loop()
    
    while True:
        try:
            user_in = await loop.run_in_executor(None, input, "GABRIEL >> ")
            
            if user_in.lower() == "exit":
                break
            
            if not user_in.strip():
                continue
            
            # TEMPORAL CHECK
            if "schedule" in user_in.lower():
                now = datetime.now()
                success, msg, conflicts = mem.ingest_event(
                    user_in.replace("schedule", "").strip() or "Task",
                    now + timedelta(hours=1), 60
                )
                print(f"result: {msg}")
                continue
            
            # MUSIC EXECUTION
            if "/music" in user_in:
                result = music.compose(user_in.replace("/music", "").strip())
                print(f"MAESTRO: {result}")
                continue
            
            # TEMPORAL CONTEXT QUERY
            if "upcoming" in user_in.lower() or "schedule" in user_in.lower():
                print(mem.get_context())
                continue
            
            # INTELLECTUAL EXECUTION (STREAMING)
            context = mem.get_context(3)
            print("GABRIEL: ", end="", flush=True)
            
            async for token in brain.think_stream(user_in, context):
                print(token, end="", flush=True)
            print("") # Newline at end
            print("")
            
            gc.collect(0)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"ERROR: {e}")
    
    ears.stop()
    print("SYSTEM HALT.")


if __name__ == "__main__":
    asyncio.run(main())

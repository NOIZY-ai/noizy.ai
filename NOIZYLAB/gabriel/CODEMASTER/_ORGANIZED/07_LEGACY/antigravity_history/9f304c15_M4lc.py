"""
GABRIEL INFINITY KERNEL
The Temporal Operating System for M2 Ultra
GORUNFREE - Limits Removed

Modules:
  1. MemCellTemporal - 4D Timeline with conflict detection
  2. HyperCortex - 70B/8B brain with GC freeze
  3. Maestro - Async music composition
  4. MetalEars - Metal FFT audio analysis
  5. DreamChamber - PC Link & Infrastructure Control
"""

import asyncio
import os
import time
import gc
import hashlib
import subprocess
import socket
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

# HYPERVELOCITY RUNTIME
try:
    import uvloop
    uvloop.install()
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

VOL_PATH = Path("./data/gabriel_vol/")
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
            # Lazy import to avoid startup lag if not used
            from audiocraft.models import MusicGen
            import mido
            
            print("Loading MusicGen...")
            # Small model for faster loading in dev, or large for prod
            self.gen = MusicGen.get_pretrained(MODELS["MUSIC"])
            try:
                self.midi = mido.open_output('Gabriel_Virtual_Out', virtual=True)
            except:
                self.midi = None 
            print("MAESTRO ONLINE.")
            return True
        except ImportError:
            print("Maestro warning: 'audiocraft' not installed. Music generation disabled.")
            return False
        except Exception as e:
            print(f"Maestro load error: {e}")
            return False
    
    async def compose(self, text: str, duration: int = 10):
        if not self.gen:
            return "MusicGen not loaded."
        
        loop = asyncio.get_running_loop()
        
        def _generate():
            self.gen.set_generation_params(duration=duration)
            wav = self.gen.generate([text])
            return f"Audio rendered: {text[:30]}..."
            
        print(f"Maestro composing: '{text}'...")
        result = await loop.run_in_executor(None, _generate)
        return result


# ============================================================================
# MODULE 4: METAL EARS (FFT Analysis)
# ============================================================================

class MetalEars:
    def __init__(self):
        self.stream = None
        self.peak = 0
        self._running = False
        self.mx = None
        self.fft = None
    
    def start(self) -> bool:
        try:
            import sounddevice as sd
            import mlx.core as mx
            import mlx.fft as fft
            
            # Pre-load MLX to avoid import in hot loop
            self.mx = mx
            self.fft = fft
            
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
        if not self._running or self.mx is None:
            return
            
        try:
            # Zero-copy where possible, but here we cast to tensor
            tensor = self.mx.array(indata.flatten())
            # Simple energy check or real FFT
            spectrum = self.fft.rfft(tensor)
            self.peak = self.mx.mean(self.mx.abs(spectrum)).item()
        except Exception:
            pass
    
    def stop(self):
        if self.stream:
            self.stream.stop()
            self._running = False


# ============================================================================
# MODULE 5: DREAMCHAMBER (PC Link)
# ============================================================================

class DreamChamberConnector:
    def __init__(self):
        self.ip = "10.90.90.20"
        self.mac = "XX:XX:XX:XX:XX:XX"  # Placeholder
        self.mount_script = Path(__file__).parent / "mount_pc_shares.sh"
        print("DREAMCHAMBER LINK ONLINE.")

    def ping(self) -> bool:
        try:
            subprocess.check_call(
                ['ping', '-c', '1', '-W', '500', self.ip], 
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False

    def is_mounted(self) -> bool:
        return os.path.ismount("/Volumes/PC_Bridge")

    def wake(self):
        # Broadcast WOL
        if "XX" in self.mac:
            return "❌ MAC Address not configured in kernel."
        
        try:
            addrs = self.mac.split(':')
            hw_addr = struct.pack('BBBBBB', *[int(x, 16) for x in addrs])
            magic = b'\xff' * 6 + hw_addr * 16
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic, ('10.90.90.255', 9))
            sock.close()
            return f"✨ Magic Packet sent to {self.mac}"
        except Exception as e:
            return f"❌ WOL Error: {e}"

    def force_mount(self) -> str:
        if not self.mount_script.exists():
            return "❌ Mount script missing."
        
        res = subprocess.run([str(self.mount_script)], capture_output=True, text=True)
        if res.returncode == 0:
            return "✅ Drive Mounted Successfully."
        else:
            return f"❌ Mount Failed: {res.stderr}"

    def status_report(self) -> str:
        online = "🟢 ONLINE" if self.ping() else "🔴 OFFLINE"
        mount = "💾 MOUNTED" if self.is_mounted() else "⚠️ UNMOUNTED"
        return f"PC STATUS: {online} | {mount}"


# ============================================================================
# MODULE 6: UNIVERSAL SEARCH (The All-Seeing Eye)
# ============================================================================

class UniversalSearch:
    def __init__(self):
        self.code_db = Path("NOIZYLAB_DB/gabriel_index.db")
        self.vis_db = Path("NOIZYLAB_DB/visual_index.db")
        print("UNIVERSAL SEARCH ONLINE.")

    def search_code(self, query: str, limit=5) -> str:
        if not self.code_db.exists(): return "Code Index Offline."
        try:
            import sqlite3
            conn = sqlite3.connect(self.code_db)
            # FTS5 Query
            res = conn.execute("SELECT path, snippet(grif_search, 2, '<b>', '</b>', '...', 10) FROM grif_search WHERE grif_search MATCH ? ORDER BY rank LIMIT ?", (query, limit)).fetchall()
            conn.close()
            if not res: return "No code found."
            return "\n".join([f"[CODE] {r[0]}" for r in res])
        except Exception as e:
            return f"Search Error: {e}"

    def search_media(self, query: str, limit=5) -> str:
        if not self.vis_db.exists(): return "Visual Index Offline."
        try:
            import sqlite3
            conn = sqlite3.connect(self.vis_db)
            # Simple Like Query
            q = f"%{query}%"
            res = conn.execute("SELECT path, media_type, volume FROM assets WHERE filename LIKE ? LIMIT ?", (q, limit)).fetchall()
            conn.close()
            if not res: return "No media found."
            return "\n".join([f"[{r[1].upper()}] {r[2]} :: {r[0]}" for r in res])
        except Exception as e:
            return f"Search Error: {e}"
            
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
    dream = DreamChamberConnector()
    eye = UniversalSearch()
    
    # Load what's available
    brain.load()
    music.load()
    
    # MetalEars (Local Mic) - Disabled by default for iPhone exclusivity
    if os.environ.get("ENABLE_LOCAL_MIC") == "1":
        print("  EARS:  [ON] Listening on Local Mic")
        ears.start()
    else:
        print("  EARS:  [OFF] Remote Mic Only (iPhone)")
    
    print("")
    print("SYSTEM READY. Type 'exit' to quit.")
    print("")

    # --- PACK HEARTBEAT ---
    print("🐺 GABRIEL INFINITY PACK CHECK:")
    scanner_pid = "OFFLINE"
    try:
        res = subprocess.check_output(["pgrep", "-f", "visual_scanner.py"]).decode().strip()
        if res: scanner_pid = f"FLOWING (PID {res.split()[0]})"
    except: pass
    print(f"   🌊 FISHNET FLOW:   {scanner_pid}")
    
    dash_pid = "OFFLINE"
    try:
        res = subprocess.check_output(["pgrep", "-f", "streamlit run"]).decode().strip()
        if res: dash_pid = f"WATCHING (PID {res.split()[0]})"
    except: pass
    print(f"   👁️  DASHBOARD:     {dash_pid}")
    
    pc_status = "UNREACHABLE"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex(("10.90.90.20", 445)) == 0: pc_status = "LINKED 🟢"
        s.close()
    except: pass
    print(f"   💻 DREAMCHAMBER:  {pc_status}")
    print("\n   [COMMANDS]: /say <text>, /audio, /visual, /code, /find, /help")
    
    loop = asyncio.get_running_loop()
    
    while True:
        try:
            # Get Input
            user_in = await loop.run_in_executor(None, input, "GABRIEL >> ")
            if not user_in: continue
            
            # --- TRUE FLOW COMMANDS ---
            if "/say" in user_in:
                text = user_in.replace("/say", "").strip()
                if text:
                    print(f"🗣️  Speaking through Avatar: '{text}'")
                    # Fire and Forget request to Hypervelocity
                    cmd = f'curl -X POST -H "Content-Type: application/json" -d \'{{"text": "{text}"}}\' http://localhost:8000/api/speak > /dev/null 2>&1 &'
                    subprocess.call(cmd, shell=True)
                continue

            if "/search" in user_in:
                query = user_in.replace("/search", "").strip()
                print(f"  🔍 SEARCHING UNIVERSE FOR: '{query}'...")
                
                # 1. SEARCH VISUAL VAULT (Media/Projects)
                try:
                    conn = sqlite3.connect("NOIZYLAB_DB/visual_index.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT filename, path, media_type FROM assets WHERE filename LIKE ? OR path LIKE ? LIMIT 5", (f"%{query}%", f"%{query}%"))
                    media_hits = cursor.fetchall()
                    conn.close()
                    
                    if media_hits:
                        print(f"  [MEDIA/PROJECTS] ({len(media_hits)} found)")
                        for fname, fpath, mtype in media_hits:
                            icon = "📄"
                            if mtype == 'project': icon = "🎛️"
                            elif mtype == 'video': icon = "🎬"
                            elif mtype == 'audio': icon = "🎵"
                            print(f"  {icon} {fname}  -> {fpath}")
                    else:
                        print("  [MEDIA] No matches.")
                except:
                    print("  [MEDIA] Index Offline.")

                # 2. SEARCH CODE VAULT (Sonic)
                try:
                    conn = sqlite3.connect("NOIZYLAB_DB/gabriel_index.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT path, snippet FROM code_index WHERE code_index MATCH ? ORDER BY rank LIMIT 3", (query,))
                    code_hits = cursor.fetchall()
                    conn.close()
                    
                    if code_hits:
                        print(f"  [CODE_VAULT] ({len(code_hits)} found)")
                        for cpath, csnip in code_hits:
                            print(f"  💎 {cpath}")
                    else:
                        print("  [CODE] No matches.")
                except:
                    print("  [CODE] Index Offline.")
                continue
                
            if user_in.lower() == "exit": break
            
            if user_in.lower() == "exit":
                break
            
            if not user_in.strip():
                continue
            
            # PROMPT PROCESSING
            prompt_lower = user_in.lower()
            
            # --- SKILL: DREAMCHAMBER (PC) ---
            if "pc" in prompt_lower or "dreamchamber" in prompt_lower:
                if "status" in prompt_lower or "check" in prompt_lower:
                    print(f"GABRIEL: {dream.status_report()}")
                    continue
                if "wake" in prompt_lower or "boot" in prompt_lower:
                    print(f"GABRIEL: {dream.wake()}")
                    continue
                if "mount" in prompt_lower or "connect" in prompt_lower:
                    print("GABRIEL: Attempting connection...")
                    print(f"GABRIEL: {dream.force_mount()}")
                    continue

            # --- SKILL: UNIVERSAL SEARCH ---
            if "/code" in user_in:
                q = user_in.replace("/code", "").strip()
                print(f"Searching Codebase for '{q}'...")
                print(eye.search_code(q))
                continue
                
            if "/find" in user_in or "/media" in user_in:
                q = user_in.replace("/find", "").replace("/media", "").strip()
                print(f"Searching Visual Vault for '{q}'...")
                print(eye.search_media(q))
                continue

            # --- SKILL: TEMPORAL (SCHEDULE) ---
            if "schedule" in prompt_lower:
                now = datetime.now()
                success, msg, conflicts = mem.ingest_event(
                    user_in.replace("schedule", "").strip() or "Task",
                    now + timedelta(hours=1), 60
                )
                print(f"result: {msg}")
                continue
            
            # --- SKILL: MAESTRO (MUSIC) ---
            if "/music" in user_in:
                result = await music.compose(user_in.replace("/music", "").strip())
                print(f"MAESTRO: {result}")
                continue
            
            # --- SKILL: CONTEXT QUERY ---
            if "upcoming" in prompt_lower:
                print(mem.get_context())
                continue
            
            # --- SKILL: INTELLECTUAL EXECUTION (DEFAULT) ---
            context = mem.get_context(3)
            pc_context = f" [PC: {dream.status_report()}]"
            
            print("GABRIEL: ", end="", flush=True)
            
            async for token in brain.think_stream(user_in, context + pc_context):
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

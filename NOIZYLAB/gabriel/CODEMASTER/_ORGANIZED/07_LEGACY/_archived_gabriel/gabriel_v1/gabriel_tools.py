"""
GABRIEL TOOLS v2.0 - SUPERCHARGED
The Hands - Studio, Memory, and Creative Intelligence
"""

import os
import json
import subprocess
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

class GabrielTools:
    """The hands of GABRIEL - handles studio operations and memory"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.memory_path = Path("memory")
        self.memory_path.mkdir(exist_ok=True)
        self.cache_path = Path("cache")
        self.cache_path.mkdir(exist_ok=True)
        self.start_time = datetime.now()
        self._init_ai()
        
        # Prebuilt prompts for zero-latency
        self.QUICK_PROMPTS = {
            "music_epic": self._music_prompt("epic orchestral", "heroic", 120),
            "music_chill": self._music_prompt("lo-fi hip hop", "relaxed", 85),
            "music_edm": self._music_prompt("progressive house", "euphoric", 128),
            "video_product": self._video_prompt("product reveal", "cinematic", "30s"),
            "video_trailer": self._video_prompt("movie trailer", "action", "60s"),
            "image_cyber": self._image_prompt("cyberpunk cityscape", "neon noir"),
            "image_nature": self._image_prompt("epic landscape", "golden hour"),
        }
    
    def _init_ai(self):
        """Initialize AI model with caching"""
        try:
            import google.generativeai as genai
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
            else:
                self.model = None
        except ImportError:
            self.model = None
    
    # ========== PROMPT TEMPLATES ==========
    
    def _music_prompt(self, genre: str, mood: str, bpm: int) -> str:
        return f"""Generate a PRODUCTION-READY music prompt:
Genre: {genre}
Mood: {mood}
BPM: {bpm}

Include:
- Key signature and chord progression
- Instrumentation (lead, bass, drums, pads)
- Arrangement (intro, verse, chorus, bridge, outro)
- Production techniques (compression, reverb, sidechain)
- Reference tracks for style

Format for: Suno AI / MusicFX / Udio"""

    def _video_prompt(self, concept: str, style: str, duration: str) -> str:
        return f"""Generate a CINEMATIC video prompt:
Concept: {concept}
Style: {style}
Duration: {duration}

Include:
- Shot list with camera movements
- Lighting setup (key, fill, rim)
- Color grading LUT suggestions
- VFX elements needed
- Audio/music sync points

Format for: Google Veo / VideoFX / Runway"""

    def _image_prompt(self, subject: str, style: str) -> str:
        return f"""Generate a DETAILED image prompt:
Subject: {subject}
Style: {style}

Include:
- Composition and framing
- Lighting description
- Color palette (hex codes)
- Technical details (focal length, aperture simulation)
- Negative prompts to avoid

Format for: Google ImageFX / Midjourney / DALL-E"""

    # ========== MEMORY (MemCells) ==========
    
    def save_memory(self, content: str, tags: List[str] = [], memory_type: str = "general") -> str:
        """Save content to a MemCell with smart indexing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        cell_id = f"MEM_{memory_type}_{timestamp}_{content_hash}"
        
        data = {
            "id": cell_id,
            "content": content,
            "tags": tags,
            "type": memory_type,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "access_count": 0
        }
        
        cell_path = self.memory_path / f"{cell_id}.json"
        with open(cell_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return cell_id
    
    def get_memory(self, cell_id: str) -> Optional[Dict]:
        """Retrieve a specific MemCell and increment access count"""
        cell_path = self.memory_path / f"{cell_id}.json"
        if cell_path.exists():
            with open(cell_path) as f:
                data = json.load(f)
            data["access_count"] += 1
            with open(cell_path, "w") as f:
                json.dump(data, f, indent=2)
            return data
        return None
    
    def get_all_memories(self, limit: int = 50) -> List[Dict]:
        """Get all stored memories, sorted by recency"""
        memories = []
        for cell_path in self.memory_path.glob("*.json"):
            with open(cell_path) as f:
                memories.append(json.load(f))
        return sorted(memories, key=lambda x: x.get("created", ""), reverse=True)[:limit]
    
    def search_memories(self, query: str) -> List[Dict]:
        """Search memories by content or tags with relevance scoring"""
        results = []
        query_lower = query.lower()
        
        for memory in self.get_all_memories(limit=100):
            content = memory.get("content", "").lower()
            tags = [t.lower() for t in memory.get("tags", [])]
            
            score = 0
            if query_lower in content:
                score += content.count(query_lower) * 10
            for tag in tags:
                if query_lower in tag:
                    score += 20
            
            if score > 0:
                memory["relevance_score"] = score
                results.append(memory)
        
        return sorted(results, key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        memories = self.get_all_memories(limit=1000)
        types = {}
        for m in memories:
            t = m.get("type", "general")
            types[t] = types.get(t, 0) + 1
        
        return {
            "total": len(memories),
            "types": types,
            "oldest": memories[-1].get("created") if memories else None,
            "newest": memories[0].get("created") if memories else None
        }
    
    # ========== AI THINKING ==========
    
    async def genius_think(self, prompt: str, system_prompt: str = "") -> str:
        """GENIUS MODE: Multi-step reasoning with caching"""
        if not self.model:
            return "⚠️ AI MODEL NOT INITIALIZED. Set GEMINI_API_KEY."
        
        # Check cache first
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        cache_file = self.cache_path / f"{cache_key}.json"
        
        if cache_file.exists():
            with open(cache_file) as f:
                cached = json.load(f)
            if (datetime.now() - datetime.fromisoformat(cached["timestamp"])).seconds < 3600:
                return cached["response"]
        
        try:
            # Chain of Thought prompting
            cot_prompt = f"""
{system_prompt}

TASK: {prompt}

APPROACH:
1. Analyze the request carefully
2. Consider the best approach
3. Provide a production-ready response

Respond directly and concisely.
"""
            
            response = self.model.generate_content(cot_prompt)
            result = response.text
            
            # Cache the response
            with open(cache_file, "w") as f:
                json.dump({
                    "prompt": prompt,
                    "response": result,
                    "timestamp": datetime.now().isoformat()
                }, f)
            
            # Save to memory
            self.save_memory(
                content=f"Q: {prompt}\n\nA: {result}",
                tags=["conversation", "ai_response"],
                memory_type="conversation"
            )
            
            return result
            
        except Exception as e:
            return f"⚠️ THINKING ERROR: {e}"
    
    # ========== STUDIO TOOLS ==========
    
    async def generate_music_prompt(self, genre: str, mood: str, tempo: int = 120) -> str:
        """Generate a production-ready music prompt"""
        prompt = self._music_prompt(genre, mood, tempo)
        result = await self.genius_think(prompt)
        self.save_memory(result, ["music", genre, mood], "music_prompt")
        return result
    
    async def generate_video_prompt(self, concept: str, style: str, duration: str = "30s") -> str:
        """Generate a cinematic video prompt"""
        prompt = self._video_prompt(concept, style, duration)
        result = await self.genius_think(prompt)
        self.save_memory(result, ["video", concept, style], "video_prompt")
        return result
    
    async def generate_image_prompt(self, subject: str, style: str) -> str:
        """Generate a visual prompt"""
        prompt = self._image_prompt(subject, style)
        result = await self.genius_think(prompt)
        self.save_memory(result, ["image", subject, style], "image_prompt")
        return result
    
    async def generate_voice_script(self, topic: str, duration: str = "30s", tone: str = "professional") -> str:
        """Generate a voice-over script"""
        prompt = f"""Write a {duration} voice-over script:
Topic: {topic}
Tone: {tone}

Include:
- Attention-grabbing hook
- Key message points
- Call to action
- Pause markers [PAUSE]
- Emphasis markers *like this*

Format for: ElevenLabs / Neural TTS"""
        result = await self.genius_think(prompt)
        self.save_memory(result, ["voice", topic, tone], "voice_script")
        return result
    
    def speak(self, text: str, voice: str = "Samantha", rate: int = 180) -> bool:
        """Synthesize speech using macOS Neural TTS"""
        try:
            # Clean text for speech
            clean_text = text.replace('"', '\\"').replace("'", "\\'")
            cmd = f'say -v "{voice}" -r {rate} "{clean_text}"'
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            print(f"Speech error: {e}")
            return False
    
    def speak_async(self, text: str, voice: str = "Samantha", rate: int = 180):
        """Non-blocking speech synthesis"""
        import threading
        thread = threading.Thread(target=self.speak, args=(text, voice, rate))
        thread.start()
    
    # ========== QUICK COMMANDS ==========
    
    def get_quick_prompt(self, key: str) -> Optional[str]:
        """Get a pre-built prompt for zero latency"""
        return self.QUICK_PROMPTS.get(key)
    
    async def execute_command(self, command: str, params: Dict[str, Any] = {}) -> Dict:
        """Execute a studio command"""
        commands = {
            "music": self.generate_music_prompt,
            "video": self.generate_video_prompt,
            "image": self.generate_image_prompt,
            "voice": self.generate_voice_script,
            "speak": lambda text, **kw: self.speak(text, **kw),
            "speak_async": lambda text, **kw: self.speak_async(text, **kw),
            "save": lambda content, tags=[], t="general": self.save_memory(content, tags, t),
            "search": lambda query: self.search_memories(query),
            "memories": lambda: self.get_all_memories(),
            "stats": lambda: self.get_memory_stats(),
            "quick": lambda key: self.get_quick_prompt(key),
        }
        
        if command in commands:
            try:
                result = commands[command](**params)
                if asyncio.iscoroutine(result):
                    result = await result
                return {"success": True, "result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": f"Unknown command: {command}"}
    
    # ========== UTILITIES ==========
    
    def get_uptime(self) -> str:
        """Get system uptime"""
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        import platform
        return {
            "hostname": platform.node(),
            "system": platform.system(),
            "processor": platform.processor(),
            "python": platform.python_version(),
            "uptime": self.get_uptime(),
            "memory_count": len(self.get_all_memories()),
        }

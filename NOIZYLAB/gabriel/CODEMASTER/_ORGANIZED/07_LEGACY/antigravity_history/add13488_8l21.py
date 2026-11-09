"""
GABRIEL TOOLS v1.0
The Hands - Studio & Memory Functions
"""

import os
import json
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

class GabrielTools:
    """The hands of GABRIEL - handles studio operations and memory"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.memory_path = Path("memory")
        self.memory_path.mkdir(exist_ok=True)
        self.start_time = datetime.now()
        self._init_ai()
    
    def _init_ai(self):
        """Initialize AI model"""
        try:
            import google.generativeai as genai
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
            else:
                self.model = None
        except ImportError:
            self.model = None
    
    # ========== MEMORY (MemCells) ==========
    
    def save_memory(self, content: str, tags: List[str] = []) -> str:
        """Save content to a MemCell"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cell_id = f"MEM_{timestamp}"
        
        data = {
            "id": cell_id,
            "content": content,
            "tags": tags,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        
        cell_path = self.memory_path / f"{cell_id}.json"
        with open(cell_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return cell_id
    
    def get_memory(self, cell_id: str) -> Optional[Dict]:
        """Retrieve a specific MemCell"""
        cell_path = self.memory_path / f"{cell_id}.json"
        if cell_path.exists():
            with open(cell_path) as f:
                return json.load(f)
        return None
    
    def get_all_memories(self) -> List[Dict]:
        """Get all stored memories"""
        memories = []
        for cell_path in self.memory_path.glob("*.json"):
            with open(cell_path) as f:
                memories.append(json.load(f))
        return sorted(memories, key=lambda x: x.get("created", ""), reverse=True)
    
    def search_memories(self, query: str) -> List[Dict]:
        """Search memories by content or tags"""
        results = []
        query_lower = query.lower()
        
        for memory in self.get_all_memories():
            content = memory.get("content", "").lower()
            tags = [t.lower() for t in memory.get("tags", [])]
            
            if query_lower in content or query_lower in tags:
                results.append(memory)
        
        return results
    
    # ========== AI THINKING ==========
    
    async def genius_think(self, prompt: str, system_prompt: str = "") -> str:
        """
        GENIUS MODE: Multi-step reasoning with self-critique
        """
        if not self.model:
            return "⚠️ AI MODEL NOT INITIALIZED. Set GEMINI_API_KEY."
        
        try:
            # Step 1: Chain of Thought
            cot_prompt = f"""
            {system_prompt}
            
            TASK: {prompt}
            
            INSTRUCTIONS:
            1. Think step-by-step about this problem
            2. Consider multiple approaches
            3. Be specific and actionable
            
            FORMAT:
            ## THINKING
            [Your reasoning]
            
            ## SOLUTION
            [Your answer]
            """
            
            response = self.model.generate_content(cot_prompt)
            draft = response.text
            
            # Step 2: Self-Critique
            critique_prompt = f"""
            You are reviewing this AI response:
            
            TASK: {prompt}
            RESPONSE: {draft}
            
            Rate 1-10 and explain. If score < 9, provide BETTER VERSION.
            """
            
            critique = self.model.generate_content(critique_prompt)
            
            if "better version" in critique.text.lower():
                # Step 3: Refinement
                refine_prompt = f"""
                ORIGINAL: {draft}
                CRITIQUE: {critique.text}
                
                Produce the FINAL, PERFECTED version.
                """
                final = self.model.generate_content(refine_prompt)
                return final.text
            
            return draft
            
        except Exception as e:
            return f"⚠️ THINKING ERROR: {e}"
    
    # ========== STUDIO TOOLS ==========
    
    async def generate_music_prompt(self, genre: str, mood: str, tempo: int = 120) -> str:
        """Generate a production-ready music prompt"""
        prompt = f"""
        Generate a detailed music production prompt for:
        - Genre: {genre}
        - Mood: {mood}
        - Tempo: {tempo} BPM
        
        Include: Key, chord progression, instrumentation, arrangement, production tips.
        Format for Suno/MusicFX.
        """
        return await self.genius_think(prompt)
    
    async def generate_video_prompt(self, concept: str, style: str, duration: str) -> str:
        """Generate a cinematic video prompt"""
        prompt = f"""
        Generate a video production prompt for:
        - Concept: {concept}
        - Style: {style}
        - Duration: {duration}
        
        Include: Shot types, camera movements, lighting, VFX notes.
        Format for Veo/VideoFX.
        """
        return await self.genius_think(prompt)
    
    async def generate_image_prompt(self, subject: str, style: str) -> str:
        """Generate a visual prompt"""
        prompt = f"""
        Generate an image prompt for:
        - Subject: {subject}
        - Style: {style}
        
        Include: Composition, lighting, color palette, technical details.
        Format for ImageFX/Midjourney.
        """
        return await self.genius_think(prompt)
    
    def speak(self, text: str, voice: str = "Samantha", rate: int = 180) -> bool:
        """Synthesize speech using macOS Neural TTS"""
        try:
            cmd = f'say -v "{voice}" -r {rate} "{text}"'
            subprocess.run(cmd, shell=True)
            return True
        except Exception as e:
            print(f"Speech error: {e}")
            return False
    
    # ========== COMMANDS ==========
    
    async def execute_command(self, command: str, params: Dict[str, Any] = {}) -> Dict:
        """Execute a studio command"""
        commands = {
            "music": self.generate_music_prompt,
            "video": self.generate_video_prompt,
            "image": self.generate_image_prompt,
            "speak": lambda text, **kw: self.speak(text, **kw),
            "save": lambda content, tags=[]: self.save_memory(content, tags),
            "search": lambda query: self.search_memories(query),
            "memories": lambda: self.get_all_memories(),
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


import os
import json
from sonic_templator import SonicTemplator
from deepseek_brain import DeepSeekBrain
from voice_core import VoiceCore
from memcell_core import MemCellCore

class GabrielGenesis:
    """
    GABRIEL GENESIS: The Creative Spark.
    Orchestrates complex flows between MemCell, Templates, and Intelligence.
    """
    def __init__(self):
        self.templator = SonicTemplator()
        self.brain = DeepSeekBrain()
        self.voice = VoiceCore()
        self.memcell = MemCellCore()

    def run_genesis(self, project_name, style="ableton", vibe="Dark Techno"):
        """
        Executes the 'Creative Genesis' Flow:
        1. Create Project Structure (SonicTemplator)
        2. Generate Creative Brief (DeepSeek R1)
        3. Announce Completion (VoiceCore)
        """
        results = {}
        
        # Step 1: Structure
        structure_res = self.templator.create_project(project_name, style)
        results['structure'] = structure_res
        
        if 'error' in structure_res:
            return {"error": structure_res['error'], "step": "structure"}
            
        project_path = structure_res.get('path')
        
        # Step 2: Intelligence
        prompt = f"Write a high-concept Creative Brief for a music project named '{project_name}'. Style: {style}. Vibe: {vibe}. Output in detailed Markdown."
        brain_res = self.brain.ask(prompt)
        results['intelligence'] = brain_res
        
        if brain_res.get('status') == 'success' or brain_res.get('status') == 'simulated':
            brief_content = brain_res.get('response', 'No content generated.')
            brief_path = os.path.join(project_path, "CREATIVE_BRIEF.md")
            try:
                with open(brief_path, 'w') as f:
                    f.write(brief_content)
                results['brief_path'] = brief_path
            except Exception as e:
                results['brief_error'] = str(e)
                
        # Step 3: Voice
        self.voice.speak(f"Genesis Complete. Project {project_name} initialized.")
        
        # Step 4: MemCell Persistence
        self.memcell.add_item(f"GENESIS PROJECT: {project_name} ({style}) - {vibe}", "Genesis_Log")
        
        return results

if __name__ == "__main__":
    genesis = GabrielGenesis()
    print(genesis.run_genesis("Omega_Protocol", "ableton", "Cyberpunk Industrial"))


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
        2. Generate Creative Manifesto (DeepSeek R1)
        3. Define Technical Specs (BPM, Key, Libraries)
        4. Announce Completion (VoiceCore)
        """
        results = {}
        
        print(f"✨ [GENESIS] Sparking: {project_name} | {style} | {vibe}")
        self.voice.speak(f"Initiating Genesis Protocol for {project_name}.")
        
        # Step 1: Structure (SonicTemplator)
        structure_res = self.templator.create_project(project_name, style)
        results['structure'] = structure_res
        
        if 'error' in structure_res:
             self.voice.speak("Genesis Aborted. Structure failure.")
             return {"error": structure_res['error'], "step": "structure"}
            
        project_path = structure_res.get('path')
        
        # Step 2: Intelligence (DeepSeek R1)
        # We ask for a structured JSON response embedded in the markdown
        prompt = (
            f"You are the GABRIEL SYSTEM ARCHITECT. Create a 'Genesis Manifesto' for a new project.\n"
            f"NAME: {project_name}\nTYPE: {style}\nVIBE: {vibe}\n\n"
            f"1. Write a high-concept Creative Vision (Markdown).\n"
            f"2. Define Technical Specs (JSON format: BPM, Key, Instrumentation/Libraries).\n"
            f"3. Suggest 3 immediate Next Actions."
        )
        
        # Explicitly invoke R1 (Reasoner)
        brain_res = self.brain.ask(prompt, model_type="reasoner")
        results['intelligence'] = brain_res
        
        content = brain_res.get('response', 'No content generated.')
        
        # Save Manifesto
        brief_path = os.path.join(project_path, "GENESIS_MANIFESTO.md")
        try:
            with open(brief_path, 'w') as f:
                f.write(content)
            results['brief_path'] = brief_path
        except Exception as e:
            results['brief_error'] = str(e)
            
        # Optional: Code Scaffolding for 'code' type
        if style == "code" or "python" in style:
            main_py = os.path.join(project_path, "main.py")
            if not os.path.exists(main_py):
                with open(main_py, 'w') as f:
                    f.write(f'# GABRIEL GENESIS PROJECT: {project_name}\n# VIBE: {vibe}\n\ndef main():\n    print("GORUNFREE!!!")\n\nif __name__ == "__main__":\n    main()\n')

        # Step 3: Voice Feedback
        self.voice.speak(f"Genesis Complete. {project_name} is ready for expansion.")
        
        # Step 4: MemCell Persistence (Correct Method)
        try:
            self.memcell.collect(
                f"GENESIS: {project_name}", 
                {"style": style, "vibe": vibe, "path": project_path}
            )
        except Exception as e:
            print(f"❌ [MEMCELL] Error: {e}")
        
        return results

if __name__ == "__main__":
    genesis = GabrielGenesis()
    print(genesis.run_genesis("Omega_Protocol", "ableton", "Cyberpunk Industrial"))

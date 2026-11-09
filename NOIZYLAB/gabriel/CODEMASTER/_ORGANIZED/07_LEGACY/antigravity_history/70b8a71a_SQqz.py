import os
import requests
from typing import Optional, Dict, Any

class DeepSeekBrain:
    """
    Advanced Interface for DeepSeek AI (R1 & V3).
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/chat/completions"
        self.model = "deepseek-reasoner" # DeepSeek R1 Model for Advanced Reasoning
        self.chat_model = "deepseek-chat" # Standard Chat V3
        
    def ask(self, query: str, model_type: str = "reasoner") -> Dict[str, Any]:
        """
        Send a query to DeepSeek AI.
        model_type: 'reasoner' (DeepSeek R1) or 'chat' (DeepSeek V3).
        """
        if not self.api_key:
            # Fallback for Development without Key
            return {
                "response": "DeepSeek Link Offline. (Simulated Response)",
                "reasoning": "No API Key detected.",
                "status": "simulated"
            }
            
        target_model = self.model if model_type == "reasoner" else self.chat_model
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": "You are GABRIEL SYSTEM OMEGA. The M2 Ultra Overlord. You are precise, redundant, and 100% optimized. Output markdown."},
                {"role": "user", "content": query}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            message = data['choices'][0]['message']
            content = message.get('content', '')
            # R1 returns 'reasoning_content', V3 does not.
            reasoning = message.get('reasoning_content', '')
            
            return {
                "response": content,
                "reasoning": reasoning,
                "model": target_model,
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def generate_code(self, prompt: str) -> Dict[str, Any]:
        """Generate Python code based on the prompt."""
        return self.ask(f"Generate Python code for: {prompt}")

if __name__ == "__main__":
    # Test with dummy key to see error handling or real key if env is set
    brain = DeepSeekBrain()
    print(brain.ask("Hello Gabriel"))

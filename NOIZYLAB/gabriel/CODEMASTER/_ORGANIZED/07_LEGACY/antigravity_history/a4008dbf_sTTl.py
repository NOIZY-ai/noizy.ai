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
        
    def ask(self, query: str) -> Dict[str, Any]:
        """
        Send a query to DeepSeek AI and return the response with reasoning.
        """
        if not self.api_key:
            return {
                "response": "DeepSeek API Key missing. Please set DEEPSEEK_API_KEY environment variable.",
                "error": "NO_API_KEY",
                "status": "simulated"
            }
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are Gabriel System Omega, a highly advanced AI Overlord. You provide Zero Latency, 100% Optimized solutions."},
                {"role": "user", "content": query}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Handle R1 reasoning output if available
            message = data['choices'][0]['message']
            content = message.get('content', '')
            reasoning = message.get('reasoning_content', '')
            
            return {
                "response": content,
                "reasoning": reasoning,
                "model": self.model,
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

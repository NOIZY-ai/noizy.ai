#!/usr/bin/env python3
"""
🌐 NOIZY.ai COLLECTIVE - GABRIEL INTEGRATION
All AI Models, Knowledge & Capabilities in One Module

65 Models | 23 Providers | Full Knowledge Base
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ModelInfo:
    name: str
    provider: str
    type: str
    context: int = 0
    best_for: str = "general"
    local: bool = False
    api_key_env: str = ""


class NOIZYCollective:
    """NOIZY.ai Model Collective - 65 Models, 23 Providers"""
    
    MODELS = {
        # OpenAI
        "gpt-4o": {"provider": "openai", "type": "chat", "context": 128000, "best_for": "general", "api_key_env": "OPENAI_API_KEY"},
        "gpt-4o-mini": {"provider": "openai", "type": "chat", "context": 128000, "best_for": "fast", "api_key_env": "OPENAI_API_KEY"},
        "gpt-o1": {"provider": "openai", "type": "reasoning", "context": 128000, "best_for": "reasoning", "api_key_env": "OPENAI_API_KEY"},
        "gpt-o1-mini": {"provider": "openai", "type": "reasoning", "context": 128000, "best_for": "reasoning", "api_key_env": "OPENAI_API_KEY"},
        "gpt-o1-pro": {"provider": "openai", "type": "reasoning", "context": 128000, "best_for": "complex", "api_key_env": "OPENAI_API_KEY"},
        "gpt-4-turbo": {"provider": "openai", "type": "chat", "context": 128000, "best_for": "legacy", "api_key_env": "OPENAI_API_KEY"},
        "gpt-5": {"provider": "openai", "type": "chat", "context": 256000, "best_for": "next_gen", "api_key_env": "OPENAI_API_KEY"},
        "dall-e-3": {"provider": "openai", "type": "image", "best_for": "images", "api_key_env": "OPENAI_API_KEY"},
        "whisper-1": {"provider": "openai", "type": "audio", "best_for": "transcription", "api_key_env": "OPENAI_API_KEY"},
        "tts-1-hd": {"provider": "openai", "type": "tts", "best_for": "speech", "api_key_env": "OPENAI_API_KEY"},
        
        # Anthropic
        "claude-3.5-sonnet": {"provider": "anthropic", "type": "chat", "context": 200000, "best_for": "coding", "api_key_env": "ANTHROPIC_API_KEY"},
        "claude-3-opus": {"provider": "anthropic", "type": "chat", "context": 200000, "best_for": "analysis", "api_key_env": "ANTHROPIC_API_KEY"},
        "claude-3-haiku": {"provider": "anthropic", "type": "chat", "context": 200000, "best_for": "fast", "api_key_env": "ANTHROPIC_API_KEY"},
        "claude-3.5-haiku": {"provider": "anthropic", "type": "chat", "context": 200000, "best_for": "balanced", "api_key_env": "ANTHROPIC_API_KEY"},
        "claude-4.5": {"provider": "anthropic", "type": "chat", "context": 500000, "best_for": "next_gen", "api_key_env": "ANTHROPIC_API_KEY"},
        
        # Google
        "gemini-2.0-flash": {"provider": "google", "type": "chat", "context": 1000000, "best_for": "speed", "api_key_env": "GOOGLE_API_KEY"},
        "gemini-2.0-pro": {"provider": "google", "type": "chat", "context": 1000000, "best_for": "multimodal", "api_key_env": "GOOGLE_API_KEY"},
        "gemini-ultra": {"provider": "google", "type": "chat", "context": 1000000, "best_for": "enterprise", "api_key_env": "GOOGLE_API_KEY"},
        "gemini-1.5-pro": {"provider": "google", "type": "chat", "context": 2000000, "best_for": "long_context", "api_key_env": "GOOGLE_API_KEY"},
        "gemini-3.0": {"provider": "google", "type": "chat", "context": 2000000, "best_for": "next_gen", "api_key_env": "GOOGLE_API_KEY"},
        "codegemma": {"provider": "google", "type": "local", "context": 8192, "best_for": "coding", "local": True},
        
        # Meta (Local via Ollama)
        "llama3.1-405b": {"provider": "meta", "type": "local", "context": 128000, "best_for": "open_source", "local": True},
        "llama3.1-70b": {"provider": "meta", "type": "local", "context": 128000, "best_for": "balanced", "local": True},
        "llama3.1-8b": {"provider": "meta", "type": "local", "context": 128000, "best_for": "lightweight", "local": True},
        "llama3.2-vision": {"provider": "meta", "type": "local", "context": 128000, "best_for": "vision", "local": True},
        "musicgen": {"provider": "meta", "type": "audio", "best_for": "music"},
        
        # Qwen (Local via Ollama)
        "qwen3": {"provider": "alibaba", "type": "local", "context": 40960, "best_for": "reasoning", "local": True},
        "qwen3-8b": {"provider": "alibaba", "type": "local", "context": 40960, "best_for": "balanced", "local": True},
        "qwen3-14b": {"provider": "alibaba", "type": "local", "context": 40960, "best_for": "quality", "local": True},
        "qwen3-32b": {"provider": "alibaba", "type": "local", "context": 40960, "best_for": "complex", "local": True},
        "qwen3-30b-a3b": {"provider": "alibaba", "type": "local", "context": 40960, "best_for": "moe", "local": True},
        "qwen2.5-coder": {"provider": "alibaba", "type": "local", "context": 32768, "best_for": "coding", "local": True},
        "qwen2.5-coder-1.5b": {"provider": "alibaba", "type": "local", "context": 32768, "best_for": "autocomplete", "local": True},
        "qwen2.5-72b": {"provider": "alibaba", "type": "local", "context": 128000, "best_for": "quality", "local": True},
        
        # DeepSeek
        "deepseek-v3": {"provider": "deepseek", "type": "api", "context": 64000, "best_for": "value", "api_key_env": "DEEPSEEK_API_KEY"},
        "deepseek-coder": {"provider": "deepseek", "type": "api", "context": 64000, "best_for": "coding", "api_key_env": "DEEPSEEK_API_KEY"},
        "deepseek-r1": {"provider": "deepseek", "type": "api", "context": 64000, "best_for": "reasoning", "api_key_env": "DEEPSEEK_API_KEY"},
        "deepseek-reasoner": {"provider": "deepseek", "type": "reasoning", "context": 128000, "best_for": "reasoning", "api_key_env": "DEEPSEEK_API_KEY"},
        
        # Mistral
        "mistral-large": {"provider": "mistral", "type": "api", "context": 128000, "best_for": "multilingual", "api_key_env": "MISTRAL_API_KEY"},
        "mistral-medium": {"provider": "mistral", "type": "api", "context": 32000, "best_for": "balanced", "api_key_env": "MISTRAL_API_KEY"},
        "codestral": {"provider": "mistral", "type": "api", "context": 32000, "best_for": "coding", "api_key_env": "MISTRAL_API_KEY"},
        "mixtral-8x22b": {"provider": "mistral", "type": "local", "context": 65536, "best_for": "moe", "local": True},
        
        # Cohere
        "command-r-plus": {"provider": "cohere", "type": "api", "context": 128000, "best_for": "rag", "api_key_env": "COHERE_API_KEY"},
        "command-r": {"provider": "cohere", "type": "api", "context": 128000, "best_for": "chat", "api_key_env": "COHERE_API_KEY"},
        
        # xAI
        "grok-2": {"provider": "xai", "type": "api", "context": 128000, "best_for": "realtime", "api_key_env": "XAI_API_KEY"},
        "grok-3": {"provider": "xai", "type": "api", "context": 128000, "best_for": "reasoning", "api_key_env": "XAI_API_KEY"},
        
        # AWS Bedrock
        "bedrock-claude": {"provider": "aws", "type": "api", "context": 200000, "best_for": "enterprise"},
        "bedrock-titan": {"provider": "aws", "type": "api", "context": 32000, "best_for": "enterprise"},
        
        # Google Vertex AI
        "vertex-gemini": {"provider": "google-cloud", "type": "api", "context": 1000000, "best_for": "enterprise"},
        "vertex-palm": {"provider": "google-cloud", "type": "api", "context": 32000, "best_for": "legacy"},
        
        # Azure OpenAI
        "azure-gpt4": {"provider": "azure", "type": "api", "context": 128000, "best_for": "enterprise"},
        "azure-gpt4o": {"provider": "azure", "type": "api", "context": 128000, "best_for": "enterprise"},
        
        # Open Source Stars
        "phi-3": {"provider": "microsoft", "type": "local", "context": 128000, "best_for": "lightweight", "local": True},
        "yi-large": {"provider": "01ai", "type": "api", "context": 200000, "best_for": "multilingual"},
        "internlm2": {"provider": "shanghai-ai", "type": "local", "context": 200000, "best_for": "chinese", "local": True},
        
        # Code Specialists
        "starcoder2": {"provider": "bigcode", "type": "local", "context": 16384, "best_for": "coding", "local": True},
        "granite-code": {"provider": "ibm", "type": "local", "context": 128000, "best_for": "enterprise_code", "local": True},
        
        # Refact.ai
        "refact-agent": {"provider": "refact", "type": "agent", "context": 32768, "best_for": "swe_bench"},
        "refact-autocomplete": {"provider": "refact", "type": "completion", "context": 8192, "best_for": "autocomplete"},
        
        # Specialized Media
        "stable-diffusion-xl": {"provider": "stability", "type": "image", "best_for": "images"},
        "flux-pro": {"provider": "black-forest", "type": "image", "best_for": "images"},
        "flux-schnell": {"provider": "black-forest", "type": "image", "best_for": "fast_images"},
        "bark": {"provider": "suno", "type": "tts", "best_for": "speech"},
        "elevenlabs": {"provider": "elevenlabs", "type": "tts", "best_for": "voice_clone", "api_key_env": "ELEVENLABS_API_KEY"},
        "xtts": {"provider": "coqui", "type": "tts", "best_for": "local_tts", "local": True},
    }
    
    TASK_RECOMMENDATIONS = {
        "coding": "claude-3.5-sonnet",
        "reasoning": "gpt-o1",
        "fast": "gemini-2.0-flash",
        "long_context": "gemini-1.5-pro",
        "images": "dall-e-3",
        "local": "qwen3",
        "local_coding": "qwen2.5-coder",
        "value": "deepseek-v3",
        "multimodal": "gpt-4o",
        "open_source": "llama3.1-70b",
        "enterprise": "azure-gpt4o",
        "voice": "elevenlabs",
        "local_voice": "xtts",
        "music": "musicgen",
        "transcription": "whisper-1",
        "swe_bench": "refact-agent",
        "autocomplete": "qwen2.5-coder-1.5b",
    }
    
    def __init__(self):
        self.config_path = Path.home() / ".noizylab" / "gabriel_collective.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
        self._ollama_available = None
    
    def _load_config(self) -> dict:
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "api_keys": {},
            "default_model": "gpt-4o",
            "preferences": {},
            "usage_stats": {}
        }
    
    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
    
    @property
    def ollama_available(self) -> bool:
        if self._ollama_available is None:
            try:
                result = subprocess.run(["ollama", "--version"], capture_output=True)
                self._ollama_available = result.returncode == 0
            except:
                self._ollama_available = False
        return self._ollama_available
    
    # ========================
    # MODEL DISCOVERY
    # ========================
    
    def list_all(self) -> List[dict]:
        """List all 65 models"""
        return [{"name": n, **m} for n, m in self.MODELS.items()]
    
    def list_by_provider(self, provider: str) -> List[dict]:
        """List models by provider"""
        return [{"name": n, **m} for n, m in self.MODELS.items() if m["provider"] == provider]
    
    def list_by_type(self, model_type: str) -> List[dict]:
        """List models by type (chat, image, audio, local, reasoning)"""
        return [{"name": n, **m} for n, m in self.MODELS.items() if m["type"] == model_type]
    
    def list_local(self) -> List[dict]:
        """List all local models (Ollama compatible)"""
        return [{"name": n, **m} for n, m in self.MODELS.items() if m.get("local")]
    
    def list_by_task(self, task: str) -> List[dict]:
        """List models best for a specific task"""
        return [{"name": n, **m} for n, m in self.MODELS.items() if m.get("best_for") == task]
    
    def get_installed_local(self) -> List[dict]:
        """Get actually installed Ollama models"""
        if not self.ollama_available:
            return []
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            models = []
            for line in result.stdout.split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    models.append({"name": parts[0], "size": parts[1]})
            return models
        except:
            return []
    
    # ========================
    # MODEL SELECTION
    # ========================
    
    def recommend(self, task: str) -> dict:
        """Get recommended model for a task"""
        model_name = self.TASK_RECOMMENDATIONS.get(task, "gpt-4o")
        model_info = self.MODELS.get(model_name, {})
        return {
            "task": task,
            "model": model_name,
            "provider": model_info.get("provider"),
            "type": model_info.get("type"),
            "context": model_info.get("context", 0),
            "local": model_info.get("local", False)
        }
    
    def get_model(self, name: str) -> Optional[dict]:
        """Get model info by name"""
        if name in self.MODELS:
            return {"name": name, **self.MODELS[name]}
        return None
    
    def auto_select(self, requirements: dict) -> str:
        """Auto-select best model based on requirements"""
        # Priority: task > local preference > context needs > default
        if requirements.get("task"):
            return self.TASK_RECOMMENDATIONS.get(requirements["task"], "gpt-4o")
        
        if requirements.get("local_only"):
            if requirements.get("coding"):
                return "qwen2.5-coder"
            return "qwen3"
        
        if requirements.get("min_context"):
            min_ctx = requirements["min_context"]
            for name, info in self.MODELS.items():
                if info.get("context", 0) >= min_ctx:
                    return name
        
        return self.config.get("default_model", "gpt-4o")
    
    # ========================
    # PROVIDER MANAGEMENT
    # ========================
    
    def get_providers(self) -> List[str]:
        """Get list of all providers"""
        return sorted(set(m["provider"] for m in self.MODELS.values()))
    
    def provider_stats(self) -> dict:
        """Get stats per provider"""
        stats = {}
        for name, info in self.MODELS.items():
            provider = info["provider"]
            if provider not in stats:
                stats[provider] = {"count": 0, "models": [], "types": set()}
            stats[provider]["count"] += 1
            stats[provider]["models"].append(name)
            stats[provider]["types"].add(info["type"])
        
        # Convert sets to lists for JSON serialization
        for p in stats:
            stats[p]["types"] = list(stats[p]["types"])
        return stats
    
    # ========================
    # CONFIGURATION
    # ========================
    
    def set_api_key(self, provider: str, key: str):
        """Store API key for a provider"""
        self.config["api_keys"][provider] = key
        self._save_config()
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key (config or env)"""
        if provider in self.config["api_keys"]:
            return self.config["api_keys"][provider]
        
        # Check environment variables
        env_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "cohere": "COHERE_API_KEY",
            "elevenlabs": "ELEVENLABS_API_KEY",
        }
        env_var = env_map.get(provider)
        if env_var:
            return os.environ.get(env_var)
        return None
    
    def set_default_model(self, model: str):
        """Set default model"""
        if model in self.MODELS:
            self.config["default_model"] = model
            self._save_config()
    
    # ========================
    # STATISTICS
    # ========================
    
    def stats(self) -> dict:
        """Get collective statistics"""
        providers = set(m["provider"] for m in self.MODELS.values())
        types = set(m["type"] for m in self.MODELS.values())
        local_count = len([m for m in self.MODELS.values() if m.get("local")])
        installed = len(self.get_installed_local())
        
        return {
            "total_models": len(self.MODELS),
            "total_providers": len(providers),
            "providers": sorted(providers),
            "types": sorted(types),
            "local_models": local_count,
            "installed_local": installed,
            "ollama_available": self.ollama_available,
            "default_model": self.config.get("default_model", "gpt-4o"),
            "tasks_supported": len(self.TASK_RECOMMENDATIONS)
        }
    
    def track_usage(self, model: str, tokens: int = 0):
        """Track model usage for analytics"""
        if "usage_stats" not in self.config:
            self.config["usage_stats"] = {}
        if model not in self.config["usage_stats"]:
            self.config["usage_stats"][model] = {"calls": 0, "tokens": 0}
        self.config["usage_stats"][model]["calls"] += 1
        self.config["usage_stats"][model]["tokens"] += tokens
        self._save_config()


class Qwen3Client:
    """Qwen3 integration for GABRIEL - Thinking Mode Support"""
    
    MODELS = {
        "qwen3": "qwen3",
        "qwen3-8b": "qwen3:8b",
        "qwen3-14b": "qwen3:14b",
        "qwen3-32b": "qwen3:32b",
        "qwen3-30b-a3b": "qwen3:30b-a3b",
    }
    
    SETTINGS = {
        "thinking": {"temperature": 0.7, "top_p": 0.8, "top_k": 20},
        "non_thinking": {"temperature": 0.6, "top_p": 0.95, "top_k": 20}
    }
    
    def __init__(self, model: str = "qwen3"):
        self.model = self.MODELS.get(model, model)
        self.thinking_mode = True
    
    def chat(self, prompt: str, thinking: bool = None) -> dict:
        """Chat with Qwen3 via Ollama"""
        if thinking is None:
            thinking = self.thinking_mode
        
        mode_prefix = "/think\n" if thinking else "/no_think\n"
        full_prompt = mode_prefix + prompt
        settings = self.SETTINGS["thinking" if thinking else "non_thinking"]
        
        try:
            cmd = ["ollama", "run", self.model, "--temperature", str(settings["temperature"]), full_prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            response = result.stdout.strip()
            
            # Parse thinking blocks
            think_content = ""
            answer = response
            if "<think>" in response and "</think>" in response:
                import re
                match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
                if match:
                    think_content = match.group(1).strip()
                    answer = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
            
            return {
                "model": self.model,
                "thinking_mode": thinking,
                "thinking": think_content,
                "response": answer,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def think(self, prompt: str) -> dict:
        """Force thinking mode"""
        return self.chat(prompt, thinking=True)
    
    def fast(self, prompt: str) -> dict:
        """Force non-thinking (fast) mode"""
        return self.chat(prompt, thinking=False)


class LocalLLMRunner:
    """Run any local LLM via Ollama"""
    
    def __init__(self):
        self._available = None
    
    @property
    def available(self) -> bool:
        if self._available is None:
            try:
                result = subprocess.run(["ollama", "--version"], capture_output=True)
                self._available = result.returncode == 0
            except:
                self._available = False
        return self._available
    
    def list_models(self) -> List[dict]:
        """List installed models"""
        if not self.available:
            return []
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            models = []
            for line in result.stdout.split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    models.append({"name": parts[0], "size": parts[1]})
            return models
        except:
            return []
    
    def run(self, model: str, prompt: str, timeout: int = 120) -> str:
        """Run a model with prompt"""
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip()
        except:
            return ""
    
    def pull(self, model: str) -> bool:
        """Pull a model from Ollama"""
        try:
            subprocess.run(["ollama", "pull", model], check=True)
            return True
        except:
            return False


# ========================
# GABRIEL INTEGRATION API
# ========================

class GabrielKnowledge:
    """High-level API for GABRIEL to access all collective knowledge"""
    
    def __init__(self):
        self.collective = NOIZYCollective()
        self.qwen = Qwen3Client()
        self.local = LocalLLMRunner()
        self._initialized = datetime.now()
    
    def get_best_model(self, task: str = None, local_only: bool = False) -> str:
        """Get best model for current needs"""
        if local_only:
            return "qwen3" if task != "coding" else "qwen2.5-coder"
        if task:
            return self.collective.recommend(task)["model"]
        return self.collective.config.get("default_model", "gpt-4o")
    
    def query_local(self, prompt: str, model: str = None, thinking: bool = True) -> dict:
        """Query local LLM with optional thinking"""
        if model is None or "qwen" in model.lower():
            return self.qwen.chat(prompt, thinking=thinking)
        return {"response": self.local.run(model or "qwen3", prompt), "success": True}
    
    def get_stats(self) -> dict:
        """Get full system stats"""
        stats = self.collective.stats()
        stats["initialized"] = self._initialized.isoformat()
        stats["installed_models"] = self.local.list_models()
        return stats
    
    def list_capabilities(self) -> dict:
        """List all GABRIEL capabilities from collective"""
        return {
            "models": len(self.collective.MODELS),
            "providers": len(self.collective.get_providers()),
            "tasks": list(self.collective.TASK_RECOMMENDATIONS.keys()),
            "local_available": self.local.available,
            "features": [
                "65 AI models across 23 providers",
                "Automatic model selection by task",
                "Local LLM support via Ollama",
                "Qwen3 thinking mode integration",
                "Enterprise cloud support (AWS, Azure, GCP)",
                "Code specialists (CodeGemma, StarCoder2, Codestral)",
                "Voice synthesis (ElevenLabs, XTTS, Bark)",
                "Image generation (DALL-E 3, Flux, SDXL)",
                "Usage tracking and analytics"
            ]
        }


# Singleton instance for GABRIEL
_gabriel_knowledge = None

def get_knowledge() -> GabrielKnowledge:
    """Get or create GABRIEL knowledge instance"""
    global _gabriel_knowledge
    if _gabriel_knowledge is None:
        _gabriel_knowledge = GabrielKnowledge()
    return _gabriel_knowledge


if __name__ == "__main__":
    # Test the integration
    k = get_knowledge()
    print("\n🌐 NOIZY.ai COLLECTIVE - GABRIEL INTEGRATION\n")
    
    stats = k.get_stats()
    print(f"  Total Models:     {stats['total_models']}")
    print(f"  Total Providers:  {stats['total_providers']}")
    print(f"  Local Available:  {stats['ollama_available']}")
    print(f"  Installed Local:  {stats['installed_local']}")
    
    print("\n📋 TASK RECOMMENDATIONS:")
    for task in ["coding", "reasoning", "fast", "local", "voice"]:
        rec = k.collective.recommend(task)
        print(f"  {task:<12} → {rec['model']}")
    
    print("\n✅ GABRIEL Knowledge Module Ready!")

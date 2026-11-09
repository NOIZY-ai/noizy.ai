"""
AI GENERATORS v2.0 - GORUNFREE EDITION
Unified interface for multiple AI providers
"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional, Any
from dataclasses import dataclass


def _get_env_key(*names: str) -> Optional[str]:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


@dataclass
class GeneratorConfig:
    """Configuration for AI generators"""
    gemini_key: Optional[str] = None
    claude_key: Optional[str] = None
    openai_key: Optional[str] = None
    nvidia_key: Optional[str] = None
    deepseek_key: Optional[str] = None


class AIGenerator:
    """Unified AI text generation across providers"""
    
    def __init__(self, config: Optional[GeneratorConfig] = None):
        if config is None:
            config = GeneratorConfig(
                gemini_key=_get_env_key("GEMINI_API_KEY", "GOOGLE_API_KEY"),
                claude_key=os.environ.get("ANTHROPIC_API_KEY"),
                openai_key=os.environ.get("OPENAI_API_KEY"),
                nvidia_key=os.environ.get("NVIDIA_API_KEY"),
                deepseek_key=os.environ.get("DEEPSEEK_API_KEY"),
            )
        else:
            if not config.gemini_key:
                config.gemini_key = _get_env_key("GEMINI_API_KEY", "GOOGLE_API_KEY")
            if not config.claude_key:
                config.claude_key = os.environ.get("ANTHROPIC_API_KEY")
            if not config.openai_key:
                config.openai_key = os.environ.get("OPENAI_API_KEY")
            if not config.nvidia_key:
                config.nvidia_key = os.environ.get("NVIDIA_API_KEY")
            if not config.deepseek_key:
                config.deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        self.config = config
    
    def generate(
        self,
        prompt: str,
        provider: str = "Gemini",
        system_prompt: str = "",
        max_tokens: int = 1024
    ) -> str:
        """Generate text using specified provider"""
        
        providers = {
            "Gemini": self._generate_gemini,
            "Claude": self._generate_claude,
            "OpenAI": self._generate_openai,
            "NVIDIA": self._generate_nvidia,
            "DeepSeek": self._generate_deepseek,
        }
        
        generator = providers.get(provider)
        if not generator:
            return f"⚠️ Unknown provider: {provider}"
        
        try:
            return generator(prompt, system_prompt, max_tokens)
        except Exception as e:
            return f"⚠️ {provider} error: {e}"
    
    def _generate_gemini(self, prompt: str, system: str, max_tokens: int) -> str:
        """Generate with Google Gemini"""
        if not self.config.gemini_key:
            return "⚠️ Missing Gemini API key"
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            return model.generate_content(full_prompt).text
        except ImportError:
            return "⚠️ google-generativeai not installed"
    
    def _generate_claude(self, prompt: str, system: str, max_tokens: int) -> str:
        """Generate with Anthropic Claude"""
        if not self.config.claude_key:
            return "⚠️ Missing Claude API key"
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.config.claude_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": full_prompt}]
        }
        
        return self._http_post(url, headers, data, lambda r: r['content'][0]['text'])
    
    def _generate_openai(self, prompt: str, system: str, max_tokens: int) -> str:
        """Generate with OpenAI GPT-4"""
        if not self.config.openai_key:
            return "⚠️ Missing OpenAI API key"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.openai_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        data = {"model": "gpt-4o", "messages": messages, "max_tokens": max_tokens}
        return self._http_post(url, headers, data, lambda r: r['choices'][0]['message']['content'])
    
    def _generate_nvidia(self, prompt: str, system: str, max_tokens: int) -> str:
        """Generate with NVIDIA Nemotron"""
        if not self.config.nvidia_key:
            return "⚠️ Missing NVIDIA API key"
        
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.nvidia_key}",
            "Content-Type": "application/json"
        }
        
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        data = {
            "model": "nvidia/llama-3.1-nemotron-70b-instruct",
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": max_tokens
        }
        
        return self._http_post(url, headers, data, lambda r: r['choices'][0]['message']['content'])
    
    def _generate_deepseek(self, prompt: str, system: str, max_tokens: int) -> str:
        """Generate with DeepSeek"""
        if not self.config.deepseek_key:
            return "⚠️ Missing DeepSeek API key"
        
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.deepseek_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        data = {"model": "deepseek-chat", "messages": messages, "max_tokens": max_tokens}
        return self._http_post(url, headers, data, lambda r: r['choices'][0]['message']['content'])
    
    def _http_post(self, url: str, headers: dict, data: dict, extractor: Any) -> str:
        """Helper for HTTP POST requests"""
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                return extractor(result)
        except urllib.error.HTTPError as e:
            return f"⚠️ HTTP {e.code}: {e.reason}"
        except Exception as e:
            raise

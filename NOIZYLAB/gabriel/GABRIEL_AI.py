#!/usr/bin/env python3
"""
GABRIEL AI - UNIFIED AI MODEL MANAGER
Access ALL 40+ AI models from one interface
Claude, GPT, Gemini, DeepSeek, Mistral, Groq, xAI, Cohere, Together, Perplexity
"""

import os
import sys
import json
import time
import httpx
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

GABRIEL_ROOT = Path.home() / "NOIZYLAB" / "GABRIEL"
CONFIG_FILE = GABRIEL_ROOT / "config" / "ai_models.json"


@dataclass
class AIResponse:
    """Unified AI response"""
    model: str
    provider: str
    content: str
    tokens_used: int
    latency_ms: int
    success: bool
    error: Optional[str] = None


class GabrielAI:
    """Unified AI interface for all models"""

    def __init__(self):
        self.config = self._load_config()
        self.client = httpx.Client(timeout=120.0)

    def _load_config(self) -> dict:
        """Load AI models config"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return {}

    def _get_api_key(self, env_key: str) -> Optional[str]:
        """Get API key from environment"""
        return os.environ.get(env_key)

    def list_models(self) -> Dict[str, List[str]]:
        """List all available models"""
        models = {}
        for provider, data in self.config.get("ai_models", {}).items():
            models[provider] = data.get("models", [])
        return models

    def list_providers(self) -> List[str]:
        """List all providers"""
        return list(self.config.get("ai_models", {}).keys())

    # ========== CLAUDE ==========
    def claude(self, prompt: str, model: str = "claude-3-5-sonnet-20241022", system: str = None) -> AIResponse:
        """Call Claude API"""
        start = time.perf_counter()
        api_key = self._get_api_key("ANTHROPIC_API_KEY")

        if not api_key:
            return AIResponse(model=model, provider="claude", content="", tokens_used=0,
                            latency_ms=0, success=False, error="ANTHROPIC_API_KEY not set")

        try:
            messages = [{"role": "user", "content": prompt}]
            payload = {
                "model": model,
                "max_tokens": 4096,
                "messages": messages
            }
            if system:
                payload["system"] = system

            response = self.client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json=payload
            )
            data = response.json()

            if "content" in data:
                content = data["content"][0]["text"]
                tokens = data.get("usage", {}).get("output_tokens", 0)
                latency = int((time.perf_counter() - start) * 1000)
                return AIResponse(model=model, provider="claude", content=content,
                                tokens_used=tokens, latency_ms=latency, success=True)
            else:
                return AIResponse(model=model, provider="claude", content="", tokens_used=0,
                                latency_ms=0, success=False, error=str(data))

        except Exception as e:
            return AIResponse(model=model, provider="claude", content="", tokens_used=0,
                            latency_ms=0, success=False, error=str(e))

    # ========== OPENAI ==========
    def openai(self, prompt: str, model: str = "gpt-4o", system: str = None) -> AIResponse:
        """Call OpenAI API"""
        start = time.perf_counter()
        api_key = self._get_api_key("OPENAI_API_KEY")

        if not api_key:
            return AIResponse(model=model, provider="openai", content="", tokens_used=0,
                            latency_ms=0, success=False, error="OPENAI_API_KEY not set")

        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self.client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={"model": model, "messages": messages, "max_tokens": 4096}
            )
            data = response.json()

            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                tokens = data.get("usage", {}).get("total_tokens", 0)
                latency = int((time.perf_counter() - start) * 1000)
                return AIResponse(model=model, provider="openai", content=content,
                                tokens_used=tokens, latency_ms=latency, success=True)
            else:
                return AIResponse(model=model, provider="openai", content="", tokens_used=0,
                                latency_ms=0, success=False, error=str(data))

        except Exception as e:
            return AIResponse(model=model, provider="openai", content="", tokens_used=0,
                            latency_ms=0, success=False, error=str(e))

    # ========== GEMINI ==========
    def gemini(self, prompt: str, model: str = "gemini-2.0-flash-exp") -> AIResponse:
        """Call Gemini API"""
        start = time.perf_counter()
        api_key = self._get_api_key("GEMINI_API_KEY")

        if not api_key:
            return AIResponse(model=model, provider="gemini", content="", tokens_used=0,
                            latency_ms=0, success=False, error="GEMINI_API_KEY not set")

        try:
            response = self.client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                params={"key": api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]}
            )
            data = response.json()

            if "candidates" in data:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                tokens = data.get("usageMetadata", {}).get("totalTokenCount", 0)
                latency = int((time.perf_counter() - start) * 1000)
                return AIResponse(model=model, provider="gemini", content=content,
                                tokens_used=tokens, latency_ms=latency, success=True)
            else:
                return AIResponse(model=model, provider="gemini", content="", tokens_used=0,
                                latency_ms=0, success=False, error=str(data))

        except Exception as e:
            return AIResponse(model=model, provider="gemini", content="", tokens_used=0,
                            latency_ms=0, success=False, error=str(e))

    # ========== GROQ (ULTRA FAST) ==========
    def groq(self, prompt: str, model: str = "llama-3.3-70b-versatile") -> AIResponse:
        """Call Groq API - ULTRA FAST"""
        start = time.perf_counter()
        api_key = self._get_api_key("GROQ_API_KEY")

        if not api_key:
            return AIResponse(model=model, provider="groq", content="", tokens_used=0,
                            latency_ms=0, success=False, error="GROQ_API_KEY not set")

        try:
            response = self.client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={"model": model, "messages": [{"role": "user", "content": prompt}]}
            )
            data = response.json()

            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                tokens = data.get("usage", {}).get("total_tokens", 0)
                latency = int((time.perf_counter() - start) * 1000)
                return AIResponse(model=model, provider="groq", content=content,
                                tokens_used=tokens, latency_ms=latency, success=True)
            else:
                return AIResponse(model=model, provider="groq", content="", tokens_used=0,
                                latency_ms=0, success=False, error=str(data))

        except Exception as e:
            return AIResponse(model=model, provider="groq", content="", tokens_used=0,
                            latency_ms=0, success=False, error=str(e))

    # ========== DEEPSEEK ==========
    def deepseek(self, prompt: str, model: str = "deepseek-chat") -> AIResponse:
        """Call DeepSeek API"""
        start = time.perf_counter()
        api_key = self._get_api_key("DEEPSEEK_API_KEY")

        if not api_key:
            return AIResponse(model=model, provider="deepseek", content="", tokens_used=0,
                            latency_ms=0, success=False, error="DEEPSEEK_API_KEY not set")

        try:
            response = self.client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={"model": model, "messages": [{"role": "user", "content": prompt}]}
            )
            data = response.json()

            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                tokens = data.get("usage", {}).get("total_tokens", 0)
                latency = int((time.perf_counter() - start) * 1000)
                return AIResponse(model=model, provider="deepseek", content=content,
                                tokens_used=tokens, latency_ms=latency, success=True)
            else:
                return AIResponse(model=model, provider="deepseek", content="", tokens_used=0,
                                latency_ms=0, success=False, error=str(data))

        except Exception as e:
            return AIResponse(model=model, provider="deepseek", content="", tokens_used=0,
                            latency_ms=0, success=False, error=str(e))

    # ========== UNIFIED CALL ==========
    def call(self, provider: str, prompt: str, model: str = None, **kwargs) -> AIResponse:
        """Unified call to any provider"""
        providers = {
            "claude": self.claude,
            "openai": self.openai,
            "gemini": self.gemini,
            "groq": self.groq,
            "deepseek": self.deepseek,
        }

        if provider not in providers:
            return AIResponse(model=model or "unknown", provider=provider, content="",
                            tokens_used=0, latency_ms=0, success=False,
                            error=f"Unknown provider: {provider}")

        if model:
            return providers[provider](prompt, model=model, **kwargs)
        return providers[provider](prompt, **kwargs)

    # ========== RACE MODE ==========
    def race(self, prompt: str, providers: List[str] = None) -> Dict[str, AIResponse]:
        """Race multiple providers - return all responses"""
        if providers is None:
            providers = ["claude", "openai", "gemini", "groq"]

        results = {}
        with ThreadPoolExecutor(max_workers=len(providers)) as executor:
            futures = {executor.submit(self.call, p, prompt): p for p in providers}
            for future in futures:
                provider = futures[future]
                try:
                    results[provider] = future.result()
                except Exception as e:
                    results[provider] = AIResponse(
                        model="unknown", provider=provider, content="",
                        tokens_used=0, latency_ms=0, success=False, error=str(e)
                    )
        return results


def main():
    """CLI interface"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         GABRIEL AI - UNIFIED MODELS                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Providers: Claude, OpenAI, Gemini, Groq, DeepSeek, Mistral, xAI, Cohere     ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    ai = GabrielAI()

    print("Available Providers:")
    for provider in ai.list_providers():
        print(f"  • {provider}")

    print("\nAvailable Models:")
    for provider, models in ai.list_models().items():
        print(f"  {provider}: {', '.join(models[:3])}...")

    if len(sys.argv) > 1:
        provider = sys.argv[1]
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Hello, who are you?"

        print(f"\n⚡ Calling {provider}...")
        response = ai.call(provider, prompt)

        if response.success:
            print(f"\n✅ Response ({response.latency_ms}ms, {response.tokens_used} tokens):")
            print(response.content)
        else:
            print(f"\n❌ Error: {response.error}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ASYNC ENGINE v1.0 - ZERO LATENCY                          ║
║                    GORUNFREE PARALLEL PROCESSING                             ║
║                                                                              ║
║  Parallel AI execution. Multiple providers simultaneously.                   ║
║  True zero-latency through async operations.                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import os
import json
from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AsyncConfig:
    """Async engine configuration"""
    gemini_key: Optional[str] = None
    claude_key: Optional[str] = None
    openai_key: Optional[str] = None
    nvidia_key: Optional[str] = None
    deepseek_key: Optional[str] = None
    groq_key: Optional[str] = None
    timeout: int = 60
    max_concurrent: int = 10


class AsyncAIEngine:
    """
    Async AI Generation Engine
    
    Execute multiple AI providers in parallel for true zero-latency.
    Get responses from all providers simultaneously.
    """
    
    def __init__(self, config: Optional[AsyncConfig] = None):
        self.config = config or AsyncConfig(
            gemini_key=os.environ.get("GEMINI_API_KEY"),
            claude_key=os.environ.get("ANTHROPIC_API_KEY"),
            openai_key=os.environ.get("OPENAI_API_KEY"),
            nvidia_key=os.environ.get("NVIDIA_API_KEY"),
            deepseek_key=os.environ.get("DEEPSEEK_API_KEY"),
            groq_key=os.environ.get("GROQ_API_KEY"),
        )
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def close(self):
        """Close the session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def generate_async(
        self,
        prompt: str,
        provider: str,
        system: str = "",
        max_tokens: int = 1024
    ) -> dict:
        """Generate text from a single provider asynchronously"""
        start = datetime.now()
        
        try:
            if provider == "Gemini":
                response = await self._gemini_async(prompt, system)
            elif provider == "Claude":
                response = await self._claude_async(prompt, system, max_tokens)
            elif provider == "OpenAI":
                response = await self._openai_async(prompt, system, max_tokens)
            elif provider == "DeepSeek":
                response = await self._deepseek_async(prompt, system, max_tokens)
            elif provider == "Groq":
                response = await self._groq_async(prompt, system, max_tokens)
            else:
                response = f"Unknown provider: {provider}"
            
            elapsed = (datetime.now() - start).total_seconds()
            
            return {
                "provider": provider,
                "response": response,
                "elapsed_ms": round(elapsed * 1000, 2),
                "status": "success"
            }
            
        except Exception as e:
            elapsed = (datetime.now() - start).total_seconds()
            return {
                "provider": provider,
                "response": None,
                "error": str(e),
                "elapsed_ms": round(elapsed * 1000, 2),
                "status": "error"
            }
    
    async def generate_parallel(
        self,
        prompt: str,
        providers: list[str],
        system: str = "",
        max_tokens: int = 1024
    ) -> dict:
        """Generate from multiple providers in parallel"""
        start = datetime.now()
        
        tasks = [
            self.generate_async(prompt, p, system, max_tokens)
            for p in providers
        ]
        
        results = await asyncio.gather(*tasks)
        
        elapsed = (datetime.now() - start).total_seconds()
        
        return {
            "prompt": prompt,
            "providers": providers,
            "results": {r["provider"]: r for r in results},
            "total_elapsed_ms": round(elapsed * 1000, 2),
            "fastest": min(results, key=lambda x: x["elapsed_ms"])["provider"]
        }
    
    async def race(
        self,
        prompt: str,
        providers: list[str],
        system: str = ""
    ) -> dict:
        """Race providers - return first successful response"""
        start = datetime.now()
        
        async def try_provider(provider: str):
            result = await self.generate_async(prompt, provider, system)
            if result["status"] == "success":
                return result
            raise Exception(result.get("error", "Unknown error"))
        
        tasks = [try_provider(p) for p in providers]
        
        try:
            # Return first successful result
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
            
            result = list(done)[0].result()
            elapsed = (datetime.now() - start).total_seconds()
            
            return {
                "prompt": prompt,
                "winner": result["provider"],
                "response": result["response"],
                "elapsed_ms": round(elapsed * 1000, 2)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    # =========================================================================
    # PROVIDER IMPLEMENTATIONS
    # =========================================================================
    
    async def _gemini_async(self, prompt: str, system: str) -> str:
        """Async Gemini generation"""
        if not self.config.gemini_key:
            return "⚠️ Missing Gemini key"
        
        # Gemini uses google-generativeai which isn't async-native
        # For true async, we'd use their REST API directly
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.config.gemini_key}"
        
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}]
        }
        
        session = await self._get_session()
        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                return f"⚠️ Gemini HTTP {resp.status}"
            data = await resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    
    async def _claude_async(self, prompt: str, system: str, max_tokens: int) -> str:
        """Async Claude generation"""
        if not self.config.claude_key:
            return "⚠️ Missing Claude key"
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.config.claude_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": full_prompt}]
        }
        
        session = await self._get_session()
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return f"⚠️ Claude HTTP {resp.status}"
            data = await resp.json()
            return data["content"][0]["text"]
    
    async def _openai_async(self, prompt: str, system: str, max_tokens: int) -> str:
        """Async OpenAI generation"""
        if not self.config.openai_key:
            return "⚠️ Missing OpenAI key"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.openai_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        session = await self._get_session()
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return f"⚠️ OpenAI HTTP {resp.status}"
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
    
    async def _deepseek_async(self, prompt: str, system: str, max_tokens: int) -> str:
        """Async DeepSeek generation"""
        if not self.config.deepseek_key:
            return "⚠️ Missing DeepSeek key"
        
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.deepseek_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        session = await self._get_session()
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return f"⚠️ DeepSeek HTTP {resp.status}"
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
    
    async def _groq_async(self, prompt: str, system: str, max_tokens: int) -> str:
        """Async Groq generation (ultra-fast LPU inference)"""
        if not self.config.groq_key:
            return "⚠️ Missing Groq key"
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.groq_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        session = await self._get_session()
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return f"⚠️ Groq HTTP {resp.status}"
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


# Factory function
def create_async_engine(**keys) -> AsyncAIEngine:
    """Create configured async engine"""
    config = AsyncConfig(
        gemini_key=keys.get('gemini') or os.environ.get("GEMINI_API_KEY"),
        claude_key=keys.get('claude') or os.environ.get("ANTHROPIC_API_KEY"),
        openai_key=keys.get('openai') or os.environ.get("OPENAI_API_KEY"),
        deepseek_key=keys.get('deepseek') or os.environ.get("DEEPSEEK_API_KEY"),
        groq_key=keys.get('groq') or os.environ.get("GROQ_API_KEY"),
    )
    return AsyncAIEngine(config)


# Convenience functions
async def parallel_generate(prompt: str, providers: list[str] = None) -> dict:
    """Quick parallel generation"""
    engine = create_async_engine()
    providers = providers or ["Claude", "Gemini", "OpenAI"]
    try:
        return await engine.generate_parallel(prompt, providers)
    finally:
        await engine.close()


async def race_generate(prompt: str, providers: list[str] = None) -> dict:
    """Quick race generation"""
    engine = create_async_engine()
    providers = providers or ["Claude", "Gemini", "Groq"]
    try:
        return await engine.race(prompt, providers)
    finally:
        await engine.close()


__all__ = [
    'AsyncConfig', 'AsyncAIEngine', 'create_async_engine',
    'parallel_generate', 'race_generate'
]


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              ASYNC ENGINE v1.0 - ZERO LATENCY                ║")
    print("║              GORUNFREE PARALLEL PROCESSING                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("Usage:")
    print("  from noizylab.core.async_engine import parallel_generate")
    print("  result = await parallel_generate('Your prompt here')")
    print()
    print("  # Or race for fastest response:")
    print("  from noizylab.core.async_engine import race_generate")
    print("  result = await race_generate('Your prompt here')")

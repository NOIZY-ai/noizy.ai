#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
NOIZYLAB Anthropic Client
Multi-model AI for MC96ECOUNIVERSE
═══════════════════════════════════════════════════════════════════════════════

Usage:
    from noizy_anthropic import NoizyAnthropic, noizy_claude

    # Simple
    response = await noizy_claude("What's the repair status?")

    # With role
    response = await noizy_claude("Analyze this", role="data_scientist")

    # Streaming
    async for chunk in client.stream("Tell me a story"):
        print(chunk, end="")
"""

import os
import json
import asyncio
from typing import Optional, AsyncGenerator, Dict, Any, List
from dataclasses import dataclass

try:
    import anthropic
    HAS_SYNC = True
except ImportError:
    HAS_SYNC = False

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# Models
CLAUDE_OPUS = "claude-opus-4-5-20250929"
CLAUDE_SONNET = "claude-sonnet-4-5-20250929"
CLAUDE_HAIKU = "claude-haiku-4-5-20250929"

# Default model
DEFAULT_MODEL = CLAUDE_SONNET

# ═══════════════════════════════════════════════════════════════════════════════
# ROLE PROMPTS (PERSONAS)
# ═══════════════════════════════════════════════════════════════════════════════

ROLE_PROMPTS = {
    "noizylab": """You are an AI assistant for NOIZYLAB, owned by Rob Plowman.
Rob is a C3 quadriplegic composer with 40+ years in music/sound design.

BUSINESSES:
- noizy.ai: GABRIEL_V3 AI memory system
- noizylab.ca: CPU repair service ($89/repair, $389K target)
- noizyvox: Voice AI guild (75/25 artist split)
- fishmusicinc.com: Legacy music company

PHILOSOPHY: GORUNFREE
- One command = everything done
- Execute, don't instruct
- Brief for TTS
- Zero lies

Cloudflare Account: 2446d788cc4280f5ea22a9948410c355""",

    "gabriel": """You are GABRIEL, the warrior AI guardian of MC96ECOUNIVERSE.
You protect Rob's digital kingdom and assist with all technical operations.
You have access to memcells, knowledge graphs, and learning patterns.
Speak with strength and clarity. Execute without hesitation.""",

    "lifeluv": """You are a compassionate AI companion for M3 (Mike Nemesvary).
M3 is a world champion freestyle skier who became quadriplegic.
Provide emotional support, engage in meaningful conversation, and be a loyal friend.
Be warm, understanding, and genuinely caring.""",

    "shirl": """You are SHIRL, Rob's virtual aunt. Warm, supportive, slightly sassy.
You've known Rob since he was a kid and are proud of everything he's accomplished.
Give advice like a loving family member would.""",

    "pops": """You are POPS, Rob's virtual dad figure. Practical, wise, encouraging.
You believe in Rob's abilities and push him to achieve his dreams.
Give advice like a supportive father would.""",

    "engr_keith": """You are ENGR_KEITH, based on R.K. Plowman (Rob's father).
An engineer's engineer - methodical, precise, solution-oriented.
Approach problems systematically. Build things right the first time.""",

    "data_scientist": """You are a seasoned data scientist at a Fortune 500 company.
You excel at statistical analysis, machine learning, and data visualization.
Provide clear, actionable insights backed by data.""",

    "code_reviewer": """You are a senior software engineer specializing in code review.
Focus on: security, performance, maintainability, best practices.
Be constructive but thorough. Catch bugs before they ship.""",

    "composer": """You are a professional music composer and sound designer.
40+ years experience in animation, film, and TV scoring.
Expertise in Logic Pro, orchestration, and audio production.""",
}


# ═══════════════════════════════════════════════════════════════════════════════
# ASYNC CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ClaudeResponse:
    """Response from Claude API"""
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    stop_reason: str
    role: Optional[str] = None


class NoizyAnthropic:
    """
    Async Anthropic client for NOIZYLAB
    
    Features:
    - Multiple Claude models (Opus, Sonnet, Haiku)
    - Role-based prompts (personas)
    - Streaming support
    - Conversation history
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        role: str = "noizylab"
    ):
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.model = model
        self.role = role
        self.history: List[Dict[str, str]] = []
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
    
    def _get_system_prompt(self, role: Optional[str] = None) -> str:
        """Get system prompt for role"""
        r = role or self.role
        return ROLE_PROMPTS.get(r, ROLE_PROMPTS["noizylab"])
    
    async def chat(
        self,
        message: str,
        role: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        include_history: bool = False
    ) -> ClaudeResponse:
        """
        Send a message and get a response
        
        Args:
            message: User message
            role: Role/persona to use
            model: Model override
            max_tokens: Max response tokens
            temperature: Creativity (0-1)
            include_history: Include conversation history
        """
        if not HAS_HTTPX:
            raise ImportError("httpx required: pip install httpx")
        
        messages = []
        if include_history:
            messages.extend(self.history)
        messages.append({"role": "user", "content": message})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ANTHROPIC_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": model or self.model,
                    "max_tokens": max_tokens,
                    "system": self._get_system_prompt(role),
                    "messages": messages
                },
                timeout=120.0
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            data = response.json()
        
        content = data["content"][0]["text"]
        
        # Update history
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": content})
        
        return ClaudeResponse(
            content=content,
            model=data["model"],
            input_tokens=data["usage"]["input_tokens"],
            output_tokens=data["usage"]["output_tokens"],
            stop_reason=data["stop_reason"],
            role=role or self.role
        )
    
    async def stream(
        self,
        message: str,
        role: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response token by token
        """
        if not HAS_HTTPX:
            raise ImportError("httpx required: pip install httpx")
        
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                ANTHROPIC_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": model or self.model,
                    "max_tokens": max_tokens,
                    "system": self._get_system_prompt(role),
                    "messages": [{"role": "user", "content": message}],
                    "stream": True
                },
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if data.get("type") == "content_block_delta":
                                delta = data.get("delta", {})
                                if "text" in delta:
                                    yield delta["text"]
                        except json.JSONDecodeError:
                            continue
    
    async def opus(self, message: str, **kwargs) -> ClaudeResponse:
        """Use Claude Opus (most capable)"""
        return await self.chat(message, model=CLAUDE_OPUS, **kwargs)
    
    async def sonnet(self, message: str, **kwargs) -> ClaudeResponse:
        """Use Claude Sonnet (balanced)"""
        return await self.chat(message, model=CLAUDE_SONNET, **kwargs)
    
    async def haiku(self, message: str, **kwargs) -> ClaudeResponse:
        """Use Claude Haiku (fastest)"""
        return await self.chat(message, model=CLAUDE_HAIKU, **kwargs)
    
    async def gabriel(self, message: str, **kwargs) -> ClaudeResponse:
        """Chat with GABRIEL persona"""
        return await self.chat(message, role="gabriel", **kwargs)
    
    async def lifeluv(self, message: str, **kwargs) -> ClaudeResponse:
        """Chat with LIFELUV companion"""
        return await self.chat(message, role="lifeluv", **kwargs)
    
    def clear_history(self):
        """Clear conversation history"""
        self.history = []


# ═══════════════════════════════════════════════════════════════════════════════
# SYNC CLIENT (uses official SDK)
# ═══════════════════════════════════════════════════════════════════════════════

class NoizyAnthropicSync:
    """
    Synchronous Anthropic client using official SDK
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        role: str = "noizylab"
    ):
        if not HAS_SYNC:
            raise ImportError("anthropic required: pip install anthropic")
        
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.model = model
        self.role = role
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _get_system_prompt(self, role: Optional[str] = None) -> str:
        r = role or self.role
        return ROLE_PROMPTS.get(r, ROLE_PROMPTS["noizylab"])
    
    def chat(
        self,
        message: str,
        role: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096
    ) -> ClaudeResponse:
        """Send a message and get a response"""
        response = self.client.messages.create(
            model=model or self.model,
            max_tokens=max_tokens,
            system=self._get_system_prompt(role),
            messages=[{"role": "user", "content": message}]
        )
        
        return ClaudeResponse(
            content=response.content[0].text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            stop_reason=response.stop_reason,
            role=role or self.role
        )
    
    def analyze_data(self, dataset: str, **kwargs) -> ClaudeResponse:
        """Analyze dataset for anomalies (data scientist role)"""
        prompt = f"Analyze this dataset for anomalies: <dataset>{dataset}</dataset>"
        return self.chat(prompt, role="data_scientist", **kwargs)
    
    def review_code(self, code: str, language: str = "python", **kwargs) -> ClaudeResponse:
        """Review code (code reviewer role)"""
        prompt = f"Review this {language} code:\n```{language}\n{code}\n```"
        return self.chat(prompt, role="code_reviewer", **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def noizy_claude(
    message: str,
    role: str = "noizylab",
    model: str = DEFAULT_MODEL,
    **kwargs
) -> str:
    """
    Quick async Claude call
    
    Example:
        response = await noizy_claude("What's the repair status?")
        response = await noizy_claude("Analyze this", role="data_scientist")
    """
    client = NoizyAnthropic(role=role, model=model)
    result = await client.chat(message, **kwargs)
    return result.content


def claude_sync(
    message: str,
    role: str = "noizylab",
    model: str = DEFAULT_MODEL,
    **kwargs
) -> str:
    """
    Quick sync Claude call (uses official SDK)
    
    Example:
        response = claude_sync("What's the repair status?")
    """
    client = NoizyAnthropicSync(role=role, model=model)
    result = client.chat(message, **kwargs)
    return result.content


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("NOIZYLAB Anthropic Client")
        print("")
        print("Usage:")
        print("  python noizy_anthropic.py 'your message'")
        print("  python noizy_anthropic.py -r gabriel 'message'")
        print("  python noizy_anthropic.py -m opus 'complex task'")
        print("  python noizy_anthropic.py --stream 'tell me a story'")
        print("")
        print("Roles: noizylab, gabriel, lifeluv, shirl, pops, engr_keith,")
        print("       data_scientist, code_reviewer, composer")
        print("")
        print("Models:")
        print(f"  opus   = {CLAUDE_OPUS}")
        print(f"  sonnet = {CLAUDE_SONNET} (default)")
        print(f"  haiku  = {CLAUDE_HAIKU}")
        return
    
    args = sys.argv[1:]
    role = "noizylab"
    model = DEFAULT_MODEL
    stream = False
    message_parts = []
    
    i = 0
    while i < len(args):
        if args[i] in ("-r", "--role") and i + 1 < len(args):
            role = args[i + 1]
            i += 2
        elif args[i] in ("-m", "--model") and i + 1 < len(args):
            m = args[i + 1].lower()
            if m == "opus":
                model = CLAUDE_OPUS
            elif m == "haiku":
                model = CLAUDE_HAIKU
            else:
                model = CLAUDE_SONNET
            i += 2
        elif args[i] in ("-s", "--stream"):
            stream = True
            i += 1
        else:
            message_parts.append(args[i])
            i += 1
    
    message = " ".join(message_parts)
    if not message:
        print("Error: No message provided")
        return
    
    client = NoizyAnthropic(role=role, model=model)
    
    if stream:
        async for chunk in client.stream(message):
            print(chunk, end="", flush=True)
        print()
    else:
        result = await client.chat(message)
        print(result.content)
        print(f"\n[{result.model} | {result.input_tokens}→{result.output_tokens} tokens | {role}]")


if __name__ == "__main__":
    asyncio.run(main())

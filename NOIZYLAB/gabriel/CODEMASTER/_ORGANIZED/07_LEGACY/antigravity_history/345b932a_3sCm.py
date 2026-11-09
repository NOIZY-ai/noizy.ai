"""
DREAMCHAMBER v1.0 - GORUNFREE EDITION
Multi-AI Convergence Engine for Creative Flow

The DREAMCHAMBER is where creativity flows like LIFELUV.
All AI engines work in parallel, ideas converge, greatness emerges.
"""

import asyncio
from typing import Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import json

from .generators import AIGenerator, GeneratorConfig
from .agents import AGENT_PROMPTS, get_agent
from .router import SmartRouter
from .knowledge_graph import KnowledgeGraph, get_graph


@dataclass
class Dream:
    """A vision in the DREAMCHAMBER"""
    id: str
    prompt: str
    visions: dict[str, str] = field(default_factory=dict)  # provider -> response
    merged_vision: Optional[str] = None
    entities_found: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "visions": self.visions,
            "merged_vision": self.merged_vision,
            "entities": self.entities_found,
            "created_at": self.created_at
        }


class DreamChamber:
    """
    Multi-AI Convergence Engine
    
    Consult multiple AI providers in parallel, merge insights,
    build knowledge graph connections. Flow like LIFELUV.
    """
    
    def __init__(self, config: Optional[GeneratorConfig] = None):
        self.generator = AIGenerator(config)
        self.router = SmartRouter()
        self.graph = get_graph()
        self.dreams: list[Dream] = []
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    def dream(
        self,
        prompt: str,
        providers: Optional[list[str]] = None,
        system_prompt: Optional[str] = None
    ) -> Dream:
        """
        Consult multiple AI providers with the same prompt.
        Returns a Dream with all visions.
        """
        if providers is None:
            providers = ["Gemini", "Claude", "OpenAI"]
        
        sys = system_prompt or "You are a visionary AI. Be bold, creative, actionable. GORUNFREE."
        dream_id = f"dream_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        dream = Dream(id=dream_id, prompt=prompt)
        
        # Collect visions from each provider
        for provider in providers:
            response = self.generator.generate(prompt, provider, sys)
            dream.visions[provider] = response
            
            # Extract entities for knowledge graph
            entities = self.graph.extract_from_text(response)
            dream.entities_found.extend(entities)
        
        # Also extract from prompt
        prompt_entities = self.graph.extract_from_text(prompt)
        dream.entities_found.extend(prompt_entities)
        dream.entities_found = list(set(dream.entities_found))
        
        self.dreams.append(dream)
        return dream
    
    def merge_visions(self, dream: Dream, merger_provider: str = "Claude") -> str:
        """
        Merge multiple AI visions into a unified response.
        Uses one AI to synthesize all perspectives.
        """
        if not dream.visions:
            return "No visions to merge"
        
        # Build merge prompt
        visions_text = "\n\n".join([
            f"### {provider} Vision:\n{vision}"
            for provider, vision in dream.visions.items()
        ])
        
        merge_prompt = f"""You are synthesizing multiple AI perspectives into one actionable plan.

Original Request: {dream.prompt}

{visions_text}

Create a unified response that:
1. Captures the best ideas from each perspective
2. Resolves any conflicts
3. Is concrete and actionable
4. Maintains GORUNFREE philosophy (zero latency, forward motion)

Synthesized Response:"""
        
        merged = self.generator.generate(
            merge_prompt,
            merger_provider,
            "You are a master synthesizer. Combine perspectives brilliantly."
        )
        
        dream.merged_vision = merged
        return merged
    
    def flow(self, prompt: str) -> dict:
        """
        Full LIFELUV flow: route, dream, merge, learn.
        The complete creative cycle.
        """
        # 1. Route to best agent for context
        agent = self.router.route(prompt)
        agent_prompt = get_agent(agent)
        
        # 2. Dream with multiple AIs
        dream = self.dream(prompt, system_prompt=agent_prompt)
        
        # 3. Merge visions
        merged = self.merge_visions(dream)
        
        # 4. Build knowledge
        self.graph.extract_from_text(merged)
        
        return {
            "agent": agent,
            "dream": dream.to_dict(),
            "merged": merged,
            "graph_stats": self.graph.stats()
        }
    
    def quick(self, prompt: str, provider: str = "Claude") -> str:
        """Quick single-provider response with routing"""
        agent = self.router.route(prompt)
        system = get_agent(agent)
        response = self.generator.generate(prompt, provider, system)
        self.graph.extract_from_text(f"{prompt} {response}")
        return response
    
    def get_history(self, limit: int = 10) -> list[dict]:
        """Get recent dreams"""
        return [d.to_dict() for d in self.dreams[-limit:]]
    
    def export_knowledge(self) -> dict:
        """Export knowledge graph"""
        return self.graph.to_json()


# Factory function
def create_chamber(
    gemini_key: Optional[str] = None,
    claude_key: Optional[str] = None,
    openai_key: Optional[str] = None,
    nvidia_key: Optional[str] = None,
    deepseek_key: Optional[str] = None
) -> DreamChamber:
    """Create a configured DreamChamber"""
    config = GeneratorConfig(
        gemini_key=gemini_key,
        claude_key=claude_key,
        openai_key=openai_key,
        nvidia_key=nvidia_key,
        deepseek_key=deepseek_key
    )
    return DreamChamber(config)

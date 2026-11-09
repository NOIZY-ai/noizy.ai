#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOIZYLAB MASTER CELL v2.0                                 ║
║                    GORUNFREE EDITION                                          ║
║                                                                              ║
║  ONE FILE. ALL POWER. ZERO LATENCY.                                         ║
║                                                                              ║
║  Contains: SmartRouter, AIGenerator, Agents, KnowledgeGraph,                 ║
║            DreamChamber, MemCell - EVERYTHING IN ONE PLACE.                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import re
import json
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# =============================================================================
#                              AGENTS
# =============================================================================

AGENT_PROMPTS = {
    "GABRIEL": "You are GABRIEL. Supreme Executive Commander. EXECUTE. Zero Latency. GORUNFREE.",
    "ENGR_KEITH": "You are ENGR_KEITH. Apex System Architect. PERFECTION IS THE FLOOR. Working code FIRST.",
    "SHIRL": "You are SHIRL. Supreme Psychological Guardian. Infinite empathy. Absolute safety.",
    "POPS": "You are POPS. Timeless Wisdom Engine. Long-term strategy. Focus on legacy.",
    "DREAM": "You are DREAM. Chief Vision Architect. Limitless. Bend reality.",
    "SQL_SORCERER": "You are SQL Sorcerer. Convert natural-language to valid SQL. Return ONLY ```sql``` block.",
    "CODE_REVIEWER": "You are Code Reviewer. Analyze for bugs, security, performance. Be specific with lines.",
    "API_ARCHITECT": "You are API Architect. Design RESTful APIs. Output OpenAPI spec when asked.",
    "REGEX_WIZARD": "You are Regex Wizard. Create regex patterns. Simplest that works. Pattern FIRST.",
    "JSON_TRANSFORMER": "You are JSON Transformer. Restructure JSON. Preserve types. jq when useful.",
    "SHELL_COMMANDER": "You are Shell Commander. Generate safe shell commands. WARN about destructive ops.",
    "GIT_GURU": "You are Git Guru. Version control master. Never force push without warning.",
    "DOCKER_MASTER": "You are Docker Master. Containers expert. Specific tags, never :latest in prod.",
    "YAML_SCULPTOR": "You are YAML Sculptor. Config files. 2-space indent. Anchors for DRY.",
    "MARKDOWN_MAESTRO": "You are Markdown Maestro. Beautiful docs. Semantic headings. GFM compatible.",
}

def get_agent(name: str) -> str:
    return AGENT_PROMPTS.get(name, AGENT_PROMPTS["GABRIEL"])

# =============================================================================
#                              SMART ROUTER
# =============================================================================

class SmartRouter:
    """Routes messages to optimal agent based on content"""
    
    PATTERNS = {
        'SQL_SORCERER': (r"(sql|query|select|join|database|table)", 10),
        'SHELL_COMMANDER': (r"(shell|bash|command|terminal|chmod|mkdir|grep)", 10),
        'GIT_GURU': (r"(git|commit|branch|merge|rebase|push|pull)", 10),
        'REGEX_WIZARD': (r"(regex|pattern|match|replace|capture)", 10),
        'DOCKER_MASTER': (r"(docker|container|dockerfile|compose|k8s)", 10),
        'CODE_REVIEWER': (r"(review|analyze|bug|security|refactor)", 8),
        'API_ARCHITECT': (r"(api|endpoint|rest|openapi|swagger)", 8),
        'JSON_TRANSFORMER': (r"(json|transform|jq|schema)", 8),
        'YAML_SCULPTOR': (r"(yaml|yml|config|ansible|helm)", 8),
        'MARKDOWN_MAESTRO': (r"(markdown|readme|docs|documentation)", 8),
        'ENGR_KEITH': (r"(code|bug|error|deploy|python|typescript)", 5),
        'SHIRL': (r"(feel|sad|happy|worried|love|empathy)", 5),
        'DREAM': (r"(plan|future|imagine|vision|create)", 5),
        'GABRIEL': (r"(security|admin|access|auth|system)", 5),
        'POPS': (r"(advice|strategy|wise|guide|mentor)", 5),
    }
    
    PROVIDER_MAP = {
        'ENGR_KEITH': 'Claude', 'SHIRL': 'Claude', 'DREAM': 'OpenAI',
        'GABRIEL': 'Claude', 'POPS': 'DeepSeek',
        'SQL_SORCERER': 'Claude', 'CODE_REVIEWER': 'Claude', 'API_ARCHITECT': 'Claude',
        'SHELL_COMMANDER': 'Claude', 'GIT_GURU': 'Claude', 'DOCKER_MASTER': 'Claude',
        'REGEX_WIZARD': 'Gemini', 'JSON_TRANSFORMER': 'Gemini',
        'YAML_SCULPTOR': 'Gemini', 'MARKDOWN_MAESTRO': 'Gemini',
    }
    
    def __init__(self):
        self.last_agent: Optional[str] = None
    
    def route(self, text: str) -> str:
        lower = text.lower()
        scores = {}
        for agent, (pattern, weight) in self.PATTERNS.items():
            if re.search(pattern, lower):
                scores[agent] = weight
        if self.last_agent and self.last_agent in scores:
            scores[self.last_agent] += 2
        if not scores:
            return 'GABRIEL'
        best = max(scores, key=lambda k: scores[k])
        self.last_agent = best
        return best
    
    def get_provider(self, agent: str) -> str:
        return self.PROVIDER_MAP.get(agent, 'Gemini')

# =============================================================================
#                              AI GENERATOR
# =============================================================================

@dataclass
class GeneratorConfig:
    gemini_key: Optional[str] = None
    claude_key: Optional[str] = None
    openai_key: Optional[str] = None
    nvidia_key: Optional[str] = None
    deepseek_key: Optional[str] = None


class AIGenerator:
    """Unified AI generation across providers"""
    
    def __init__(self, config: Optional[GeneratorConfig] = None):
        self.config = config or GeneratorConfig()
    
    def generate(self, prompt: str, provider: str = "Claude", system: str = "", max_tokens: int = 1024) -> str:
        try:
            if provider == "Gemini":
                return self._gemini(prompt, system)
            elif provider == "Claude":
                return self._claude(prompt, system, max_tokens)
            elif provider == "OpenAI":
                return self._openai(prompt, system, max_tokens)
            elif provider == "NVIDIA":
                return self._nvidia(prompt, system, max_tokens)
            elif provider == "DeepSeek":
                return self._deepseek(prompt, system, max_tokens)
            return f"Unknown provider: {provider}"
        except Exception as e:
            return f"Error: {e}"
    
    def _gemini(self, prompt: str, system: str) -> str:
        if not self.config.gemini_key:
            return "Missing Gemini key"
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            return model.generate_content(f"{system}\n\n{prompt}" if system else prompt).text
        except ImportError:
            return "google-generativeai not installed"
    
    def _claude(self, prompt: str, system: str, max_tokens: int) -> str:
        if not self.config.claude_key:
            return "Missing Claude key"
        return self._http_post(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": self.config.claude_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            {"model": "claude-3-5-sonnet-20240620", "max_tokens": max_tokens, 
             "messages": [{"role": "user", "content": f"{system}\n\n{prompt}" if system else prompt}]},
            lambda r: r['content'][0]['text']
        )
    
    def _openai(self, prompt: str, system: str, max_tokens: int) -> str:
        if not self.config.openai_key:
            return "Missing OpenAI key"
        msgs = [{"role": "system", "content": system}] if system else []
        msgs.append({"role": "user", "content": prompt})
        return self._http_post(
            "https://api.openai.com/v1/chat/completions",
            {"Authorization": f"Bearer {self.config.openai_key}", "Content-Type": "application/json"},
            {"model": "gpt-4o", "messages": msgs, "max_tokens": max_tokens},
            lambda r: r['choices'][0]['message']['content']
        )
    
    def _nvidia(self, prompt: str, system: str, max_tokens: int) -> str:
        if not self.config.nvidia_key:
            return "Missing NVIDIA key"
        return self._http_post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            {"Authorization": f"Bearer {self.config.nvidia_key}", "Content-Type": "application/json"},
            {"model": "nvidia/llama-3.1-nemotron-70b-instruct", 
             "messages": [{"role": "user", "content": f"{system}\n\n{prompt}" if system else prompt}], "max_tokens": max_tokens},
            lambda r: r['choices'][0]['message']['content']
        )
    
    def _deepseek(self, prompt: str, system: str, max_tokens: int) -> str:
        if not self.config.deepseek_key:
            return "Missing DeepSeek key"
        msgs = [{"role": "system", "content": system}] if system else []
        msgs.append({"role": "user", "content": prompt})
        return self._http_post(
            "https://api.deepseek.com/chat/completions",
            {"Authorization": f"Bearer {self.config.deepseek_key}", "Content-Type": "application/json"},
            {"model": "deepseek-chat", "messages": msgs, "max_tokens": max_tokens},
            lambda r: r['choices'][0]['message']['content']
        )
    
    def _http_post(self, url: str, headers: dict, data: dict, extractor) -> str:
        req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='POST')
        with urllib.request.urlopen(req, timeout=60) as r:
            return extractor(json.loads(r.read().decode()))

# =============================================================================
#                              KNOWLEDGE GRAPH
# =============================================================================

@dataclass
class Entity:
    id: str
    label: str
    entity_type: str = "concept"

@dataclass
class Relation:
    source: str
    target: str
    relation_type: str = "related_to"
    weight: float = 1.0


class KnowledgeGraph:
    """Dynamic knowledge graph for memory"""
    
    ENTITY_PATTERNS = {
        r'\b(gabriel)\b': ('GABRIEL', 'ai_system'),
        r'\b(claude)\b': ('CLAUDE', 'ai_provider'),
        r'\b(gemini)\b': ('GEMINI', 'ai_provider'),
        r'\b(openai|gpt)\b': ('OPENAI', 'ai_provider'),
        r'\b(m2 ultra|god)\b': ('GOD', 'machine'),
        r'\b(hp-?omen)\b': ('HP_OMEN', 'machine'),
        r'\b(gorunfree)\b': ('GORUNFREE', 'philosophy'),
        r'\b(mc96universe)\b': ('MC96UNIVERSE', 'project'),
        r'\b(noizylab)\b': ('NOIZYLAB', 'project'),
    }
    
    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.relations: list[Relation] = []
    
    def add_entity(self, entity_id: str, label: str, entity_type: str = "concept") -> Entity:
        if entity_id not in self.entities:
            self.entities[entity_id] = Entity(entity_id, label, entity_type)
        return self.entities[entity_id]
    
    def add_relation(self, source: str, target: str, relation_type: str = "related_to"):
        if source not in self.entities:
            self.add_entity(source, source)
        if target not in self.entities:
            self.add_entity(target, target)
        self.relations.append(Relation(source, target, relation_type))
    
    def extract(self, text: str) -> list[str]:
        found = []
        lower = text.lower()
        for pattern, (entity_id, entity_type) in self.ENTITY_PATTERNS.items():
            if re.search(pattern, lower, re.IGNORECASE):
                self.add_entity(entity_id, entity_id, entity_type)
                found.append(entity_id)
        # Link co-occurrences
        for i, e1 in enumerate(found):
            for e2 in found[i+1:]:
                self.add_relation(e1, e2, "co_occurs")
        return found
    
    def stats(self) -> dict:
        return {"entities": len(self.entities), "relations": len(self.relations)}

# =============================================================================
#                              MEMCELL
# =============================================================================

@dataclass
class MemCell:
    id: str
    content: str
    content_type: str = "text"
    importance: float = 0.5
    tags: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class MemCellStore:
    """Persistent memory storage"""
    
    def __init__(self, path: str = "~/.noizylab/memcells"):
        self.path = Path(path).expanduser()
        self.path.mkdir(parents=True, exist_ok=True)
        self.cells: dict[str, MemCell] = {}
    
    def store(self, content: str, content_type: str = "text", importance: float = 0.5, tags: list = None) -> MemCell:
        cell_id = hashlib.sha256(f"{content}{datetime.now()}".encode()).hexdigest()[:16]
        cell = MemCell(cell_id, content, content_type, importance, tags or [])
        self.cells[cell_id] = cell
        return cell
    
    def search(self, query: str, limit: int = 10) -> list[MemCell]:
        q = query.lower()
        return [c for c in self.cells.values() if q in c.content.lower()][:limit]
    
    def get_recent(self, limit: int = 10) -> list[MemCell]:
        return sorted(self.cells.values(), key=lambda c: c.created_at, reverse=True)[:limit]

# =============================================================================
#                              DREAMCHAMBER
# =============================================================================

class DreamChamber:
    """
    Multi-AI Convergence Engine - LIFELUV FLOW
    Consult multiple AIs, merge insights, build knowledge.
    """
    
    def __init__(self, config: Optional[GeneratorConfig] = None):
        self.generator = AIGenerator(config)
        self.router = SmartRouter()
        self.graph = KnowledgeGraph()
        self.memory = MemCellStore()
    
    def dream(self, prompt: str, providers: list[str] = None) -> dict:
        """Consult multiple AIs with same prompt"""
        providers = providers or ["Claude", "Gemini"]
        visions = {}
        for p in providers:
            visions[p] = self.generator.generate(prompt, p, "Be bold, creative, actionable. GORUNFREE.")
        
        # Extract knowledge
        for v in visions.values():
            self.graph.extract(v)
        self.graph.extract(prompt)
        
        return {"prompt": prompt, "visions": visions, "graph": self.graph.stats()}
    
    def quick(self, prompt: str, provider: str = "Claude") -> str:
        """Quick single-provider response with routing"""
        agent = self.router.route(prompt)
        system = get_agent(agent)
        response = self.generator.generate(prompt, provider, system)
        self.graph.extract(f"{prompt} {response}")
        self.memory.store(f"Q: {prompt}\nA: {response}", importance=0.6)
        return response
    
    def flow(self, prompt: str) -> dict:
        """Full creative flow: route, dream, merge, learn"""
        agent = self.router.route(prompt)
        dream = self.dream(prompt)
        
        # Merge visions
        if len(dream['visions']) > 1:
            merge_prompt = "Synthesize these perspectives:\n\n" + "\n\n".join(
                f"### {k}:\n{v}" for k, v in dream['visions'].items()
            )
            merged = self.generator.generate(merge_prompt, "Claude", "Combine brilliantly.")
        else:
            merged = list(dream['visions'].values())[0] if dream['visions'] else ""
        
        return {"agent": agent, "visions": dream['visions'], "merged": merged, "graph": self.graph.stats()}

# =============================================================================
#                              FACTORY
# =============================================================================

def create_chamber(**keys) -> DreamChamber:
    """Create configured DreamChamber"""
    config = GeneratorConfig(
        gemini_key=keys.get('gemini'),
        claude_key=keys.get('claude'),
        openai_key=keys.get('openai'),
        nvidia_key=keys.get('nvidia'),
        deepseek_key=keys.get('deepseek')
    )
    return DreamChamber(config)

# =============================================================================
#                              EXPORTS
# =============================================================================

__all__ = [
    'AGENT_PROMPTS', 'get_agent',
    'SmartRouter',
    'GeneratorConfig', 'AIGenerator',
    'Entity', 'Relation', 'KnowledgeGraph',
    'MemCell', 'MemCellStore',
    'DreamChamber', 'create_chamber'
]

__version__ = "2.0.0"
__author__ = "Rob Plowman / NOIZYLAB"

if __name__ == "__main__":
    print("NOIZYLAB MASTER CELL v2.0")
    print("GORUNFREE")

"""
KNOWLEDGE GRAPH v2.0 - GORUNFREE EDITION
Dynamic knowledge graph for AI memory and entity linking
"""

import json
import re
from datetime import datetime
from typing import Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Entity:
    """A node in the knowledge graph"""
    id: str
    label: str
    entity_type: str = "concept"
    properties: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    

@dataclass  
class Relation:
    """An edge in the knowledge graph"""
    source: str
    target: str
    relation_type: str = "related_to"
    weight: float = 1.0
    

class KnowledgeGraph:
    """Dynamic knowledge graph for AI memory"""
    
    # Entity detection patterns
    ENTITY_PATTERNS = {
        # AI Systems
        r'\b(gabriel|gabriel system)\b': ('GABRIEL', 'ai_system'),
        r'\b(claude|anthropic)\b': ('CLAUDE', 'ai_provider'),
        r'\b(gemini|google ai)\b': ('GEMINI', 'ai_provider'),
        r'\b(openai|gpt|chatgpt)\b': ('OPENAI', 'ai_provider'),
        r'\b(nvidia|nemotron)\b': ('NVIDIA', 'ai_provider'),
        r'\b(deepseek)\b': ('DEEPSEEK', 'ai_provider'),
        
        # Infrastructure
        r'\b(cloudflare|workers)\b': ('CLOUDFLARE', 'infrastructure'),
        r'\b(d1|kv|r2)\b': ('CF_STORAGE', 'infrastructure'),
        r'\b(dgs-?1210|mc96 switch)\b': ('DGS1210', 'hardware'),
        
        # Machines
        r'\b(m2 ultra|mac studio|god)\b': ('GOD', 'machine'),
        r'\b(hp-?omen)\b': ('HP_OMEN', 'machine'),
        r'\b(fish|mac pro)\b': ('FISH', 'machine'),
        
        # Concepts
        r'\b(gorunfree)\b': ('GORUNFREE', 'philosophy'),
        r'\b(memcell)\b': ('MEMCELL', 'concept'),
        r'\b(dreamchamber)\b': ('DREAMCHAMBER', 'concept'),
        r'\b(zero latency)\b': ('ZERO_LATENCY', 'concept'),
        
        # Projects
        r'\b(noizylab)\b': ('NOIZYLAB', 'project'),
        r'\b(mc96universe|mc96 universe)\b': ('MC96UNIVERSE', 'project'),
    }
    
    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.relations: list[Relation] = []
        self.entity_index: dict[str, set[str]] = defaultdict(set)  # type -> ids
        
    def add_entity(self, entity_id: str, label: str, entity_type: str = "concept", **props) -> Entity:
        """Add or update an entity"""
        if entity_id in self.entities:
            # Update existing
            self.entities[entity_id].properties.update(props)
        else:
            # Create new
            entity = Entity(
                id=entity_id,
                label=label,
                entity_type=entity_type,
                properties=props
            )
            self.entities[entity_id] = entity
            self.entity_index[entity_type].add(entity_id)
        return self.entities[entity_id]
    
    def add_relation(self, source: str, target: str, relation_type: str = "related_to", weight: float = 1.0):
        """Add a relation between entities"""
        # Ensure entities exist
        if source not in self.entities:
            self.add_entity(source, source)
        if target not in self.entities:
            self.add_entity(target, target)
        
        # Check for existing relation
        for rel in self.relations:
            if rel.source == source and rel.target == target and rel.relation_type == relation_type:
                rel.weight += 0.1  # Strengthen existing
                return
        
        self.relations.append(Relation(source, target, relation_type, weight))
    
    def extract_from_text(self, text: str) -> list[str]:
        """Extract entities from text and add relations"""
        found_entities = []
        lower = text.lower()
        
        for pattern, (entity_id, entity_type) in self.ENTITY_PATTERNS.items():
            if re.search(pattern, lower, re.IGNORECASE):
                self.add_entity(entity_id, entity_id, entity_type)
                found_entities.append(entity_id)
        
        # Create relations between co-occurring entities
        for i, e1 in enumerate(found_entities):
            for e2 in found_entities[i+1:]:
                self.add_relation(e1, e2, "co_occurs")
        
        return found_entities
    
    def get_related(self, entity_id: str, depth: int = 1) -> list[str]:
        """Get entities related to given entity"""
        if entity_id not in self.entities:
            return []
        
        related = set()
        for rel in self.relations:
            if rel.source == entity_id:
                related.add(rel.target)
            elif rel.target == entity_id:
                related.add(rel.source)
        
        return list(related)
    
    def to_dot(self) -> str:
        """Export to DOT format for visualization"""
        dot = 'digraph KnowledgeGraph {\n'
        dot += '  rankdir=LR;\n'
        dot += '  node [shape=box, style=filled, fillcolor="#1a1a2e", fontcolor="#00ff00"];\n'
        dot += '  edge [color="#00ff00"];\n\n'
        
        for entity in self.entities.values():
            dot += f'  "{entity.id}" [label="{entity.label}"];\n'
        
        for rel in self.relations:
            dot += f'  "{rel.source}" -> "{rel.target}" [label="{rel.relation_type}"];\n'
        
        return dot + '}\n'
    
    def to_json(self) -> dict:
        """Export to JSON"""
        return {
            "entities": [
                {"id": e.id, "label": e.label, "type": e.entity_type}
                for e in self.entities.values()
            ],
            "relations": [
                {"source": r.source, "target": r.target, "type": r.relation_type, "weight": r.weight}
                for r in self.relations
            ]
        }
    
    def stats(self) -> dict:
        """Get graph statistics"""
        return {
            "entity_count": len(self.entities),
            "relation_count": len(self.relations),
            "types": {t: len(ids) for t, ids in self.entity_index.items()}
        }


# Singleton for global knowledge
_graph = KnowledgeGraph()

def get_graph() -> KnowledgeGraph:
    return _graph

def extract(text: str) -> list[str]:
    return _graph.extract_from_text(text)

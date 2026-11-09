#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PROMPT LIBRARY v1.0                                       ║
║                    GORUNFREE PROMPT MODULES                                  ║
║                                                                              ║
║  Load and manage prompt modules from AI_COMPLETE_BRAIN.                     ║
║  Dynamic prompt loading. Template interpolation. Zero latency.              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import re
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PromptModule:
    """A loaded prompt module"""
    name: str
    content: str
    path: Path
    tags: list[str] = field(default_factory=list)
    router_tags: list[str] = field(default_factory=list)
    category: str = "general"
    loaded_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def render(self, **kwargs) -> str:
        """Render prompt with template variables"""
        result = self.content
        for key, value in kwargs.items():
            result = result.replace(f"{{{key}}}", str(value))
            result = result.replace(f"${{{key}}}", str(value))
            result = result.replace(f"<<{key}>>", str(value))
        return result


class PromptLibrary:
    """
    Prompt Module Library
    
    Loads and manages prompt modules from the PROMPT_MODULES directory.
    Supports template interpolation and dynamic loading.
    """
    
    DEFAULT_PATH = Path.home() / "AI_COMPLETE_BRAIN" / "PROMPT_MODULES"
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = Path(base_path) if base_path else self.DEFAULT_PATH
        self.modules: dict[str, PromptModule] = {}
        self._load_all()
    
    def _parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """Parse YAML-like frontmatter from markdown"""
        metadata = {}
        body = content
        
        # Check for frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                body = parts[2].strip()
                
                # Simple YAML parsing
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
        
        return metadata, body
    
    def _extract_tags(self, content: str) -> list[str]:
        """Extract router tags from content"""
        tags = []
        
        # Look for ## ROUTER TAGS section
        match = re.search(r'## ROUTER TAGS\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if match:
            section = match.group(1)
            # Extract /tag patterns
            tags = re.findall(r'`(/\w+)`', section)
        
        return tags
    
    def _load_module(self, path: Path) -> Optional[PromptModule]:
        """Load a single prompt module"""
        try:
            content = path.read_text()
            metadata, body = self._parse_frontmatter(content)
            
            name = path.stem
            tags = self._extract_tags(content)
            category = metadata.get('category', 'general')
            
            return PromptModule(
                name=name,
                content=body,
                path=path,
                tags=tags,
                router_tags=tags,
                category=category
            )
        except Exception as e:
            print(f"⚠️ Failed to load {path}: {e}")
            return None
    
    def _load_all(self):
        """Load all prompt modules"""
        if not self.base_path.exists():
            print(f"⚠️ Prompt library path not found: {self.base_path}")
            return
        
        for path in self.base_path.glob('*.md'):
            module = self._load_module(path)
            if module:
                self.modules[module.name] = module
                # Also index by router tags
                for tag in module.router_tags:
                    self.modules[tag] = module
        
        print(f"📚 Loaded {len(set(m.name for m in self.modules.values()))} prompt modules")
    
    def get(self, name: str) -> Optional[PromptModule]:
        """Get a prompt module by name or tag"""
        # Try direct lookup
        if name in self.modules:
            return self.modules[name]
        
        # Try with / prefix
        if f"/{name}" in self.modules:
            return self.modules[f"/{name}"]
        
        # Try uppercase
        if name.upper() in self.modules:
            return self.modules[name.upper()]
        
        return None
    
    def render(self, name: str, **kwargs) -> str:
        """Get and render a prompt"""
        module = self.get(name)
        if module:
            return module.render(**kwargs)
        return f"⚠️ Prompt module '{name}' not found"
    
    def list_modules(self) -> list[str]:
        """List all module names"""
        return list(set(m.name for m in self.modules.values()))
    
    def list_by_category(self, category: str) -> list[PromptModule]:
        """List modules by category"""
        return [m for m in set(self.modules.values()) if m.category == category]
    
    def search(self, query: str) -> list[PromptModule]:
        """Search modules by content"""
        query_lower = query.lower()
        results = []
        
        for module in set(self.modules.values()):
            if query_lower in module.name.lower() or query_lower in module.content.lower():
                results.append(module)
        
        return results
    
    def reload(self):
        """Reload all modules"""
        self.modules.clear()
        self._load_all()


# Global instance
_library: Optional[PromptLibrary] = None


def get_library() -> PromptLibrary:
    """Get or create the global prompt library"""
    global _library
    if _library is None:
        _library = PromptLibrary()
    return _library


def get_prompt(name: str, **kwargs) -> str:
    """Quick access to get and render a prompt"""
    return get_library().render(name, **kwargs)


def list_prompts() -> list[str]:
    """List all available prompts"""
    return get_library().list_modules()


__all__ = [
    'PromptModule', 'PromptLibrary', 'get_library', 'get_prompt', 'list_prompts'
]


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              PROMPT LIBRARY v1.0                             ║")
    print("║              GORUNFREE PROMPT MODULES                        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    lib = get_library()
    
    print(f"📚 {len(lib.list_modules())} modules loaded:")
    for name in sorted(lib.list_modules()):
        module = lib.get(name)
        tags = ', '.join(module.router_tags) if module.router_tags else 'no tags'
        print(f"   • {name} [{tags}]")

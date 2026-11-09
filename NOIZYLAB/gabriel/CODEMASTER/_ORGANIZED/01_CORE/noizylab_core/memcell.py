"""
MEMCELL v2.0 - GORUNFREE EDITION
Timestamped memory storage with relevance scoring
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class MemCell:
    """Atomic unit of long-term memory"""
    id: str
    content: str
    content_type: str = "text"  # text, code, config, prompt
    source: str = "user"  # user, ai, scan, import
    importance: float = 0.5  # 0.0 - 1.0
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MemCell':
        return cls(**data)


class MemCellStore:
    """Persistent memory storage with indexing"""
    
    def __init__(self, storage_path: str = "~/.noizylab/memcells"):
        self.storage_path = Path(storage_path).expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_path / "index.json"
        self.cells: dict[str, MemCell] = {}
        self._load_index()
    
    def _load_index(self):
        """Load index from disk"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                    for cell_data in data.get('cells', []):
                        cell = MemCell.from_dict(cell_data)
                        self.cells[cell.id] = cell
            except Exception as e:
                print(f"Error loading memcell index: {e}")
    
    def _save_index(self):
        """Save index to disk"""
        data = {
            'version': '2.0',
            'updated': datetime.now().isoformat(),
            'count': len(self.cells),
            'cells': [cell.to_dict() for cell in self.cells.values()]
        }
        with open(self.index_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID from content hash"""
        hash_input = f"{content}{datetime.now().isoformat()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def store(
        self,
        content: str,
        content_type: str = "text",
        source: str = "user",
        importance: float = 0.5,
        tags: Optional[list[str]] = None,
        **metadata
    ) -> MemCell:
        """Store a new memory cell"""
        cell = MemCell(
            id=self._generate_id(content),
            content=content,
            content_type=content_type,
            source=source,
            importance=importance,
            tags=tags or [],
            metadata=metadata
        )
        self.cells[cell.id] = cell
        self._save_index()
        return cell
    
    def get(self, cell_id: str) -> Optional[MemCell]:
        """Retrieve a memory cell by ID"""
        return self.cells.get(cell_id)
    
    def search(
        self,
        query: str = "",
        content_type: Optional[str] = None,
        tags: Optional[list[str]] = None,
        min_importance: float = 0.0,
        limit: int = 20
    ) -> list[MemCell]:
        """Search memory cells"""
        results = []
        query_lower = query.lower()
        
        for cell in self.cells.values():
            # Filter by content type
            if content_type and cell.content_type != content_type:
                continue
            
            # Filter by importance
            if cell.importance < min_importance:
                continue
            
            # Filter by tags
            if tags and not any(t in cell.tags for t in tags):
                continue
            
            # Filter by query
            if query and query_lower not in cell.content.lower():
                continue
            
            results.append(cell)
        
        # Sort by importance, then by date
        results.sort(key=lambda c: (-c.importance, c.created_at), reverse=False)
        return results[:limit]
    
    def update(self, cell_id: str, **updates) -> Optional[MemCell]:
        """Update a memory cell"""
        cell = self.cells.get(cell_id)
        if not cell:
            return None
        
        for key, value in updates.items():
            if hasattr(cell, key):
                setattr(cell, key, value)
        
        cell.updated_at = datetime.now().isoformat()
        self._save_index()
        return cell
    
    def delete(self, cell_id: str) -> bool:
        """Delete a memory cell"""
        if cell_id in self.cells:
            del self.cells[cell_id]
            self._save_index()
            return True
        return False
    
    def get_recent(self, limit: int = 10) -> list[MemCell]:
        """Get most recent memories"""
        sorted_cells = sorted(
            self.cells.values(),
            key=lambda c: c.created_at,
            reverse=True
        )
        return sorted_cells[:limit]
    
    def get_important(self, limit: int = 10) -> list[MemCell]:
        """Get most important memories"""
        sorted_cells = sorted(
            self.cells.values(),
            key=lambda c: c.importance,
            reverse=True
        )
        return sorted_cells[:limit]
    
    def stats(self) -> dict:
        """Get storage statistics"""
        types = {}
        tags = {}
        
        for cell in self.cells.values():
            types[cell.content_type] = types.get(cell.content_type, 0) + 1
            for tag in cell.tags:
                tags[tag] = tags.get(tag, 0) + 1
        
        return {
            'total': len(self.cells),
            'types': types,
            'top_tags': dict(sorted(tags.items(), key=lambda x: -x[1])[:10]),
            'avg_importance': sum(c.importance for c in self.cells.values()) / len(self.cells) if self.cells else 0
        }


# Global store instance
_store: Optional[MemCellStore] = None

def get_store() -> MemCellStore:
    global _store
    if _store is None:
        _store = MemCellStore()
    return _store

def store(content: str, **kwargs) -> MemCell:
    return get_store().store(content, **kwargs)

def search(query: str, **kwargs) -> list[MemCell]:
    return get_store().search(query, **kwargs)

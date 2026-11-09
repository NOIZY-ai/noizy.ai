import hashlib
import json
import time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict

@dataclass
class Evidence:
    source_id: str
    locator: str
    quote: str = "" # Max 25 words

@dataclass
class MemCell:
    id: str
    type: str
    claim: str
    evidence: List[Evidence]
    confidence: float # 0.0 to 1.0
    links: Dict[str, List[str]] = field(default_factory=lambda: {"supports": [], "contradicts": [], "related": []})
    timestamp: float = field(default_factory=time.time)
    integrity: str = ""

    def compute_integrity(self):
        """Generates SHA256 hash of the immutable core fields."""
        payload = f"{self.id}:{self.type}:{self.claim}:{self.confidence}"
        self.integrity = hashlib.sha256(payload.encode()).hexdigest()
        return self.integrity

class OverlapEngine:
    def __init__(self):
        self.memory_store: Dict[str, MemCell] = {}

    def ingest(self, cell: MemCell):
        """TRUTH GATE: Ingests a new MemCell. Enforces evidence requirement."""
        if not cell.evidence:
            cell.type = "UNVERIFIED"
            print(f"TRUTH GATE WARNING: MemCell {cell.id} lacks evidence. Marked UNVERIFIED.")
        
        cell.compute_integrity()
        
        # Merge Logic (Simplified)
        if cell.id in self.memory_store:
            existing = self.memory_store[cell.id]
            if existing.claim == cell.claim:
                # Merge Evidence
                existing.evidence.extend(cell.evidence)
            else:
                # Conflict
                self._create_conflict(existing, cell)
        else:
            self.memory_store[cell.id] = cell
            
    def _create_conflict(self, existing: MemCell, new_cell: MemCell):
        """Creates a CONFLICT cell linking the two contradictions."""
        conflict_id = f"CONFLICT_{existing.id}_{new_cell.id}"
        print(f"CONFLICT DETECTED: {conflict_id}")
        # Implementation would create a new separate conflict tracking cell here
        
    def get_verified_memory(self) -> List[MemCell]:
        return [c for c in self.memory_store.values() if c.type != "UNVERIFIED"]

# Example Usage
if __name__ == "__main__":
    eng = OverlapEngine()
    ev = Evidence(source_id="manual_entry", locator="prompt", quote="GABRIEL OS DIRECTIVE")
    cell = MemCell(id="mission_01", type="DIRECTIVE", claim="Maximize effectiveness", evidence=[ev], confidence=1.0)
    eng.ingest(cell)
    print(json.dumps([asdict(c) for c in eng.get_verified_memory()], indent=2))

#!/usr/bin/env python3
"""
MemCell V4.0 - The Neural Core (Overlap Engine)
Hot/Cold Memory Tiers + Causal Edges + Counterfactual Tracking + Temporal Weighting
"""

import json
import datetime
import time
import sys
from pathlib import Path
from collections import Counter, deque
from typing import Optional
import hashlib

# Configuration
MEMORY_DIR = Path.home() / "NOIZYLAB" / "memory"
MEMORY_FILE = MEMORY_DIR / "memcell_v4.json"
COLD_STORAGE = MEMORY_DIR / "cold_storage.json"


class CausalEdge:
    """Represents a cause-effect relationship."""

    def __init__(self, cause: str, effect: str, confidence: float = 1.0):
        self.cause = cause
        self.effect = effect
        self.confidence = confidence
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "cause": self.cause,
            "effect": self.effect,
            "confidence": self.confidence,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CausalEdge":
        edge = cls(data["cause"], data["effect"], data.get("confidence", 1.0))
        edge.created_at = data.get("created_at", edge.created_at)
        return edge


class MemCell:
    """
    V4 Neural Memory Engine with:
    - Hot/Cold memory tiers (RAM vs disk)
    - Causal edges (cause -> effect relationships)
    - Counterfactual storage (what was rejected + why)
    - Temporal weighting (recent > old)
    """

    HOT_LIMIT = 100  # Max items in hot memory (RAM)
    COLD_LIMIT = 1000  # Max items in cold storage (disk)

    def __init__(self):
        self._ensure_memory()
        self.memory = self._load_memory()
        self.hot_cache = deque(maxlen=self.HOT_LIMIT)
        self.causal_edges: list[CausalEdge] = []
        self.counterfactuals: list[dict] = []
        self._warm_up_cache()
        self.dirty = False

    def _ensure_memory(self):
        """Initialize memory directory and files."""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        if not MEMORY_FILE.exists():
            initial_mem = {
                "system_start": datetime.datetime.now().isoformat(),
                "version": "4.0",
                "neural_state": {
                    "vibe": "neutral",
                    "focus": "idle",
                    "short_term": [],
                    "patterns": [],
                    "causal_edges": [],
                    "counterfactuals": [],
                },
                "personas": {"active": ["shirl", "engr"], "overlap_detected": False},
                "stats": {
                    "total_events": 0,
                    "cache_promotions": 0,
                    "cache_demotions": 0,
                },
            }
            self._save_memory(initial_mem)

    def _load_memory(self) -> dict:
        """Load memory from persistent storage."""
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_memory(self, data: dict = None):
        """Persist memory to disk."""
        with open(MEMORY_FILE, "w") as f:
            json.dump(data or self.memory, f, indent=2)
        self.dirty = False

    def _warm_up_cache(self):
        """Load recent items into hot cache."""
        ns = self.memory.get("neural_state", {})
        short_term = ns.get("short_term", [])
        for item in short_term[-self.HOT_LIMIT :]:
            self.hot_cache.append(item)

        # Load causal edges
        for edge_data in ns.get("causal_edges", []):
            self.causal_edges.append(CausalEdge.from_dict(edge_data))

        # Load counterfactuals
        self.counterfactuals = ns.get("counterfactuals", [])[-50:]

    def _hash_entry(self, entry: dict) -> str:
        """Generate hash for deduplication."""
        content = f"{entry.get('a', '')}:{entry.get('s', '')}:{json.dumps(entry.get('d', {}), sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def detect_overlaps(self, history: list) -> list[str]:
        """Analyze history for recurring subjects (The Overlap)."""
        subjects = [h.get("s", "").lower() for h in history if h.get("s")]
        if not subjects:
            return []

        counts = Counter(subjects)
        # Apply temporal weighting - recent subjects count more
        for i, h in enumerate(reversed(history[-20:])):
            subj = h.get("s", "").lower()
            if subj:
                counts[subj] += 0.1 * (20 - i)  # Decay weight

        overlaps = [subj for subj, count in counts.items() if count >= 2]
        return overlaps

    def track(self, action: str, subject: str, details: dict = None) -> bool:
        """Log action with deep overlap scanning."""
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            "t": timestamp,
            "a": action,
            "s": subject,
            "d": details or {},
            "hash": self._hash_entry({"a": action, "s": subject, "d": details or {}}),
        }

        ns = self.memory["neural_state"]

        # Check for duplicate in hot cache
        entry_hash = entry["hash"]
        for existing in self.hot_cache:
            if existing.get("hash") == entry_hash:
                # Update timestamp but don't duplicate
                existing["t"] = timestamp
                self.dirty = True
                return True

        # Add to hot cache
        self.hot_cache.append(entry)
        ns["short_term"].append(entry)
        ns["focus"] = subject

        # Update stats
        self.memory["stats"]["total_events"] = self.memory["stats"].get("total_events", 0) + 1

        # Heuristic Vibe detection
        action_lower = action.lower()
        if "error" in action_lower or "fail" in action_lower:
            ns["vibe"] = "critical"
        elif "optimize" in action_lower or "success" in action_lower:
            ns["vibe"] = "aligned"
        elif "boot" in action_lower or "start" in action_lower:
            ns["vibe"] = "awakening"

        # Hot/Cold tier management
        if len(ns["short_term"]) > self.HOT_LIMIT:
            self._demote_to_cold(ns["short_term"][:-self.HOT_LIMIT])
            ns["short_term"] = ns["short_term"][-self.HOT_LIMIT:]
            self.memory["stats"]["cache_demotions"] = self.memory["stats"].get("cache_demotions", 0) + 1

        # OVERLAP ENGINE
        overlaps = self.detect_overlaps(ns["short_term"])
        ns["patterns"] = overlaps

        # Detect active overlap
        if subject.lower() in overlaps:
            self.memory["personas"]["overlap_detected"] = True
            ns["vibe"] = "connected"

        self.dirty = True
        self._save_memory()
        return True

    def _demote_to_cold(self, items: list):
        """Move items to cold storage."""
        cold = []
        if COLD_STORAGE.exists():
            try:
                cold = json.loads(COLD_STORAGE.read_text())
            except Exception:
                cold = []

        cold.extend(items)

        # Trim cold storage
        if len(cold) > self.COLD_LIMIT:
            cold = cold[-self.COLD_LIMIT:]

        COLD_STORAGE.write_text(json.dumps(cold, indent=2))

    def add_causal_edge(self, cause: str, effect: str, confidence: float = 1.0):
        """Add a cause-effect relationship."""
        edge = CausalEdge(cause, effect, confidence)
        self.causal_edges.append(edge)

        # Persist
        ns = self.memory["neural_state"]
        ns["causal_edges"] = [e.to_dict() for e in self.causal_edges[-100:]]
        self._save_memory()

    def add_counterfactual(self, decision: str, rejected: str, reason: str):
        """Store what was rejected and why (negative knowledge)."""
        cf = {
            "decision": decision,
            "rejected": rejected,
            "reason": reason,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.counterfactuals.append(cf)

        # Persist
        ns = self.memory["neural_state"]
        ns["counterfactuals"] = self.counterfactuals[-50:]
        self._save_memory()

    def recall(self, include_detail: bool = False) -> str:
        """Generate a status report from memory."""
        ns = self.memory.get("neural_state", {})
        ov = self.memory.get("personas", {}).get("overlap_detected", False)
        patterns = ns.get("patterns", [])
        stats = self.memory.get("stats", {})

        report = f"""[MEMCELL V4 NEURAL CORE]
TIME: {datetime.datetime.now().strftime("%H:%M:%S")}
FOCUS: {ns.get("focus", "idle")}
VIBE: {ns.get("vibe", "neutral")}
OVERLAP: {"ACTIVE" if ov else "Inactive"}
PATTERNS: {", ".join(patterns[:5]) if patterns else "None detected"}
HOT CACHE: {len(self.hot_cache)}/{self.HOT_LIMIT}
TOTAL EVENTS: {stats.get("total_events", 0)}
CAUSAL EDGES: {len(self.causal_edges)}
"""

        if include_detail and self.causal_edges:
            report += "\nRECENT CAUSAL LINKS:\n"
            for edge in self.causal_edges[-3:]:
                report += f"  {edge.cause} -> {edge.effect} (conf: {edge.confidence})\n"

        return report

    def search_patterns(self, query: str) -> list[dict]:
        """Search memory for matching patterns."""
        results = []
        query_lower = query.lower()

        for item in self.hot_cache:
            if query_lower in item.get("s", "").lower() or query_lower in str(item.get("d", {})).lower():
                results.append(item)

        # Also search cold if needed
        if len(results) < 10 and COLD_STORAGE.exists():
            try:
                cold = json.loads(COLD_STORAGE.read_text())
                for item in reversed(cold):
                    if query_lower in item.get("s", "").lower():
                        results.append(item)
                        if len(results) >= 20:
                            break
            except Exception:
                pass

        return results[:20]

    def get_recent(self, n: int = 10) -> list[dict]:
        """Get n most recent events."""
        return list(self.hot_cache)[-n:]

    def get_stats(self) -> dict:
        """Get memory statistics."""
        return {
            "version": "4.0",
            "hot_cache_size": len(self.hot_cache),
            "hot_cache_limit": self.HOT_LIMIT,
            "total_events": self.memory.get("stats", {}).get("total_events", 0),
            "causal_edges": len(self.causal_edges),
            "counterfactuals": len(self.counterfactuals),
            "patterns_detected": len(self.memory.get("neural_state", {}).get("patterns", [])),
            "vibe": self.memory.get("neural_state", {}).get("vibe", "unknown"),
        }


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    mc = MemCell()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "track" and len(sys.argv) >= 4:
            mc.track(sys.argv[2], sys.argv[3])
            print("🧠 Pattern Ingested.")

        elif cmd == "recall":
            print(mc.recall(include_detail=True))

        elif cmd == "search" and len(sys.argv) >= 3:
            results = mc.search_patterns(sys.argv[2])
            print(f"Found {len(results)} matches:")
            for r in results[:5]:
                print(f"  [{r.get('t', 'N/A')[:10]}] {r.get('s')} - {r.get('a')}")

        elif cmd == "stats":
            print(json.dumps(mc.get_stats(), indent=2))

        elif cmd == "recent":
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            for item in mc.get_recent(n):
                print(f"  [{item.get('t', '')[:19]}] {item.get('s')}: {item.get('a')}")

        else:
            print("Usage: memory_engine.py [track|recall|search|stats|recent] [args...]")
    else:
        print(json.dumps(mc.memory, indent=2))

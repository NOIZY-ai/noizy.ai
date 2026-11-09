#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Knowledge Tools
===================================
Deep knowledge index search. Extracted from v1 monolith.
Same brain file, cleaner interface.
"""

import json
from typing import Any

from ..config import BRAIN_FILE


def _load_brain() -> dict:
    try:
        if BRAIN_FILE.exists():
            return json.loads(BRAIN_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        pass
    return {}


class KnowledgeTools:
    """Knowledge index tools."""

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        dispatch = {
            "stats": self._stats,
            "search": self._search,
            "prompts": self._prompts,
            "functions": self._functions,
            "entries": self._entries,
            "imports": self._imports,
            "todos": self._todos,
            "explore": self._explore,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown knowledge action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    async def _stats(self, args: dict) -> dict:
        brain = _load_brain()
        stats = brain.get("stats", {})
        return {
            "version": brain.get("version", "unknown"),
            "total_files": stats.get("total_files", 0),
            "total_lines": stats.get("total_lines", 0),
            "created": brain.get("created", "unknown"),
        }

    async def _search(self, args: dict) -> dict:
        query = args.get("query", "").lower()
        search_type = args.get("type", "all")
        limit = args.get("limit", 20)
        brain = _load_brain()
        results = []

        sections = {
            "prompts": "prompts",
            "functions": "functions",
            "classes": "classes",
            "knowledge": "knowledge_base",
            "files": "files",
        }

        for section_name, brain_key in sections.items():
            if search_type not in ("all", section_name) or len(results) >= limit:
                continue
            for item in brain.get(brain_key, []):
                searchable = json.dumps(item).lower()
                if query in searchable:
                    results.append({"type": section_name, **item})
                    if len(results) >= limit:
                        break

        return {"query": query, "count": len(results), "results": results}

    async def _prompts(self, args: dict) -> dict:
        brain = _load_brain()
        prompts = brain.get("prompts", [])
        query = args.get("query", "").lower()
        limit = args.get("limit", 20)

        if query:
            prompts = [p for p in prompts if query in json.dumps(p).lower()]

        return {"total": len(brain.get("prompts", [])), "results": prompts[:limit]}

    async def _functions(self, args: dict) -> dict:
        brain = _load_brain()
        functions = brain.get("functions", [])
        name = args.get("name", "").lower()
        limit = args.get("limit", 50)

        matches = [f for f in functions if name in f.get("name", "").lower()]
        return {"total_indexed": len(functions), "matches": len(matches), "results": matches[:limit]}

    async def _entries(self, args: dict) -> dict:
        brain = _load_brain()
        kb = brain.get("knowledge_base", [])
        query = args.get("query", "").lower()
        limit = args.get("limit", 20)

        matches = [k for k in kb if query in json.dumps(k).lower()]
        return {"total_indexed": len(kb), "matches": len(matches), "results": matches[:limit]}

    async def _imports(self, args: dict) -> dict:
        brain = _load_brain()
        imports = brain.get("imports", [])
        filter_str = args.get("filter", "").lower()

        if filter_str:
            imports = [i for i in imports if filter_str in i.lower()]

        return {"total": len(brain.get("imports", [])), "filtered": len(imports), "imports": sorted(imports)}

    async def _todos(self, args: dict) -> dict:
        brain = _load_brain()
        limit = args.get("limit", 50)
        todos = brain.get("todos", [])
        return {"total": len(todos), "results": todos[:limit]}

    async def _explore(self, args: dict) -> dict:
        brain = _load_brain()
        category = args.get("category", "")
        limit = args.get("limit", 30)
        by_cat = brain.get("by_category", {})
        files = by_cat.get(category, [])
        return {"category": category, "total": len(files), "results": files[:limit]}

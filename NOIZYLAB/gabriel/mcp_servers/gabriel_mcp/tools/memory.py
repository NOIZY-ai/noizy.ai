#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Memory Tools
================================
Extracted from the v1 monolith. Same functionality, clean interface.
"""

import json
from datetime import datetime
from typing import Any

from ..config import MEMORY_FILE, TASKS_FILE


def _load_json(path, default=None):
    try:
        if path.exists():
            return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        pass
    return default if default is not None else {}


def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str))


class MemoryTools:
    """Memory and task management tools."""

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        dispatch = {
            "store": self._store,
            "recall": self._recall,
            "add_task": self._add_task,
            "complete_task": self._complete_task,
            "list_tasks": self._list_tasks,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown memory action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    async def _store(self, args: dict) -> dict:
        key = args.get("key", "")
        value = args.get("value", "")
        tags = args.get("tags", [])

        memory = _load_json(MEMORY_FILE, {"entries": []})
        entry = {
            "id": f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "key": key,
            "value": value,
            "tags": tags,
            "timestamp": datetime.now().isoformat(),
        }
        memory["entries"].append(entry)
        memory["entries"] = memory["entries"][-1000:]
        _save_json(MEMORY_FILE, memory)

        return {"stored": key, "id": entry["id"]}

    async def _recall(self, args: dict) -> dict:
        query = args.get("query", "").lower()
        limit = args.get("limit", 10)

        memory = _load_json(MEMORY_FILE, {"entries": []})
        matches = []
        for entry in reversed(memory["entries"]):
            if (query in entry.get("key", "").lower()
                    or query in entry.get("value", "").lower()
                    or any(query in t.lower() for t in entry.get("tags", []))):
                matches.append(entry)
                if len(matches) >= limit:
                    break

        return {"query": query, "count": len(matches), "results": matches}

    async def _add_task(self, args: dict) -> dict:
        tasks = _load_json(TASKS_FILE, {"pending": [], "completed": []})
        task = {
            "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": args.get("title", ""),
            "description": args.get("description", ""),
            "priority": args.get("priority", "medium"),
            "created": datetime.now().isoformat(),
        }
        tasks["pending"].append(task)
        _save_json(TASKS_FILE, tasks)
        return {"task_id": task["id"], "status": "pending"}

    async def _complete_task(self, args: dict) -> dict:
        task_id = args.get("task_id", "")
        tasks = _load_json(TASKS_FILE, {"pending": [], "completed": []})

        for i, task in enumerate(tasks["pending"]):
            if task["id"] == task_id:
                task["completed_at"] = datetime.now().isoformat()
                tasks["completed"].append(task)
                tasks["pending"].pop(i)
                _save_json(TASKS_FILE, tasks)
                return {"task_id": task_id, "status": "completed"}

        return {"error": f"Task not found: {task_id}"}

    async def _list_tasks(self, args: dict) -> dict:
        status = args.get("status", "pending")
        tasks = _load_json(TASKS_FILE, {"pending": [], "completed": []})

        if status == "all":
            return tasks
        return {"tasks": tasks.get(status, []), "count": len(tasks.get(status, []))}

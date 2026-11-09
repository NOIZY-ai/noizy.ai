#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Codebase Tools
==================================
Code search, read, write, list. Extracted from v1 monolith.
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from ..config import NOIZYLAB_ROOT


class CodebaseTools:
    """Codebase interaction tools."""

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        dispatch = {
            "search": self._search,
            "read": self._read,
            "write": self._write,
            "list": self._list,
            "scan": self._scan,
            "git_status": self._git_status,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown codebase action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    async def _search(self, args: dict) -> dict:
        query = args.get("query", "")
        path = Path(args.get("path", str(NOIZYLAB_ROOT)))
        search_type = args.get("type", "both")
        results = {"files": [], "matches": []}

        if search_type in ("filename", "both"):
            for p in path.rglob("*"):
                if p.is_file() and query.lower() in p.name.lower():
                    results["files"].append(str(p))
                    if len(results["files"]) >= 50:
                        break

        if search_type in ("content", "both"):
            try:
                cmd = [
                    "grep", "-r", "-l", "-i",
                    "--include=*.py", "--include=*.ts", "--include=*.js", "--include=*.md",
                    query, str(path),
                ]
                proc = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await proc.communicate()
                results["matches"] = [m for m in stdout.decode().strip().split("\n") if m][:50]
            except OSError:
                pass

        return results

    async def _read(self, args: dict) -> dict:
        path = Path(args.get("path", ""))
        max_lines = args.get("lines", 500)

        if not path.exists():
            return {"error": f"File not found: {path}"}
        if not path.is_file():
            return {"error": f"Not a file: {path}"}

        content = path.read_text()
        lines = content.split("\n")
        truncated = len(lines) > max_lines

        return {
            "path": str(path),
            "lines": len(lines),
            "truncated": truncated,
            "content": "\n".join(lines[:max_lines]),
        }

    async def _write(self, args: dict) -> dict:
        path = Path(args.get("path", ""))
        content = args.get("content", "")
        append = args.get("append", False)

        path.parent.mkdir(parents=True, exist_ok=True)
        if append:
            with open(path, "a") as f:
                f.write(content)
        else:
            path.write_text(content)

        return {"path": str(path), "status": "written", "mode": "append" if append else "overwrite"}

    async def _list(self, args: dict) -> dict:
        path = Path(args.get("path", str(NOIZYLAB_ROOT)))
        pattern = args.get("pattern", "*")
        recursive = args.get("recursive", False)

        if not path.exists():
            return {"error": f"Path not found: {path}"}

        items = list(path.rglob(pattern) if recursive else path.glob(pattern))[:100]
        return {
            "path": str(path),
            "count": len(items),
            "items": [
                {"name": f.name, "type": "dir" if f.is_dir() else "file", "size": f.stat().st_size if f.is_file() else 0}
                for f in items
            ],
        }

    async def _scan(self, args: dict) -> dict:
        path = Path(args.get("path", str(NOIZYLAB_ROOT)))
        depth = args.get("depth", 3)

        if not path.exists():
            return {"error": f"Path not found: {path}"}

        stats = {"root": str(path), "files": 0, "dirs": 0, "by_type": {}}

        def scan(current: Path, d: int):
            if d > depth:
                return
            try:
                for item in sorted(current.iterdir()):
                    if item.name.startswith("."):
                        continue
                    if item.is_dir():
                        stats["dirs"] += 1
                        if d < depth:
                            scan(item, d + 1)
                    else:
                        stats["files"] += 1
                        ext = item.suffix or "no_ext"
                        stats["by_type"][ext] = stats["by_type"].get(ext, 0) + 1
            except PermissionError:
                pass

        scan(path, 0)
        return stats

    async def _git_status(self, args: dict) -> dict:
        path = args.get("path", str(NOIZYLAB_ROOT))
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "status", "--porcelain", "-b",
                cwd=path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            return {"status": stdout.decode() or "clean"}
        except Exception as e:
            return {"error": str(e)}

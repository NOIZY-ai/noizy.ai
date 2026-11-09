#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Tool Router
==============================
Thin dispatch layer. Maps namespaced tool calls to their handlers.

Tool naming convention:
  chamber.*    → ChamberOrchestrator
  audio.*      → AudioTools
  character.*  → CharacterTools
  memory.*     → MemoryTools
  codebase.*   → CodebaseTools
  system.*     → SystemTools
  knowledge.*  → KnowledgeTools
  github.*     → GitHubTools (gh CLI)
  gh.*         → GitHubAPITools (REST API direct)
  git.*        → GitTools (local git operations)
"""

import json
from typing import Any

from .chamber import ChamberOrchestrator
from ..tools.audio import AudioTools
from ..tools.characters import CharacterTools
from ..tools.memory import MemoryTools
from ..tools.codebase import CodebaseTools
from ..tools.system import SystemTools
from ..tools.knowledge import KnowledgeTools
from ..tools.github import GitHubTools
from ..tools.github_api import GitHubAPITools
from ..tools.git import GitTools


class ToolRouter:
    """
    Routes MCP tool calls to domain handlers.

    Each tool name is namespaced: "domain.action"
    The router splits on the dot and dispatches.
    """

    def __init__(self):
        self.chamber = ChamberOrchestrator()
        self.audio = AudioTools()
        self.characters = CharacterTools()
        self.memory = MemoryTools()
        self.codebase = CodebaseTools()
        self.system = SystemTools()
        self.knowledge = KnowledgeTools()
        self.github = GitHubTools()
        self.github_api = GitHubAPITools()
        self.git = GitTools()

        # Domain registry — maps prefix to handler
        self._domains = {
            "chamber": self._handle_chamber,
            "audio": self._handle_audio,
            "character": self._handle_character,
            "memory": self._handle_memory,
            "codebase": self._handle_codebase,
            "system": self._handle_system,
            "knowledge": self._handle_knowledge,
            "github": self._handle_github,
            "gh": self._handle_github_api,
            "git": self._handle_git,
        }

    async def route(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """
        Route a tool call to the appropriate domain handler.
        Returns JSON string (MCP-ready).
        """
        parts = tool_name.split(".", 1)
        if len(parts) != 2:
            return json.dumps({"error": f"Invalid tool name format: {tool_name}. Use 'domain.action'"})

        domain, action = parts
        handler = self._domains.get(domain)
        if not handler:
            return json.dumps({"error": f"Unknown domain: {domain}. Available: {list(self._domains.keys())}"})

        try:
            result = await handler(action, arguments)
            if isinstance(result, str):
                return result
            return json.dumps(result, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e), "domain": domain, "action": action})

    # ── Domain Handlers ─────────────────────────────────────────────

    async def _handle_chamber(self, action: str, args: dict) -> Any:
        dispatch = {
            "start": lambda: self.chamber.start_session(
                characters=args.get("characters"),
                metadata=args.get("metadata"),
            ),
            "activate": lambda: self.chamber.activate_chamber(args.get("session_id")),
            "process": lambda: self.chamber.begin_processing(args.get("session_id")),
            "complete": lambda: self.chamber.complete_processing(
                args.get("session_id"), args.get("results")
            ),
            "close": lambda: self.chamber.close_session(args.get("session_id")),
            "status": lambda: self.chamber.status(args.get("session_id")),
            "add_character": lambda: self.chamber.add_character(
                args["character"], args.get("session_id")
            ),
            "remove_character": lambda: self.chamber.remove_character(
                args["character"], args.get("session_id")
            ),
            "list_characters": lambda: self.chamber.list_characters(args.get("session_id")),
            "queue_audio": lambda: self.chamber.queue_audio(
                args["character"], args["action_type"],
                args.get("params"), args.get("session_id")
            ),
            "audio_status": lambda: self.chamber.get_audio_status(args.get("session_id")),
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown chamber action: {action}", "available": list(dispatch.keys())}
        return fn()

    async def _handle_audio(self, action: str, args: dict) -> Any:
        return await self.audio.handle(action, args)

    async def _handle_character(self, action: str, args: dict) -> Any:
        return await self.characters.handle(action, args)

    async def _handle_memory(self, action: str, args: dict) -> Any:
        return await self.memory.handle(action, args)

    async def _handle_codebase(self, action: str, args: dict) -> Any:
        return await self.codebase.handle(action, args)

    async def _handle_system(self, action: str, args: dict) -> Any:
        return await self.system.handle(action, args)

    async def _handle_knowledge(self, action: str, args: dict) -> Any:
        return await self.knowledge.handle(action, args)

    async def _handle_github(self, action: str, args: dict) -> Any:
        return await self.github.handle(action, args)

    async def _handle_github_api(self, action: str, args: dict) -> Any:
        return await self.github_api.handle(action, args)

    async def _handle_git(self, action: str, args: dict) -> Any:
        return await self.git.handle(action, args)

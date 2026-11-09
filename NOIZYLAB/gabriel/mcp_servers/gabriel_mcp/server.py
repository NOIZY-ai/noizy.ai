#!/usr/bin/env python3
"""
GABRIEL MCP SERVER v2
======================
Thin entry point. Routes to orchestrator. That's it.

Architecture:
  server.py (this file) → ToolRouter → domain handlers → StateStore

  Claude asks → Gabriel dispatches → heavy lifting stays local →
  lightweight summary returns across the wire.

Tool Naming Convention:
  chamber.start       → Start dream chamber session
  chamber.status      → Get session status
  chamber.activate    → Activate chamber
  chamber.process     → Begin audio processing
  chamber.complete    → Mark processing done
  chamber.close       → Close session
  chamber.add_character    → Add character to session
  chamber.remove_character → Remove character
  chamber.list_characters  → List loaded characters
  chamber.queue_audio      → Queue audio job
  chamber.audio_status     → Audio pipeline status
  audio.process       → Queue audio processing
  audio.route_to_cocoro → Route through Cocoro
  audio.route_to_fish   → Route through Fish
  audio.render        → Render output
  audio.export        → Export final
  audio.status        → Job status
  audio.list_jobs     → List audio jobs
  character.list      → List available characters
  character.get       → Get character summary
  character.create    → Create character definition
  character.update    → Update character
  character.delete    → Delete character
  memory.store        → Store memory
  memory.recall       → Search memory
  memory.add_task     → Add task
  memory.complete_task → Complete task
  memory.list_tasks   → List tasks
  codebase.search     → Search code
  codebase.read       → Read file
  codebase.write      → Write file
  codebase.list       → List directory
  codebase.scan       → Scan project structure
  codebase.git_status → Git status
  system.info         → System info
  system.run          → Run command
  knowledge.stats     → Brain statistics
  knowledge.search    → Search knowledge
  knowledge.prompts   → Search prompts
  knowledge.functions → Search functions
  knowledge.entries   → Search knowledge base
  knowledge.imports   → List imports
  knowledge.todos     → List TODOs
  knowledge.explore   → Explore by category
"""

import asyncio
import json
import sys
from datetime import datetime

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types
except ImportError:
    import subprocess
    print("Installing MCP SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp"])
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types

from config import ensure_dirs, SERVER_NAME, SERVER_VERSION
from orchestrator.router import ToolRouter

# ── Initialize ──────────────────────────────────────────────────────
ensure_dirs()
app = Server(SERVER_NAME)
router = ToolRouter()


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr)


# ── Tool Definitions ────────────────────────────────────────────────
# Each tool is namespaced: "domain.action"
# The router handles dispatch. Server just declares the schema.

TOOL_DEFINITIONS = [
    # ── CHAMBER (Dream Chamber Orchestration) ───────────────────
    types.Tool(
        name="chamber.start",
        description="Start a dream chamber session. Loads characters, initializes pipeline.",
        inputSchema={
            "type": "object",
            "properties": {
                "characters": {"type": "array", "items": {"type": "string"}, "description": "Character names to load"},
                "metadata": {"type": "object", "description": "Session metadata"},
            },
        },
    ),
    types.Tool(
        name="chamber.status",
        description="Get current chamber session status",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "Session ID (uses current if empty)"},
            },
        },
    ),
    types.Tool(
        name="chamber.activate",
        description="Activate the chamber — characters loaded, ready to flow",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="chamber.process",
        description="Begin audio processing pipeline",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="chamber.complete",
        description="Mark processing complete with results",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "results": {"type": "object", "description": "Processing results (stays on Gabriel)"},
            },
        },
    ),
    types.Tool(
        name="chamber.close",
        description="Close a chamber session",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="chamber.add_character",
        description="Add a character to the active session",
        inputSchema={
            "type": "object",
            "properties": {
                "character": {"type": "string", "description": "Character name"},
                "session_id": {"type": "string"},
            },
            "required": ["character"],
        },
    ),
    types.Tool(
        name="chamber.list_characters",
        description="List characters in session and available on disk",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="chamber.queue_audio",
        description="Queue an audio processing job for a character",
        inputSchema={
            "type": "object",
            "properties": {
                "character": {"type": "string"},
                "action_type": {"type": "string", "enum": ["record", "process_cocoro", "process_fish", "render", "export"]},
                "params": {"type": "object"},
                "session_id": {"type": "string"},
            },
            "required": ["character", "action_type"],
        },
    ),
    types.Tool(
        name="chamber.audio_status",
        description="Get audio pipeline status for current session",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
            },
        },
    ),
    # ── AUDIO ───────────────────────────────────────────────────
    types.Tool(
        name="audio.process",
        description="Queue standalone audio processing",
        inputSchema={
            "type": "object",
            "properties": {
                "character": {"type": "string"},
                "source": {"type": "string", "description": "Source file path"},
                "pipeline": {"type": "string", "default": "default"},
            },
        },
    ),
    types.Tool(
        name="audio.route_to_cocoro",
        description="Route audio through Cocoro processing",
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {"type": "string"},
                "character": {"type": "string"},
                "preset": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="audio.route_to_fish",
        description="Route audio through Fish processing",
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {"type": "string"},
                "character": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="audio.list_jobs",
        description="List audio processing jobs",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 20},
            },
        },
    ),
    # ── CHARACTER ───────────────────────────────────────────────
    types.Tool(
        name="character.list",
        description="List all available character definitions",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="character.get",
        description="Get character configuration summary",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        },
    ),
    types.Tool(
        name="character.create",
        description="Create a new character definition",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "voice_profile": {"type": "string"},
                "cocoro_preset": {"type": "string"},
                "fish_preset": {"type": "string"},
                "personality": {"type": "string"},
            },
            "required": ["name"],
        },
    ),
    # ── MEMORY ──────────────────────────────────────────────────
    types.Tool(
        name="memory.store",
        description="Store information in Gabriel memory",
        inputSchema={
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["key", "value"],
        },
    ),
    types.Tool(
        name="memory.recall",
        description="Search Gabriel memory",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    ),
    types.Tool(
        name="memory.add_task",
        description="Add a task",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
            },
            "required": ["title"],
        },
    ),
    types.Tool(
        name="memory.list_tasks",
        description="List tasks",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["pending", "completed", "all"], "default": "pending"},
            },
        },
    ),
    # ── CODEBASE ────────────────────────────────────────────────
    types.Tool(
        name="codebase.search",
        description="Search codebase for files or content",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "path": {"type": "string"},
                "type": {"type": "string", "enum": ["filename", "content", "both"], "default": "both"},
            },
            "required": ["query"],
        },
    ),
    types.Tool(
        name="codebase.read",
        description="Read file contents",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "lines": {"type": "integer", "default": 500},
            },
            "required": ["path"],
        },
    ),
    types.Tool(
        name="codebase.scan",
        description="Scan project structure",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "depth": {"type": "integer", "default": 3},
            },
            "required": ["path"],
        },
    ),
    types.Tool(
        name="codebase.git_status",
        description="Git status",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
        },
    ),
    # ── SYSTEM ──────────────────────────────────────────────────
    types.Tool(
        name="system.info",
        description="Get system information",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="system.run",
        description="Execute a shell command (safe commands only)",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "cwd": {"type": "string"},
                "timeout": {"type": "integer", "default": 30},
            },
            "required": ["command"],
        },
    ),
    # ── KNOWLEDGE ───────────────────────────────────────────────
    types.Tool(
        name="knowledge.stats",
        description="Get brain statistics",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="knowledge.search",
        description="Search deep knowledge index",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "type": {"type": "string", "enum": ["all", "prompts", "functions", "classes", "knowledge", "files"], "default": "all"},
                "limit": {"type": "integer", "default": 20},
            },
            "required": ["query"],
        },
    ),
    types.Tool(
        name="knowledge.explore",
        description="Explore files by category",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["voice", "ai_ml", "prompts", "api", "database", "cloud", "network", "automation", "ui", "config", "docs"]},
                "limit": {"type": "integer", "default": 30},
            },
            "required": ["category"],
        },
    ),
    # ── GITHUB (GitHub Genius) ─────────────────────────────────
    types.Tool(
        name="github.pr_list",
        description="List pull requests",
        inputSchema={
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                "limit": {"type": "integer", "default": 30},
                "base": {"type": "string", "description": "Filter by base branch"},
                "author": {"type": "string", "description": "Filter by author"},
            },
        },
    ),
    types.Tool(
        name="github.pr_view",
        description="View detailed PR information",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "integer", "description": "PR number"},
            },
            "required": ["number"],
        },
    ),
    types.Tool(
        name="github.pr_create",
        description="Create a pull request",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "base": {"type": "string", "default": "main"},
                "head": {"type": "string", "description": "Source branch"},
                "draft": {"type": "boolean", "default": False},
            },
            "required": ["title"],
        },
    ),
    types.Tool(
        name="github.pr_merge",
        description="Merge a pull request",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "integer"},
                "method": {"type": "string", "enum": ["merge", "squash", "rebase"], "default": "squash"},
                "delete_branch": {"type": "boolean", "default": True},
            },
            "required": ["number"],
        },
    ),
    types.Tool(
        name="github.pr_checks",
        description="Get PR check/CI status",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "integer"},
            },
            "required": ["number"],
        },
    ),
    types.Tool(
        name="github.pr_review",
        description="Submit a PR review (approve, comment, request changes)",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "integer"},
                "action": {"type": "string", "enum": ["approve", "comment", "request-changes"], "default": "comment"},
                "body": {"type": "string", "description": "Review comment"},
            },
            "required": ["number"],
        },
    ),
    types.Tool(
        name="github.issue_list",
        description="List issues",
        inputSchema={
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                "limit": {"type": "integer", "default": 30},
                "labels": {"type": "string", "description": "Filter by label"},
            },
        },
    ),
    types.Tool(
        name="github.issue_create",
        description="Create an issue",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "labels": {"type": "array", "items": {"type": "string"}},
                "assignees": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["title"],
        },
    ),
    types.Tool(
        name="github.issue_close",
        description="Close an issue",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "integer"},
                "reason": {"type": "string", "enum": ["completed", "not_planned"], "default": "completed"},
            },
            "required": ["number"],
        },
    ),
    types.Tool(
        name="github.workflow_list",
        description="List GitHub Actions workflows",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="github.run_list",
        description="List recent workflow runs",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 10},
                "workflow": {"type": "string", "description": "Filter by workflow name"},
            },
        },
    ),
    types.Tool(
        name="github.run_view",
        description="View a workflow run's details",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Run ID"},
            },
            "required": ["id"],
        },
    ),
    types.Tool(
        name="github.analyze_repo",
        description="Comprehensive repository analysis (PRs, issues, actions, languages)",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="github.analyze_pr",
        description="Deep PR analysis for code review readiness",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "integer"},
            },
            "required": ["number"],
        },
    ),
    types.Tool(
        name="github.branch_list",
        description="List repository branches",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="github.branch_compare",
        description="Compare two branches (ahead/behind commits)",
        inputSchema={
            "type": "object",
            "properties": {
                "base": {"type": "string", "default": "main"},
                "head": {"type": "string", "description": "Branch to compare"},
            },
            "required": ["head"],
        },
    ),
    # ── GH (GitHub REST API Direct) ────────────────────────────────
    types.Tool(
        name="gh.api",
        description="Raw GitHub API request (GET/POST/PATCH/PUT/DELETE)",
        inputSchema={
            "type": "object",
            "properties": {
                "method": {"type": "string", "enum": ["GET", "POST", "PATCH", "PUT", "DELETE"], "default": "GET"},
                "endpoint": {"type": "string", "description": "API endpoint (e.g., /repos/owner/repo)"},
                "params": {"type": "object", "description": "Query parameters"},
                "data": {"type": "object", "description": "Request body"},
            },
            "required": ["endpoint"],
        },
    ),
    types.Tool(
        name="gh.auth_status",
        description="Check GitHub authentication status",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="gh.pulls",
        description="List pull requests via API",
        inputSchema={
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                "limit": {"type": "integer", "default": 30},
            },
            "required": ["owner", "repo"],
        },
    ),
    types.Tool(
        name="gh.pull",
        description="Get PR details via API",
        inputSchema={
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "number": {"type": "integer"},
            },
            "required": ["owner", "repo", "number"],
        },
    ),
    types.Tool(
        name="gh.issues",
        description="List issues via API",
        inputSchema={
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                "limit": {"type": "integer", "default": 30},
            },
            "required": ["owner", "repo"],
        },
    ),
    types.Tool(
        name="gh.search_code",
        description="Search code across GitHub",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "limit": {"type": "integer", "default": 30},
            },
            "required": ["query"],
        },
    ),
    types.Tool(
        name="gh.graphql",
        description="Execute GraphQL query",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "GraphQL query"},
                "variables": {"type": "object", "description": "Query variables"},
            },
            "required": ["query"],
        },
    ),
    # ── GIT (Local Git Operations) ─────────────────────────────────
    types.Tool(
        name="git.status",
        description="Get repository status",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repository path"},
                "short": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.log",
        description="Get commit log",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 20},
                "branch": {"type": "string"},
                "file": {"type": "string"},
                "oneline": {"type": "boolean", "default": True},
            },
        },
    ),
    types.Tool(
        name="git.diff",
        description="Show diff",
        inputSchema={
            "type": "object",
            "properties": {
                "staged": {"type": "boolean", "default": False},
                "ref1": {"type": "string"},
                "ref2": {"type": "string"},
                "file": {"type": "string"},
                "stat": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.branch_list",
        description="List branches",
        inputSchema={
            "type": "object",
            "properties": {
                "all": {"type": "boolean", "default": False},
                "remote": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.branch_create",
        description="Create a branch",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "base": {"type": "string"},
                "checkout": {"type": "boolean", "default": False},
            },
            "required": ["name"],
        },
    ),
    types.Tool(
        name="git.checkout",
        description="Checkout a ref",
        inputSchema={
            "type": "object",
            "properties": {
                "ref": {"type": "string"},
                "create": {"type": "boolean", "default": False},
            },
            "required": ["ref"],
        },
    ),
    types.Tool(
        name="git.commit",
        description="Create a commit",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "all": {"type": "boolean", "default": False},
            },
            "required": ["message"],
        },
    ),
    types.Tool(
        name="git.add",
        description="Stage files",
        inputSchema={
            "type": "object",
            "properties": {
                "files": {"type": "array", "items": {"type": "string"}},
                "all": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.push",
        description="Push to remote",
        inputSchema={
            "type": "object",
            "properties": {
                "remote": {"type": "string", "default": "origin"},
                "branch": {"type": "string"},
                "set_upstream": {"type": "boolean", "default": False},
                "force": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.pull",
        description="Pull from remote",
        inputSchema={
            "type": "object",
            "properties": {
                "remote": {"type": "string", "default": "origin"},
                "branch": {"type": "string"},
                "rebase": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.fetch",
        description="Fetch from remote",
        inputSchema={
            "type": "object",
            "properties": {
                "remote": {"type": "string", "default": "origin"},
                "branch": {"type": "string"},
                "prune": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.stash_save",
        description="Save changes to stash",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "include_untracked": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.stash_pop",
        description="Pop from stash",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "integer", "default": 0},
            },
        },
    ),
    types.Tool(
        name="git.stash_list",
        description="List stashes",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="git.merge",
        description="Merge a branch",
        inputSchema={
            "type": "object",
            "properties": {
                "branch": {"type": "string"},
                "no_ff": {"type": "boolean", "default": False},
                "squash": {"type": "boolean", "default": False},
                "message": {"type": "string"},
            },
            "required": ["branch"],
        },
    ),
    types.Tool(
        name="git.rebase",
        description="Rebase onto a branch",
        inputSchema={
            "type": "object",
            "properties": {
                "onto": {"type": "string"},
                "abort": {"type": "boolean", "default": False},
                "continue": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="git.tag_list",
        description="List tags",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="git.tag_create",
        description="Create a tag",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "message": {"type": "string"},
                "ref": {"type": "string"},
            },
            "required": ["name"],
        },
    ),
    types.Tool(
        name="git.contributors",
        description="List contributors by commit count",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="git.search_commits",
        description="Search commit messages",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 20},
            },
            "required": ["query"],
        },
    ),
]


# ── MCP Handlers ────────────────────────────────────────────────────

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return TOOL_DEFINITIONS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """All tool calls go through the router. Server doesn't touch logic."""
    result = await router.route(name, arguments)
    return [types.TextContent(type="text", text=result)]


# ── Main ────────────────────────────────────────────────────────────

async def main():
    log(f"GABRIEL MCP Server v{SERVER_VERSION} starting...")
    log(f"Tools registered: {len(TOOL_DEFINITIONS)}")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

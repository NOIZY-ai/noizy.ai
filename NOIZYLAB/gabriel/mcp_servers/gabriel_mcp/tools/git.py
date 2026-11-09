#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Local Git Tools
===================================
Pure git operations. No GitHub API required.
Works offline. Handles all local repository management.

Consolidates git operations from codebase.py and adds
comprehensive branch, commit, stash, and merge capabilities.
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..config import NOIZYLAB_ROOT


async def _run_git(args: list[str], cwd: Optional[str] = None) -> dict:
    """Run git command and return parsed output."""
    cmd = ["git"] + args
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd or str(NOIZYLAB_ROOT),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)

        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if proc.returncode != 0:
            return {"error": error or f"git exited with code {proc.returncode}", "code": proc.returncode}

        return {"output": output, "code": 0}

    except asyncio.TimeoutError:
        return {"error": "Command timed out", "code": -1}
    except FileNotFoundError:
        return {"error": "git not found", "code": -1}
    except Exception as e:
        return {"error": str(e), "code": -1}


class GitTools:
    """Local git operations for Gabriel MCP."""

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        """Dispatch git actions."""
        dispatch = {
            # Status & Info
            "status": self._status,
            "log": self._log,
            "show": self._show,
            "diff": self._diff,
            "blame": self._blame,
            # Branches
            "branch_list": self._branch_list,
            "branch_create": self._branch_create,
            "branch_delete": self._branch_delete,
            "branch_current": self._branch_current,
            "checkout": self._checkout,
            "switch": self._switch,
            # Commits
            "commit": self._commit,
            "amend": self._amend,
            "reset": self._reset,
            "revert": self._revert,
            # Staging
            "add": self._add,
            "unstage": self._unstage,
            "discard": self._discard,
            # Remote
            "fetch": self._fetch,
            "pull": self._pull,
            "push": self._push,
            "remote_list": self._remote_list,
            # Stash
            "stash_save": self._stash_save,
            "stash_pop": self._stash_pop,
            "stash_list": self._stash_list,
            "stash_drop": self._stash_drop,
            # Merge & Rebase
            "merge": self._merge,
            "rebase": self._rebase,
            "cherry_pick": self._cherry_pick,
            # Tags
            "tag_list": self._tag_list,
            "tag_create": self._tag_create,
            "tag_delete": self._tag_delete,
            # Analysis
            "contributors": self._contributors,
            "file_history": self._file_history,
            "search_commits": self._search_commits,
            # Config
            "config_get": self._config_get,
            "config_set": self._config_set,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown git action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    # ── Status & Info ───────────────────────────────────────────────

    async def _status(self, args: dict) -> dict:
        """Get repository status."""
        cwd = args.get("path")
        short = args.get("short", False)

        cmd = ["status", "--porcelain", "-b"] if short else ["status"]
        result = await _run_git(cmd, cwd)

        if "error" in result:
            return result

        output = result["output"]

        if short:
            lines = output.split("\n")
            branch_line = lines[0] if lines else ""
            changes = [l for l in lines[1:] if l.strip()]

            return {
                "branch": branch_line.replace("## ", "").split("...")[0] if branch_line else "unknown",
                "clean": len(changes) == 0,
                "changes": len(changes),
                "files": [{"status": l[:2].strip(), "path": l[3:]} for l in changes],
            }

        return {"status": output}

    async def _log(self, args: dict) -> dict:
        """Get commit log."""
        limit = args.get("limit", 20)
        branch = args.get("branch")
        path = args.get("file")
        oneline = args.get("oneline", True)
        cwd = args.get("path")

        cmd = ["log", f"-{limit}"]
        if oneline:
            cmd.append("--oneline")
        else:
            cmd.extend(["--format=%H|%an|%ae|%at|%s"])
        if branch:
            cmd.append(branch)
        if path:
            cmd.extend(["--", path])

        result = await _run_git(cmd, cwd)
        if "error" in result:
            return result

        if oneline:
            commits = []
            for line in result["output"].split("\n"):
                if line.strip():
                    parts = line.split(" ", 1)
                    commits.append({"sha": parts[0], "message": parts[1] if len(parts) > 1 else ""})
            return {"commits": commits}

        commits = []
        for line in result["output"].split("\n"):
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 5:
                    commits.append({
                        "sha": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "timestamp": parts[3],
                        "message": parts[4],
                    })
        return {"commits": commits}

    async def _show(self, args: dict) -> dict:
        """Show commit details."""
        ref = args.get("ref", "HEAD")
        stat = args.get("stat", True)
        cwd = args.get("path")

        cmd = ["show", ref]
        if stat:
            cmd.append("--stat")
        else:
            cmd.append("--name-only")

        result = await _run_git(cmd, cwd)
        return result

    async def _diff(self, args: dict) -> dict:
        """Show diff."""
        staged = args.get("staged", False)
        ref1 = args.get("ref1")
        ref2 = args.get("ref2")
        path = args.get("file")
        stat = args.get("stat", False)
        cwd = args.get("path")

        cmd = ["diff"]
        if staged:
            cmd.append("--staged")
        if stat:
            cmd.append("--stat")
        if ref1:
            cmd.append(ref1)
        if ref2:
            cmd.append(ref2)
        if path:
            cmd.extend(["--", path])

        result = await _run_git(cmd, cwd)
        return result

    async def _blame(self, args: dict) -> dict:
        """Show file blame."""
        file_path = args.get("file")
        if not file_path:
            return {"error": "file required"}

        cwd = args.get("path")
        result = await _run_git(["blame", "--line-porcelain", file_path], cwd)
        return result

    # ── Branches ────────────────────────────────────────────────────

    async def _branch_list(self, args: dict) -> dict:
        """List branches."""
        all_branches = args.get("all", False)
        remote = args.get("remote", False)
        cwd = args.get("path")

        cmd = ["branch"]
        if all_branches:
            cmd.append("-a")
        elif remote:
            cmd.append("-r")
        cmd.append("--format=%(refname:short)|%(objectname:short)|%(upstream:short)")

        result = await _run_git(cmd, cwd)
        if "error" in result:
            return result

        branches = []
        for line in result["output"].split("\n"):
            if "|" in line:
                parts = line.split("|")
                branches.append({
                    "name": parts[0],
                    "sha": parts[1] if len(parts) > 1 else "",
                    "upstream": parts[2] if len(parts) > 2 else "",
                })
        return {"branches": branches}

    async def _branch_create(self, args: dict) -> dict:
        """Create a branch."""
        name = args.get("name")
        base = args.get("base")
        checkout = args.get("checkout", False)
        cwd = args.get("path")

        if not name:
            return {"error": "branch name required"}

        if checkout:
            cmd = ["checkout", "-b", name]
        else:
            cmd = ["branch", name]

        if base:
            cmd.append(base)

        result = await _run_git(cmd, cwd)
        if "error" not in result:
            result["created"] = name
        return result

    async def _branch_delete(self, args: dict) -> dict:
        """Delete a branch."""
        name = args.get("name")
        force = args.get("force", False)
        cwd = args.get("path")

        if not name:
            return {"error": "branch name required"}

        cmd = ["branch", "-D" if force else "-d", name]
        result = await _run_git(cmd, cwd)
        if "error" not in result:
            result["deleted"] = name
        return result

    async def _branch_current(self, args: dict) -> dict:
        """Get current branch name."""
        cwd = args.get("path")
        result = await _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
        if "error" not in result:
            return {"branch": result["output"]}
        return result

    async def _checkout(self, args: dict) -> dict:
        """Checkout a ref."""
        ref = args.get("ref")
        create = args.get("create", False)
        cwd = args.get("path")

        if not ref:
            return {"error": "ref required"}

        cmd = ["checkout"]
        if create:
            cmd.append("-b")
        cmd.append(ref)

        return await _run_git(cmd, cwd)

    async def _switch(self, args: dict) -> dict:
        """Switch branches (modern git switch)."""
        branch = args.get("branch")
        create = args.get("create", False)
        cwd = args.get("path")

        if not branch:
            return {"error": "branch required"}

        cmd = ["switch"]
        if create:
            cmd.append("-c")
        cmd.append(branch)

        return await _run_git(cmd, cwd)

    # ── Commits ─────────────────────────────────────────────────────

    async def _commit(self, args: dict) -> dict:
        """Create a commit."""
        message = args.get("message")
        all_changes = args.get("all", False)
        cwd = args.get("path")

        if not message:
            return {"error": "commit message required"}

        cmd = ["commit", "-m", message]
        if all_changes:
            cmd.append("-a")

        return await _run_git(cmd, cwd)

    async def _amend(self, args: dict) -> dict:
        """Amend the last commit."""
        message = args.get("message")
        no_edit = args.get("no_edit", True)
        cwd = args.get("path")

        cmd = ["commit", "--amend"]
        if message:
            cmd.extend(["-m", message])
        elif no_edit:
            cmd.append("--no-edit")

        return await _run_git(cmd, cwd)

    async def _reset(self, args: dict) -> dict:
        """Reset to a ref."""
        ref = args.get("ref", "HEAD")
        mode = args.get("mode", "mixed")  # soft, mixed, hard
        cwd = args.get("path")

        cmd = ["reset", f"--{mode}", ref]
        return await _run_git(cmd, cwd)

    async def _revert(self, args: dict) -> dict:
        """Revert a commit."""
        ref = args.get("ref")
        no_commit = args.get("no_commit", False)
        cwd = args.get("path")

        if not ref:
            return {"error": "ref required"}

        cmd = ["revert", ref]
        if no_commit:
            cmd.append("--no-commit")

        return await _run_git(cmd, cwd)

    # ── Staging ─────────────────────────────────────────────────────

    async def _add(self, args: dict) -> dict:
        """Stage files."""
        files = args.get("files", [])
        all_files = args.get("all", False)
        cwd = args.get("path")

        if all_files:
            cmd = ["add", "-A"]
        elif files:
            cmd = ["add"] + (files if isinstance(files, list) else [files])
        else:
            return {"error": "files or all=true required"}

        return await _run_git(cmd, cwd)

    async def _unstage(self, args: dict) -> dict:
        """Unstage files."""
        files = args.get("files", [])
        cwd = args.get("path")

        if not files:
            cmd = ["reset", "HEAD"]
        else:
            cmd = ["reset", "HEAD", "--"] + (files if isinstance(files, list) else [files])

        return await _run_git(cmd, cwd)

    async def _discard(self, args: dict) -> dict:
        """Discard changes to files."""
        files = args.get("files", [])
        cwd = args.get("path")

        if not files:
            return {"error": "files required (use git.reset for full discard)"}

        cmd = ["checkout", "--"] + (files if isinstance(files, list) else [files])
        return await _run_git(cmd, cwd)

    # ── Remote ──────────────────────────────────────────────────────

    async def _fetch(self, args: dict) -> dict:
        """Fetch from remote."""
        remote = args.get("remote", "origin")
        branch = args.get("branch")
        prune = args.get("prune", False)
        cwd = args.get("path")

        cmd = ["fetch", remote]
        if branch:
            cmd.append(branch)
        if prune:
            cmd.append("--prune")

        return await _run_git(cmd, cwd)

    async def _pull(self, args: dict) -> dict:
        """Pull from remote."""
        remote = args.get("remote", "origin")
        branch = args.get("branch")
        rebase = args.get("rebase", False)
        cwd = args.get("path")

        cmd = ["pull"]
        if rebase:
            cmd.append("--rebase")
        cmd.append(remote)
        if branch:
            cmd.append(branch)

        return await _run_git(cmd, cwd)

    async def _push(self, args: dict) -> dict:
        """Push to remote."""
        remote = args.get("remote", "origin")
        branch = args.get("branch")
        set_upstream = args.get("set_upstream", False)
        force = args.get("force", False)
        cwd = args.get("path")

        cmd = ["push"]
        if set_upstream:
            cmd.append("-u")
        if force:
            cmd.append("--force-with-lease")  # Safer than --force
        cmd.append(remote)
        if branch:
            cmd.append(branch)

        return await _run_git(cmd, cwd)

    async def _remote_list(self, args: dict) -> dict:
        """List remotes."""
        cwd = args.get("path")
        result = await _run_git(["remote", "-v"], cwd)
        if "error" in result:
            return result

        remotes = {}
        for line in result["output"].split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    url = parts[1]
                    if name not in remotes:
                        remotes[name] = {"name": name, "url": url}

        return {"remotes": list(remotes.values())}

    # ── Stash ───────────────────────────────────────────────────────

    async def _stash_save(self, args: dict) -> dict:
        """Save changes to stash."""
        message = args.get("message")
        include_untracked = args.get("include_untracked", False)
        cwd = args.get("path")

        cmd = ["stash", "push"]
        if include_untracked:
            cmd.append("-u")
        if message:
            cmd.extend(["-m", message])

        return await _run_git(cmd, cwd)

    async def _stash_pop(self, args: dict) -> dict:
        """Pop from stash."""
        index = args.get("index", 0)
        cwd = args.get("path")

        cmd = ["stash", "pop", f"stash@{{{index}}}"]
        return await _run_git(cmd, cwd)

    async def _stash_list(self, args: dict) -> dict:
        """List stashes."""
        cwd = args.get("path")
        result = await _run_git(["stash", "list"], cwd)
        if "error" in result:
            return result

        stashes = []
        for line in result["output"].split("\n"):
            if line.strip():
                stashes.append(line)

        return {"stashes": stashes, "count": len(stashes)}

    async def _stash_drop(self, args: dict) -> dict:
        """Drop a stash."""
        index = args.get("index", 0)
        cwd = args.get("path")

        cmd = ["stash", "drop", f"stash@{{{index}}}"]
        return await _run_git(cmd, cwd)

    # ── Merge & Rebase ──────────────────────────────────────────────

    async def _merge(self, args: dict) -> dict:
        """Merge a branch."""
        branch = args.get("branch")
        no_ff = args.get("no_ff", False)
        squash = args.get("squash", False)
        message = args.get("message")
        cwd = args.get("path")

        if not branch:
            return {"error": "branch required"}

        cmd = ["merge"]
        if no_ff:
            cmd.append("--no-ff")
        if squash:
            cmd.append("--squash")
        if message:
            cmd.extend(["-m", message])
        cmd.append(branch)

        return await _run_git(cmd, cwd)

    async def _rebase(self, args: dict) -> dict:
        """Rebase onto a branch."""
        onto = args.get("onto")
        abort = args.get("abort", False)
        continue_rebase = args.get("continue", False)
        cwd = args.get("path")

        if abort:
            return await _run_git(["rebase", "--abort"], cwd)
        if continue_rebase:
            return await _run_git(["rebase", "--continue"], cwd)
        if not onto:
            return {"error": "onto branch required"}

        return await _run_git(["rebase", onto], cwd)

    async def _cherry_pick(self, args: dict) -> dict:
        """Cherry-pick a commit."""
        ref = args.get("ref")
        no_commit = args.get("no_commit", False)
        cwd = args.get("path")

        if not ref:
            return {"error": "ref required"}

        cmd = ["cherry-pick"]
        if no_commit:
            cmd.append("-n")
        cmd.append(ref)

        return await _run_git(cmd, cwd)

    # ── Tags ────────────────────────────────────────────────────────

    async def _tag_list(self, args: dict) -> dict:
        """List tags."""
        cwd = args.get("path")
        result = await _run_git(["tag", "-l", "--sort=-v:refname"], cwd)
        if "error" in result:
            return result

        tags = [t for t in result["output"].split("\n") if t.strip()]
        return {"tags": tags}

    async def _tag_create(self, args: dict) -> dict:
        """Create a tag."""
        name = args.get("name")
        message = args.get("message")
        ref = args.get("ref")
        cwd = args.get("path")

        if not name:
            return {"error": "tag name required"}

        cmd = ["tag"]
        if message:
            cmd.extend(["-a", name, "-m", message])
        else:
            cmd.append(name)
        if ref:
            cmd.append(ref)

        result = await _run_git(cmd, cwd)
        if "error" not in result:
            result["created"] = name
        return result

    async def _tag_delete(self, args: dict) -> dict:
        """Delete a tag."""
        name = args.get("name")
        cwd = args.get("path")

        if not name:
            return {"error": "tag name required"}

        result = await _run_git(["tag", "-d", name], cwd)
        if "error" not in result:
            result["deleted"] = name
        return result

    # ── Analysis ────────────────────────────────────────────────────

    async def _contributors(self, args: dict) -> dict:
        """List contributors by commit count."""
        cwd = args.get("path")
        result = await _run_git(["shortlog", "-sn", "--all"], cwd)
        if "error" in result:
            return result

        contributors = []
        for line in result["output"].split("\n"):
            if line.strip():
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    contributors.append({
                        "commits": int(parts[0].strip()),
                        "name": parts[1].strip(),
                    })

        return {"contributors": contributors}

    async def _file_history(self, args: dict) -> dict:
        """Get history for a specific file."""
        file_path = args.get("file")
        limit = args.get("limit", 20)
        cwd = args.get("path")

        if not file_path:
            return {"error": "file required"}

        cmd = ["log", f"-{limit}", "--oneline", "--follow", "--", file_path]
        return await _run_git(cmd, cwd)

    async def _search_commits(self, args: dict) -> dict:
        """Search commit messages."""
        query = args.get("query")
        limit = args.get("limit", 20)
        cwd = args.get("path")

        if not query:
            return {"error": "query required"}

        cmd = ["log", f"-{limit}", "--oneline", f"--grep={query}"]
        return await _run_git(cmd, cwd)

    # ── Config ──────────────────────────────────────────────────────

    async def _config_get(self, args: dict) -> dict:
        """Get a git config value."""
        key = args.get("key")
        scope = args.get("scope", "local")  # local, global, system
        cwd = args.get("path")

        if not key:
            return {"error": "key required"}

        cmd = ["config"]
        if scope == "global":
            cmd.append("--global")
        elif scope == "system":
            cmd.append("--system")
        cmd.extend(["--get", key])

        result = await _run_git(cmd, cwd)
        if "error" not in result:
            return {"key": key, "value": result["output"]}
        return result

    async def _config_set(self, args: dict) -> dict:
        """Set a git config value."""
        key = args.get("key")
        value = args.get("value")
        scope = args.get("scope", "local")
        cwd = args.get("path")

        if not key or value is None:
            return {"error": "key and value required"}

        cmd = ["config"]
        if scope == "global":
            cmd.append("--global")
        elif scope == "system":
            cmd.append("--system")
        cmd.extend([key, value])

        result = await _run_git(cmd, cwd)
        if "error" not in result:
            return {"key": key, "value": value, "set": True}
        return result

#!/usr/bin/env python3
"""
GABRIEL MCP v2 — GitHub API Client
=====================================
Direct GitHub REST API integration. No gh CLI dependency.
Supports personal access tokens and GitHub App authentication.

API Version: 2026-03-10
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urljoin, urlencode
import aiohttp

from ..config import NOIZYLAB_ROOT


# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"


def _get_token() -> Optional[str]:
    """Get GitHub token from environment or gh CLI config."""
    # 1. Environment variable
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token

    # 2. Try gh CLI config
    gh_config = os.path.expanduser("~/.config/gh/hosts.yml")
    if os.path.exists(gh_config):
        try:
            import yaml
            with open(gh_config) as f:
                config = yaml.safe_load(f)
                if config and "github.com" in config:
                    return config["github.com"].get("oauth_token")
        except (ImportError, Exception):
            pass

    return None


class GitHubAPIClient:
    """
    Async GitHub REST API client.

    Usage:
        async with GitHubAPIClient() as client:
            user = await client.get("/user")
            repos = await client.get("/user/repos", params={"per_page": 10})
    """

    def __init__(self, token: Optional[str] = None, base_url: str = GITHUB_API_BASE):
        self.token = token or _get_token()
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": GITHUB_API_VERSION,
                "User-Agent": "Gabriel-MCP/2.0",
            }
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            self._session = aiohttp.ClientSession(headers=headers)

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None,
    ) -> dict:
        """Make an API request."""
        await self._ensure_session()

        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        if params:
            url = f"{url}?{urlencode(params)}"

        try:
            async with self._session.request(
                method, url, json=json_data, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                text = await response.text()

                if response.status == 204:
                    return {"success": True, "status": 204}

                try:
                    data = json.loads(text) if text else {}
                except json.JSONDecodeError:
                    data = {"raw": text}

                if response.status >= 400:
                    return {
                        "error": data.get("message", f"HTTP {response.status}"),
                        "status": response.status,
                        "documentation_url": data.get("documentation_url"),
                    }

                return {
                    "data": data,
                    "status": response.status,
                    "rate_limit": {
                        "remaining": response.headers.get("X-RateLimit-Remaining"),
                        "reset": response.headers.get("X-RateLimit-Reset"),
                    },
                }

        except asyncio.TimeoutError:
            return {"error": "Request timed out"}
        except aiohttp.ClientError as e:
            return {"error": str(e)}

    async def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        return await self.request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        return await self.request("POST", endpoint, json_data=data)

    async def patch(self, endpoint: str, data: Optional[dict] = None) -> dict:
        return await self.request("PATCH", endpoint, json_data=data)

    async def put(self, endpoint: str, data: Optional[dict] = None) -> dict:
        return await self.request("PUT", endpoint, json_data=data)

    async def delete(self, endpoint: str) -> dict:
        return await self.request("DELETE", endpoint)


class GitHubAPITools:
    """
    GitHub API tools for Gabriel MCP.
    Direct REST API — no gh CLI required.
    """

    def __init__(self):
        self._client: Optional[GitHubAPIClient] = None

    async def _get_client(self) -> GitHubAPIClient:
        if self._client is None:
            self._client = GitHubAPIClient()
            await self._client._ensure_session()
        return self._client

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        """Dispatch GitHub API actions."""
        dispatch = {
            # Core
            "api": self._raw_api,
            "auth_status": self._auth_status,
            # User
            "user": self._get_user,
            "user_repos": self._user_repos,
            # Repository
            "repo": self._get_repo,
            "repo_contents": self._repo_contents,
            "repo_commits": self._repo_commits,
            "repo_branches": self._repo_branches,
            "repo_tags": self._repo_tags,
            "repo_releases": self._repo_releases,
            "repo_contributors": self._repo_contributors,
            "repo_languages": self._repo_languages,
            "repo_topics": self._repo_topics,
            # Pull Requests
            "pulls": self._list_pulls,
            "pull": self._get_pull,
            "pull_create": self._create_pull,
            "pull_update": self._update_pull,
            "pull_merge": self._merge_pull,
            "pull_files": self._pull_files,
            "pull_commits": self._pull_commits,
            "pull_reviews": self._pull_reviews,
            "pull_review_create": self._create_review,
            # Issues
            "issues": self._list_issues,
            "issue": self._get_issue,
            "issue_create": self._create_issue,
            "issue_update": self._update_issue,
            "issue_comments": self._issue_comments,
            "issue_comment_create": self._create_issue_comment,
            # Actions
            "workflows": self._list_workflows,
            "workflow_runs": self._list_workflow_runs,
            "workflow_run": self._get_workflow_run,
            "workflow_dispatch": self._dispatch_workflow,
            # Search
            "search_code": self._search_code,
            "search_repos": self._search_repos,
            "search_issues": self._search_issues,
            # GraphQL
            "graphql": self._graphql,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown api action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    # ── Core ────────────────────────────────────────────────────────

    async def _raw_api(self, args: dict) -> dict:
        """Make a raw API request."""
        method = args.get("method", "GET").upper()
        endpoint = args.get("endpoint", "")
        params = args.get("params")
        data = args.get("data")

        if not endpoint:
            return {"error": "endpoint required"}

        client = await self._get_client()
        return await client.request(method, endpoint, params=params, json_data=data)

    async def _auth_status(self, args: dict) -> dict:
        """Check authentication status."""
        client = await self._get_client()
        result = await client.get("/user")

        if "error" in result:
            return {
                "authenticated": False,
                "error": result["error"],
                "hint": "Set GITHUB_TOKEN or GH_TOKEN environment variable",
            }

        user = result.get("data", {})
        return {
            "authenticated": True,
            "user": user.get("login"),
            "name": user.get("name"),
            "scopes": result.get("rate_limit"),
        }

    # ── User ────────────────────────────────────────────────────────

    async def _get_user(self, args: dict) -> dict:
        """Get user profile."""
        username = args.get("username")
        client = await self._get_client()

        endpoint = f"/users/{username}" if username else "/user"
        return await client.get(endpoint)

    async def _user_repos(self, args: dict) -> dict:
        """List user repositories."""
        username = args.get("username")
        params = {
            "per_page": args.get("limit", 30),
            "sort": args.get("sort", "updated"),
            "type": args.get("type", "all"),
        }

        client = await self._get_client()
        endpoint = f"/users/{username}/repos" if username else "/user/repos"
        return await client.get(endpoint, params=params)

    # ── Repository ──────────────────────────────────────────────────

    def _parse_repo(self, args: dict) -> tuple[str, str]:
        """Parse owner/repo from args."""
        owner = args.get("owner", "")
        repo = args.get("repo", "")

        # Support "owner/repo" format
        if not owner and "/" in repo:
            owner, repo = repo.split("/", 1)

        return owner, repo

    async def _get_repo(self, args: dict) -> dict:
        """Get repository details."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}")

    async def _repo_contents(self, args: dict) -> dict:
        """Get repository contents (file or directory)."""
        owner, repo = self._parse_repo(args)
        path = args.get("path", "")
        ref = args.get("ref")

        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        params = {"ref": ref} if ref else None
        return await client.get(f"/repos/{owner}/{repo}/contents/{path}", params=params)

    async def _repo_commits(self, args: dict) -> dict:
        """List repository commits."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        params = {
            "per_page": args.get("limit", 30),
            "sha": args.get("branch"),
            "path": args.get("path"),
            "author": args.get("author"),
        }
        params = {k: v for k, v in params.items() if v}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/commits", params=params)

    async def _repo_branches(self, args: dict) -> dict:
        """List repository branches."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/branches", params={"per_page": 100})

    async def _repo_tags(self, args: dict) -> dict:
        """List repository tags."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/tags", params={"per_page": 30})

    async def _repo_releases(self, args: dict) -> dict:
        """List repository releases."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/releases", params={"per_page": 10})

    async def _repo_contributors(self, args: dict) -> dict:
        """List repository contributors."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/contributors", params={"per_page": 30})

    async def _repo_languages(self, args: dict) -> dict:
        """Get repository languages."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/languages")

    async def _repo_topics(self, args: dict) -> dict:
        """Get repository topics."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/topics")

    # ── Pull Requests ───────────────────────────────────────────────

    async def _list_pulls(self, args: dict) -> dict:
        """List pull requests."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        params = {
            "state": args.get("state", "open"),
            "per_page": args.get("limit", 30),
            "sort": args.get("sort", "created"),
            "direction": args.get("direction", "desc"),
            "base": args.get("base"),
            "head": args.get("head"),
        }
        params = {k: v for k, v in params.items() if v}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/pulls", params=params)

    async def _get_pull(self, args: dict) -> dict:
        """Get pull request details."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/pulls/{number}")

    async def _create_pull(self, args: dict) -> dict:
        """Create a pull request."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        data = {
            "title": args.get("title"),
            "body": args.get("body", ""),
            "head": args.get("head"),
            "base": args.get("base", "main"),
            "draft": args.get("draft", False),
        }

        if not data["title"] or not data["head"]:
            return {"error": "title and head branch required"}

        client = await self._get_client()
        return await client.post(f"/repos/{owner}/{repo}/pulls", data=data)

    async def _update_pull(self, args: dict) -> dict:
        """Update a pull request."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        data = {}
        for key in ["title", "body", "state", "base"]:
            if args.get(key):
                data[key] = args[key]

        client = await self._get_client()
        return await client.patch(f"/repos/{owner}/{repo}/pulls/{number}", data=data)

    async def _merge_pull(self, args: dict) -> dict:
        """Merge a pull request."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        data = {
            "merge_method": args.get("method", "squash"),
            "commit_title": args.get("title"),
            "commit_message": args.get("message"),
        }
        data = {k: v for k, v in data.items() if v}

        client = await self._get_client()
        return await client.put(f"/repos/{owner}/{repo}/pulls/{number}/merge", data=data)

    async def _pull_files(self, args: dict) -> dict:
        """Get files changed in a pull request."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/pulls/{number}/files", params={"per_page": 100})

    async def _pull_commits(self, args: dict) -> dict:
        """Get commits in a pull request."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/pulls/{number}/commits", params={"per_page": 100})

    async def _pull_reviews(self, args: dict) -> dict:
        """Get reviews on a pull request."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/pulls/{number}/reviews")

    async def _create_review(self, args: dict) -> dict:
        """Create a pull request review."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        data = {
            "event": args.get("event", "COMMENT"),  # APPROVE, REQUEST_CHANGES, COMMENT
            "body": args.get("body", ""),
            "comments": args.get("comments", []),
        }

        client = await self._get_client()
        return await client.post(f"/repos/{owner}/{repo}/pulls/{number}/reviews", data=data)

    # ── Issues ──────────────────────────────────────────────────────

    async def _list_issues(self, args: dict) -> dict:
        """List issues."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        params = {
            "state": args.get("state", "open"),
            "per_page": args.get("limit", 30),
            "sort": args.get("sort", "created"),
            "direction": args.get("direction", "desc"),
            "labels": args.get("labels"),
            "assignee": args.get("assignee"),
        }
        params = {k: v for k, v in params.items() if v}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/issues", params=params)

    async def _get_issue(self, args: dict) -> dict:
        """Get issue details."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/issues/{number}")

    async def _create_issue(self, args: dict) -> dict:
        """Create an issue."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        data = {
            "title": args.get("title"),
            "body": args.get("body", ""),
            "labels": args.get("labels", []),
            "assignees": args.get("assignees", []),
        }

        if not data["title"]:
            return {"error": "title required"}

        client = await self._get_client()
        return await client.post(f"/repos/{owner}/{repo}/issues", data=data)

    async def _update_issue(self, args: dict) -> dict:
        """Update an issue."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        data = {}
        for key in ["title", "body", "state", "labels", "assignees"]:
            if args.get(key) is not None:
                data[key] = args[key]

        client = await self._get_client()
        return await client.patch(f"/repos/{owner}/{repo}/issues/{number}", data=data)

    async def _issue_comments(self, args: dict) -> dict:
        """Get issue comments."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")

        if not owner or not repo or not number:
            return {"error": "owner, repo, and number required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/issues/{number}/comments", params={"per_page": 100})

    async def _create_issue_comment(self, args: dict) -> dict:
        """Create an issue comment."""
        owner, repo = self._parse_repo(args)
        number = args.get("number")
        body = args.get("body")

        if not owner or not repo or not number or not body:
            return {"error": "owner, repo, number, and body required"}

        client = await self._get_client()
        return await client.post(f"/repos/{owner}/{repo}/issues/{number}/comments", data={"body": body})

    # ── Actions ─────────────────────────────────────────────────────

    async def _list_workflows(self, args: dict) -> dict:
        """List workflows."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/actions/workflows")

    async def _list_workflow_runs(self, args: dict) -> dict:
        """List workflow runs."""
        owner, repo = self._parse_repo(args)
        if not owner or not repo:
            return {"error": "owner and repo required"}

        params = {
            "per_page": args.get("limit", 10),
            "branch": args.get("branch"),
            "status": args.get("status"),
        }
        params = {k: v for k, v in params.items() if v}

        workflow_id = args.get("workflow_id")
        if workflow_id:
            endpoint = f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
        else:
            endpoint = f"/repos/{owner}/{repo}/actions/runs"

        client = await self._get_client()
        return await client.get(endpoint, params=params)

    async def _get_workflow_run(self, args: dict) -> dict:
        """Get workflow run details."""
        owner, repo = self._parse_repo(args)
        run_id = args.get("run_id")

        if not owner or not repo or not run_id:
            return {"error": "owner, repo, and run_id required"}

        client = await self._get_client()
        return await client.get(f"/repos/{owner}/{repo}/actions/runs/{run_id}")

    async def _dispatch_workflow(self, args: dict) -> dict:
        """Trigger a workflow dispatch event."""
        owner, repo = self._parse_repo(args)
        workflow_id = args.get("workflow_id")
        ref = args.get("ref", "main")
        inputs = args.get("inputs", {})

        if not owner or not repo or not workflow_id:
            return {"error": "owner, repo, and workflow_id required"}

        data = {"ref": ref, "inputs": inputs}

        client = await self._get_client()
        return await client.post(f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches", data=data)

    # ── Search ──────────────────────────────────────────────────────

    async def _search_code(self, args: dict) -> dict:
        """Search code."""
        query = args.get("query", "")
        if not query:
            return {"error": "query required"}

        # Add repo scope if provided
        owner, repo = self._parse_repo(args)
        if owner and repo:
            query = f"{query} repo:{owner}/{repo}"

        params = {
            "q": query,
            "per_page": args.get("limit", 30),
        }

        client = await self._get_client()
        return await client.get("/search/code", params=params)

    async def _search_repos(self, args: dict) -> dict:
        """Search repositories."""
        query = args.get("query", "")
        if not query:
            return {"error": "query required"}

        params = {
            "q": query,
            "per_page": args.get("limit", 30),
            "sort": args.get("sort", "stars"),
        }

        client = await self._get_client()
        return await client.get("/search/repositories", params=params)

    async def _search_issues(self, args: dict) -> dict:
        """Search issues and pull requests."""
        query = args.get("query", "")
        if not query:
            return {"error": "query required"}

        # Add repo scope if provided
        owner, repo = self._parse_repo(args)
        if owner and repo:
            query = f"{query} repo:{owner}/{repo}"

        params = {
            "q": query,
            "per_page": args.get("limit", 30),
            "sort": args.get("sort", "created"),
        }

        client = await self._get_client()
        return await client.get("/search/issues", params=params)

    # ── GraphQL ─────────────────────────────────────────────────────

    async def _graphql(self, args: dict) -> dict:
        """Execute a GraphQL query."""
        query = args.get("query", "")
        variables = args.get("variables", {})

        if not query:
            return {"error": "query required"}

        client = await self._get_client()

        # GraphQL uses different endpoint
        async with aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {client.token}",
            "Content-Type": "application/json",
        }) as session:
            async with session.post(
                "https://api.github.com/graphql",
                json={"query": query, "variables": variables},
            ) as response:
                return await response.json()

#!/usr/bin/env python3
"""
GABRIEL MCP v2 — GitHub Tools
================================
GitHub genius for Gabriel. Full gh CLI integration.

Capabilities:
- PR lifecycle (create, review, merge, list, diff)
- Issue management (create, list, close, link to PRs)
- Repository analysis (stats, contributors, languages)
- Branch operations (list, create, delete, compare)
- Actions/Workflows (status, trigger, logs)
- Code review assistance (diff analysis, comment suggestions)
- Intelligent commit message generation
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Any, Optional

from ..config import NOIZYLAB_ROOT


async def _run_gh(args: list[str], cwd: Optional[str] = None) -> dict:
    """Run gh CLI command and return parsed output."""
    cmd = ["gh"] + args
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
            return {"error": error or f"gh exited with code {proc.returncode}"}

        # Try to parse JSON if output looks like JSON
        if output.startswith(("{", "[")):
            try:
                return {"data": json.loads(output)}
            except json.JSONDecodeError:
                pass

        return {"output": output}

    except asyncio.TimeoutError:
        return {"error": "Command timed out"}
    except FileNotFoundError:
        return {"error": "gh CLI not found. Install: https://cli.github.com"}
    except Exception as e:
        return {"error": str(e)}


class GitHubTools:
    """GitHub integration tools for Gabriel MCP."""

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        """Dispatch GitHub actions."""
        dispatch = {
            # PR Operations
            "pr_list": self._pr_list,
            "pr_view": self._pr_view,
            "pr_create": self._pr_create,
            "pr_merge": self._pr_merge,
            "pr_diff": self._pr_diff,
            "pr_checks": self._pr_checks,
            "pr_review": self._pr_review,
            "pr_comment": self._pr_comment,
            # Issue Operations
            "issue_list": self._issue_list,
            "issue_view": self._issue_view,
            "issue_create": self._issue_create,
            "issue_close": self._issue_close,
            "issue_comment": self._issue_comment,
            # Repository Operations
            "repo_view": self._repo_view,
            "repo_clone": self._repo_clone,
            "repo_contributors": self._repo_contributors,
            "repo_languages": self._repo_languages,
            # Branch Operations
            "branch_list": self._branch_list,
            "branch_create": self._branch_create,
            "branch_delete": self._branch_delete,
            "branch_compare": self._branch_compare,
            # Actions/Workflows
            "workflow_list": self._workflow_list,
            "workflow_run": self._workflow_run,
            "run_list": self._run_list,
            "run_view": self._run_view,
            "run_logs": self._run_logs,
            # Analysis
            "analyze_repo": self._analyze_repo,
            "analyze_pr": self._analyze_pr,
            "suggest_reviewers": self._suggest_reviewers,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown github action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    # ── PR Operations ───────────────────────────────────────────────

    async def _pr_list(self, args: dict) -> dict:
        """List pull requests."""
        state = args.get("state", "open")
        limit = args.get("limit", 30)
        base = args.get("base")
        author = args.get("author")

        cmd = ["pr", "list", "--state", state, "--limit", str(limit), "--json",
               "number,title,author,state,createdAt,headRefName,baseRefName,isDraft,labels"]

        if base:
            cmd.extend(["--base", base])
        if author:
            cmd.extend(["--author", author])

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        prs = result.get("data", [])
        return {
            "count": len(prs),
            "state": state,
            "prs": [
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "author": pr["author"]["login"] if pr.get("author") else "unknown",
                    "branch": pr.get("headRefName"),
                    "base": pr.get("baseRefName"),
                    "draft": pr.get("isDraft", False),
                    "labels": [l["name"] for l in pr.get("labels", [])],
                    "created": pr.get("createdAt"),
                }
                for pr in prs
            ],
        }

    async def _pr_view(self, args: dict) -> dict:
        """View PR details."""
        pr_number = args.get("number")
        if not pr_number:
            return {"error": "PR number required"}

        result = await _run_gh([
            "pr", "view", str(pr_number), "--json",
            "number,title,body,author,state,createdAt,mergedAt,closedAt,"
            "headRefName,baseRefName,additions,deletions,changedFiles,"
            "commits,comments,reviews,labels,assignees,milestone"
        ])

        if "error" in result:
            return result

        pr = result.get("data", {})
        return {
            "number": pr.get("number"),
            "title": pr.get("title"),
            "body_preview": (pr.get("body") or "")[:500],
            "author": pr.get("author", {}).get("login"),
            "state": pr.get("state"),
            "branch": pr.get("headRefName"),
            "base": pr.get("baseRefName"),
            "stats": {
                "additions": pr.get("additions"),
                "deletions": pr.get("deletions"),
                "changed_files": pr.get("changedFiles"),
                "commits": len(pr.get("commits", [])),
                "comments": len(pr.get("comments", [])),
                "reviews": len(pr.get("reviews", [])),
            },
            "labels": [l["name"] for l in pr.get("labels", [])],
            "assignees": [a["login"] for a in pr.get("assignees", [])],
            "created": pr.get("createdAt"),
            "merged": pr.get("mergedAt"),
        }

    async def _pr_create(self, args: dict) -> dict:
        """Create a pull request."""
        title = args.get("title")
        body = args.get("body", "")
        base = args.get("base", "main")
        head = args.get("head")
        draft = args.get("draft", False)

        if not title:
            return {"error": "PR title required"}

        cmd = ["pr", "create", "--title", title, "--body", body, "--base", base]
        if head:
            cmd.extend(["--head", head])
        if draft:
            cmd.append("--draft")

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        # Parse PR URL from output
        output = result.get("output", "")
        pr_match = re.search(r'/pull/(\d+)', output)
        pr_number = int(pr_match.group(1)) if pr_match else None

        return {
            "created": True,
            "pr_number": pr_number,
            "url": output.strip(),
            "title": title,
            "base": base,
        }

    async def _pr_merge(self, args: dict) -> dict:
        """Merge a pull request."""
        pr_number = args.get("number")
        method = args.get("method", "squash")  # merge, squash, rebase
        delete_branch = args.get("delete_branch", True)

        if not pr_number:
            return {"error": "PR number required"}

        cmd = ["pr", "merge", str(pr_number), f"--{method}"]
        if delete_branch:
            cmd.append("--delete-branch")

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        return {
            "merged": True,
            "pr_number": pr_number,
            "method": method,
            "branch_deleted": delete_branch,
        }

    async def _pr_diff(self, args: dict) -> dict:
        """Get PR diff summary."""
        pr_number = args.get("number")
        if not pr_number:
            return {"error": "PR number required"}

        result = await _run_gh(["pr", "diff", str(pr_number), "--stat"])
        if "error" in result:
            return result

        return {
            "pr_number": pr_number,
            "diff_stat": result.get("output", ""),
        }

    async def _pr_checks(self, args: dict) -> dict:
        """Get PR check status."""
        pr_number = args.get("number")
        if not pr_number:
            return {"error": "PR number required"}

        result = await _run_gh(["pr", "checks", str(pr_number), "--json", "name,state,conclusion"])
        if "error" in result:
            return result

        checks = result.get("data", [])
        return {
            "pr_number": pr_number,
            "total": len(checks),
            "passed": sum(1 for c in checks if c.get("conclusion") == "success"),
            "failed": sum(1 for c in checks if c.get("conclusion") == "failure"),
            "pending": sum(1 for c in checks if c.get("state") in ("queued", "in_progress")),
            "checks": checks,
        }

    async def _pr_review(self, args: dict) -> dict:
        """Submit a PR review."""
        pr_number = args.get("number")
        action = args.get("action", "comment")  # approve, comment, request-changes
        body = args.get("body", "")

        if not pr_number:
            return {"error": "PR number required"}

        cmd = ["pr", "review", str(pr_number), f"--{action}"]
        if body:
            cmd.extend(["--body", body])

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        return {"reviewed": True, "pr_number": pr_number, "action": action}

    async def _pr_comment(self, args: dict) -> dict:
        """Add a comment to a PR."""
        pr_number = args.get("number")
        body = args.get("body")

        if not pr_number or not body:
            return {"error": "PR number and comment body required"}

        result = await _run_gh(["pr", "comment", str(pr_number), "--body", body])
        if "error" in result:
            return result

        return {"commented": True, "pr_number": pr_number}

    # ── Issue Operations ────────────────────────────────────────────

    async def _issue_list(self, args: dict) -> dict:
        """List issues."""
        state = args.get("state", "open")
        limit = args.get("limit", 30)
        labels = args.get("labels")

        cmd = ["issue", "list", "--state", state, "--limit", str(limit), "--json",
               "number,title,author,state,createdAt,labels,assignees"]

        if labels:
            cmd.extend(["--label", labels])

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        issues = result.get("data", [])
        return {
            "count": len(issues),
            "state": state,
            "issues": [
                {
                    "number": i["number"],
                    "title": i["title"],
                    "author": i["author"]["login"] if i.get("author") else "unknown",
                    "labels": [l["name"] for l in i.get("labels", [])],
                    "assignees": [a["login"] for a in i.get("assignees", [])],
                    "created": i.get("createdAt"),
                }
                for i in issues
            ],
        }

    async def _issue_view(self, args: dict) -> dict:
        """View issue details."""
        issue_number = args.get("number")
        if not issue_number:
            return {"error": "Issue number required"}

        result = await _run_gh([
            "issue", "view", str(issue_number), "--json",
            "number,title,body,author,state,createdAt,closedAt,labels,assignees,comments"
        ])

        if "error" in result:
            return result

        issue = result.get("data", {})
        return {
            "number": issue.get("number"),
            "title": issue.get("title"),
            "body_preview": (issue.get("body") or "")[:500],
            "author": issue.get("author", {}).get("login"),
            "state": issue.get("state"),
            "labels": [l["name"] for l in issue.get("labels", [])],
            "assignees": [a["login"] for a in issue.get("assignees", [])],
            "comments": len(issue.get("comments", [])),
            "created": issue.get("createdAt"),
            "closed": issue.get("closedAt"),
        }

    async def _issue_create(self, args: dict) -> dict:
        """Create an issue."""
        title = args.get("title")
        body = args.get("body", "")
        labels = args.get("labels", [])
        assignees = args.get("assignees", [])

        if not title:
            return {"error": "Issue title required"}

        cmd = ["issue", "create", "--title", title, "--body", body]
        for label in labels:
            cmd.extend(["--label", label])
        for assignee in assignees:
            cmd.extend(["--assignee", assignee])

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        output = result.get("output", "")
        issue_match = re.search(r'/issues/(\d+)', output)
        issue_number = int(issue_match.group(1)) if issue_match else None

        return {
            "created": True,
            "issue_number": issue_number,
            "url": output.strip(),
            "title": title,
        }

    async def _issue_close(self, args: dict) -> dict:
        """Close an issue."""
        issue_number = args.get("number")
        reason = args.get("reason", "completed")  # completed, not_planned

        if not issue_number:
            return {"error": "Issue number required"}

        cmd = ["issue", "close", str(issue_number)]
        if reason == "not_planned":
            cmd.append("--reason=not_planned")

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        return {"closed": True, "issue_number": issue_number, "reason": reason}

    async def _issue_comment(self, args: dict) -> dict:
        """Comment on an issue."""
        issue_number = args.get("number")
        body = args.get("body")

        if not issue_number or not body:
            return {"error": "Issue number and body required"}

        result = await _run_gh(["issue", "comment", str(issue_number), "--body", body])
        if "error" in result:
            return result

        return {"commented": True, "issue_number": issue_number}

    # ── Repository Operations ───────────────────────────────────────

    async def _repo_view(self, args: dict) -> dict:
        """View repository info."""
        repo = args.get("repo")  # owner/repo or None for current

        cmd = ["repo", "view", "--json",
               "name,owner,description,url,sshUrl,createdAt,pushedAt,"
               "stargazerCount,forkCount,isPrivate,defaultBranchRef"]
        if repo:
            cmd.append(repo)

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        data = result.get("data", {})
        return {
            "name": data.get("name"),
            "owner": data.get("owner", {}).get("login"),
            "description": data.get("description"),
            "url": data.get("url"),
            "ssh_url": data.get("sshUrl"),
            "stars": data.get("stargazerCount"),
            "forks": data.get("forkCount"),
            "private": data.get("isPrivate"),
            "default_branch": data.get("defaultBranchRef", {}).get("name"),
            "created": data.get("createdAt"),
            "last_push": data.get("pushedAt"),
        }

    async def _repo_clone(self, args: dict) -> dict:
        """Clone a repository."""
        repo = args.get("repo")
        directory = args.get("directory")

        if not repo:
            return {"error": "Repository required (owner/repo)"}

        cmd = ["repo", "clone", repo]
        if directory:
            cmd.append(directory)

        result = await _run_gh(cmd, cwd=str(NOIZYLAB_ROOT.parent))
        if "error" in result:
            return result

        return {"cloned": True, "repo": repo}

    async def _repo_contributors(self, args: dict) -> dict:
        """Get repository contributors."""
        result = await _run_gh([
            "api", "repos/{owner}/{repo}/contributors",
            "--jq", ".[].login"
        ])
        if "error" in result:
            return result

        contributors = result.get("output", "").strip().split("\n")
        return {"contributors": [c for c in contributors if c], "count": len(contributors)}

    async def _repo_languages(self, args: dict) -> dict:
        """Get repository languages."""
        result = await _run_gh(["api", "repos/{owner}/{repo}/languages"])
        if "error" in result:
            return result

        return {"languages": result.get("data", {})}

    # ── Branch Operations ───────────────────────────────────────────

    async def _branch_list(self, args: dict) -> dict:
        """List branches."""
        result = await _run_gh([
            "api", "repos/{owner}/{repo}/branches",
            "--jq", ".[].name"
        ])
        if "error" in result:
            return result

        branches = result.get("output", "").strip().split("\n")
        return {"branches": [b for b in branches if b], "count": len(branches)}

    async def _branch_create(self, args: dict) -> dict:
        """Create a new branch."""
        name = args.get("name")
        base = args.get("base", "main")

        if not name:
            return {"error": "Branch name required"}

        # Get base SHA
        sha_result = await _run_gh([
            "api", f"repos/{{owner}}/{{repo}}/git/refs/heads/{base}",
            "--jq", ".object.sha"
        ])
        if "error" in sha_result:
            return sha_result

        sha = sha_result.get("output", "").strip()

        # Create branch
        result = await _run_gh([
            "api", "repos/{owner}/{repo}/git/refs",
            "-X", "POST",
            "-f", f"ref=refs/heads/{name}",
            "-f", f"sha={sha}",
        ])

        if "error" in result:
            return result

        return {"created": True, "branch": name, "base": base}

    async def _branch_delete(self, args: dict) -> dict:
        """Delete a branch."""
        name = args.get("name")
        if not name:
            return {"error": "Branch name required"}

        result = await _run_gh([
            "api", f"repos/{{owner}}/{{repo}}/git/refs/heads/{name}",
            "-X", "DELETE"
        ])

        if "error" in result:
            return result

        return {"deleted": True, "branch": name}

    async def _branch_compare(self, args: dict) -> dict:
        """Compare two branches."""
        base = args.get("base", "main")
        head = args.get("head")

        if not head:
            return {"error": "Head branch required"}

        result = await _run_gh([
            "api", f"repos/{{owner}}/{{repo}}/compare/{base}...{head}",
            "--jq", "{ahead_by, behind_by, total_commits: .commits | length, status}"
        ])

        if "error" in result:
            return result

        return {"base": base, "head": head, **result.get("data", {})}

    # ── Actions/Workflows ───────────────────────────────────────────

    async def _workflow_list(self, args: dict) -> dict:
        """List workflows."""
        result = await _run_gh(["workflow", "list", "--json", "name,id,state"])
        if "error" in result:
            return result

        return {"workflows": result.get("data", [])}

    async def _workflow_run(self, args: dict) -> dict:
        """Trigger a workflow run."""
        workflow = args.get("workflow")
        ref = args.get("ref", "main")

        if not workflow:
            return {"error": "Workflow name or ID required"}

        result = await _run_gh(["workflow", "run", workflow, "--ref", ref])
        if "error" in result:
            return result

        return {"triggered": True, "workflow": workflow, "ref": ref}

    async def _run_list(self, args: dict) -> dict:
        """List workflow runs."""
        limit = args.get("limit", 10)
        workflow = args.get("workflow")

        cmd = ["run", "list", "--limit", str(limit), "--json",
               "databaseId,displayTitle,status,conclusion,createdAt,headBranch"]
        if workflow:
            cmd.extend(["--workflow", workflow])

        result = await _run_gh(cmd)
        if "error" in result:
            return result

        runs = result.get("data", [])
        return {
            "count": len(runs),
            "runs": [
                {
                    "id": r["databaseId"],
                    "title": r.get("displayTitle"),
                    "status": r.get("status"),
                    "conclusion": r.get("conclusion"),
                    "branch": r.get("headBranch"),
                    "created": r.get("createdAt"),
                }
                for r in runs
            ],
        }

    async def _run_view(self, args: dict) -> dict:
        """View a workflow run."""
        run_id = args.get("id")
        if not run_id:
            return {"error": "Run ID required"}

        result = await _run_gh([
            "run", "view", str(run_id), "--json",
            "databaseId,displayTitle,status,conclusion,createdAt,updatedAt,jobs"
        ])

        if "error" in result:
            return result

        return result.get("data", {})

    async def _run_logs(self, args: dict) -> dict:
        """Get workflow run logs (summary)."""
        run_id = args.get("id")
        if not run_id:
            return {"error": "Run ID required"}

        result = await _run_gh(["run", "view", str(run_id), "--log"])
        if "error" in result:
            return result

        # Return truncated logs
        output = result.get("output", "")
        lines = output.split("\n")
        return {
            "run_id": run_id,
            "total_lines": len(lines),
            "tail": "\n".join(lines[-100:]),  # Last 100 lines
        }

    # ── Analysis ────────────────────────────────────────────────────

    async def _analyze_repo(self, args: dict) -> dict:
        """Comprehensive repository analysis."""
        repo_info = await self._repo_view(args)
        prs = await self._pr_list({"limit": 10})
        issues = await self._issue_list({"limit": 10})
        runs = await self._run_list({"limit": 5})
        languages = await self._repo_languages(args)

        return {
            "repository": repo_info,
            "open_prs": prs.get("count", 0),
            "recent_prs": prs.get("prs", [])[:5],
            "open_issues": issues.get("count", 0),
            "recent_issues": issues.get("issues", [])[:5],
            "recent_runs": runs.get("runs", []),
            "languages": languages.get("languages", {}),
        }

    async def _analyze_pr(self, args: dict) -> dict:
        """Deep PR analysis for code review."""
        pr_number = args.get("number")
        if not pr_number:
            return {"error": "PR number required"}

        pr_details = await self._pr_view({"number": pr_number})
        pr_checks = await self._pr_checks({"number": pr_number})
        pr_diff = await self._pr_diff({"number": pr_number})

        return {
            "pr": pr_details,
            "checks": pr_checks,
            "diff_summary": pr_diff.get("diff_stat"),
            "review_readiness": {
                "all_checks_pass": pr_checks.get("failed", 0) == 0,
                "has_assignees": len(pr_details.get("assignees", [])) > 0,
                "has_labels": len(pr_details.get("labels", [])) > 0,
                "changes_scope": "large" if pr_details.get("stats", {}).get("changed_files", 0) > 10 else "manageable",
            },
        }

    async def _suggest_reviewers(self, args: dict) -> dict:
        """Suggest reviewers based on file ownership."""
        contributors = await self._repo_contributors(args)
        return {
            "suggested_reviewers": contributors.get("contributors", [])[:5],
            "note": "Based on repository contributors. For accurate suggestions, consider CODEOWNERS.",
        }

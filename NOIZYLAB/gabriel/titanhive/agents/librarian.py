"""
LIBRARIAN AGENT
===============
Organizes, indexes, and searches files across the GABRIEL vault.
"""

import asyncio
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class FileInfo:
    """File information."""
    path: Path
    name: str
    extension: str
    size_mb: float
    modified: datetime
    file_type: str  # code, document, media, archive, other


class LibrarianAgent:
    """
    Librarian Agent - File Organization & Search

    Responsibilities:
    - Index files across volumes
    - Search by name, content, or type
    - Organize files by project/date
    - Track large files and duplicates
    - Generate file statistics
    """

    # File type mappings
    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.swift', '.sh', '.zsh', '.bash'}
    DOC_EXTENSIONS = {'.md', '.txt', '.pdf', '.doc', '.docx', '.rtf', '.json', '.yaml', '.yml', '.toml', '.xml', '.html', '.css'}
    MEDIA_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.mp3', '.wav', '.m4a', '.heic', '.webp', '.svg'}
    ARCHIVE_EXTENSIONS = {'.zip', '.tar', '.gz', '.7z', '.rar', '.dmg', '.iso'}

    def __init__(self, root_paths: Optional[list[Path]] = None):
        """
        Initialize Librarian.

        Args:
            root_paths: Paths to index (defaults to GABRIEL root)
        """
        self.root_paths = root_paths or [
            Path.home() / "NOIZYLAB" / "GABRIEL",
            Path.home() / "Documents",
        ]
        self._index: dict[str, FileInfo] = {}
        self._last_indexed: Optional[datetime] = None

    def _get_file_type(self, ext: str) -> str:
        """Determine file type from extension."""
        ext_lower = ext.lower()
        if ext_lower in self.CODE_EXTENSIONS:
            return "code"
        elif ext_lower in self.DOC_EXTENSIONS:
            return "document"
        elif ext_lower in self.MEDIA_EXTENSIONS:
            return "media"
        elif ext_lower in self.ARCHIVE_EXTENSIONS:
            return "archive"
        return "other"

    def index_path(self, path: Path, max_depth: int = 10) -> int:
        """
        Index all files under a path.

        Returns:
            Number of files indexed
        """
        count = 0
        try:
            for root, dirs, files in os.walk(path):
                # Skip hidden and common exclude dirs
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
                    'node_modules', '__pycache__', '.git', 'venv', '.venv', 'build', 'dist'
                }]

                depth = str(root).count(os.sep) - str(path).count(os.sep)
                if depth > max_depth:
                    continue

                for name in files:
                    if name.startswith('.'):
                        continue
                    try:
                        file_path = Path(root) / name
                        stat = file_path.stat()
                        ext = file_path.suffix

                        info = FileInfo(
                            path=file_path,
                            name=name,
                            extension=ext,
                            size_mb=stat.st_size / (1024 * 1024),
                            modified=datetime.fromtimestamp(stat.st_mtime),
                            file_type=self._get_file_type(ext),
                        )
                        self._index[str(file_path)] = info
                        count += 1
                    except (PermissionError, FileNotFoundError):
                        continue
        except Exception:
            pass

        return count

    def index_all(self) -> int:
        """Index all root paths."""
        total = 0
        for path in self.root_paths:
            if path.exists():
                total += self.index_path(path)
        self._last_indexed = datetime.now()
        return total

    def search(self, query: str, file_type: Optional[str] = None, limit: int = 20) -> list[FileInfo]:
        """
        Search indexed files.

        Args:
            query: Search query (matches name or path)
            file_type: Filter by type (code, document, media, archive, other)
            limit: Maximum results

        Returns:
            Matching FileInfo objects
        """
        query_lower = query.lower()
        results = []

        for path, info in self._index.items():
            if file_type and info.file_type != file_type:
                continue

            if query_lower in info.name.lower() or query_lower in str(info.path).lower():
                results.append(info)

            if len(results) >= limit:
                break

        # Sort by modification date (newest first)
        results.sort(key=lambda x: x.modified, reverse=True)
        return results[:limit]

    def search_content(self, pattern: str, file_types: Optional[list[str]] = None, limit: int = 20) -> list[tuple[FileInfo, str]]:
        """
        Search file contents using ripgrep.

        Args:
            pattern: Regex pattern to search
            file_types: File types to search (defaults to code + document)
            limit: Maximum results

        Returns:
            List of (FileInfo, matched_line) tuples
        """
        if file_types is None:
            file_types = ["code", "document"]

        results = []

        for path in self.root_paths:
            if not path.exists():
                continue

            try:
                cmd = ["rg", "-l", "-m", str(limit), pattern, str(path)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue
                    file_path = Path(line)
                    if str(file_path) in self._index:
                        info = self._index[str(file_path)]
                        if info.file_type in file_types:
                            results.append((info, line))

                    if len(results) >= limit:
                        break
            except Exception:
                continue

        return results[:limit]

    def get_large_files(self, min_size_mb: float = 100, limit: int = 20) -> list[FileInfo]:
        """Get files larger than threshold."""
        large = [info for info in self._index.values() if info.size_mb >= min_size_mb]
        large.sort(key=lambda x: x.size_mb, reverse=True)
        return large[:limit]

    def get_recent_files(self, days: int = 7, limit: int = 20) -> list[FileInfo]:
        """Get recently modified files."""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        recent = [info for info in self._index.values()
                  if info.modified.timestamp() > cutoff]
        recent.sort(key=lambda x: x.modified, reverse=True)
        return recent[:limit]

    def get_stats(self) -> dict:
        """Get file statistics."""
        stats = {
            "total_files": len(self._index),
            "total_size_gb": sum(f.size_mb for f in self._index.values()) / 1024,
            "by_type": {},
            "last_indexed": self._last_indexed.isoformat() if self._last_indexed else None,
        }

        for info in self._index.values():
            if info.file_type not in stats["by_type"]:
                stats["by_type"][info.file_type] = {"count": 0, "size_mb": 0}
            stats["by_type"][info.file_type]["count"] += 1
            stats["by_type"][info.file_type]["size_mb"] += info.size_mb

        return stats

    def format_stats(self) -> str:
        """Format statistics as string."""
        stats = self.get_stats()
        lines = [
            "═══ LIBRARIAN STATS ═══",
            f"Total Files: {stats['total_files']:,}",
            f"Total Size: {stats['total_size_gb']:.1f} GB",
            "─── By Type ───",
        ]

        for file_type, data in stats["by_type"].items():
            lines.append(f"  {file_type}: {data['count']:,} ({data['size_mb']/1024:.1f} GB)")

        if stats['last_indexed']:
            lines.append(f"Last Indexed: {stats['last_indexed']}")

        return "\n".join(lines)

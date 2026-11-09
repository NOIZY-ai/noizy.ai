#!/usr/bin/env python3
"""
NOIZY.ai Enterprise Migration Script
=====================================
Migrates code from NOIZYLAB and M2 Ultra to the enterprise monorepo.

Usage:
    python migrate-to-enterprise.py --source ~/NOIZYLAB --target ~/noizy-enterprise
    python migrate-to-enterprise.py --dry-run  # Preview changes
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


# Migration mappings: source -> destination
MIGRATIONS = {
    # Gabriel MCP v2
    "gabriel/mcp_servers/gabriel_mcp/orchestrator": "projects/gabriel/mcp-server/orchestrator",
    "gabriel/mcp_servers/gabriel_mcp/tools": "projects/gabriel/mcp-server/tools",
    "gabriel/mcp_servers/gabriel_mcp/pipeline": "projects/gabriel/mcp-server/pipeline",
    "gabriel/mcp_servers/gabriel_mcp/state": "projects/gabriel/mcp-server/state",
    "gabriel/mcp_servers/gabriel_mcp/server.py": "projects/gabriel/mcp-server/server.py",
    "gabriel/mcp_servers/gabriel_mcp/config.py": "projects/gabriel/mcp-server/config.py",
    "gabriel/mcp_servers/gabriel_mcp/__main__.py": "projects/gabriel/mcp-server/__main__.py",
    "gabriel/mcp_servers/gabriel_mcp/start.sh": "projects/gabriel/mcp-server/start.sh",
    "gabriel/mcp_servers/gabriel_mcp/tests": "projects/gabriel/mcp-server/tests",

    # Characters
    "gabriel/characters": "projects/gabriel/characters",

    # Brain/Knowledge
    "gabriel/memcell_data": "projects/gabriel/memcell",

    # Architecture docs
    "SUPERSONIC_2.1_ARCHITECTURE.md": "projects/supersonic/docs/SUPERSONIC_2.1_ARCHITECTURE.md",
    "enterprise/ENTERPRISE_ARCHITECTURE.md": "docs/architecture/ENTERPRISE_ARCHITECTURE.md",
}

# Archive mappings: source -> archive destination
ARCHIVES = {
    "gabriel/mcp_servers/gabriel_mcp/server_v1.py": "archive/noizylab_legacy/gabriel_v1/server.py",
}


class Migrator:
    def __init__(self, source: Path, target: Path, dry_run: bool = False):
        self.source = source
        self.target = target
        self.dry_run = dry_run
        self.log = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run(self):
        """Execute the migration."""
        print(f"\n{'=' * 60}")
        print("NOIZY.ai Enterprise Migration")
        print(f"{'=' * 60}")
        print(f"Source: {self.source}")
        print(f"Target: {self.target}")
        print(f"Mode:   {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"{'=' * 60}\n")

        # Verify source exists
        if not self.source.exists():
            print(f"ERROR: Source directory not found: {self.source}")
            return False

        # Verify target exists
        if not self.target.exists():
            print(f"ERROR: Target directory not found: {self.target}")
            print("Run init-enterprise-repo.sh first to create the structure.")
            return False

        # Run migrations
        print("Migrating active code...")
        for src_rel, dst_rel in MIGRATIONS.items():
            self._migrate(src_rel, dst_rel)

        print("\nArchiving legacy code...")
        for src_rel, dst_rel in ARCHIVES.items():
            self._archive(src_rel, dst_rel)

        # Update migration log
        self._update_migration_log()

        print(f"\n{'=' * 60}")
        print(f"Migration {'preview' if self.dry_run else 'complete'}!")
        print(f"{'=' * 60}")

        return True

    def _migrate(self, src_rel: str, dst_rel: str):
        """Migrate a file or directory."""
        src_path = self.source / src_rel
        dst_path = self.target / dst_rel

        if not src_path.exists():
            print(f"  SKIP (not found): {src_rel}")
            return

        action = "COPY" if src_path.is_file() else "COPY DIR"

        if self.dry_run:
            print(f"  [DRY RUN] {action}: {src_rel} -> {dst_rel}")
        else:
            print(f"  {action}: {src_rel} -> {dst_rel}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
            else:
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)

        self.log.append({
            "timestamp": self.timestamp,
            "action": "migrate",
            "source": src_rel,
            "destination": dst_rel,
        })

    def _archive(self, src_rel: str, dst_rel: str):
        """Archive a file or directory."""
        src_path = self.source / src_rel
        dst_path = self.target / dst_rel

        if not src_path.exists():
            print(f"  SKIP (not found): {src_rel}")
            return

        if self.dry_run:
            print(f"  [DRY RUN] ARCHIVE: {src_rel} -> {dst_rel}")
        else:
            print(f"  ARCHIVE: {src_rel} -> {dst_rel}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
            else:
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)

            # Create archive metadata
            meta_path = dst_path.parent / "ARCHIVED_DATE.txt"
            meta_path.write_text(f"Archived: {self.timestamp}\nSource: {src_rel}\n")

        self.log.append({
            "timestamp": self.timestamp,
            "action": "archive",
            "source": src_rel,
            "destination": dst_rel,
        })

    def _update_migration_log(self):
        """Update the migration log in the target repo."""
        if self.dry_run:
            return

        log_path = self.target / "archive" / "MIGRATION_LOG.md"
        if not log_path.exists():
            return

        entries = []
        for entry in self.log:
            action = entry["action"].upper()
            entries.append(f"- [{action}] {entry['source']} → {entry['destination']}")

        if entries:
            content = log_path.read_text()
            new_section = f"\n### {self.timestamp}: Migration from NOIZYLAB\n"
            new_section += "\n".join(entries) + "\n"
            content += new_section
            log_path.write_text(content)


def main():
    parser = argparse.ArgumentParser(description="Migrate NOIZYLAB to enterprise repo")
    parser.add_argument("--source", type=Path, default=Path.home() / "NOIZYLAB",
                        help="Source directory (default: ~/NOIZYLAB)")
    parser.add_argument("--target", type=Path, default=Path.home() / "noizy-enterprise",
                        help="Target directory (default: ~/noizy-enterprise)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without executing")

    args = parser.parse_args()

    migrator = Migrator(args.source, args.target, args.dry_run)
    success = migrator.run()

    if not success:
        exit(1)


if __name__ == "__main__":
    main()

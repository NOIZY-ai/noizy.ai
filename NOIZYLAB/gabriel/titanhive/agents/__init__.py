"""
GABRIEL HIVE AGENTS
===================
Autonomous AI agents for the TitanHive system.

Agents:
- Librarian: Organizes and indexes files on the Mac Pro Vault
- SysAdmin: Monitors health, updates, and manages backups
- Researcher: Browses web and docs to solve problems
- Guardian: Monitors thermals and memory, auto-optimizes
"""

from .guardian import GuardianAgent
from .librarian import LibrarianAgent
from .sysadmin import SysAdminAgent

__all__ = ["GuardianAgent", "LibrarianAgent", "SysAdminAgent"]

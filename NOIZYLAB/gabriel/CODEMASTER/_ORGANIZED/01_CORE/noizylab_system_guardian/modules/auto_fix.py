#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔧 SYSTEM DOCTOR AUTO-FIX MODULE                                           ║
║  Part of GABRIEL SYSTEM OMEGA - MC96DIGIUNIVERSE                            ║
║  GORUNFREE x1000                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Automated repair and optimization commands for common system issues.
"""

import subprocess
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum

# Try to import Rich
try:
    from rich.console import Console
    from rich.prompt import Confirm
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class FixCategory(Enum):
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    PROCESS = "process"
    SYSTEM = "system"


@dataclass
class AutoFix:
    """An auto-fix action."""
    name: str
    description: str
    command: list[str]
    category: FixCategory
    requires_sudo: bool = False
    dangerous: bool = False
    
    def execute(self, dry_run: bool = False) -> tuple[bool, str]:
        """Execute the fix. Returns (success, output)."""
        if dry_run:
            cmd_str = " ".join(self.command)
            if self.requires_sudo:
                cmd_str = f"sudo {cmd_str}"
            return True, f"[DRY RUN] Would execute: {cmd_str}"
        
        try:
            cmd = self.command
            if self.requires_sudo:
                cmd = ["sudo"] + cmd
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, result.stdout or "Command completed successfully"
            else:
                return False, result.stderr or f"Command failed with code {result.returncode}"
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)


class SystemRepair:
    """Collection of auto-fix actions."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.fixes = self._build_fixes()
    
    def _build_fixes(self) -> dict[str, AutoFix]:
        """Build the collection of available fixes."""
        return {
            # Memory fixes
            "purge_memory": AutoFix(
                name="Purge Inactive Memory",
                description="Free up inactive memory by purging the disk cache",
                command=["purge"],
                category=FixCategory.MEMORY,
                requires_sudo=True
            ),
            
            # Disk fixes
            "flush_dns": AutoFix(
                name="Flush DNS Cache",
                description="Clear the DNS cache to fix name resolution issues",
                command=["dscacheutil", "-flushcache"],
                category=FixCategory.NETWORK,
                requires_sudo=True
            ),
            "restart_mdns": AutoFix(
                name="Restart mDNS Responder",
                description="Restart the DNS responder service",
                command=["killall", "-HUP", "mDNSResponder"],
                category=FixCategory.NETWORK,
                requires_sudo=True
            ),
            "clear_logs": AutoFix(
                name="Clear System Logs",
                description="Remove old system log files to free disk space",
                command=["rm", "-rf", "/var/log/*.log.*"],
                category=FixCategory.DISK,
                requires_sudo=True,
                dangerous=True
            ),
            "empty_trash": AutoFix(
                name="Empty All Trash",
                description="Permanently delete all items in Trash",
                command=["rm", "-rf", str(Path.home() / ".Trash" / "*")],
                category=FixCategory.DISK,
                dangerous=True
            ),
            "clear_caches": AutoFix(
                name="Clear User Caches",
                description="Remove user application caches",
                command=["rm", "-rf", str(Path.home() / "Library" / "Caches" / "*")],
                category=FixCategory.DISK,
                dangerous=True
            ),
            
            # Process fixes
            "kill_zombies": AutoFix(
                name="Reap Zombie Processes",
                description="Attempt to clean up zombie processes",
                command=["pkill", "-9", "-z"],
                category=FixCategory.PROCESS,
                requires_sudo=True
            ),
            
            # System optimization
            "disable_animations": AutoFix(
                name="Disable macOS Animations",
                description="Speed up UI by disabling animations",
                command=["defaults", "write", "NSGlobalDomain", "NSAutomaticWindowAnimationsEnabled", "-bool", "false"],
                category=FixCategory.SYSTEM
            ),
            "speed_dock": AutoFix(
                name="Speed Up Dock",
                description="Make Dock appear instantly",
                command=["defaults", "write", "com.apple.dock", "autohide-delay", "-float", "0"],
                category=FixCategory.SYSTEM
            ),
            "restart_dock": AutoFix(
                name="Restart Dock",
                description="Restart the Dock to apply changes",
                command=["killall", "Dock"],
                category=FixCategory.SYSTEM
            ),
            "restart_finder": AutoFix(
                name="Restart Finder",
                description="Restart Finder to fix display issues",
                command=["killall", "Finder"],
                category=FixCategory.SYSTEM
            ),
            "verify_disk": AutoFix(
                name="Verify System Disk",
                description="Run disk verification on the boot volume",
                command=["diskutil", "verifyVolume", "/"],
                category=FixCategory.DISK,
                requires_sudo=True
            ),
            "repair_permissions": AutoFix(
                name="Reset Home Folder Permissions",
                description="Fix common permission issues in home folder",
                command=["chown", "-R", os.environ.get("USER", "m2ultra"), str(Path.home())],
                category=FixCategory.DISK,
                requires_sudo=True
            ),
        }
    
    def list_fixes(self, category: Optional[FixCategory] = None) -> list[AutoFix]:
        """List available fixes, optionally filtered by category."""
        if category:
            return [f for f in self.fixes.values() if f.category == category]
        return list(self.fixes.values())
    
    def run_fix(self, fix_name: str, confirm: bool = True, dry_run: bool = False) -> tuple[bool, str]:
        """Run a specific fix by name."""
        if fix_name not in self.fixes:
            return False, f"Unknown fix: {fix_name}"
        
        fix = self.fixes[fix_name]
        
        if confirm and RICH_AVAILABLE and not dry_run:
            self.console.print(f"\n[bold]{fix.name}[/bold]")
            self.console.print(f"[dim]{fix.description}[/dim]")
            
            if fix.dangerous:
                self.console.print("[bold red]⚠️  This action is potentially dangerous![/bold red]")
            
            if fix.requires_sudo:
                self.console.print("[yellow]Requires sudo privileges[/yellow]")
            
            if not Confirm.ask("Proceed?"):
                return False, "Cancelled by user"
        
        return fix.execute(dry_run)
    
    def run_quick_optimize(self, dry_run: bool = False) -> list[tuple[str, bool, str]]:
        """Run a set of safe, quick optimizations."""
        quick_fixes = [
            "purge_memory",
            "flush_dns",
            "restart_mdns",
            "disable_animations",
            "speed_dock",
            "restart_dock",
        ]
        
        results = []
        for fix_name in quick_fixes:
            success, output = self.run_fix(fix_name, confirm=False, dry_run=dry_run)
            results.append((fix_name, success, output))
        
        return results
    
    def print_available_fixes(self):
        """Print all available fixes."""
        if RICH_AVAILABLE:
            from rich.table import Table
            from rich import box
            
            table = Table(
                title="🔧 Available Auto-Fix Actions",
                box=box.ROUNDED,
                title_style="bold cyan"
            )
            table.add_column("Name", style="cyan")
            table.add_column("Category", style="magenta")
            table.add_column("Description")
            table.add_column("Sudo", justify="center")
            table.add_column("⚠️", justify="center")
            
            for name, fix in self.fixes.items():
                sudo = "✓" if fix.requires_sudo else ""
                danger = "⚠️" if fix.dangerous else ""
                table.add_row(name, fix.category.value, fix.description, sudo, danger)
            
            self.console.print(table)
        else:
            print("\n🔧 Available Auto-Fix Actions:")
            print("-" * 60)
            for name, fix in self.fixes.items():
                sudo = "[sudo]" if fix.requires_sudo else ""
                danger = "[DANGEROUS]" if fix.dangerous else ""
                print(f"  {name}: {fix.description} {sudo} {danger}")


# Quick functions for common operations
def quick_memory_purge():
    """Quick purge of inactive memory."""
    repair = SystemRepair()
    return repair.run_fix("purge_memory", confirm=False)


def quick_dns_flush():
    """Quick flush of DNS cache."""
    repair = SystemRepair()
    repair.run_fix("flush_dns", confirm=False)
    return repair.run_fix("restart_mdns", confirm=False)


def quick_optimize():
    """Run all safe quick optimizations."""
    repair = SystemRepair()
    return repair.run_quick_optimize()


if __name__ == "__main__":
    repair = SystemRepair()
    repair.print_available_fixes()

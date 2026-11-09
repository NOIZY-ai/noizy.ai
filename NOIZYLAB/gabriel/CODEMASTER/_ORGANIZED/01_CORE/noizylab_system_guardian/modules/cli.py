#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🩺 SYSTEM DOCTOR CLI v1.1.0                                                 ║
║  Command-line interface for the TechTool Killer diagnostic scanner          ║
║  + Auto-Fix capabilities                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python -m modules.cli                  # Run full scan
    python -m modules.cli --disk           # Disk scan only
    python -m modules.cli --full --export  # Full scan with JSON export
    python -m modules.cli --fix            # Show available fixes
    python -m modules.cli --optimize       # Run quick optimizations
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.system_doctor import SystemDoctor, RICH_AVAILABLE, HealthStatus
from modules.auto_fix import SystemRepair

if RICH_AVAILABLE:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
else:
    console = None


def print_banner():
    """Print the System Doctor banner."""
    if RICH_AVAILABLE:
        console.print()
        console.print(Panel.fit(
            "[bold cyan]🩺 SYSTEM DOCTOR[/bold cyan] [white]v1.1.0[/white]\n"
            "[dim]TechTool Killer - GABRIEL SYSTEM OMEGA[/dim]\n"
            "[magenta]MC96DIGIUNIVERSE // GORUNFREE x1000[/magenta]",
            border_style="cyan"
        ))
        console.print()
    else:
        print("\n" + "=" * 50)
        print("  🩺 SYSTEM DOCTOR v1.1.0")
        print("  TechTool Killer - GABRIEL SYSTEM OMEGA")
        print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🩺 System Doctor - Mac Diagnostic Scanner + Auto-Fix",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m modules.cli --full              Run all diagnostic modules
  python -m modules.cli --disk --memory     Run disk and memory scans
  python -m modules.cli --full --export     Run full scan and export JSON
  python -m modules.cli --fix               List available auto-fix actions
  python -m modules.cli --optimize          Run quick system optimizations
  python -m modules.cli --run-fix purge_memory   Run a specific fix
        """
    )
    
    # Scan type options
    scan_group = parser.add_argument_group("Scan Options")
    scan_group.add_argument("--full", "-f", action="store_true", 
                            help="Run all diagnostic modules")
    scan_group.add_argument("--disk", "-d", action="store_true",
                            help="Scan disk health and space usage")
    scan_group.add_argument("--smart", "-s", action="store_true",
                            help="Scan SMART data (requires smartmontools)")
    scan_group.add_argument("--memory", "-m", action="store_true",
                            help="Scan memory usage and pressure")
    scan_group.add_argument("--thermal", "-t", action="store_true",
                            help="Scan CPU temperature and thermal status")
    scan_group.add_argument("--network", "-n", action="store_true",
                            help="Scan network interfaces and connectivity")
    scan_group.add_argument("--process", "-p", action="store_true",
                            help="Scan for resource-hogging processes")
    
    # Auto-fix options
    fix_group = parser.add_argument_group("Auto-Fix Options")
    fix_group.add_argument("--fix", action="store_true",
                           help="List all available auto-fix actions")
    fix_group.add_argument("--optimize", "-o", action="store_true",
                           help="Run quick system optimizations (safe)")
    fix_group.add_argument("--run-fix", metavar="NAME",
                           help="Run a specific fix by name")
    fix_group.add_argument("--dry-run", action="store_true",
                           help="Show what would be done without executing")
    fix_group.add_argument("--no-confirm", action="store_true",
                           help="Don't ask for confirmation before fixes")
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--export", "-e", action="store_true",
                              help="Export results to JSON file")
    output_group.add_argument("--quiet", "-q", action="store_true",
                              help="Minimal output (just status)")
    output_group.add_argument("--verbose", "-v", action="store_true",
                              help="Verbose output")
    
    args = parser.parse_args()
    
    # Print banner
    if not args.quiet:
        print_banner()
    
    # Handle fix-related commands
    if args.fix:
        repair = SystemRepair()
        repair.print_available_fixes()
        return 0
    
    if args.optimize:
        repair = SystemRepair()
        if RICH_AVAILABLE:
            console.print("[bold cyan]🔧 Running Quick Optimizations...[/bold cyan]\n")
        else:
            print("🔧 Running Quick Optimizations...\n")
        
        results = repair.run_quick_optimize(dry_run=args.dry_run)
        
        for name, success, output in results:
            icon = "✅" if success else "❌"
            if RICH_AVAILABLE:
                style = "green" if success else "red"
                console.print(f"  {icon} [{style}]{name}[/{style}]: {output[:60]}")
            else:
                print(f"  {icon} {name}: {output[:60]}")
        
        if RICH_AVAILABLE:
            console.print("\n[bold green]🚀 Quick optimization complete![/bold green]")
        else:
            print("\n🚀 Quick optimization complete!")
        return 0
    
    if args.run_fix:
        repair = SystemRepair()
        success, output = repair.run_fix(
            args.run_fix, 
            confirm=not args.no_confirm, 
            dry_run=args.dry_run
        )
        
        if RICH_AVAILABLE:
            if success:
                console.print(f"[green]✅ {args.run_fix}: {output}[/green]")
            else:
                console.print(f"[red]❌ {args.run_fix}: {output}[/red]")
        else:
            icon = "✅" if success else "❌"
            print(f"{icon} {args.run_fix}: {output}")
        
        return 0 if success else 1
    
    # If no scan type specified, default to full scan
    if not any([args.full, args.disk, args.smart, args.memory, 
                args.thermal, args.network, args.process]):
        args.full = True
    
    # Initialize doctor
    doctor = SystemDoctor(verbose=args.verbose)
    
    # Run requested scans
    if args.full:
        doctor.run_full_scan()
    else:
        if args.disk:
            doctor.scan_disks()
        if args.smart:
            doctor.scan_smart()
        if args.memory:
            doctor.scan_memory()
        if args.thermal:
            doctor.scan_thermal()
        if args.network:
            doctor.scan_network()
        if args.process:
            doctor.scan_processes()
    
    # Print results
    if not args.quiet:
        doctor.print_results()
    
    # Export if requested
    if args.export:
        filepath = doctor.export_json()
        if RICH_AVAILABLE:
            console.print(f"[green]📊 Report saved to:[/green] {filepath}")
        else:
            print(f"📊 Report saved to: {filepath}")
    
    # Return exit code based on status
    overall = doctor._get_overall_status()
    
    if overall == HealthStatus.CRITICAL:
        return 2
    elif overall == HealthStatus.WARNING:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

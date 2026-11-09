#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🩺 SYSTEM DOCTOR CLI                                                        ║
║  Command-line interface for the TechTool Killer diagnostic scanner          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python -m modules.cli                # Run full scan
    python -m modules.cli --disk         # Disk scan only
    python -m modules.cli --smart        # SMART scan only
    python -m modules.cli --memory       # Memory scan only
    python -m modules.cli --thermal      # Thermal scan only
    python -m modules.cli --network      # Network scan only
    python -m modules.cli --process      # Process scan only
    python -m modules.cli --full         # Full scan (all modules)
    python -m modules.cli --full --export   # Full scan with JSON export
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.system_doctor import SystemDoctor, RICH_AVAILABLE

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
            "[bold cyan]🩺 SYSTEM DOCTOR[/bold cyan] [white]v1.0.0[/white]\n"
            "[dim]TechTool Killer - GABRIEL SYSTEM OMEGA[/dim]\n"
            "[magenta]MC96DIGIUNIVERSE // GORUNFREE x1000[/magenta]",
            border_style="cyan"
        ))
        console.print()
    else:
        print("\n" + "=" * 50)
        print("  🩺 SYSTEM DOCTOR v1.0.0")
        print("  TechTool Killer - GABRIEL SYSTEM OMEGA")
        print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🩺 System Doctor - Mac Diagnostic Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m modules.cli --full              Run all diagnostic modules
  python -m modules.cli --disk --memory     Run disk and memory scans
  python -m modules.cli --full --export     Run full scan and export JSON
        """
    )
    
    # Scan type options
    parser.add_argument("--full", "-f", action="store_true", 
                        help="Run all diagnostic modules")
    parser.add_argument("--disk", "-d", action="store_true",
                        help="Scan disk health and space usage")
    parser.add_argument("--smart", "-s", action="store_true",
                        help="Scan SMART data (requires smartmontools)")
    parser.add_argument("--memory", "-m", action="store_true",
                        help="Scan memory usage and pressure")
    parser.add_argument("--thermal", "-t", action="store_true",
                        help="Scan CPU temperature and thermal status")
    parser.add_argument("--network", "-n", action="store_true",
                        help="Scan network interfaces and connectivity")
    parser.add_argument("--process", "-p", action="store_true",
                        help="Scan for resource-hogging processes")
    
    # Output options
    parser.add_argument("--export", "-e", action="store_true",
                        help="Export results to JSON file")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Minimal output (just status)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    # If no scan type specified, default to full scan
    if not any([args.full, args.disk, args.smart, args.memory, 
                args.thermal, args.network, args.process]):
        args.full = True
    
    # Print banner
    if not args.quiet:
        print_banner()
    
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
    from modules.system_doctor import HealthStatus
    overall = doctor._get_overall_status()
    
    if overall == HealthStatus.CRITICAL:
        return 2
    elif overall == HealthStatus.WARNING:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

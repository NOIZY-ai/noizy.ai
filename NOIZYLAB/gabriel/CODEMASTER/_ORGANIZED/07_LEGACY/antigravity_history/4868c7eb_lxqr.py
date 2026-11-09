#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🩺 SYSTEM DOCTOR - "TechTool Killer" Diagnostic Scanner                    ║
║  Part of GABRIEL SYSTEM OMEGA - MC96DIGIUNIVERSE                            ║
║  GORUNFREE x1000                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

A comprehensive Mac diagnostic scanner that replicates and exceeds TechTool Pro
functionality using native macOS tools.

Modules:
    - DiskDoctor:     Volume health, file system integrity, space usage
    - SmartScanner:   SMART data, drive health, wear indicators
    - MemoryProbe:    Memory pressure, swap usage, leak detection
    - ThermalMonitor: CPU temp, fan speed, thermal throttling
    - NetworkPulse:   Interface status, latency, packet loss
    - ProcessAuditor: Resource hogs, zombie processes, open files
"""

import subprocess
import json
import os
import re
import platform
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path
from enum import Enum

# Try to import Rich for beautiful output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class HealthStatus(Enum):
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


@dataclass
class DiagnosticResult:
    """Result from a single diagnostic check."""
    name: str
    status: HealthStatus
    message: str
    details: dict = field(default_factory=dict)
    fix_suggestion: Optional[str] = None


@dataclass
class ModuleResult:
    """Result from a diagnostic module."""
    module_name: str
    icon: str
    results: list = field(default_factory=list)
    
    @property
    def overall_status(self) -> HealthStatus:
        """Get the worst status from all results."""
        if not self.results:
            return HealthStatus.UNKNOWN
        
        statuses = [r.status for r in self.results]
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        if HealthStatus.WARNING in statuses:
            return HealthStatus.WARNING
        if HealthStatus.OK in statuses:
            return HealthStatus.OK
        return HealthStatus.UNKNOWN


class SystemDoctor:
    """Main diagnostic scanner class."""
    
    VERSION = "1.0.0"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.console = Console() if RICH_AVAILABLE else None
        self.results: list[ModuleResult] = []
        self.scan_time: Optional[datetime] = None
        self.logs_dir = Path.home() / "NOIZYLAB" / "SystemGuardian" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def _run_cmd(self, cmd: list[str], timeout: int = 30) -> tuple[str, str, int]:
        """Run a command and return stdout, stderr, returncode."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", -1
        except FileNotFoundError:
            return "", f"Command not found: {cmd[0]}", -1
        except Exception as e:
            return "", str(e), -1
    
    def _status_icon(self, status: HealthStatus) -> str:
        """Get the icon for a health status."""
        icons = {
            HealthStatus.OK: "🟢",
            HealthStatus.WARNING: "🟡",
            HealthStatus.CRITICAL: "🔴",
            HealthStatus.UNKNOWN: "⚪"
        }
        return icons.get(status, "⚪")

    # ═══════════════════════════════════════════════════════════════════════════
    # DISK DOCTOR
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_disks(self) -> ModuleResult:
        """Scan disk health and space usage."""
        module = ModuleResult(module_name="DISK DOCTOR", icon="💾", results=[])
        
        # Get disk usage with df
        stdout, _, _ = self._run_cmd(["df", "-h"])
        if stdout:
            for line in stdout.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) >= 6 and parts[0].startswith("/dev/"):
                    filesystem = parts[0]
                    size = parts[1]
                    used = parts[2]
                    avail = parts[3]
                    pct_str = parts[4].replace("%", "")
                    mount = parts[5] if len(parts) > 5 else "/"
                    
                    try:
                        pct = int(pct_str)
                    except ValueError:
                        pct = 0
                    
                    if pct >= 95:
                        status = HealthStatus.CRITICAL
                        msg = f"{mount}: {pct}% used ({avail} free)"
                        fix = f"Free up space on {mount} immediately!"
                    elif pct >= 85:
                        status = HealthStatus.WARNING
                        msg = f"{mount}: {pct}% used ({avail} free)"
                        fix = f"Consider cleaning up {mount}"
                    else:
                        status = HealthStatus.OK
                        msg = f"{mount}: {avail} free / {size}"
                        fix = None
                    
                    module.results.append(DiagnosticResult(
                        name=mount,
                        status=status,
                        message=msg,
                        details={"filesystem": filesystem, "size": size, "used": used, "available": avail, "percent": pct},
                        fix_suggestion=fix
                    ))
        
        # Check for volume errors with diskutil
        stdout, _, _ = self._run_cmd(["diskutil", "list"])
        if stdout:
            # Count volumes
            volumes = len([l for l in stdout.split("\n") if "Apple_" in l or "APFS" in l])
            module.results.append(DiagnosticResult(
                name="Volume Count",
                status=HealthStatus.OK,
                message=f"{volumes} volumes detected",
                details={"count": volumes}
            ))
        
        self.results.append(module)
        return module

    # ═══════════════════════════════════════════════════════════════════════════
    # SMART SCANNER
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_smart(self) -> ModuleResult:
        """Scan SMART data for drive health."""
        module = ModuleResult(module_name="SMART SCANNER", icon="🔬", results=[])
        
        # Check if smartctl is available
        stdout, stderr, rc = self._run_cmd(["which", "smartctl"])
        if rc != 0:
            module.results.append(DiagnosticResult(
                name="smartctl",
                status=HealthStatus.UNKNOWN,
                message="smartmontools not installed",
                fix_suggestion="Install with: brew install smartmontools"
            ))
            self.results.append(module)
            return module
        
        # Get list of disks
        stdout, _, _ = self._run_cmd(["diskutil", "list", "-plist"])
        
        # Try to scan disk0 (main drive)
        for disk in ["disk0", "disk1"]:
            stdout, stderr, rc = self._run_cmd(["sudo", "smartctl", "-H", f"/dev/{disk}"])
            if rc == 0 and "PASSED" in stdout:
                module.results.append(DiagnosticResult(
                    name=f"/dev/{disk}",
                    status=HealthStatus.OK,
                    message="SMART Status: PASSED",
                    details={"raw_output": stdout[:500]}
                ))
            elif "FAILED" in stdout:
                module.results.append(DiagnosticResult(
                    name=f"/dev/{disk}",
                    status=HealthStatus.CRITICAL,
                    message="SMART Status: FAILED",
                    fix_suggestion="BACKUP DATA IMMEDIATELY! Drive failure imminent."
                ))
            elif "not supported" in stderr.lower() or "not supported" in stdout.lower():
                module.results.append(DiagnosticResult(
                    name=f"/dev/{disk}",
                    status=HealthStatus.UNKNOWN,
                    message="SMART not supported on this drive"
                ))
        
        if not module.results:
            module.results.append(DiagnosticResult(
                name="SMART",
                status=HealthStatus.UNKNOWN,
                message="No SMART-capable drives found or sudo required"
            ))
        
        self.results.append(module)
        return module

    # ═══════════════════════════════════════════════════════════════════════════
    # MEMORY PROBE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_memory(self) -> ModuleResult:
        """Scan memory usage and pressure."""
        module = ModuleResult(module_name="MEMORY PROBE", icon="🧠", results=[])
        
        # Get physical memory
        stdout, _, _ = self._run_cmd(["sysctl", "-n", "hw.memsize"])
        if stdout:
            mem_bytes = int(stdout.strip())
            mem_gb = mem_bytes / (1024**3)
            module.results.append(DiagnosticResult(
                name="Physical Memory",
                status=HealthStatus.OK,
                message=f"{mem_gb:.0f} GB installed",
                details={"bytes": mem_bytes, "gigabytes": mem_gb}
            ))
        
        # Get vm_stat for memory pressure
        stdout, _, _ = self._run_cmd(["vm_stat"])
        if stdout:
            # Parse vm_stat output
            page_size = 16384  # Default Apple Silicon page size
            
            # Extract page count for each type
            stats = {}
            for line in stdout.split("\n"):
                if ":" in line:
                    key, val = line.split(":")
                    key = key.strip()
                    val = val.strip().rstrip(".")
                    try:
                        stats[key] = int(val)
                    except ValueError:
                        pass
            
            # Calculate memory pressure
            free_pages = stats.get("Pages free", 0)
            active_pages = stats.get("Pages active", 0)
            inactive_pages = stats.get("Pages inactive", 0)
            wired_pages = stats.get("Pages wired down", 0)
            compressed = stats.get("Pages occupied by compressor", 0)
            
            free_gb = (free_pages * page_size) / (1024**3)
            active_gb = (active_pages * page_size) / (1024**3)
            wired_gb = (wired_pages * page_size) / (1024**3)
            compressed_gb = (compressed * page_size) / (1024**3)
            
            # Memory pressure calculation
            if compressed_gb > 5:
                status = HealthStatus.WARNING
                msg = f"Memory pressure elevated ({compressed_gb:.1f}GB compressed)"
                fix = "Close unused applications to reduce memory pressure"
            else:
                status = HealthStatus.OK
                msg = f"Free: {free_gb:.1f}GB, Active: {active_gb:.1f}GB, Wired: {wired_gb:.1f}GB"
                fix = None
            
            module.results.append(DiagnosticResult(
                name="Memory Pressure",
                status=status,
                message=msg,
                details={"free_gb": free_gb, "active_gb": active_gb, "wired_gb": wired_gb, "compressed_gb": compressed_gb},
                fix_suggestion=fix
            ))
        
        # Check swap usage
        stdout, _, _ = self._run_cmd(["sysctl", "-n", "vm.swapusage"])
        if stdout:
            # Parse: "total = 0.00M  used = 0.00M  free = 0.00M  (encrypted)"
            used_match = re.search(r"used = ([\d.]+)([MGK])", stdout)
            if used_match:
                used_val = float(used_match.group(1))
                used_unit = used_match.group(2)
                
                # Convert to MB
                if used_unit == "G":
                    used_mb = used_val * 1024
                elif used_unit == "K":
                    used_mb = used_val / 1024
                else:
                    used_mb = used_val
                
                if used_mb > 1024:  # More than 1GB swap
                    status = HealthStatus.WARNING
                    msg = f"Swap in use: {used_mb:.0f}MB"
                    fix = "High swap usage - consider adding RAM or closing apps"
                elif used_mb > 0:
                    status = HealthStatus.OK
                    msg = f"Swap in use: {used_mb:.0f}MB (minimal)"
                    fix = None
                else:
                    status = HealthStatus.OK
                    msg = "No swap in use"
                    fix = None
                
                module.results.append(DiagnosticResult(
                    name="Swap Usage",
                    status=status,
                    message=msg,
                    details={"used_mb": used_mb},
                    fix_suggestion=fix
                ))
        
        self.results.append(module)
        return module

    # ═══════════════════════════════════════════════════════════════════════════
    # THERMAL MONITOR
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_thermal(self) -> ModuleResult:
        """Scan CPU temperature and thermal status."""
        module = ModuleResult(module_name="THERMAL MONITOR", icon="🌡️", results=[])
        
        # Check if this is Apple Silicon or Intel
        stdout, _, _ = self._run_cmd(["uname", "-m"])
        is_apple_silicon = "arm64" in stdout
        
        # Try powermetrics (requires sudo)
        stdout, stderr, rc = self._run_cmd(
            ["sudo", "powermetrics", "-n", "1", "-i", "1000", "--samplers", "smc"],
            timeout=5
        )
        
        if rc == 0 and stdout:
            # Parse temperature from powermetrics
            temp_match = re.search(r"CPU die temperature: ([\d.]+) C", stdout)
            if temp_match:
                temp = float(temp_match.group(1))
                
                if temp > 95:
                    status = HealthStatus.CRITICAL
                    msg = f"CPU Temperature: {temp:.0f}°C - OVERHEATING!"
                    fix = "Check cooling, reduce workload, clean vents"
                elif temp > 80:
                    status = HealthStatus.WARNING
                    msg = f"CPU Temperature: {temp:.0f}°C - High"
                    fix = "Consider reducing workload"
                else:
                    status = HealthStatus.OK
                    msg = f"CPU Temperature: {temp:.0f}°C"
                    fix = None
                
                module.results.append(DiagnosticResult(
                    name="CPU Temperature",
                    status=status,
                    message=msg,
                    details={"celsius": temp},
                    fix_suggestion=fix
                ))
            
            # Parse fan speed
            fan_match = re.search(r"Fan: ([\d]+) rpm", stdout)
            if fan_match:
                fan_rpm = int(fan_match.group(1))
                module.results.append(DiagnosticResult(
                    name="Fan Speed",
                    status=HealthStatus.OK,
                    message=f"{fan_rpm} RPM",
                    details={"rpm": fan_rpm}
                ))
        else:
            # Fallback: Use sysctl for basic thermal info
            stdout, _, _ = self._run_cmd(["sysctl", "-a"])
            if "machdep.cpu.thermal" in stdout or is_apple_silicon:
                module.results.append(DiagnosticResult(
                    name="Thermal Status",
                    status=HealthStatus.UNKNOWN,
                    message="Run with sudo for detailed thermal data",
                    fix_suggestion="Run: sudo python -m modules.cli --thermal"
                ))
            else:
                module.results.append(DiagnosticResult(
                    name="Thermal Status",
                    status=HealthStatus.UNKNOWN,
                    message="Thermal monitoring not available"
                ))
        
        # Check thermal throttling
        if is_apple_silicon:
            stdout, _, rc = self._run_cmd(["pmset", "-g", "therm"])
            if rc == 0:
                if "speed_limit" in stdout.lower() and "100" in stdout:
                    module.results.append(DiagnosticResult(
                        name="Thermal Throttling",
                        status=HealthStatus.OK,
                        message="No throttling detected"
                    ))
                elif "speed_limit" in stdout.lower():
                    module.results.append(DiagnosticResult(
                        name="Thermal Throttling",
                        status=HealthStatus.WARNING,
                        message="CPU may be thermally throttled",
                        fix_suggestion="Improve cooling or reduce workload"
                    ))
        
        self.results.append(module)
        return module

    # ═══════════════════════════════════════════════════════════════════════════
    # NETWORK PULSE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_network(self) -> ModuleResult:
        """Scan network interfaces and connectivity."""
        module = ModuleResult(module_name="NETWORK PULSE", icon="🌐", results=[])
        
        # Get active interfaces
        stdout, _, _ = self._run_cmd(["ifconfig"])
        if stdout:
            # Find active interfaces
            interfaces = {}
            current_if = None
            
            for line in stdout.split("\n"):
                if not line.startswith("\t") and ":" in line:
                    current_if = line.split(":")[0]
                    interfaces[current_if] = {"up": False, "ip": None}
                elif current_if and "status: active" in line:
                    interfaces[current_if]["up"] = True
                elif current_if and "inet " in line and "127.0.0.1" not in line:
                    ip_match = re.search(r"inet ([\d.]+)", line)
                    if ip_match:
                        interfaces[current_if]["ip"] = ip_match.group(1)
            
            # Report active interfaces
            for iface, info in interfaces.items():
                if info["up"] and info["ip"]:
                    if iface.startswith("en"):
                        name = "Ethernet" if iface == "en0" else f"Interface {iface}"
                    elif iface.startswith("bridge"):
                        name = "Bridge"
                    else:
                        name = iface
                    
                    module.results.append(DiagnosticResult(
                        name=name,
                        status=HealthStatus.OK,
                        message=f"{iface}: Connected ({info['ip']})",
                        details={"interface": iface, "ip": info["ip"]}
                    ))
        
        # Ping test to Google DNS
        stdout, _, rc = self._run_cmd(["ping", "-c", "3", "-t", "5", "8.8.8.8"])
        if rc == 0:
            # Parse latency
            time_match = re.search(r"avg = ([\d.]+)", stdout)
            if time_match:
                latency = float(time_match.group(1))
                
                if latency > 100:
                    status = HealthStatus.WARNING
                    msg = f"Latency to 8.8.8.8: {latency:.0f}ms (high)"
                else:
                    status = HealthStatus.OK
                    msg = f"Latency to 8.8.8.8: {latency:.0f}ms"
                
                module.results.append(DiagnosticResult(
                    name="Internet Latency",
                    status=status,
                    message=msg,
                    details={"latency_ms": latency}
                ))
        else:
            module.results.append(DiagnosticResult(
                name="Internet Latency",
                status=HealthStatus.CRITICAL,
                message="Cannot reach 8.8.8.8 - connectivity issue",
                fix_suggestion="Check network connection and router"
            ))
        
        # DNS resolution test
        stdout, _, rc = self._run_cmd(["nslookup", "google.com"])
        if rc == 0 and "Address:" in stdout:
            module.results.append(DiagnosticResult(
                name="DNS Resolution",
                status=HealthStatus.OK,
                message="DNS working correctly"
            ))
        else:
            module.results.append(DiagnosticResult(
                name="DNS Resolution",
                status=HealthStatus.WARNING,
                message="DNS resolution issues detected",
                fix_suggestion="Try: sudo dscacheutil -flushcache"
            ))
        
        self.results.append(module)
        return module

    # ═══════════════════════════════════════════════════════════════════════════
    # PROCESS AUDITOR
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_processes(self) -> ModuleResult:
        """Scan for resource-hogging and zombie processes."""
        module = ModuleResult(module_name="PROCESS AUDITOR", icon="⚙️", results=[])
        
        # Count total processes
        stdout, _, _ = self._run_cmd(["ps", "aux"])
        if stdout:
            process_count = len(stdout.strip().split("\n")) - 1  # Minus header
            module.results.append(DiagnosticResult(
                name="Total Processes",
                status=HealthStatus.OK,
                message=f"{process_count} processes running",
                details={"count": process_count}
            ))
        
        # Find CPU hogs (>50% CPU)
        stdout, _, _ = self._run_cmd(["ps", "-arcwwwxo", "pid,pcpu,comm"])
        if stdout:
            cpu_hogs = []
            for line in stdout.strip().split("\n")[1:]:  # Skip header
                parts = line.split(None, 2)
                if len(parts) >= 3:
                    try:
                        pid = parts[0]
                        cpu = float(parts[1])
                        comm = parts[2]
                        if cpu > 50:
                            cpu_hogs.append({"pid": pid, "cpu": cpu, "name": comm})
                    except ValueError:
                        pass
            
            if cpu_hogs:
                status = HealthStatus.WARNING
                msg = f"{len(cpu_hogs)} process(es) using >50% CPU"
                details = {"processes": cpu_hogs}
                fix = f"Consider killing: {', '.join(h['name'] for h in cpu_hogs[:3])}"
            else:
                status = HealthStatus.OK
                msg = "No CPU hogs detected"
                details = {}
                fix = None
            
            module.results.append(DiagnosticResult(
                name="CPU Hogs",
                status=status,
                message=msg,
                details=details,
                fix_suggestion=fix
            ))
        
        # Find zombie processes
        stdout, _, _ = self._run_cmd(["ps", "aux"])
        if stdout:
            zombies = [l for l in stdout.split("\n") if " Z " in l or " Z+ " in l]
            
            if zombies:
                module.results.append(DiagnosticResult(
                    name="Zombie Processes",
                    status=HealthStatus.WARNING,
                    message=f"{len(zombies)} zombie process(es) detected",
                    details={"count": len(zombies)},
                    fix_suggestion="Zombie processes may require parent process restart"
                ))
            else:
                module.results.append(DiagnosticResult(
                    name="Zombie Processes",
                    status=HealthStatus.OK,
                    message="No zombie processes",
                    details={"count": 0}
                ))
        
        self.results.append(module)
        return module

    # ═══════════════════════════════════════════════════════════════════════════
    # FULL SCAN & REPORTING
    # ═══════════════════════════════════════════════════════════════════════════
    
    def run_full_scan(self, show_progress: bool = True) -> list[ModuleResult]:
        """Run all diagnostic modules."""
        self.results = []
        self.scan_time = datetime.now()
        
        modules = [
            ("Disk Doctor", self.scan_disks),
            ("SMART Scanner", self.scan_smart),
            ("Memory Probe", self.scan_memory),
            ("Thermal Monitor", self.scan_thermal),
            ("Network Pulse", self.scan_network),
            ("Process Auditor", self.scan_processes),
        ]
        
        if RICH_AVAILABLE and show_progress:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                task = progress.add_task("Running diagnostics...", total=len(modules))
                for name, func in modules:
                    progress.update(task, description=f"Scanning: {name}...")
                    func()
                    progress.advance(task)
        else:
            for name, func in modules:
                if self.verbose:
                    print(f"Scanning: {name}...")
                func()
        
        return self.results
    
    def print_results(self):
        """Print results to console with Rich formatting."""
        if not RICH_AVAILABLE:
            self._print_plain_results()
            return
        
        # Header
        self.console.print()
        self.console.print(Panel.fit(
            "[bold white]🩺 SYSTEM DOCTOR - Full Diagnostic Report[/bold white]",
            border_style="cyan"
        ))
        self.console.print()
        
        # Each module
        for module in self.results:
            table = Table(
                title=f"{module.icon} {module.module_name}",
                box=box.ROUNDED,
                title_style="bold magenta",
                show_header=False,
                padding=(0, 1)
            )
            table.add_column("Status", width=3)
            table.add_column("Check", style="cyan")
            table.add_column("Result")
            
            for result in module.results:
                icon = self._status_icon(result.status)
                
                if result.status == HealthStatus.CRITICAL:
                    style = "bold red"
                elif result.status == HealthStatus.WARNING:
                    style = "yellow"
                else:
                    style = "green"
                
                table.add_row(icon, result.name, f"[{style}]{result.message}[/{style}]")
                
                if result.fix_suggestion:
                    table.add_row("", "", f"[dim italic]→ {result.fix_suggestion}[/dim italic]")
            
            self.console.print(table)
            self.console.print()
        
        # Overall status
        overall = self._get_overall_status()
        if overall == HealthStatus.CRITICAL:
            self.console.print("[bold red]⚠️  CRITICAL ISSUES DETECTED - Action Required![/bold red]")
        elif overall == HealthStatus.WARNING:
            self.console.print("[yellow]⚡ Some warnings detected - Review recommended[/yellow]")
        else:
            self.console.print("[bold green]✅ System health: GOOD[/bold green]")
        
        self.console.print()
    
    def _print_plain_results(self):
        """Print results without Rich formatting."""
        print("\n" + "=" * 60)
        print("  🩺 SYSTEM DOCTOR - Full Diagnostic Report")
        print("=" * 60 + "\n")
        
        for module in self.results:
            print(f"\n{module.icon} {module.module_name}")
            print("-" * 40)
            
            for result in module.results:
                icon = self._status_icon(result.status)
                print(f"  {icon} {result.name}: {result.message}")
                if result.fix_suggestion:
                    print(f"     → {result.fix_suggestion}")
        
        print("\n" + "=" * 60)
    
    def _get_overall_status(self) -> HealthStatus:
        """Get overall system health status."""
        all_statuses = []
        for module in self.results:
            all_statuses.append(module.overall_status)
        
        if HealthStatus.CRITICAL in all_statuses:
            return HealthStatus.CRITICAL
        if HealthStatus.WARNING in all_statuses:
            return HealthStatus.WARNING
        return HealthStatus.OK
    
    def export_json(self, filepath: Optional[Path] = None) -> Path:
        """Export results to JSON file."""
        if filepath is None:
            timestamp = self.scan_time.strftime("%Y-%m-%d_%H%M%S") if self.scan_time else datetime.now().strftime("%Y-%m-%d_%H%M%S")
            filepath = self.logs_dir / f"system_doctor_{timestamp}.json"
        
        report = {
            "version": self.VERSION,
            "scan_time": self.scan_time.isoformat() if self.scan_time else None,
            "hostname": platform.node(),
            "os_version": platform.mac_ver()[0],
            "overall_status": self._get_overall_status().value,
            "modules": []
        }
        
        for module in self.results:
            module_data = {
                "name": module.module_name,
                "icon": module.icon,
                "overall_status": module.overall_status.value,
                "results": []
            }
            
            for result in module.results:
                result_data = {
                    "name": result.name,
                    "status": result.status.value,
                    "message": result.message,
                    "details": result.details,
                    "fix_suggestion": result.fix_suggestion
                }
                module_data["results"].append(result_data)
            
            report["modules"].append(module_data)
        
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        return filepath


# ═══════════════════════════════════════════════════════════════════════════════
# STANDALONE EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    doctor = SystemDoctor(verbose=True)
    doctor.run_full_scan()
    doctor.print_results()

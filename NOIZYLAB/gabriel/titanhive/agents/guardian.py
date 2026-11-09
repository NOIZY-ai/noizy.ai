"""
GUARDIAN AGENT
==============
Monitors system health, memory pressure, and thermals.
Auto-optimizes when needed.
"""

import asyncio
import subprocess
import psutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional


@dataclass
class SystemHealth:
    """Current system health snapshot."""
    timestamp: datetime
    cpu_percent: float
    memory_used_gb: float
    memory_available_gb: float
    memory_pressure: str  # "normal", "warning", "critical"
    cpu_temp_c: Optional[float]
    gpu_temp_c: Optional[float]
    fan_speed_rpm: Optional[int]
    swap_used_gb: float
    process_count: int
    top_memory_processes: list[tuple[str, float]]  # (name, gb)


class GuardianAgent:
    """
    Guardian Agent - System Health Monitor & Auto-Optimizer

    Responsibilities:
    - Monitor memory pressure (critical for 192GB AI workloads)
    - Track CPU and GPU thermals
    - Alert when resources are constrained
    - Auto-kill runaway processes (optional)
    - Suggest optimizations
    """

    # Thresholds
    MEMORY_WARNING_GB = 30  # Warn when < 30GB available
    MEMORY_CRITICAL_GB = 10  # Critical when < 10GB available
    CPU_WARNING_PERCENT = 90
    TEMP_WARNING_C = 85

    def __init__(self, on_alert: Optional[Callable[[str, str], None]] = None):
        """
        Initialize Guardian.

        Args:
            on_alert: Callback for alerts (level, message)
        """
        self.on_alert = on_alert or (lambda l, m: print(f"[{l}] {m}"))
        self._running = False
        self._last_health: Optional[SystemHealth] = None

    def get_health(self) -> SystemHealth:
        """Get current system health snapshot."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        cpu = psutil.cpu_percent(interval=0.1)

        # Memory calculations
        used_gb = mem.used / (1024**3)
        available_gb = mem.available / (1024**3)
        swap_used_gb = swap.used / (1024**3)

        # Memory pressure level
        if available_gb < self.MEMORY_CRITICAL_GB:
            pressure = "critical"
        elif available_gb < self.MEMORY_WARNING_GB:
            pressure = "warning"
        else:
            pressure = "normal"

        # Get thermals (macOS specific)
        cpu_temp = self._get_cpu_temp()
        gpu_temp = self._get_gpu_temp()
        fan_speed = self._get_fan_speed()

        # Top memory processes
        top_procs = []
        try:
            for proc in sorted(psutil.process_iter(['name', 'memory_info']),
                             key=lambda p: p.info.get('memory_info', 0) or 0,
                             reverse=True)[:5]:
                try:
                    name = proc.info['name']
                    mem_gb = (proc.info['memory_info'].rss / (1024**3)) if proc.info['memory_info'] else 0
                    if mem_gb > 0.1:  # Only show > 100MB
                        top_procs.append((name, mem_gb))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass

        health = SystemHealth(
            timestamp=datetime.now(),
            cpu_percent=cpu,
            memory_used_gb=used_gb,
            memory_available_gb=available_gb,
            memory_pressure=pressure,
            cpu_temp_c=cpu_temp,
            gpu_temp_c=gpu_temp,
            fan_speed_rpm=fan_speed,
            swap_used_gb=swap_used_gb,
            process_count=len(list(psutil.process_iter())),
            top_memory_processes=top_procs,
        )

        self._last_health = health
        return health

    def _get_cpu_temp(self) -> Optional[float]:
        """Get CPU temperature on macOS."""
        try:
            # Try using powermetrics (requires sudo) or osx-cpu-temp
            result = subprocess.run(
                ["sudo", "powermetrics", "--samplers", "smc", "-i1", "-n1"],
                capture_output=True, text=True, timeout=5
            )
            # Parse temperature from output
            for line in result.stdout.split('\n'):
                if 'CPU die temperature' in line:
                    temp = float(line.split(':')[1].strip().replace(' C', ''))
                    return temp
        except Exception:
            pass
        return None

    def _get_gpu_temp(self) -> Optional[float]:
        """Get GPU temperature on macOS."""
        try:
            result = subprocess.run(
                ["sudo", "powermetrics", "--samplers", "smc", "-i1", "-n1"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split('\n'):
                if 'GPU die temperature' in line:
                    temp = float(line.split(':')[1].strip().replace(' C', ''))
                    return temp
        except Exception:
            pass
        return None

    def _get_fan_speed(self) -> Optional[int]:
        """Get fan speed on macOS."""
        try:
            result = subprocess.run(
                ["sudo", "powermetrics", "--samplers", "smc", "-i1", "-n1"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split('\n'):
                if 'Fan' in line and 'rpm' in line:
                    # Extract RPM value
                    import re
                    match = re.search(r'(\d+)\s*rpm', line)
                    if match:
                        return int(match.group(1))
        except Exception:
            pass
        return None

    def check_and_alert(self) -> list[tuple[str, str]]:
        """Check health and return any alerts."""
        health = self.get_health()
        alerts = []

        # Memory alerts
        if health.memory_pressure == "critical":
            alerts.append(("CRITICAL",
                f"Memory critical: only {health.memory_available_gb:.1f}GB available!"))
        elif health.memory_pressure == "warning":
            alerts.append(("WARNING",
                f"Memory low: {health.memory_available_gb:.1f}GB available"))

        # CPU alerts
        if health.cpu_percent > self.CPU_WARNING_PERCENT:
            alerts.append(("WARNING", f"CPU high: {health.cpu_percent:.1f}%"))

        # Temperature alerts
        if health.cpu_temp_c and health.cpu_temp_c > self.TEMP_WARNING_C:
            alerts.append(("WARNING", f"CPU temp high: {health.cpu_temp_c:.1f}°C"))
        if health.gpu_temp_c and health.gpu_temp_c > self.TEMP_WARNING_C:
            alerts.append(("WARNING", f"GPU temp high: {health.gpu_temp_c:.1f}°C"))

        # Swap usage
        if health.swap_used_gb > 5:
            alerts.append(("WARNING", f"Swap in use: {health.swap_used_gb:.1f}GB"))

        # Send alerts
        for level, message in alerts:
            self.on_alert(level, message)

        return alerts

    def get_optimization_suggestions(self) -> list[str]:
        """Get optimization suggestions based on current state."""
        health = self.get_health()
        suggestions = []

        if health.memory_available_gb < 100:
            suggestions.append(
                "Consider closing unused apps to free memory for AI workloads"
            )

        if health.memory_available_gb > 150:
            suggestions.append(
                "You have plenty of VRAM! Try running larger models like llama3.1:70b"
            )

        if health.swap_used_gb > 0:
            suggestions.append(
                "Swap is in use. Close memory-hungry apps for better performance"
            )

        if health.top_memory_processes:
            top_proc, top_mem = health.top_memory_processes[0]
            if top_mem > 20:
                suggestions.append(
                    f"{top_proc} is using {top_mem:.1f}GB. Consider if needed."
                )

        return suggestions

    def format_status(self) -> str:
        """Format current status as string."""
        health = self.get_health()

        lines = [
            "═══ GUARDIAN STATUS ═══",
            f"Memory: {health.memory_used_gb:.0f}GB / 192GB ({health.memory_pressure})",
            f"Available: {health.memory_available_gb:.0f}GB for AI",
            f"CPU: {health.cpu_percent:.1f}%",
        ]

        if health.cpu_temp_c:
            lines.append(f"CPU Temp: {health.cpu_temp_c:.1f}°C")
        if health.gpu_temp_c:
            lines.append(f"GPU Temp: {health.gpu_temp_c:.1f}°C")
        if health.fan_speed_rpm:
            lines.append(f"Fan: {health.fan_speed_rpm} RPM")

        if health.swap_used_gb > 0:
            lines.append(f"Swap: {health.swap_used_gb:.1f}GB")

        lines.append(f"Processes: {health.process_count}")

        if health.top_memory_processes:
            lines.append("─── Top Memory Users ───")
            for name, gb in health.top_memory_processes[:3]:
                lines.append(f"  {name}: {gb:.1f}GB")

        return "\n".join(lines)

    async def monitor_loop(self, interval: float = 5.0):
        """Run continuous monitoring loop."""
        self._running = True
        while self._running:
            self.check_and_alert()
            await asyncio.sleep(interval)

    def stop(self):
        """Stop the monitoring loop."""
        self._running = False

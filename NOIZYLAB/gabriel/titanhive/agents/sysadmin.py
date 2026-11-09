"""
SYSADMIN AGENT
==============
Manages system health, updates, backups, and remote nodes.
"""

import asyncio
import json
import os
import socket
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable


@dataclass
class NodeStatus:
    """Status of a network node."""
    name: str
    host: str
    port: int
    online: bool
    latency_ms: Optional[float]
    last_check: datetime
    extra_info: dict


class SysAdminAgent:
    """
    SysAdmin Agent - System & Network Management

    Responsibilities:
    - Monitor network nodes (Omen, Mac Pro, etc.)
    - Perform health checks
    - Manage backups and syncs
    - Execute remote commands
    - Track uptime and availability
    """

    def __init__(self, on_status: Optional[Callable[[str, str], None]] = None):
        """
        Initialize SysAdmin.

        Args:
            on_status: Callback for status updates
        """
        self.on_status = on_status or (lambda n, s: print(f"[{n}] {s}"))

        # Define nodes to monitor
        self.nodes = {
            "ollama": {
                "host": os.getenv("OLLAMA_URL", "http://localhost:11434").replace("http://", "").split(":")[0],
                "port": 11434,
                "type": "service",
            },
            "omen": {
                "host": os.getenv("OMEN_HOST", "10.0.0.160"),
                "port": 22,
                "type": "ssh",
                "user": os.getenv("OMEN_USER", "admin"),
            },
        }

        self._node_status: dict[str, NodeStatus] = {}
        self._history: list[dict] = []

    def check_port(self, host: str, port: int, timeout: float = 2.0) -> tuple[bool, float]:
        """
        Check if a port is open.

        Returns:
            (is_open, latency_ms)
        """
        import time
        start = time.perf_counter()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.close()
            latency = (time.perf_counter() - start) * 1000
            return True, latency
        except Exception:
            return False, 0

    def check_node(self, name: str) -> NodeStatus:
        """Check a specific node."""
        if name not in self.nodes:
            raise ValueError(f"Unknown node: {name}")

        node = self.nodes[name]
        online, latency = self.check_port(node["host"], node["port"])

        extra_info = {}

        # Get additional info for online nodes
        if online:
            if node.get("type") == "ssh":
                # Try to get uptime via SSH
                try:
                    result = subprocess.run(
                        ["ssh", "-o", "ConnectTimeout=2", "-o", "StrictHostKeyChecking=no",
                         f"{node.get('user', 'root')}@{node['host']}", "uptime"],
                        capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        extra_info["uptime"] = result.stdout.strip()
                except Exception:
                    pass

            elif node.get("type") == "service" and name == "ollama":
                # Get Ollama model count
                try:
                    import urllib.request
                    url = f"http://{node['host']}:{node['port']}/api/tags"
                    with urllib.request.urlopen(url, timeout=2) as resp:
                        data = json.loads(resp.read())
                        extra_info["models"] = len(data.get("models", []))
                except Exception:
                    pass

        status = NodeStatus(
            name=name,
            host=node["host"],
            port=node["port"],
            online=online,
            latency_ms=latency if online else None,
            last_check=datetime.now(),
            extra_info=extra_info,
        )

        self._node_status[name] = status
        return status

    def check_all_nodes(self) -> dict[str, NodeStatus]:
        """Check all nodes."""
        for name in self.nodes:
            self.check_node(name)
        return self._node_status

    def send_wol(self, mac_address: str, broadcast: str = "255.255.255.255") -> bool:
        """Send Wake-on-LAN magic packet."""
        try:
            mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
            magic_packet = b'\xff' * 6 + mac_bytes * 16
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, (broadcast, 9))
            sock.close()
            return True
        except Exception:
            return False

    def run_remote_command(self, node_name: str, command: str, timeout: int = 30) -> tuple[bool, str]:
        """
        Run a command on a remote node via SSH.

        Returns:
            (success, output)
        """
        if node_name not in self.nodes:
            return False, f"Unknown node: {node_name}"

        node = self.nodes[node_name]
        if node.get("type") != "ssh":
            return False, f"Node {node_name} doesn't support SSH"

        try:
            result = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no",
                 f"{node.get('user', 'root')}@{node['host']}", command],
                capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)

    def sync_to_vault(self, source: Path, vault_path: Path, dry_run: bool = True) -> tuple[bool, str]:
        """
        Sync files to vault using rsync.

        Args:
            source: Source path
            vault_path: Destination vault path
            dry_run: If True, only simulate

        Returns:
            (success, output)
        """
        cmd = ["rsync", "-avz", "--progress"]
        if dry_run:
            cmd.append("--dry-run")

        cmd.extend([str(source) + "/", str(vault_path) + "/"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)

    def get_network_speed(self) -> dict:
        """Test network speed to nodes."""
        results = {}

        for name, node in self.nodes.items():
            status = self.check_node(name)
            if status.online:
                results[name] = {
                    "latency_ms": status.latency_ms,
                    "status": "online",
                }
            else:
                results[name] = {"status": "offline"}

        return results

    def format_status(self) -> str:
        """Format current status as string."""
        self.check_all_nodes()

        lines = ["═══ SYSADMIN STATUS ═══"]

        for name, status in self._node_status.items():
            state = "ONLINE" if status.online else "OFFLINE"
            latency = f"{status.latency_ms:.1f}ms" if status.latency_ms else "N/A"
            lines.append(f"{name}: {state} ({latency})")

            for key, value in status.extra_info.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)

    async def monitor_loop(self, interval: float = 30.0):
        """Run continuous monitoring loop."""
        self._running = True
        while self._running:
            self.check_all_nodes()
            await asyncio.sleep(interval)

    def stop(self):
        """Stop the monitoring loop."""
        self._running = False

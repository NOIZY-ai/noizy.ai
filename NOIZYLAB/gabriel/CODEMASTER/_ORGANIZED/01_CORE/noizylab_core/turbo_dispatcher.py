#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TURBO DISPATCHER v1.0                                     ║
║                    GORUNFREE x1000 COMMAND CENTER                            ║
║                                                                              ║
║  Unified command dispatcher for all GABRIEL operations.                     ║
║  One entry point. All power. Zero latency.                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Any
from dataclasses import dataclass, field


@dataclass
class Command:
    """A dispatchable command"""
    name: str
    description: str
    handler: Callable
    category: str = "general"
    aliases: list = field(default_factory=list)


class TurboDispatcher:
    """
    GORUNFREE Command Dispatcher
    
    Routes commands to appropriate handlers.
    Extensible, fast, zero-latency execution.
    """
    
    def __init__(self):
        self.commands: dict[str, Command] = {}
        self.aliases: dict[str, str] = {}
        self.history: list[dict] = []
        self._register_builtins()
    
    def register(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        category: str = "general",
        aliases: list = None
    ):
        """Register a command"""
        cmd = Command(name, description, handler, category, aliases or [])
        self.commands[name] = cmd
        for alias in cmd.aliases:
            self.aliases[alias] = name
    
    def dispatch(self, command: str, *args, **kwargs) -> Any:
        """Dispatch a command by name"""
        start = datetime.now()
        
        # Resolve alias
        resolved = self.aliases.get(command, command)
        
        if resolved not in self.commands:
            return {"error": f"Unknown command: {command}", "available": list(self.commands.keys())}
        
        cmd = self.commands[resolved]
        
        try:
            result = cmd.handler(*args, **kwargs)
            elapsed = (datetime.now() - start).total_seconds()
            
            self.history.append({
                "command": command,
                "resolved": resolved,
                "args": args,
                "elapsed_ms": round(elapsed * 1000, 2),
                "timestamp": start.isoformat(),
                "status": "success"
            })
            
            return result
            
        except Exception as e:
            self.history.append({
                "command": command,
                "resolved": resolved,
                "error": str(e),
                "timestamp": start.isoformat(),
                "status": "error"
            })
            return {"error": str(e)}
    
    def _register_builtins(self):
        """Register built-in commands"""
        
        # System commands
        self.register("status", self._cmd_status, "System status", "system", ["st"])
        self.register("scan", self._cmd_scan, "Run visual scanner", "system")
        self.register("help", self._cmd_help, "Show help", "system", ["?", "h"])
        self.register("history", self._cmd_history, "Command history", "system")
        
        # AI commands
        self.register("ask", self._cmd_ask, "Ask GABRIEL", "ai", ["a", "q"])
        self.register("dream", self._cmd_dream, "Multi-AI dream", "ai", ["d"])
        self.register("flow", self._cmd_flow, "Full creative flow", "ai", ["f"])
        
        # File commands
        self.register("index", self._cmd_index, "Index code files", "file")
        self.register("search", self._cmd_search, "Search memcells", "file", ["s"])
        
        # Launcher commands
        self.register("sovereign", self._cmd_sovereign, "Run SOVEREIGN_FINAL_100", "launcher")
        self.register("portal", self._cmd_portal, "Open DREAMCHAMBER portal", "launcher")
        
        # Slack commands
        self.register("slack", self._cmd_slack, "Send to Slack", "comm", ["sl"])
    
    # =========================================================================
    # COMMAND HANDLERS
    # =========================================================================
    
    def _cmd_status(self) -> dict:
        """Get system status"""
        return {
            "status": "ONLINE",
            "alignment": "100%",
            "energy": "∞ INFINITE",
            "gorunfree": "x1000 ACTIVE",
            "commands_registered": len(self.commands),
            "history_length": len(self.history),
            "timestamp": datetime.now().isoformat()
        }
    
    def _cmd_scan(self, path: str = "/Volumes") -> dict:
        """Run visual scanner"""
        scanner_path = Path(__file__).parent.parent.parent / "GABRIEL_UNIFIED/core/visual_scanner.py"
        
        if not scanner_path.exists():
            # Try alternative path
            alt_path = Path.home() / ".gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/GABRIEL_UNIFIED/core/visual_scanner.py"
            if alt_path.exists():
                scanner_path = alt_path
            else:
                return {"error": "visual_scanner.py not found"}
        
        result = subprocess.run(
            [sys.executable, str(scanner_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            "status": "completed" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "output_lines": len(result.stdout.split('\n')) if result.stdout else 0
        }
    
    def _cmd_help(self, category: Optional[str] = None) -> dict:
        """Show help"""
        if category:
            cmds = {k: v for k, v in self.commands.items() if v.category == category}
        else:
            cmds = self.commands
        
        return {
            "commands": {
                name: {
                    "description": cmd.description,
                    "category": cmd.category,
                    "aliases": cmd.aliases
                }
                for name, cmd in cmds.items()
            }
        }
    
    def _cmd_history(self, limit: int = 10) -> list:
        """Get command history"""
        return self.history[-limit:]
    
    def _cmd_ask(self, prompt: str, provider: str = "Claude") -> dict:
        """Ask GABRIEL"""
        try:
            from .master_cell import DreamChamber, GeneratorConfig
            
            config = GeneratorConfig(
                claude_key=os.environ.get("ANTHROPIC_API_KEY"),
                gemini_key=os.environ.get("GEMINI_API_KEY"),
                openai_key=os.environ.get("OPENAI_API_KEY")
            )
            
            chamber = DreamChamber(config)
            response = chamber.quick(prompt, provider)
            
            return {"prompt": prompt, "provider": provider, "response": response}
            
        except Exception as e:
            return {"error": str(e)}
    
    def _cmd_dream(self, prompt: str, providers: list = None) -> dict:
        """Multi-AI dream"""
        try:
            from .master_cell import DreamChamber, GeneratorConfig
            
            config = GeneratorConfig(
                claude_key=os.environ.get("ANTHROPIC_API_KEY"),
                gemini_key=os.environ.get("GEMINI_API_KEY"),
                openai_key=os.environ.get("OPENAI_API_KEY")
            )
            
            chamber = DreamChamber(config)
            result = chamber.dream(prompt, providers or ["Claude", "Gemini"])
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def _cmd_flow(self, prompt: str) -> dict:
        """Full creative flow"""
        try:
            from .master_cell import DreamChamber, GeneratorConfig
            
            config = GeneratorConfig(
                claude_key=os.environ.get("ANTHROPIC_API_KEY"),
                gemini_key=os.environ.get("GEMINI_API_KEY"),
                openai_key=os.environ.get("OPENAI_API_KEY")
            )
            
            chamber = DreamChamber(config)
            return chamber.flow(prompt)
            
        except Exception as e:
            return {"error": str(e)}
    
    def _cmd_index(self) -> dict:
        """Run forensic scanner to index code"""
        scanner_path = Path(__file__).parent.parent / "utils/forensic_scanner.py"
        
        if not scanner_path.exists():
            return {"error": "forensic_scanner.py not found"}
        
        result = subprocess.run(
            [sys.executable, str(scanner_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            "status": "completed" if result.returncode == 0 else "error",
            "output": result.stdout[-2000:] if result.stdout else ""
        }
    
    def _cmd_search(self, query: str) -> dict:
        """Search memcells"""
        try:
            from .master_cell import MemCellStore
            
            store = MemCellStore()
            results = store.search(query)
            
            return {"query": query, "results": [r.content[:200] for r in results]}
            
        except Exception as e:
            return {"error": str(e)}
    
    def _cmd_sovereign(self) -> dict:
        """Run SOVEREIGN_FINAL_100.sh"""
        script_path = Path.home() / "NOIZYLAB/GABRIEL/SOVEREIGN_FINAL_100.sh"
        
        if not script_path.exists():
            return {"error": "SOVEREIGN_FINAL_100.sh not found"}
        
        result = subprocess.run(
            ["zsh", str(script_path)],
            capture_output=True,
            text=True,
            env={**os.environ, "TERM": "xterm-256color"},
            timeout=60
        )
        
        return {
            "status": "SINGULARITY REACHED" if result.returncode == 0 else "error",
            "alignment": "100%",
            "gorunfree": "x1000 ACTIVE"
        }
    
    def _cmd_portal(self) -> dict:
        """Open DREAMCHAMBER portal"""
        portal_path = Path.home() / "noizylab/DREAMCHAMBER/index.html"
        
        if not portal_path.exists():
            return {"error": "DREAMCHAMBER portal not found"}
        
        subprocess.run(["open", str(portal_path)])
        return {"status": "Portal opened", "path": str(portal_path)}
    
    def _cmd_slack(self, message: str, channel: str = "#social") -> dict:
        """Send message to Slack"""
        try:
            from .slack_bridge import create_slack_bridge
            
            bridge = create_slack_bridge()
            result = bridge.send_message(message, channel)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}


# Global dispatcher instance
_dispatcher: Optional[TurboDispatcher] = None


def get_dispatcher() -> TurboDispatcher:
    """Get or create the global dispatcher"""
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = TurboDispatcher()
    return _dispatcher


def dispatch(command: str, *args, **kwargs) -> Any:
    """Dispatch a command"""
    return get_dispatcher().dispatch(command, *args, **kwargs)


__all__ = ['TurboDispatcher', 'Command', 'get_dispatcher', 'dispatch']


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              TURBO DISPATCHER v1.0                           ║")
    print("║              GORUNFREE x1000 COMMAND CENTER                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    d = get_dispatcher()
    
    # Show status
    print("📊 STATUS:")
    status = d.dispatch("status")
    for k, v in status.items():
        print(f"   {k}: {v}")
    
    print()
    print("📋 AVAILABLE COMMANDS:")
    help_info = d.dispatch("help")
    for name, info in help_info["commands"].items():
        aliases = f" ({', '.join(info['aliases'])})" if info['aliases'] else ""
        print(f"   {name}{aliases}: {info['description']} [{info['category']}]")

#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    REALTIME WATCHER v1.0                                     ║
║                    GORUNFREE FILE MONITORING                                 ║
║                                                                              ║
║  Watch files for changes and trigger AI-powered actions.                    ║
║  Auto-format, auto-fix, auto-document. Zero latency.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import hashlib
import threading
from pathlib import Path
from typing import Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


@dataclass
class WatchEvent:
    """File change event"""
    path: Path
    event_type: str  # created, modified, deleted
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    old_hash: Optional[str] = None
    new_hash: Optional[str] = None


@dataclass 
class WatchConfig:
    """Watcher configuration"""
    paths: list[Path] = field(default_factory=list)
    extensions: list[str] = field(default_factory=lambda: ['.py', '.js', '.ts', '.json', '.md'])
    ignore_patterns: list[str] = field(default_factory=lambda: ['__pycache__', '.git', 'node_modules', '.venv'])
    poll_interval: float = 1.0
    auto_format: bool = False
    auto_lint: bool = False


class RealtimeWatcher:
    """
    Realtime File Watcher
    
    Monitors files for changes and triggers callbacks.
    Perfect for auto-formatting, linting, and AI-powered fixes.
    """
    
    def __init__(self, config: Optional[WatchConfig] = None):
        self.config = config or WatchConfig()
        self.handlers: dict[str, list[Callable]] = {
            'created': [],
            'modified': [],
            'deleted': [],
            '*': []
        }
        self.file_hashes: dict[str, str] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.events: list[WatchEvent] = []
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def watch(self, path: str | Path):
        """Add a path to watch"""
        self.config.paths.append(Path(path))
        return self
    
    def on(self, event_type: str, handler: Callable[[WatchEvent], None]):
        """Register an event handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        return self
    
    def _get_hash(self, path: Path) -> str:
        """Get file content hash"""
        try:
            return hashlib.md5(path.read_bytes()).hexdigest()
        except:
            return ""
    
    def _should_watch(self, path: Path) -> bool:
        """Check if file should be watched"""
        # Check extension
        if self.config.extensions and path.suffix not in self.config.extensions:
            return False
        
        # Check ignore patterns
        path_str = str(path)
        for pattern in self.config.ignore_patterns:
            if pattern in path_str:
                return False
        
        return True
    
    def _scan_files(self) -> dict[str, str]:
        """Scan all watched paths and return file hashes"""
        files = {}
        
        for watch_path in self.config.paths:
            if not watch_path.exists():
                continue
            
            if watch_path.is_file():
                if self._should_watch(watch_path):
                    files[str(watch_path)] = self._get_hash(watch_path)
            else:
                for path in watch_path.rglob('*'):
                    if path.is_file() and self._should_watch(path):
                        files[str(path)] = self._get_hash(path)
        
        return files
    
    def _check_changes(self):
        """Check for file changes"""
        current = self._scan_files()
        
        # Check for new and modified files
        for path, new_hash in current.items():
            old_hash = self.file_hashes.get(path)
            
            if old_hash is None:
                # New file
                event = WatchEvent(
                    path=Path(path),
                    event_type='created',
                    new_hash=new_hash
                )
                self._trigger_event(event)
            elif old_hash != new_hash:
                # Modified file
                event = WatchEvent(
                    path=Path(path),
                    event_type='modified',
                    old_hash=old_hash,
                    new_hash=new_hash
                )
                self._trigger_event(event)
        
        # Check for deleted files
        for path in set(self.file_hashes.keys()) - set(current.keys()):
            event = WatchEvent(
                path=Path(path),
                event_type='deleted',
                old_hash=self.file_hashes[path]
            )
            self._trigger_event(event)
        
        self.file_hashes = current
    
    def _trigger_event(self, event: WatchEvent):
        """Trigger event handlers"""
        self.events.append(event)
        
        # Wildcard handlers
        for handler in self.handlers.get('*', []):
            self.executor.submit(handler, event)
        
        # Specific handlers
        for handler in self.handlers.get(event.event_type, []):
            self.executor.submit(handler, event)
    
    def start(self, blocking: bool = False):
        """Start watching"""
        self._running = True
        
        # Initial scan
        self.file_hashes = self._scan_files()
        print(f"🔍 Watching {len(self.file_hashes)} files...")
        
        def watch_loop():
            while self._running:
                try:
                    self._check_changes()
                except Exception as e:
                    print(f"⚠️ Watch error: {e}")
                time.sleep(self.config.poll_interval)
        
        if blocking:
            watch_loop()
        else:
            self._thread = threading.Thread(target=watch_loop, daemon=True)
            self._thread.start()
        
        return self
    
    def stop(self):
        """Stop watching"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("🛑 Watcher stopped")
    
    def get_recent_events(self, limit: int = 10) -> list[WatchEvent]:
        """Get recent events"""
        return self.events[-limit:]


# ═══════════════════════════════════════════════════════════════════════════
# PRE-BUILT HANDLERS
# ═══════════════════════════════════════════════════════════════════════════

def log_handler(event: WatchEvent):
    """Simple logging handler"""
    emoji = {'created': '✨', 'modified': '📝', 'deleted': '🗑️'}.get(event.event_type, '📌')
    print(f"{emoji} [{event.event_type.upper()}] {event.path.name}")


def python_lint_handler(event: WatchEvent):
    """Auto-lint Python files"""
    if event.path.suffix != '.py' or event.event_type == 'deleted':
        return
    
    import subprocess
    result = subprocess.run(
        ['python3', '-m', 'py_compile', str(event.path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ {event.path.name} syntax OK")
    else:
        print(f"❌ {event.path.name} has errors:")
        print(result.stderr)


def format_handler(event: WatchEvent):
    """Auto-format Python files with black"""
    if event.path.suffix != '.py' or event.event_type == 'deleted':
        return
    
    import subprocess
    try:
        subprocess.run(
            ['black', '--quiet', str(event.path)],
            capture_output=True,
            timeout=10
        )
        print(f"🎨 Formatted {event.path.name}")
    except:
        pass


def ai_review_handler(event: WatchEvent):
    """AI-powered code review on changes"""
    if event.path.suffix != '.py' or event.event_type == 'deleted':
        return
    
    try:
        from .turbo_dispatcher import dispatch
        
        content = event.path.read_text()[:2000]
        result = dispatch("ask", f"Quick review this Python code change:\n```python\n{content}\n```", "Claude")
        
        if "response" in result:
            print(f"🤖 AI Review for {event.path.name}:")
            print(result["response"][:300])
    except:
        pass


# Factory function
def create_watcher(*paths, **options) -> RealtimeWatcher:
    """Create a configured watcher"""
    config = WatchConfig(
        paths=[Path(p) for p in paths] if paths else [Path('.')],
        extensions=options.get('extensions', ['.py', '.js', '.ts']),
        poll_interval=options.get('interval', 1.0)
    )
    
    watcher = RealtimeWatcher(config)
    
    # Add default log handler
    watcher.on('*', log_handler)
    
    # Add lint handler for Python
    if options.get('lint', True):
        watcher.on('modified', python_lint_handler)
    
    return watcher


__all__ = [
    'WatchEvent', 'WatchConfig', 'RealtimeWatcher', 'create_watcher',
    'log_handler', 'python_lint_handler', 'format_handler', 'ai_review_handler'
]


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              REALTIME WATCHER v1.0                           ║")
    print("║              GORUNFREE FILE MONITORING                       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Watch current directory
    watcher = create_watcher('.', extensions=['.py'], lint=True)
    
    print("Press Ctrl+C to stop...")
    try:
        watcher.start(blocking=True)
    except KeyboardInterrupt:
        watcher.stop()

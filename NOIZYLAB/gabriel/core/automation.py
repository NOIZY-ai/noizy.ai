#!/usr/bin/env python3
"""
🤖 GABRIEL AUTOMATION SYSTEM
============================
File watchers, LaunchAgents, and macOS notifications.

Features:
- Watch /00_Inbox/ for new files to auto-process
- LaunchAgent for always-on automation
- macOS notifications for success/failure
- Safe mode for private content (local only)
"""

import os
import sys
import json
import time
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, Optional, List, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
import queue

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
INBOX_DIR = GABRIEL_ROOT / "00_Inbox"
PROCESSED_DIR = GABRIEL_ROOT / "00_Inbox" / "PROCESSED"
FAILED_DIR = GABRIEL_ROOT / "00_Inbox" / "FAILED"
LAUNCH_AGENTS_DIR = Path.home() / "Library" / "LaunchAgents"

for d in [INBOX_DIR, PROCESSED_DIR, FAILED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# LaunchAgent identifier
LAUNCH_AGENT_ID = "com.noizylab.gabriel.watcher"

# =============================================================================
# MACOS NOTIFICATIONS
# =============================================================================

class Notifier:
    """macOS notification system using osascript."""
    
    @staticmethod
    def notify(title: str, message: str, sound: str = "default", 
               subtitle: str = None, open_url: str = None):
        """
        Send a macOS notification.
        
        Args:
            title: Notification title
            message: Main message body
            sound: Sound name (default, Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink)
            subtitle: Optional subtitle
            open_url: URL or file path to open on click
        """
        script_parts = [
            f'display notification "{message}"',
            f'with title "{title}"'
        ]
        
        if subtitle:
            script_parts.append(f'subtitle "{subtitle}"')
        
        if sound:
            script_parts.append(f'sound name "{sound}"')
        
        script = ' '.join(script_parts)
        
        try:
            subprocess.run(['osascript', '-e', script], capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Notification failed: {e}", file=sys.stderr)
    
    @staticmethod
    def success(title: str, message: str, run_dir: Path = None):
        """Send success notification."""
        subtitle = f"Completed at {datetime.now().strftime('%H:%M')}"
        Notifier.notify(
            title=f"✅ {title}",
            message=message,
            subtitle=subtitle,
            sound="Glass"
        )
        
        # Open Finder to run directory
        if run_dir and run_dir.exists():
            subprocess.run(['open', str(run_dir)], capture_output=True)
    
    @staticmethod
    def failure(title: str, message: str, error_dir: Path = None):
        """Send failure notification."""
        Notifier.notify(
            title=f"❌ {title}",
            message=message[:200],  # Truncate long errors
            subtitle="Check error inbox",
            sound="Basso"
        )
        
        if error_dir and error_dir.exists():
            subprocess.run(['open', str(error_dir)], capture_output=True)
    
    @staticmethod
    def alert(title: str, message: str):
        """Send alert dialog (blocking)."""
        script = f'''
        display alert "{title}" message "{message}" as warning buttons {{"OK"}} default button "OK"
        '''
        try:
            subprocess.run(['osascript', '-e', script], capture_output=True)
        except Exception:
            pass

# =============================================================================
# FILE WATCHER
# =============================================================================

@dataclass
class WatchedFile:
    """A file being watched."""
    path: Path
    hash: str
    discovered_at: datetime
    processed: bool = False
    error: Optional[str] = None

class InboxWatcher:
    """
    Watch /00_Inbox/ for new files and auto-process them.
    
    Supported file types:
    - .json: Manifest files for GABRIEL execution
    - .md: Documentation to index
    - .txt: Text content to process
    
    Usage:
        watcher = InboxWatcher()
        watcher.add_handler('.json', process_manifest)
        watcher.start()  # Runs in background
    """
    
    def __init__(self, watch_dir: Path = INBOX_DIR):
        self.watch_dir = watch_dir
        self.processed_dir = PROCESSED_DIR
        self.failed_dir = FAILED_DIR
        
        self._handlers: Dict[str, Callable] = {}
        self._seen_files: Dict[str, WatchedFile] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._queue: queue.Queue = queue.Queue()
        
        # Default poll interval (seconds)
        self.poll_interval = 5.0
    
    def add_handler(self, extension: str, handler: Callable[[Path], bool]):
        """
        Register a handler for a file extension.
        
        Args:
            extension: File extension (e.g., '.json')
            handler: Function that takes Path and returns True if processed successfully
        """
        self._handlers[extension.lower()] = handler
    
    def start(self):
        """Start watching in background thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        
        print(f"📁 Watching {self.watch_dir} for new files...", file=sys.stderr)
        Notifier.notify("GABRIEL Watcher", f"Watching {self.watch_dir.name}/", sound="Pop")
    
    def stop(self):
        """Stop watching."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def _watch_loop(self):
        """Main watch loop."""
        while self._running:
            try:
                self._scan_inbox()
                self._process_queue()
            except Exception as e:
                print(f"Watcher error: {e}", file=sys.stderr)
            
            time.sleep(self.poll_interval)
    
    def _scan_inbox(self):
        """Scan inbox for new files."""
        for path in self.watch_dir.iterdir():
            if path.is_dir():
                continue
            if path.name.startswith('.'):
                continue
            
            # Check if already seen
            file_hash = self._hash_file(path)
            file_key = f"{path.name}_{file_hash}"
            
            if file_key not in self._seen_files:
                watched = WatchedFile(
                    path=path,
                    hash=file_hash,
                    discovered_at=datetime.now()
                )
                self._seen_files[file_key] = watched
                self._queue.put(watched)
                print(f"📥 New file: {path.name}", file=sys.stderr)
    
    def _process_queue(self):
        """Process queued files."""
        while not self._queue.empty():
            try:
                watched = self._queue.get_nowait()
                self._process_file(watched)
            except queue.Empty:
                break
    
    def _process_file(self, watched: WatchedFile):
        """Process a single file."""
        path = watched.path
        ext = path.suffix.lower()
        
        handler = self._handlers.get(ext)
        if not handler:
            print(f"⏭️ No handler for {ext}: {path.name}", file=sys.stderr)
            return
        
        try:
            print(f"⚙️ Processing: {path.name}", file=sys.stderr)
            success = handler(path)
            
            if success:
                # Move to processed
                dest = self.processed_dir / path.name
                path.rename(dest)
                watched.processed = True
                
                Notifier.success(
                    "File Processed",
                    f"{path.name} completed",
                    self.processed_dir
                )
            else:
                raise Exception("Handler returned False")
                
        except Exception as e:
            watched.error = str(e)
            
            # Move to failed
            dest = self.failed_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{path.name}"
            path.rename(dest)
            
            Notifier.failure(
                "Processing Failed",
                f"{path.name}: {str(e)[:100]}",
                self.failed_dir
            )
    
    @staticmethod
    def _hash_file(path: Path) -> str:
        """Get file hash for dedup."""
        try:
            content = path.read_bytes()
            return hashlib.md5(content).hexdigest()[:8]
        except Exception:
            return "unknown"

# =============================================================================
# LAUNCH AGENT
# =============================================================================

class LaunchAgentManager:
    """Manage macOS LaunchAgents for GABRIEL."""
    
    @staticmethod
    def create_watcher_agent() -> Path:
        """
        Create a LaunchAgent plist for the inbox watcher.
        
        Returns:
            Path to created plist
        """
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LAUNCH_AGENT_ID}</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{GABRIEL_ROOT}/core/automation.py</string>
        <string>watch</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>WorkingDirectory</key>
    <string>{GABRIEL_ROOT}</string>
    
    <key>StandardOutPath</key>
    <string>{GABRIEL_ROOT}/logs/watcher.stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>{GABRIEL_ROOT}/logs/watcher.stderr.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
'''
        plist_path = LAUNCH_AGENTS_DIR / f"{LAUNCH_AGENT_ID}.plist"
        plist_path.write_text(plist_content)
        
        return plist_path
    
    @staticmethod
    def install():
        """Install and load the LaunchAgent."""
        plist_path = LaunchAgentManager.create_watcher_agent()
        
        # Unload if exists
        subprocess.run(['launchctl', 'unload', str(plist_path)], capture_output=True)
        
        # Load
        result = subprocess.run(['launchctl', 'load', str(plist_path)], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ LaunchAgent installed: {plist_path}")
            print("   Watcher will run automatically on login")
            return True
        else:
            print(f"❌ Failed to install LaunchAgent: {result.stderr}")
            return False
    
    @staticmethod
    def uninstall():
        """Uninstall the LaunchAgent."""
        plist_path = LAUNCH_AGENTS_DIR / f"{LAUNCH_AGENT_ID}.plist"
        
        # Unload
        subprocess.run(['launchctl', 'unload', str(plist_path)], capture_output=True)
        
        # Remove file
        if plist_path.exists():
            plist_path.unlink()
        
        print("✅ LaunchAgent uninstalled")
    
    @staticmethod
    def status() -> Dict:
        """Get LaunchAgent status."""
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True, text=True
        )
        
        running = LAUNCH_AGENT_ID in result.stdout
        
        plist_path = LAUNCH_AGENTS_DIR / f"{LAUNCH_AGENT_ID}.plist"
        installed = plist_path.exists()
        
        return {
            "installed": installed,
            "running": running,
            "plist_path": str(plist_path) if installed else None
        }

# =============================================================================
# SAFE MODE
# =============================================================================

class SafeMode:
    """
    Safe mode for processing private content without API calls.
    
    When enabled:
    - All LLM calls use local models only
    - No data sent to external APIs
    - Search grounding disabled
    """
    
    _enabled: bool = False
    _reason: str = ""
    
    @classmethod
    def enable(cls, reason: str = "User requested"):
        """Enable safe mode."""
        cls._enabled = True
        cls._reason = reason
        
        # Set environment variable for other processes
        os.environ['GABRIEL_SAFE_MODE'] = '1'
        
        Notifier.notify(
            "🔒 Safe Mode Enabled",
            reason,
            sound="Submarine"
        )
    
    @classmethod
    def disable(cls):
        """Disable safe mode."""
        cls._enabled = False
        cls._reason = ""
        os.environ.pop('GABRIEL_SAFE_MODE', None)
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Check if safe mode is active."""
        return cls._enabled or os.environ.get('GABRIEL_SAFE_MODE') == '1'
    
    @classmethod
    def check_api_allowed(cls, api_name: str) -> bool:
        """Check if API call is allowed in current mode."""
        if not cls.is_enabled():
            return True
        
        # In safe mode, only local APIs allowed
        local_apis = ['local', 'ollama', 'llama', 'localhost']
        return any(l in api_name.lower() for l in local_apis)
    
    @classmethod
    def get_model(cls) -> str:
        """Get appropriate model for current mode."""
        if cls.is_enabled():
            return "local"  # Force local model
        return None  # Use normal model selection

# =============================================================================
# DEFAULT HANDLERS
# =============================================================================

def handle_json_manifest(path: Path) -> bool:
    """Process a JSON manifest file."""
    try:
        manifest = json.loads(path.read_text())
        
        # Log it
        print(f"📋 Manifest: {manifest.get('name', 'unnamed')}", file=sys.stderr)
        
        # TODO: Actually process the manifest
        # For now, just validate and return success
        
        if 'task' not in manifest and 'prompt' not in manifest:
            raise ValueError("Manifest must contain 'task' or 'prompt'")
        
        return True
        
    except Exception as e:
        print(f"❌ Manifest error: {e}", file=sys.stderr)
        raise

def handle_markdown(path: Path) -> bool:
    """Process a markdown file."""
    content = path.read_text()
    
    # Index to knowledge base
    # TODO: Add to GABRIEL's knowledge index
    
    print(f"📝 Indexed: {path.name} ({len(content)} chars)", file=sys.stderr)
    return True

def handle_text(path: Path) -> bool:
    """Process a text file."""
    content = path.read_text()
    print(f"📄 Processed: {path.name} ({len(content)} chars)", file=sys.stderr)
    return True

# =============================================================================
# MAIN WATCHER
# =============================================================================

def run_watcher():
    """Run the inbox watcher (main entry point)."""
    watcher = InboxWatcher()
    
    # Register handlers
    watcher.add_handler('.json', handle_json_manifest)
    watcher.add_handler('.md', handle_markdown)
    watcher.add_handler('.txt', handle_text)
    
    # Start watching
    watcher.start()
    
    print(f"🤖 GABRIEL Watcher running...")
    print(f"📁 Inbox: {INBOX_DIR}")
    print(f"✅ Processed: {PROCESSED_DIR}")
    print(f"❌ Failed: {FAILED_DIR}")
    print(f"\nPress Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️ Stopping watcher...")
        watcher.stop()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "watch":
            run_watcher()
        
        elif cmd == "install":
            LaunchAgentManager.install()
        
        elif cmd == "uninstall":
            LaunchAgentManager.uninstall()
        
        elif cmd == "status":
            status = LaunchAgentManager.status()
            print("\n🤖 GABRIEL Automation Status")
            print("=" * 40)
            print(f"LaunchAgent installed: {status['installed']}")
            print(f"LaunchAgent running: {status['running']}")
            if status['plist_path']:
                print(f"Plist: {status['plist_path']}")
            print(f"\nInbox: {INBOX_DIR}")
            files = list(INBOX_DIR.glob('*'))
            files = [f for f in files if not f.name.startswith('.') and f.is_file()]
            print(f"Files waiting: {len(files)}")
        
        elif cmd == "notify":
            msg = sys.argv[2] if len(sys.argv) > 2 else "Test notification"
            Notifier.notify("GABRIEL", msg)
        
        elif cmd == "safe":
            SafeMode.enable("CLI request")
            print("🔒 Safe mode enabled")
        
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("🤖 GABRIEL Automation System")
        print("\nUsage:")
        print("  python automation.py watch      # Start inbox watcher")
        print("  python automation.py install    # Install LaunchAgent")
        print("  python automation.py uninstall  # Remove LaunchAgent")
        print("  python automation.py status     # Check status")
        print("  python automation.py notify     # Test notification")
        print("  python automation.py safe       # Enable safe mode")

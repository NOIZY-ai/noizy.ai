#!/usr/bin/env python3
"""
🧠 GABRIEL AUTONOMOUS AGENT
Proactive monitoring + MCP tool integration

This runs alongside the MCP server to provide:
- Continuous codebase monitoring
- Proactive insights and alerts  
- Background task execution
- Event-driven workflows
"""

import os
import sys
import json
import time
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import threading
import queue

# Import NOIZY Collective Knowledge
try:
    from noizy_collective import get_knowledge, NOIZYCollective, Qwen3Client, LocalLLMRunner
    COLLECTIVE_AVAILABLE = True
except ImportError:
    COLLECTIVE_AVAILABLE = False

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
NOIZYLAB_ROOT = Path("/Users/m2ultra/NOIZYLAB")
WATCH_PATHS = [
    NOIZYLAB_ROOT / "GABRIEL",
    NOIZYLAB_ROOT / "MC96",
    NOIZYLAB_ROOT / "AGENTS",
]


@dataclass
class Event:
    type: str
    data: Dict
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 0


@dataclass
class Task:
    name: str
    func: Callable
    interval: int
    last_run: Optional[datetime] = None
    enabled: bool = True


class FileWatcher:
    """Watch filesystem for changes"""
    
    def __init__(self, paths: List[Path]):
        self.paths = paths
        self.file_hashes: Dict[str, str] = {}
        self.changes: List[Dict] = []
    
    def compute_hash(self, filepath: Path) -> Optional[str]:
        try:
            return hashlib.md5(filepath.read_bytes()).hexdigest()
        except:
            return None
    
    def scan(self) -> List[Dict]:
        """Scan for changes since last check"""
        changes = []
        skip_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.venv'}
        
        for watch_path in self.paths:
            if not watch_path.exists():
                continue
                
            for root, dirs, files in os.walk(watch_path):
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    filepath = Path(root) / file
                    current_hash = self.compute_hash(filepath)
                    
                    if current_hash is None:
                        continue
                    
                    str_path = str(filepath)
                    
                    if str_path in self.file_hashes:
                        if self.file_hashes[str_path] != current_hash:
                            changes.append({
                                'type': 'modified',
                                'path': str_path,
                                'time': datetime.now().isoformat(),
                            })
                    else:
                        changes.append({
                            'type': 'new',
                            'path': str_path,
                            'time': datetime.now().isoformat(),
                        })
                    
                    self.file_hashes[str_path] = current_hash
        
        self.changes.extend(changes)
        self.changes = self.changes[-100:]
        
        return changes


class InsightEngine:
    """Generate proactive insights"""
    
    def __init__(self):
        self.insights: List[Dict] = []
        self.stats_history: List[Dict] = []
    
    def analyze_changes(self, changes: List[Dict]) -> List[Dict]:
        """Generate insights from file changes"""
        insights = []
        
        if len(changes) > 10:
            insights.append({
                'type': 'alert',
                'level': 'warning',
                'message': f'High activity: {len(changes)} files changed',
                'suggestion': 'Consider committing changes',
            })
        
        py_changes = [c for c in changes if c['path'].endswith('.py')]
        if len(py_changes) > 5:
            insights.append({
                'type': 'info',
                'level': 'info', 
                'message': f'{len(py_changes)} Python files modified',
                'suggestion': 'Run tests to verify changes',
            })
        
        return insights
    
    def analyze_codebase(self, stats: Dict) -> List[Dict]:
        """Generate insights from codebase stats"""
        insights = []
        
        if stats.get('total_lines', 0) > 100000:
            insights.append({
                'type': 'scale',
                'level': 'info',
                'message': f"Large codebase: {stats['total_lines']:,} lines",
            })
        
        hot_files = stats.get('hot_files', [])
        complex_files = [f for f in hot_files if f.get('complexity', 0) > 100]
        if complex_files:
            insights.append({
                'type': 'complexity',
                'level': 'warning',
                'message': f'{len(complex_files)} high-complexity files detected',
                'files': [f['path'] for f in complex_files[:5]],
            })
        
        return insights


class TaskScheduler:
    """Schedule and run background tasks"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.running = False
        self.event_queue: queue.Queue = queue.Queue()
    
    def register(self, name: str, func: Callable, interval: int):
        """Register a recurring task"""
        self.tasks[name] = Task(name=name, func=func, interval=interval)
    
    def should_run(self, task: Task) -> bool:
        if not task.enabled:
            return False
        if task.last_run is None:
            return True
        return datetime.now() - task.last_run > timedelta(seconds=task.interval)
    
    async def run_task(self, task: Task):
        """Execute a single task"""
        try:
            if asyncio.iscoroutinefunction(task.func):
                await task.func()
            else:
                task.func()
            task.last_run = datetime.now()
        except Exception as e:
            self.event_queue.put(Event(
                type='task_error',
                data={'task': task.name, 'error': str(e)},
                priority=1
            ))
    
    async def run_loop(self):
        """Main scheduler loop"""
        self.running = True
        
        while self.running:
            for task in self.tasks.values():
                if self.should_run(task):
                    await self.run_task(task)
            
            await asyncio.sleep(1)
    
    def stop(self):
        self.running = False


class GabrielAgent:
    """Main autonomous agent with NOIZY Collective integration"""
    
    def __init__(self):
        self.watcher = FileWatcher(WATCH_PATHS)
        self.insights = InsightEngine()
        self.scheduler = TaskScheduler()
        self.state = {
            'started': None,
            'last_scan': None,
            'total_changes': 0,
            'total_insights': 0,
        }
        self.running = False
        
        # NOIZY Collective Integration
        self.knowledge = get_knowledge() if COLLECTIVE_AVAILABLE else None
        self.collective = NOIZYCollective() if COLLECTIVE_AVAILABLE else None
        self.qwen = Qwen3Client() if COLLECTIVE_AVAILABLE else None
        self.local_llm = LocalLLMRunner() if COLLECTIVE_AVAILABLE else None
        
        self.scheduler.register('file_watch', self.watch_files, interval=30)
        self.scheduler.register('health_check', self.health_check, interval=60)
        self.scheduler.register('cleanup', self.cleanup, interval=300)
    
    # ========================
    # NOIZY COLLECTIVE METHODS
    # ========================
    
    def get_model_for_task(self, task: str) -> str:
        """Get best model for a specific task"""
        if self.collective:
            return self.collective.recommend(task)["model"]
        return "gpt-4o"
    
    def query_local_llm(self, prompt: str, thinking: bool = True) -> dict:
        """Query local LLM (Qwen3 with thinking mode)"""
        if self.qwen:
            return self.qwen.chat(prompt, thinking=thinking)
        return {"error": "Collective not available", "success": False}
    
    def list_available_models(self) -> List[dict]:
        """List all available models in the collective"""
        if self.collective:
            return self.collective.list_all()
        return []
    
    def get_collective_stats(self) -> dict:
        """Get NOIZY Collective statistics"""
        if self.knowledge:
            return self.knowledge.get_stats()
        return {"error": "Collective not available"}
    
    def auto_select_model(self, requirements: dict) -> str:
        """Auto-select best model based on requirements"""
        if self.collective:
            return self.collective.auto_select(requirements)
        return "gpt-4o"
    
    def watch_files(self):
        """Periodic file watching task"""
        changes = self.watcher.scan()
        
        if changes:
            self.state['total_changes'] += len(changes)
            self.state['last_scan'] = datetime.now().isoformat()
            
            insights = self.insights.analyze_changes(changes)
            if insights:
                self.state['total_insights'] += len(insights)
                self.log_insights(insights)
            
            self.save_state()
    
    def health_check(self):
        """System health check"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'uptime': str(datetime.now() - datetime.fromisoformat(self.state['started'])) if self.state['started'] else None,
            'changes_detected': self.state['total_changes'],
            'insights_generated': self.state['total_insights'],
            'watched_paths': [str(p) for p in WATCH_PATHS],
        }
        
        status_file = GABRIEL_ROOT / "agent_status.json"
        status_file.write_text(json.dumps(status, indent=2))
    
    def cleanup(self):
        """Cleanup old data"""
        self.watcher.changes = self.watcher.changes[-50:]
        self.insights.insights = self.insights.insights[-50:]
    
    def log_insights(self, insights: List[Dict]):
        """Log insights to file"""
        log_file = GABRIEL_ROOT / "insights.log"
        
        with open(log_file, 'a') as f:
            for insight in insights:
                f.write(f"[{datetime.now().isoformat()}] {insight['level'].upper()}: {insight['message']}\n")
    
    def save_state(self):
        """Persist agent state"""
        state_file = GABRIEL_ROOT / "agent_state.json"
        state_file.write_text(json.dumps(self.state, indent=2, default=str))
    
    def load_state(self):
        """Load persisted state"""
        state_file = GABRIEL_ROOT / "agent_state.json"
        if state_file.exists():
            try:
                self.state = json.loads(state_file.read_text())
            except:
                pass
    
    async def start(self):
        """Start the agent"""
        print("🧠 GABRIEL AGENT STARTING...")
        print(f"   Watching: {len(WATCH_PATHS)} paths")
        print(f"   Tasks: {len(self.scheduler.tasks)}")
        
        self.load_state()
        self.state['started'] = datetime.now().isoformat()
        self.running = True
        
        self.watcher.scan()
        
        print("✅ GABRIEL AGENT ONLINE\n")
        
        try:
            await self.scheduler.run_loop()
        except KeyboardInterrupt:
            print("\n🛑 GABRIEL AGENT STOPPING...")
            self.scheduler.stop()
            self.save_state()
            print("✅ State saved. Goodbye.")
    
    def status(self) -> Dict:
        """Get current agent status"""
        return {
            'running': self.running,
            'state': self.state,
            'tasks': {name: {'enabled': t.enabled, 'last_run': t.last_run.isoformat() if t.last_run else None} 
                     for name, t in self.scheduler.tasks.items()},
            'recent_changes': self.watcher.changes[-10:],
        }


async def main():
    agent = GabrielAgent()
    await agent.start()


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🧠 GABRIEL AUTONOMOUS AGENT                                 ║
║                                                               ║
║   Proactive monitoring & intelligence                         ║
║   Press Ctrl+C to stop                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
    asyncio.run(main())

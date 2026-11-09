#!/usr/bin/env python3
"""
📊 GABRIEL OBSERVABILITY SYSTEM
===============================
Structured logging, run summaries, and error inbox.

Features:
- JSONL event logs (queryable, parseable)
- Automatic run summaries with artifacts index
- Error inbox for failed runs
- Real-time log streaming
- Log aggregation and search
"""

import os
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Dict, Optional, List, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from contextlib import contextmanager
import threading
import queue

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
LOGS_DIR = GABRIEL_ROOT / "logs"
EVENTS_DIR = LOGS_DIR / "events"
ERROR_INBOX = GABRIEL_ROOT / "00_Inbox" / "FAILED"

for d in [LOGS_DIR, EVENTS_DIR, ERROR_INBOX]:
    d.mkdir(parents=True, exist_ok=True)

# =============================================================================
# EVENT TYPES
# =============================================================================

class EventType(Enum):
    """Standard event types for structured logging."""
    # Lifecycle
    RUN_STARTED = "run_started"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"
    
    # Routing
    ROUTER_CALLED = "router_called"
    ROUTER_DECISION = "router_decision"
    
    # Execution
    EXECUTOR_STARTED = "executor_started"
    EXECUTOR_COMPLETED = "executor_completed"
    EXECUTOR_FAILED = "executor_failed"
    
    # Verification
    VERIFIER_STARTED = "verifier_started"
    VERIFIER_PASSED = "verifier_passed"
    VERIFIER_FAILED = "verifier_failed"
    
    # Model calls
    MODEL_CALL_STARTED = "model_call_started"
    MODEL_CALL_COMPLETED = "model_call_completed"
    MODEL_CALL_FAILED = "model_call_failed"
    MODEL_FALLBACK = "model_fallback"
    
    # Budget
    BUDGET_CHECK = "budget_check"
    BUDGET_WARNING = "budget_warning"
    BUDGET_EXCEEDED = "budget_exceeded"
    
    # Artifacts
    ARTIFACT_CREATED = "artifact_created"
    ARTIFACT_DELETED = "artifact_deleted"
    
    # System
    SYSTEM_ERROR = "system_error"
    RATE_LIMITED = "rate_limited"
    RETRY_ATTEMPT = "retry_attempt"
    
    # Custom
    CUSTOM = "custom"

class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# =============================================================================
# STRUCTURED EVENT
# =============================================================================

@dataclass
class Event:
    """Structured log event."""
    timestamp: str
    event_type: str
    level: str
    
    # Context
    run_id: Optional[str] = None
    agent: Optional[str] = None
    step: Optional[str] = None
    
    # Event data
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Performance
    duration_ms: Optional[float] = None
    tokens: Optional[int] = None
    cost_cents: Optional[float] = None
    
    # Error info
    error: Optional[str] = None
    error_trace: Optional[str] = None
    
    def to_jsonl(self) -> str:
        """Convert to JSONL format."""
        return json.dumps(asdict(self), default=str)
    
    @classmethod
    def from_jsonl(cls, line: str) -> 'Event':
        """Parse from JSONL."""
        data = json.loads(line)
        return cls(**data)

# =============================================================================
# LOGGER
# =============================================================================

class StructuredLogger:
    """
    Structured JSONL logger for GABRIEL.
    
    Usage:
        log = StructuredLogger("my-run-123")
        log.info("Starting process", {"items": 10})
        log.event(EventType.EXECUTOR_STARTED, agent="writer")
        log.error("Something failed", error=e)
    """
    
    def __init__(self, run_id: str = None, agent: str = None):
        self.run_id = run_id or f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent = agent
        
        # File paths
        self.log_file = LOGS_DIR / f"{self.run_id}.jsonl"
        self.summary_file = LOGS_DIR / f"{self.run_id}_summary.json"
        
        # Daily event log
        today = datetime.now().strftime("%Y-%m-%d")
        self.events_file = EVENTS_DIR / f"{today}.jsonl"
        
        # Stats
        self._event_counts: Dict[str, int] = {}
        self._errors: List[Event] = []
        self._start_time = time.time()
        
        # Async queue for non-blocking writes
        self._queue: queue.Queue = queue.Queue()
        self._writer_thread: Optional[threading.Thread] = None
        self._running = True
        
        self._start_writer()
    
    def _start_writer(self):
        """Start background writer thread."""
        def writer():
            while self._running or not self._queue.empty():
                try:
                    event = self._queue.get(timeout=0.1)
                    self._write_event(event)
                except queue.Empty:
                    continue
        
        self._writer_thread = threading.Thread(target=writer, daemon=True)
        self._writer_thread.start()
    
    def _write_event(self, event: Event):
        """Write event to log files."""
        line = event.to_jsonl() + "\n"
        
        # Write to run log
        with open(self.log_file, 'a') as f:
            f.write(line)
        
        # Write to daily events
        with open(self.events_file, 'a') as f:
            f.write(line)
    
    def _create_event(self, event_type: EventType, level: LogLevel,
                      message: str = "", data: Dict = None, **kwargs) -> Event:
        """Create an event."""
        event = Event(
            timestamp=datetime.now().isoformat(),
            event_type=event_type.value,
            level=level.value,
            run_id=self.run_id,
            agent=kwargs.pop('agent', self.agent),
            message=message,
            data=data or {},
            **kwargs
        )
        
        # Track stats
        self._event_counts[event_type.value] = self._event_counts.get(event_type.value, 0) + 1
        
        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            self._errors.append(event)
        
        return event
    
    def log(self, event: Event):
        """Queue an event for logging."""
        self._queue.put(event)
        
        # Also print to stderr for real-time feedback
        emoji = {"DEBUG": "🔍", "INFO": "ℹ️", "WARN": "⚠️", "ERROR": "❌", "CRITICAL": "🔥"}.get(event.level, "📝")
        print(f"{emoji} [{event.event_type}] {event.message}", file=sys.stderr)
    
    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
    
    def debug(self, message: str, data: Dict = None, **kwargs):
        """Log debug message."""
        event = self._create_event(EventType.CUSTOM, LogLevel.DEBUG, message, data, **kwargs)
        self.log(event)
    
    def info(self, message: str, data: Dict = None, **kwargs):
        """Log info message."""
        event = self._create_event(EventType.CUSTOM, LogLevel.INFO, message, data, **kwargs)
        self.log(event)
    
    def warn(self, message: str, data: Dict = None, **kwargs):
        """Log warning."""
        event = self._create_event(EventType.CUSTOM, LogLevel.WARN, message, data, **kwargs)
        self.log(event)
    
    def error(self, message: str, error: Exception = None, data: Dict = None, **kwargs):
        """Log error."""
        event = self._create_event(
            EventType.SYSTEM_ERROR, LogLevel.ERROR, message, data,
            error=str(error) if error else None,
            error_trace=traceback.format_exc() if error else None,
            **kwargs
        )
        self.log(event)
    
    def event(self, event_type: EventType, level: LogLevel = LogLevel.INFO,
              message: str = "", data: Dict = None, **kwargs):
        """Log a structured event."""
        event = self._create_event(event_type, level, message, data, **kwargs)
        self.log(event)
    
    # -------------------------------------------------------------------------
    # Timing helpers
    # -------------------------------------------------------------------------
    
    @contextmanager
    def timed(self, name: str, event_type: EventType = EventType.CUSTOM):
        """Context manager for timing operations."""
        start = time.time()
        try:
            yield
            duration_ms = (time.time() - start) * 1000
            self.event(event_type, message=f"{name} completed", 
                      data={"duration_ms": duration_ms}, duration_ms=duration_ms)
        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self.error(f"{name} failed", error=e, duration_ms=duration_ms)
            raise
    
    # -------------------------------------------------------------------------
    # Summary generation
    # -------------------------------------------------------------------------
    
    def generate_summary(self) -> Dict:
        """Generate run summary."""
        duration = time.time() - self._start_time
        
        summary = {
            "run_id": self.run_id,
            "generated_at": datetime.now().isoformat(),
            "duration_secs": round(duration, 2),
            "event_counts": self._event_counts,
            "error_count": len(self._errors),
            "errors": [
                {"message": e.message, "error": e.error, "timestamp": e.timestamp}
                for e in self._errors[-10:]  # Last 10 errors
            ],
            "log_file": str(self.log_file),
            "status": "failed" if self._errors else "success"
        }
        
        # Save summary
        self.summary_file.write_text(json.dumps(summary, indent=2))
        
        return summary
    
    def close(self):
        """Close the logger and generate summary."""
        self._running = False
        if self._writer_thread:
            self._writer_thread.join(timeout=2.0)
        
        # Generate summary
        summary = self.generate_summary()
        
        # Copy to error inbox if failed
        if self._errors:
            self._copy_to_error_inbox()
        
        return summary
    
    def _copy_to_error_inbox(self):
        """Copy failed run to error inbox."""
        import shutil
        
        # Create error folder
        error_dir = ERROR_INBOX / f"{self.run_id}_{datetime.now().strftime('%H%M%S')}"
        error_dir.mkdir(exist_ok=True)
        
        # Copy log file
        if self.log_file.exists():
            shutil.copy(self.log_file, error_dir / "run.jsonl")
        
        # Copy summary
        if self.summary_file.exists():
            shutil.copy(self.summary_file, error_dir / "summary.json")
        
        # Write error extract
        error_extract = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "error_count": len(self._errors),
            "errors": [asdict(e) for e in self._errors]
        }
        (error_dir / "errors.json").write_text(json.dumps(error_extract, indent=2))

# =============================================================================
# LOG SEARCH / AGGREGATION
# =============================================================================

class LogAggregator:
    """Search and aggregate logs."""
    
    @staticmethod
    def search_events(query: str = None, event_type: str = None,
                      level: str = None, since: datetime = None,
                      limit: int = 100) -> List[Event]:
        """Search events across all logs."""
        events = []
        
        for log_file in sorted(EVENTS_DIR.glob("*.jsonl"), reverse=True):
            if len(events) >= limit:
                break
            
            try:
                with open(log_file) as f:
                    for line in f:
                        if len(events) >= limit:
                            break
                        
                        try:
                            event = Event.from_jsonl(line.strip())
                            
                            # Apply filters
                            if event_type and event.event_type != event_type:
                                continue
                            if level and event.level != level:
                                continue
                            if since and event.timestamp < since.isoformat():
                                continue
                            if query and query.lower() not in event.message.lower():
                                continue
                            
                            events.append(event)
                        except Exception:
                            continue
            except Exception:
                continue
        
        return events
    
    @staticmethod
    def get_error_summary(days: int = 7) -> Dict:
        """Get error summary for past N days."""
        since = datetime.now() - timedelta(days=days)
        errors = LogAggregator.search_events(level="ERROR", since=since, limit=1000)
        
        # Group by error type
        by_type: Dict[str, int] = {}
        by_day: Dict[str, int] = {}
        
        for e in errors:
            by_type[e.event_type] = by_type.get(e.event_type, 0) + 1
            day = e.timestamp[:10]
            by_day[day] = by_day.get(day, 0) + 1
        
        return {
            "total_errors": len(errors),
            "by_type": dict(sorted(by_type.items(), key=lambda x: -x[1])),
            "by_day": dict(sorted(by_day.items())),
            "recent": [
                {"message": e.message, "type": e.event_type, "time": e.timestamp}
                for e in errors[:10]
            ]
        }
    
    @staticmethod
    def get_run_timeline(run_id: str) -> List[Dict]:
        """Get event timeline for a run."""
        log_file = LOGS_DIR / f"{run_id}.jsonl"
        if not log_file.exists():
            return []
        
        events = []
        with open(log_file) as f:
            for line in f:
                try:
                    event = Event.from_jsonl(line.strip())
                    events.append({
                        "time": event.timestamp,
                        "type": event.event_type,
                        "message": event.message,
                        "level": event.level,
                        "duration_ms": event.duration_ms
                    })
                except Exception:
                    continue
        
        return events

# =============================================================================
# ARTIFACT INDEX
# =============================================================================

def generate_artifacts_index(run_dir: Path) -> Dict:
    """Generate artifacts/index.json for a run."""
    artifacts_dir = run_dir / "artifacts"
    if not artifacts_dir.exists():
        return {"artifacts": []}
    
    index = {
        "run_id": run_dir.name,
        "generated_at": datetime.now().isoformat(),
        "artifacts": []
    }
    
    for artifact in artifacts_dir.iterdir():
        if artifact.suffix == ".json" and artifact.name.endswith(".meta.json"):
            continue
        
        meta_file = artifact.with_suffix(artifact.suffix + ".meta.json")
        
        entry = {
            "name": artifact.name,
            "path": str(artifact),
            "size_bytes": artifact.stat().st_size,
            "modified": datetime.fromtimestamp(artifact.stat().st_mtime).isoformat()
        }
        
        # Add metadata if exists
        if meta_file.exists():
            try:
                entry["meta"] = json.loads(meta_file.read_text())
            except Exception:
                pass
        
        index["artifacts"].append(entry)
    
    # Save index
    index_file = artifacts_dir / "index.json"
    index_file.write_text(json.dumps(index, indent=2))
    
    return index

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

_logger: Optional[StructuredLogger] = None

def get_logger(run_id: str = None) -> StructuredLogger:
    """Get or create the global logger."""
    global _logger
    if _logger is None or (run_id and _logger.run_id != run_id):
        if _logger:
            _logger.close()
        _logger = StructuredLogger(run_id)
    return _logger

def log_event(event_type: EventType, message: str = "", **kwargs):
    """Quick event logging."""
    get_logger().event(event_type, message=message, **kwargs)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "errors":
            summary = LogAggregator.get_error_summary()
            print("\n❌ ERROR SUMMARY (Last 7 days)")
            print("=" * 50)
            print(f"Total errors: {summary['total_errors']}")
            print(f"\nBy type:")
            for t, c in summary['by_type'].items():
                print(f"  {t}: {c}")
            print(f"\nBy day:")
            for d, c in summary['by_day'].items():
                print(f"  {d}: {c}")
        
        elif cmd == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else None
            events = LogAggregator.search_events(query=query, limit=20)
            print(f"\n🔍 Search results: {len(events)} events")
            for e in events:
                print(f"  [{e.timestamp[:19]}] [{e.level}] {e.message[:60]}")
        
        elif cmd == "inbox":
            print(f"\n📥 ERROR INBOX: {ERROR_INBOX}")
            for d in sorted(ERROR_INBOX.iterdir())[-10:]:
                if d.is_dir():
                    print(f"  📁 {d.name}")
        
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("📊 GABRIEL Observability System")
        print("\nUsage:")
        print("  python observability.py errors   # View error summary")
        print("  python observability.py search   # Search events")
        print("  python observability.py inbox    # View error inbox")

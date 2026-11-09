import json
import time
import uuid
import threading
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List, Union, Callable
from pathlib import Path
from queue import Queue
import inspect
import traceback
import functools
import sys

from loguru import logger as loguru_logger
from database.MicroMongo import MongoClient


class LogFormatter:
    """Handles structured JSON formatting for logs"""

    @staticmethod
    def format_timestamp(epoch_time: float) -> Dict[str, Union[float, str]]:
        """Create dual timestamp format"""
        dt = datetime.fromtimestamp(epoch_time)

        # Create ordinal suffix for day
        day = dt.day
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

        human_readable = dt.strftime(f"%a, {day}{suffix} %b @ %H:%M:%S.%f")[:-4]

        return {"epoch": epoch_time, "human": human_readable}

    @staticmethod
    def extract_context() -> Dict[str, Any]:
        """Extract calling context automatically"""
        frame = inspect.currentframe()
        try:
            # Go up the stack to find the actual caller
            # Skip: extract_context -> format_log -> log_method -> actual_caller
            for _ in range(4):
                frame = frame.f_back
                if frame is None:
                    break

            if frame:
                return {
                    "function": frame.f_code.co_name,
                    "module": frame.f_globals.get("__name__", "unknown"),
                    "line": frame.f_lineno,
                    "file": frame.f_code.co_filename,
                }
        finally:
            del frame

        return {
            "function": "unknown",
            "module": "unknown",
            "line": 0,
            "file": "unknown",
        }

    @staticmethod
    def format_log(
        level: str,
        message: str,
        extra: Optional[Dict] = None,
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Format a complete log entry"""
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": LogFormatter.format_timestamp(time.time()),
            "level": level.upper(),
            "logger": "application",
            "message": str(message),
            "context": LogFormatter.extract_context(),
            "extra": extra or {},
            "trace_id": trace_id,
        }

        return log_entry


class DatabaseLogSink:
    """Handles async database storage for logs"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        self.db = None
        self.collection = None
        self.batch_queue = Queue()
        self.batch_size = config.get("batch_size", 100)
        self.enabled_levels = set(
            config.get("levels", ["INFO", "WARNING", "ERROR", "CRITICAL"])
        )
        self.worker_thread = None
        self.shutdown_event = threading.Event()

        if config.get("enabled", True):
            self._initialize_database()
            self._start_worker()

    def _initialize_database(self):
        """Initialize database connection"""
        try:
            db_path = self.config.get("path", "./logs/app_logs")
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

            self.client = MongoClient(db_path)
            self.db = self.client["logs"]
            self.collection = self.db["entries"]

            # Create indexes for common queries
            # Note: TinyDB doesn't have traditional indexes, but we can optimize by structure

        except Exception as e:
            print(f"Failed to initialize log database: {e}")
            self.client = None

    def _start_worker(self):
        """Start background worker thread for batch processing"""
        if self.client:
            self.worker_thread = threading.Thread(
                target=self._batch_worker, daemon=True
            )
            self.worker_thread.start()

    def _batch_worker(self):
        """Background worker that processes log batches"""
        batch = []

        while not self.shutdown_event.is_set():
            try:
                # Collect batch
                while len(batch) < self.batch_size:
                    try:
                        log_entry = self.batch_queue.get(timeout=1.0)
                        batch.append(log_entry)
                    except:
                        break  # Timeout or shutdown

                # Insert batch if we have entries
                if batch and self.collection:
                    try:
                        self.collection.insert_many(batch)
                        batch.clear()
                    except Exception as e:
                        print(f"Failed to insert log batch: {e}")
                        batch.clear()  # Clear to prevent memory buildup

            except Exception as e:
                print(f"Batch worker error: {e}")
                time.sleep(1)

    def write_log(self, log_entry: Dict[str, Any]):
        """Add log entry to batch queue"""
        if (
            self.client
            and log_entry["level"] in self.enabled_levels
            and not self.shutdown_event.is_set()
        ):
            try:
                self.batch_queue.put(log_entry, block=False)
            except:
                # Queue full, skip this log to prevent blocking
                pass

    def shutdown(self):
        """Graceful shutdown of database sink"""
        self.shutdown_event.set()

        # Process remaining logs in queue
        remaining_logs = []
        try:
            while True:
                remaining_logs.append(self.batch_queue.get_nowait())
        except:
            pass

        if remaining_logs and self.collection:
            try:
                self.collection.insert_many(remaining_logs)
            except Exception as e:
                print(f"Failed to insert remaining logs during shutdown: {e}")

        if self.worker_thread:
            self.worker_thread.join(timeout=5)


class StructuredLogger:
    """Main logger class that orchestrates file and database logging"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.trace_id = None

        # Initialize database sink
        self.db_sink = DatabaseLogSink(self.config.get("database", {}))

        # Configure loguru for file logging
        self._configure_file_logging()

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "database": {
                "enabled": True,
                "path": "./logs/app_logs",
                "batch_size": 100,
                "levels": ["INFO", "WARNING", "ERROR", "CRITICAL"],
            },
            "file": {
                "enabled": True,
                "path": "./logs/app.log",
                "rotation": "100 MB",
                "retention": "30 days",
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            },
            "format": {"include_trace": True, "auto_context": True},
        }

    def _configure_file_logging(self):
        """Configure loguru file logging"""
        file_config = self.config.get("file", {})

        if file_config.get("enabled", True):
            # Remove default handler
            loguru_logger.remove()

            # Add file handler
            log_path = file_config.get("path", "./logs/app.log")
            Path(log_path).parent.mkdir(parents=True, exist_ok=True)

            loguru_logger.add(
                log_path,
                rotation=file_config.get("rotation", "100 MB"),
                retention=file_config.get("retention", "30 days"),
                format=file_config.get(
                    "format",
                    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                ),
                level="DEBUG",
            )

            # Add console handler for development
            loguru_logger.add(
                lambda msg: print(msg, end=""),
                format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
                level="INFO",
            )

    def set_trace_id(self, trace_id: str):
        """Set correlation ID for request tracing"""
        self.trace_id = trace_id

    def clear_trace_id(self):
        """Clear the current trace ID"""
        self.trace_id = None

    def _log(self, level: str, message: str, **kwargs):
        """Internal logging method"""
        extra = kwargs.get("extra", {})

        # Create structured log entry
        log_entry = LogFormatter.format_log(
            level=level, message=message, extra=extra, trace_id=self.trace_id
        )

        # Send to database sink
        self.db_sink.write_log(log_entry)

        # Send to loguru (file + console)
        loguru_method = getattr(loguru_logger, level.lower())

        # Format extra data for loguru
        if extra:
            extra_str = f" | Extra: {json.dumps(extra, default=str)}"
            message_with_extra = f"{message}{extra_str}"
        else:
            message_with_extra = message

        if self.trace_id:
            message_with_extra = f"[{self.trace_id}] {message_with_extra}"

        loguru_method(message_with_extra)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log("DEBUG", message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log("ERROR", message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log("CRITICAL", message, **kwargs)

    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        extra = kwargs.get("extra", {})
        extra["traceback"] = traceback.format_exc()
        kwargs["extra"] = extra
        self._log("ERROR", message, **kwargs)

    def catch(
        self,
        exception=Exception,
        level="ERROR",
        reraise=False,
        onerror=None,
        exclude=None,
        default=None,
        message="An error has been caught in function '{record[function]}'",
    ):
        """
        Decorator to automatically catch and log exceptions (like loguru's @logger.catch)

        Args:
            exception: Exception type(s) to catch
            level: Log level for caught exceptions
            reraise: Whether to reraise the exception after logging
            onerror: Function to call when exception occurs
            exclude: Exception type(s) to exclude from catching
            default: Default return value when exception is caught
            message: Log message template
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except BaseException as e:
                    # Check if we should exclude this exception
                    if exclude and isinstance(e, exclude):
                        raise

                    # Check if we should catch this exception type
                    if not isinstance(e, exception):
                        raise

                    # Extract function info
                    func_info = {
                        "function": func.__name__,
                        "module": func.__module__,
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys()),
                    }

                    # Format the message
                    record = {
                        "function": func.__name__,
                        "module": func.__module__,
                        "exception": {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc(),
                        },
                    }

                    formatted_message = message.format(record=record)

                    # Log the exception
                    extra_data = {
                        "caught_exception": True,
                        "function_info": func_info,
                        "exception_type": type(e).__name__,
                        "exception_message": str(e),
                        "traceback": traceback.format_exc(),
                    }

                    self._log(level, formatted_message, extra=extra_data)

                    # Call onerror callback if provided
                    if onerror:
                        try:
                            onerror(e)
                        except Exception:
                            self._log(
                                "ERROR",
                                "Error in onerror callback",
                                extra={"callback_error": traceback.format_exc()},
                            )

                    # Reraise if requested
                    if reraise:
                        raise

                    # Return default value
                    return default

            return wrapper

        return decorator

    def shutdown(self):
        """Graceful shutdown"""
        self.db_sink.shutdown()


class LogDB:
    """Database interface for querying logs"""

    def __init__(self, db_path: str = "./logs/app_logs"):
        self.client = MongoClient(db_path)
        self.db = self.client["logs"]
        self.collection = self.db["entries"]

    def find(self, filter_dict: Optional[Dict] = None):
        """Find logs with MongoDB-style queries"""
        return self.collection.find(filter_dict or {})

    def find_one(self, filter_dict: Optional[Dict] = None):
        """Find single log entry"""
        return self.collection.find_one(filter_dict or {})

    def count(self, filter_dict: Optional[Dict] = None) -> int:
        """Count matching log entries"""
        return self.collection.count_documents(filter_dict or {})

    def get_recent_errors(self, hours: int = 24, limit: int = 100):
        """Get recent error logs"""
        since = time.time() - (hours * 3600)
        return self.collection.find(
            {
                "level": {"$in": ["ERROR", "CRITICAL"]},
                "timestamp.epoch": {"$gte": since},
            }
        ).limit(limit)

    def get_by_trace_id(self, trace_id: str):
        """Get all logs for a specific trace ID"""
        return self.collection.find({"trace_id": trace_id})

    def get_by_module(self, module_name: str, level: Optional[str] = None):
        """Get logs from specific module"""
        filter_dict = {"context.module": module_name}
        if level:
            filter_dict["level"] = level.upper()
        return self.collection.find(filter_dict)

    def get_performance_logs(self, min_duration: float = 1000):
        """Get logs with performance data above threshold"""
        return self.collection.find(
            {"extra.performance.duration_ms": {"$gte": min_duration}}
        )

    def delete_old_logs(self, days: int = 30):
        """Delete logs older than specified days"""
        cutoff = time.time() - (days * 24 * 3600)
        result = self.collection.delete_many({"timestamp.epoch": {"$lt": cutoff}})
        return result.deleted_count


# Create global logger instance
logger = StructuredLogger()


# Context manager for trace IDs
class trace_context:
    """Context manager for request tracing"""

    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or str(uuid.uuid4())[:8]
        self.previous_trace_id = None

    def __enter__(self):
        self.previous_trace_id = logger.trace_id
        logger.set_trace_id(self.trace_id)
        return self.trace_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.trace_id = self.previous_trace_id


# Convenience functions
def set_trace_id(trace_id: str):
    """Set global trace ID"""
    logger.set_trace_id(trace_id)


def clear_trace_id():
    """Clear global trace ID"""
    logger.clear_trace_id()


def shutdown():
    """Shutdown logging system gracefully"""
    logger.shutdown()


# Example usage and testing
if __name__ == "__main__":
    # Basic usage
    logger.info("Application started")
    logger.debug("Debug information", extra={"debug_level": "verbose"})

    # With structured data
    logger.info(
        "User login",
        extra={
            "user_id": "12345",
            "ip_address": "192.168.1.1",
            "login_method": "oauth",
        },
    )

    # Performance logging
    start_time = time.time()
    time.sleep(0.1)  # Simulate work
    duration = (time.time() - start_time) * 1000

    logger.info(
        "API request completed",
        extra={
            "endpoint": "/api/users",
            "method": "GET",
            "performance": {"duration_ms": duration},
            "response_code": 200,
        },
    )

    # Error logging
    try:
        raise ValueError("Something went wrong")
    except Exception:
        logger.exception("An error occurred", extra={"error_context": "user_creation"})

    # Test the @logger.catch decorator
    @logger.catch
    def risky_function(x, y):
        """Function that might raise an exception"""
        if x == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return y / x

    @logger.catch(exception=ValueError, level="WARNING", default="default_value")
    def another_risky_function(value):
        """Function with custom catch parameters"""
        if value < 0:
            raise ValueError("Negative values not allowed")
        if value == 0:
            raise ZeroDivisionError("Zero not allowed either")
        return value * 2

    # Test the decorator
    print("\n=== Testing @logger.catch decorator ===")

    # This will work fine
    result1 = risky_function(2, 10)
    print(f"Result 1: {result1}")

    # This will be caught and logged
    result2 = risky_function(0, 10)  # Will return None (default)
    print(f"Result 2: {result2}")

    # This will catch ValueError but not ZeroDivisionError
    result3 = another_risky_function(-5)  # Caught, returns "default_value"
    print(f"Result 3: {result3}")

    try:
        result4 = another_risky_function(0)  # ZeroDivisionError not caught, will raise
        print(f"Result 4: {result4}")
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError was not caught by decorator: {e}")

    # Trace context usage
    with trace_context("req_123") as trace_id:
        logger.info("Processing request", extra={"step": "validation"})
        logger.info("Request validated", extra={"step": "processing"})
        logger.info("Request completed", extra={"step": "response"})

    # Query examples
    time.sleep(2)  # Let async inserts complete

    log_db = LogDB()

    print("\n=== Recent Errors ===")
    for error in log_db.get_recent_errors(hours=1):
        print(f"{error['timestamp']['human']}: {error['message']}")

    print("\n=== Performance Logs ===")
    for perf_log in log_db.get_performance_logs(min_duration=50):
        duration = perf_log["extra"].get("performance", {}).get("duration_ms", 0)
        print(f"{perf_log['message']}: {duration}ms")

    print("\n=== Trace Logs ===")
    for trace_log in log_db.get_by_trace_id("req_123"):
        print(f"{trace_log['timestamp']['human']}: {trace_log['message']}")

    print("\n=== Caught Exception Logs ===")
    for caught_log in log_db.find({"extra.caught_exception": True}):
        print(
            f"{caught_log['timestamp']['human']}: {caught_log['message']} - {caught_log['extra']['exception_type']}"
        )

    # Graceful shutdown
    shutdown()

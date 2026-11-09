"""
📝 GABRIEL STRUCTURED LOGGING
100% Perfect Logging
GORUNFREE Protocol
"""

import structlog
import logging
import sys
from typing import Any, Dict

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Get logger
logger = structlog.get_logger()


def get_logger(name: str = "gabriel") -> structlog.BoundLogger:
    """
    Get structured logger
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)


def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """
    Log error with context
    
    Args:
        error: Exception to log
        context: Additional context
    """
    logger.error(
        "error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True
    )


def log_performance(operation: str, duration_ms: float, context: Dict[str, Any] = None) -> None:
    """
    Log performance metric
    
    Args:
        operation: Operation name
        duration_ms: Duration in milliseconds
        context: Additional context
    """
    logger.info(
        "performance_metric",
        operation=operation,
        duration_ms=duration_ms,
        context=context or {}
    )


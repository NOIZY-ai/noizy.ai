"""
📊 PROMETHEUS METRICS - 100% PERFECT
Perfect metrics collection
GORUNFREE Protocol
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from typing import Optional
from ..logging import get_logger

logger = get_logger("metrics")

# Voice generation metrics
voice_generation_total = Counter(
    "voice_generation_total",
    "Total voice generations",
    ["service", "status"]
)

voice_generation_duration = Histogram(
    "voice_generation_duration_seconds",
    "Voice generation duration",
    ["service"]
)

# API metrics
api_requests_total = Counter(
    "api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"]
)

api_request_duration = Histogram(
    "api_request_duration_seconds",
    "API request duration",
    ["method", "endpoint"]
)

# Cache metrics
cache_hits_total = Counter(
    "cache_hits_total",
    "Total cache hits",
    ["cache_type"]
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total cache misses",
    ["cache_type"]
)

# Database metrics
database_queries_total = Counter(
    "database_queries_total",
    "Total database queries",
    ["operation"]
)

database_query_duration = Histogram(
    "database_query_duration_seconds",
    "Database query duration",
    ["operation"]
)

# Active users
active_users = Gauge(
    "active_users",
    "Number of active users"
)


def record_voice_generation(service: str, status: str, duration: float) -> None:
    """
    Record voice generation metric
    
    Args:
        service: Service name
        status: Status (success/failure)
        duration: Duration in seconds
    """
    voice_generation_total.labels(service=service, status=status).inc()
    voice_generation_duration.labels(service=service).observe(duration)


def record_api_request(method: str, endpoint: str, status: int, duration: float) -> None:
    """
    Record API request metric
    
    Args:
        method: HTTP method
        endpoint: Endpoint path
        status: HTTP status code
        duration: Duration in seconds
    """
    api_requests_total.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)


def record_cache_hit(cache_type: str) -> None:
    """
    Record cache hit
    
    Args:
        cache_type: Cache type
    """
    cache_hits_total.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str) -> None:
    """
    Record cache miss
    
    Args:
        cache_type: Cache type
    """
    cache_misses_total.labels(cache_type=cache_type).inc()


def record_database_query(operation: str, duration: float) -> None:
    """
    Record database query
    
    Args:
        operation: Operation type
        duration: Duration in seconds
    """
    database_queries_total.labels(operation=operation).inc()
    database_query_duration.labels(operation=operation).observe(duration)


def set_active_users(count: int) -> None:
    """
    Set active users count
    
    Args:
        count: Number of active users
    """
    active_users.set(count)


def get_metrics() -> bytes:
    """
    Get Prometheus metrics
    
    Returns:
        Metrics in Prometheus format
    """
    return generate_latest()

"""
💾 CACHING SYSTEM - 100% PERFECT
Perfect caching implementation
GORUNFREE Protocol
"""

from .redis_cache import (
    get_cache,
    set_cache,
    delete_cache,
    clear_cache_pattern,
    cached,
    cache_key,
    get_redis_client
)

__all__ = [
    "get_cache",
    "set_cache",
    "delete_cache",
    "clear_cache_pattern",
    "cached",
    "cache_key",
    "get_redis_client",
]


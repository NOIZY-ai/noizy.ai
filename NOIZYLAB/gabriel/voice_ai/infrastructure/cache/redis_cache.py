"""
💾 REDIS CACHING LAYER
100% Perfect Caching
GORUNFREE Protocol
"""

import json
import redis
from typing import Optional, Any, Union
from functools import wraps
import hashlib
from ..config import settings
from ..logging import get_logger

logger = get_logger("cache")

# Redis connection pool
redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """
    Get Redis client (singleton)
    
    Returns:
        Redis client instance or None if connection fails
    """
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            redis_client.ping()
        except Exception as e:
            logger.warning("redis_connection_failed", error=str(e))
            return None
    return redis_client


def cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate cache key
    
    Args:
        prefix: Key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Cache key string
    """
    key_data = f"{prefix}:{args}:{kwargs}"
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    return f"gabriel:{prefix}:{key_hash}"


def get_cache(key: str) -> Optional[Any]:
    """
    Get value from cache
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None
    """
    try:
        client = get_redis_client()
        value = client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        logger.warning("cache_get_failed", key=key, error=str(e))
    return None


def set_cache(key: str, value: Any, ttl: int = None) -> bool:
    """
    Set value in cache
    
    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds (default from config)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_redis_client()
        ttl = ttl or settings.REDIS_CACHE_TTL
        client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        logger.warning("cache_set_failed", key=key, error=str(e))
        return False


def delete_cache(key: str) -> bool:
    """
    Delete value from cache
    
    Args:
        key: Cache key
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_redis_client()
        client.delete(key)
        return True
    except Exception as e:
        logger.warning("cache_delete_failed", key=key, error=str(e))
        return False


def clear_cache_pattern(pattern: str) -> int:
    """
    Clear cache by pattern
    
    Args:
        pattern: Redis pattern (e.g., "gabriel:voice:*")
        
    Returns:
        Number of keys deleted
    """
    try:
        client = get_redis_client()
        keys = client.keys(pattern)
        if keys:
            return client.delete(*keys)
        return 0
    except Exception as e:
        logger.warning("cache_clear_failed", pattern=pattern, error=str(e))
        return 0


def cached(ttl: int = None, key_prefix: str = "cache"):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Cache key prefix
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = cache_key(f"{key_prefix}:{func.__name__}", *args, **kwargs)
            cached_value = get_cache(key)
            if cached_value is not None:
                logger.debug("cache_hit", function=func.__name__, key=key)
                return cached_value
            
            result = await func(*args, **kwargs)
            set_cache(key, result, ttl)
            logger.debug("cache_miss", function=func.__name__, key=key)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = cache_key(f"{key_prefix}:{func.__name__}", *args, **kwargs)
            cached_value = get_cache(key)
            if cached_value is not None:
                logger.debug("cache_hit", function=func.__name__, key=key)
                return cached_value
            
            result = func(*args, **kwargs)
            set_cache(key, result, ttl)
            logger.debug("cache_miss", function=func.__name__, key=key)
            return result
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


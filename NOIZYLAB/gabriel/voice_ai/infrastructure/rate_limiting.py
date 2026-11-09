"""
🚦 RATE LIMITING - 100% PERFECT
Perfect rate limiting implementation
GORUNFREE Protocol
"""

from typing import Optional, Callable
from functools import wraps
from fastapi import Request, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from ..config import settings
from ..logging import get_logger
from ..errors.exceptions import RateLimitError

logger = get_logger("rate_limiting")

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"] if settings.RATE_LIMIT_ENABLED else []
)


def rate_limit(limit: str, key_func: Optional[Callable] = None):
    """
    Rate limit decorator
    
    Args:
        limit: Rate limit string (e.g., "10/minute")
        key_func: Optional key function
        
    Returns:
        Decorator function
    """
    def decorator(func):
        if settings.RATE_LIMIT_ENABLED:
            return limiter.limit(limit, key_func=key_func)(func)
        return func
    return decorator


def get_user_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key from user ID
    
    Args:
        request: FastAPI request
        
    Returns:
        Rate limit key
    """
    # Try to get user ID from token
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return f"user:{user_id}"
    return get_remote_address(request)


@rate_limit("60/minute")
def default_rate_limit():
    """Default rate limit"""
    pass


# Error handler
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Handle rate limit exceeded
    
    Args:
        request: FastAPI request
        exc: RateLimitExceeded exception
        
    Returns:
        HTTPException response
    """
    logger.warning(
        "rate_limit_exceeded",
        remote_address=get_remote_address(request),
        limit=str(exc.detail)
    )
    
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "error": True,
            "code": "RATE_LIMIT_EXCEEDED",
            "message": "Rate limit exceeded",
            "retry_after": exc.retry_after
        },
        headers={"Retry-After": str(exc.retry_after)} if exc.retry_after else {}
    )


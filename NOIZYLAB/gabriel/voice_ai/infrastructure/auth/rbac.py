"""
🔐 ROLE-BASED ACCESS CONTROL
Perfect RBAC implementation
GORUNFREE Protocol
"""

from typing import List, Callable
from functools import wraps
from fastapi import HTTPException, status
from .jwt_auth import get_current_user
from ..errors.exceptions import AuthorizationError
from ..logging import get_logger

logger = get_logger("rbac")


def require_role(allowed_roles: List[str]):
    """
    Decorator to require specific role
    
    Args:
        allowed_roles: List of allowed roles
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from kwargs or args
            user = kwargs.get("current_user") or (args[0] if args else None)
            
            if not user:
                raise AuthorizationError("User not authenticated")
            
            user_role = user.get("role")
            if user_role not in allowed_roles:
                logger.warning(
                    "unauthorized_access_attempt",
                    user_id=user.get("user_id"),
                    user_role=user_role,
                    required_roles=allowed_roles
                )
                raise AuthorizationError(
                    f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def check_permission(user_role: str, required_permission: str) -> bool:
    """
    Check if user has required permission
    
    Args:
        user_role: User's role
        required_permission: Required permission
        
    Returns:
        True if user has permission, False otherwise
    """
    # Permission matrix
    permissions = {
        "admin": ["*"],  # All permissions
        "voice_actor": [
            "voice:create",
            "voice:read",
            "voice:update",
            "voice:delete",
            "license:read",
            "revenue:read"
        ],
        "client": [
            "voice:read",
            "voice:generate",
            "license:create",
            "license:read",
            "payment:create"
        ],
        "guest": ["voice:read"]
    }
    
    user_perms = permissions.get(user_role, [])
    return "*" in user_perms or required_permission in user_perms


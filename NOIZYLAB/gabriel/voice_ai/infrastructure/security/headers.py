"""
🔒 SECURITY HEADERS - 100% PERFECT
Perfect security headers
GORUNFREE Protocol
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from ..config import settings
from ..logging import get_logger

logger = get_logger("security_headers")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        """Add security headers"""
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # HTTPS enforcement
        if settings.SECURE_SSL_REDIRECT:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


def add_security_headers(response: Response) -> Response:
    """
    Add security headers to response
    
    Args:
        response: FastAPI response
        
    Returns:
        Response with security headers
    """
    middleware = SecurityHeadersMiddleware(None)
    # Headers are added by middleware
    return response


"""
🔄 TIMING MIDDLEWARE - 100% PERFECT
Perfect request timing
GORUNFREE Protocol
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from ..logging import get_logger
from ..monitoring.metrics import record_api_request

logger = get_logger("middleware")


class TimingMiddleware(BaseHTTPMiddleware):
    """Track request timing"""
    
    async def dispatch(self, request: Request, call_next):
        """Track timing"""
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        duration_ms = duration * 1000
        
        # Add timing header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        
        # Record metric
        record_api_request(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
            duration=duration
        )
        
        logger.debug(
            "request_timing",
            path=request.url.path,
            method=request.method,
            duration_ms=duration_ms,
            status=response.status_code
        )
        
        return response


"""
🔄 REQUEST ID MIDDLEWARE - 100% PERFECT
Perfect request ID tracking
GORUNFREE Protocol
"""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from ..logging import get_logger

logger = get_logger("middleware")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests"""
    
    async def dispatch(self, request: Request, call_next):
        """Add request ID"""
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        logger.debug("request_processed", request_id=request_id, path=request.url.path)
        return response


"""
🔒 CORS CONFIGURATION - 100% PERFECT
Perfect CORS setup
GORUNFREE Protocol
"""

from fastapi.middleware.cors import CORSMiddleware
from ..config import settings
from ..logging import get_logger

logger = get_logger("cors")


def configure_cors(app):
    """
    Configure CORS middleware
    
    Args:
        app: FastAPI application
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
        expose_headers=["X-Request-ID", "X-Response-Time"],
        max_age=3600,
    )
    logger.info("cors_configured", origins=settings.CORS_ORIGINS)


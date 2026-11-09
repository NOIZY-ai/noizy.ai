"""
⚠️ GABRIEL ERROR HANDLING
100% Perfect Error Management
GORUNFREE Protocol
"""

from .exceptions import (
    GabrielError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    PaymentError,
    VoiceGenerationError,
    DatabaseError,
)
from .handlers import error_handler, validation_error_handler

__all__ = [
    "GabrielError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "PaymentError",
    "VoiceGenerationError",
    "DatabaseError",
    "error_handler",
    "validation_error_handler",
]


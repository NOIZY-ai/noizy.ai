"""
⚠️ CUSTOM EXCEPTIONS
Perfect error handling
GORUNFREE Protocol
"""

from typing import Optional, Dict, Any


class GabrielError(Exception):
    """Base exception for all Gabriel errors"""
    
    def __init__(
        self,
        message: str,
        code: str = "GENERIC_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(GabrielError):
    """Validation error"""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details={"field": field, **(details or {})}
        )


class AuthenticationError(GabrielError):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=401,
            details=details or {}
        )


class AuthorizationError(GabrielError):
    """Authorization error"""
    
    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=403,
            details=details or {}
        )


class NotFoundError(GabrielError):
    """Resource not found error"""
    
    def __init__(self, resource: str, identifier: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": identifier, **(details or {})}
        )


class ConflictError(GabrielError):
    """Resource conflict error"""
    
    def __init__(self, message: str, resource: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details={"resource": resource, **(details or {})}
        )


class RateLimitError(GabrielError):
    """Rate limit exceeded error"""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after": retry_after, **(details or {})}
        )


class PaymentError(GabrielError):
    """Payment processing error"""
    
    def __init__(self, message: str, payment_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="PAYMENT_ERROR",
            status_code=402,
            details={"payment_id": payment_id, **(details or {})}
        )


class VoiceGenerationError(GabrielError):
    """Voice generation error"""
    
    def __init__(self, message: str, service: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VOICE_GENERATION_ERROR",
            status_code=500,
            details={"service": service, **(details or {})}
        )


class DatabaseError(GabrielError):
    """Database operation error"""
    
    def __init__(self, message: str, operation: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details={"operation": operation, **(details or {})}
        )


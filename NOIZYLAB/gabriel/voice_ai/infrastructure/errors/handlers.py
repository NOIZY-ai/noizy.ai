"""
⚠️ ERROR HANDLERS
Perfect error handling middleware
GORUNFREE Protocol
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .exceptions import GabrielError
from ..logging import get_logger

logger = get_logger("error_handler")


async def error_handler(request: Request, exc: GabrielError) -> JSONResponse:
    """
    Handle Gabriel custom errors
    
    Args:
        request: FastAPI request
        exc: GabrielError exception
        
    Returns:
        JSON error response
    """
    logger.error(
        "error_occurred",
        error_code=exc.code,
        error_message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation errors
    
    Args:
        request: FastAPI request
        exc: RequestValidationError exception
        
    Returns:
        JSON error response
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        "validation_error",
        errors=errors,
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "code": "VALIDATION_ERROR",
            "message": "Validation failed",
            "details": {"errors": errors}
        }
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle generic exceptions
    
    Args:
        request: FastAPI request
        exc: Generic exception
        
    Returns:
        JSON error response
    """
    logger.error(
        "unhandled_error",
        error_type=type(exc).__name__,
        error_message=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "code": "INTERNAL_ERROR",
            "message": "An internal error occurred",
            "details": {}
        }
    )


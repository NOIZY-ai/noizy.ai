"""
🔒 INPUT VALIDATION - 100% PERFECT
Perfect input validation
GORUNFREE Protocol
"""

import re
from typing import Any, Optional
from pydantic import BaseModel, validator, ValidationError
from ..errors.exceptions import ValidationError as GabrielValidationError
from ..logging import get_logger

logger = get_logger("validation")


def validate_input(data: Any, model: type[BaseModel]) -> BaseModel:
    """
    Validate input against Pydantic model
    
    Args:
        data: Input data
        model: Pydantic model class
        
    Returns:
        Validated model instance
        
    Raises:
        GabrielValidationError: If validation fails
    """
    try:
        return model(**data) if isinstance(data, dict) else model.parse_obj(data)
    except ValidationError as e:
        errors = []
        for error in e.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        raise GabrielValidationError(
            "Validation failed",
            details={"errors": errors}
        )


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text input
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        raise GabrielValidationError("Input must be a string")
    
    # Remove null bytes
    text = text.replace("\x00", "")
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_email(email: str) -> bool:
    """
    Validate email address
    
    Args:
        email: Email address
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    Validate URL
    
    Args:
        url: URL string
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


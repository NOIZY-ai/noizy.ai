"""
🛠️ HELPER FUNCTIONS - 100% PERFECT
Perfect utility helpers
GORUNFREE Protocol
"""

import uuid
from typing import Optional


def generate_id(prefix: Optional[str] = None) -> str:
    """
    Generate unique ID
    
    Args:
        prefix: Optional prefix
        
    Returns:
        Unique ID string
    """
    id_str = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{id_str}"
    return id_str


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable string
    
    Args:
        bytes_value: Bytes value
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_duration(seconds: float) -> str:
    """
    Format duration to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1.5s", "150ms")
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f}μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


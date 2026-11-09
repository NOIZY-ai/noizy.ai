"""
📧 EMAIL SYSTEM - 100% PERFECT
Perfect email implementation
GORUNFREE Protocol
"""

import os
from .email_service import send_email, send_welcome_email, send_verification_email

__all__ = [
    "send_email",
    "send_welcome_email",
    "send_verification_email",
]

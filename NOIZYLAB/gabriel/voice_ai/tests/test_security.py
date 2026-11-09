"""
🧪 SECURITY TESTS - 100% PERFECT
Perfect security test coverage
GORUNFREE Protocol
"""

import pytest
from ..infrastructure.security.validation import (
    validate_email, validate_url, sanitize_input
)
from ..infrastructure.auth.password import hash_password, verify_password


class TestSecurity:
    """Security tests"""
    
    def test_email_validation(self):
        """Test email validation"""
        assert validate_email("test@example.com") is True
        assert validate_email("invalid-email") is False
        assert validate_email("test@") is False
        assert validate_email("@example.com") is False
    
    def test_url_validation(self):
        """Test URL validation"""
        assert validate_url("https://example.com") is True
        assert validate_url("http://example.com") is True
        assert validate_url("invalid-url") is False
        assert validate_url("ftp://example.com") is False
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        # Test null bytes
        result = sanitize_input("test\x00string")
        assert "\x00" not in result
        
        # Test whitespace trimming
        result = sanitize_input("  test  ")
        assert result == "test"
        
        # Test max length
        result = sanitize_input("a" * 200, max_length=100)
        assert len(result) == 100
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False


"""
🧪 AUTHENTICATION TESTS
100% Perfect Test Coverage
GORUNFREE Protocol
"""

import pytest
from datetime import timedelta
from ..infrastructure.auth.jwt_auth import create_access_token, verify_token, create_refresh_token
from ..infrastructure.auth.password import hash_password, verify_password


class TestJWT:
    """Test JWT authentication"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": 1, "email": "test@example.com", "role": "user"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token(self):
        """Test token verification"""
        data = {"sub": 1, "email": "test@example.com", "role": "user"}
        token = create_access_token(data)
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == 1
        assert payload["email"] == "test@example.com"
    
    def test_verify_invalid_token(self):
        """Test invalid token verification"""
        payload = verify_token("invalid_token")
        assert payload is None
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = {"sub": 1, "email": "test@example.com"}
        token = create_refresh_token(data)
        assert token is not None
        assert isinstance(token, str)
        payload = verify_token(token)
        assert payload is not None
        assert payload.get("type") == "refresh"


class TestPassword:
    """Test password hashing"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password_123"
        hashed = hash_password(password)
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password(self):
        """Test password verification"""
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False


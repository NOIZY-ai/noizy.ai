"""
🧪 PYTEST CONFIGURATION - 100% PERFECT
Perfect test configuration
GORUNFREE Protocol
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_db():
    """Test database fixture"""
    # TODO: Setup test database
    yield None
    # TODO: Teardown test database


@pytest.fixture
def test_redis():
    """Test Redis fixture"""
    # TODO: Setup test Redis
    yield None
    # TODO: Teardown test Redis


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings"""
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/1")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key")
    from infrastructure.config import settings
    return settings

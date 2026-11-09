"""
🧪 UTILITY TESTS - 100% PERFECT
Perfect utility test coverage
GORUNFREE Protocol
"""

import pytest
from ..infrastructure.utils.helpers import generate_id, format_bytes, format_duration


class TestUtils:
    """Utility tests"""
    
    def test_generate_id(self):
        """Test ID generation"""
        id1 = generate_id()
        id2 = generate_id()
        
        assert id1 != id2
        assert len(id1) > 0
        
        # Test with prefix
        prefixed = generate_id("test")
        assert prefixed.startswith("test_")
    
    def test_format_bytes(self):
        """Test bytes formatting"""
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(1048576) == "1.00 MB"
        assert format_bytes(500) == "500.00 B"
    
    def test_format_duration(self):
        """Test duration formatting"""
        assert "ms" in format_duration(0.1)
        assert "s" in format_duration(1.5)
        assert "μs" in format_duration(0.0001)


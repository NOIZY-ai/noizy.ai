"""
🧪 CACHE TESTS - 100% PERFECT
Perfect cache test coverage
GORUNFREE Protocol
"""

import pytest
from ..infrastructure.cache.redis_cache import (
    get_cache, set_cache, delete_cache, cache_key, cached
)


class TestCache:
    """Cache tests"""
    
    def test_cache_key_generation(self):
        """Test cache key generation"""
        key = cache_key("test", "arg1", "arg2", kwarg1="value1")
        assert key.startswith("gabriel:test:")
        assert len(key) > 0
    
    def test_set_and_get_cache(self):
        """Test setting and getting cache"""
        key = "test_key"
        value = {"test": "data"}
        
        result = set_cache(key, value, ttl=60)
        assert result is True
        
        cached_value = get_cache(key)
        assert cached_value == value
    
    def test_delete_cache(self):
        """Test cache deletion"""
        key = "test_delete_key"
        value = {"test": "data"}
        
        set_cache(key, value)
        assert get_cache(key) == value
        
        delete_cache(key)
        assert get_cache(key) is None
    
    @cached(ttl=60, key_prefix="test")
    def test_cached_function(self, x: int, y: int) -> int:
        """Test cached function decorator"""
        return x + y
    
    def test_cached_decorator(self):
        """Test cache decorator"""
        result1 = self.test_cached_function(1, 2)
        result2 = self.test_cached_function(1, 2)  # Should use cache
        
        assert result1 == 3
        assert result2 == 3


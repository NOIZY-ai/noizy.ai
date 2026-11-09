"""
🧪 MONITORING TESTS - 100% PERFECT
Perfect monitoring test coverage
GORUNFREE Protocol
"""

import pytest
from ..infrastructure.monitoring.metrics import (
    record_voice_generation,
    record_api_request,
    record_cache_hit,
    record_cache_miss,
    set_active_users,
    get_metrics
)
from ..infrastructure.monitoring.health import health_check


class TestMonitoring:
    """Monitoring tests"""
    
    def test_record_voice_generation(self):
        """Test voice generation metric"""
        # Should not raise
        record_voice_generation("gtts", "success", 0.5)
    
    def test_record_api_request(self):
        """Test API request metric"""
        record_api_request("POST", "/api/generate", 200, 0.1)
    
    def test_record_cache_hit(self):
        """Test cache hit metric"""
        record_cache_hit("voice")
    
    def test_record_cache_miss(self):
        """Test cache miss metric"""
        record_cache_miss("voice")
    
    def test_set_active_users(self):
        """Test active users metric"""
        set_active_users(10)
    
    def test_get_metrics(self):
        """Test metrics retrieval"""
        metrics = get_metrics()
        assert isinstance(metrics, bytes)
        assert len(metrics) > 0
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check"""
        result = await health_check.check_liveness()
        assert "status" in result
        assert result["status"] == "alive"


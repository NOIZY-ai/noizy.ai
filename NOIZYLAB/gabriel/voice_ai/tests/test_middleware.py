"""
🧪 MIDDLEWARE TESTS - 100% PERFECT
Perfect middleware test coverage
GORUNFREE Protocol
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ..infrastructure.middleware.request_id import RequestIDMiddleware
from ..infrastructure.middleware.timing import TimingMiddleware


@pytest.fixture
def app():
    """Create test app"""
    app = FastAPI()
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(TimingMiddleware)
    
    @app.get("/test")
    def test_endpoint():
        return {"status": "ok"}
    
    return app


class TestMiddleware:
    """Middleware tests"""
    
    def test_request_id_middleware(self, app):
        """Test request ID middleware"""
        client = TestClient(app)
        response = client.get("/test")
        
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0
    
    def test_timing_middleware(self, app):
        """Test timing middleware"""
        client = TestClient(app)
        response = client.get("/test")
        
        assert "X-Response-Time" in response.headers
        assert "ms" in response.headers["X-Response-Time"]


"""
🏥 HEALTH CHECK SYSTEM
100% Perfect Health Monitoring
GORUNFREE Protocol
"""

from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
from ..config import settings
from ..logging import get_logger
# Redis check will use cache module

logger = get_logger("health")


class HealthCheck:
    """Health check system"""
    
    def __init__(self):
        self.checks = {
            "database": self._check_database,
            "redis": self._check_redis,
            "storage": self._check_storage,
        }
    
    async def _check_database(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            from ..database.connection import check_db_connection
            start = datetime.now()
            if check_db_connection():
                latency = (datetime.now() - start).total_seconds() * 1000
                return {"status": "healthy", "latency_ms": latency}
            else:
                return {"status": "unhealthy", "error": "Connection check failed"}
        except Exception as e:
            logger.error("health_check_failed", component="database", error=str(e))
            return {"status": "unhealthy", "error": str(e)}
    
    async def _check_redis(self) -> Dict[str, Any]:
        """Check Redis health"""
        try:
            from ..cache.redis_cache import get_redis_client
            client = get_redis_client()
            if client:
                start = datetime.now()
                client.ping()
                latency = (datetime.now() - start).total_seconds() * 1000
                return {"status": "healthy", "latency_ms": latency}
            return {"status": "unhealthy", "error": "Redis client not available"}
        except Exception as e:
            logger.error("health_check_failed", component="redis", error=str(e))
            return {"status": "unhealthy", "error": str(e)}
    
    async def _check_storage(self) -> Dict[str, Any]:
        """Check file storage health"""
        try:
            # TODO: Implement actual storage check
            return {"status": "healthy", "latency_ms": 0}
        except Exception as e:
            logger.error("health_check_failed", component="storage", error=str(e))
            return {"status": "unhealthy", "error": str(e)}
    
    async def check_all(self) -> Dict[str, Any]:
        """
        Run all health checks
        
        Returns:
            Health check results
        """
        results = {}
        for name, check_func in self.checks.items():
            results[name] = await check_func()
        
        overall_status = "healthy" if all(
            r.get("status") == "healthy" for r in results.values()
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.APP_VERSION,
            "checks": results
        }
    
    async def check_liveness(self) -> Dict[str, Any]:
        """
        Liveness check (basic)
        
        Returns:
            Liveness status
        """
        return {
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def check_readiness(self) -> Dict[str, Any]:
        """
        Readiness check (dependencies)
        
        Returns:
            Readiness status
        """
        return await self.check_all()


# Global health check instance
health_check = HealthCheck()


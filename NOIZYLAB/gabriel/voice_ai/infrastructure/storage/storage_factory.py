"""
📦 STORAGE FACTORY - 100% PERFECT
Perfect storage factory
GORUNFREE Protocol
"""

from typing import Optional
from ..config import settings
from .cloudflare_r2 import CloudflareR2Storage
from .s3_storage import S3Storage
from .local_storage import LocalStorage
from ..logging import get_logger

logger = get_logger("storage_factory")

_storage_instance: Optional[object] = None


def get_storage():
    """
    Get storage instance (singleton)
    
    Returns:
        Storage instance
    """
    global _storage_instance
    
    if _storage_instance is None:
        storage_type = settings.STORAGE_TYPE.lower()
        
        if storage_type == "cloudflare_r2":
            _storage_instance = CloudflareR2Storage(
                account_id=settings.CLOUDFLARE_R2_ACCOUNT_ID,
                access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY_ID,
                secret_access_key=settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY,
                bucket=settings.CLOUDFLARE_R2_BUCKET
            )
        elif storage_type == "s3":
            _storage_instance = S3Storage(
                bucket=settings.CLOUDFLARE_R2_BUCKET  # Reuse config
            )
        else:
            _storage_instance = LocalStorage()
        
        logger.info("storage_initialized", type=storage_type)
    
    return _storage_instance


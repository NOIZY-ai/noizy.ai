"""
📦 LOCAL STORAGE - 100% PERFECT
Perfect local storage implementation
GORUNFREE Protocol
"""

from pathlib import Path
from typing import Optional
from ..logging import get_logger

logger = get_logger("local_storage")


class LocalStorage:
    """Local file storage implementation"""
    
    def __init__(self, base_path: str = "storage"):
        """
        Initialize local storage
        
        Args:
            base_path: Base storage path
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("local_storage_initialized", path=str(self.base_path))
    
    def upload_file(self, file_path: str, key: str, content_type: Optional[str] = None) -> str:
        """
        Upload file (copy to storage)
        
        Args:
            file_path: Source file path
            key: Storage key
            content_type: Content type (unused for local)
            
        Returns:
            Local file path
        """
        try:
            dest_path = self.base_path / key
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(file_path, dest_path)
            
            logger.info("file_uploaded", key=key, path=str(dest_path))
            return str(dest_path)
        except Exception as e:
            logger.error("upload_failed", key=key, error=str(e))
            raise
    
    def download_file(self, key: str, file_path: str) -> bool:
        """
        Download file (copy from storage)
        
        Args:
            key: Storage key
            file_path: Destination file path
            
        Returns:
            True if successful
        """
        try:
            source_path = self.base_path / key
            if not source_path.exists():
                logger.warning("file_not_found", key=key)
                return False
            
            import shutil
            shutil.copy2(source_path, file_path)
            
            logger.info("file_downloaded", key=key)
            return True
        except Exception as e:
            logger.error("download_failed", key=key, error=str(e))
            return False
    
    def delete_file(self, key: str) -> bool:
        """
        Delete file
        
        Args:
            key: Storage key
            
        Returns:
            True if successful
        """
        try:
            file_path = self.base_path / key
            if file_path.exists():
                file_path.unlink()
                logger.info("file_deleted", key=key)
                return True
            return False
        except Exception as e:
            logger.error("delete_failed", key=key, error=str(e))
            return False


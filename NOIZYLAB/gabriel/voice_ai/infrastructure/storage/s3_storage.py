"""
📦 AWS S3 STORAGE - 100% PERFECT
Perfect S3 storage implementation
GORUNFREE Protocol
"""

import boto3
from typing import Optional
from ..logging import get_logger

logger = get_logger("s3_storage")


class S3Storage:
    """AWS S3 storage implementation"""
    
    def __init__(self, bucket: str, region: str = "us-east-1"):
        """
        Initialize S3 storage
        
        Args:
            bucket: S3 bucket name
            region: AWS region
        """
        self.bucket = bucket
        self.client = boto3.client('s3', region_name=region)
        logger.info("s3_storage_initialized", bucket=bucket, region=region)
    
    def upload_file(self, file_path: str, key: str, content_type: Optional[str] = None) -> str:
        """Upload file to S3"""
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.client.upload_file(file_path, self.bucket, key, ExtraArgs=extra_args)
            url = f"https://{self.bucket}.s3.amazonaws.com/{key}"
            logger.info("file_uploaded", key=key, bucket=self.bucket)
            return url
        except Exception as e:
            logger.error("upload_failed", key=key, error=str(e))
            raise
    
    def download_file(self, key: str, file_path: str) -> bool:
        """Download file from S3"""
        try:
            self.client.download_file(self.bucket, key, file_path)
            logger.info("file_downloaded", key=key)
            return True
        except Exception as e:
            logger.error("download_failed", key=key, error=str(e))
            return False
    
    def delete_file(self, key: str) -> bool:
        """Delete file from S3"""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info("file_deleted", key=key)
            return True
        except Exception as e:
            logger.error("delete_failed", key=key, error=str(e))
            return False


"""
📦 CLOUDFLARE R2 STORAGE - 100% PERFECT
Perfect R2 storage implementation
GORUNFREE Protocol
"""

import boto3
from typing import Optional, BinaryIO
from botocore.config import Config
from ..logging import get_logger

logger = get_logger("r2_storage")


class CloudflareR2Storage:
    """Cloudflare R2 storage implementation"""
    
    def __init__(
        self,
        account_id: str,
        access_key_id: str,
        secret_access_key: str,
        bucket: str
    ):
        """
        Initialize R2 storage
        
        Args:
            account_id: R2 account ID
            access_key_id: R2 access key ID
            secret_access_key: R2 secret access key
            bucket: R2 bucket name
        """
        self.account_id = account_id
        self.bucket = bucket
        
        # R2 endpoint
        endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
        
        # Create S3-compatible client
        self.client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version='s3v4')
        )
        
        logger.info("r2_storage_initialized", bucket=bucket)
    
    def upload_file(self, file_path: str, key: str, content_type: Optional[str] = None) -> str:
        """
        Upload file to R2
        
        Args:
            file_path: Local file path
            key: R2 object key
            content_type: Content type
            
        Returns:
            Public URL
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.client.upload_file(file_path, self.bucket, key, ExtraArgs=extra_args)
            
            # Generate public URL (if public bucket)
            url = f"https://{self.bucket}.r2.cloudflarestorage.com/{key}"
            
            logger.info("file_uploaded", key=key, bucket=self.bucket)
            return url
        except Exception as e:
            logger.error("upload_failed", key=key, error=str(e))
            raise
    
    def download_file(self, key: str, file_path: str) -> bool:
        """
        Download file from R2
        
        Args:
            key: R2 object key
            file_path: Local file path
            
        Returns:
            True if successful
        """
        try:
            self.client.download_file(self.bucket, key, file_path)
            logger.info("file_downloaded", key=key)
            return True
        except Exception as e:
            logger.error("download_failed", key=key, error=str(e))
            return False
    
    def delete_file(self, key: str) -> bool:
        """
        Delete file from R2
        
        Args:
            key: R2 object key
            
        Returns:
            True if successful
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info("file_deleted", key=key)
            return True
        except Exception as e:
            logger.error("delete_failed", key=key, error=str(e))
            return False
    
    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        Get presigned URL
        
        Args:
            key: R2 object key
            expires_in: Expiration in seconds
            
        Returns:
            Presigned URL
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            logger.error("presigned_url_failed", key=key, error=str(e))
            raise


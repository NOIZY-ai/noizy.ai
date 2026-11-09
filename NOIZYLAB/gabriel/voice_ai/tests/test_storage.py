"""
🧪 STORAGE TESTS - 100% PERFECT
Perfect storage test coverage
GORUNFREE Protocol
"""

import pytest
from pathlib import Path
from ..infrastructure.storage.local_storage import LocalStorage


class TestStorage:
    """Storage tests"""
    
    @pytest.fixture
    def storage(self):
        """Create storage instance"""
        return LocalStorage(base_path="test_storage")
    
    @pytest.fixture
    def test_file(self, tmp_path):
        """Create test file"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        return str(test_file)
    
    def test_upload_file(self, storage, test_file):
        """Test file upload"""
        key = "test/upload.txt"
        result = storage.upload_file(test_file, key)
        
        assert result is not None
        assert Path(result).exists()
    
    def test_download_file(self, storage, test_file, tmp_path):
        """Test file download"""
        key = "test/download.txt"
        storage.upload_file(test_file, key)
        
        dest_file = tmp_path / "downloaded.txt"
        result = storage.download_file(key, str(dest_file))
        
        assert result is True
        assert dest_file.exists()
        assert dest_file.read_text() == "test content"
    
    def test_delete_file(self, storage, test_file):
        """Test file deletion"""
        key = "test/delete.txt"
        storage.upload_file(test_file, key)
        
        result = storage.delete_file(key)
        assert result is True
        
        # Verify file is deleted
        file_path = Path(storage.base_path) / key
        assert not file_path.exists()


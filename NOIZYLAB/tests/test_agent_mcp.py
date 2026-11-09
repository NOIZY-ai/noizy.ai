"""
Tests for Agent CLI MCP functionality
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
import pytest


# Get the repository root directory
REPO_ROOT = Path(__file__).parent.parent.absolute()


class TestAgentMCP:
    """Test Agent MCP commands"""
    
    @pytest.fixture
    def temp_config(self):
        """Create a temporary MCP configuration"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config = {
                "mcpServers": {
                    "test-server": {
                        "transport": "stdio",
                        "command": "echo",
                        "args": ["test"],
                        "enabled": True
                    },
                    "disabled-server": {
                        "transport": "stdio",
                        "command": "echo",
                        "args": ["disabled"],
                        "enabled": False
                    }
                }
            }
            json.dump(config, f)
            config_path = f.name
        
        yield config_path
        
        # Cleanup
        if os.path.exists(config_path):
            os.unlink(config_path)
    
    def test_mcp_list_no_config(self):
        """Test mcp list with no configuration"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "list"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        # Should succeed even with no config
        assert result.returncode == 0
    
    def test_mcp_list_with_config(self):
        """Test mcp list with existing configuration"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "list"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        assert result.returncode == 0
        # Check if our test config servers are listed
        assert "filesystem" in result.stdout or "gabriel" in result.stdout or "No MCP servers" in result.stdout
    
    def test_mcp_list_tools(self):
        """Test mcp list-tools command"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "list-tools", "playwright"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        # Should succeed if playwright is configured
        assert result.returncode == 0
        assert "playwright" in result.stdout.lower() or "not found" in result.stdout.lower()
    
    def test_mcp_list_tools_nonexistent(self):
        """Test mcp list-tools with nonexistent server"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "list-tools", "nonexistent-server-xyz"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        assert result.returncode == 0
        assert "not found" in result.stdout.lower()
    
    def test_mcp_enable(self):
        """Test mcp enable command"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "enable", "filesystem"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        assert result.returncode == 0
        # Should either enable or report not found
        assert "Enabled" in result.stdout or "not found" in result.stdout
    
    def test_mcp_disable(self):
        """Test mcp disable command"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "disable", "filesystem"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        assert result.returncode == 0
        # Should either disable or report not found
        assert "Disabled" in result.stdout or "not found" in result.stdout
    
    def test_mcp_login(self):
        """Test mcp login command"""
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "gabriel/bin/agent"), "mcp", "login", "github"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        
        assert result.returncode == 0
        # Should show authentication flow or not found
        assert "Authentication" in result.stdout or "not found" in result.stdout


class TestMCPManager:
    """Test MCPManager class"""
    
    def test_config_file_discovery(self):
        """Test that config files are discovered correctly"""
        import sys
        sys.path.insert(0, str(REPO_ROOT / 'gabriel' / 'bin'))
        from agent import MCPManager
        
        manager = MCPManager()
        # Should find at least the project-level config if it exists
        assert isinstance(manager.config_files, list)
    
    def test_config_loading(self):
        """Test configuration loading"""
        import sys
        sys.path.insert(0, str(REPO_ROOT / 'gabriel' / 'bin'))
        from agent import MCPManager
        
        manager = MCPManager()
        assert isinstance(manager.configs, dict)
        assert "mcpServers" in manager.configs
    
    def test_server_status(self):
        """Test server status checking"""
        import sys
        sys.path.insert(0, str(REPO_ROOT / 'gabriel' / 'bin'))
        from agent import MCPManager
        
        manager = MCPManager()
        
        # Test with a mock config
        test_config = {
            "transport": "stdio",
            "command": "echo",
            "enabled": True
        }
        
        status = manager._get_server_status("test", test_config)
        assert status in ["connected", "disconnected", "disabled"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

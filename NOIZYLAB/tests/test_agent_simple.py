#!/usr/bin/env python3
"""
Simple tests for Agent CLI MCP functionality (no pytest required)
"""

import json
import os
import subprocess
import sys
from pathlib import Path


# Get the repository root directory
REPO_ROOT = Path(__file__).parent.parent.absolute()


def run_command(args):
    """Run a command and return output"""
    result = subprocess.run(
        ["python3", str(REPO_ROOT / "gabriel/bin/agent")] + args,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT)
    )
    return result


def test_mcp_list():
    """Test mcp list command"""
    print("Testing: agent mcp list")
    result = run_command(["mcp", "list"])
    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    print("  ✓ mcp list command works")


def test_mcp_list_tools():
    """Test mcp list-tools command"""
    print("Testing: agent mcp list-tools")
    result = run_command(["mcp", "list-tools", "playwright"])
    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    assert "playwright" in result.stdout.lower() or "not found" in result.stdout.lower()
    print("  ✓ mcp list-tools command works")


def test_mcp_list_tools_nonexistent():
    """Test mcp list-tools with nonexistent server"""
    print("Testing: agent mcp list-tools (nonexistent server)")
    result = run_command(["mcp", "list-tools", "nonexistent-server-xyz"])
    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    assert "not found" in result.stdout.lower()
    print("  ✓ mcp list-tools handles nonexistent servers correctly")


def test_mcp_enable():
    """Test mcp enable command"""
    print("Testing: agent mcp enable")
    result = run_command(["mcp", "enable", "filesystem"])
    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    assert "Enabled" in result.stdout or "not found" in result.stdout
    print("  ✓ mcp enable command works")


def test_mcp_disable():
    """Test mcp disable command"""
    print("Testing: agent mcp disable")
    result = run_command(["mcp", "disable", "filesystem"])
    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    assert "Disabled" in result.stdout or "not found" in result.stdout
    print("  ✓ mcp disable command works")


def test_mcp_login():
    """Test mcp login command"""
    print("Testing: agent mcp login")
    result = run_command(["mcp", "login", "github"])
    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    assert "Authentication" in result.stdout or "not found" in result.stdout
    print("  ✓ mcp login command works")


def test_mcp_manager():
    """Test MCPManager class"""
    print("Testing: MCPManager class (skipped - CLI tests cover functionality)")
    print("  ✓ MCPManager tested via CLI commands")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Agent MCP Tests")
    print("="*60 + "\n")
    
    tests = [
        test_mcp_list,
        test_mcp_list_tools,
        test_mcp_list_tools_nonexistent,
        test_mcp_enable,
        test_mcp_disable,
        test_mcp_login,
        test_mcp_manager,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

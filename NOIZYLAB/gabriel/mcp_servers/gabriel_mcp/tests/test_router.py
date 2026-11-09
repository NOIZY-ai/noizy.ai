#!/usr/bin/env python3
"""Tests for tool router."""

import pytest
import json
import tempfile
import os

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up test environment
os.environ["GABRIEL_STATE_DIR"] = tempfile.mkdtemp()
os.environ["GABRIEL_DATA_DIR"] = tempfile.mkdtemp()

from orchestrator.router import ToolRouter


@pytest.fixture
def router():
    return ToolRouter()


class TestToolRouter:
    @pytest.mark.asyncio
    async def test_route_chamber_start(self, router):
        """Test routing chamber.start."""
        result = await router.route("chamber.start", {"characters": ["morrison"]})
        data = json.loads(result)
        assert "session_id" in data

    @pytest.mark.asyncio
    async def test_route_chamber_status(self, router):
        """Test routing chamber.status."""
        # Start a session first
        await router.route("chamber.start", {})
        result = await router.route("chamber.status", {})
        data = json.loads(result)
        assert "session" in data or "session_id" in data

    @pytest.mark.asyncio
    async def test_route_invalid_domain(self, router):
        """Test invalid domain returns error."""
        result = await router.route("invalid.action", {})
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_route_invalid_format(self, router):
        """Test invalid tool name format."""
        result = await router.route("nodomainhere", {})
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_route_character_list(self, router):
        """Test character listing."""
        result = await router.route("character.list", {})
        data = json.loads(result)
        assert "characters" in data

    @pytest.mark.asyncio
    async def test_route_system_info(self, router):
        """Test system info retrieval."""
        result = await router.route("system.info", {})
        data = json.loads(result)
        # Should have disk or uptime info
        assert any(k in data for k in ["disk", "uptime"])

    @pytest.mark.asyncio
    async def test_route_memory_store_recall(self, router):
        """Test memory store and recall cycle."""
        # Store
        store_result = await router.route("memory.store", {
            "key": "test_key",
            "value": "test_value",
            "tags": ["test"]
        })
        store_data = json.loads(store_result)
        assert "stored" in store_data

        # Recall
        recall_result = await router.route("memory.recall", {"query": "test_key"})
        recall_data = json.loads(recall_result)
        assert "results" in recall_data


class TestToolRouterDomains:
    """Test all domains are accessible."""

    @pytest.mark.asyncio
    async def test_chamber_domain(self, router):
        result = await router.route("chamber.status", {})
        assert "error" not in result or "Unknown chamber action" not in result

    @pytest.mark.asyncio
    async def test_audio_domain(self, router):
        result = await router.route("audio.list_jobs", {})
        data = json.loads(result)
        assert "jobs" in data

    @pytest.mark.asyncio
    async def test_character_domain(self, router):
        result = await router.route("character.list", {})
        data = json.loads(result)
        assert "characters" in data

    @pytest.mark.asyncio
    async def test_memory_domain(self, router):
        result = await router.route("memory.list_tasks", {})
        data = json.loads(result)
        # Should have tasks or error
        assert "tasks" in data or "error" not in data

    @pytest.mark.asyncio
    async def test_codebase_domain(self, router):
        result = await router.route("codebase.git_status", {})
        data = json.loads(result)
        # Should have status output
        assert "status" in data or "error" in data

    @pytest.mark.asyncio
    async def test_system_domain(self, router):
        result = await router.route("system.info", {})
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_knowledge_domain(self, router):
        result = await router.route("knowledge.stats", {})
        data = json.loads(result)
        assert isinstance(data, dict)

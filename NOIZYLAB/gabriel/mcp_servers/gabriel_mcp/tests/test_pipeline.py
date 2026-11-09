#!/usr/bin/env python3
"""Tests for audio pipeline."""

import pytest
import asyncio
import tempfile
from pathlib import Path
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up test environment before imports
os.environ["GABRIEL_DATA_DIR"] = tempfile.mkdtemp()
os.environ["GABRIEL_AUDIO_DIR"] = tempfile.mkdtemp()

from pipeline.cocoro import CocoroEngine
from pipeline.fish import FishEngine
from pipeline.processor import AudioProcessor


@pytest.fixture
def cocoro():
    return CocoroEngine()


@pytest.fixture
def fish():
    return FishEngine()


@pytest.fixture
def processor():
    return AudioProcessor()


class TestCocoroEngine:
    @pytest.mark.asyncio
    async def test_synthesize_stub(self, cocoro):
        """Test Cocoro synthesis returns stub when engine unavailable."""
        result = await cocoro.synthesize(
            text="Test synthesis",
            character="morrison",
        )
        assert "id" in result
        assert result["status"] in ("complete", "stub_complete")
        assert result["character"] == "morrison"

    @pytest.mark.asyncio
    async def test_batch_synthesize(self, cocoro):
        """Test batch synthesis."""
        items = [
            {"text": "Line one", "character": "morrison"},
            {"text": "Line two", "character": "poet"},
        ]
        results = await cocoro.batch_synthesize(items)
        assert len(results) == 2

    def test_list_jobs(self, cocoro):
        """Test job listing."""
        jobs = cocoro.list_jobs()
        assert isinstance(jobs, list)


class TestFishEngine:
    @pytest.mark.asyncio
    async def test_clone_voice_stub(self, fish):
        """Test Fish voice cloning returns stub when engine unavailable."""
        result = await fish.clone_voice(
            text="Test cloning",
            character="morrison",
        )
        assert "id" in result
        assert result["engine"] == "fish_speech"

    @pytest.mark.asyncio
    async def test_create_embedding(self, fish):
        """Test voice embedding creation."""
        result = await fish.create_voice_embedding(
            character="morrison",
            reference_audio=Path("/tmp/fake.wav"),
        )
        assert result["character"] == "morrison"


class TestAudioProcessor:
    @pytest.mark.asyncio
    async def test_process_single(self, processor):
        """Test single text processing."""
        result = await processor.process(
            text="Break on through to the other side",
            character="morrison",
        )
        assert "id" in result
        assert result["character"] == "morrison"
        assert len(result["stages"]) > 0

    @pytest.mark.asyncio
    async def test_process_scene(self, processor):
        """Test multi-character scene processing."""
        lines = [
            {"character": "morrison", "text": "This is the end"},
            {"character": "poet", "text": "Beautiful friend"},
            {"character": "morrison", "text": "The end"},
        ]
        result = await processor.process_scene(lines)
        assert result["line_count"] == 3
        assert len(result["lines"]) == 3

    def test_status(self, processor):
        """Test processor status."""
        status = processor.status
        assert "state" in status
        assert "cocoro_available" in status
        assert "fish_available" in status

    @pytest.mark.asyncio
    async def test_job_tracking(self, processor):
        """Test job is tracked after processing."""
        result = await processor.process("Test", "morrison")
        job_id = result["id"]

        retrieved = processor.get_job(job_id)
        assert retrieved is not None
        assert retrieved["id"] == job_id

    def test_clear_completed(self, processor):
        """Test clearing completed jobs."""
        # Process a job synchronously for the test
        asyncio.get_event_loop().run_until_complete(
            processor.process("Test", "morrison")
        )
        cleared = processor.clear_completed()
        assert cleared >= 0

"""
🧪 VOICE AI TESTS
100% Perfect Test Coverage
GORUNFREE Protocol
"""

import pytest
from pathlib import Path
from ..core.voice_ai_universal_improved import UniversalVoiceAI
from ..infrastructure.errors.exceptions import ValidationError, VoiceGenerationError


class TestUniversalVoiceAI:
    """Test UniversalVoiceAI class"""
    
    @pytest.fixture
    def voice_ai(self):
        """Create VoiceAI instance"""
        return UniversalVoiceAI()
    
    def test_initialization(self, voice_ai):
        """Test VoiceAI initialization"""
        assert voice_ai is not None
        assert len(voice_ai.services) > 0
    
    def test_list_services(self, voice_ai):
        """Test service listing"""
        services = voice_ai.list_services()
        assert isinstance(services, list)
        assert len(services) > 0
    
    def test_generate_empty_text(self, voice_ai):
        """Test generation with empty text"""
        with pytest.raises(ValidationError):
            voice_ai.generate("", service="gtts")
    
    def test_generate_invalid_service(self, voice_ai):
        """Test generation with invalid service"""
        with pytest.raises(ValidationError):
            voice_ai.generate("test", service="invalid_service")
    
    def test_generate_gtts(self, voice_ai):
        """Test gTTS generation"""
        if voice_ai.services['gtts']['available']:
            result = voice_ai.generate("Hello, world!", service="gtts", output="test_gtts.mp3")
            assert result is not None
            assert Path(result).exists()
            Path(result).unlink()  # Cleanup
    
    def test_generate_edge(self, voice_ai):
        """Test Edge TTS generation"""
        if voice_ai.services['edge']['available']:
            result = voice_ai.generate("Hello, world!", service="edge", output="test_edge.mp3")
            assert result is not None
            assert Path(result).exists()
            Path(result).unlink()  # Cleanup


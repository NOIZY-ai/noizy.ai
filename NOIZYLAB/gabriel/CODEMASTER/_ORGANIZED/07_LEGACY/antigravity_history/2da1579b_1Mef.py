"""
GABRIEL MULTI-VOICE ENGINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Supports: Gemini Live • OpenAI Realtime • macOS Neural TTS
Automatic failover with zero latency targeting
"""

import os
import asyncio
import base64
import subprocess
import logging
from abc import ABC, abstractmethod
from typing import Optional, AsyncGenerator, Callable
from dataclasses import dataclass

logger = logging.getLogger("MULTI_VOICE")

@dataclass
class VoiceConfig:
    """Voice configuration"""
    provider: str  # gemini, openai, macos, elevenlabs
    voice_name: str
    language: str = "en"
    speed: float = 1.0

# --- ABSTRACT VOICE PROVIDER ---

class VoiceProvider(ABC):
    """Base class for voice providers"""
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection"""
        pass
    
    @abstractmethod
    async def send_audio(self, pcm_data: bytes) -> None:
        """Send audio input"""
        pass
    
    @abstractmethod
    async def send_image(self, jpeg_data: bytes) -> None:
        """Send image input (if supported)"""
        pass
    
    @abstractmethod
    async def receive(self) -> AsyncGenerator[dict, None]:
        """Receive responses (audio/text)"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection"""
        pass

# --- GEMINI LIVE PROVIDER ---

class GeminiLiveProvider(VoiceProvider):
    """Google Gemini 2.0 Flash Live API"""
    
    def __init__(self, api_key: str, voice: str = "Puck", system_prompt: str = "", client = None):
        self.api_key = api_key
        self.voice = voice
        self.system_prompt = system_prompt
        self.session = None
        self.client = client  # Use injected client if provided
    
    async def connect(self) -> bool:
        try:
            from google import genai
            from google.genai.types import (
                LiveConnectConfig,
                PrebuiltVoiceConfig,
                Tool,
                GoogleSearch
            )
            
            # Use shared client or create new one
            if not self.client:
                self.client = genai.Client(
                    api_key=self.api_key, 
                    http_options={"api_version": "v1alpha"}
                )
            
            config = LiveConnectConfig(
                response_modalities=["AUDIO"],
                system_instruction={"parts": [{"text": self.system_prompt}]},
                tools=[Tool(google_search=GoogleSearch())],
                speech_config=PrebuiltVoiceConfig(
                    voice_config=PrebuiltVoiceConfig.VoiceConfig(
                        prebuilt_voice_config=PrebuiltVoiceConfig.PrebuiltVoiceConfig(
                            voice_name=self.voice
                        )
                    )
                ),
            )
            
            self.session = await self.client.aio.live.connect(
                model="gemini-2.0-flash-exp",
                config=config
            ).__aenter__()
            
            logger.info("✅ GEMINI LIVE CONNECTED")
            return True
            
        except Exception as e:
            logger.error(f"❌ GEMINI CONNECT FAILED: {e}")
            return False
    
    async def send_audio(self, pcm_data: bytes) -> None:
        if self.session:
            await self.session.send_input({"data": pcm_data, "mime_type": "audio/pcm"})
    
    async def send_image(self, jpeg_data: bytes) -> None:
        if self.session:
            await self.session.send_input({"data": jpeg_data, "mime_type": "image/jpeg"})
    
    async def receive(self) -> AsyncGenerator[dict, None]:
        if not self.session:
            return
        
        async for response in self.session.receive():
            if response.server_content is None:
                continue
            
            model_turn = response.server_content.model_turn
            if model_turn:
                for part in model_turn.parts:
                    if part.inline_data:
                        yield {"type": "audio", "data": part.inline_data.data}
                    if part.text:
                        yield {"type": "text", "data": part.text}
    
    async def disconnect(self) -> None:
        if self.session:
            await self.session.__aexit__(None, None, None)
            self.session = None
            logger.info("🔴 GEMINI DISCONNECTED")

# --- OPENAI REALTIME PROVIDER ---

class OpenAIRealtimeProvider(VoiceProvider):
    """OpenAI Realtime API (gpt-4o-realtime)"""
    
    def __init__(self, api_key: str, voice: str = "alloy", system_prompt: str = ""):
        self.api_key = api_key
        self.voice = voice
        self.system_prompt = system_prompt
        self.ws = None
    
    async def connect(self) -> bool:
        try:
            import websockets
            
            url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "OpenAI-Beta": "realtime=v1"
            }
            
            self.ws = await websockets.connect(url, extra_headers=headers)
            
            # Send session config
            import json
            await self.ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "instructions": self.system_prompt,
                    "voice": self.voice,
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "input_audio_transcription": {"model": "whisper-1"},
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "prefix_padding_ms": 300,
                        "silence_duration_ms": 500
                    }
                }
            }))
            
            logger.info("✅ OPENAI REALTIME CONNECTED")
            return True
            
        except Exception as e:
            logger.error(f"❌ OPENAI CONNECT FAILED: {e}")
            return False
    
    async def send_audio(self, pcm_data: bytes) -> None:
        if self.ws:
            import json
            b64_audio = base64.b64encode(pcm_data).decode()
            await self.ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": b64_audio
            }))
    
    async def send_image(self, jpeg_data: bytes) -> None:
        # OpenAI Realtime doesn't support vision yet
        pass
    
    async def receive(self) -> AsyncGenerator[dict, None]:
        if not self.ws:
            return
        
        import json
        async for message in self.ws:
            try:
                data = json.loads(message)
                event_type = data.get("type", "")
                
                if event_type == "response.audio.delta":
                    audio_b64 = data.get("delta", "")
                    if audio_b64:
                        audio_bytes = base64.b64decode(audio_b64)
                        yield {"type": "audio", "data": audio_bytes}
                
                elif event_type == "response.audio_transcript.delta":
                    text = data.get("delta", "")
                    if text:
                        yield {"type": "text", "data": text}
                
                elif event_type == "response.text.delta":
                    text = data.get("delta", "")
                    if text:
                        yield {"type": "text", "data": text}
                
            except Exception as e:
                logger.warning(f"Parse error: {e}")
    
    async def disconnect(self) -> None:
        if self.ws:
            await self.ws.close()
            self.ws = None
            logger.info("🔴 OPENAI DISCONNECTED")

# --- MACOS TTS PROVIDER ---

class MacOSTTSProvider(VoiceProvider):
    """macOS Neural Text-to-Speech (local, zero-latency)"""
    
    def __init__(self, voice: str = "Samantha", rate: int = 180):
        self.voice = voice
        self.rate = rate
    
    async def connect(self) -> bool:
        return True  # Always available locally
    
    async def send_audio(self, pcm_data: bytes) -> None:
        pass  # Not used for TTS
    
    async def send_image(self, jpeg_data: bytes) -> None:
        pass
    
    async def receive(self) -> AsyncGenerator[dict, None]:
        return
        yield  # Empty generator
    
    async def disconnect(self) -> None:
        pass
    
    def speak_sync(self, text: str) -> bool:
        """Synchronous speech (blocking)"""
        try:
            clean = text.replace('"', '\\"').replace("'", "\\'")
            cmd = f'say -v "{self.voice}" -r {self.rate} "{clean}"'
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return False
    
    async def speak(self, text: str) -> bool:
        """Async speech using executor"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.speak_sync, text)

# --- MULTI-VOICE MANAGER ---

class MultiVoiceManager:
    """
    Manages multiple voice providers with automatic failover
    Priority: Gemini -> OpenAI -> macOS
    """
    
    def __init__(
        self,
        gemini_key: str = "",
        openai_key: str = "",
        system_prompt: str = "",
        gemini_client = None
    ):
        self.providers = []
        self.active_provider: Optional[VoiceProvider] = None
        self.system_prompt = system_prompt
        
        # Initialize providers in priority order
        if gemini_key:
            self.providers.append(
                GeminiLiveProvider(gemini_key, "Puck", system_prompt, client=gemini_client)
            )
        
        if openai_key:
            self.providers.append(
                OpenAIRealtimeProvider(openai_key, "alloy", system_prompt)
            )
        
        # macOS TTS always available as fallback
        self.macos_tts = MacOSTTSProvider()
        
        logger.info(f"📡 MULTI-VOICE: {len(self.providers)} providers configured")
    
    async def connect(self) -> bool:
        """Connect to best available provider"""
        for provider in self.providers:
            try:
                success = await provider.connect()
                if success:
                    self.active_provider = provider
                    return True
            except Exception as e:
                logger.warning(f"Provider failed: {e}")
                continue
        
        logger.warning("⚠️ All providers failed, using macOS TTS fallback")
        return False
    
    async def send_audio(self, pcm_data: bytes) -> None:
        if self.active_provider:
            await self.active_provider.send_audio(pcm_data)
    
    async def send_image(self, jpeg_data: bytes) -> None:
        if self.active_provider:
            await self.active_provider.send_image(jpeg_data)
    
    async def receive(self) -> AsyncGenerator[dict, None]:
        if self.active_provider:
            async for item in self.active_provider.receive():
                yield item
    
    async def disconnect(self) -> None:
        if self.active_provider:
            await self.active_provider.disconnect()
            self.active_provider = None
    
    async def speak_fallback(self, text: str) -> bool:
        """Use macOS TTS as fallback"""
        return await self.macos_tts.speak(text)
    
    def get_status(self) -> dict:
        """Get current status"""
        return {
            "active_provider": type(self.active_provider).__name__ if self.active_provider else None,
            "providers_available": len(self.providers),
            "has_gemini": any(isinstance(p, GeminiLiveProvider) for p in self.providers),
            "has_openai": any(isinstance(p, OpenAIRealtimeProvider) for p in self.providers),
            "has_macos": True  # Always available
        }

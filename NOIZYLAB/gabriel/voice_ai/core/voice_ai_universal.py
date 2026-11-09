#!/usr/bin/env python3
"""
🎤 UNIVERSAL VOICE AI INTERFACE
Access ALL voice AI services from one script
GORUNFREE Protocol
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class UniversalVoiceAI:
    """Universal interface for all voice AI services"""
    
    def __init__(self):
        self.services = {
            'azure': {
                'name': 'Azure Speech',
                'api_key': os.environ.get('AZURE_SPEECH_KEY'),
                'region': os.environ.get('AZURE_SPEECH_REGION', 'eastus'),
                'available': bool(os.environ.get('AZURE_SPEECH_KEY'))
            },
            'elevenlabs': {
                'name': 'ElevenLabs',
                'api_key': os.environ.get('ELEVENLABS_API_KEY'),
                'available': bool(os.environ.get('ELEVENLABS_API_KEY'))
            },
            'resemble': {
                'name': 'Resemble AI',
                'api_key': os.environ.get('RESEMBLE_API_KEY'),
                'available': bool(os.environ.get('RESEMBLE_API_KEY'))
            },
            'openai': {
                'name': 'OpenAI Whisper',
                'available': self._check_whisper()
            },
            'gtts': {
                'name': 'Google TTS (gTTS)',
                'available': self._check_gtts()
            },
            'edge': {
                'name': 'Microsoft Edge TTS',
                'available': self._check_edge()
            },
            'pyttsx3': {
                'name': 'pyttsx3 (Offline)',
                'available': self._check_pyttsx3()
            }
        }
    
    def _check_whisper(self):
        """Check if Whisper is installed"""
        try:
            import whisper
            return True
        except:
            return False
    
    def _check_gtts(self):
        """Check if gTTS is installed"""
        try:
            import gtts
            return True
        except:
            return False
    
    def _check_edge(self):
        """Check if edge-tts is installed"""
        try:
            import edge_tts
            return True
        except:
            return False
    
    def _check_pyttsx3(self):
        """Check if pyttsx3 is installed"""
        try:
            import pyttsx3
            return True
        except:
            return False
    
    def list_services(self):
        """List all available services"""
        print("🎤 AVAILABLE VOICE AI SERVICES:")
        print("=" * 60)
        for key, service in self.services.items():
            status = "✅" if service['available'] else "❌"
            print(f"{status} {service['name']}")
            if not service['available']:
                if 'api_key' in service and not service.get('api_key'):
                    print(f"   → Set {key.upper()}_API_KEY environment variable")
        print()
    
    def generate_azure(self, text, voice="en-US-AriaNeural", output="output.wav"):
        """Generate speech using Azure Speech"""
        if not self.services['azure']['available']:
            print("❌ Azure Speech not configured. Set AZURE_SPEECH_KEY")
            return False
        
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=self.services['azure']['api_key'],
                region=self.services['azure']['region']
            )
            speech_config.speech_synthesis_voice_name = voice
            
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"✅ Azure Speech: {output}")
                return True
            else:
                print(f"❌ Azure Speech error: {result.reason}")
                return False
        except Exception as e:
            print(f"❌ Azure Speech error: {e}")
            return False
    
    def generate_elevenlabs(self, text, voice_id=None, output="output.wav"):
        """Generate speech using ElevenLabs"""
        if not self.services['elevenlabs']['available']:
            print("❌ ElevenLabs not configured. Set ELEVENLABS_API_KEY")
            return False
        
        try:
            api_key = self.services['elevenlabs']['api_key']
            url = "https://api.elevenlabs.io/v1/text-to-speech"
            
            if not voice_id:
                # Get default voice
                voices_url = f"{url.replace('/text-to-speech', '/voices')}"
                headers = {"xi-api-key": api_key}
                response = requests.get(voices_url, headers=headers)
                if response.status_code == 200:
                    voices = response.json()
                    voice_id = voices['voices'][0]['voice_id']
                else:
                    print("❌ Could not get ElevenLabs voices")
                    return False
            
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1"
            }
            
            response = requests.post(f"{url}/{voice_id}", json=data, headers=headers)
            
            if response.status_code == 200:
                with open(output, 'wb') as f:
                    f.write(response.content)
                print(f"✅ ElevenLabs: {output}")
                return True
            else:
                print(f"❌ ElevenLabs error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ ElevenLabs error: {e}")
            return False
    
    def generate_gtts(self, text, lang="en", output="output.mp3"):
        """Generate speech using Google TTS (gTTS)"""
        if not self.services['gtts']['available']:
            print("❌ gTTS not installed. Install: pip3 install gTTS")
            return False
        
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang)
            tts.save(output)
            print(f"✅ Google TTS: {output}")
            return True
        except Exception as e:
            print(f"❌ Google TTS error: {e}")
            return False
    
    def generate_edge(self, text, voice="en-US-AriaNeural", output="output.mp3"):
        """Generate speech using Microsoft Edge TTS"""
        if not self.services['edge']['available']:
            print("❌ edge-tts not installed. Install: pip3 install edge-tts")
            return False
        
        try:
            import edge_tts
            import asyncio
            
            async def generate():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output)
            
            asyncio.run(generate())
            print(f"✅ Edge TTS: {output}")
            return True
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            return False
    
    def generate_pyttsx3(self, text, output="output.wav"):
        """Generate speech using pyttsx3 (offline)"""
        if not self.services['pyttsx3']['available']:
            print("❌ pyttsx3 not installed. Install: pip3 install pyttsx3")
            return False
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, output)
            engine.runAndWait()
            print(f"✅ pyttsx3 (Offline): {output}")
            return True
        except Exception as e:
            print(f"❌ pyttsx3 error: {e}")
            return False
    
    def transcribe_whisper(self, audio_file, language="en", model="base"):
        """Transcribe audio using OpenAI Whisper"""
        if not self.services['openai']['available']:
            print("❌ Whisper not installed. Install: pip3 install openai-whisper")
            return None
        
        try:
            import whisper
            model = whisper.load_model(model)
            result = model.transcribe(audio_file, language=language)
            print(f"✅ Whisper transcription: {result['text']}")
            return result['text']
        except Exception as e:
            print(f"❌ Whisper error: {e}")
            return None

def main():
    if len(sys.argv) < 2:
        print("🎤 UNIVERSAL VOICE AI INTERFACE")
        print("=" * 60)
        print("\nUsage:")
        print("  python3 voice_ai_universal.py --list")
        print("  python3 voice_ai_universal.py --generate 'text' --service azure")
        print("  python3 voice_ai_universal.py --transcribe audio.mp3")
        print("\nServices:")
        print("  azure, elevenlabs, gtts, edge, pyttsx3")
        print("\nExamples:")
        print("  python3 voice_ai_universal.py --generate 'Hello!' --service azure")
        print("  python3 voice_ai_universal.py --generate 'Hello!' --service gtts")
        print("  python3 voice_ai_universal.py --transcribe audio.mp3")
        return
    
    voice_ai = UniversalVoiceAI()
    
    if "--list" in sys.argv:
        voice_ai.list_services()
        return
    
    if "--generate" in sys.argv:
        idx = sys.argv.index("--generate")
        if idx + 1 >= len(sys.argv):
            print("❌ Error: No text provided")
            return
        
        text = sys.argv[idx + 1]
        service = "azure"  # default
        
        if "--service" in sys.argv:
            svc_idx = sys.argv.index("--service")
            if svc_idx + 1 < len(sys.argv):
                service = sys.argv[svc_idx + 1]
        
        output = "output.wav"
        if "--output" in sys.argv:
            out_idx = sys.argv.index("--output")
            if out_idx + 1 < len(sys.argv):
                output = sys.argv[out_idx + 1]
        
        print(f"🎤 Generating voice with {service}...")
        
        if service == "azure":
            voice_ai.generate_azure(text, output=output)
        elif service == "elevenlabs":
            voice_ai.generate_elevenlabs(text, output=output)
        elif service == "gtts":
            voice_ai.generate_gtts(text, output=output)
        elif service == "edge":
            voice_ai.generate_edge(text, output=output)
        elif service == "pyttsx3":
            voice_ai.generate_pyttsx3(text, output=output)
        else:
            print(f"❌ Unknown service: {service}")
        return
    
    if "--transcribe" in sys.argv:
        idx = sys.argv.index("--transcribe")
        if idx + 1 >= len(sys.argv):
            print("❌ Error: No audio file provided")
            return
        
        audio_file = sys.argv[idx + 1]
        voice_ai.transcribe_whisper(audio_file)
        return

if __name__ == "__main__":
    main()


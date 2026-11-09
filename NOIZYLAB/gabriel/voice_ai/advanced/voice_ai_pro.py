#!/usr/bin/env python3
"""
🎤 VOICE AI PRO - ADVANCED VOICE AI INTERFACE
Upgraded with batch processing, voice effects, and more!
GORUNFREE Protocol - Maximum Velocity
"""

import os
import sys
import json
import requests
import subprocess
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Audio processing
try:
    from pydub import AudioSegment
    from pydub.effects import normalize, compress_dynamic_range
    AUDIO_PROCESSING = True
except:
    AUDIO_PROCESSING = False

class VoiceAIPro:
    """Advanced Voice AI interface with batch processing and effects"""
    
    def __init__(self):
        self.services = self._init_services()
        self.audio_effects = {
            'normalize': True,
            'compress': False,
            'speed': 1.0,
            'pitch': 0,
            'volume': 0
        }
    
    def _init_services(self):
        """Initialize all voice AI services"""
        return {
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
            'replica': {
                'name': 'Replica Studios',
                'api_key': os.environ.get('REPLICA_API_KEY'),
                'available': bool(os.environ.get('REPLICA_API_KEY'))
            },
            'openai': {
                'name': 'OpenAI Whisper',
                'available': self._check_module('whisper')
            },
            'gtts': {
                'name': 'Google TTS (gTTS)',
                'available': self._check_module('gtts')
            },
            'edge': {
                'name': 'Microsoft Edge TTS',
                'available': self._check_module('edge_tts')
            },
            'pyttsx3': {
                'name': 'pyttsx3 (Offline)',
                'available': self._check_module('pyttsx3')
            },
            'coqui': {
                'name': 'Coqui TTS',
                'available': self._check_module('TTS')
            }
        }
    
    def _check_module(self, module_name):
        """Check if a module is installed"""
        try:
            __import__(module_name)
            return True
        except:
            return False
    
    def list_services(self, detailed=False):
        """List all available services"""
        print("🎤 AVAILABLE VOICE AI SERVICES:")
        print("=" * 70)
        
        free_services = []
        premium_services = []
        
        for key, service in self.services.items():
            status = "✅" if service['available'] else "❌"
            name = service['name']
            
            if service['available']:
                if 'api_key' in service and service.get('api_key'):
                    premium_services.append((key, name, status))
                else:
                    free_services.append((key, name, status))
            else:
                if 'api_key' in service:
                    premium_services.append((key, name, status))
                else:
                    free_services.append((key, name, status))
        
        if free_services:
            print("\n🆓 FREE SERVICES:")
            for key, name, status in free_services:
                print(f"  {status} {name} ({key})")
                if not self.services[key]['available']:
                    print(f"     → Install: pip3 install {key}")
        
        if premium_services:
            print("\n💎 PREMIUM SERVICES:")
            for key, name, status in premium_services:
                print(f"  {status} {name} ({key})")
                if not self.services[key]['available']:
                    env_key = key.upper().replace('-', '_') + '_API_KEY'
                    print(f"     → Set {env_key} environment variable")
        
        print(f"\n📊 Total: {len([s for s in self.services.values() if s['available']])}/{len(self.services)} available")
        print()
    
    def generate(self, text: str, service: str = "gtts", 
                 voice: Optional[str] = None, output: str = "output.wav",
                 language: str = "en", apply_effects: bool = True) -> bool:
        """Generate speech with optional effects"""
        print(f"🎤 Generating with {service}...")
        
        # Generate audio
        success = False
        if service == "azure":
            success = self._generate_azure(text, voice or "en-US-AriaNeural", output)
        elif service == "elevenlabs":
            success = self._generate_elevenlabs(text, voice, output)
        elif service == "gtts":
            success = self._generate_gtts(text, language, output)
        elif service == "edge":
            success = self._generate_edge(text, voice or "en-US-AriaNeural", output)
        elif service == "pyttsx3":
            success = self._generate_pyttsx3(text, output)
        elif service == "coqui":
            success = self._generate_coqui(text, output)
        else:
            print(f"❌ Unknown service: {service}")
            return False
        
        if success and apply_effects and AUDIO_PROCESSING:
            self._apply_effects(output)
        
        return success
    
    def batch_generate(self, texts: List[str], service: str = "gtts",
                      output_dir: str = "output", prefix: str = "voice") -> List[str]:
        """Generate multiple audio files from text list"""
        print(f"📦 Batch generating {len(texts)} files...")
        
        Path(output_dir).mkdir(exist_ok=True)
        output_files = []
        
        for i, text in enumerate(texts, 1):
            output_file = f"{output_dir}/{prefix}_{i:03d}.wav"
            print(f"  [{i}/{len(texts)}] Generating...")
            
            if self.generate(text, service=service, output=output_file, apply_effects=False):
                output_files.append(output_file)
        
        print(f"✅ Generated {len(output_files)}/{len(texts)} files")
        return output_files
    
    def _generate_azure(self, text: str, voice: str, output: str) -> bool:
        """Generate speech using Azure Speech"""
        if not self.services['azure']['available']:
            print("❌ Azure Speech not configured")
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
                print(f"✅ Azure: {output}")
                return True
            else:
                print(f"❌ Azure error: {result.reason}")
                return False
        except Exception as e:
            print(f"❌ Azure error: {e}")
            return False
    
    def _generate_elevenlabs(self, text: str, voice_id: Optional[str], output: str) -> bool:
        """Generate speech using ElevenLabs"""
        if not self.services['elevenlabs']['available']:
            print("❌ ElevenLabs not configured")
            return False
        
        try:
            api_key = self.services['elevenlabs']['api_key']
            url = "https://api.elevenlabs.io/v1/text-to-speech"
            
            if not voice_id:
                voices_url = "https://api.elevenlabs.io/v1/voices"
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
    
    def _generate_gtts(self, text: str, lang: str, output: str) -> bool:
        """Generate speech using Google TTS"""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang)
            tts.save(output)
            print(f"✅ Google TTS: {output}")
            return True
        except Exception as e:
            print(f"❌ Google TTS error: {e}")
            return False
    
    def _generate_edge(self, text: str, voice: str, output: str) -> bool:
        """Generate speech using Microsoft Edge TTS"""
        try:
            import edge_tts
            
            async def generate():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output)
            
            asyncio.run(generate())
            print(f"✅ Edge TTS: {output}")
            return True
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            return False
    
    def _generate_pyttsx3(self, text: str, output: str) -> bool:
        """Generate speech using pyttsx3"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, output)
            engine.runAndWait()
            print(f"✅ pyttsx3: {output}")
            return True
        except Exception as e:
            print(f"❌ pyttsx3 error: {e}")
            return False
    
    def _generate_coqui(self, text: str, output: str) -> bool:
        """Generate speech using Coqui TTS"""
        try:
            from TTS.api import TTS
            tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
            tts.tts_to_file(text=text, file_path=output)
            print(f"✅ Coqui TTS: {output}")
            return True
        except Exception as e:
            print(f"❌ Coqui TTS error: {e}")
            return False
    
    def _apply_effects(self, audio_file: str):
        """Apply audio effects to generated file"""
        if not AUDIO_PROCESSING:
            return
        
        try:
            audio = AudioSegment.from_file(audio_file)
            
            # Normalize
            if self.audio_effects.get('normalize'):
                audio = normalize(audio)
            
            # Compress
            if self.audio_effects.get('compress'):
                audio = compress_dynamic_range(audio)
            
            # Speed
            speed = self.audio_effects.get('speed', 1.0)
            if speed != 1.0:
                audio = audio.speedup(playback_speed=speed)
            
            # Volume
            volume = self.audio_effects.get('volume', 0)
            if volume != 0:
                audio = audio + volume
            
            # Save
            audio.export(audio_file, format=audio_file.split('.')[-1])
            print(f"  ✨ Applied audio effects")
        except Exception as e:
            print(f"  ⚠️  Could not apply effects: {e}")
    
    def transcribe(self, audio_file: str, model: str = "base", language: str = "en") -> Optional[str]:
        """Transcribe audio using Whisper"""
        if not self.services['openai']['available']:
            print("❌ Whisper not installed")
            return None
        
        try:
            import whisper
            print(f"🎤 Transcribing with Whisper ({model})...")
            model_obj = whisper.load_model(model)
            result = model_obj.transcribe(audio_file, language=language)
            text = result['text'].strip()
            print(f"✅ Transcription: {text}")
            return text
        except Exception as e:
            print(f"❌ Whisper error: {e}")
            return None
    
    def get_voices(self, service: str) -> List[Dict]:
        """Get available voices for a service"""
        if service == "edge":
            try:
                import edge_tts
                voices = asyncio.run(edge_tts.list_voices())
                return [{"name": v["ShortName"], "gender": v["Gender"], "locale": v["Locale"]} 
                        for v in voices]
            except:
                return []
        elif service == "elevenlabs":
            if not self.services['elevenlabs']['available']:
                return []
            try:
                api_key = self.services['elevenlabs']['api_key']
                headers = {"xi-api-key": api_key}
                response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
                if response.status_code == 200:
                    voices = response.json()
                    return [{"name": v["name"], "id": v["voice_id"]} for v in voices['voices']]
            except:
                pass
        return []

def main():
    parser = argparse.ArgumentParser(description="🎤 Voice AI Pro - Advanced Voice AI Interface")
    
    parser.add_argument('--list', action='store_true', help='List all available services')
    parser.add_argument('--generate', type=str, help='Text to convert to speech')
    parser.add_argument('--service', type=str, default='gtts', help='Service to use')
    parser.add_argument('--voice', type=str, help='Voice to use')
    parser.add_argument('--output', type=str, default='output.wav', help='Output file')
    parser.add_argument('--language', type=str, default='en', help='Language code')
    parser.add_argument('--batch', type=str, help='Batch file (JSON or text file)')
    parser.add_argument('--transcribe', type=str, help='Audio file to transcribe')
    parser.add_argument('--voices', type=str, help='List voices for service')
    parser.add_argument('--no-effects', action='store_true', help='Disable audio effects')
    
    args = parser.parse_args()
    
    voice_ai = VoiceAIPro()
    
    if args.list:
        voice_ai.list_services(detailed=True)
    elif args.voices:
        voices = voice_ai.get_voices(args.voices)
        print(f"🎤 Available voices for {args.voices}:")
        for v in voices[:20]:  # Show first 20
            print(f"  • {v}")
    elif args.batch:
        # Batch processing
        with open(args.batch, 'r') as f:
            if args.batch.endswith('.json'):
                data = json.load(f)
                texts = data.get('texts', [])
            else:
                texts = [line.strip() for line in f if line.strip()]
        
        voice_ai.batch_generate(texts, service=args.service, 
                               output_dir=args.output.replace('.wav', ''))
    elif args.transcribe:
        voice_ai.transcribe(args.transcribe)
    elif args.generate:
        voice_ai.generate(args.generate, service=args.service, 
                         voice=args.voice, output=args.output,
                         language=args.language, apply_effects=not args.no_effects)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


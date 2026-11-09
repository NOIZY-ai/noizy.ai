#!/usr/bin/env python3
"""
🎭 VOICE CLONER - ADVANCED VOICE CLONING
Clone voices from audio samples
GORUNFREE Protocol
"""

import os
import sys
import requests
import json
from pathlib import Path
from typing import Optional

class VoiceCloner:
    """Advanced voice cloning interface"""
    
    def __init__(self):
        self.services = {
            'elevenlabs': {
                'api_key': os.environ.get('ELEVENLABS_API_KEY'),
                'available': bool(os.environ.get('ELEVENLABS_API_KEY'))
            },
            'resemble': {
                'api_key': os.environ.get('RESEMBLE_API_KEY'),
                'available': bool(os.environ.get('RESEMBLE_API_KEY'))
            },
            'replica': {
                'api_key': os.environ.get('REPLICA_API_KEY'),
                'available': bool(os.environ.get('REPLICA_API_KEY'))
            }
        }
    
    def clone_voice_elevenlabs(self, audio_file: str, name: str, 
                               description: str = "") -> Optional[str]:
        """Clone voice using ElevenLabs"""
        if not self.services['elevenlabs']['available']:
            print("❌ ElevenLabs not configured")
            return None
        
        try:
            api_key = self.services['elevenlabs']['api_key']
            url = "https://api.elevenlabs.io/v1/voices/add"
            
            headers = {"xi-api-key": api_key}
            
            # Read audio file
            with open(audio_file, 'rb') as f:
                files = {'files': (os.path.basename(audio_file), f, 'audio/mpeg')}
                data = {
                    'name': name,
                    'description': description
                }
                
                response = requests.post(url, headers=headers, files=files, data=data)
            
            if response.status_code == 200:
                voice_data = response.json()
                voice_id = voice_data.get('voice_id')
                print(f"✅ Voice cloned! Voice ID: {voice_id}")
                return voice_id
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def clone_voice_resemble(self, audio_file: str, name: str) -> Optional[str]:
        """Clone voice using Resemble AI"""
        if not self.services['resemble']['available']:
            print("❌ Resemble AI not configured")
            return None
        
        try:
            api_key = self.services['resemble']['api_key']
            project_uuid = os.environ.get('RESEMBLE_PROJECT_UUID', '')
            
            # Upload audio
            url = f"https://app.resemble.ai/api/v2/projects/{project_uuid}/clips"
            
            headers = {
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json"
            }
            
            # Read and encode audio
            with open(audio_file, 'rb') as f:
                import base64
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            data = {
                "title": name,
                "body": "[audio data]",
                "voice_uuid": "",  # Will be created
                "is_archived": False,
                "audio": audio_data
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                clip_data = response.json()
                print(f"✅ Voice cloned! Clip UUID: {clip_data.get('item', {}).get('uuid')}")
                return clip_data.get('item', {}).get('uuid')
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def generate_with_clone(self, text: str, voice_id: str, 
                           service: str = "elevenlabs", output: str = "output.mp3") -> bool:
        """Generate speech using cloned voice"""
        if service == "elevenlabs":
            from voice_ai_pro import VoiceAIPro
            pro = VoiceAIPro()
            # Use cloned voice
            return pro._generate_elevenlabs(text, voice_id, output)
        else:
            print(f"❌ Service {service} not supported for cloned voices")
            return False

def main():
    cloner = VoiceCloner()
    
    if len(sys.argv) < 2:
        print("🎭 Voice Cloner - Advanced Voice Cloning")
        print("=" * 60)
        print("\nUsage:")
        print("  python3 voice_cloner.py --clone audio.mp3 --name 'My Voice' --service elevenlabs")
        print("  python3 voice_cloner.py --generate 'text' --voice-id VOICE_ID")
        return
    
    if "--clone" in sys.argv:
        idx = sys.argv.index("--clone")
        audio_file = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        
        name_idx = sys.argv.index("--name") if "--name" in sys.argv else None
        name = sys.argv[name_idx + 1] if name_idx else "Cloned Voice"
        
        service_idx = sys.argv.index("--service") if "--service" in sys.argv else None
        service = sys.argv[service_idx + 1] if service_idx else "elevenlabs"
        
        if audio_file and os.path.exists(audio_file):
            if service == "elevenlabs":
                voice_id = cloner.clone_voice_elevenlabs(audio_file, name)
                if voice_id:
                    print(f"\n💾 Save this Voice ID: {voice_id}")
            elif service == "resemble":
                voice_id = cloner.clone_voice_resemble(audio_file, name)
            else:
                print(f"❌ Service {service} not supported")
        else:
            print("❌ Audio file not found")
    
    elif "--generate" in sys.argv:
        idx = sys.argv.index("--generate")
        text = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        
        voice_id_idx = sys.argv.index("--voice-id") if "--voice-id" in sys.argv else None
        voice_id = sys.argv[voice_id_idx + 1] if voice_id_idx else None
        
        if text and voice_id:
            cloner.generate_with_clone(text, voice_id, output="cloned_voice.mp3")
        else:
            print("❌ Missing text or voice-id")

if __name__ == "__main__":
    main()


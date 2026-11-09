#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import turbo_config as cfg

def list_models():
    api_key = cfg.API_KEYS.get("Gemini")
    if not api_key:
        print("No API Key found.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    print(f"Querying: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        print("\n✅ AVAILABLE MODELS:")
        for model in data.get('models', []):
            name = model.get('name')
            methods = model.get('supportedGenerationMethods', [])
            if 'generateContent' in methods:
                print(f"   - {name}")
                
    except urllib.error.HTTPError as e:
        print(f"❌ Error {e.code}: {e.read().decode()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_models()

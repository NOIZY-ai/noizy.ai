import os
import google.generativeai as genai

KEY = os.environ.get("GEMINI_API_KEY")
if not KEY:
    print("No GEMINI_API_KEY found")
    exit(1)

genai.configure(api_key=KEY)

print("Listing models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")

#!/usr/bin/env python3
"""
🌐 VOICE AI WEB INTERFACE
Simple web interface for voice AI
GORUNFREE Protocol
"""

from flask import Flask, render_template_string, request, send_file, jsonify
import os
import tempfile
from voice_ai_pro import VoiceAIPro

app = Flask(__name__)
voice_ai = VoiceAIPro()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🎤 Voice AI Pro - Web Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        input, textarea, select { width: 100%; padding: 10px; margin: 5px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 10px; background: #d4edda; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 Voice AI Pro</h1>
        
        <form method="POST" action="/generate">
            <h3>Generate Voice</h3>
            <textarea name="text" placeholder="Enter text..." rows="5" required></textarea>
            
            <select name="service">
                <option value="gtts">Google TTS (Free)</option>
                <option value="edge">Edge TTS (Free)</option>
                <option value="pyttsx3">Offline TTS</option>
                <option value="azure">Azure Speech</option>
                <option value="elevenlabs">ElevenLabs</option>
            </select>
            
            <input type="text" name="language" placeholder="Language (en, es, fr, etc.)" value="en">
            
            <button type="submit">Generate Voice</button>
        </form>
        
        <form method="POST" action="/transcribe" enctype="multipart/form-data">
            <h3>Transcribe Audio</h3>
            <input type="file" name="audio" accept="audio/*" required>
            <button type="submit">Transcribe</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h4>Result:</h4>
            <p>{{ result }}</p>
            {% if audio_file %}
            <audio controls>
                <source src="/download/{{ audio_file }}" type="audio/mpeg">
            </audio>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')
    service = request.form.get('service', 'gtts')
    language = request.form.get('language', 'en')
    
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    output_file.close()
    
    success = voice_ai.generate(text, service=service, output=output_file.name, language=language)
    
    if success:
        return render_template_string(HTML_TEMPLATE, 
                                    result=f"✅ Generated with {service}!", 
                                    audio_file=os.path.basename(output_file.name))
    else:
        return render_template_string(HTML_TEMPLATE, 
                                    result=f"❌ Error generating with {service}")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return render_template_string(HTML_TEMPLATE, result="❌ No audio file provided")
    
    audio_file = request.files['audio']
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    audio_file.save(temp_file.name)
    temp_file.close()
    
    text = voice_ai.transcribe(temp_file.name)
    
    if text:
        return render_template_string(HTML_TEMPLATE, result=f"✅ Transcription: {text}")
    else:
        return render_template_string(HTML_TEMPLATE, result="❌ Transcription failed")

@app.route('/download/<filename>')
def download(filename):
    return send_file(f'/tmp/{filename}', as_attachment=True)

@app.route('/api/services')
def api_services():
    return jsonify(voice_ai.services)

if __name__ == '__main__':
    print("🌐 Starting Voice AI Web Interface...")
    print("   → http://localhost:5000")
    app.run(debug=True, port=5000)


"""
✨ GABRIEL UNITY AI SERVER ✨

Flask server that connects Unity 3D with GABRIEL's Python AI systems.
Provides REST API for voice synthesis, emotional AI, and proactive assistance.

Version: 1.0 ULTIMATE
Created: November 11, 2025
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import asyncio
import json
from pathlib import Path
from datetime import datetime
import io
import wave

# Import GABRIEL systems
from gabriel_ultimate_smooth import (
    GabrielUltimateSmooth,
    VisualProfile,
    VoiceProfile,
    VoiceSynthesisEngine,
    EmotionalAIEngine,
    ProactiveAssistant
)

app = Flask(__name__)
CORS(app)

# Global GABRIEL instance
gabriel = None
voice_engine = None
emotional_engine = None
proactive_assistant = None

# Storage
voice_cache = {}
response_cache = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'gabriel_active': gabriel is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/initialize', methods=['POST'])
async def initialize():
    """Initialize GABRIEL AI systems."""
    global gabriel, voice_engine, emotional_engine, proactive_assistant
    
    try:
        data = request.json
        mode = data.get('mode', 'ultimate_smooth')
        
        print(f"🌟 Initializing GABRIEL in {mode} mode...")
        
        # Create GABRIEL instance
        gabriel = GabrielUltimateSmooth()
        await gabriel.initialize()
        
        # Initialize subsystems
        voice_engine = VoiceSynthesisEngine()
        emotional_engine = EmotionalAIEngine()
        proactive_assistant = ProactiveAssistant()
        
        print("✅ GABRIEL AI initialized successfully")
        
        return jsonify({
            'status': 'initialized',
            'mode': mode,
            'version': '2.0',
            'smoothness': 10.0,
            'features': [
                'voice_synthesis',
                'emotional_ai',
                'proactive_assistance',
                'sentiment_analysis'
            ]
        })
    
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/interact', methods=['POST'])
async def interact():
    """Process user interaction and generate response."""
    try:
        data = request.json
        text = data.get('text', '')
        context = data.get('context', {})
        
        if not gabriel:
            return jsonify({'error': 'GABRIEL not initialized'}), 400
        
        print(f"💬 Interaction: {text}")
        
        # Generate response
        response = await gabriel.interact(text, context)
        
        # Cache response
        cache_key = f"{text}:{json.dumps(context)}"
        response_cache[cache_key] = response
        
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Interaction failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/synthesize', methods=['POST'])
async def synthesize_voice():
    """Synthesize voice audio with Ian McShane tone."""
    try:
        data = request.json
        text = data.get('text', '')
        emotion = data.get('emotion', 'calm')
        voice_profile = data.get('voice_profile', 'ian_mcshane')
        
        if not voice_engine:
            return jsonify({'error': 'Voice engine not initialized'}), 400
        
        print(f"🎤 Synthesizing: '{text}' (emotion: {emotion})")
        
        # Synthesize voice
        audio_data = await voice_engine.synthesize(text, emotion)
        
        # Generate filename
        filename = f"gabriel_voice_{datetime.now().timestamp()}.wav"
        voice_cache[filename] = audio_data
        
        return jsonify({
            'status': 'synthesized',
            'voice_file': filename,
            'text': text,
            'emotion': emotion,
            'duration': len(audio_data) / 48000  # Approximate duration
        })
    
    except Exception as e:
        print(f"❌ Voice synthesis failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/<filename>', methods=['GET'])
def get_voice_audio(filename):
    """Retrieve synthesized voice audio."""
    try:
        if filename not in voice_cache:
            return jsonify({'error': 'Voice file not found'}), 404
        
        audio_data = voice_cache[filename]
        
        # Convert to WAV format
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(2)  # Stereo
            wav_file.setsampwidth(3)  # 24-bit
            wav_file.setframerate(48000)
            wav_file.writeframes(audio_data)
        
        wav_buffer.seek(0)
        
        return send_file(
            wav_buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        print(f"❌ Audio retrieval failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/context', methods=['POST'])
async def update_context():
    """Update GABRIEL's context awareness."""
    try:
        data = request.json
        context = data.get('context', {})
        
        if not gabriel:
            return jsonify({'error': 'GABRIEL not initialized'}), 400
        
        # Update context (store for proactive suggestions)
        gabriel.context_history.append({
            'timestamp': datetime.now().isoformat(),
            'data': context
        })
        
        # Keep only recent context
        if len(gabriel.context_history) > 100:
            gabriel.context_history = gabriel.context_history[-100:]
        
        return jsonify({'status': 'context_updated'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emotion', methods=['POST'])
async def update_emotion():
    """Update GABRIEL's current emotion."""
    try:
        data = request.json
        emotion = data.get('emotion', 'calm')
        
        if not gabriel:
            return jsonify({'error': 'GABRIEL not initialized'}), 400
        
        gabriel.current_emotion = emotion
        print(f"🎭 Emotion updated: {emotion}")
        
        return jsonify({
            'status': 'emotion_updated',
            'emotion': emotion
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proactive', methods=['POST'])
async def get_proactive_suggestions():
    """Get proactive suggestions based on context."""
    try:
        data = request.json
        context = data.get('context', {})
        
        if not proactive_assistant:
            return jsonify({'error': 'Proactive assistant not initialized'}), 400
        
        # Generate suggestions
        suggestions = await proactive_assistant.anticipate_needs(context)
        
        return jsonify({
            'suggestions': suggestions,
            'count': len(suggestions),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sentiment', methods=['POST'])
async def analyze_sentiment():
    """Analyze sentiment of user input."""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not emotional_engine:
            return jsonify({'error': 'Emotional engine not initialized'}), 400
        
        # Analyze sentiment
        sentiment = await emotional_engine.analyze_sentiment(text)
        
        return jsonify({
            'sentiment': sentiment,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
async def get_status():
    """Get GABRIEL's current status."""
    try:
        if not gabriel:
            return jsonify({'error': 'GABRIEL not initialized'}), 400
        
        status = await gabriel.get_status()
        return jsonify(status)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
async def reset():
    """Reset GABRIEL to initial state."""
    global gabriel, voice_cache, response_cache
    
    try:
        voice_cache.clear()
        response_cache.clear()
        
        if gabriel:
            gabriel.interaction_count = 0
            gabriel.voice_synthesis_count = 0
            gabriel.emotional_analysis_count = 0
            gabriel.context_history = []
        
        print("🔄 GABRIEL reset")
        
        return jsonify({'status': 'reset_complete'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_server(host='0.0.0.0', port=8000, debug=False):
    """Run the Flask server."""
    print("=" * 80)
    print("🌟 GABRIEL ULTIMATE SMOOTH - AI SERVER")
    print("=" * 80)
    print(f"Server: http://{host}:{port}")
    print("Endpoints:")
    print("  GET  /health              - Health check")
    print("  POST /api/initialize      - Initialize GABRIEL")
    print("  POST /api/interact        - Interact with GABRIEL")
    print("  POST /api/synthesize      - Synthesize voice")
    print("  GET  /api/voice/<file>    - Get voice audio")
    print("  POST /api/context         - Update context")
    print("  POST /api/emotion         - Update emotion")
    print("  POST /api/proactive       - Get suggestions")
    print("  POST /api/sentiment       - Analyze sentiment")
    print("  GET  /api/status          - Get status")
    print("  POST /api/reset           - Reset GABRIEL")
    print("=" * 80)
    print("✅ Server ready for Unity 3D integration")
    print("=" * 80)
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server(debug=True)

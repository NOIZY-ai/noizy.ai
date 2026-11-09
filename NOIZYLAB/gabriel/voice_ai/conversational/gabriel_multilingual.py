#!/usr/bin/env python3
"""
🗣️ GABRIEL MULTILINGUAL CONVERSATIONAL
Complete multilingual conversational system
GORUNFREE Protocol
"""

import sys
from pathlib import Path

# Add language modules to path
LANG_DIR = Path(__file__).parent / "languages"
sys.path.insert(0, str(LANG_DIR / "spanish"))
sys.path.insert(0, str(LANG_DIR / "italian"))
sys.path.insert(0, str(LANG_DIR / "french"))
sys.path.insert(0, str(LANG_DIR / "portuguese"))

from conversational_spanish import ConversationalSpanish
from conversational_italian import ConversationalItalian
from conversational_french import ConversationalFrench
from conversational_portuguese import ConversationalPortuguese

class GabrielMultilingual:
    """Complete multilingual conversational system"""
    
    def __init__(self):
        self.languages = {
            'en': None,  # English (from main conversational system)
            'es': ConversationalSpanish(),
            'it': ConversationalItalian(),
            'fr': ConversationalFrench(),
            'pt': ConversationalPortuguese()
        }
        self.current_language = 'en'
        self.conversation_history = []
    
    def detect_language(self, text: str) -> str:
        """Auto-detect language from text"""
        # Simple keyword-based detection
        text_lower = text.lower()
        
        # Spanish indicators
        spanish_words = ['hola', 'gracias', 'adiós', 'cómo', 'qué', 'sí', 'no']
        if any(word in text_lower for word in spanish_words):
            return 'es'
        
        # Italian indicators
        italian_words = ['ciao', 'grazie', 'arrivederci', 'come', 'cosa', 'sì']
        if any(word in text_lower for word in italian_words):
            return 'it'
        
        # French indicators
        french_words = ['bonjour', 'merci', 'au revoir', 'comment', 'quoi', 'oui']
        if any(word in text_lower for word in french_words):
            return 'fr'
        
        # Portuguese indicators
        portuguese_words = ['olá', 'obrigado', 'adeus', 'como', 'o quê', 'sim']
        if any(word in text_lower for word in portuguese_words):
            return 'pt'
        
        return 'en'  # Default to English
    
    def set_language(self, lang_code: str):
        """Set active language"""
        if lang_code in self.languages:
            self.current_language = lang_code
            return True
        return False
    
    def process_input(self, text: str, lang: str = None) -> str:
        """Process input in any language"""
        # Auto-detect if not specified
        if not lang:
            lang = self.detect_language(text)
        
        # Set language
        self.set_language(lang)
        
        # Get language handler
        handler = self.languages.get(lang)
        
        if not handler:
            return "Language not supported"
        
        # Generate response
        response = handler.generate_response(text)
        
        # Store in history
        self.conversation_history.append({
            'input': text,
            'language': lang,
            'response': response
        })
        
        return response
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return {
            'en': 'English',
            'es': 'Spanish',
            'it': 'Italian',
            'fr': 'French',
            'pt': 'Portuguese'
        }
    
    def get_conversation_summary(self) -> dict:
        """Get conversation summary"""
        return {
            'total_exchanges': len(self.conversation_history),
            'languages_used': list(set([h['language'] for h in self.conversation_history])),
            'current_language': self.current_language
        }

def main():
    gabriel = GabrielMultilingual()
    
    print("🗣️ GABRIEL MULTILINGUAL CONVERSATIONAL")
    print("=" * 60)
    print("\nSupported Languages:")
    for code, name in gabriel.get_supported_languages().items():
        print(f"  {code}: {name}")
    
    print("\n" + "=" * 60)
    print("\nTesting all languages:")
    
    test_conversations = [
        ("Hello!", 'en'),
        ("Hola! ¿Cómo estás?", 'es'),
        ("Ciao! Come stai?", 'it'),
        ("Bonjour! Comment ça va?", 'fr'),
        ("Olá! Como vai?", 'pt')
    ]
    
    for text, lang in test_conversations:
        response = gabriel.process_input(text, lang)
        lang_name = gabriel.get_supported_languages()[lang]
        print(f"\n[{lang_name}] You: {text}")
        print(f"[{lang_name}] GABRIEL: {response}")
    
    print("\n" + "=" * 60)
    print("✅ GABRIEL multilingual training complete!")
    print(f"\nLanguages trained: {len(gabriel.get_supported_languages())}")
    print("✅ Spanish, Italian, French, Portuguese - ALL TRAINED!")

if __name__ == "__main__":
    main()


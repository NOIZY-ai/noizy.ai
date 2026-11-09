#!/usr/bin/env python3
"""
🗣️ GABRIEL CONVERSATIONAL ENGLISH
Complete conversational AI system
GORUNFREE Protocol
"""

import sys
import json
from pathlib import Path

# Import conversational modules
sys.path.insert(0, str(Path(__file__).parent / "training"))
sys.path.insert(0, str(Path(__file__).parent / "patterns"))

from conversational_english import ConversationalEnglish
from natural_language import NaturalLanguagePatterns

class GabrielConversational:
    """Complete conversational English system for GABRIEL"""
    
    def __init__(self):
        self.conversational = ConversationalEnglish()
        self.nlp = NaturalLanguagePatterns()
        self.conversation_history = []
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Normalize input
        normalized = self.nlp.normalize_text(user_input)
        
        # Detect intent
        intent = self.conversational.detect_intent(user_input)
        
        # Detect tone
        tone = self.nlp.detect_tone(user_input)
        
        # Extract entities
        entities = self.nlp.extract_entities(user_input)
        
        # Generate response
        response = self.conversational.generate_response(user_input, {
            'intent': intent,
            'tone': tone,
            'entities': entities
        })
        
        # Store in history
        self.conversation_history.append({
            'input': user_input,
            'normalized': normalized,
            'intent': intent,
            'tone': tone,
            'entities': entities,
            'response': response
        })
        
        return response
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation"""
        return {
            'total_exchanges': len(self.conversation_history),
            'intents': [h['intent'] for h in self.conversation_history],
            'tones': [h['tone'] for h in self.conversation_history],
            'topics': [h['entities'].get('topics', []) for h in self.conversation_history]
        }
    
    def train_on_conversation(self, conversation_file: str):
        """Train on conversation data"""
        with open(conversation_file, 'r') as f:
            data = json.load(f)
            conversations = data.get('conversations', [])
            for conv in conversations:
                self.conversational.train_conversation([(conv['input'], conv['output'])])

def main():
    gabriel = GabrielConversational()
    
    print("🗣️ GABRIEL CONVERSATIONAL ENGLISH")
    print("=" * 60)
    print("\nGABRIEL is now trained in conversational English!")
    print("\nTry these examples:")
    
    examples = [
        "Hello!",
        "How are you doing?",
        "What can you help me with?",
        "That's really interesting!",
        "Thank you so much!",
        "Goodbye!"
    ]
    
    for example in examples:
        response = gabriel.process_input(example)
        print(f"\nYou: {example}")
        print(f"GABRIEL: {response}")
    
    print("\n" + "=" * 60)
    print("✅ GABRIEL conversational English training complete!")

if __name__ == "__main__":
    main()


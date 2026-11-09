#!/usr/bin/env python3
"""
🗣️ NATURAL LANGUAGE PATTERNS
Complete natural conversational English patterns
GORUNFREE Protocol
"""

import re
from typing import List, Dict, Tuple

class NaturalLanguagePatterns:
    """Natural language understanding and generation"""
    
    def __init__(self):
        self.contractions = {
            "i'm": "I am",
            "you're": "you are",
            "he's": "he is",
            "she's": "she is",
            "it's": "it is",
            "we're": "we are",
            "they're": "they are",
            "i've": "I have",
            "you've": "you have",
            "we've": "we have",
            "they've": "they have",
            "i'll": "I will",
            "you'll": "you will",
            "he'll": "he will",
            "she'll": "she will",
            "we'll": "we will",
            "they'll": "they will",
            "i'd": "I would",
            "you'd": "you would",
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "doesn't": "does not",
            "didn't": "did not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not",
            "wouldn't": "would not",
            "couldn't": "could not",
            "shouldn't": "should not"
        }
        
        self.slang = {
            "gonna": "going to",
            "wanna": "want to",
            "gotta": "got to",
            "lemme": "let me",
            "gimme": "give me",
            "kinda": "kind of",
            "sorta": "sort of",
            "dunno": "don't know",
            "y'all": "you all",
            "ain't": "is not"
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize conversational text"""
        text = text.lower().strip()
        
        # Expand contractions
        for contraction, expansion in self.contractions.items():
            text = text.replace(contraction, expansion)
        
        # Expand slang
        for slang, standard in self.slang.items():
            text = text.replace(slang, standard)
        
        return text
    
    def extract_entities(self, text: str) -> Dict:
        """Extract named entities from text"""
        entities = {
            'names': [],
            'places': [],
            'dates': [],
            'numbers': [],
            'topics': []
        }
        
        # Extract names (capitalized words)
        name_pattern = r'\b[A-Z][a-z]+\b'
        names = re.findall(name_pattern, text)
        entities['names'] = names
        
        # Extract numbers
        number_pattern = r'\d+'
        numbers = re.findall(number_pattern, text)
        entities['numbers'] = numbers
        
        return entities
    
    def detect_tone(self, text: str) -> str:
        """Detect conversational tone"""
        text_lower = text.lower()
        
        # Positive indicators
        positive_words = ['great', 'awesome', 'wonderful', 'excellent', 'fantastic', 
                         'amazing', 'love', 'happy', 'excited', 'good', 'nice']
        if any(word in text_lower for word in positive_words):
            return 'positive'
        
        # Negative indicators
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 
                         'frustrated', 'worried', 'disappointed']
        if any(word in text_lower for word in negative_words):
            return 'negative'
        
        # Question indicators
        if '?' in text or any(q in text_lower for q in ['what', 'how', 'why', 'when', 'where', 'who']):
            return 'questioning'
        
        return 'neutral'
    
    def generate_variations(self, phrase: str) -> List[str]:
        """Generate natural variations of a phrase"""
        variations = []
        
        # Add filler words
        fillers = ['well', 'you know', 'I mean', 'like', 'actually', 'basically']
        for filler in fillers:
            variations.append(f"{filler}, {phrase}")
        
        # Add emphasis
        emphasis = ['really', 'very', 'quite', 'pretty', 'rather']
        for emp in emphasis:
            if 'good' in phrase.lower():
                variations.append(phrase.replace('good', f'{emp} good'))
        
        return variations

def main():
    nlp = NaturalLanguagePatterns()
    
    print("🗣️ NATURAL LANGUAGE PATTERNS")
    print("=" * 60)
    
    test_texts = [
        "I'm gonna go to the store, y'all.",
        "I don't know what you're talking about.",
        "That's really great! I'm so excited!",
        "What's the weather like today?"
    ]
    
    for text in test_texts:
        print(f"\nOriginal: {text}")
        normalized = nlp.normalize_text(text)
        print(f"Normalized: {normalized}")
        tone = nlp.detect_tone(text)
        print(f"Tone: {tone}")
        entities = nlp.extract_entities(text)
        print(f"Entities: {entities}")

if __name__ == "__main__":
    main()


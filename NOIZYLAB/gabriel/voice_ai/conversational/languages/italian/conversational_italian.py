#!/usr/bin/env python3
"""
🗣️ GABRIEL CONVERSATIONAL ITALIAN
Complete Italian conversational patterns
GORUNFREE Protocol
"""

class ConversationalItalian:
    """Italian conversational patterns"""
    
    def __init__(self):
        self.patterns = {
            'greetings': {
                'formal': [
                    "Buongiorno", "Buonasera", "Buonanotte",
                    "Salve", "Piacere di conoscerla",
                    "Come sta?", "Come va?"
                ],
                'casual': [
                    "Ciao", "Salve", "Come stai?",
                    "Come va?", "Tutto bene?", "Come butta?"
                ]
            },
            'farewells': {
                'formal': [
                    "Arrivederci", "A presto", "Buona giornata",
                    "Ci vediamo", "Buon proseguimento"
                ],
                'casual': [
                    "Ciao", "A presto", "Ci sentiamo",
                    "A dopo", "Ci vediamo"
                ]
            },
            'questions': [
                "Cosa?", "Chi?", "Dove?", "Quando?", "Perché?",
                "Come?", "Puoi?", "Potresti?", "Vuoi?"
            ],
            'affirmations': [
                "Sì", "Certo", "Certamente", "Perfetto",
                "Esatto", "Giusto", "Va bene", "D'accordo"
            ],
            'negations': [
                "No", "Assolutamente no", "Per niente",
                "Mai", "Niente affatto"
            ],
            'politeness': [
                "Per favore", "Grazie", "Molte grazie",
                "Prego", "Scusa", "Mi dispiace", "Perdonami"
            ],
            'emotions': {
                'positive': [
                    "Che bello!", "Fantastico!", "Eccellente!",
                    "Meraviglioso!", "Perfetto!"
                ],
                'negative': [
                    "Che peccato", "Mi dispiace",
                    "Che triste", "Che frustrante"
                ]
            }
        }
        
        self.responses = {
            'greeting': [
                "Ciao! Come posso aiutarti?",
                "Salve! Di cosa hai bisogno?",
                "Buongiorno! Come posso esserti utile?",
                "Ciao, piacere. Come posso aiutarti?"
            ],
            'farewell': [
                "Arrivederci! Buona giornata!",
                "Ciao, a presto!",
                "Ci sentiamo presto. Buona fortuna!",
                "Arrivederci, è stato un piacere parlare con te."
            ],
            'question': [
                "Buona domanda. Fammi pensare...",
                "Sono felice di aiutarti con questo.",
                "Domanda interessante. Ti spiego...",
                "Certo, posso aiutarti con questo."
            ],
            'acknowledgment': [
                "Capisco.",
                "Certo.",
                "Ha senso.",
                "Comprendo."
            ]
        }
    
    def detect_intent(self, text: str) -> str:
        """Detect Italian conversational intent"""
        text_lower = text.lower()
        
        for pattern_type, patterns in self.patterns.items():
            if isinstance(patterns, dict):
                for sub_type, sub_patterns in patterns.items():
                    for pattern in sub_patterns:
                        if pattern.lower() in text_lower:
                            return pattern_type
            else:
                for pattern in patterns:
                    if pattern.lower() in text_lower:
                        return pattern_type
        
        if any(q in text_lower for q in ['?', 'cosa', 'come', 'perché', 'quando', 'dove', 'chi']):
            return 'question'
        
        return 'general'
    
    def generate_response(self, text: str) -> str:
        """Generate Italian response"""
        import random
        intent = self.detect_intent(text)
        
        if intent == 'greetings':
            return random.choice(self.responses['greeting'])
        elif intent == 'farewells':
            return random.choice(self.responses['farewell'])
        elif intent == 'questions':
            return random.choice(self.responses['question'])
        else:
            return random.choice(self.responses['acknowledgment'])


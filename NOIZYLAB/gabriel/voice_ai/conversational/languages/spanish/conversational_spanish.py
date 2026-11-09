#!/usr/bin/env python3
"""
🗣️ GABRIEL CONVERSATIONAL SPANISH
Complete Spanish conversational patterns
GORUNFREE Protocol
"""

class ConversationalSpanish:
    """Spanish conversational patterns"""
    
    def __init__(self):
        self.patterns = {
            'greetings': {
                'formal': [
                    "Buenos días", "Buenas tardes", "Buenas noches",
                    "Hola, ¿cómo está usted?", "Mucho gusto",
                    "Encantado de conocerle", "¿Cómo le va?"
                ],
                'casual': [
                    "Hola", "¿Qué tal?", "¿Qué pasa?", "¿Cómo estás?",
                    "¿Qué onda?", "¿Cómo andas?", "Ey, ¿qué hay?"
                ]
            },
            'farewells': {
                'formal': [
                    "Adiós", "Hasta luego", "Hasta pronto",
                    "Que tenga un buen día", "Nos vemos"
                ],
                'casual': [
                    "Chao", "Nos vemos", "Hasta luego",
                    "Cuídate", "Nos hablamos"
                ]
            },
            'questions': [
                "¿Qué?", "¿Quién?", "¿Dónde?", "¿Cuándo?", "¿Por qué?",
                "¿Cómo?", "¿Puedes?", "¿Podrías?", "¿Quieres?"
            ],
            'affirmations': [
                "Sí", "Claro", "Por supuesto", "Desde luego",
                "Por cierto", "Exacto", "Correcto", "Vale"
            ],
            'negations': [
                "No", "Para nada", "De ninguna manera",
                "Absolutamente no", "Nunca"
            ],
            'politeness': [
                "Por favor", "Gracias", "Muchas gracias",
                "De nada", "Perdón", "Disculpe", "Lo siento"
            ],
            'emotions': {
                'positive': [
                    "¡Qué bien!", "¡Genial!", "¡Excelente!",
                    "¡Fantástico!", "¡Maravilloso!"
                ],
                'negative': [
                    "Qué mal", "Qué pena", "Lo siento",
                    "Qué triste", "Qué frustrante"
                ]
            }
        }
        
        self.responses = {
            'greeting': [
                "¡Hola! ¿En qué puedo ayudarte?",
                "Hola, ¿qué tal? ¿Cómo puedo ayudarte?",
                "¡Buenos días! ¿En qué te puedo ayudar?",
                "Hola, encantado. ¿Qué necesitas?"
            ],
            'farewell': [
                "¡Adiós! Que tengas un buen día.",
                "Hasta luego, cuídate.",
                "Nos vemos pronto. ¡Que vaya bien!",
                "Adiós, fue un placer hablar contigo."
            ],
            'question': [
                "Buena pregunta. Déjame pensar...",
                "Me alegra ayudarte con eso.",
                "Interesante pregunta. Te explico...",
                "Claro, puedo ayudarte con eso."
            ],
            'acknowledgment': [
                "Entiendo.",
                "Claro.",
                "Tiene sentido.",
                "Comprendo."
            ]
        }
    
    def detect_intent(self, text: str) -> str:
        """Detect Spanish conversational intent"""
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
        
        if any(q in text_lower for q in ['?', 'qué', 'cómo', 'por qué', 'cuándo', 'dónde', 'quién']):
            return 'question'
        
        return 'general'
    
    def generate_response(self, text: str) -> str:
        """Generate Spanish response"""
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


#!/usr/bin/env python3
"""
🗣️ GABRIEL CONVERSATIONAL PORTUGUESE
Complete Portuguese conversational patterns
GORUNFREE Protocol
"""

class ConversationalPortuguese:
    """Portuguese conversational patterns"""
    
    def __init__(self):
        self.patterns = {
            'greetings': {
                'formal': [
                    "Bom dia", "Boa tarde", "Boa noite",
                    "Olá, como está?", "Prazer em conhecê-lo",
                    "Como vai?", "Tudo bem?"
                ],
                'casual': [
                    "Oi", "Olá", "E aí?",
                    "Tudo bem?", "Como vai?", "Tudo certo?",
                    "Fala aí", "E aí, beleza?"
                ]
            },
            'farewells': {
                'formal': [
                    "Adeus", "Até logo", "Tenha um bom dia",
                    "Até breve", "Nos vemos"
                ],
                'casual': [
                    "Tchau", "Falou", "Até mais",
                    "Valeu", "Até logo"
                ]
            },
            'questions': [
                "O quê?", "Quem?", "Onde?", "Quando?", "Por quê?",
                "Como?", "Pode?", "Poderia?", "Quer?"
            ],
            'affirmations': [
                "Sim", "Claro", "Com certeza", "Perfeito",
                "Exato", "Certo", "Tudo bem", "OK"
            ],
            'negations': [
                "Não", "De jeito nenhum", "Nunca",
                "Absolutamente não", "Nem pensar"
            ],
            'politeness': [
                "Por favor", "Obrigado", "Muito obrigado",
                "De nada", "Desculpe", "Com licença", "Desculpa"
            ],
            'emotions': {
                'positive': [
                    "Que legal!", "Ótimo!", "Excelente!",
                    "Fantástico!", "Maravilhoso!"
                ],
                'negative': [
                    "Que pena", "Sinto muito",
                    "Que triste", "Que frustrante"
                ]
            }
        }
        
        self.responses = {
            'greeting': [
                "Olá! Como posso ajudá-lo?",
                "Oi! O que você precisa?",
                "Bom dia! Como posso ajudá-lo?",
                "Oi, prazer. Como posso ajudar?"
            ],
            'farewell': [
                "Adeus! Tenha um bom dia!",
                "Tchau, até logo!",
                "Até mais. Boa sorte!",
                "Adeus, foi um prazer conversar com você."
            ],
            'question': [
                "Boa pergunta. Deixe-me pensar...",
                "Fico feliz em ajudar com isso.",
                "Pergunta interessante. Deixe-me explicar...",
                "Claro, posso ajudar com isso."
            ],
            'acknowledgment': [
                "Entendo.",
                "Certo.",
                "Faz sentido.",
                "Compreendo."
            ]
        }
    
    def detect_intent(self, text: str) -> str:
        """Detect Portuguese conversational intent"""
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
        
        if any(q in text_lower for q in ['?', 'o quê', 'como', 'por quê', 'quando', 'onde', 'quem']):
            return 'question'
        
        return 'general'
    
    def generate_response(self, text: str) -> str:
        """Generate Portuguese response"""
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


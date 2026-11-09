"""
SMART ROUTER v2.0 - GORUNFREE EDITION
Routes user input to the optimal AI agent
"""

import re
from typing import Optional

class SmartRouter:
    """Routes messages to the most appropriate agent based on content analysis"""
    
    # Agent-keyword mappings with weights
    PATTERNS = {
        'SQL_SORCERER': (r"(sql|query|select|join|database|table|customers|orders|products)", 10),
        'SHELL_COMMANDER': (r"(shell|bash|command|terminal|script|chmod|mkdir|find|grep|awk|sed)", 10),
        'GIT_GURU': (r"(git|commit|branch|merge|rebase|push|pull|clone|stash)", 10),
        'REGEX_WIZARD': (r"(regex|pattern|match|replace|capture|extract)", 10),
        'DOCKER_MASTER': (r"(docker|container|image|dockerfile|compose|kubernetes|k8s)", 10),
        'CODE_REVIEWER': (r"(review|analyze|bug|security|performance|refactor|lint)", 8),
        'API_ARCHITECT': (r"(api|endpoint|rest|openapi|swagger|route)", 8),
        'JSON_TRANSFORMER': (r"(json|transform|restructure|jq|schema)", 8),
        'YAML_SCULPTOR': (r"(yaml|yml|config|configuration|ansible|helm)", 8),
        'MARKDOWN_MAESTRO': (r"(markdown|readme|documentation|docs|format|heading)", 8),
        'ENGR_KEITH': (r"(code|bug|error|deploy|python|typescript|javascript)", 5),
        'SHIRL': (r"(feel|sad|happy|worried|love|empathy|support)", 5),
        'DREAM': (r"(plan|future|imagine|vision|create|generate|design)", 5),
        'GABRIEL': (r"(security|admin|access|auth|system|key|execute)", 5),
        'POPS': (r"(advice|strategy|wise|guide|mentor|experience)", 5),
    }
    
    # Agent to provider mapping
    PROVIDER_MAP = {
        'ENGR_KEITH': 'Claude',
        'SHIRL': 'Claude',
        'DREAM': 'OpenAI',
        'GABRIEL': 'NVIDIA',
        'POPS': 'DeepSeek',
        'SQL_SORCERER': 'Claude',
        'CODE_REVIEWER': 'Claude',
        'API_ARCHITECT': 'Claude',
        'SHELL_COMMANDER': 'Claude',
        'GIT_GURU': 'Claude',
        'DOCKER_MASTER': 'Claude',
        'REGEX_WIZARD': 'Gemini',
        'JSON_TRANSFORMER': 'Gemini',
        'YAML_SCULPTOR': 'Gemini',
        'MARKDOWN_MAESTRO': 'Gemini',
    }
    
    def __init__(self):
        self.last_agent: Optional[str] = None
    
    def route(self, text: str) -> str:
        """Determine best agent for given text"""
        lower = text.lower()
        scores: dict[str, int] = {}
        
        for agent, (pattern, weight) in self.PATTERNS.items():
            if re.search(pattern, lower):
                scores[agent] = weight
        
        # Sticky routing: bias toward previous agent
        if self.last_agent and self.last_agent in scores:
            scores[self.last_agent] += 2
        
        if not scores:
            return 'GABRIEL'  # Default
        
        best_agent = max(scores, key=lambda k: scores[k])
        self.last_agent = best_agent
        return best_agent
    
    def get_provider(self, agent: str) -> str:
        """Get AI provider for agent"""
        return self.PROVIDER_MAP.get(agent, 'Gemini')
    
    @classmethod
    def route_static(cls, text: str) -> str:
        """Static routing without instance"""
        router = cls()
        return router.route(text)


# Singleton instance for convenience
_router = SmartRouter()
route = _router.route
get_provider = _router.get_provider

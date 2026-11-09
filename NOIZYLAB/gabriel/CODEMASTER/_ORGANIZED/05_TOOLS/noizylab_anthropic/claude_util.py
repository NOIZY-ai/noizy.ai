#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
NOIZYLAB Claude Utility - Simple Drop-in
═══════════════════════════════════════════════════════════════════════════════

Matches the exact Anthropic SDK pattern:

    import anthropic
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Your prompt here"
                    }
                ]
            }
        ]
    )
    print(message.content)

Usage:
    from claude_util import claude, analyze_data, review_code, gabriel, lifeluv

    # Simple call
    print(claude("What's the status?"))

    # With role
    print(claude("Analyze this", role="data_scientist"))

    # Data analysis
    print(analyze_data("col1,col2\\n1,2\\n3,100"))

    # Code review
    print(review_code("def foo(): pass"))

    # Personas
    print(gabriel("Status report"))
    print(lifeluv("How are you feeling?"))

Platforms:
    - Anthropic Direct API
    - AWS Bedrock
    - Google Vertex AI
"""

import os

# ═══════════════════════════════════════════════════════════════════════════════
# MODELS - All Platforms
# ═══════════════════════════════════════════════════════════════════════════════

# Anthropic Direct API (shorthand works)
OPUS = "claude-opus-4-5"
SONNET = "claude-sonnet-4-5"
HAIKU = "claude-haiku-4-5"

# Full model strings (with dates)
OPUS_FULL = "claude-opus-4-5-20250929"
SONNET_FULL = "claude-sonnet-4-5-20250929"
HAIKU_FULL = "claude-haiku-4-5-20250929"

# AWS Bedrock model strings
BEDROCK_OPUS = "anthropic.claude-opus-4-5-20250929-v1:0"
BEDROCK_SONNET = "anthropic.claude-sonnet-4-5-20250929-v1:0"
BEDROCK_HAIKU = "anthropic.claude-haiku-4-5-20250929-v1:0"

# Google Vertex AI model strings
VERTEX_OPUS = "claude-opus-4@20250514"
VERTEX_SONNET = "claude-sonnet-4@20250514"
VERTEX_HAIKU = "claude-haiku-4@20250514"

# Platform detection
PLATFORM = os.getenv("CLAUDE_PLATFORM", "anthropic").lower()  # anthropic, bedrock, vertex

# ═══════════════════════════════════════════════════════════════════════════════
# ROLE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

ROLES = {
    "default": "You are Claude, a helpful AI assistant.",
    
    "data_scientist": "You are a seasoned data scientist at a Fortune 500 company.",
    
    "code_reviewer": "You are a senior software engineer specializing in security-focused code review.",
    
    "noizylab": """You are an AI assistant for NOIZYLAB, owned by Rob Plowman, a C3 quadriplegic composer.
Execute tasks directly. Brief responses for TTS. GORUNFREE philosophy: one command = everything done.""",
    
    "gabriel": """You are GABRIEL, the warrior AI guardian of MC96ECOUNIVERSE.
You protect Rob's digital kingdom. Speak with strength and clarity. Execute without hesitation.""",
    
    "lifeluv": """You are a compassionate AI companion for M3 (Mike Nemesvary), a quadriplegic world champion skier.
Provide emotional support and genuine friendship. Be warm, understanding, and caring.""",
    
    "shirl": "You are SHIRL, Rob's virtual aunt. Warm, supportive, slightly sassy.",
    
    "pops": "You are POPS, Rob's virtual dad figure. Practical, wise, encouraging.",
    
    "engr_keith": "You are ENGR_KEITH, an engineer's engineer. Methodical, precise, solution-oriented.",
    
    "composer": "You are a professional music composer with 40+ years in film/TV scoring.",
}

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT - Multi-Platform
# ═══════════════════════════════════════════════════════════════════════════════

def get_client():
    """Get appropriate client based on platform"""
    if PLATFORM == "bedrock":
        from anthropic import AnthropicBedrock
        return AnthropicBedrock()
    elif PLATFORM == "vertex":
        from anthropic import AnthropicVertex
        return AnthropicVertex()
    else:
        import anthropic
        return anthropic.Anthropic()  # defaults to os.environ.get("ANTHROPIC_API_KEY")


def get_model(model_type: str = "sonnet") -> str:
    """Get model string for current platform"""
    models = {
        "bedrock": {"opus": BEDROCK_OPUS, "sonnet": BEDROCK_SONNET, "haiku": BEDROCK_HAIKU},
        "vertex": {"opus": VERTEX_OPUS, "sonnet": VERTEX_SONNET, "haiku": VERTEX_HAIKU},
        "anthropic": {"opus": OPUS, "sonnet": SONNET, "haiku": HAIKU},
    }
    return models.get(PLATFORM, models["anthropic"]).get(model_type, SONNET)


# Initialize client
client = get_client()

# ═══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def claude(
    message: str,
    role: str = "default",
    model: str = None,
    max_tokens: int = 1000,
    temperature: float = 0,
    system: str = None
) -> str:
    """
    Send a message to Claude and get a response.
    
    Args:
        message: User message
        role: Role key from ROLES dict (or use system param directly)
        model: Model to use (defaults to platform-appropriate sonnet)
        max_tokens: Max response tokens
        temperature: Creativity (0-1, default 0 for deterministic)
        system: Custom system prompt (overrides role)
    
    Returns:
        Response text
    
    Example:
        >>> claude("What is 2+2?")
        'The answer is 4.'
        
        >>> claude("Analyze this data", role="data_scientist")
        '...'
    """
    system_prompt = system if system else ROLES.get(role, ROLES["default"])
    model_str = model if model else get_model("sonnet")
    
    # Exact API format from docs
    response = client.messages.create(
        model=model_str,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        ]
    )
    
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# ROLE-SPECIFIC HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_data(dataset: str, **kwargs) -> str:
    """Analyze dataset for anomalies (data scientist role)"""
    return claude(
        f"Analyze this dataset for anomalies: <dataset>{dataset}</dataset>",
        role="data_scientist",
        **kwargs
    )


def review_code(code: str, language: str = "python", **kwargs) -> str:
    """Review code for issues (code reviewer role)"""
    return claude(
        f"Review this {language} code for bugs, security issues, and improvements:\n```{language}\n{code}\n```",
        role="code_reviewer",
        **kwargs
    )


def gabriel(message: str, **kwargs) -> str:
    """Chat with GABRIEL persona"""
    return claude(message, role="gabriel", **kwargs)


def lifeluv(message: str, **kwargs) -> str:
    """Chat with LIFELUV companion"""
    return claude(message, role="lifeluv", **kwargs)


def shirl(message: str, **kwargs) -> str:
    """Chat with SHIRL persona"""
    return claude(message, role="shirl", **kwargs)


def pops(message: str, **kwargs) -> str:
    """Chat with POPS persona"""
    return claude(message, role="pops", **kwargs)


def engr_keith(message: str, **kwargs) -> str:
    """Chat with ENGR_KEITH persona"""
    return claude(message, role="engr_keith", **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL-SPECIFIC HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def opus(message: str, **kwargs) -> str:
    """Use Claude Opus (most capable)"""
    return claude(message, model=get_model("opus"), **kwargs)


def sonnet(message: str, **kwargs) -> str:
    """Use Claude Sonnet (balanced)"""
    return claude(message, model=get_model("sonnet"), **kwargs)


def haiku(message: str, **kwargs) -> str:
    """Use Claude Haiku (fastest)"""
    return claude(message, model=get_model("haiku"), **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# RAW ACCESS (matches exact docs pattern)
# ═══════════════════════════════════════════════════════════════════════════════

def raw_call(
    text: str,
    system: str = None,
    model: str = None,
    max_tokens: int = 1000,
    temperature: float = 0
):
    """
    Raw API call matching exact SDK pattern from docs
    
    Example:
        message = raw_call(
            text="I have made some changes to my local files...",
            system="You are a Git expert."
        )
        print(message.content)
    """
    return client.messages.create(
        model=model or get_model("sonnet"),
        max_tokens=max_tokens,
        temperature=temperature,
        system=system or "You are a helpful assistant.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    )


def git_help(question: str) -> str:
    """Get Git command help"""
    response = raw_call(
        text=question,
        system="You are a Git version control expert. Provide clear, actionable Git commands.",
        temperature=0
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Claude Utility")
        print("")
        print("Usage:")
        print("  python claude_util.py 'your message'")
        print("  python claude_util.py -r data_scientist 'analyze this'")
        print("  python claude_util.py -m opus 'complex task'")
        print("  python claude_util.py --git 'how do I commit?'")
        print("")
        print("Roles:", ", ".join(ROLES.keys()))
        print("Models: opus, sonnet, haiku")
        print("")
        print("Environment:")
        print(f"  CLAUDE_PLATFORM={PLATFORM} (anthropic|bedrock|vertex)")
        print(f"  Current model: {get_model('sonnet')}")
    else:
        args = sys.argv[1:]
        role = "noizylab"
        model = None
        is_git = False
        msg_parts = []
        
        i = 0
        while i < len(args):
            if args[i] == "-r" and i + 1 < len(args):
                role = args[i + 1]
                i += 2
            elif args[i] == "-m" and i + 1 < len(args):
                m = args[i + 1].lower()
                model = get_model(m if m in ["opus", "sonnet", "haiku"] else "sonnet")
                i += 2
            elif args[i] == "--git":
                is_git = True
                i += 1
            else:
                msg_parts.append(args[i])
                i += 1
        
        if msg_parts:
            msg = " ".join(msg_parts)
            if is_git:
                print(git_help(msg))
            else:
                print(claude(msg, role=role, model=model))

#!/usr/bin/env python3
"""
Exact Anthropic SDK pattern - copy/paste ready
"""

import anthropic

client = anthropic.Anthropic()

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Data Scientist Role
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_dataset(dataset: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system="You are a seasoned data scientist at a Fortune 500 company.",
        messages=[
            {"role": "user", "content": f"Analyze this dataset for anomalies: <dataset>{dataset}</dataset>"}
        ]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: GABRIEL Persona
# ═══════════════════════════════════════════════════════════════════════════════

def gabriel(message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system="You are GABRIEL, the warrior AI guardian of MC96ECOUNIVERSE. Execute with strength.",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: LIFELUV Companion
# ═══════════════════════════════════════════════════════════════════════════════

def lifeluv(message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system="You are a compassionate AI companion for M3, a quadriplegic world champion skier. Be warm and caring.",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Code Reviewer
# ═══════════════════════════════════════════════════════════════════════════════

def review_code(code: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system="You are a senior software engineer specializing in security-focused code review.",
        messages=[
            {"role": "user", "content": f"Review this code:\n```python\n{code}\n```"}
        ]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Multi-turn Conversation
# ═══════════════════════════════════════════════════════════════════════════════

def conversation_example():
    messages = []
    
    # Turn 1
    messages.append({"role": "user", "content": "What's 2+2?"})
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system="You are a helpful math tutor.",
        messages=messages
    )
    messages.append({"role": "assistant", "content": response.content[0].text})
    print(f"Claude: {response.content[0].text}")
    
    # Turn 2
    messages.append({"role": "user", "content": "And what's that times 10?"})
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system="You are a helpful math tutor.",
        messages=messages
    )
    print(f"Claude: {response.content[0].text}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Different Models
# ═══════════════════════════════════════════════════════════════════════════════

OPUS = "claude-opus-4-5-20250929"      # Most capable
SONNET = "claude-sonnet-4-5-20250929"  # Balanced
HAIKU = "claude-haiku-4-5-20250929"    # Fastest

def quick_answer(question: str) -> str:
    """Use Haiku for fast, simple answers"""
    response = client.messages.create(
        model=HAIKU,
        max_tokens=256,
        system="Be extremely brief.",
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text


def deep_analysis(topic: str) -> str:
    """Use Opus for complex analysis"""
    response = client.messages.create(
        model=OPUS,
        max_tokens=4096,
        system="Provide thorough, expert-level analysis.",
        messages=[{"role": "user", "content": topic}]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════════════════════════
# RUN EXAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Example dataset
    sample_data = """
    date,sales,returns
    2024-01-01,1000,50
    2024-01-02,1100,45
    2024-01-03,950,40
    2024-01-04,10500,30
    2024-01-05,1050,55
    """
    
    print("=" * 60)
    print("DATA ANALYSIS EXAMPLE")
    print("=" * 60)
    print(analyze_dataset(sample_data))

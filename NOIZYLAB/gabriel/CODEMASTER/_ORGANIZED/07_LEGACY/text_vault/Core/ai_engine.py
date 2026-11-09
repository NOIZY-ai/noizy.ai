#!/usr/bin/env python3
"""
🧠 CODEBEAST AI CORE ENGINE 🧠
The Brain of Your Super Smart Development Beast

This module provides the core AI functionality powered by OpenAI
for intelligent code analysis, generation, and assistance.
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
import json
from datetime import datetime

import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

@dataclass
class AIResponse:
    """Structure for AI responses"""
    content: str
    usage: Dict[str, Any]
    model: str
    timestamp: datetime
    success: bool
    error: Optional[str] = None

class CodeBeastAI:
    """
    🧠 The AI Brain of CodeBeast
    Provides intelligent code assistance using OpenAI
    """
    
    def __init__(self):
        self.console = Console()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        if not self.api_key:
            self.console.print("[red]❌ OpenAI API key not found! Please set OPENAI_API_KEY in .env file[/red]")
            return
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        self.console.print("[green]🧠 CodeBeast AI Engine Initialized![/green]")
        
    def _create_system_prompt(self, role: str = "assistant") -> str:
        """Create system prompt for different AI roles"""
        base_prompt = """You are CodeBeast AI, a super intelligent coding assistant that is:
        - STRONG: Can handle complex coding challenges and large codebases
        - SMART: Provides intelligent insights, best practices, and optimization suggestions  
        - HELPFUL: Always ready to assist with clear, actionable solutions

        You specialize in:
        - Code analysis and review
        - Bug detection and fixing
        - Performance optimization
        - Documentation generation
        - Architecture recommendations
        - Testing strategies
        - Security analysis
        """
        
        role_prompts = {
            "code_reviewer": base_prompt + "\nFocus on: Code quality, security issues, performance bottlenecks, and best practices.",
            "debugger": base_prompt + "\nFocus on: Finding bugs, analyzing error patterns, and providing fix suggestions.",
            "optimizer": base_prompt + "\nFocus on: Performance improvements, memory optimization, and efficiency gains.",
            "documenter": base_prompt + "\nFocus on: Creating clear documentation, docstrings, and code comments.",
            "architect": base_prompt + "\nFocus on: System design, patterns, scalability, and maintainability.",
            "security_analyst": base_prompt + "\nFocus on: Security vulnerabilities, threat analysis, and secure coding practices."
        }
        
        return role_prompts.get(role, base_prompt)
    
    async def analyze_code(self, code: str, language: str = "python", 
                          analysis_type: str = "general") -> AIResponse:
        """
        🔍 Analyze code with AI
        """
        try:
            system_prompt = self._create_system_prompt("code_reviewer")
            
            user_prompt = f"""
            Please analyze this {language} code:

            ```{language}
            {code}
            ```

            Analysis type: {analysis_type}
            
            Provide:
            1. 🎯 Code Quality Assessment
            2. 🔒 Security Analysis  
            3. 🚀 Performance Insights
            4. 📚 Best Practices Recommendations
            5. 🐛 Potential Issues
            6. ✨ Improvement Suggestions
            """
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("🧠 Analyzing code with AI...", total=None)
                
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            
            return AIResponse(
                content=response.choices[0].message.content or "",
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                timestamp=datetime.now(),
                success=True
            )
            
        except Exception as e:
            return AIResponse(
                content="",
                usage={},
                model=self.model,
                timestamp=datetime.now(),
                success=False,
                error=str(e)
            )
    
    async def generate_code(self, description: str, language: str = "python",
                           framework: Optional[str] = None) -> AIResponse:
        """
        🛠️ Generate code from description
        """
        try:
            system_prompt = self._create_system_prompt("architect")
            
            framework_context = f" using {framework}" if framework else ""
            
            user_prompt = f"""
            Generate {language} code{framework_context} for:
            
            {description}
            
            Requirements:
            1. Write clean, maintainable code
            2. Include proper error handling
            3. Add comprehensive docstrings
            4. Follow best practices
            5. Include usage examples
            6. Add type hints where applicable
            """
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("🛠️ Generating code with AI...", total=None)
                
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            
            return AIResponse(
                content=response.choices[0].message.content or "",
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                timestamp=datetime.now(),
                success=True
            )
            
        except Exception as e:
            return AIResponse(
                content="",
                usage={},
                model=self.model,
                timestamp=datetime.now(),
                success=False,
                error=str(e)
            )
    
    async def debug_code(self, code: str, error_message: Optional[str] = None,
                        language: str = "python") -> AIResponse:
        """
        🐛 Debug code and find solutions
        """
        try:
            system_prompt = self._create_system_prompt("debugger")
            
            error_context = f"\nError message: {error_message}" if error_message else ""
            
            user_prompt = f"""
            Debug this {language} code:

            ```{language}
            {code}
            ```
            {error_context}
            
            Please provide:
            1. 🔍 Issue Identification
            2. 🎯 Root Cause Analysis
            3. 🛠️ Step-by-step Fix
            4. ✅ Corrected Code
            5. 🛡️ Prevention Tips
            """
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("🐛 Debugging with AI...", total=None)
                
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=0.3  # Lower temperature for debugging
                )
            
            return AIResponse(
                content=response.choices[0].message.content or "",
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                timestamp=datetime.now(),
                success=True
            )
            
        except Exception as e:
            return AIResponse(
                content="",
                usage={},
                model=self.model,
                timestamp=datetime.now(),
                success=False,
                error=str(e)
            )
    
    async def optimize_code(self, code: str, language: str = "python",
                           optimization_type: str = "performance") -> AIResponse:
        """
        🚀 Optimize code for performance, memory, or readability
        """
        try:
            system_prompt = self._create_system_prompt("optimizer")
            
            user_prompt = f"""
            Optimize this {language} code for {optimization_type}:

            ```{language}
            {code}
            ```
            
            Provide:
            1. 📊 Current Performance Analysis
            2. 🎯 Optimization Opportunities
            3. ⚡ Optimized Code
            4. 📈 Expected Improvements
            5. 📝 Explanation of Changes
            """
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("🚀 Optimizing with AI...", total=None)
                
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=0.5
                )
            
            return AIResponse(
                content=response.choices[0].message.content or "",
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                timestamp=datetime.now(),
                success=True
            )
            
        except Exception as e:
            return AIResponse(
                content="",
                usage={},
                model=self.model,
                timestamp=datetime.now(),
                success=False,
                error=str(e)
            )
    
    async def generate_documentation(self, code: str, language: str = "python",
                                   doc_type: str = "api") -> AIResponse:
        """
        📚 Generate comprehensive documentation
        """
        try:
            system_prompt = self._create_system_prompt("documenter")
            
            user_prompt = f"""
            Generate {doc_type} documentation for this {language} code:

            ```{language}
            {code}
            ```
            
            Include:
            1. 📖 Clear Description
            2. 📋 Parameters & Return Values
            3. 💡 Usage Examples
            4. ⚠️ Important Notes
            5. 🔗 Related Functions/Classes
            """
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("📚 Generating docs with AI...", total=None)
                
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=0.4
                )
            
            return AIResponse(
                content=response.choices[0].message.content or "",
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                timestamp=datetime.now(),
                success=True
            )
            
        except Exception as e:
            return AIResponse(
                content="",
                usage={},
                model=self.model,
                timestamp=datetime.now(),
                success=False,
                error=str(e)
            )
    
    def display_response(self, response: AIResponse, title: str = "AI Response"):
        """
        🎨 Display AI response with rich formatting
        """
        if not response.success:
            self.console.print(f"[red]❌ Error: {response.error}[/red]")
            return
        
        # Display the response in a beautiful panel
        panel = Panel(
            Markdown(response.content),
            title=f"🧠 {title}",
            expand=False,
            border_style="blue"
        )
        
        self.console.print(panel)
        
        # Display usage info
        if response.usage:
            usage_text = f"🔧 Model: {response.model} | Tokens: {response.usage.get('total_tokens', 'N/A')} | Time: {response.timestamp.strftime('%H:%M:%S')}"
            self.console.print(f"[dim]{usage_text}[/dim]")

# Global AI instance
_ai_instance = None

def get_ai_engine() -> CodeBeastAI:
    """Get the global AI engine instance"""
    global _ai_instance
    if _ai_instance is None:
        _ai_instance = CodeBeastAI()
    return _ai_instance
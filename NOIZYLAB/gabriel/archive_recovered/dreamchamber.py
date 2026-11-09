#!/usr/bin/env python3
"""
🌙 DREAMCHAMBER - AI Council of Wisdom
═══════════════════════════════════════════════════════════════════
Query multiple AI models simultaneously, collect diverse perspectives,
synthesize wisdom, extract insights, find consensus.

Features:
- Parallel multi-model queries
- Thinking mode support (Qwen3)
- Response synthesis
- Key insight extraction
- Consensus finding
- Session history
- MCP-ready architecture
═══════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import subprocess
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Paths
CHAMBER_PATH = Path.home() / ".noizylab" / "dreamchamber"
SESSIONS_PATH = CHAMBER_PATH / "sessions"
CONFIG_PATH = CHAMBER_PATH / "config.json"


class CouncilMember:
    """A member of the AI Council"""
    def __init__(self, name: str, model: str, specialty: str, weight: float = 1.0):
        self.name = name
        self.model = model
        self.specialty = specialty
        self.weight = weight
        self.enabled = True


class DreamChamber:
    """
    🌙 DREAMCHAMBER - The AI Council
    
    Pose questions to multiple AI models simultaneously,
    collect diverse perspectives, synthesize unified wisdom.
    """
    
    # Default Council - Local models via Ollama (M2 Ultra optimized)
    DEFAULT_COUNCIL = [
        CouncilMember("Oracle", "qwen2.5:72b", "reasoning", 1.3),
        CouncilMember("Sage", "llama3.1:70b", "general", 1.2),
        CouncilMember("Coder", "codestral:latest", "coding", 1.1),
        CouncilMember("Scout", "llama3.2:latest", "fast", 0.9),
    ]
    
    def __init__(self):
        """Initialize the DREAMCHAMBER"""
        CHAMBER_PATH.mkdir(parents=True, exist_ok=True)
        SESSIONS_PATH.mkdir(exist_ok=True)
        
        self.config = self._load_config()
        self.installed_models = self._get_installed_models()
        self.council = self._init_council()
        self.current_session = None
    
    def _load_config(self) -> dict:
        """Load chamber configuration"""
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                return json.load(f)
        return {
            "synthesizer": "qwen3",
            "parallel": True,
            "timeout": 120,
            "max_response_length": 4000
        }
    
    def _save_config(self):
        """Save configuration"""
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def _get_installed_models(self) -> List[str]:
        """Get installed Ollama models"""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
            models = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    models.append(line.split()[0])
            return models
        except:
            return []
    
    def _init_council(self) -> List[CouncilMember]:
        """Initialize available council members"""
        council = []
        for member in self.DEFAULT_COUNCIL:
            model_base = member.model.split(":")[0]
            # Check if model is installed
            for installed in self.installed_models:
                if model_base in installed:
                    member.model = installed
                    council.append(member)
                    break
        
        # Ensure at least Oracle (qwen3) if available
        if not council:
            for m in self.installed_models:
                if "qwen" in m.lower():
                    council.append(CouncilMember("Oracle", m, "reasoning", 1.3))
                    break
        
        return council
    
    def _query_model(self, model: str, prompt: str, thinking: bool = False, timeout: int = 300) -> dict:
        """Query a single model via Ollama"""
        start = time.time()
        
        # Add thinking mode prefix for Qwen3
        if thinking and "qwen" in model.lower():
            prompt = "/think\n" + prompt
        
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            response = result.stdout.strip()
            latency = int((time.time() - start) * 1000)
            
            # Parse thinking blocks from Qwen3
            thinking_content = ""
            if "<think>" in response and "</think>" in response:
                match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
                if match:
                    thinking_content = match.group(1).strip()
                    response = re.sub(r"<think>.*?</think>", "", response, re.DOTALL).strip()
            
            return {
                "response": response,
                "thinking": thinking_content,
                "latency_ms": latency,
                "success": True,
                "error": ""
            }
        except subprocess.TimeoutExpired:
            return {"response": "", "thinking": "", "latency_ms": 0, "success": False, "error": "Timeout"}
        except Exception as e:
            return {"response": "", "thinking": "", "latency_ms": 0, "success": False, "error": str(e)}
    
    # ═══════════════════════════════════════════════════════════════
    # CORE COUNCIL OPERATIONS
    # ═══════════════════════════════════════════════════════════════
    
    def convene(self, question: str, context: str = "", parallel: bool = True) -> dict:
        """
        🌙 CONVENE THE COUNCIL
        
        Query all council members with the same question,
        collect responses for synthesis.
        """
        session_id = f"dream_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(question.encode()).hexdigest()[:6]}"
        
        session = {
            "id": session_id,
            "question": question,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "council_size": len(self.council),
            "responses": [],
            "synthesis": "",
            "insights": [],
            "consensus": "",
            "best_response": "",
            "best_member": ""
        }
        
        full_prompt = f"{context}\n\n{question}" if context else question
        
        print(f"\n🌙 DREAMCHAMBER CONVENED")
        print(f"═" * 50)
        print(f"   Session:  {session_id}")
        print(f"   Question: {question[:60]}{'...' if len(question) > 60 else ''}")
        print(f"   Council:  {len(self.council)} members")
        print(f"═" * 50)
        
        if parallel and len(self.council) > 1:
            # Parallel queries
            with ThreadPoolExecutor(max_workers=min(len(self.council), 6)) as executor:
                futures = {}
                for member in self.council:
                    if member.enabled:
                        thinking = member.specialty == "reasoning"
                        future = executor.submit(
                            self._query_model, member.model, full_prompt, thinking
                        )
                        futures[future] = member
                
                for future in as_completed(futures):
                    member = futures[future]
                    try:
                        result = future.result()
                        result["member"] = member.name
                        result["model"] = member.model
                        result["specialty"] = member.specialty
                        result["weight"] = member.weight
                        session["responses"].append(result)
                        
                        status = "✅" if result["success"] else "❌"
                        chars = len(result.get("response", ""))
                        ms = result.get("latency_ms", 0)
                        print(f"   {status} {member.name:<12} │ {chars:>5} chars │ {ms:>5}ms")
                    except Exception as e:
                        print(f"   ❌ {member.name:<12} │ Error: {e}")
        else:
            # Sequential queries
            for member in self.council:
                if member.enabled:
                    print(f"   ⏳ Querying {member.name}...", end=" ", flush=True)
                    thinking = member.specialty == "reasoning"
                    result = self._query_model(member.model, full_prompt, thinking)
                    result["member"] = member.name
                    result["model"] = member.model
                    result["specialty"] = member.specialty
                    result["weight"] = member.weight
                    session["responses"].append(result)
                    
                    status = "✅" if result["success"] else "❌"
                    print(status)
        
        print(f"═" * 50)
        successful = sum(1 for r in session["responses"] if r["success"])
        print(f"   Complete: {successful}/{len(self.council)} responses")
        
        self.current_session = session
        self._save_session(session)
        
        return session
    
    def synthesize(self, session: dict = None) -> str:
        """
        🔮 SYNTHESIZE COUNCIL WISDOM
        
        Combine all responses into unified, comprehensive wisdom.
        """
        session = session or self.current_session
        if not session:
            return "No session to synthesize"
        
        successful_responses = [r for r in session["responses"] if r["success"] and r["response"]]
        if not successful_responses:
            return "No successful responses to synthesize"
        
        # Build synthesis prompt
        responses_text = "\n\n".join([
            f"═══ {r['member']} ({r['specialty']}) ═══\n{r['response'][:self.config.get('max_response_length', 4000)]}"
            for r in successful_responses
        ])
        
        synthesis_prompt = f"""You are synthesizing wisdom from a council of AI advisors.

ORIGINAL QUESTION:
{session['question']}

COUNCIL RESPONSES:
{responses_text}

YOUR TASK - Create a SYNTHESIS that:
1. Identifies key themes across all responses
2. Notes areas of strong agreement
3. Highlights unique valuable perspectives  
4. Resolves any contradictions intelligently
5. Provides a comprehensive, unified answer

SYNTHESIZED WISDOM:"""
        
        print(f"\n🔮 SYNTHESIZING COUNCIL WISDOM...")
        
        synthesizer = self.config.get("synthesizer", "qwen3")
        result = self._query_model(synthesizer, synthesis_prompt, thinking=True, timeout=180)
        
        session["synthesis"] = result.get("response", "Synthesis failed")
        self._save_session(session)
        
        print(f"   ✅ Synthesis complete ({len(session['synthesis'])} chars)")
        
        return session["synthesis"]
    
    def extract_insights(self, session: dict = None, count: int = 5) -> List[str]:
        """
        💡 EXTRACT KEY INSIGHTS
        
        Pull out the most valuable insights from council responses.
        """
        session = session or self.current_session
        if not session:
            return []
        
        successful = [r for r in session["responses"] if r["success"]]
        if not successful:
            return []
        
        insights_prompt = f"""Extract the TOP {count} most valuable, actionable insights.

QUESTION: {session['question']}

COUNCIL RESPONSES:
{chr(10).join([f"• {r['member']}: {r['response'][:500]}..." for r in successful])}

List exactly {count} insights. Each must be:
- Specific and actionable
- Unique (no duplicates)
- Valuable for answering the question

Format: One insight per line, starting with "- """
        
        result = self._query_model(self.config.get("synthesizer", "qwen3"), insights_prompt, thinking=False)
        
        # Parse insights
        insights = []
        for line in result.get("response", "").split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                insight = line.lstrip("-•").strip()
                if insight and len(insight) > 10:
                    insights.append(insight)
        
        session["insights"] = insights[:count]
        self._save_session(session)
        
        print(f"\n💡 EXTRACTED {len(session['insights'])} INSIGHTS")
        for i, insight in enumerate(session["insights"], 1):
            print(f"   {i}. {insight[:80]}{'...' if len(insight) > 80 else ''}")
        
        return session["insights"]
    
    def find_consensus(self, session: dict = None) -> str:
        """
        🤝 FIND CONSENSUS
        
        Identify what all council members agree on.
        """
        session = session or self.current_session
        if not session:
            return "No session"
        
        successful = [r for r in session["responses"] if r["success"]]
        if len(successful) < 2:
            return "Need at least 2 responses for consensus"
        
        consensus_prompt = f"""Analyze these AI responses for CONSENSUS.

QUESTION: {session['question']}

RESPONSES:
{chr(10).join([f"[{r['member']}]: {r['response'][:600]}" for r in successful])}

Identify:
1. Points ALL models agree on (strong consensus)
2. Points MOST models agree on (general consensus)
3. Any significant disagreements

CONSENSUS ANALYSIS:"""
        
        result = self._query_model(self.config.get("synthesizer", "qwen3"), consensus_prompt, thinking=True)
        
        session["consensus"] = result.get("response", "")
        self._save_session(session)
        
        print(f"\n🤝 CONSENSUS FOUND")
        
        return session["consensus"]
    
    def rank_best(self, session: dict = None) -> dict:
        """
        🏆 RANK & IDENTIFY BEST RESPONSE
        """
        session = session or self.current_session
        if not session:
            return {}
        
        successful = [r for r in session["responses"] if r["success"] and r["response"]]
        if not successful:
            return {}
        
        # Score: weighted combination of length, weight, and latency
        def score(r):
            length_score = min(len(r["response"]) / 1000, 3)  # Cap at 3
            weight_score = r.get("weight", 1.0)
            speed_score = 1.0 / (1 + r.get("latency_ms", 1000) / 5000)
            return length_score * weight_score + speed_score
        
        ranked = sorted(successful, key=score, reverse=True)
        best = ranked[0]
        
        session["best_response"] = best["response"]
        session["best_member"] = best["member"]
        self._save_session(session)
        
        print(f"\n🏆 BEST RESPONSE: {best['member']} ({best['model']})")
        
        return best
    
    def full_analysis(self, question: str, context: str = "") -> dict:
        """
        🌙 FULL DREAMCHAMBER ANALYSIS
        
        Convene → Synthesize → Extract → Consensus → Rank
        All in one call.
        """
        session = self.convene(question, context)
        
        if any(r["success"] for r in session["responses"]):
            self.synthesize(session)
            self.extract_insights(session)
            self.find_consensus(session)
            self.rank_best(session)
        
        return session
    
    def quick_query(self, question: str) -> dict:
        """
        ⚡ QUICK QUERY - Fast response using smallest model only
        """
        # Find fastest model (Scout/llama3.2)
        fast_model = None
        for m in self.council:
            if m.specialty == "fast" or "3.2" in m.model:
                fast_model = m
                break
        
        if not fast_model and self.council:
            fast_model = self.council[-1]  # Use last (usually smallest)
        
        if not fast_model:
            return {"error": "No models available"}
        
        print(f"\n⚡ QUICK QUERY via {fast_model.name}")
        result = self._query_model(fast_model.model, question, thinking=False, timeout=60)
        result["member"] = fast_model.name
        result["model"] = fast_model.model
        
        return result
    
    # ═══════════════════════════════════════════════════════════════
    # SESSION MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    
    def _save_session(self, session: dict):
        """Save session to disk"""
        path = SESSIONS_PATH / f"{session['id']}.json"
        with open(path, "w") as f:
            json.dump(session, f, indent=2)
    
    def load_session(self, session_id: str) -> Optional[dict]:
        """Load a saved session"""
        path = SESSIONS_PATH / f"{session_id}.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None
    
    def list_sessions(self, limit: int = 10) -> List[dict]:
        """List recent sessions"""
        sessions = []
        for f in sorted(SESSIONS_PATH.glob("dream_*.json"), reverse=True)[:limit]:
            with open(f) as file:
                data = json.load(file)
                sessions.append({
                    "id": data["id"],
                    "question": data["question"][:50] + "...",
                    "timestamp": data["timestamp"],
                    "responses": len(data.get("responses", []))
                })
        return sessions
    
    def get_council_status(self) -> dict:
        """Get council status"""
        return {
            "installed_models": len(self.installed_models),
            "council_members": len(self.council),
            "members": [
                {"name": m.name, "model": m.model, "specialty": m.specialty}
                for m in self.council
            ],
            "synthesizer": self.config.get("synthesizer", "qwen3")
        }


# ═══════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🌙 DREAMCHAMBER - AI Council of Wisdom",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dreamchamber ask "What is the best way to learn programming?"
  dreamchamber ask "Explain quantum computing" --full
  dreamchamber status
  dreamchamber sessions
  dreamchamber load dream_20251225_224500_abc123
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Ask command
    ask = subparsers.add_parser("ask", help="Ask the council a question")
    ask.add_argument("question", help="Your question")
    ask.add_argument("--context", "-c", default="", help="Additional context")
    ask.add_argument("--full", "-f", action="store_true", help="Full analysis (synth + insights + consensus)")
    ask.add_argument("--sequential", "-s", action="store_true", help="Query sequentially (not parallel)")
    
    # Status command
    subparsers.add_parser("status", help="Show council status")
    
    # Sessions command
    sessions = subparsers.add_parser("sessions", help="List recent sessions")
    sessions.add_argument("--limit", "-n", type=int, default=10, help="Number of sessions")
    
    # Load command
    load = subparsers.add_parser("load", help="Load a session")
    load.add_argument("session_id", help="Session ID to load")
    
    # Synthesize command
    synth = subparsers.add_parser("synthesize", help="Synthesize current/loaded session")
    synth.add_argument("--session", "-s", help="Session ID (optional)")
    
    args = parser.parse_args()
    
    chamber = DreamChamber()
    
    if args.command == "ask":
        if args.full:
            session = chamber.full_analysis(args.question, args.context)
        else:
            session = chamber.convene(args.question, args.context, parallel=not args.sequential)
        
        print(f"\n📁 Session saved: {session['id']}")
        
    elif args.command == "status":
        status = chamber.get_council_status()
        print(f"\n🌙 DREAMCHAMBER STATUS")
        print(f"═" * 40)
        print(f"   Installed Models: {status['installed_models']}")
        print(f"   Council Members:  {status['council_members']}")
        print(f"   Synthesizer:      {status['synthesizer']}")
        print(f"\n   COUNCIL:")
        for m in status["members"]:
            print(f"   • {m['name']:<12} │ {m['model']:<20} │ {m['specialty']}")
        
    elif args.command == "sessions":
        sessions = chamber.list_sessions(args.limit)
        print(f"\n📜 RECENT SESSIONS ({len(sessions)})")
        print(f"═" * 60)
        for s in sessions:
            print(f"   {s['id']} │ {s['responses']} responses │ {s['question']}")
        
    elif args.command == "load":
        session = chamber.load_session(args.session_id)
        if session:
            chamber.current_session = session
            print(f"\n✅ Loaded: {session['id']}")
            print(f"   Question: {session['question']}")
            print(f"   Responses: {len(session.get('responses', []))}")
            if session.get("synthesis"):
                print(f"   Synthesis: {len(session['synthesis'])} chars")
        else:
            print(f"❌ Session not found: {args.session_id}")
        
    elif args.command == "synthesize":
        if args.session:
            session = chamber.load_session(args.session)
            if session:
                chamber.current_session = session
        
        if chamber.current_session:
            synthesis = chamber.synthesize()
            print(f"\n🔮 SYNTHESIS:\n{synthesis}")
        else:
            print("❌ No session loaded. Use 'ask' or 'load' first.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

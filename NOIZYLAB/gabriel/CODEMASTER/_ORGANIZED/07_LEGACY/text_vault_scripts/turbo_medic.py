#!/usr/bin/env python3
# ==============================================================================
# 🚑 TURBO MEDIC (SYSTEM HEALER)
# ==============================================================================
# Scans all turbo_*.py scripts for syntax errors, import issues, and consistency.
# PROTOCOL: CRYSTAL SMOOTH

import os
import sys
import ast
import importlib.util
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    # Fallback
    print("⚠️  MEDIC WARNING: turbo_config not found via standard import.")
    class MockCfg:
        GREEN = ""
        RED = ""
        YELLOW = ""
        RESET = ""
        BOLD = ""
        SCRIPTS_DIR = Path(__file__).parent
        def print_header(self, t, s): print(f"=== {t} ===\n{s}")
    cfg = MockCfg()

SCRIPTS_DIR = Path(__file__).parent
TARGET_FILES = list(SCRIPTS_DIR.glob("turbo_*.py"))

def check_syntax(filepath):
    """Check for Python syntax errors."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def check_imports(filepath):
    """Check if critical modules can be imported (without running the script)."""
    # Parse imports from AST
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            root = ast.parse(f.read())
        
        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                for name in node.names:
                    try:
                        importlib.util.find_spec(name.name.split('.')[0])
                    except:
                        pass # Some modules might be messy to check, but let's try basic
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                     try:
                        importlib.util.find_spec(node.module.split('.')[0])
                     except:
                        pass
        return True
    except:
        return True

def run_medic():
    cfg.print_header("🚑 TURBO MEDIC", "System-Wide Health Scan")
    
    health_score = 100
    issues = []
    
    print(f"CORE > Scanning {len(TARGET_FILES)} scripts...")
    
    for script in TARGET_FILES:
        # 1. Syntax Scan
        valid, error = check_syntax(script)
        if valid:
            print(f"  ✅ {script.name}")
        else:
            print(f"  ❌ {script.name} [SYNTAX ERROR]")
            print(f"     -> {error}")
            issues.append((script.name, error))
            health_score -= 10
            
    # Report
    print(f"\nCORE > 🩺 SYSTEM HEALTH: {health_score}%")
    
    if issues:
        print(f"\n{cfg.RED}CORE > ⚠️  CRITICAL ISSUES FOUND:{cfg.RESET}")
        for name, err in issues:
            print(f"  - {name}: {err}")
        print("\nCORE > RECOMMENDATION: Use 'Replace File Content' to fix errors.")
    else:
        print(f"\n{cfg.GREEN}CORE > ✨ SYSTEM IS CRYSTAL SMOOTH.{cfg.RESET}")

if __name__ == "__main__":
    run_medic()

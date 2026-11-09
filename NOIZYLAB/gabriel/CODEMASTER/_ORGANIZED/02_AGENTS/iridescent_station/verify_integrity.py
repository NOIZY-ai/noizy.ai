
import os
import sys

def test_imports():
    print("Testing imports...")
    try:
        import streamlit
        import google.generativeai
        import functions_framework
        print("✅ Core dependencies found.")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        sys.exit(1)

def lint_app():
    print("Linting app.py...")
    try:
        # Just compile it to check for syntax errors
        with open("app.py", "r") as f:
            compile(f.read(), "app.py", "exec")
        print("✅ app.py syntax is valid.")
    except Exception as e:
        print(f"❌ app.py syntax error: {e}")
        sys.exit(1)

def lint_worker():
    print("Linting google_worker.py...")
    try:
        with open("google_worker.py", "r") as f:
            compile(f.read(), "google_worker.py", "exec")
        print("✅ google_worker.py syntax is valid.")
    except Exception as e:
        print(f"❌ google_worker.py syntax error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_imports()
    lint_app()
    lint_worker()
    print("--- INTEGRITY CHECK PASSED ---")

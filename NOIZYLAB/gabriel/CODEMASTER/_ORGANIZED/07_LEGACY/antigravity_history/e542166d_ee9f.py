#!/usr/bin/env python3
"""
prompt_contract.py
The Gatekeeper. Schema or Reject.
Part of the MIACLE Spine.
"""
import json
from typing import Dict, Any

class PromptContract:
    @staticmethod
    def validate(data: Any, schema: Dict[str, Any]) -> bool:
        """
        Simple Schema Validator.
        Enforces types and required keys.
        """
        # 1. Type Check
        if not isinstance(data, dict):
            print("❌ [Contract] REJECT: Root must be a JSON Object.")
            return False

        # 2. Key Check
        for key, expected_type in schema.items():
            if key not in data:
                print(f"❌ [Contract] REJECT: Missing required key '{key}'.")
                return False
            
            # Simple type mapping
            py_type = {
                "string": str,
                "int": int,
                "list": list,
                "dict": dict,
                "bool": bool
            }.get(expected_type)

            if py_type and not isinstance(data[key], py_type):
                print(f"❌ [Contract] REJECT: Key '{key}' must be {expected_type}.")
                return False

        print("✅ [Contract] ACCEPT: Schema Valid.")
        return True

if __name__ == "__main__":
    # Test Contract
    schema = {
        "action": "string",
        "rationale": "string",
        "confidence": "float" # This will fail our simple mapper above, intentional for test
    }
    
    payload = {
        "action": "deploy",
        "rationale": "tested",
        # Missing confidence
    }
    
    PromptContract.validate(payload, schema)

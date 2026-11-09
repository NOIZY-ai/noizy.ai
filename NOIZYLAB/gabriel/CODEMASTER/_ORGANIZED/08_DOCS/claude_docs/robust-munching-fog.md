# Plan: Store Anthropic API Key in macOS Keychain

## Objective
Securely store the user's Anthropic API key in macOS Keychain so NLR_01 can access it.

## Steps

1. **Receive API key from user**
   - User provides their Anthropic API key (starts with `sk-ant-...`)

2. **Store in Keychain**
   - Run: `security add-generic-password -s "NLR_01" -a "anthropic_api_key" -w "<API_KEY>"`
   - This stores the key securely in macOS Keychain under service "NLR_01"

3. **Verify storage**
   - Run: `security find-generic-password -s "NLR_01" -a "anthropic_api_key"`
   - Confirms the entry exists (without revealing the key)

## Files Already Configured
- `/Users/m2ultra/NOIZYLAB/PROJECTS/NLR_01/config/config.yaml` - Already references `${keychain:NLR_01:anthropic_api_key}`
- `/Users/m2ultra/NOIZYLAB/PROJECTS/NLR_01/src/config.py` - Already has Keychain lookup functions

## Ready for Execution
Once the user provides their API key, a single command stores it securely.

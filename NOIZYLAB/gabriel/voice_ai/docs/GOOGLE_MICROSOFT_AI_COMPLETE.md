# 🚀 GOOGLE & MICROSOFT AI - COMPLETE INSTALLATION GUIDE
**Created:** December 24, 2025  
**System:** macOS (M2 Ultra)  
**Status:** ACTIVE INSTALLATION

---

## 📋 TABLE OF CONTENTS
1. [Google AI Products](#google-ai-products)
2. [Microsoft AI Products](#microsoft-ai-products)
3. [Installation Status](#installation-status)
4. [API Setup](#api-setup)
5. [Web-Based Access](#web-based-access)
6. [Command Line Tools](#command-line-tools)

---

## 🔵 GOOGLE AI PRODUCTS

### 1. **Gemini AI Model**
- **Description:** Advanced multimodal LLM (text, image, audio)
- **Versions:** Nano, Pro, Ultra, Gemini 2.5, Gemini 3 Pro
- **Access Methods:**
  - Web: https://gemini.google.com
  - iOS/Android: Gemini app
  - API: Google AI Studio (https://aistudio.google.com)
- **Installation:**
  ```bash
  # Web-based (no install needed)
  open https://gemini.google.com
  
  # API access via Python
  pip install google-generativeai
  ```

### 2. **NotebookLM**
- **Description:** AI-powered research & note-taking tool
- **Features:** Audio Overview (podcast summaries), document synthesis
- **Access:** Web-based at https://notebooklm.google.com
- **Installation:** Browser-based only (Chrome recommended)

### 3. **Antigravity**
- **Description:** Google's development tool (installed ✅)
- **Location:** `/Applications/Antigravity.app`
- **Installation:**
  ```bash
  brew install --cask antigravity
  ```
- **Status:** ✅ INSTALLED

### 4. **Veo Video Generation**
- **Description:** Text-to-video model (1080p, 4K in Veo 2)
- **Access:** Via Google AI Studio (https://aistudio.google.com)
- **Status:** Web-based API access

### 5. **Nano Banana 2**
- **Description:** AI image generation (integrated in Gemini app)
- **Features:** Enhanced control, color precision, text alignment
- **Access:** Via Gemini app/web interface

### 6. **SynthID Detector**
- **Description:** Watermarking tool for AI-generated content detection
- **Access:** Via Google AI Studio
- **Status:** API-based

### 7. **LearnLM**
- **Description:** Personal AI tutor models
- **Access:** Integrated in Google services
- **Status:** Web-based

### 8. **Google Chrome** (AI-Enhanced)
- **Status:** ✅ INSTALLED at `/Applications/Google Chrome.app`
- **Features:** AI-powered search, Gemini integration

---

## 🔴 MICROSOFT AI PRODUCTS

### 1. **Microsoft Copilot**
- **Description:** Generative AI chatbot (replaces Cortana)
- **Integration:** Microsoft 365, Bing, Edge, Windows
- **Access Methods:**
  - Web: https://copilot.microsoft.com
  - Edge Browser: Built-in
  - Microsoft 365: Integrated in Office apps
- **Installation:**
  ```bash
  # Access via Edge (already installed)
  open -a "Microsoft Edge" https://copilot.microsoft.com
  ```

### 2. **Azure Copilot**
- **Description:** AI companion for Azure cloud operations
- **Features:** Migration, deployment, resource optimization
- **Access:** Via Azure Portal (https://portal.azure.com)
- **CLI:** ✅ Azure CLI installed (`az --version`)

### 3. **Microsoft Designer**
- **Description:** AI-based image creation & design app
- **Platforms:** Windows 11, iOS, Android, Web
- **Access:** https://designer.microsoft.com
- **Status:** Web-based (no macOS native app)

### 4. **Microsoft Edge** (AI-Enhanced)
- **Status:** ✅ INSTALLED at `/Applications/Microsoft Edge.app`
- **Features:** Copilot integration, AI-powered search

### 5. **Azure Machine Learning**
- **Description:** Enterprise ML lifecycle management
- **Access:** Via Azure Portal
- **CLI:** Available via `az ml` commands

### 6. **Foundry Tools**
- **Description:** Ready-to-use APIs for intelligent agents
- **Access:** Via Azure Cognitive Services
- **Status:** API-based

### 7. **Microsoft Teams** (AI Features)
- **Features:** Real-time transcription, translation, meeting summaries
- **Installation:** Requires sudo (manual install needed)
- **Status:** ⚠️ Pending (needs password)

### 8. **Microsoft 365 Copilot**
- **Description:** AI integrated in Word, Excel, PowerPoint, Outlook
- **Access:** Requires Microsoft 365 subscription
- **Status:** Subscription-based

---

## ✅ INSTALLATION STATUS

### Installed & Ready:
- ✅ **Antigravity** - `/Applications/Antigravity.app`
- ✅ **Google Chrome** - `/Applications/Google Chrome.app`
- ✅ **Microsoft Edge** - `/Applications/Microsoft Edge.app`
- ✅ **Azure CLI** - `/opt/homebrew/bin/az` (v2.81.0)
- ✅ **Gemini 2** (file finder) - `/Applications/Gemini 2.app`

### Web-Based (No Install Needed):
- 🌐 **Gemini** - https://gemini.google.com
- 🌐 **NotebookLM** - https://notebooklm.google.com
- 🌐 **Google AI Studio** - https://aistudio.google.com
- 🌐 **Microsoft Copilot** - https://copilot.microsoft.com
- 🌐 **Microsoft Designer** - https://designer.microsoft.com
- 🌐 **Azure Portal** - https://portal.azure.com

### Pending Installation:
- ⚠️ **Microsoft Teams** - Requires sudo password

---

## 🔑 API SETUP

### Google AI API Setup:
1. **Get API Key:**
   - Visit: https://aistudio.google.com/apikey
   - Create new API key
   - Save to environment variable:
     ```bash
     export GOOGLE_AI_API_KEY="your-key-here"
     echo 'export GOOGLE_AI_API_KEY="your-key-here"' >> ~/.zshrc
     ```

2. **Install Python SDK:**
   ```bash
   pip install google-generativeai
   ```

3. **Test Connection:**
   ```python
   import google.generativeai as genai
   genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Hello!")
   print(response.text)
   ```

### Microsoft Azure AI Setup:
1. **Install Azure CLI** (✅ Already installed):
   ```bash
   az --version  # Verify installation
   ```

2. **Login to Azure:**
   ```bash
   az login
   ```

3. **Set Subscription:**
   ```bash
   az account list --output table
   az account set --subscription "Your-Subscription-Name"
   ```

4. **Create OpenAI Resource:**
   ```bash
   az group create --name ai-resources --location eastus
   az cognitiveservices account create \
     --name your-openai-resource \
     --resource-group ai-resources \
     --kind OpenAI \
     --sku S0 \
     --location eastus
   ```

5. **Get API Key:**
   ```bash
   az cognitiveservices account keys list \
     --name your-openai-resource \
     --resource-group ai-resources
   ```

6. **Set Environment Variable:**
   ```bash
   export AZURE_OPENAI_API_KEY="your-key-here"
   export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
   echo 'export AZURE_OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
   echo 'export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"' >> ~/.zshrc
   ```

---

## 🌐 WEB-BASED ACCESS

### Quick Launch Commands:
```bash
# Google AI
open https://gemini.google.com
open https://notebooklm.google.com
open https://aistudio.google.com

# Microsoft AI
open -a "Microsoft Edge" https://copilot.microsoft.com
open https://designer.microsoft.com
open https://portal.azure.com
```

### Browser Bookmarks:
- **Google Gemini:** https://gemini.google.com
- **NotebookLM:** https://notebooklm.google.com
- **Google AI Studio:** https://aistudio.google.com
- **Microsoft Copilot:** https://copilot.microsoft.com
- **Microsoft Designer:** https://designer.microsoft.com
- **Azure Portal:** https://portal.azure.com

---

## 💻 COMMAND LINE TOOLS

### Google AI CLI:
```bash
# Install Gemini CLI (if available)
brew install gemini-cli  # Check availability

# Use Google AI via Python
pip install google-generativeai
```

### Microsoft Azure CLI:
```bash
# Already installed ✅
az --version

# Common commands
az login
az account list
az cognitiveservices account list
az ml workspace list
```

### Quick Test Scripts:
```bash
# Test Google AI API
python3 << EOF
import os
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
print(model.generate_content("Hello from Gemini!").text)
EOF

# Test Azure CLI
az account show
```

---

## 📊 COMPLETE PRODUCT MATRIX

| Product | Type | Access | Status |
|---------|------|--------|--------|
| **Google Gemini** | LLM | Web/API | 🌐 Available |
| **NotebookLM** | Research Tool | Web | 🌐 Available |
| **Antigravity** | Dev Tool | App | ✅ Installed |
| **Veo** | Video Gen | API | 🌐 Available |
| **Nano Banana 2** | Image Gen | Gemini App | 🌐 Available |
| **SynthID** | Detection | API | 🌐 Available |
| **LearnLM** | Education | Integrated | 🌐 Available |
| **Microsoft Copilot** | Chatbot | Web/Edge | 🌐 Available |
| **Azure Copilot** | Cloud AI | Portal/CLI | ✅ CLI Ready |
| **Microsoft Designer** | Image Gen | Web | 🌐 Available |
| **Azure ML** | ML Platform | Portal/CLI | ✅ CLI Ready |
| **Foundry Tools** | APIs | Azure | 🌐 Available |
| **Teams AI** | Collaboration | App | ⚠️ Pending |

---

## 🚀 NEXT STEPS

1. **Get API Keys:**
   - Google AI: https://aistudio.google.com/apikey
   - Azure OpenAI: Create via Azure Portal

2. **Set Environment Variables:**
   ```bash
   # Add to ~/.zshrc
   export GOOGLE_AI_API_KEY="your-key"
   export AZURE_OPENAI_API_KEY="your-key"
   export AZURE_OPENAI_ENDPOINT="your-endpoint"
   ```

3. **Install Python Packages:**
   ```bash
   pip install google-generativeai openai azure-ai-textanalytics
   ```

4. **Test Installations:**
   ```bash
   # Test Google
   open https://gemini.google.com
   
   # Test Microsoft
   open -a "Microsoft Edge" https://copilot.microsoft.com
   
   # Test Azure CLI
   az --version
   ```

5. **Create Quick Access Scripts:**
   ```bash
   # Create aliases in ~/.zshrc
   alias gemini="open https://gemini.google.com"
   alias copilot="open -a 'Microsoft Edge' https://copilot.microsoft.com"
   alias notebooklm="open https://notebooklm.google.com"
   alias designer="open https://designer.microsoft.com"
   ```

---

## 📝 NOTES

- Most Google AI tools are web-based (no local install needed)
- Microsoft Copilot is integrated in Edge browser
- Azure CLI provides command-line access to all Azure AI services
- API keys required for programmatic access
- Some tools require subscriptions (Microsoft 365, Azure)

---

**GORUNFREE!** 🚀  
**Last Updated:** December 24, 2025


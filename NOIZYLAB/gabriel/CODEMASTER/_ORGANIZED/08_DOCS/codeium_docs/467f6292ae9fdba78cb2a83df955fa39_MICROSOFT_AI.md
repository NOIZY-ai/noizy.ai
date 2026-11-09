�%# 🔷 MICROSOFT AI - COMPLETE GUIDE

## Azure OpenAI Service

### Configuration for OpenManus

```toml
[llm]
api_type = "azure"
model = "gpt-4o"
base_url = "https://YOUR_RESOURCE.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT"
api_key = "YOUR_AZURE_OPENAI_KEY"
api_version = "2024-08-01-preview"
max_tokens = 8192
temperature = 0.7
```

### Azure OpenAI Models

| Model | Deployment Name | Use Case |
|-------|-----------------|----------|
| GPT-4o | gpt-4o | Best multimodal |
| GPT-4o-mini | gpt-4o-mini | Fast + cheap |
| GPT-4 Turbo | gpt-4-turbo | High quality |
| o1 | o1 | Advanced reasoning |
| o1-mini | o1-mini | Fast reasoning |

---

## Microsoft 365 Copilot

### Features
- **Word**: Draft, rewrite, summarize documents
- **Excel**: Analyze data, create formulas, generate charts
- **PowerPoint**: Create presentations from prompts
- **Outlook**: Draft emails, summarize threads
- **Teams**: Meeting summaries, action items
- **OneNote**: Organize and summarize notes

### API Access
Microsoft Graph API + Copilot plugins:
```
https://graph.microsoft.com/v1.0/
```

---

## Azure AI Services (Cognitive Services)

### Vision
| Service | Endpoint | Use |
|---------|----------|-----|
| Computer Vision | `/vision/v3.2/analyze` | Image analysis |
| Face API | `/face/v1.0/detect` | Face detection |
| Custom Vision | `/customvision/v3.0/` | Custom models |
| Document Intelligence | `/formrecognizer/v2.1/` | OCR, forms |

### Speech
| Service | Endpoint | Use |
|---------|----------|-----|
| Speech-to-Text | `/speech/recognition/` | Transcription |
| Text-to-Speech | `/speech/synthesis/` | Voice generation |
| Speech Translation | `/speech/translation/` | Real-time translate |
| Speaker Recognition | `/speaker/verification/` | Voice ID |

### Language
| Service | Endpoint | Use |
|---------|----------|-----|
| Text Analytics | `/text/analytics/v3.1/` | Sentiment, entities |
| Translator | `/translator/text/v3.0/` | Translation |
| Language Understanding | `/luis/v3.0/` | Intent detection |
| QnA Maker | `/qnamaker/v5.0/` | FAQ bots |

---

## Azure Machine Learning

### Endpoints
- **Managed Online Endpoints**: Real-time inference
- **Batch Endpoints**: Large-scale batch processing
- **Serverless API**: Pay-per-token models

### Serverless Models (No Deployment)
```python
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential("YOUR_GITHUB_TOKEN")
)
```

Available models:
- Llama 3.1 405B
- Mistral Large
- Phi-3
- Cohere Command R+

---

## GitHub Copilot

### IDE Integration
- VS Code, Visual Studio, JetBrains, Neovim
- Code completion, chat, inline suggestions

### API (via GitHub Models)
```bash
curl https://models.inference.ai.azure.com/chat/completions \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## Bing AI / Copilot (Consumer)

### Web Access
- https://copilot.microsoft.com
- https://bing.com/chat

### Features
- Web search grounding
- Image generation (DALL-E 3)
- Code interpreter
- Plugin ecosystem

---

## Microsoft Designer (Image AI)

### Features
- AI image generation
- Background removal
- Design templates
- Brand kit integration

### Access
- https://designer.microsoft.com
- Integrated in Microsoft 365

---

## Power Platform AI

### Power Automate
- AI Builder actions
- Document processing
- Text recognition
- Sentiment analysis

### Power Apps
- Copilot for app building
- AI-powered forms
- Intelligent data extraction

### Power BI
- Copilot for reports
- Natural language queries
- Auto-insights

---

## API Keys & Endpoints

### Get Azure OpenAI Key
1. Azure Portal → Create "Azure OpenAI" resource
2. Keys and Endpoint → Copy Key 1
3. Deploy a model in Azure AI Studio

### Get GitHub Token (for GitHub Models)
1. GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate new token with `models:read` scope

---

## Quick Setup for OpenManus

### Azure OpenAI
```toml
[llm]
api_type = "azure"
model = "gpt-4o"
base_url = "https://YOUR_RESOURCE.openai.azure.com/openai/deployments/gpt-4o"
api_key = "YOUR_KEY"
api_version = "2024-08-01-preview"
```

### GitHub Models (Free Tier)
```toml
[llm]
model = "gpt-4o"
base_url = "https://models.inference.ai.azure.com"
api_key = "YOUR_GITHUB_TOKEN"
```

---

## Pricing (Azure OpenAI)

| Model | Input (1M tokens) | Output (1M tokens) |
|-------|-------------------|---------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| o1 | $15.00 | $60.00 |
| o1-mini | $3.00 | $12.00 |

---

*Microsoft AI Guide • NOIZYLAB*
�%*cascade08"(a1b6a0eed5fda92b075b21780c1e15f048a239dd2@file:///Users/m2ultra/NOIZYLAB/AI_COMMAND_CENTER/MICROSOFT_AI.md:file:///Users/m2ultra/NOIZYLAB
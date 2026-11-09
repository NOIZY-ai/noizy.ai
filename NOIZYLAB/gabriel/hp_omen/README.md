# GABRIEL HP-OMEN Integration

## GABRIEL Workers AI Controller

**GABRIEL DIRECTS & CONTROLS ALL WORKERS AI INFERENCE**

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     GABRIEL INFINITY X1000                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║   ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐   ║
║   │  Cloudflare     │      │    Workers AI   │      │   HP-OMEN       │   ║
║   │  Workers Edge   │◄────►│    Models       │◄────►│   Bridge        │   ║
║   │                 │      │                 │      │   10.0.0.160    │   ║
║   └────────┬────────┘      └────────┬────────┘      └────────┬────────┘   ║
║            │                        │                        │            ║
║            ▼                        ▼                        ▼            ║
║   ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐   ║
║   │  D1 MemCell     │      │  KV Cache       │      │  R2 Storage     │   ║
║   │  (Memories)     │      │  (Fast Access)  │      │  (Files)        │   ║
║   └─────────────────┘      └─────────────────┘      └─────────────────┘   ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Quick Start

### Deploy to Cloudflare

```bash
cd hp_omen

# Install dependencies
npm install

# Create D1 database
npm run db:create

# Create KV namespace
npm run kv:create

# Create R2 bucket
npm run r2:create

# Create Queue
npm run queue:create

# Update wrangler.toml with IDs from above commands

# Run migrations
npm run db:migrate

# Deploy to Cloudflare
npm run deploy
```

### Test the API

```bash
# Status
curl https://gabriel-hp-omen.<your-subdomain>.workers.dev/api/status

# Think
curl -X POST https://gabriel-hp-omen.<your-subdomain>.workers.dev/api/think \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is GABRIEL?"}'

# OpenAI-compatible
curl -X POST https://gabriel-hp-omen.<your-subdomain>.workers.dev/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello GABRIEL"}]}'
```

## Available Models

| Model | ID | Best For |
|-------|-----|----------|
| Llama 3.3 70B | `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | General reasoning |
| Llama 3.1 8B | `@cf/meta/llama-3.1-8b-instruct` | Fast responses |
| DeepSeek R1 | `@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | Deep reasoning |
| Qwen 2.5 72B | `@cf/qwen/qwen2.5-72b-instruct` | Complex tasks |
| Qwen Coder | `@cf/qwen/qwen2.5-coder-32b-instruct` | Code generation |
| Hermes 2 Pro | `@hf/nousresearch/hermes-2-pro-mistral-7b` | Function calling |
| BGE Large | `@cf/baai/bge-large-en-v1.5` | Embeddings |
| LLaVA | `@cf/llava-hf/llava-1.5-7b-hf` | Vision |

## API Endpoints

### Core Inference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | System status and capabilities |
| `/api/think` | POST | Direct inference |
| `/api/stream` | POST | Streaming inference |
| `/api/embed` | POST | Generate embeddings |
| `/api/code` | POST | Code generation (Qwen Coder) |
| `/api/reason` | POST | Deep reasoning (DeepSeek R1) |

### OpenAI-Compatible

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/completions` | POST | Chat completions (streaming supported) |
| `/v1/embeddings` | POST | Embeddings API |

### Function Calling

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tools/list` | GET | List traditional tools |
| `/api/tools/call` | POST | Traditional function calling |
| `/api/embedded/tools` | GET | List embedded tools |
| `/api/embedded/call` | POST | Embedded function calling (runWithTools) |

### Batch API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/batch/submit` | POST | Queue batch job |
| `/api/batch/status/:id` | GET | Check batch status |
| `/api/batch/results/:id` | GET | Get batch results |
| `/api/native-batch/submit` | POST | Native Workers AI batch |
| `/api/native-batch/poll` | POST | Poll native batch status |

## Embedded Tools

GABRIEL includes 10 built-in tools for embedded function calling:

| Tool | Description |
|------|-------------|
| `search_knowledge` | Search GABRIEL's memory database |
| `remember` | Store information for future recall |
| `cache_get` | Retrieve cached values |
| `cache_set` | Store values in KV cache |
| `fetch_web` | Fetch content from URLs |
| `hp_omen_status` | Check HP-OMEN machine status |
| `hp_omen_send` | Send messages to HP-OMEN |
| `storage_list` | List R2 storage files |
| `storage_get` | Get files from R2 storage |
| `calculate` | Perform math calculations |

### Example: Embedded Tool Call

```bash
curl -X POST https://gabriel-hp-omen.workers.dev/api/embedded/call \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Check if HP-OMEN is online and remember the result",
    "verbose": true
  }'
```

## Network Topology

```
╔═══════════════════════════════════════════════════════════════╗
║                    GABRIEL NETWORK MESH                       ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   M2Ultra (Mac Studio)        HP-OMEN (DaFixer/RSP)           ║
║   ├── VPN: 10.100.0.1         ├── VPN: 10.100.0.2             ║
║   ├── LAN: 10.0.0.x           ├── LAN: 10.0.0.160             ║
║   └── Port: 5174              └── Port: 5175                  ║
║                                                               ║
║   PORTAL_PAD                  MOBILE                          ║
║   └── VPN: 10.100.0.3         └── VPN: 10.100.0.4             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## HP-OMEN Bridge

### Local Bridge Endpoints (Python Flask)

| Endpoint | Description |
|----------|-------------|
| `GET /api/bridge/status` | Bridge status (hostname, IP, uptime, peers) |
| `GET /api/bridge/peers` | List discovered peers |
| `GET /api/bridge/discover` | Trigger UDP discovery broadcast |
| `GET /api/bridge/ping/<ip>` | Ping a specific IP |
| `POST /api/bridge/send` | Send message to peer |

### Start HP-OMEN Bridge

```bash
# On HP-OMEN machine
pip3 install -r requirements.txt
python3 network_bridge.py
```

### Deploy from M2Ultra

```bash
# Connect to HP-OMEN via VPN
./connect_omen.sh

# Deploy GABRIEL to HP-OMEN
./deploy_gabriel_remote.sh

# Monitor connection
python3 connection_monitor.py
```

## Files

| File | Description |
|------|-------------|
| `src/index.ts` | Main Workers AI Controller |
| `src/tools.ts` | Embedded function calling tools |
| `schema.sql` | D1 database schema |
| `wrangler.toml` | Cloudflare Workers config |
| `package.json` | Dependencies |
| `network_bridge.py` | Flask-based network bridge |
| `gabriel_uplink.py` | Whisper voice transmission |
| `deploy_gabriel_remote.sh` | SSH deployment script |

## SMB Volumes (HP-OMEN)

```
/Volumes/4TB Big Fish     - 1.9Ti available
/Volumes/4TB Blue Fish    - 64Gi available
/Volumes/4TB FISH SG      - 710Gi available
/Volumes/EW               - 66Gi available
/Volumes/FISH             - 145Gi available
/Volumes/RSP              - 145Gi available
```

## GORUNFREEX1000

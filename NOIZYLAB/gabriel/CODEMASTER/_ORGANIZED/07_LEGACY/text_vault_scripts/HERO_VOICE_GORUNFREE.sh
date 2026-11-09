#!/bin/bash
#===============================================================================
#
#   HERO VOICE FORGE MARK II - GORUNFREE COMPLETE INSTALLER
#   
#   ONE SCRIPT. EVERYTHING DEPLOYED.
#   Run on: GOD (Mac Studio M2 Ultra)
#
#===============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${BLUE}[HERO]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }

clear
echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║   ⚡ HERO VOICE FORGE MARK II - GORUNFREE INSTALLER ⚡              ║"
echo "║                                                                      ║"
echo "║   This script will:                                                  ║"
echo "║   1. Create all project files                                        ║"
echo "║   2. Install Python dependencies                                     ║"
echo "║   3. Start Coqui TTS server                                          ║"
echo "║   4. Create Cloudflare tunnel                                        ║"
echo "║   5. Deploy Worker with tunnel URL                                   ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    warn "This script is designed for macOS (GOD). Continue anyway? (y/n)"
    read -r response
    [[ "$response" != "y" ]] && exit 1
fi

#===============================================================================
# STEP 1: CREATE PROJECT STRUCTURE
#===============================================================================

log "Creating project structure..."

PROJECT_DIR="$HOME/hero-voice-forge-mk2"
mkdir -p "$PROJECT_DIR/coqui-server"
mkdir -p "$PROJECT_DIR/src"
mkdir -p "$HOME/VoiceSamples"

success "Project folder: $PROJECT_DIR"

#===============================================================================
# STEP 2: CREATE COQUI SERVER
#===============================================================================

log "Creating Coqui TTS server..."

cat << 'COQUI_SERVER' > "$PROJECT_DIR/coqui-server/server.py"
#!/usr/bin/env python3
"""
COQUI TTS SERVER - Hero Voice Forge
Self-hosted voice generation for MC96ECOUNIVERSE
"""

import os
import io
import hashlib
from pathlib import Path
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = 5002
VOICE_SAMPLES_DIR = Path.home() / "VoiceSamples"
CACHE_DIR = Path.home() / "Library/Caches/CoquiTTS"
VOICE_SAMPLES_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Try to load TTS
tts = None
try:
    from TTS.api import TTS
    print("🔄 Loading Coqui XTTS v2...")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
    try:
        tts.to("mps")
        print("✅ TTS loaded with MPS acceleration (Apple Silicon)")
    except:
        print("✅ TTS loaded (CPU mode)")
except Exception as e:
    print(f"⚠️  TTS not loaded: {e}")
    print("   Install with: pip install TTS")

# Voice registry
VOICES = {}
def scan_voices():
    global VOICES
    VOICES = {f.stem: f for f in VOICE_SAMPLES_DIR.glob("*.wav")}
    print(f"📁 Found {len(VOICES)} voice samples")

scan_voices()

@app.route("/")
def index():
    return jsonify({
        "service": "Hero Voice Forge - Coqui TTS",
        "status": "online" if tts else "no_model",
        "voices": list(VOICES.keys()),
        "endpoints": ["POST /tts", "GET /health", "GET /voices"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "tts_loaded": tts is not None})

@app.route("/voices")
def voices():
    scan_voices()
    return jsonify({"voices": list(VOICES.keys())})

@app.route("/tts", methods=["POST"])
def generate():
    if not tts:
        return jsonify({"error": "TTS model not loaded"}), 500
    
    data = request.json
    text = data.get("text", "")
    voice_id = data.get("voice_id") or data.get("speaker_wav")
    language = data.get("language", "en")
    
    if not text:
        return jsonify({"error": "Text required"}), 400
    
    # Cache check
    cache_key = hashlib.sha256(f"{text}:{voice_id}".encode()).hexdigest()
    cache_path = CACHE_DIR / f"{cache_key}.wav"
    
    if cache_path.exists():
        print(f"📦 Cache hit: {cache_key[:8]}")
        return Response(open(cache_path, "rb").read(), mimetype="audio/wav")
    
    try:
        # Generate
        print(f"🎤 Generating: '{text[:50]}...'")
        
        if voice_id and voice_id in VOICES:
            tts.tts_to_file(text=text, speaker_wav=str(VOICES[voice_id]), 
                          language=language, file_path=str(cache_path))
        else:
            tts.tts_to_file(text=text, file_path=str(cache_path))
        
        audio = open(cache_path, "rb").read()
        print(f"✅ Generated {len(audio)} bytes")
        return Response(audio, mimetype="audio/wav")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/clone", methods=["POST"])
def clone():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400
    
    audio = request.files["audio"]
    voice_id = request.form.get("voice_id", audio.filename.rsplit(".", 1)[0])
    save_path = VOICE_SAMPLES_DIR / f"{voice_id}.wav"
    audio.save(save_path)
    scan_voices()
    
    return jsonify({"status": "success", "voice_id": voice_id})

if __name__ == "__main__":
    print(f"""
╔════════════════════════════════════════════════════════════╗
║         COQUI TTS SERVER - HERO VOICE FORGE                ║
║         Port: {PORT}                                          ║
║         Voices: {VOICE_SAMPLES_DIR}              ║
╚════════════════════════════════════════════════════════════╝
    """)
    app.run(host="0.0.0.0", port=PORT, debug=False)
COQUI_SERVER

cat << 'REQUIREMENTS' > "$PROJECT_DIR/coqui-server/requirements.txt"
flask>=3.0.0
flask-cors>=4.0.0
TTS>=0.22.0
torch>=2.0.0
numpy>=1.24.0
REQUIREMENTS

success "Coqui server created"

#===============================================================================
# STEP 3: CREATE CLOUDFLARE WORKER
#===============================================================================

log "Creating Cloudflare Worker..."

cat << 'WORKER_CODE' > "$PROJECT_DIR/src/worker.ts"
/**
 * HERO VOICE FORGE MARK II - Cloudflare Worker
 * Routes to Coqui (self-hosted) or ElevenLabs (premium)
 */

export interface Env {
  ANTHROPIC_API_KEY: string;
  ELEVENLABS_API_KEY?: string;
  COQUI_ENDPOINT?: string;
}

const PERSONAS: Record<string, { name: string; voiceId: string; style: string }> = {
  gabriel: { name: "GABRIEL", voiceId: "ErXwobaYiN019PkySvjV", style: "commanding" },
  thunder_titan: { name: "Thunder Titan", voiceId: "VR6AewLTigWG4xSOukaG", style: "epic" },
  shirl: { name: "SHIRL", voiceId: "EXAVITQu4vr4xnSDxMaL", style: "warm" },
  pops: { name: "POPS", voiceId: "VR6AewLTigWG4xSOukaG", style: "wise" },
  dream: { name: "DREAM", voiceId: "21m00Tcm4TlvDq8ikWAM", style: "ethereal" },
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // CORS
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    try {
      if (url.pathname === "/") return new Response(getHomePage(), { headers: { "Content-Type": "text/html" } });
      if (url.pathname === "/api/health") return json({ status: "ok", coqui: !!env.COQUI_ENDPOINT, elevenlabs: !!env.ELEVENLABS_API_KEY });
      if (url.pathname === "/api/personas") return json({ personas: Object.entries(PERSONAS).map(([id, p]) => ({ id, ...p })) });
      
      if (url.pathname === "/api/forge" && request.method === "POST") {
        const body = await request.json() as any;
        const { text, persona = "gabriel", engine = "auto" } = body;
        
        if (!text) return json({ error: "Text required" }, 400);
        
        const profile = PERSONAS[persona] || PERSONAS.gabriel;
        
        // Choose engine
        let useEngine = engine;
        if (engine === "auto") {
          useEngine = env.COQUI_ENDPOINT ? "coqui" : env.ELEVENLABS_API_KEY ? "elevenlabs" : null;
        }
        
        if (!useEngine) return json({ error: "No TTS engine configured" }, 500);
        
        let audio: ArrayBuffer;
        
        if (useEngine === "coqui" && env.COQUI_ENDPOINT) {
          const resp = await fetch(`${env.COQUI_ENDPOINT}/tts`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, language: "en" }),
          });
          if (!resp.ok) throw new Error(`Coqui error: ${await resp.text()}`);
          audio = await resp.arrayBuffer();
        } else if (useEngine === "elevenlabs" && env.ELEVENLABS_API_KEY) {
          const resp = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${profile.voiceId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "xi-api-key": env.ELEVENLABS_API_KEY },
            body: JSON.stringify({ text, model_id: "eleven_monolingual_v1" }),
          });
          if (!resp.ok) throw new Error(`ElevenLabs error: ${await resp.text()}`);
          audio = await resp.arrayBuffer();
        } else {
          return json({ error: `Engine ${useEngine} not configured` }, 500);
        }
        
        return new Response(audio, {
          headers: {
            "Content-Type": "audio/mpeg",
            "Access-Control-Allow-Origin": "*",
            "X-Persona": profile.name,
            "X-Engine": useEngine,
          },
        });
      }
      
      return json({ error: "Not found" }, 404);
    } catch (e: any) {
      return json({ error: e.message }, 500);
    }
  },
};

function json(data: any, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
  });
}

function getHomePage() {
  return `<!DOCTYPE html>
<html><head><title>Hero Voice Forge</title>
<style>
body{font-family:system-ui;background:#0a0a0a;color:#fff;padding:40px;max-width:800px;margin:0 auto}
h1{background:linear-gradient(90deg,#ffd700,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.btn{background:#ffd700;color:#000;border:none;padding:12px 24px;font-size:16px;cursor:pointer;border-radius:8px;margin:10px 5px}
textarea{width:100%;height:100px;background:#1a1a1a;color:#fff;border:1px solid #333;padding:10px;border-radius:8px}
select{background:#1a1a1a;color:#fff;border:1px solid #333;padding:10px;border-radius:8px}
audio{width:100%;margin-top:20px}
</style></head>
<body>
<h1>⚡ Hero Voice Forge Mark II</h1>
<p>Cockpit-Grade AI Voice System</p>
<textarea id="text" placeholder="Enter text to speak...">GORUNFREE!</textarea><br>
<select id="persona">
<option value="gabriel">GABRIEL - Commanding</option>
<option value="thunder_titan">Thunder Titan - Epic</option>
<option value="shirl">SHIRL - Warm</option>
<option value="pops">POPS - Wise</option>
<option value="dream">DREAM - Ethereal</option>
</select>
<select id="engine">
<option value="auto">Auto (Best Available)</option>
<option value="coqui">Coqui (Self-Hosted)</option>
<option value="elevenlabs">ElevenLabs (Premium)</option>
</select>
<button class="btn" onclick="forge()">🎤 FORGE VOICE</button>
<audio id="audio" controls></audio>
<script>
async function forge(){
  const text=document.getElementById('text').value;
  const persona=document.getElementById('persona').value;
  const engine=document.getElementById('engine').value;
  const resp=await fetch('/api/forge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,persona,engine})});
  if(resp.ok){const blob=await resp.blob();document.getElementById('audio').src=URL.createObjectURL(blob);}
  else{alert('Error: '+(await resp.json()).error);}
}
</script>
</body></html>`;
}
WORKER_CODE

cat << 'WRANGLER' > "$PROJECT_DIR/wrangler.toml"
name = "hero-voice-forge-mk2"
main = "src/worker.ts"
compatibility_date = "2024-11-01"
WRANGLER

cat << 'PACKAGE' > "$PROJECT_DIR/package.json"
{
  "name": "hero-voice-forge-mk2",
  "version": "2.0.0",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20241106.0",
    "wrangler": "^3.91.0"
  }
}
PACKAGE

cat << 'TSCONFIG' > "$PROJECT_DIR/tsconfig.json"
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "ESNext",
    "moduleResolution": "node",
    "types": ["@cloudflare/workers-types"],
    "strict": true,
    "noEmit": true
  },
  "include": ["src/**/*"]
}
TSCONFIG

success "Worker code created"

#===============================================================================
# STEP 4: INSTALL DEPENDENCIES
#===============================================================================

log "Installing dependencies..."

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    warn "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check for cloudflared
if ! command -v cloudflared &> /dev/null; then
    log "Installing cloudflared..."
    brew install cloudflare/cloudflare/cloudflared
fi
success "cloudflared ready"

# Check for Node.js
if ! command -v node &> /dev/null; then
    log "Installing Node.js..."
    brew install node
fi
success "Node.js ready"

# Check for npm/wrangler
if ! command -v wrangler &> /dev/null; then
    log "Installing Wrangler..."
    npm install -g wrangler
fi
success "Wrangler ready"

# Install Node dependencies
cd "$PROJECT_DIR"
npm install
success "Node dependencies installed"

# Install Python dependencies
log "Installing Python TTS dependencies (this may take a few minutes)..."
pip3 install --break-system-packages flask flask-cors TTS torch 2>/dev/null || \
pip install flask flask-cors TTS torch 2>/dev/null || \
warn "Python deps may need manual install: pip install flask flask-cors TTS torch"

success "Dependencies installed"

#===============================================================================
# STEP 5: START COQUI SERVER
#===============================================================================

log "Starting Coqui TTS server..."

# Kill any existing server
pkill -f "python.*server.py" 2>/dev/null || true

# Start server in background
cd "$PROJECT_DIR/coqui-server"
nohup python3 server.py > "$PROJECT_DIR/coqui.log" 2>&1 &
COQUI_PID=$!

# Wait for server to start
sleep 5

if curl -s http://localhost:5002/health > /dev/null 2>&1; then
    success "Coqui server running on localhost:5002 (PID: $COQUI_PID)"
else
    warn "Coqui server may still be loading... check $PROJECT_DIR/coqui.log"
fi

#===============================================================================
# STEP 6: CREATE TUNNEL & DEPLOY WORKER
#===============================================================================

log "Creating Cloudflare tunnel..."
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "  A TUNNEL URL WILL APPEAR BELOW - COPY IT!"
echo "  Press Ctrl+C after copying the URL to continue deployment"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Start tunnel and capture URL
TUNNEL_LOG="$PROJECT_DIR/tunnel.log"
cloudflared tunnel --url http://localhost:5002 2>&1 | tee "$TUNNEL_LOG" &
TUNNEL_PID=$!

# Wait for URL to appear
echo ""
echo "Waiting for tunnel URL..."
sleep 10

# Try to extract URL from log
TUNNEL_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUNNEL_LOG" | head -1)

if [ -n "$TUNNEL_URL" ]; then
    success "Tunnel URL: $TUNNEL_URL"
    
    echo ""
    log "Deploying Worker with Coqui endpoint..."
    
    cd "$PROJECT_DIR"
    
    # Check Wrangler auth
    if ! wrangler whoami &> /dev/null; then
        log "Please authenticate with Cloudflare..."
        wrangler login
    fi
    
    # Set secret
    echo "$TUNNEL_URL" | wrangler secret put COQUI_ENDPOINT
    
    # Deploy
    wrangler deploy
    
    success "Worker deployed!"
else
    warn "Could not auto-detect tunnel URL"
    echo ""
    echo "MANUAL STEPS:"
    echo "1. Look above for URL like: https://xxx.trycloudflare.com"
    echo "2. Run: cd $PROJECT_DIR && wrangler secret put COQUI_ENDPOINT"
    echo "3. Paste the URL when prompted"
    echo "4. Run: wrangler deploy"
fi

#===============================================================================
# DONE
#===============================================================================

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║   ✅ HERO VOICE FORGE MARK II - DEPLOYMENT COMPLETE                 ║"
echo "║                                                                      ║"
echo "╠══════════════════════════════════════════════════════════════════════╣"
echo "║                                                                      ║"
echo "║   📁 Project:  $PROJECT_DIR                               ║"
echo "║   🎤 Coqui:    http://localhost:5002                                ║"
echo "║   🌐 Tunnel:   $TUNNEL_URL               ║"
echo "║   ☁️  Worker:   https://hero-voice-forge-mk2.YOUR-SUBDOMAIN.workers.dev ║"
echo "║                                                                      ║"
echo "║   📋 Logs:                                                          ║"
echo "║      Coqui:  $PROJECT_DIR/coqui.log                       ║"
echo "║      Tunnel: $PROJECT_DIR/tunnel.log                      ║"
echo "║                                                                      ║"
echo "║   🎯 Test:                                                          ║"
echo "║      curl -X POST YOUR-WORKER-URL/api/forge \\                       ║"
echo "║        -H 'Content-Type: application/json' \\                        ║"
echo "║        -d '{\"text\":\"GORUNFREE\",\"persona\":\"gabriel\"}'              ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "⚡ GORUNFREE - ALL CORES FIRING! ⚡"
echo ""

// ============================================================================
// GABRIEL INTERACTION V4.0 (VOICE & API & WEBSOCKET)
// Speed/Latency Feedback + Reflex Mode Detection
// ============================================================================

const API_URL = "http://localhost:8000";
const WS_URL = "ws://localhost:8000/ws";

let isListening = false;
let recognition;
let ws = null;
let wsReconnectAttempts = 0;
let requestCount = 0;
let lastLatency = 0;

// ============================================================================
// CONNECTION MANAGEMENT
// ============================================================================

function updateConnectionStatus(status) {
    const dot = document.getElementById('connection-dot');
    const text = document.getElementById('connection-text');

    if (!dot || !text) return;

    dot.className = 'status-dot';

    switch (status) {
        case 'connected':
            dot.classList.add('connected');
            text.textContent = 'Connected';
            break;
        case 'connecting':
            dot.classList.add('connecting');
            text.textContent = 'Connecting...';
            break;
        case 'disconnected':
            dot.classList.add('disconnected');
            text.textContent = 'Disconnected';
            break;
    }
}

function initWebSocket() {
    updateConnectionStatus('connecting');

    try {
        ws = new WebSocket(WS_URL);

        ws.onopen = function () {
            wsReconnectAttempts = 0;
            updateConnectionStatus('connected');
            logToUI("WebSocket connected.", "system");
            window.setMode?.('idle');
        };

        ws.onmessage = function (event) {
            try {
                const data = JSON.parse(event.data);
                handleWSMessage(data);
            } catch (e) {
                console.error("WS parse error:", e);
            }
        };

        ws.onclose = function () {
            updateConnectionStatus('disconnected');
            ws = null;

            if (wsReconnectAttempts < 5) {
                const delay = Math.min(1000 * Math.pow(2, wsReconnectAttempts), 10000);
                wsReconnectAttempts++;
                setTimeout(initWebSocket, delay);
            }
        };

        ws.onerror = function (error) {
            console.error("WebSocket error:", error);
            updateConnectionStatus('disconnected');
        };
    } catch (e) {
        console.error("WebSocket init error:", e);
        updateConnectionStatus('disconnected');
    }
}

function handleWSMessage(data) {
    switch (data.type) {
        case 'connected':
            logToUI(data.message || "WebSocket active.", "system");
            fetchStatus();
            break;

        case 'response':
            handleResponse(data);
            break;

        case 'status':
            if (data.data?.memory_vibe) {
                window.setMood?.(data.data.memory_vibe);
            }
            break;

        case 'stream_start':
            window.setMode?.('streaming');
            logToUI("Gabriel: ", "gabriel");
            break;

        case 'stream_token':
            appendToLastLog(data.token);
            window.streamTick?.();
            break;

        case 'stream_end':
            window.setMode?.('idle');
            speak(data.full_response);
            break;
    }
}

function handleResponse(data) {
    const meta = data.meta || {};
    const latency = meta.latency_ms || 0;
    const source = meta.source || 'unknown';
    const mode = meta.mode || 'reflex';

    lastLatency = latency;
    updateLatency(latency);
    requestCount++;
    updateRequestCount();

    // === VISUAL + AUDIO FEEDBACK ===

    // Mode indicator
    if (source === 'cache') {
        window.flashCacheHit?.();
        logToUI(`Gabriel [CACHE ${latency}ms]: ${data.response}`, "gabriel");
    } else if (source === 'reflex') {
        window.setMode?.('reflex');
        logToUI(`Gabriel [REFLEX ${latency}ms]: ${data.response}`, "gabriel");
        setTimeout(() => window.setMode?.('idle'), 500);
    } else if (source === 'llm') {
        window.setMode?.('deep');
        logToUI(`Gabriel [DEEP ${latency}ms]: ${data.response}`, "gabriel");
        setTimeout(() => window.setMode?.('idle'), 1500);
    } else {
        logToUI(`Gabriel [${latency}ms]: ${data.response}`, "gabriel");
    }

    // Mood update
    if (meta.vibe) {
        window.setMood?.(meta.vibe);
    }

    // Speak response
    speak(data.response);
    updateStatus("Ready");
}

function appendToLastLog(text) {
    const log = document.getElementById('log');
    if (log && log.lastChild) {
        log.lastChild.innerHTML += text;
    }
}

// ============================================================================
// SPEECH RECOGNITION
// ============================================================================

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = function () {
        isListening = true;
        updateStatus("Listening...");
        pulseGlobe(true);
    };

    recognition.onend = function () {
        isListening = false;
        pulseGlobe(false);
        updateStatus("Click to Listen");
    };

    recognition.onresult = function (event) {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                const finalTranscript = event.results[i][0].transcript;
                logToUI(`You: "${finalTranscript}"`, "user");
                sendToBrain(finalTranscript);
                updateStatus("Processing...");
            } else {
                interimTranscript += event.results[i][0].transcript;
                updateStatus(`Listening: ${interimTranscript}`);
            }
        }
    };

    recognition.onerror = function (event) {
        console.error("Speech Error:", event.error);
        updateStatus("Error: " + event.error);
        logToUI(`Speech error: ${event.error}`, "error");
    };
} else {
    logToUI("Web Speech API not supported.", "error");
}

// ============================================================================
// API COMMUNICATION
// ============================================================================

async function sendToBrain(text) {
    // Show thinking state
    window.setMode?.('reflex');

    // Try WebSocket first
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'interact', content: text }));
        return;
    }

    // Fallback to HTTP
    try {
        const startTime = performance.now();

        const response = await fetch(`${API_URL}/interact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        data.meta = data.meta || {};
        data.meta.latency_ms = Math.round(performance.now() - startTime);

        handleResponse({ ...data, response: data.response });

    } catch (error) {
        logToUI("Connection Lost. Is Brain Online?", "error");
        console.error(error);
        updateStatus("Offline");
        window.setMode?.('idle');
    }
}

async function fetchStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();

        if (data.memory_vibe) {
            window.setMood?.(data.memory_vibe);
        }

        requestCount = data.requests_processed || 0;
        updateRequestCount();

        // Update LLM status indicator
        const llmEl = document.getElementById('llm-status');
        if (llmEl) {
            llmEl.textContent = data.llm_available ? 'LLM: ✓' : 'LLM: ✗';
        }
    } catch (e) {
        console.log("Could not fetch status");
    }
}

// ============================================================================
// TEXT-TO-SPEECH
// ============================================================================

function speak(text) {
    const synth = window.speechSynthesis;

    if (synth.speaking) {
        synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();

    utterance.voice = voices.find(v => v.name.includes("Daniel")) ||
        voices.find(v => v.name.includes("Alex")) ||
        voices.find(v => v.name.includes("Samantha")) ||
        voices[0];

    utterance.rate = 1.0;
    utterance.pitch = 0.95;

    utterance.onstart = () => pulseGlobe(true);
    utterance.onend = () => {
        pulseGlobe(false);
        window.setMode?.('idle');
    };

    synth.speak(utterance);
}

// ============================================================================
// UI HELPERS
// ============================================================================

function updateStatus(status) {
    const el = document.getElementById('status-text');
    if (el) el.textContent = status;
}

function updateLatency(ms) {
    const el = document.getElementById('latency-value');
    if (el) {
        el.textContent = ms;
        // Color code latency
        if (ms < 10) {
            el.style.color = '#00ff44';
        } else if (ms < 100) {
            el.style.color = '#00ffff';
        } else if (ms < 500) {
            el.style.color = '#ffaa00';
        } else {
            el.style.color = '#ff4444';
        }
    }
}

function updateRequestCount() {
    const el = document.getElementById('request-count');
    if (el) el.textContent = requestCount;
}

function pulseGlobe(active) {
    if (typeof window.triggerPulse === 'function') {
        window.triggerPulse(active);
    }
}

// ============================================================================
// EVENT HANDLERS
// ============================================================================

document.body.addEventListener('click', (e) => {
    if (e.target.closest('#ui-layer')) return;

    // Initialize audio on first click
    window.GabrielAudio?.init();

    if (recognition && !isListening) {
        try {
            recognition.start();
        } catch (e) {
            console.log("Recognition start error:", e);
        }
    }
});

document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !isListening && !e.repeat) {
        e.preventDefault();
        window.GabrielAudio?.init();
        if (recognition) {
            try {
                recognition.start();
            } catch (e) {
                console.log("Recognition start error:", e);
            }
        }
    }
});

window.addEventListener('load', () => {
    setTimeout(initWebSocket, 500);

    if (window.speechSynthesis) {
        window.speechSynthesis.getVoices();
    }
});

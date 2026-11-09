// ============================================================================
// GABRIEL INTERACTION V3.0 (VOICE & API & WEBSOCKET)
// Zero Latency UI + WebSocket + Connection Management
// ============================================================================

const API_URL = "http://localhost:8000";
const WS_URL = "ws://localhost:8000/ws";

let isListening = false;
let recognition;
let ws = null;
let wsReconnectAttempts = 0;
let requestCount = 0;

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

            // Reconnect with backoff
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
            // Fetch initial status
            fetchStatus();
            break;

        case 'response':
            logToUI(`Gabriel: ${data.response}`, "gabriel");
            updateLatency(data.meta?.latency_ms);
            if (data.meta?.vibe) {
                window.setMood(data.meta.vibe);
            }
            speak(data.response);
            break;

        case 'status':
            if (data.data?.memory_vibe) {
                window.setMood(data.data.memory_vibe);
            }
            break;

        case 'activity':
            // Background activity from other clients
            break;

        case 'stream_start':
            logToUI("Gabriel: ", "gabriel");
            break;

        case 'stream_token':
            appendToLastLog(data.token);
            break;

        case 'stream_end':
            speak(data.full_response);
            break;
    }
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
    // Try WebSocket first
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'interact', content: text }));
        requestCount++;
        updateRequestCount();
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
        const latency = Math.round(performance.now() - startTime);

        requestCount++;
        updateRequestCount();
        updateLatency(latency);

        logToUI(`Gabriel: ${data.response}`, "gabriel");

        if (data.meta?.vibe) {
            window.setMood(data.meta.vibe);
        }

        speak(data.response);
        updateStatus("Ready");

    } catch (error) {
        logToUI("Connection Lost. Is Brain Online?", "error");
        console.error(error);
        updateStatus("Offline");
    }
}

async function fetchStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();

        if (data.memory_vibe) {
            window.setMood(data.memory_vibe);
        }

        requestCount = data.requests_processed || 0;
        updateRequestCount();
    } catch (e) {
        console.log("Could not fetch status");
    }
}

// ============================================================================
// TEXT-TO-SPEECH
// ============================================================================

function speak(text) {
    const synth = window.speechSynthesis;

    // Cancel any ongoing speech
    if (synth.speaking) {
        synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();

    // Voice selection priority
    utterance.voice = voices.find(v => v.name.includes("Daniel")) ||
        voices.find(v => v.name.includes("Alex")) ||
        voices.find(v => v.name.includes("Samantha")) ||
        voices[0];

    utterance.rate = 1.0;
    utterance.pitch = 0.95;

    utterance.onstart = () => pulseGlobe(true);
    utterance.onend = () => pulseGlobe(false);

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
    if (el) el.textContent = ms || '--';
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

// Click to listen
document.body.addEventListener('click', (e) => {
    // Ignore clicks on UI elements
    if (e.target.closest('#ui-layer')) return;

    if (recognition && !isListening) {
        try {
            recognition.start();
        } catch (e) {
            console.log("Recognition start error:", e);
        }
    }
});

// Keyboard shortcut (spacebar to talk)
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !isListening && !e.repeat) {
        e.preventDefault();
        if (recognition) {
            try {
                recognition.start();
            } catch (e) {
                console.log("Recognition start error:", e);
            }
        }
    }
});

// Initialize WebSocket on load
window.addEventListener('load', () => {
    // Delay to let server start
    setTimeout(initWebSocket, 500);

    // Load voices
    if (window.speechSynthesis) {
        window.speechSynthesis.getVoices();
    }
});

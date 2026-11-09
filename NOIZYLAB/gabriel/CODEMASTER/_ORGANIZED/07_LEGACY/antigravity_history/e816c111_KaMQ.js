
// ============================================================================
// GABRIEL INTERACTION (VOICE & API)
// Version: 2.0 (Zero Latency UI)
// ============================================================================

const API_URL = "http://localhost:8000";
let isListening = false;
let recognition;
let shouldAutoRestart = true; // Auto-heal voice engine

// Initialize Web Speech API
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false; // We want single commands for snappy response
    recognition.interimResults = true; // Zero latency feedback
    recognition.lang = 'en-US';

    recognition.onstart = function () {
        isListening = true;
        updateStatus("Listening...");
        pulseGlobe(true);
    };

    recognition.onend = function () {
        isListening = false;
        pulseGlobe(false);
        // Auto-restart if we want continuous "Always On" listening (optional toggling)
        if (shouldAutoRestart) {
            // updateStatus("Standby..."); 
            // recognition.start(); // Uncomment for "Always On" God Mode
        }
    };

    recognition.onresult = function (event) {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                const finalTranscript = event.results[i][0].transcript;
                logToUI(`Heard: "${finalTranscript}"`);
                sendToBrain(finalTranscript);
                updateStatus("Thinking...");
            } else {
                interimTranscript += event.results[i][0].transcript;
                updateStatus(`Listening: ${interimTranscript}`);
            }
        }
    };

    recognition.onerror = function (event) {
        console.error("Speech Error:", event.error);
        updateStatus("Error: " + event.error);
        if (event.error === 'network') {
            updateStatus("Network Error. Retrying...");
        }
    };
} else {
    logToUI("Web Speech API not supported.");
}

async function sendToBrain(text) {
    try {
        // Optimistic UI: Assume success
        const startTime = performance.now();

        const response = await fetch(`${API_URL}/interact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        const latency = Math.round(performance.now() - startTime);

        logToUI(`Gabriel (${latency}ms): ${data.response}`);
        speak(data.response);
        updateStatus("Ready");

    } catch (error) {
        logToUI("Connection Lost. Is Brain Online?");
        console.error(error);
        updateStatus("Offline");
    }
}

function speak(text) {
    // Zero latency audio cancel
    const synth = window.speechSynthesis;
    if (synth.speaking) {
        synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();
    // God Mode Voice Selection
    utterance.voice = voices.find(v => v.name.includes("Daniel")) ||
        voices.find(v => v.name.includes("Samantha")) ||
        voices[0];

    utterance.rate = 1.05; // Slightly faster for efficiency
    utterance.pitch = 0.95; // Deep/Authoritative
    synth.speak(utterance);
}

function updateStatus(status) {
    const el = document.getElementById('input-indicator');
    if (el) el.innerText = status;
}

function pulseGlobe(active) {
    if (typeof window.triggerPulse === 'function') {
        window.triggerPulse(active);
    }
}

// Click to listen
document.body.addEventListener('click', () => {
    // Resume audio context if needed
    if (recognition && !isListening) {
        try {
            recognition.start();
        } catch (e) {
            console.log("Recognition validation", e);
        }
    }
});

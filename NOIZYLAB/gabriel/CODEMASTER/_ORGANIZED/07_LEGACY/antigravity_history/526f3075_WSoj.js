
// ============================================================================
// GABRIEL INTERACTION (VOICE & API)
// ============================================================================

const API_URL = "http://localhost:8000";
let isListening = false;
let recognition;

// Initialize Web Speech API
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = function () {
        isListening = true;
        updateStatus("Listening...");
        pulseGlobe(true);
    };

    recognition.onend = function () {
        isListening = false;
        updateStatus("Processing...");
        pulseGlobe(false);
    };

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        logToUI(`Heard: "${transcript}"`);
        sendToBrain(transcript);
    };

    recognition.onerror = function (event) {
        console.error(event.error);
        updateStatus("Error: " + event.error);
    };
} else {
    logToUI("Web Speech API not supported.");
}

async function sendToBrain(text) {
    try {
        const response = await fetch(`${API_URL}/interact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        logToUI(`Gabriel: ${data.response}`);
        speak(data.response);

    } catch (error) {
        logToUI("Connection Lost. Is Brain Online?");
        console.error(error);
    }
    updateStatus("Click to Listen");
}

function speak(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    // Try to find a good voice
    const voices = synth.getVoices();
    // Prefer a deep/tech voice if available (OS dependent)
    utterance.voice = voices.find(v => v.name.includes("Daniel")) || voices[0];
    utterance.rate = 1.0;
    utterance.pitch = 0.9;
    synth.speak(utterance);
}

function updateStatus(status) {
    document.getElementById('input-indicator').innerText = status;
}

function pulseGlobe(active) {
    if (active && file_globe) {
        // Visual feedback hook for 3D engine
        // globe.material.color.setHex(0xff00ff);
    }
}

// Click to listen
document.body.addEventListener('click', () => {
    if (!isListening && recognition) {
        recognition.start();
    }
});

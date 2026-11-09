// ============================================================================
// GABRIEL 3D ENGINE V4.0 (THREE.JS)
// Enhanced Visual States + Speed/Latency Feedback
// ============================================================================

let scene, camera, renderer, globe, particles, innerCore, pulseRing;
let targetRotationX = 0;
let targetRotationY = 0;
let pulseState = 0;
let moodColor = new THREE.Color(0x00ffff);
let targetMoodColor = new THREE.Color(0x00ffff);

// State tracking
let currentMode = 'idle';
let streamingActive = false;
let compressionActive = false;

// Mood color mapping
const MOOD_COLORS = {
    neutral: 0x00ffff,
    aligned: 0x00ff88,
    connected: 0x88ff00,
    critical: 0xff4444,
    awakening: 0xffaa00,
    thinking: 0x8888ff,
    reflex: 0x00ffaa,
    deep: 0x6644ff,
};

// State colors
const STATE_COLORS = {
    cacheHit: 0x00ff44,
    cacheMiss: 0xffaa00,
    streaming: 0x00ddff,
    preload: 0xaaffaa,
};

function init3D() {
    const container = document.getElementById('canvas-container');

    // Scene Setup
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.002);

    // Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 22;

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Inner Core (Glowing center)
    const coreGeometry = new THREE.SphereGeometry(3, 32, 32);
    const coreMaterial = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0.15,
    });
    innerCore = new THREE.Mesh(coreGeometry, coreMaterial);
    scene.add(innerCore);

    // Main Globe - "Neural Network"
    const geometry = new THREE.IcosahedronGeometry(10, 3);
    const material = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        wireframe: true,
        transparent: true,
        opacity: 0.25,
        blending: THREE.AdditiveBlending
    });
    globe = new THREE.Mesh(geometry, material);
    scene.add(globe);

    // Pulse Ring (for reflex mode)
    const ringGeometry = new THREE.TorusGeometry(12, 0.15, 16, 100);
    const ringMaterial = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0,
    });
    pulseRing = new THREE.Mesh(ringGeometry, ringMaterial);
    pulseRing.rotation.x = Math.PI / 2;
    scene.add(pulseRing);

    // Outer ambient ring
    const outerRingGeometry = new THREE.TorusGeometry(14, 0.05, 16, 100);
    const outerRingMaterial = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0.3,
    });
    const outerRing = new THREE.Mesh(outerRingGeometry, outerRingMaterial);
    outerRing.rotation.x = Math.PI / 2;
    scene.add(outerRing);

    // Particles - "Neural Activity"
    const pGeometry = new THREE.BufferGeometry();
    const pCount = 4000;
    const posArray = new Float32Array(pCount * 3);

    for (let i = 0; i < pCount * 3; i += 3) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const r = 8 + Math.random() * 25;

        posArray[i] = r * Math.sin(phi) * Math.cos(theta);
        posArray[i + 1] = r * Math.sin(phi) * Math.sin(theta);
        posArray[i + 2] = r * Math.cos(phi);
    }

    pGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const pMaterial = new THREE.PointsMaterial({
        size: 0.12,
        color: 0xffffff,
        transparent: true,
        opacity: 0.5,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true,
    });

    particles = new THREE.Points(pGeometry, pMaterial);
    scene.add(particles);

    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0x00ffff, 1.5, 100);
    pointLight1.position.set(15, 15, 15);
    scene.add(pointLight1);

    // Events
    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('mousemove', onMouseMove, false);

    logToUI("Visual System Online (V4 + Latency Feedback).", "system");
    animate();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onMouseMove(event) {
    targetRotationX = (event.clientY - window.innerHeight / 2) * 0.0005;
    targetRotationY = (event.clientX - window.innerWidth / 2) * 0.0005;
}

function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // Base rotation
    globe.rotation.y += 0.003;
    globe.rotation.x += (targetRotationX - globe.rotation.x) * 0.02;
    globe.rotation.y += (targetRotationY - globe.rotation.y) * 0.02;

    innerCore.rotation.y -= 0.002;
    innerCore.rotation.x += 0.001;

    // === MODE-SPECIFIC ANIMATIONS ===

    if (currentMode === 'reflex') {
        // REFLEX: Tight pulse ring, fast response
        pulseState += 0.15;
        const ringScale = 1 + Math.sin(pulseState * 2) * 0.1;
        pulseRing.scale.set(ringScale, ringScale, 1);
        pulseRing.material.opacity = 0.6 + Math.sin(pulseState * 3) * 0.3;
        globe.scale.set(1, 1, 1);
        innerCore.material.opacity = 0.3;

    } else if (currentMode === 'deep') {
        // DEEP: Slow glow expansion
        pulseState += 0.02;
        const scale = 1 + Math.sin(pulseState) * 0.15;
        globe.scale.set(scale, scale, scale);
        innerCore.scale.set(scale * 1.2, scale * 1.2, scale * 1.2);
        innerCore.material.opacity = 0.4 + Math.sin(pulseState) * 0.2;
        pulseRing.material.opacity *= 0.95;

    } else if (currentMode === 'streaming') {
        // STREAMING: Typing ripple effect
        pulseState += 0.2;
        const positions = particles.geometry.attributes.position.array;
        for (let i = 0; i < positions.length; i += 3) {
            positions[i + 1] += Math.sin(time * 5 + i * 0.01) * 0.02;
        }
        particles.geometry.attributes.position.needsUpdate = true;
        particles.material.opacity = 0.7 + Math.sin(pulseState * 5) * 0.2;

    } else if (currentMode === 'idle') {
        // IDLE: Breathing animation, low noise
        const breathe = Math.sin(time * 0.5) * 0.02 + 1;
        innerCore.scale.set(breathe, breathe, breathe);
        globe.scale.lerp(new THREE.Vector3(1, 1, 1), 0.02);
        pulseRing.material.opacity *= 0.98;
        particles.material.opacity += (0.4 - particles.material.opacity) * 0.02;
    }

    // Voice active overrides
    if (window.isPulsing) {
        pulseState += 0.1;
        const scale = 1 + Math.sin(pulseState) * 0.08;
        globe.scale.set(scale, scale, scale);
        const hue = (Math.sin(pulseState * 0.5) + 1) * 0.1 + 0.5;
        globe.material.color.setHSL(hue, 1.0, 0.5);
        innerCore.material.opacity = 0.3 + Math.sin(pulseState) * 0.15;
        particles.material.opacity = 0.7 + Math.sin(pulseState * 2) * 0.2;
    }

    // Compression effect
    if (compressionActive) {
        const squeeze = 0.95 + Math.sin(time * 10) * 0.02;
        globe.scale.x *= squeeze;
        globe.scale.z *= squeeze;
        particles.material.opacity *= 0.8;
    }

    // Color transitions
    moodColor.lerp(targetMoodColor, 0.03);
    globe.material.color.lerp(moodColor, 0.03);
    innerCore.material.color.lerp(moodColor, 0.03);
    pulseRing.material.color.lerp(moodColor, 0.05);

    // Particle drift
    particles.rotation.y -= 0.001;
    particles.rotation.x += 0.0003;

    renderer.render(scene, camera);
}

// === STATE TRIGGERS ===

window.triggerPulse = function (active) {
    window.isPulsing = active;
};

window.setMode = function (mode) {
    currentMode = mode;
    pulseState = 0;

    const moodEl = document.getElementById('mood-value');
    if (moodEl) {
        const label = {
            'reflex': '⚡ Reflex',
            'deep': '🧠 Deep Think',
            'streaming': '📡 Streaming',
            'idle': '💤 Idle'
        }[mode] || mode;
        moodEl.textContent = label;
    }

    // Trigger appropriate audio
    if (mode === 'reflex') {
        window.GabrielAudio?.playClick();
    } else if (mode === 'deep') {
        window.GabrielAudio?.playSubHum();
    }
};

window.setMood = function (mood) {
    const color = MOOD_COLORS[mood] || MOOD_COLORS.neutral;
    targetMoodColor.setHex(color);

    const moodEl = document.getElementById('mood-value');
    if (moodEl && currentMode === 'idle') {
        moodEl.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
    }
};

window.flashCacheHit = function () {
    // Green flash
    const originalColor = targetMoodColor.clone();
    targetMoodColor.setHex(STATE_COLORS.cacheHit);
    pulseRing.material.opacity = 1;
    pulseRing.material.color.setHex(STATE_COLORS.cacheHit);

    // Play chime
    window.GabrielAudio?.playChime();

    setTimeout(() => {
        targetMoodColor.copy(originalColor);
    }, 200);
};

window.flashCacheMiss = function () {
    // Amber fade
    const originalColor = targetMoodColor.clone();
    targetMoodColor.setHex(STATE_COLORS.cacheMiss);

    setTimeout(() => {
        targetMoodColor.copy(originalColor);
    }, 400);
};

window.flashPreload = function () {
    // Icon halo effect
    pulseRing.material.opacity = 0.5;
    pulseRing.material.color.setHex(STATE_COLORS.preload);
    pulseRing.scale.set(1.3, 1.3, 1);

    // Whoosh sound
    window.GabrielAudio?.playWhoosh();
};

window.setCompression = function (active) {
    compressionActive = active;
};

window.streamTick = function () {
    // Quick particle burst for each token
    particles.material.opacity = Math.min(1, particles.material.opacity + 0.1);
    window.GabrielAudio?.playTick();
};

// Utility to log to HTML UI
function logToUI(msg, type = 'system') {
    const log = document.getElementById('log');
    if (!log) return;

    const line = document.createElement('div');
    line.className = `log-line ${type}`;

    const timestamp = new Date().toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    line.innerHTML = `<span style="opacity: 0.5">[${timestamp}]</span> ${msg}`;
    log.appendChild(line);

    while (log.children.length > 8) {
        log.removeChild(log.firstChild);
    }

    log.scrollTop = log.scrollHeight;
}

window.logToUI = logToUI;

init3D();

// ============================================================================
// GABRIEL 3D ENGINE V4.1 - ADAPTIVE RENDERING (PHASE 7)
// Lower FPS when idle, full fidelity on interaction only
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

// === PHASE 7: Adaptive Rendering ===
let targetFPS = 60;
let currentFPS = 30;  // Start lower
let lastInteraction = Date.now();
const IDLE_TIMEOUT = 3000;  // 3s to idle mode
const IDLE_FPS = 15;
const ACTIVE_FPS = 60;
let animationId = null;
let lastFrameTime = 0;
let frameInterval = 1000 / currentFPS;

// Performance tracking
let frameCount = 0;
let lastFPSUpdate = Date.now();
let actualFPS = 0;

// Mood/state colors
const MOOD_COLORS = {
    neutral: 0x00ffff, aligned: 0x00ff88, connected: 0x88ff00,
    critical: 0xff4444, awakening: 0xffaa00, thinking: 0x8888ff,
    reflex: 0x00ffaa, deep: 0x6644ff,
};

const STATE_COLORS = {
    cacheHit: 0x00ff44, cacheMiss: 0xffaa00, streaming: 0x00ddff, preload: 0xaaffaa,
};

function init3D() {
    const container = document.getElementById('canvas-container');

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.002);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 22;

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Inner Core
    const coreGeometry = new THREE.SphereGeometry(3, 32, 32);
    const coreMaterial = new THREE.MeshBasicMaterial({ color: 0x00ffff, transparent: true, opacity: 0.15 });
    innerCore = new THREE.Mesh(coreGeometry, coreMaterial);
    scene.add(innerCore);

    // Main Globe
    const geometry = new THREE.IcosahedronGeometry(10, 3);
    const material = new THREE.MeshBasicMaterial({
        color: 0x00ffff, wireframe: true, transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending
    });
    globe = new THREE.Mesh(geometry, material);
    scene.add(globe);

    // Pulse Ring
    const ringGeometry = new THREE.TorusGeometry(12, 0.15, 16, 100);
    const ringMaterial = new THREE.MeshBasicMaterial({ color: 0x00ffff, transparent: true, opacity: 0 });
    pulseRing = new THREE.Mesh(ringGeometry, ringMaterial);
    pulseRing.rotation.x = Math.PI / 2;
    scene.add(pulseRing);

    // Outer Ring
    const outerRing = new THREE.Mesh(
        new THREE.TorusGeometry(14, 0.05, 16, 100),
        new THREE.MeshBasicMaterial({ color: 0x00ffff, transparent: true, opacity: 0.3 })
    );
    outerRing.rotation.x = Math.PI / 2;
    scene.add(outerRing);

    // Particles (reduced count for performance)
    const pGeometry = new THREE.BufferGeometry();
    const pCount = 2000;  // Reduced from 4000
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
        size: 0.12, color: 0xffffff, transparent: true, opacity: 0.5,
        blending: THREE.AdditiveBlending, sizeAttenuation: true
    });
    particles = new THREE.Points(pGeometry, pMaterial);
    scene.add(particles);

    // Lights
    scene.add(new THREE.AmbientLight(0x404040, 0.5));
    const pl = new THREE.PointLight(0x00ffff, 1.5, 100);
    pl.position.set(15, 15, 15);
    scene.add(pl);

    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('mousemove', onMouseMove, false);

    logToUI("Visual System Online (Adaptive V4.1).", "system");
    requestAnimationFrame(adaptiveAnimate);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onMouseMove(event) {
    markInteraction();
    targetRotationX = (event.clientY - window.innerHeight / 2) * 0.0005;
    targetRotationY = (event.clientX - window.innerWidth / 2) * 0.0005;
}

function markInteraction() {
    lastInteraction = Date.now();
    if (currentFPS < ACTIVE_FPS) {
        setTargetFPS(ACTIVE_FPS);
    }
}

function setTargetFPS(fps) {
    targetFPS = fps;
    frameInterval = 1000 / fps;
}

// === ADAPTIVE FRAME RATE ===
function adaptiveAnimate(timestamp) {
    animationId = requestAnimationFrame(adaptiveAnimate);

    // Check idle timeout
    const timeSinceInteraction = Date.now() - lastInteraction;
    if (timeSinceInteraction > IDLE_TIMEOUT && currentMode === 'idle') {
        if (targetFPS !== IDLE_FPS) {
            setTargetFPS(IDLE_FPS);
        }
    }

    // Smooth FPS transition
    currentFPS += (targetFPS - currentFPS) * 0.1;
    frameInterval = 1000 / currentFPS;

    // Frame limiting
    const elapsed = timestamp - lastFrameTime;
    if (elapsed < frameInterval) return;
    lastFrameTime = timestamp - (elapsed % frameInterval);

    // FPS counter
    frameCount++;
    if (Date.now() - lastFPSUpdate >= 1000) {
        actualFPS = frameCount;
        frameCount = 0;
        lastFPSUpdate = Date.now();
        updateFPSDisplay();
    }

    // === RENDER ===
    const time = Date.now() * 0.001;

    // Base rotation (slower when idle)
    const rotSpeed = currentMode === 'idle' ? 0.001 : 0.003;
    globe.rotation.y += rotSpeed;
    globe.rotation.x += (targetRotationX - globe.rotation.x) * 0.02;
    globe.rotation.y += (targetRotationY - globe.rotation.y) * 0.02;
    innerCore.rotation.y -= 0.002;

    // Mode-specific (skip heavy effects when idle with low FPS)
    if (currentFPS > 20 || currentMode !== 'idle') {
        animateModeEffects(time);
    }

    // Color transitions
    moodColor.lerp(targetMoodColor, 0.03);
    globe.material.color.lerp(moodColor, 0.03);
    innerCore.material.color.lerp(moodColor, 0.03);

    // Particle drift (skip in low FPS)
    if (currentFPS > 20) {
        particles.rotation.y -= 0.001;
    }

    renderer.render(scene, camera);
}

function animateModeEffects(time) {
    if (currentMode === 'reflex') {
        pulseState += 0.15;
        const ringScale = 1 + Math.sin(pulseState * 2) * 0.1;
        pulseRing.scale.set(ringScale, ringScale, 1);
        pulseRing.material.opacity = 0.6 + Math.sin(pulseState * 3) * 0.3;
    } else if (currentMode === 'deep') {
        pulseState += 0.02;
        const scale = 1 + Math.sin(pulseState) * 0.15;
        globe.scale.set(scale, scale, scale);
        innerCore.material.opacity = 0.4 + Math.sin(pulseState) * 0.2;
        pulseRing.material.opacity *= 0.95;
    } else if (currentMode === 'streaming') {
        pulseState += 0.2;
        particles.material.opacity = 0.7 + Math.sin(pulseState * 5) * 0.2;
    } else {
        // Idle breathing
        const breathe = Math.sin(time * 0.5) * 0.02 + 1;
        innerCore.scale.set(breathe, breathe, breathe);
        globe.scale.lerp(new THREE.Vector3(1, 1, 1), 0.02);
        pulseRing.material.opacity *= 0.98;
    }

    if (window.isPulsing) {
        pulseState += 0.1;
        const scale = 1 + Math.sin(pulseState) * 0.08;
        globe.scale.set(scale, scale, scale);
    }

    if (compressionActive) {
        const squeeze = 0.95 + Math.sin(time * 10) * 0.02;
        globe.scale.x *= squeeze;
    }
}

function updateFPSDisplay() {
    const el = document.getElementById('fps-value');
    if (el) el.textContent = Math.round(actualFPS);
}

// === STATE TRIGGERS ===
window.triggerPulse = function (active) { window.isPulsing = active; markInteraction(); };

window.setMode = function (mode) {
    currentMode = mode;
    pulseState = 0;
    markInteraction();

    // Boost FPS during deep/streaming
    if (mode === 'deep' || mode === 'streaming') {
        setTargetFPS(ACTIVE_FPS);
    }

    const moodEl = document.getElementById('mood-value');
    if (moodEl) {
        moodEl.textContent = { 'reflex': '⚡ Reflex', 'deep': '🧠 Deep', 'streaming': '📡 Stream', 'idle': '💤 Idle' }[mode] || mode;
    }

    // Audio (skip in deep compute - Phase 7)
    if (mode === 'reflex') window.GabrielAudio?.playClick();
    // No sound for deep mode - saves CPU
};

window.setMood = function (mood) {
    targetMoodColor.setHex(MOOD_COLORS[mood] || MOOD_COLORS.neutral);
};

window.flashCacheHit = function () {
    markInteraction();
    targetMoodColor.setHex(STATE_COLORS.cacheHit);
    pulseRing.material.opacity = 1;
    window.GabrielAudio?.playChime();
    setTimeout(() => targetMoodColor.setHex(MOOD_COLORS.neutral), 200);
};

window.flashCacheMiss = function () {
    targetMoodColor.setHex(STATE_COLORS.cacheMiss);
    setTimeout(() => targetMoodColor.setHex(MOOD_COLORS.neutral), 400);
};

window.setCompression = function (active) { compressionActive = active; };
window.streamTick = function () { particles.material.opacity = Math.min(1, particles.material.opacity + 0.1); };

function logToUI(msg, type = 'system') {
    const log = document.getElementById('log');
    if (!log) return;
    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    const ts = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    line.innerHTML = `<span style="opacity: 0.5">[${ts}]</span> ${msg}`;
    log.appendChild(line);
    while (log.children.length > 8) log.removeChild(log.firstChild);
    log.scrollTop = log.scrollHeight;
}

window.logToUI = logToUI;
init3D();

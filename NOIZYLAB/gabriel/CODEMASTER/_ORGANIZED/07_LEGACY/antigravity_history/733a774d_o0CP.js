// ============================================================================
// GABRIEL 3D ENGINE V3.0 (THREE.JS)
// Enhanced Neural Visualization + Mood States + Audio Reactivity
// ============================================================================

let scene, camera, renderer, globe, particles, innerCore;
let targetRotationX = 0;
let targetRotationY = 0;
let pulseState = 0;
let moodColor = new THREE.Color(0x00ffff);
let targetMoodColor = new THREE.Color(0x00ffff);

// Mood color mapping
const MOOD_COLORS = {
    neutral: 0x00ffff,
    aligned: 0x00ff88,
    connected: 0x88ff00,
    critical: 0xff4444,
    awakening: 0xffaa00,
    thinking: 0x8888ff,
};

function init3D() {
    const container = document.getElementById('canvas-container');

    // Scene Setup
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.002);

    // Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 22;

    // Renderer (Optimized for Retina)
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

    // Outer Ring
    const ringGeometry = new THREE.TorusGeometry(14, 0.05, 16, 100);
    const ringMaterial = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0.3,
    });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.rotation.x = Math.PI / 2;
    scene.add(ring);

    // Expose for Interaction.js
    window.gabrielGlobe = globe;
    window.gabrielCore = innerCore;

    // Particles - "Neural Activity" (increased density)
    const pGeometry = new THREE.BufferGeometry();
    const pCount = 4000;
    const posArray = new Float32Array(pCount * 3);
    const sizeArray = new Float32Array(pCount);

    for (let i = 0; i < pCount * 3; i += 3) {
        // Distribute in sphere
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const r = 8 + Math.random() * 25;

        posArray[i] = r * Math.sin(phi) * Math.cos(theta);
        posArray[i + 1] = r * Math.sin(phi) * Math.sin(theta);
        posArray[i + 2] = r * Math.cos(phi);

        sizeArray[i / 3] = Math.random() * 0.15 + 0.05;
    }

    pGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    pGeometry.setAttribute('size', new THREE.BufferAttribute(sizeArray, 1));

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

    // Ambient Light
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    scene.add(ambientLight);

    // Point Lights
    const pointLight1 = new THREE.PointLight(0x00ffff, 1.5, 100);
    pointLight1.position.set(15, 15, 15);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xff00ff, 0.5, 100);
    pointLight2.position.set(-15, -10, 10);
    scene.add(pointLight2);

    // Events
    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('mousemove', onMouseMove, false);

    logToUI("Visual System Online (God Mode V4).", "system");
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

    // Rotate Globe
    globe.rotation.y += 0.003;
    globe.rotation.x += (targetRotationX - globe.rotation.x) * 0.02;
    globe.rotation.y += (targetRotationY - globe.rotation.y) * 0.02;

    // Inner core slow rotation
    innerCore.rotation.y -= 0.002;
    innerCore.rotation.x += 0.001;

    // Breathing animation
    const breathe = Math.sin(time * 0.5) * 0.02 + 1;
    innerCore.scale.set(breathe, breathe, breathe);

    // Pulse Animation (Voice active)
    if (window.isPulsing) {
        pulseState += 0.1;
        const scale = 1 + Math.sin(pulseState) * 0.08;
        globe.scale.set(scale, scale, scale);

        // Dynamic color shift during speech
        const hue = (Math.sin(pulseState * 0.5) + 1) * 0.1 + 0.5;
        globe.material.color.setHSL(hue, 1.0, 0.5);
        innerCore.material.opacity = 0.3 + Math.sin(pulseState) * 0.15;

        // Particle excitement
        particles.material.opacity = 0.7 + Math.sin(pulseState * 2) * 0.2;
    } else {
        // Smooth return to normal
        globe.scale.lerp(new THREE.Vector3(1, 1, 1), 0.05);
        globe.material.color.lerp(moodColor, 0.05);
        innerCore.material.color.lerp(moodColor, 0.05);
        innerCore.material.opacity += (0.15 - innerCore.material.opacity) * 0.05;
        particles.material.opacity += (0.5 - particles.material.opacity) * 0.05;
    }

    // Mood color transition
    moodColor.lerp(targetMoodColor, 0.02);

    // Particle drift
    particles.rotation.y -= 0.001;
    particles.rotation.x += 0.0003;

    renderer.render(scene, camera);
}

// Global Pulse Trigger
window.triggerPulse = function (active) {
    window.isPulsing = active;
};

// Set Mood Color
window.setMood = function (mood) {
    const color = MOOD_COLORS[mood] || MOOD_COLORS.neutral;
    targetMoodColor.setHex(color);

    // Update UI
    const moodEl = document.getElementById('mood-value');
    if (moodEl) {
        moodEl.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
    }
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

    // Keep last 8 lines
    while (log.children.length > 8) {
        log.removeChild(log.firstChild);
    }

    // Scroll to bottom
    log.scrollTop = log.scrollHeight;
}

// Export for interaction.js
window.logToUI = logToUI;

// Initialize
init3D();

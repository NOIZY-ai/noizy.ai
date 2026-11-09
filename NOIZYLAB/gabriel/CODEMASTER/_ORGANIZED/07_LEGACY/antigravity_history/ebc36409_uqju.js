
// ============================================================================
// GABRIEL 3D ENGINE (THREE.JS)
// Version: 2.0 (Connected / Optimized)
// ============================================================================

let scene, camera, renderer, globe, particles;
let targetRotationX = 0;
let targetRotationY = 0;
let pulseState = 0;

function init3D() {
    const container = document.getElementById('canvas-container');

    // Scene Setup
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.002);

    // Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 20;

    // Renderer (Optimized for Retina Performance)
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap at 2x to prevent lag
    container.appendChild(renderer.domElement);

    // Geometry - The "Brain" Globe
    const geometry = new THREE.IcosahedronGeometry(10, 2);
    const material = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        wireframe: true,
        transparent: true,
        opacity: 0.3,
        blending: THREE.AdditiveBlending
    });
    globe = new THREE.Mesh(geometry, material);
    scene.add(globe);

    // Expose for Interaction.js
    window.file_globe = globe;

    // Particles - "Neural Activity"
    const pGeometry = new THREE.BufferGeometry();
    const pCount = 3000; // Increased density
    const posArray = new Float32Array(pCount * 3);

    for (let i = 0; i < pCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 45;
    }

    pGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const pMaterial = new THREE.PointsMaterial({
        size: 0.12,
        color: 0xffffff,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });

    particles = new THREE.Points(pGeometry, pMaterial);
    scene.add(particles);

    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00ffff, 1.5, 100);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);

    // Events
    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('mousemove', onMouseMove, false);

    logToUI("Visual System Online (God Mode).");
    animate();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onMouseMove(event) {
    targetRotationX = (event.clientY - window.innerHeight / 2) * 0.001;
    targetRotationY = (event.clientX - window.innerWidth / 2) * 0.001;
}

function animate() {
    requestAnimationFrame(animate);

    // Rotate Globe
    globe.rotation.y += 0.005;
    globe.rotation.x += (targetRotationX - globe.rotation.x) * 0.05;
    globe.rotation.y += (targetRotationY - globe.rotation.y) * 0.05;

    // Pulse Animation (Triggered by Voice)
    if (window.isPulsing) {
        pulseState += 0.1;
        const scale = 1 + Math.sin(pulseState) * 0.05;
        globe.scale.set(scale, scale, scale);
        globe.material.color.setHSL((Math.sin(pulseState) + 1) * 0.5, 1.0, 0.5);
    } else {
        // Return to normal
        globe.scale.lerp(new THREE.Vector3(1, 1, 1), 0.1);
        globe.material.color.lerp(new THREE.Color(0x00ffff), 0.1);
    }

    // Particle Drift
    particles.rotation.y -= 0.0015;
    particles.rotation.x += 0.0005;

    renderer.render(scene, camera);
}

// Global Pulse Trigger
window.triggerPulse = function (active) {
    window.isPulsing = active;
};

// Utility to log to HTML UI
function logToUI(msg) {
    const log = document.getElementById('log');
    if (!log) return;
    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerText = `> ${msg}`;
    log.appendChild(line);
    // Keep last 5 lines
    while (log.children.length > 5) {
        log.removeChild(log.firstChild);
    }
}

init3D();

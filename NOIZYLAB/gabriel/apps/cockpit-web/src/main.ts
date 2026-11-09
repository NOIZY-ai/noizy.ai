import { gabriel } from './state';
import { TempleEngine } from '../../temple_engine';
import { makeAnalyser, bassEnergy } from './audio';
import * as THREE from 'three';

// 1. INIT SYSTEMS
const temple = new TempleEngine();
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

// 2. SETUP CANVAS
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('canvas-container')?.appendChild(renderer.domElement);
camera.position.z = 5;

// 3. THE "MISSING PIECE" HOLDER (Placeholder for the drop)
const geometry = new THREE.SphereGeometry(1, 32, 32);
const material = new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true });
const avatarCore = new THREE.Mesh(geometry, material);
scene.add(avatarCore);

// 4. ANIMATION LOOP (The Heartbeat)
function animate() {
    requestAnimationFrame(animate);

    // Reactive Logic
    const level = gabriel.audioLevel || 0.01;
    const scale = 1 + level * 0.5;
    avatarCore.scale.set(scale, scale, scale);
    avatarCore.rotation.x += 0.01;
    avatarCore.rotation.y += 0.01;

    renderer.render(scene, camera);
}

// 5. START
animate();
console.log("[GABRIEL] Cockpit Online. Format: THREE.js");

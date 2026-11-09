// editor.js
// The "AI Design Lab" - Visualizing Code for Manipulation
// UPGRADE: 0% Latency Game Loop & Master Critic Integration

const canvas = document.getElementById('designCanvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true, alpha: false }); // Optimize for speed
const codeDisplay = document.getElementById('codeDisplay');
const fpsCounter = document.getElementById('fpsCounter');

// State
let objects = []; 
let selectedObject = null;
let isDragging = false;
let dragStartX, dragStartY;
let isDirty = true; // Optimization: Only redraw when something changes

// Performance Monitoring
let lastTime = 0;
let frameCount = 0;
let fpsTimer = 0;

// Configuration
const canvasWidth = 800;
const canvasHeight = 600;

// --- Object Classes ---

class DesignObject {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.width = 100;
        this.height = 100;
        this.rotation = 0;
        this.color = `hsl(${Math.random() * 360}, 70%, 50%)`;
        
        // PHYSICS (Living Art)
        this.vx = (Math.random() - 0.5) * 0.2; // Slow drift
        this.vy = (Math.random() - 0.5) * 0.2;
        this.vr = (Math.random() - 0.5) * 0.005; // Slow spin

        // IMAGE HANDLING
        if (this.type === 'image') {
            this.img = new Image();
            this.imgLoaded = false;
        }
    }

    // Set source for image objects
    setSrc(url) {
        if (this.type === 'image' && this.img) {
            this.img.src = url;
            this.img.onload = () => { this.imgLoaded = true; isDirty = true; };
        }
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.rotation += this.vr;

        // Bounce mechanics
        if (this.x < 0 || this.x > 800) this.vx *= -1;
        if (this.y < 0 || this.y > 600) this.vy *= -1;
    }

    draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        if (this.type === 'rect') {
            ctx.fillStyle = this.color;
            ctx.fillRect(-this.width/2, -this.height/2, this.width, this.height);
        } else if (this.type === 'circle') {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(0, 0, this.width/2, 0, Math.PI * 2);
            ctx.fill();
        } else if (this.type === 'image' && this.imgLoaded) {
            try {
                ctx.drawImage(this.img, -this.width/2, -this.height/2, this.width, this.height);
            } catch(e) { } // Prevent crash
        }
        
        if (this === selectedObject) {
            ctx.strokeStyle = '#00ff41';
            ctx.lineWidth = 2;
            ctx.strokeRect(-this.width/2 - 5, -this.height/2 - 5, this.width + 10, this.height + 10);
        }
        
        ctx.restore();
    }
    
    hitTest(mx, my) {
        return (mx > this.x - this.width/2 && 
                mx < this.x + this.width/2 && 
                my > this.y - this.height/2 && 
                my < this.y + this.height/2);
    }
}

// --- Main Render Loop (0% Latency) ---

// --- Main Render Loop (0% Latency + Motion) ---

function gameLoop(timestamp) {
    // 1. Calculate FPS
    const deltaTime = timestamp - lastTime;
    lastTime = timestamp;
    
    // 2. PHYSICS UPDATE (Motion)
    objects.forEach(obj => obj.update());
    isDirty = true; // Always redraw for motion

    // 3. Render
    if (isDirty) {
        renderFrame();
        isDirty = false;
    }
    
    // 4. Overlay & Architect Eye
    if (typeof drawArchitectOverlay === 'function') {
        drawArchitectOverlay(ctx, canvasWidth, canvasHeight);
    }
    
    // 5. Audio Spectrum (HUD)
    if (window.AudioSys) {
        window.AudioSys.drawVisualizer(ctx, canvasWidth, canvasHeight);
        
        // HARDWARE STATUS HUD
        if (window.AudioSys.getHardwareName) {
            ctx.fillStyle = 'rgba(0, 255, 204, 0.8)';
            ctx.font = '12px monospace';
            ctx.textAlign = 'right';
            ctx.fillText(`AUDIO INPUT: ${window.AudioSys.getHardwareName()}`, canvasWidth - 10, canvasHeight - 10);
            ctx.textAlign = 'left'; // Reset
        }
    }

    requestAnimationFrame(gameLoop);
}

// SYNESTHESIA MODULE
window.addEventListener('noizy-beat', (e) => {
    const type = e.detail.type;
    const canvas = document.getElementById('designCanvas');
    if (!canvas) return;
    
    // KICK: Scale Pulse
    if (type === 'kick') {
        canvas.style.transform = 'scale(1.02)';
        canvas.style.filter = 'brightness(1.1)';
        setTimeout(() => {
            canvas.style.transform = 'scale(1)';
            canvas.style.filter = 'brightness(1)';
        }, 50);
    }
    
    // SNARE: Chromatic Glitch (CSS Shift)
    if (type === 'snare') {
        canvas.style.transform = 'translateX(5px)';
        canvas.style.filter = 'hue-rotate(90deg)';
        setTimeout(() => {
            canvas.style.transform = 'translateX(0)';
            canvas.style.filter = 'hue-rotate(0deg)';
        }, 50);
    }
});

function renderFrame() {
    // 1. Clear Canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0,0, canvasWidth, canvasHeight);
    
    // 2. Draw all objects
    objects.forEach(obj => obj.draw(ctx));
    
    // 3. Apply Filter (If active)
    applyFilters();
}

// Start Loop
requestAnimationFrame(gameLoop);


// --- Event Listeners: Object Manipulation & 4D Tilt ---

// 4D TILT EFFECT
document.addEventListener('mousemove', (e) => {
    const rx = (e.clientX / window.innerWidth - 0.5) * 20; // -10 to 10 deg
    const ry = (e.clientY / window.innerHeight - 0.5) * 20;
    
    // Apply to container or canvas directly if it has perspective
    // Note: Canvas needs 'transform-style: preserve-3d' in CSS for best effect
    canvas.style.transform = `perspective(1000px) rotateY(${rx}deg) rotateX(${-ry}deg) scale(0.95)`;
});

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    
    selectedObject = null;
    for (let i = objects.length - 1; i >= 0; i--) {
        if (objects[i].hitTest(mx, my)) {
            selectedObject = objects[i];
            objects.splice(i, 1);
            objects.push(selectedObject);
            
            isDragging = true;
            dragStartX = mx - selectedObject.x;
            dragStartY = my - selectedObject.y;
            
            updateCodeDisplay('drag');
            isDirty = true; // Trigger redraw
            break;
        }
    }
    // If we missed objects, still redraw to clear selection
    if (!selectedObject) isDirty = true;
});

canvas.addEventListener('mousemove', (e) => {
    if (isDragging && selectedObject) {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        
        selectedObject.x = mx - dragStartX;
        selectedObject.y = my - dragStartY;
        
        isDirty = true; // Trigger redraw
    }
});

window.addEventListener('mouseup', () => {
    isDragging = false;
});

// --- Tools Buttons ---

document.getElementById('addRect').addEventListener('click', () => {
    window.AudioSys.playTone(300, 'square', 0.1); // SFX
    const obj = new DesignObject(canvasWidth/2, canvasHeight/2, 'rect');
    objects.push(obj);
    selectedObject = obj;
    updateCodeDisplay('create');
    isDirty = true;
});

document.getElementById('addCircle').addEventListener('click', () => {
    window.AudioSys.playTone(400, 'sine', 0.1); // SFX
    const obj = new DesignObject(canvasWidth/2, canvasHeight/2, 'circle');
    objects.push(obj);
    selectedObject = obj;
    updateCodeDisplay('create');
    isDirty = true;
});

document.getElementById('clearCanvas').addEventListener('click', () => {
    objects = [];
    selectedObject = null;
    isDirty = true;
});

// --- Art Director Integration (Doctorate) ---
const director = new ArtDirector();
const directorSelect = document.getElementById('directorEra');

document.getElementById('autoDirectBtn').addEventListener('click', () => {
    const era = directorSelect.value;
    const brief = director.generateBrief(era);
    
    objects = [];
    
    brief.objects.forEach(objDef => {
        const newObj = new DesignObject(objDef.x, objDef.y, objDef.type);
        newObj.width = objDef.width;
        newObj.height = objDef.height;
        newObj.color = objDef.color;
        newObj.rotation = objDef.rotation;
        
        if (objDef.type === 'triangle') newObj.type = 'rect'; // Fallback
        if (objDef.type === 'image' && objDef.src) {
             newObj.setSrc(objDef.src);
        }
        
        objects.push(newObj);
    });
    
    updateCodeDisplay('direct', brief);
    isDirty = true;
    
    const btn = document.getElementById('autoDirectBtn');
    const originalText = btn.innerText;
    btn.innerText = "Generated!";
    setTimeout(() => btn.innerText = originalText, 1000);
});

document.getElementById('critiqueBtn').addEventListener('click', () => {
    const era = directorSelect.value;
    const feedback = director.critique(objects, era, {hue:0}); // Passing objects to critic
    updateCodeDisplay('critique', feedback);
});

// --- Filter Logic ---

const hueRange = document.getElementById('hueRange');
const satRange = document.getElementById('satRange');
const brightRange = document.getElementById('brightRange');

[hueRange, satRange, brightRange].forEach(el => {
    el.addEventListener('input', () => {
        document.getElementById('hueVal').innerText = hueRange.value;
        document.getElementById('satVal').innerText = satRange.value;
        document.getElementById('brightVal').innerText = brightRange.value;
        
        isDirty = true; // Trigger redraw
        updateCodeDisplay('filter');
    });
});

function applyFilters() {
    const hue = parseInt(hueRange.value);
    const sat = parseInt(satRange.value);
    const bright = parseInt(brightRange.value);

    if (hue === 0 && sat === 100 && bright === 100) return;

    const imageData = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
    const data = imageData.data;
    
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i];
        let g = data[i+1];
        let b = data[i+2];

        // Optimized path could go here (e.g. Look Up Tables)
        let [h, s, l] = rgbToHsl(r, g, b);
        h = (h * 360) + hue; 
        s = s * (sat / 100); 
        l = l * (bright / 100); 
        const [newR, newG, newB] = hslToRgb(h / 360, s, l);
        
        data[i] = newR;
        data[i+1] = newG;
        data[i+2] = newB;
    }
    ctx.putImageData(imageData, 0, 0);
}

// --- Helper Functions ---
// RGB <-> HSL conversions (Standard)
function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    if (max === min) h = s = 0; 
    else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    return [h, s, l];
}

function hslToRgb(h, s, l) {
    let r, g, b;
    if (s === 0) r = g = b = l; 
    else {
        const hue2rgb = (p, q, t) => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1/6) return p + (q - p) * 6 * t;
            if (t < 1/2) return q;
            if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        };
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }
    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

// --- Dynamic Code Display ---

function updateCodeDisplay(action, data=null) {
    let snippet = '';
    if (action === 'drag') {
        snippet = `// 0% LATENCY ENGINE
// requestAnimationFrame Loop Active
selectedObject.x = mouseX - startX;
selectedObject.y = mouseY - startY;
isDirty = true; // Flag for next frame`;
    } else if (action === 'create') {
        snippet = `// OBJECT FACTORY
objects.push(new DesignObject(x, y));
isDirty = true;`;
    } else if (action === 'filter') {
        snippet = `// PIXEL PIPELINE
// Real-time manipulation buffer
h += ${hueRange.value}; 
s *= ${satRange.value/100};`;
    } else if (action === 'direct') {
        const era = document.getElementById('directorEra').value;
        const rules = Director.eras[era];
        snippet = `// ART DIRECTOR [DOCTORATE]
// Thesis: "${data.theory}"
// Engine: ${rules ? rules.layout : 'random'}
// Generating ${data.objects.length} elements...`;
    } else if (action === 'critique') {
        snippet = data; // Display the full critique text
    }
    
    codeDisplay.innerText = snippet.trim();
}

// Init
isDirty = true;
updateCodeDisplay('create');

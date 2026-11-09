// editor.js
// The "AI Design Lab" - Visualizing Code for Manipulation

const canvas = document.getElementById('designCanvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const codeDisplay = document.getElementById('codeDisplay');

// State
let objects = []; // Array to store shapes/images
let selectedObject = null;
let isDragging = false;
let dragStartX, dragStartY;

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
        this.isImage = false;
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
        }
        
        // Selection outline
        if (this === selectedObject) {
            ctx.strokeStyle = '#00ff41';
            ctx.lineWidth = 2;
            ctx.strokeRect(-this.width/2 - 5, -this.height/2 - 5, this.width + 10, this.height + 10);
        }
        
        ctx.restore();
    }
    
    hitTest(mx, my) {
        // Simple bounding box hit test (not accounting for rotation for simplicity)
        return (mx > this.x - this.width/2 && 
                mx < this.x + this.width/2 && 
                my > this.y - this.height/2 && 
                my < this.y + this.height/2);
    }
}

// --- Main Render Loop ---

function render() {
    // 1. Clear Canvas
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    // 2. Draw all objects
    objects.forEach(obj => obj.draw(ctx));
    
    // 3. Apply Filter (Color Manipulation)
    // We only apply this significantly if values are changed to save perf
    applyFilters();
}

// --- Event Listeners: Object Manipulation ---

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    
    // Check selection (reverse order to select top-most)
    selectedObject = null;
    for (let i = objects.length - 1; i >= 0; i--) {
        if (objects[i].hitTest(mx, my)) {
            selectedObject = objects[i];
            
            // Bring to front
            objects.splice(i, 1);
            objects.push(selectedObject);
            
            isDragging = true;
            dragStartX = mx - selectedObject.x;
            dragStartY = my - selectedObject.y;
            
            updateCodeDisplay('drag');
            break;
        }
    }
    render();
});

canvas.addEventListener('mousemove', (e) => {
    if (isDragging && selectedObject) {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        
        selectedObject.x = mx - dragStartX;
        selectedObject.y = my - dragStartY;
        
        render();
    }
});

window.addEventListener('mouseup', () => {
    isDragging = false;
});

// --- Tools Buttons ---

document.getElementById('addRect').addEventListener('click', () => {
    const obj = new DesignObject(canvasWidth/2, canvasHeight/2, 'rect');
    objects.push(obj);
    selectedObject = obj; // Auto-select new object
    updateCodeDisplay('create');
    render();
});

document.getElementById('addCircle').addEventListener('click', () => {
    const obj = new DesignObject(canvasWidth/2, canvasHeight/2, 'circle');
    objects.push(obj);
    selectedObject = obj;
    updateCodeDisplay('create');
    render();
});

document.getElementById('clearCanvas').addEventListener('click', () => {
    objects = [];
    selectedObject = null;
    render();
});

// --- Filter Logic (The "AI" Part) ---

const hueRange = document.getElementById('hueRange');
const satRange = document.getElementById('satRange');
const brightRange = document.getElementById('brightRange');

[hueRange, satRange, brightRange].forEach(el => {
    el.addEventListener('input', () => {
        // Update labels
        document.getElementById('hueVal').innerText = hueRange.value;
        document.getElementById('satVal').innerText = satRange.value;
        document.getElementById('brightVal').innerText = brightRange.value;
        
        render(); // Re-render logic calls applyFilters()
        updateCodeDisplay('filter');
    });
});

function applyFilters() {
    const hue = parseInt(hueRange.value);
    const sat = parseInt(satRange.value);
    const bright = parseInt(brightRange.value);

    // Optimization: Don't process pixels if default
    if (hue === 0 && sat === 100 && bright === 100) return;

    // Get Pixel Data
    const imageData = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
    const data = imageData.data;
    
    // Iterate through every pixel (R, G, B, A)
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i];
        let g = data[i+1];
        let b = data[i+2];

        // 1. Convert RGB to HSL
        let [h, s, l] = rgbToHsl(r, g, b);
        
        // 2. Manipulate
        h = (h * 360) + hue; // Shift Hue
        s = s * (sat / 100); // Scale Saturation
        l = l * (bright / 100); // Scale Lightness
        
        // 3. Convert back to RGB
        const [newR, newG, newB] = hslToRgb(h / 360, s, l);
        
        data[i] = newR;
        data[i+1] = newG;
        data[i+2] = newB;
    }
    
    // Put back modified pixels
    ctx.putImageData(imageData, 0, 0);
}

// --- Helper Functions ---

// RGB <-> HSL conversions (Standard algorithms)
function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
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
    if (s === 0) {
        r = g = b = l; // achromatic
    } else {
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

function updateCodeDisplay(action) {
    let snippet = '';
    if (action === 'drag') {
        snippet = `
// OBJECT MANIPULATION
// Canvas Event Listener: MouseMove
selectedObject.x = mouseX - dragStartX;
selectedObject.y = mouseY - dragStartY;

// Re-draw scene
render();`;
    } else if (action === 'create') {
        snippet = `
// GENERATION
const newShape = new DesignObject(x, y, 'rect');
objects.push(newShape);

// Assign random HSL color
this.color = \`hsl(\${Math.random() * 360}, 70%, 50%)\`;`;
    } else if (action === 'filter') {
        snippet = `
// PIXEL MANIPULATION (The "AI" Filter)
const imageData = ctx.getImageData(0, 0, width, height);
// Iterate EVERY pixel (R, G, B, Alpha)
for(let i=0; i<data.length; i+=4) {
    // RGB -> HSL conversion
    let [h, s, l] = rgbToHsl(data[i], data[i+1], pixel[i+2]);
    
    // Apply Shifts
    h += ${hueRange.value};       // Hue Shift
    s *= ${satRange.value/100};   // Saturation Scale
    
    // HSL -> RGB conversion back to canvas
}`;
    }
    
    codeDisplay.innerText = snippet.trim();
    // Simple syntax highlighting simulation via regex could go here
    // but text is sufficient for now.
}

// Initial render
render();
updateCodeDisplay('create');

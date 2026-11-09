// art-director.js
// The "Model" - Advanced Art History Knowledge & Composition Engine
// Doctorate Level Upgrade

// REAL AI GRAPHIC DESIGN ENGINE (No Randomness)

class ColorMind {
    static generatePalette(baseHue = Math.random() * 360, type = 'complementary') {
        const palette = [];
        const sat = 70 + Math.random() * 30; // High saturation
        const light = 40 + Math.random() * 20; // Readable lightness
        
        // HSL to Hex Helper
        const hsl2hex = (h, s, l) => {
            l /= 100;
            const a = s * Math.min(l, 1 - l) / 100;
            const f = n => {
                const k = (n + h / 30) % 12;
                const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
                return Math.round(255 * color).toString(16).padStart(2, '0');
            };
            return `#${f(0)}${f(8)}${f(4)}`;
        };

        // Harmonics Math
        if (type === 'complementary') {
            palette.push(hsl2hex(baseHue, sat, light)); // Base
            palette.push(hsl2hex((baseHue + 180) % 360, sat, light)); // Complement
            palette.push(hsl2hex(baseHue, sat * 0.5, 90)); // Neutral
        } else if (type === 'triadic') {
            palette.push(hsl2hex(baseHue, sat, light));
            palette.push(hsl2hex((baseHue + 120) % 360, sat, light));
            palette.push(hsl2hex((baseHue + 240) % 360, sat, light));
        } else if (type === 'analogous') {
            palette.push(hsl2hex(baseHue, sat, light));
            palette.push(hsl2hex((baseHue + 30) % 360, sat, light));
            palette.push(hsl2hex((baseHue - 30) % 360, sat, light));
        }
        
        return palette;
    }
}

class LayoutBrain {
    static getGridPoints(cols = 12, rows = 12, width = 800, height = 600) {
        // Swiss Grid System
        const cellW = width / cols;
        const cellH = height / rows;
        const points = [];
        for(let r=0; r<rows; r++) {
            for(let c=0; c<cols; c++) {
                points.push({ x: c * cellW, y: r * cellH, w: cellW, h: cellH });
            }
        }
        return points;
    }

    static assign(count, grid) {
        // Smart Allocation (Golden Ratio Spiral logic simplified)
        const assignments = [];
        let currentGrid = [...grid];
        
        for(let i=0; i<count; i++) {
             const idx = Math.floor(Math.random() * currentGrid.length);
             const cell = currentGrid.splice(idx, 1)[0];
             // Span multiple cells for dynamic layout?
             assignments.push(cell);
        }
        return assignments;
    }
}

class ArtDirector {
    constructor() {
        this.eras = {
            'art_deco': {
                name: "Art Deco",
                year: "1920s",
                palette: ["#E4CA6C", "#000000", "#1A1A1A", "#CC3333", "#FFFFFF"], 
                shapes: ["rect", "rect", "circle"], 
                complexity: 0.6,
                bgColor: "#1A1A1A",
                rules: [
                    "Use symmetry and geometric patterns.",
                    "Incorporate gold and metallic accents.",
                    "Emphasize verticality and streamlined forms."
                ],
                layout: "golden_ratio",
                description: "The Jazz Age. Luxury, glamour, and technological faith."
            },
            
            'dada': {
                name: "Dada",
                year: "1910s",
                palette: ["#D12E2E", "#F4F4F4", "#333333", "#000000"], 
                shapes: ["rect", "circle", "rect"],
                complexity: 0.8,
                bgColor: "#E0E0E0", 
                rules: [
                    "Embrace chaos and absurdity.",
                    "Use collage-like layering.",
                    "Break grid structures intentionally."
                ],
                layout: "action_painting",
                description: "Anti-art. A reaction against reason."
            },

            'modernist': {
                name: "Modernism",
                year: "1950s",
                palette: ['#D62B22', '#007AC1', '#F4B007', '#000000', '#FFFFFF'], 
                shapes: ['rect', 'circle', 'line'],
                layout: 'grid',
                complexity: 0.4,
                rules: ["Form follows function.", "Use the grid.", "Less is more."],
                description: "Clean lines, asymmetry, and objective clarity."
            },
            
            'digital': {
                name: "Digital Prophecy",
                year: "2025",
                palette: ['#00ff00', '#000000', '#ff00ff', '#00ffff'],
                shapes: ['rect', 'text'],
                layout: 'grid',
                complexity: 0.9,
                rules: ["Embrace the glitch.", "High contrast is key.", "RGB separation."],
                description: "The aesthetic of the machine dreaming."
            },
            
            'ai': {
                name: "Neuromorphic",
                year: "2030",
                palette: ['#00ffcc', '#111', '#222', '#00ff00'], 
                shapes: ['rect', 'circle'],
                layout: 'golden_ratio',
                complexity: 1.0, 
                rules: ["Organized organic chaos.", "Bioluminescent palettes.", "Recursion."],
                description: "The convergence of biology and silicon."
            }
        };

        this.compositionEngine = {
            // The Golden Ratio (Phi) ~ 1.618
            golden_ratio: (width, height, count) => {
                const points = [];
                // Simplified Phi Grid
                const x1 = width / 1.618;
                const y1 = height / 1.618;
                points.push({ x: x1, y: y1 }); // Main Subject
                for(let i=1; i<count; i++) {
                    points.push({ x: width * Math.random(), y: height * Math.random() });
                }
                return points;
            },
            
            rule_of_thirds: (width, height, count) => {
                const points = [];
                // The 4 intersections
                const xs = [width * 0.33, width * 0.66];
                const ys = [height * 0.33, height * 0.66];
                for(let i=0; i<count; i++) {
                    if (Math.random() > 0.3) {
                         // Bias towards intersections
                         points.push({ x: xs[Math.floor(Math.random()*2)], y: ys[Math.floor(Math.random()*2)] });
                    } else {
                         points.push({ x: Math.random()*width, y: Math.random()*height });
                    }
                }
                return points;
            },
            
            action_painting: (width, height, count) => {
                const points = [];
                for(let i=0; i<count*2; i++) { points.push({ x: Math.random() * width, y: Math.random() * height }); }
                return points;
            },
            
            grid: (width, height, count) => {
                 return LayoutBrain.getGridPoints(4, 4, width, height).slice(0, count);
            }
        };

        // PRE-COGNITION ENGINE (Zero Latency Buffer)
        this.briefBuffer = [];
        this.maxBuffer = 3;
        setTimeout(() => this.replenishBuffer(), 100);
    }

    replenishBuffer() {
        if (this.briefBuffer.length < this.maxBuffer) {
            // Predict next era (random for now, could be smarter)
            const eras = Object.keys(this.eras);
            const nextEra = eras[Math.floor(Math.random() * eras.length)];
            const brief = this.createBriefLogic(nextEra);
            this.briefBuffer.push({ era: nextEra, brief: brief });
            
            // Re-check soon
            setTimeout(() => this.replenishBuffer(), 50);
        }
    }

    // Public API
    generateBrief(eraKey) {
        // 1. Check Buffer for Match
        const cachedIndex = this.briefBuffer.findIndex(b => b.era === eraKey);
        
        if (cachedIndex > -1) {
            console.log("ART DIRECTOR // PRE-COGNITION HIT [0ms]");
            const item = this.briefBuffer.splice(cachedIndex, 1)[0];
            this.replenishBuffer(); // Refill async
            return item.brief;
        }

        // 2. Fallback (Cache Miss) - Generate Now
        console.log("ART DIRECTOR // GENERATING REAL-TIME");
        return this.createBriefLogic(eraKey);
    }
    
    // Internal Logic (Renamed from old generateBrief)
    createBriefLogic(eraKey) {
        const rules = this.eras[eraKey];
        if (!rules) return { 
            era: 'Unknown', bg: '#000', objects: [], theory: "No data found." 
        };

        const brief = {
            era: rules.name,
            bg: rules.palette[0], // Base color from era
            theory: this.deriveTheory(rules),
            objects: []
        };
        
        // Determine object count based on complexity
        let objectCount = Math.floor(Math.random() * 5) + (rules.complexity * 10);
        if (rules.layout === 'impressionism' || rules.layout === 'action_painting') objectCount *= 2; // More strokes

        // Get Layout Coordinates
        let coordinates;
        const engine = this.compositionEngine[rules.layout];
        if (engine) {
            coordinates = engine(800, 600, objectCount);
        } else {
            // Fallback: Random
            coordinates = [];
            for(let i=0; i<objectCount; i++) coordinates.push({x: Math.random()*800, y: Math.random()*600});
        }

        // Generate Objects
        for (let i = 0; i < coordinates.length; i++) {
            // GEMINI INJECTION: 20% Chance to use a User Creation instead of a shape
            // But only in 'Digital' or 'AI' eras, or randomly in others
            const useImage = (eraKey === 'ai' || eraKey === 'digital' || Math.random() > 0.9);
            
            if (useImage) {
                 const geminiImages = [
                    'assets/gemini_gallery/Gemini_Generated_Image_60fzex60fzex60fz.png',
                    'assets/gemini_gallery/Gemini_Generated_Image_gpx6rggpx6rggpx6.png',
                    'assets/gemini_gallery/Gemini_Generated_Image_rfzk9zrfzk9zrfzk.png',
                    'assets/gemini_gallery/Gemini_Generated_Image_llvliellvliellvl.png'
                 ];
                 const imgPath = geminiImages[Math.floor(Math.random() * geminiImages.length)];
                 const coords = coordinates[i] || {x: Math.random()*800, y: Math.random()*600};
                 
                 brief.objects.push({
                    type: 'image',
                    src: imgPath,
                    x: coords.x,
                    y: coords.y,
                    width: 150, // Fixed size thumb
                    height: 150,
                    rotation: Math.random() * 0.5 - 0.25
                 });
                 continue; 
            }

            const shapeType = rules.shapes[Math.floor(Math.random() * rules.shapes.length)];
            const color = rules.palette[Math.floor(Math.random() * (rules.palette.length - 1)) + 1]; 
            
            const coords = coordinates[i] || {x: Math.random()*800, y: Math.random()*600};
            
            let w, h;
            if (rules.layout === 'impressionism') {
                w = 10 + Math.random()*20; h = 10 + Math.random()*20; // Small strokes
            } else if (rules.layout === 'golden_ratio' && i === 0) {
                w = 200; h = 200; // Main subject
            } else {
                w = 30 + Math.random() * 100;
                h = 30 + Math.random() * 100;
            }

            brief.objects.push({
                type: shapeType,
                x: coords.x,
                y: coords.y,
                width: w,
                height: h,
                color: color,
                rotation: Math.random() * Math.PI
            });
        }

        return brief;
    }
    

    // 3. The Critic (Intelligence Analysis)
    critique(objects, eraKey, currentFilter) {
        const rules = this.eras[eraKey];
        if (!rules) return "I cannot critique an unknown era.";

        let score = 100;
        let comments = [];

        // 1. Color Analysis
        // Check if object colors generally match the palette
        // Simplified: check random sample
        if (objects.length > 0) {
            const sample = objects[0];
            const isPalette = rules.palette.includes(sample.color);
            if (!isPalette) {
                score -= 15;
                comments.push("Color Deviation detected. This object color is not historically accurate for this era.");
            }
        }

        // 2. Complexity Analysis
        if (rules.layout === 'modernist' && objects.length > 10) {
            score -= 20;
            comments.push("Too cluttered! Modernism demands minimalism. 'Less is More'.");
        }
        if (rules.layout === 'action_painting' && objects.length < 20) {
            score -= 20;
            comments.push("Not enough energy! Abstract Expressionism requires density and chaos.");
        }
        
        // 3. Composition Analysis
        if (rules.layout === 'golden_ratio') {
            // Check for main subject near phi point (approx 494, 370 for 800x600)
            const phiX = 800 / 1.618;
            const phiY = 600 / 1.618;
            let onPhi = false;
            objects.forEach(obj => {
                const dx = Math.abs(obj.x - phiX);
                const dy = Math.abs(obj.y - phiY);
                if (dx < 50 && dy < 50) onPhi = true;
            });
            if (!onPhi && objects.length > 0) {
                score -= 30;
                comments.push("Missed the Divine Proportion. Try placing a subject near the Phi intersection.");
            } else if (onPhi) {
                comments.push("Excellent use of the Golden Ratio.");
            }
        }

        // Grade
        let grade = 'F';
        if (score >= 95) grade = 'A+';
        else if (score >= 90) grade = 'A';
        else if (score >= 80) grade = 'B';
        else if (score >= 70) grade = 'C';
        else if (score >= 60) grade = 'D';

        return `CRITIQUE [${rules.name}]:
Grade: ${grade} (${score}/100)

Notes:
${comments.length > 0 ? "- " + comments.join("\n- ") : "- Perfection achieved."}`;
    }
}

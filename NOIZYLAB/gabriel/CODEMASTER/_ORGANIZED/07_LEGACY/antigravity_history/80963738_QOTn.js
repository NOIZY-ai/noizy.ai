// art-director.js
// The "Model" - Advanced Art History Knowledge & Composition Engine
// Doctorate Level Upgrade

class ArtDirector {
    constructor() {
        // 1. The Knowledge Base (Rules & Constraints)
        this.eras = {
            // --- Graphic Design History ---
            'origins': {
                name: 'Origins',
                palette: ['#e6dcc8', '#3b2f2f', '#c9a959', '#8a2be2'],
                shapes: ['rect', 'circle'],
                complexity: 0.3,
                layout: 'center'
            },
            'printing': {
                name: 'The Press',
                palette: ['#f0f0f0', '#111111', '#000000', '#333333'],
                shapes: ['rect'],
                complexity: 0.6,
                layout: 'grid'
            },
            'modernist': {
                name: 'Modernist',
                palette: ['#f0f0f0', '#d12e2e', '#1e3888', '#f5a623'],
                shapes: ['rect', 'circle', 'triangle'],
                complexity: 0.5,
                layout: 'asymmetrical'
            },
            'digital': {
                name: 'Digital',
                palette: ['#000022', '#00ff41', '#ff00ff', '#00ffff'],
                shapes: ['rect'],
                complexity: 0.9,
                layout: 'random'
            },
            'ai': {
                name: 'AI Revolution',
                palette: ['#050510', '#8a2be2', '#00ffcc'],
                shapes: ['circle', 'triangle'],
                complexity: 0.8,
                layout: 'organic'
            },

            // --- Art History Doctorate Expansion ---
            'renaissance': {
                name: 'Renaissance',
                palette: ['#e3dac9', '#8a5a44', '#b59453', '#2d4059'], // Earth, Gold, Lapis Lazuli
                shapes: ['rect', 'triangle'], // Representing architecture/pyramidal comp
                complexity: 0.4,
                layout: 'golden_ratio' // The Divine Proportion
            },
            'impressionism': {
                name: 'Impressionism',
                palette: ['#b4e7ce', '#e2f0cb', '#f7d9c4', '#c9c6f2'], // Pastels / Light
                shapes: ['circle'], // Dots/Strokes
                complexity: 0.9, // Many small strokes
                layout: 'rule_of_thirds' 
            },
            'surrealism': {
                name: 'Surrealism',
                palette: ['#a0a0a0', '#ff4400', '#0066ff', '#000000'], // High contrast, dreamlike
                shapes: ['circle', 'rect', 'triangle'], 
                complexity: 0.3, // Sparse but weird
                layout: 'juxtaposition' // Far apart / Floating
            },
            'abstract_expressionism': {
                name: 'Abstract Expressionism',
                palette: ['#ffffff', '#000000', '#ff0000', '#ffff00', '#0000ff'], // Pollock/Mondrian
                shapes: ['rect', 'circle'],
                complexity: 1.0, // Maximum Chaos
                layout: 'action_painting'
            }
        };

        this.compositionEngine = {
            // The Golden Ratio (Phi) ~ 1.618
            golden_ratio: (width, height, count) => {
                const points = [];
                // Simplified Phi Grid: Focus on the spiral centers
                const x1 = width / 1.618;
                const y1 = height / 1.618;
                
                // Main Subject at "The Eye"
                points.push({ x: x1, y: y1 });
                
                // Secondary points spiral out
                for(let i=1; i<count; i++) {
                    points.push({
                        x: width * Math.random(),
                        y: height * Math.random() // Fallback to balanced distribution
                    });
                }
                return points;
            },
            
            rule_of_thirds: (width, height, count) => {
                const points = [];
                // The 4 intersections
                const xs = [width * 0.33, width * 0.66];
                const ys = [height * 0.33, height * 0.66];
                
                for(let i=0; i<count; i++) {
                    // Bias heavily towards intersections
                    const useIntersection = Math.random() > 0.3;
                    if (useIntersection) {
                        points.push({
                            x: xs[Math.floor(Math.random()*2)] + (Math.random()*40-20),
                            y: ys[Math.floor(Math.random()*2)] + (Math.random()*40-20)
                        });
                    } else {
                        points.push({ x: Math.random()*width, y: Math.random()*height });
                    }
                }
                return points;
            },
            
            action_painting: (width, height, count) => {
                const points = [];
                // Pure chaos, but clustered interaction
                for(let i=0; i<count*2; i++) { // Increase count for action
                    points.push({
                        x: Math.random() * width,
                        y: Math.random() * height
                    });
                }
                return points;
            },
            
            grid: (width, height, count) => {
                 const points = [];
                 const cols = 4;
                 const rows = 4;
                 for(let i=0; i<count; i++) {
                     const c = i % cols;
                     const r = Math.floor(i / cols) % rows;
                     points.push({
                         x: 100 + (c * 150),
                         y: 100 + (r * 100)
                     });
                 }
                 return points;
            }
        };
    }

    // 2. The Worker (Procedural Generation)
    generateBrief(eraKey) {
        const rules = this.eras[eraKey];
        if (!rules) return { 
            era: 'Unknown', bg: '#000', objects: [], theory: "No data found." 
        };

        const brief = {
            era: rules.name,
            bg: rules.palette[0],
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

// art-director.js
// The "Model" - Systematized Design Knowledge

class ArtDirector {
    constructor() {
        // 1. The Knowledge Base (Rules & Constraints)
        this.eras = {
            'origins': {
                name: 'Origins',
                palette: ['#e6dcc8', '#3b2f2f', '#c9a959', '#8a2be2'], // Parchment, Ink, Gold, (Pop accent)
                shapes: ['rect', 'circle'], // Basic
                complexity: 0.3, // Simple/Sparse
                distribution: 'center' // Often centered
            },
            'printing': {
                name: 'The Press',
                palette: ['#f0f0f0', '#111111', '#000000', '#333333'],
                shapes: ['rect'], // Blocky
                complexity: 0.6,
                distribution: 'grid' // Structured
            },
            'modernist': {
                name: 'Modernist',
                palette: ['#f0f0f0', '#d12e2e', '#1e3888', '#f5a623'], // Bauhaus Primary
                shapes: ['rect', 'circle', 'triangle'], 
                complexity: 0.5, // Balanced / Minimal
                distribution: 'asymmetrical' // Dynamic balance
            },
            'digital': {
                name: 'Digital',
                palette: ['#000022', '#00ff41', '#ff00ff', '#00ffff'], // Neon/Cyber
                shapes: ['rect'],
                complexity: 0.9, // Chaotic
                distribution: 'random'
            },
            'ai': {
                name: 'AI Revolution',
                palette: ['#050510', '#8a2be2', '#ff00aa', '#00ffcc'],
                shapes: ['circle', 'triangle'], // Fluid/Organic approx
                complexity: 0.8,
                distribution: 'random'
            }
        };
    }

    // 2. The Worker (Procedural Generation)
    generateBrief(eraKey) {
        const rules = this.eras[eraKey];
        if (!rules) return null;

        const brief = {
            era: rules.name,
            bg: rules.palette[0],
            objects: []
        };

        // Determine object count based on complexity
        const objectCount = Math.floor(Math.random() * 5) + (rules.complexity * 10); 

        for (let i = 0; i < objectCount; i++) {
            const shapeType = rules.shapes[Math.floor(Math.random() * rules.shapes.length)];
            const color = rules.palette[Math.floor(Math.random() * (rules.palette.length - 1)) + 1]; // Skip BG color
            
            let x, y, width, height;

            // Layout Engine
            if (rules.distribution === 'grid') {
                // simple 4x4 grid slots
                const slotX = Math.floor(Math.random() * 4);
                const slotY = Math.floor(Math.random() * 4);
                x = 100 + (slotX * 150);
                y = 100 + (slotY * 100);
                width = 100;
                height = 80;
            } else if (rules.distribution === 'center') {
                x = 400 + (Math.random() * 200 - 100);
                y = 300 + (Math.random() * 200 - 100);
                width = 50 + Math.random() * 100;
                height = 50 + Math.random() * 100;
            } else {
                // Random / Asymmetrical
                x = Math.random() * 800;
                y = Math.random() * 600;
                width = 20 + Math.random() * 200;
                height = 20 + Math.random() * 200;
            }

            brief.objects.push({
                type: shapeType,
                x: x,
                y: y,
                width: width,
                height: height,
                color: color,
                rotation: (rules.distribution === 'random' || rules.distribution === 'asymmetrical') ? Math.random() * Math.PI : 0
            });
        }

        return brief;
    }
}
